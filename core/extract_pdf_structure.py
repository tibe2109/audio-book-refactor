#!/usr/bin/env python3
# ==============================================================================
# Step 01: Universal PDF & Course Structure Extractor
# Skill: arf_01_pdf_structure_extractor
# Generates: raw_original.txt and .session_manifest.json
# ==============================================================================
import os
import sys
import re
import json
import argparse
import datetime
import pdfplumber
import zipfile
import xml.etree.ElementTree as ET

# ------------------------------------------------------------------------------
# Noise and Header/Footer Filtering
# ------------------------------------------------------------------------------
def is_noise_line(line):
    line_str = line.strip()
    if not line_str:
        return True
    
    # PMI / Publisher licensing watermark
    if "PMI Member benefit licensed to:" in line_str or "Not for distribution, sale, or reproduction" in line_str:
        return True
    
    # Tam Quoc / ThuVienSach watermarks & links
    if "thuviensach.vn" in line_str.lower() or "downloadsach.com" in line_str.lower() or "caphebuoitoi" in line_str.lower():
        return True
    if line_str in ("tv", "https://thuviensach.vn", "http://downloadsach.com/") or line_str.startswith("http://") or line_str.startswith("https://"):
        return True
    
    # Indesign print artifacts (e.g. PPGGPPGG__EENN..iinnddbb 11 3300//1111//2222...)
    if re.search(r'PPGGPPGG__EENN', line_str, re.IGNORECASE) or re.search(r'\.iinnddbb', line_str, re.IGNORECASE):
        return True
        
    # Never Eat Alone running headers / footers
    if re.match(r'^\d+\s+Never Eat Alone$', line_str, re.IGNORECASE) or re.match(r'^Never Eat Alone\s+\d+$', line_str, re.IGNORECASE):
        return True
    if re.search(r'\s+\d+$', line_str) and len(line_str) < 80:
        nea_keywords = [
            'Member of the Club', "Don't Keep Score", "What's Your Mission", 'Build It Before You Need It',
            'The Genius of Audacity', 'The Networking Jerk', 'Do Your Homework', 'Take Names',
            'Warming the Cold Call', 'Managing the Gatekeeper', 'Never Eat Alone', 'Share Your Passions',
            'Follow Up or Fail', 'Conference Commando', 'Connecting with Connectors', 'Expanding Your Circle',
            'The Art of Small Talk', 'Health, Wealth, and Children', 'Social Arbitrage', 'Pinging',
            'Find Anchor Tenants', 'Be Interesting', 'Build Your Brand', 'Broadcast Your Brand',
            'The Write Stuff', 'Getting Close to Power', 'Build It and They Will Come', 'Never Give in to Hubris',
            'Find Mentors', 'Balance Is B.S.', 'Connected Age', 'Katharine Graham', 'Vernon Jordan',
            'Bill Clinton', 'Paul Revere', 'Dale Carnegie', 'Dalai Lama', 'Benjamin Franklin', 'Eleanor Roosevelt'
        ]
        if any(k.lower() in line_str.lower() for k in nea_keywords):
            return True

    # Standalone running header / footer page numbers
    if re.match(r'^\d+\s+Process Groups:\s+A Practice Guide$', line_str, re.IGNORECASE):
        return True
    if re.match(r'^Process Groups:\s+A Practice Guide\s+\d+$', line_str, re.IGNORECASE):
        return True
    if re.match(r'^(Introduction|The Project Environment|Role of the Project Manager|Initiating Process Group|Planning Process Group|Executing Process Group|Monitoring and Controlling Process Group|Closing Process Group|Inputs and Outputs|Tools and Techniques|References|Glossary)\s+\d+$', line_str, re.IGNORECASE):
        return True
    if re.match(r'^\d+\s+(Introduction|The Project Environment|Role of the Project Manager|Initiating Process Group|Planning Process Group|Executing Process Group|Monitoring and Controlling Process Group|Closing Process Group|Inputs and Outputs|Tools and Techniques|References|Glossary)$', line_str, re.IGNORECASE):
        return True
    if re.match(r'^\d+$', line_str):
        return True

    return False

# Cache dictionary words for ligature healing
_DICT_WORDS = None

def get_dict_words():
    global _DICT_WORDS
    if _DICT_WORDS is None:
        words = set()
        words_file = '/usr/share/dict/words'
        if os.path.exists(words_file):
            try:
                with open(words_file, 'r', encoding='utf-8', errors='ignore') as f:
                    words = set(w.strip().lower() for w in f if w.strip())
            except Exception:
                pass
        words.update(['buffett', 'facebook', 'introvert', 'extrovert', 'introverts', 'extroverts', 
                      'introversion', 'extroversion', 'temperament', 'carnegie'])
        _DICT_WORDS = words
    return _DICT_WORDS

def heal_ligatures(text):
    """Heals broken ligatures encoded as null byte in PDFs (e.g. o\\x00cially -> officially)."""
    if '\x00' not in text:
        return text
    
    dict_words = get_dict_words()
    candidates = ['fi', 'fl', 'ff', 'ffi', 'ffl']
    
    def replace_word(match):
        token = match.group(0)
        if '\x00' not in token:
            return token
        m = re.match(r'^([^a-zA-Z0-9\x00]*)([a-zA-Z0-9\x00]+)([^a-zA-Z0-9\x00]*)$', token)
        if not m:
            return token.replace('\x00', 'fi')
        prefix, core, suffix = m.groups()
        is_cap = core and core[0].isupper()
        is_all_cap = core and core.isupper()
        core_lower = core.lower()
        for cand in candidates:
            test = core_lower.replace('\x00', cand)
            if test in dict_words:
                if is_all_cap:
                    res = test.upper()
                elif is_cap:
                    res = test.capitalize()
                else:
                    res = test
                return f"{prefix}{res}{suffix}"
        return token.replace('\x00', 'fi')
        
    return re.sub(r'\S+', replace_word, text)

def clean_extracted_text(text):
    text = heal_ligatures(text)
    # Heal Vietnamese font encoding artifacts (ü/Ü -> ũ/Ũ)
    text = text.replace('ü', 'ũ').replace('Ü', 'Ũ')
    
    # Heal corrupted OCR characters in Vietnamese
    corrupted_i_map = {
        'thâït': 'thật', 'đêï': 'đệ', 'vôïi': 'vội', 'vộïi': 'vội',
        'Lôï': 'Lỗ', 'văïc': 'vặc', 'trâïn': 'trận', 'Lacï': 'Lạc',
        'laiï': 'lại', 'đếnï': 'đến', 'giốngï': 'giống',
        'ba0øn': 'bàn', 'trạân': 'trận', 'đọâi': 'đội', 'tọâi': 'tội',
        'Dạân': 'Dân', 'nọâi': 'nội', 'quạân': 'quận', 'cạâu': 'cậu',
        'Lọâ': 'Lộ', 'cóđược': 'có được',
        'trơ ûvề': 'trở về', 'Tửû': 'Tử', 'cỏû': 'cỏ', 'quăûng': 'quăng',
        'làø': 'là', 'Tư øThịnh': 'Từ Thịnh', 'Mã Đằøng': 'Mã Đằng',
        'Qøuách': 'Quách', 'thơiø': 'thời', 'phảøi': 'phải',
        'thơ đếnï': 'thợ đến'
    }
    for bad_w, good_w in corrupted_i_map.items():
        text = text.replace(bad_w, good_w)
    text = text.replace('ï', '').replace('û', '').replace('ø', '')

    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        if is_noise_line(line):
            continue
        cleaned_lines.append(line)
        
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Heal hyphenated words broken across line endings (e.g. "organi-\nzation" -> "organization")
    cleaned_text = re.sub(r'(\b[a-zA-Zà-ỹÀ-Ỹ]+)-\n\s*([a-zA-Zà-ỹÀ-Ỹ]+\b)', r'\1\2', cleaned_text)
    
    # Heal Drop-Cap splits: single capital letter on a line before word (e.g. "T\nrong" -> "Trong", "P\nroject" -> "Project")
    cleaned_text = re.sub(r'(\n|^)([A-ZÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ])\n([a-zàáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ])', r'\1\2\3', cleaned_text)
    
    # Normalize multiple blank lines
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    return cleaned_text.strip()

# ------------------------------------------------------------------------------
# Modular Course Text Extraction Helpers (Transcripts, PDF Readings, DOCX)
# ------------------------------------------------------------------------------
def clean_transcript_text(text):
    """Cleans video transcripts, removing [MUSIC]/tags and reconstructing natural paragraphs."""
    # Remove bracket tags like [MUSIC], [APPLAUSE], [SOUND]
    text = re.sub(r'\[[A-Z\s]+\]', '', text)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    full_str = ' '.join(lines)
    full_str = re.sub(r'\s+', ' ', full_str).strip()
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', full_str)
    paragraphs = []
    curr = []
    curr_len = 0
    for s in sentences:
        curr.append(s)
        curr_len += len(s)
        # Form cohesive paragraphs of ~3-4 sentences (~380+ characters)
        if curr_len >= 380 and len(curr) >= 3:
            paragraphs.append(' '.join(curr))
            curr = []
            curr_len = 0
    if curr:
        paragraphs.append(' '.join(curr))
    return '\n\n'.join(paragraphs)

def extract_pdf_clean(pdf_path):
    """Extracts text from reading PDFs with drop-cap healing and paragraph reconstruction."""
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = []
        for p in pdf.pages:
            t = p.extract_text() or ''
            pages_text.append(t)
    
    raw = '\n'.join(pages_text)
    # Heal Drop-Cap
    raw = re.sub(r'(?:\n|^)([A-ZÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ])\n([a-zàáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ])', r'\1\2', raw)
    lines = raw.split('\n')
    cleaned = []
    for l in lines:
        l_str = l.strip()
        if not l_str:
            continue
        cleaned.append(l_str)
        
    paras = []
    curr = []
    for l in cleaned:
        if l.startswith('●') or l.startswith('-') or l.startswith('•'):
            if curr:
                paras.append(' '.join(curr))
                curr = []
            paras.append(l)
        elif len(l) < 55 and not l.endswith(('.', ',', ';', ':')):
            # Heading candidate
            if curr:
                paras.append(' '.join(curr))
                curr = []
            paras.append(f"### {l}")
        else:
            curr.append(l)
            if l.endswith(('.', '!', '?')) and len(' '.join(curr)) > 300:
                paras.append(' '.join(curr))
                curr = []
    if curr:
        paras.append(' '.join(curr))
    return '\n\n'.join(paras)

def extract_docx_glossary(docx_path):
    """Extracts terms and definitions from DOCX without third-party python-docx dependency."""
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    entries = []
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        t = ''.join([node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]).strip()
        if t:
            entries.append(t)
            
    formatted = []
    for e in entries:
        if len(e) == 1 and e.isalpha():
            formatted.append(f"\n### Letter {e}\n")
        else:
            formatted.append(f"{e}\n")
    return '\n'.join(formatted).strip()

def resolve_source_file(source_dir, target_name):
    """Resolves file path tolerating stray newlines or whitespaces in filenames."""
    disk_files = os.listdir(source_dir)
    target_clean = re.sub(r'[\r\n\t]+', '', target_name).strip()
    for f in disk_files:
        f_clean = re.sub(r'[\r\n\t]+', '', f).strip()
        if f_clean == target_clean:
            return os.path.join(source_dir, f)
    raise FileNotFoundError(f"Cannot find '{target_name}' in '{source_dir}'")

# ------------------------------------------------------------------------------
# Extraction for Google Project Management (Coursera) Course Datasets
# ------------------------------------------------------------------------------
COURSERA_COURSE_1_CONFIG = {
    "title": "Google Project Management Certificate - Course 1: Foundations of Project Management",
    "slug": "Google-Project-Management-Coursera",
    "author": "Google Career Certificates",
    "modules": [
        {
            "index": 0,
            "folder": "01-Embarking-on-a-Career-in-Project-Management",
            "title": "Module 1: Embarking on a Career in Project Management",
            "files": [
                ("What is project management.txt", "What Is Project Management?"),
                ("What does a project manager do.txt", "What Does a Project Manager Do?"),
                ("Transferable project management skills.txt", "Transferable Project Management Skills"),
                ("Path to becoming a project manager.txt", "Path to Becoming a Project Manager"),
                ("JuAnne: Path to becoming a project manager.txt", "Path to Becoming a Project Manager: JuAnne's Story"),
                ("Rachel: My journey to becoming a project manager.txt", "My Journey to Becoming a Project Manager: Rachel's Story"),
                ("Finding the perfect role.txt", "Finding the Perfect Project Management Role"),
                ("From certificate to career success.txt", "From Certificate to Career Success"),
                ("Review: Embarking on a career in project management.txt", "Review: Embarking on a Career in Project Management")
            ]
        },
        {
            "index": 1,
            "folder": "02-Becoming-an-Effective-Project-Manager",
            "title": "Module 2: Becoming an Effective Project Manager",
            "files": [
                ("Introduction: Becoming an effective project manager.txt", "Introduction: Becoming an Effective Project Manager"),
                ("The value of a project manager.txt", "The Value of a Project Manager"),
                ("How project managers impact organizations.pdf", "Reading: How Project Managers Impact Organizations"),
                ("Key project manager roles and responsibilities.txt", "Key Project Manager Roles and Responsibilities"),
                ("A project manager’s role within a team.txt", "A Project Manager's Role Within a Team"),
                ("The core skills of a project manager.txt", "The Core Skills of a Project Manager"),
                ("Leadership and team dynamics.txt", "Leadership and Team Dynamics"),
                ("Working with cross-functional teams.pdf", "Reading: Working with Cross-Functional Teams"),
                ("Elita: A day in the life of a project manager.txt", "A Day in the Life of a Project Manager: Elita's Story"),
                ("Ellen: Traits of a successful project manager.txt", "Traits of a Successful Project Manager: Ellen's Story"),
                ("Amar: Project management in life and in the organization.txt", "Project Management in Life and in the Organization: Amar's Story"),
                ("Lan: Working in a Project Management Office.txt", "Working in a Project Management Office: Lan's Story"),
                ("Gilbert: Project management skills in my role.txt", "Project Management Skills in My Role: Gilbert's Story")
            ]
        },
        {
            "index": 2,
            "folder": "03-Project-Life-Cycle-and-Methodologies",
            "title": "Module 3: The Project Management Life Cycle and Methodologies",
            "files": [
                ("Introduction: The project management life cycle and methodologies.txt", "Introduction: The Project Management Life Cycle and Methodologies"),
                ("Exploring the phases of the project life cycle.txt", "Exploring the Phases of the Project Life Cycle"),
                ("Phases in action: Initiating and planning.txt", "Phases in Action: Initiating and Planning"),
                ("Phases in action: Executing and closing.txt", "Phases in Action: Executing and Closing"),
                ("Introduction to project management methodologies.txt", "Introduction to Project Management Methodologies"),
                ("Overview of Waterfall and Agile.txt", "Overview of Waterfall and Agile"),
                ("Introduction to Lean and Six Sigma.txt", "Introduction to Lean and Six Sigma")
            ]
        },
        {
            "index": 3,
            "folder": "04-Organizational-Structure-and-Culture",
            "title": "Module 4: Organizational Structure and Culture",
            "files": [
                ("Introduction: Organizational structure and culture.txt", "Introduction: Organizational Structure and Culture"),
                ("Overview of Classic and Matrix structures.txt", "Overview of Classic and Matrix Structures"),
                ("How organizational structure impacts project management.txt", "How Organizational Structure Impacts Project Management"),
                ("Introduction to organizational culture.txt", "Introduction to Organizational Culture"),
                ("Introduction to change management.txt", "Introduction to Change Management"),
                ("Participating in change management.txt", "Participating in Change Management")
            ]
        },
        {
            "index": 4,
            "folder": "05-AI-in-Project-Management",
            "title": "Special Module: Driving Impact with AI in Project Management",
            "files": [
                ("Boost your project management skills with AI.txt", "Boost Your Project Management Skills with AI"),
                ("Ben: Driving impact with AI in the workplace.txt", "Driving Impact with AI in the Workplace: Ben's Story")
            ]
        },
        {
            "index": 5,
            "folder": "06-Glossary-and-Definitions",
            "title": "Course 1 Glossary: Project Management Terms and Definitions",
            "files": [
                ("y2jk8oiXSduo5PKIlynbGg_897575212230468c87e9dcc31989f2f1_Course-1-Glossary-_-PM-Terms-and-Definitions.docx", "Course 1 Glossary: Project Management Terms and Definitions")
            ]
        }
    ]
}

COURSERA_COURSE_2_CONFIG = {
    "title": "Google Project Management Certificate - Course 2: Project Initiation: Starting a Successful Project",
    "slug": "Project-Initiation-Starting-a-Successful-Project",
    "author": "Google Career Certificates",
    "modules": [
        {
            "index": 0,
            "folder": "01-Fundamentals-of-Project-Initiation",
            "title": "Module 1: The Fundamentals of Project Initiation",
            "files": [
                ("Introduction to Course 2.txt", "Introduction to Course 2"),
                ("Why is project initiation essential.txt", "Why Is Project Initiation Essential?"),
                ("Key components of project initiation.txt", "Key Components of Project Initiation"),
                ("Afsheen: Listening to learn.txt", "Listening to Learn: Afsheen's Story"),
                ("Certificate completers: Staying motivated in the program.txt", "Staying Motivated in the Program"),
                ("Review: The fundamentals of project initiation.txt", "Review: The Fundamentals of Project Initiation")
            ]
        },
        {
            "index": 1,
            "folder": "02-Project-Goals-Scope-and-Success-Criteria",
            "title": "Module 2: Defining Project Goals, Scope, and Success Criteria",
            "files": [
                ("Introduction: Defining project goals, scope, and success criteria.txt", "Introduction: Defining Project Goals, Scope, and Success Criteria"),
                ("Determining project goals and deliverables.txt", "Determining Project Goals and Deliverables"),
                ("How to set SMART goals.txt", "How to Set SMART Goals"),
                ("Introduction to OKRs.txt", "Introduction to Objectives and Key Results (OKRs)"),
                ("Determining a project's scope.txt", "Determining a Project's Scope"),
                ("Managing changes to a project's scope.txt", "Managing Changes to a Project's Scope"),
                ("Monitoring and maintaining a project's scope.txt", "Monitoring and Maintaining a Project's Scope"),
                ("Torie: The importance of staying within scope.txt", "The Importance of Staying Within Scope: Torie's Story"),
                ("Defining success criteria.txt", "Defining Success Criteria and Metrics"),
                ("Launching and landing a project.txt", "Launching and Landing a Project"),
                ("Review: Defining project goals, scope, and success criteria.txt", "Review: Defining Project Goals, Scope, and Success Criteria")
            ]
        },
        {
            "index": 2,
            "folder": "03-Working-Effectively-with-Stakeholders",
            "title": "Module 3: Working Effectively with Stakeholders",
            "files": [
                ("Introduction: Working effectively with stakeholders.txt", "Introduction: Working Effectively with Stakeholders"),
                ("Defining project roles.txt", "Defining Project Roles and Responsibilities"),
                ("Choosing a project team.txt", "Choosing a Project Team"),
                ("John: The importance of a project team.txt", "The Importance of a Project Team: John's Story"),
                ("Completing a stakeholder analysis.txt", "Completing a Stakeholder Analysis"),
                ("Elements of a RACI chart.txt", "Elements of a RACI Chart"),
                ("Review: Working effectively with stakeholders.txt", "Review: Working Effectively with Stakeholders")
            ]
        },
        {
            "index": 3,
            "folder": "04-Resources-Tools-and-Project-Documentation",
            "title": "Module 4: Utilizing Resources, Documentation, and Tools for Project Success",
            "files": [
                ("Introduction: Utilizing resources and tools for project success.txt", "Introduction: Utilizing Resources and Tools for Project Success"),
                ("Essential project resources.txt", "Essential Project Resources"),
                ("The value of project documentation.txt", "The Value of Project Documentation"),
                ("Project proposals and charters 101.txt", "Project Proposals and Charters 101"),
                ("Developing a project charter.txt", "Developing a Project Charter"),
                ("Utilizing tools for effective project management.txt", "Utilizing Tools for Effective Project Management"),
                ("Exploring types of project management tools.txt", "Exploring Types of Project Management Tools"),
                ("Common project management tools.txt", "Common Project Management Tools"),
                ("Amar: Tools are our best friends.txt", "Tools Are Our Best Friends: Amar's Story"),
                ("Accessibility for project managers.txt", "Accessibility for Project Managers: Holly's Insights"),
                ("Course review: Project Initiation: Starting a successful project.txt", "Course Review: Project Initiation: Starting a Successful Project")
            ]
        },
        {
            "index": 4,
            "folder": "05-AI-in-Project-Initiation",
            "title": "Special Module: Driving Impact with AI in Project Initiation",
            "files": [
                ("Use AI to create a project charter.txt", "Using AI to Create a Project Charter")
            ]
        },
        {
            "index": 5,
            "folder": "06-Glossary-and-Definitions",
            "title": "Course 2 Glossary: Project Management Terms and Definitions",
            "files": [
                ("Dxi8fFH5TAyYvHxR-awMLw_8efe21fb3fd24ccf8f26314be69ab0f1_Course-2-Glossary-_-PM-Terms-and-Definitions.docx", "Course 2 Glossary: Project Management Terms and Definitions")
            ]
        }
    ]
}

COURSERA_COURSE_3_CONFIG = {
    "title": "Google Project Management Certificate - Course 3: Project Planning: Putting It All Together",
    "slug": "Project-Planning-Putting-It-All-Together",
    "author": "Google Career Certificates",
    "modules": [
        {
            "index": 0,
            "folder": "01-Beginning-the-Planning-Phase",
            "title": "Module 1: Beginning the Planning Phase",
            "files": [
                ("Introduction to Course 3.txt", "Introduction to Course 3"),
                ("The benefits of project planning.txt", "The Benefits of Project Planning"),
                ("Launching the planning phase.txt", "Launching the Planning Phase"),
                ("Facilitating a project kick-off meeting.txt", "Facilitating a Project Kick-off Meeting"),
                ("Understanding tasks and milestones.txt", "Understanding Tasks and Milestones"),
                ("The importance of setting milestones.txt", "The Importance of Setting Milestones"),
                ("How to set milestones.txt", "How to Set Milestones"),
                ("Creating a work breakdown structure.txt", "Creating a Work Breakdown Structure"),
                ("Stanton: Managing my first project.txt", "Managing My First Project: Stanton's Story"),
                ("Clennita: How planning creates a sense of team.txt", "How Planning Creates a Sense of Team: Clennita's Story"),
                ("Review: Beginning the planning phase.txt", "Review: Beginning the Planning Phase")
            ]
        },
        {
            "index": 1,
            "folder": "02-Building-a-Project-Plan",
            "title": "Module 2: Building a Project Plan",
            "files": [
                ("Introduction: Building a project plan.txt", "Introduction: Building a Project Plan"),
                ("Components of a project plan.txt", "Components of a Project Plan"),
                ("Making realistic time estimates.txt", "Making Realistic Time Estimates"),
                ("Capacity planning and the critical path.txt", "Capacity Planning and the Critical Path"),
                ("Getting accurate time estimates from your team.txt", "Getting Accurate Time Estimates from Your Team"),
                ("Developing a project schedule.txt", "Developing a Project Schedule"),
                ("Angel: The value of interpersonal skills in time estimation.txt", "The Value of Interpersonal Skills in Time Estimation: Angel's Story"),
                ("Project plan best practices.txt", "Project Plan Best Practices"),
                ("Review: Building a project plan.txt", "Review: Building a Project Plan")
            ]
        },
        {
            "index": 2,
            "folder": "03-Managing-Budgeting-and-Procurement",
            "title": "Module 3: Managing Budgeting and Procurement",
            "files": [
                ("Introduction: Managing budgeting and procurement.txt", "Introduction: Managing Budgeting and Procurement"),
                ("The importance of budget setting.txt", "The Importance of Budget Setting"),
                ("Key components of a project budget.txt", "Key Components of a Project Budget"),
                ("Creating a project budget.txt", "Creating a Project Budget"),
                ("Maintaining a project budget.txt", "Maintaining a Project Budget"),
                ("Understanding procurement.txt", "Understanding Procurement"),
                ("The procurement process.txt", "The Procurement Process"),
                ("Obtaining procurement support.txt", "Obtaining Procurement Support"),
                ("Common procurement documentation.txt", "Common Procurement Documentation"),
                ("Creating a Statement of Work.txt", "Creating a Statement of Work"),
                ("Ethics in the procurement process.txt", "Ethics in the Procurement Process"),
                ("Review: Managing budgeting and procurement.txt", "Review: Managing Budgeting and Procurement")
            ]
        },
        {
            "index": 3,
            "folder": "04-Managing-Risks-Effectively",
            "title": "Module 4: Managing Risks Effectively",
            "files": [
                ("Introduction: Managing risks effectively.txt", "Introduction: Managing Risks Effectively"),
                ("The importance of risk management.txt", "The Importance of Risk Management"),
                ("Types of risk.txt", "Types of Risk"),
                ("Tools to help identify risks.txt", "Tools to Help Identify Risks"),
                ("Identify potential project risks with gen AI.txt", "Identify Potential Project Risks with Generative AI"),
                ("Building a risk management plan.txt", "Building a Risk Management Plan"),
                ("Risk mitigation strategies.txt", "Risk Mitigation Strategies"),
                ("Communicating risks to stakeholders.txt", "Communicating Risks to Stakeholders"),
                ("Aji: Risk management at Google.txt", "Risk Management at Google: Aji's Story"),
                ("Review: Managing risks effectively.txt", "Review: Managing Risks Effectively")
            ]
        },
        {
            "index": 4,
            "folder": "05-Organizing-Communication-and-Documentation",
            "title": "Module 5: Organizing Communication and Documentation",
            "files": [
                ("Introduction: Organizing communication and documentation.txt", "Introduction: Organizing Communication and Documentation"),
                ("Why communication is critical.txt", "Why Communication Is Critical"),
                ("Starting a communication plan.txt", "Starting a Communication Plan"),
                ("Developing a communication plan.txt", "Developing a Communication Plan"),
                ("The value of project documentation.txt", "The Value of Project Documentation"),
                ("Organizing project documentation.txt", "Organizing Project Documentation"),
                ("Dan: The importance of project documentation.txt", "The Importance of Project Documentation: Dan's Story"),
                ("Chris: Organizing artifacts for a job interview.txt", "Organizing Artifacts for a Job Interview: Chris's Story"),
                ("Course review: Project planning: Putting it all together.txt", "Course Review: Project Planning: Putting It All Together")
            ]
        },
        {
            "index": 5,
            "folder": "06-Glossary-and-Definitions",
            "title": "Course 3 Glossary: Project Management Terms and Definitions",
            "files": [
                ("36-rxVmKTd2vq8VZim3dYA_28f0335399a346b09fce66dce795d7f1_Course-3-Glossary-_-PM-Terms-and-Definitions.docx", "Course 3 Glossary: Project Management Terms and Definitions")
            ]
        }
    ]
}

def detect_coursera_course(source_dir):
    """Auto-detects Coursera Course configuration based on directory files or name."""
    files = set(os.listdir(source_dir))
    
    # Check for modular text courses (e.g. 01 - ...txt)
    numbered_txts = sorted([f for f in files if re.match(r'^\d+\s*-\s*.*\.txt$', f)])
    if numbered_txts and len(numbered_txts) >= 3:
        modules = []
        for idx, f_name in enumerate(numbered_txts):
            m = re.match(r'^(\d+)\s*-\s*(.*?)\.txt$', f_name)
            num_str = m.group(1)
            raw_title = m.group(2).strip()
            safe_slug = re.sub(r'[^a-zA-Z0-9]+', '-', raw_title).strip('-')
            folder_name = f"{int(num_str):02d}-{safe_slug}"
            modules.append({
                "index": idx,
                "folder": folder_name,
                "title": f"Chapter {int(num_str)}: {raw_title}",
                "files": [(f_name, raw_title)]
            })
        base_name = os.path.basename(source_dir.rstrip('/\\'))
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', base_name).strip('-')
        return {
            "title": base_name,
            "slug": slug,
            "author": "Pete Mockaitis & Jim Detert" if "courage" in base_name.lower() else "Audiobook Producer",
            "modules": modules
        }

    c3_indicators = {"Introduction to Course 3.txt", "Review: Beginning the planning phase.txt", "Building a risk management plan.txt"}
    if c3_indicators.intersection(files):
        return COURSERA_COURSE_3_CONFIG

    c2_indicators = {"Introduction to Course 2.txt", "Why is project initiation essential.txt", "Use AI to create a project charter.txt"}
    if c2_indicators.intersection(files):
        return COURSERA_COURSE_2_CONFIG
    
    c1_indicators = {"What is project management.txt", "What does a project manager do.txt"}
    if c1_indicators.intersection(files):
        return COURSERA_COURSE_1_CONFIG

    path_lower = source_dir.lower()
    if "planning" in path_lower or "course 3" in path_lower or "course-3" in path_lower:
        return COURSERA_COURSE_3_CONFIG
    if "initiation" in path_lower or "course 2" in path_lower or "course-2" in path_lower:
        return COURSERA_COURSE_2_CONFIG
    return COURSERA_COURSE_1_CONFIG

def extract_coursera_chapters(source_dir, output_dir, book_slug=None, session_id=None):
    """Extracts all modules and source files from Google Project Management Coursera dataset."""
    course_cfg = detect_coursera_course(source_dir)
    
    if not book_slug:
        book_slug = course_cfg["slug"]
    else:
        book_slug = re.sub(r'[^a-zA-Z0-9\-]+', '-', book_slug).strip('-')

    book_dir = os.path.join(output_dir, book_slug)
    os.makedirs(book_dir, exist_ok=True)
    
    if not session_id:
        session_id = f"ses_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    modules_config = course_cfg["modules"]

    session_manifest = {
        "session_id": session_id,
        "book_slug": book_slug,
        "book_title": course_cfg.get("title", book_slug),
        "author": course_cfg.get("author", "Google Career Certificates"),
        "source_path": os.path.abspath(source_dir),
        "total_chapters": len(modules_config),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "pipeline_stage": "01_structure_extracted",
        "step_1_status": "completed",
        "chapters": [],
        "metadata": {
            "extractor_version": "2.2.0",
            "source_type": "coursera_modular_course",
            "noise_filtered": {
                "headers_removed": True,
                "footers_removed": True,
                "watermarks_removed": True,
                "music_tags_removed": True,
                "drop_cap_healed": True
            }
        }
    }

    print(f"[*] Extracting Coursera Course Dataset: {source_dir}")
    print(f"[*] Course Title: {session_manifest['book_title']}")
    print(f"[*] Target Book Slug: {book_slug}")
    print(f"[*] Output Directory: {book_dir}\n")

    total_all_chars = 0
    total_all_words = 0

    for mod in modules_config:
        folder_name = mod["folder"]
        chap_dir = os.path.join(book_dir, folder_name)
        os.makedirs(chap_dir, exist_ok=True)
        
        print(f"[*] Processing {folder_name} ({mod['title']}) [{len(mod['files'])} components]...")
        
        if len(mod["files"]) == 1 and mod["files"][0][0].endswith(".txt"):
            f_name, _ = mod["files"][0]
            resolved_path = resolve_source_file(source_dir, f_name)
            with open(resolved_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            # Remove any leading Markdown H1 if present
            content = re.sub(r'^#\s*\d+[\.\:]?\s*.*?\n+', '', content).strip()
            full_chap_text = f"# {mod['title']}\n\n{content}"
        else:
            section_texts = []
            section_texts.append(f"# {mod['title']}\n")

            for f_name, section_title in mod["files"]:
                resolved_path = resolve_source_file(source_dir, f_name)
                ext = os.path.splitext(resolved_path)[1].lower()
                
                if ext == ".txt":
                    with open(resolved_path, "r", encoding="utf-8") as f:
                        content = clean_transcript_text(f.read())
                elif ext == ".pdf":
                    content = extract_pdf_clean(resolved_path)
                elif ext == ".docx":
                    content = extract_docx_glossary(resolved_path)
                else:
                    with open(resolved_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                
                section_texts.append(f"## {section_title}\n\n{content}")

            full_chap_text = "\n\n".join(section_texts)
        cleaned_chap_text = clean_extracted_text(full_chap_text)
        
        raw_file_rel = os.path.join(folder_name, "raw_original.txt")
        raw_file_abs = os.path.join(chap_dir, "raw_original.txt")

        with open(raw_file_abs, "w", encoding="utf-8") as f:
            f.write(cleaned_chap_text)

        c_len = len(cleaned_chap_text)
        w_cnt = len(cleaned_chap_text.split())
        total_all_chars += c_len
        total_all_words += w_cnt

        chap_record = {
            "index": mod["index"],
            "folder": folder_name,
            "title": mod["title"],
            "items_count": len(mod["files"]),
            "char_count": c_len,
            "word_count": w_cnt,
            "status": "raw_extracted",
            "raw_file": raw_file_rel
        }
        session_manifest["chapters"].append(chap_record)
        print(f"    -> [✓] Wrote {c_len:,} chars ({w_cnt:,} words) to {raw_file_rel}")

    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(session_manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] STEP 01 COMPLETE! Total Chars: {total_all_chars:,} | Total Words: {total_all_words:,}")
    print(f"[✓] Session manifest saved to: {manifest_path}")
    return session_manifest

# ------------------------------------------------------------------------------
# Extraction for Standard PDF Books (e.g. Quiet by Susan Cain, Process Groups, etc.)
# ------------------------------------------------------------------------------
def detect_tam_quoc_chapters(pdf_path, total_pages):
    """Detects all 120 chapters of Tam Quoc Dien Nghia."""
    import subprocess
    try:
        proc = subprocess.run(['pdftotext', pdf_path, '-'], stdout=subprocess.PIPE, text=True, check=True)
        pages = proc.stdout.split('\x0c')
    except Exception:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        pages = [p.extract_text() or '' for p in reader.pages]

    pattern = re.compile(r'^\s*HỒI\s+(\d+)\b', re.IGNORECASE | re.MULTILINE)
    raw_chaps = []

    # TOC is on pages 1-8 (0-7 in 0-indexed). Content starts at page 9 (index 8).
    for idx, page_txt in enumerate(pages[8:], start=9):
        matches = list(pattern.finditer(page_txt))
        for m in matches:
            c_num = int(m.group(1))
            sub = page_txt[m.end():m.end()+200].strip()
            lines = [l.strip() for l in sub.split('\n') if l.strip()]
            title = ' '.join(lines[:2])
            raw_chaps.append((c_num, idx, title))

    # Sort and deduplicate by chapter number
    raw_chaps.sort(key=lambda x: x[0])
    # Keep only unique chapter numbers 1..120
    seen = set()
    unique_chaps = []
    for item in raw_chaps:
        if item[0] not in seen and 1 <= item[0] <= 120:
            seen.add(item[0])
            unique_chaps.append(item)

    chapters_config = []
    for i in range(len(unique_chaps)):
        c_num, s_page, title = unique_chaps[i]
        if i + 1 < len(unique_chaps):
            next_s_page = unique_chaps[i+1][1]
            e_page = next_s_page - 1
        else:
            e_page = total_pages
        folder_name = f"{c_num:02d}-Hoi-{c_num:02d}" if c_num < 100 else f"{c_num}-Hoi-{c_num}"
        chapters_config.append({
            "index": c_num - 1,
            "folder": folder_name,
            "title": f"Hồi {c_num}: {title}",
            "start_page": s_page,
            "end_page": e_page
        })
    return chapters_config

def detect_pdf_chapters(pdf_path, total_pages):
    """Dynamically detects chapter ranges from PDF bookmarks or known schemas."""
    # Check if Tam Quoc Dien Nghia
    if "tam quoc" in pdf_path.lower() or "tam-quoc" in pdf_path.lower() or "1005-" in pdf_path.lower() or total_pages == 1515:
        return detect_tam_quoc_chapters(pdf_path, total_pages)

    # 1. Try pypdfium2 bookmarks
    try:
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(pdf_path)
        toc = list(pdf.get_toc())
        if toc:
            raw_entries = []
            for b in toc:
                dest = b.get_dest()
                p_idx = dest.get_index() if dest else None
                if p_idx is not None:
                    raw_entries.append({
                        "level": b.level,
                        "title": b.get_title().strip(),
                        "page": p_idx + 1 # 1-based
                    })
            
            quiet_match = any("Introvert" in e["title"] or "Extrovert" in e["title"] for e in raw_entries)
            if quiet_match or "Susan Cain" in pdf_path or "Quiet" in pdf_path:
                return [
                    {"index": 0, "folder": "00-Author-Note", "title": "Author's Note", "start_page": 12, "end_page": 12},
                    {"index": 1, "folder": "01-Introduction", "title": "Introduction: The North and South of Temperament", "start_page": 13, "end_page": 28},
                    {"index": 2, "folder": "02-Chapter-01", "title": "Part One - Chapter 1: The Rise of the Mighty Likeable Fellow", "start_page": 29, "end_page": 45},
                    {"index": 3, "folder": "03-Chapter-02", "title": "Chapter 2: The Myth of Charismatic Leadership", "start_page": 46, "end_page": 84},
                    {"index": 4, "folder": "04-Chapter-03", "title": "Chapter 3: When Collaboration Kills Creativity", "start_page": 85, "end_page": 110},
                    {"index": 5, "folder": "05-Chapter-04", "title": "Part Two - Chapter 4: Is Temperament Destiny?", "start_page": 111, "end_page": 130},
                    {"index": 6, "folder": "06-Chapter-05", "title": "Chapter 5: Beyond Temperament", "start_page": 131, "end_page": 146},
                    {"index": 7, "folder": "07-Chapter-06", "title": "Chapter 6: Franklin Was A Politician, But Eleanor Spoke Out of Conscience", "start_page": 147, "end_page": 172},
                    {"index": 8, "folder": "08-Chapter-07", "title": "Chapter 7: Why Did Wall Street Crash and Warren Buffett Prosper?", "start_page": 173, "end_page": 197},
                    {"index": 9, "folder": "09-Chapter-08", "title": "Part Three - Chapter 8: Soft Power: Asian-Americans and the Extrovert Ideal", "start_page": 198, "end_page": 222},
                    {"index": 10, "folder": "10-Chapter-09", "title": "Part Four - Chapter 9: When Should You Act More Extroverted?", "start_page": 223, "end_page": 244},
                    {"index": 11, "folder": "11-Chapter-10", "title": "Chapter 10: The Communication Gap", "start_page": 245, "end_page": 263},
                    {"index": 12, "folder": "12-Chapter-11", "title": "Chapter 11: On Cobblers and Generals", "start_page": 264, "end_page": 288},
                    {"index": 13, "folder": "13-Conclusion", "title": "Conclusion: Wonderland", "start_page": 289, "end_page": 291},
                    {"index": 14, "folder": "14-Note-on-Introvert-Extrovert", "title": "A Note on the Words Introvert and Extrovert", "start_page": 294, "end_page": 296}
                ]
    except Exception as e:
        print(f"[!] Warning reading bookmarks: {e}")
        
    # Check if Never Eat Alone
    if "Never Eat Alone" in pdf_path or "Keith Ferrazzi" in pdf_path or total_pages == 320:
        return [
            {"index": 0, "folder": "01-Chapter-01", "title": "Section One: The Mind-Set - Chapter 1: Becoming a Member of the Club", "start_page": 12, "end_page": 24},
            {"index": 1, "folder": "02-Chapter-02", "title": "Chapter 2: Don't Keep Score", "start_page": 25, "end_page": 33},
            {"index": 2, "folder": "03-Chapter-03", "title": "Chapter 3: What's Your Mission? (With Bill Clinton Profile)", "start_page": 34, "end_page": 52},
            {"index": 3, "folder": "04-Chapter-04", "title": "Chapter 4: Build It Before You Need It", "start_page": 53, "end_page": 58},
            {"index": 4, "folder": "05-Chapter-05", "title": "Chapter 5: The Genius of Audacity", "start_page": 59, "end_page": 66},
            {"index": 5, "folder": "06-Chapter-06", "title": "Chapter 6: The Networking Jerk (With Katharine Graham Profile)", "start_page": 67, "end_page": 75},
            {"index": 6, "folder": "07-Chapter-07", "title": "Section Two: The Skill Set - Chapter 7: Do Your Homework", "start_page": 76, "end_page": 83},
            {"index": 7, "folder": "08-Chapter-08", "title": "Chapter 8: Take Names", "start_page": 84, "end_page": 89},
            {"index": 8, "folder": "09-Chapter-09", "title": "Chapter 9: Warming the Cold Call", "start_page": 90, "end_page": 97},
            {"index": 9, "folder": "10-Chapter-10", "title": "Chapter 10: Managing the Gatekeeper Artfully", "start_page": 98, "end_page": 104},
            {"index": 10, "folder": "11-Chapter-11", "title": "Chapter 11: Never Eat Alone", "start_page": 105, "end_page": 109},
            {"index": 11, "folder": "12-Chapter-12", "title": "Chapter 12: Share Your Passions", "start_page": 110, "end_page": 115},
            {"index": 12, "folder": "13-Chapter-13", "title": "Chapter 13: Follow Up or Fail", "start_page": 116, "end_page": 120},
            {"index": 13, "folder": "14-Chapter-14", "title": "Chapter 14: Be a Conference Commando", "start_page": 121, "end_page": 138},
            {"index": 14, "folder": "15-Chapter-15", "title": "Chapter 15: Connecting with Connectors (With Paul Revere Profile)", "start_page": 139, "end_page": 149},
            {"index": 15, "folder": "16-Chapter-16", "title": "Chapter 16: Expanding Your Circle", "start_page": 150, "end_page": 153},
            {"index": 16, "folder": "17-Chapter-17", "title": "Chapter 17: The Art of Small Talk (With Dale Carnegie Profile)", "start_page": 154, "end_page": 169},
            {"index": 17, "folder": "18-Chapter-18", "title": "Section Three: Turning Connections into Compatriots - Chapter 18: Health, Wealth, and Children", "start_page": 170, "end_page": 181},
            {"index": 18, "folder": "19-Chapter-19", "title": "Chapter 19: Social Arbitrage (With Vernon Jordan Profile)", "start_page": 182, "end_page": 191},
            {"index": 19, "folder": "20-Chapter-20", "title": "Chapter 20: Pinging—All the Time", "start_page": 192, "end_page": 200},
            {"index": 20, "folder": "21-Chapter-21", "title": "Chapter 21: Find Anchor Tenants and Feed Them", "start_page": 201, "end_page": 211},
            {"index": 21, "folder": "22-Chapter-22", "title": "Section Four: Trading Up and Giving Back - Chapter 22: Be Interesting (With Dalai Lama Profile)", "start_page": 212, "end_page": 234},
            {"index": 22, "folder": "23-Chapter-23", "title": "Chapter 23: Build Your Brand", "start_page": 235, "end_page": 241},
            {"index": 23, "folder": "24-Chapter-24", "title": "Chapter 24: Broadcast Your Brand", "start_page": 242, "end_page": 256},
            {"index": 24, "folder": "25-Chapter-25", "title": "Chapter 25: The Write Stuff", "start_page": 257, "end_page": 259},
            {"index": 25, "folder": "26-Chapter-26", "title": "Chapter 26: Getting Close to Power", "start_page": 260, "end_page": 269},
            {"index": 26, "folder": "27-Chapter-27", "title": "Chapter 27: Build It and They Will Come (With Benjamin Franklin Profile)", "start_page": 270, "end_page": 278},
            {"index": 27, "folder": "28-Chapter-28", "title": "Chapter 28: Never Give in to Hubris", "start_page": 279, "end_page": 283},
            {"index": 28, "folder": "29-Chapter-29", "title": "Chapter 29: Find Mentors, Find Mentees, Repeat (With Eleanor Roosevelt Profile)", "start_page": 284, "end_page": 296},
            {"index": 29, "folder": "30-Chapter-30", "title": "Chapter 30: Balance Is B.S.", "start_page": 297, "end_page": 301},
            {"index": 30, "folder": "31-Chapter-31", "title": "Chapter 31: Welcome to the Connected Age", "start_page": 302, "end_page": 309}
        ]

    # Check if Process Groups
    if "ProcessGroups" in pdf_path or "Process Groups" in pdf_path or total_pages == 367:
        return [
            {"index": 0, "folder": "00-Preface", "title": "Preface & Table of Contents", "start_page": 1, "end_page": 14},
            {"index": 1, "folder": "01-Introduction", "title": "Section 1: Introduction", "start_page": 15, "end_page": 28},
            {"index": 2, "folder": "02-The-Project-Environment", "title": "Section 2: The Project Environment", "start_page": 29, "end_page": 44},
            {"index": 3, "folder": "03-Role-of-the-Project-Manager", "title": "Section 3: Role of the Project Manager", "start_page": 45, "end_page": 64},
            {"index": 4, "folder": "04-Initiating-Process-Group", "title": "Section 4: Initiating Process Group", "start_page": 65, "end_page": 86},
            {"index": 5, "folder": "05-Planning-Process-Group", "title": "Section 5: Planning Process Group", "start_page": 87, "end_page": 194},
            {"index": 6, "folder": "06-Executing-Process-Group", "title": "Section 6: Executing Process Group", "start_page": 195, "end_page": 240},
            {"index": 7, "folder": "07-Monitoring-and-Controlling-Process-Group", "title": "Section 7: Monitoring and Controlling Process Group", "start_page": 241, "end_page": 308},
            {"index": 8, "folder": "08-Closing-Process-Group", "title": "Section 8: Closing Process Group", "start_page": 309, "end_page": 318},
            {"index": 9, "folder": "09-Inputs-and-Outputs", "title": "Section 9: Common Inputs and Outputs", "start_page": 319, "end_page": 332},
            {"index": 10, "folder": "10-Tools-and-Techniques", "title": "Section 10: Tools and Techniques", "start_page": 333, "end_page": 348},
            {"index": 11, "folder": "11-Glossary", "title": "Section 11: References & Glossary", "start_page": 349, "end_page": 367}
        ]
        
    return [
        {"index": 0, "folder": "01-Main-Content", "title": "Main Content", "start_page": 1, "end_page": total_pages}
    ]

def extract_pdf_chapters(pdf_path, output_dir, book_slug, session_id=None):
    """Extracts chapters from standard single PDF books."""
    book_dir = os.path.join(output_dir, book_slug)
    os.makedirs(book_dir, exist_ok=True)
    
    if not session_id:
        session_id = f"ses_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    print(f"[*] Opening PDF file: {pdf_path}")
    
    # Try high-speed extraction via pdftotext first
    pages_text = None
    try:
        import subprocess
        proc = subprocess.run(['pdftotext', pdf_path, '-'], stdout=subprocess.PIPE, text=True, check=True)
        raw_pages = proc.stdout.split('\x0c')
        if raw_pages and not raw_pages[-1].strip():
            raw_pages = raw_pages[:-1]
        pages_text = raw_pages
        print(f"[*] Fast pdftotext loaded {len(pages_text)} pages successfully.")
    except Exception as e:
        print(f"[!] Warning: fast pdftotext fallback to pdfplumber: {e}")

    total_pages = len(pages_text) if pages_text else 0
    pdf_obj = None
    if not pages_text:
        pdf_obj = pdfplumber.open(pdf_path)
        total_pages = len(pdf_obj.pages)

    chapters_config = detect_pdf_chapters(pdf_path, total_pages)
    
    session_manifest = {
        "session_id": session_id,
        "book_slug": book_slug,
        "book_title": "Tam Quốc Diễn Nghĩa" if "tam-quoc" in book_slug.lower() or "tam quoc" in book_slug.lower() else book_slug,
        "author": "La Quán Trung" if "tam-quoc" in book_slug.lower() or "tam quoc" in book_slug.lower() else "Unknown",
        "source_pdf": os.path.abspath(pdf_path),
        "total_pages": total_pages,
        "total_chapters": len(chapters_config),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "pipeline_stage": "01_pdf_extracted",
        "step_1_status": "completed",
        "chapters": [],
        "metadata": {
            "extractor_version": "2.3.0",
            "source_type": "single_pdf_book",
            "noise_filtered": {
                "headers_removed": True,
                "footers_removed": True,
                "watermarks_removed": True,
                "page_numbers_removed": True
            }
        }
    }
    
    for chap_info in chapters_config:
        folder_name = chap_info["folder"]
        chap_dir = os.path.join(book_dir, folder_name)
        os.makedirs(chap_dir, exist_ok=True)

        print(f"[*] Extracting {folder_name} ({chap_info['title']}) Pages {chap_info['start_page']} to {chap_info['end_page']}...")
        
        raw_text_parts = []
        for p_num in range(chap_info['start_page'] - 1, chap_info['end_page']):
            if pages_text and p_num < len(pages_text):
                raw_text_parts.append(pages_text[p_num])
            elif pdf_obj and p_num < len(pdf_obj.pages):
                page = pdf_obj.pages[p_num]
                txt = page.extract_text() or ""
                raw_text_parts.append(txt)

        full_chap_text = "\n\n".join(raw_text_parts)
        cleaned_text = clean_extracted_text(full_chap_text)

        raw_file_rel = os.path.join(folder_name, "raw_original.txt")
        raw_file_abs = os.path.join(chap_dir, "raw_original.txt")

        with open(raw_file_abs, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        w_cnt = len(cleaned_text.split())
        chap_record = {
            "index": chap_info["index"],
            "folder": folder_name,
            "title": chap_info["title"],
            "start_page": chap_info["start_page"],
            "end_page": chap_info["end_page"],
            "char_count": len(cleaned_text),
            "word_count": w_cnt,
            "word_count_raw": w_cnt,
            "step_1_status": "completed",
            "status": "raw_extracted",
            "raw_file": raw_file_rel
        }
        session_manifest["chapters"].append(chap_record)
        print(f"    -> [✓] Wrote {len(cleaned_text):,} chars ({w_cnt:,} words) to {raw_file_rel}")

    if pdf_obj:
        pdf_obj.close()

    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(session_manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] STEP 01 COMPLETE! Session manifest saved to: {manifest_path}")
    return session_manifest

# ------------------------------------------------------------------------------
# Universal Entrypoint & CLI
# ------------------------------------------------------------------------------
def extract_structure(source_path, output_dir="Kich-ban-clipchamp", book_slug=None, session_id=None):
    """Universal dispatcher: handles directories, PDFs, and auto-detects slug."""
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source path '{source_path}' does not exist.")
        
    if os.path.isdir(source_path):
        return extract_coursera_chapters(source_path, output_dir, book_slug, session_id)
    else:
        if not book_slug:
            raw_name = os.path.splitext(os.path.basename(source_path))[0]
            if "tam-quoc" in raw_name.lower() or "tam quoc" in raw_name.lower() or "1005-" in raw_name.lower():
                book_slug = "Tam-Quoc-Dien-Nghia"
            else:
                book_slug = re.sub(r'[^a-zA-Z0-9\-]+', '-', raw_name).strip('-')
        return extract_pdf_chapters(source_path, output_dir, book_slug, session_id)

def main():
    parser = argparse.ArgumentParser(description="Universal Step 01 Structure Extractor")
    parser.add_argument("--source_path", "--pdf_path", "--input", dest="source_path", default=None,
                        help="Path to source PDF file or source course directory")
    parser.add_argument("--output_dir", default="Kich-ban-clipchamp",
                        help="Root output directory (default: Kich-ban-clipchamp)")
    parser.add_argument("--book_slug", default=None,
                        help="Book slug name (default: auto-detected from source)")
    parser.add_argument("--session_id", default=None,
                        help="Session ID (default: auto-generated)")

    args = parser.parse_args()

    source = args.source_path
    if not source:
        # Default fallback to Google-Project-Management-Coursera if it exists
        default_coursera = "Docs/Google-Project-Management-Coursera"
        default_pg = "Docs/ProcessGroupsPracticeGuide.pdf"
        if os.path.exists(default_coursera):
            source = default_coursera
        elif os.path.exists(default_pg):
            source = default_pg
        else:
            print("[!] Please provide --source_path or --pdf_path")
            sys.exit(1)

    extract_structure(source, args.output_dir, args.book_slug, args.session_id)

if __name__ == "__main__":
    main()
