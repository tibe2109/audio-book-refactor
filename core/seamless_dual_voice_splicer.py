#!/usr/bin/env python3
# ==============================================================================
# Step 08: Universal AI Multilingual Dual-Voice TTS & Phrase-Level Splicer
# Skill: arf_08_tts_neural_bgm_mixer
# ==============================================================================
import os
import re
import json
import asyncio
import subprocess
import imageio_ffmpeg
import edge_tts

# Audio Profiles (Gender-Consistent Male Profile)
PRIMARY_VOICE_VN = "vi-VN-NamMinhNeural"  # Male narrator for Vietnamese
PRIMARY_RATE_VN = "-10%"

SECONDARY_VOICE_EN = "en-US-BrianMultilingualNeural"  # Male narrator for English/Latin terms
SECONDARY_RATE_EN = "-18%"  # Base reference rate (dynamically adapted: -24% short/acronyms, -18% medium, -15% long)

def get_adaptive_en_rate(text: str) -> str:
    """
    Dynamic Length-Adaptive Speech Rate for foreign/English terms (Anti-Auditory Swallowing & Fatigue):
    - Ultra-short / single words / acronyms (1 word, e.g. 'P-M-I', 'bar', 'role', 'scope', 'A-I'): -24%
      (Ensures crystal-clear articulation, gives full resonance to short vowels/consonants).
    - Medium phrases (2-3 words, e.g. 'Project Manager', 'Sprint Backlog', 'Google New York'): -18%
      (Balanced, professional, articulate cadence).
    - Long multi-word clauses / headings (>= 4 words, e.g. 'BECOMING AN EFFECTIVE PROJECT MANAGER'): -15%
      (Fluid, natural rhythm, prevents sluggishness or drowsiness on long phrases).
    """
    clean = re.sub(r'[^\w\s-]', '', text).strip()
    words = clean.split()
    if len(words) <= 1:
        return "-24%"
    elif len(words) in (2, 3):
        return "-18%"
    else:
        return "-15%"

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# Import the comprehensive canonical Vietnamese unaccented syllables set (1894 syllables)
try:
    from vietnamese_syllables import VIETNAMESE_SYLLABLES_SET
except ImportError:
    try:
        from core.vietnamese_syllables import VIETNAMESE_SYLLABLES_SET
    except ImportError:
        VIETNAMESE_SYLLABLES_SET = set()

# System English dictionary loaded at startup (Linux: 104k+ words)
SYSTEM_ENGLISH_WORDS = set()
for dp in ["/usr/share/dict/words", "/usr/share/dict/american-english", "/usr/share/dict/british-english"]:
    if os.path.exists(dp):
        try:
            with open(dp, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    w = line.strip().lower()
                    if w and len(w) > 1 and not any(c in w for c in "'.-"):
                        SYSTEM_ENGLISH_WORDS.add(w)
            break
        except Exception:
            pass

# Comprehensive Built-in PM, Business, and Tech Vocabulary (100% hits across all environments)
BUILTIN_PM_TERMS = {
    # Acronyms & Spelled-out forms (Note: AI, IT handled via ALLCAPS/HYPHENATED check)
    "pmi", "pmbok", "wbs", "kpi", "okr", "sla", "swot", "evm", "qa", "qc",
    "ceo", "cto", "pmo", "pmp", "capm", "raci", "smart", "pdca", "mvp", "api", "ui", "ux",
    "roi", "erp", "crm", "hr", "b2b", "b2c", "saas", "paas", "iaas", "itto", "eac", "etc",
    "vac", "tcpi", "bac", "pv", "ev", "ac", "sv", "cv", "spi", "cpi",

    # Roles & Stakeholders
    "project", "management", "manager", "director", "executive", "officer", "sponsor",
    "leader", "leadership", "stakeholder", "stakeholders", "team", "member", "client",
    "customer", "user", "developer", "engineer", "architect", "analyst", "tester",
    "product", "owner", "master", "coordinator", "facilitator",
    # Frameworks & Methodologies
    "agile", "scrum", "sprint", "kanban", "waterfall", "lean", "hybrid", "prince2", "itil",
    "framework", "methodology", "lifecycle", "cadence", "approach", "tailoring",
    # Artifacts & Deliverables
    "charter", "scope", "deliverable", "deliverables", "baseline", "milestone", "milestones",
    "backlog", "epic", "story", "stories", "burndown", "burnup", "velocity", "roadmap",
    "dashboard", "matrix", "register", "log", "report", "template", "flowchart", "diagram",
    # Processes & Phases
    "initiating", "initiation", "planning", "executing", "execution", "monitoring",
    "controlling", "closing", "closure", "governance", "procurement", "vendor", "contract",
    "kick-off", "kickoff", "onboarding", "offboarding", "handover", "sign-off", "signoff",
    "walkthrough", "standup", "retrospective", "retro", "review", "refinement", "demo",
    # Key Concepts & Technical Vocabulary
    "telehealth", "unique", "endeavor", "temporary", "pursuit", "what", "why", "how",
    "who", "when", "where", "which", "career", "embarking", "effective", "organizational",
    "culture", "structure", "value", "outcome", "outcomes", "output", "outputs", "input",
    "inputs", "tool", "tools", "technique", "techniques", "quality", "assurance", "control",
    "audit", "compliance", "risk", "risks", "issue", "issues", "change", "changes",
    "request", "requests", "assumption", "assumptions", "constraint", "constraints",
    "requirement", "requirements", "budget", "cost", "schedule", "time", "resource",
    "resources", "communication", "communications", "engagement", "feedback", "survey",
    "lessons", "learned", "creep", "plating", "best", "practice", "practices", "standard",
    "standards", "guideline", "guidelines", "metric", "metrics", "target", "targets",
    "environment", "environmental", "factors", "process", "assets", "business", "case",
    "benefits", "data", "gathering", "analysis", "representation", "expert", "judgment",
    "introduction", "preface", "glossary", "acronyms", "appendix", "jira", "confluence",
    "trello", "asana", "coursera", "google", "microsoft"
}

# Ambiguous tokens that could be VN unaccented syllable or short EN word
AMBIGUOUS_SHARED_TOKENS = {
    'a', 'an', 'in', 'on', 'at', 'to', 'do', 'so', 'no', 'can', 'may', 'bay',
    'lay', 'day', 'chat', 'con', 'ca', 'ma', 'la', 'ra', 'va', 'di', 'me', 'he',
    'be', 'of', 'for', 'the', 'as', 'by', 'with', 'from', 'up', 'out', 'is',
    'are', 'it', 'or', 'and', 'vs', 'via'
}

CUSTOM_BOOK_GLOSSARY = set()

def load_custom_glossary(book_dir):
    global CUSTOM_BOOK_GLOSSARY
    CUSTOM_BOOK_GLOSSARY.clear()
    possible_paths = [
        os.path.join(book_dir, "custom_phonetics.json"),
        os.path.join(book_dir, "custom_glossary.json"),
        os.path.join(book_dir, "pmbok_custom_phonetics.json")
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        for k in data.keys():
                            for w in k.split():
                                CUSTOM_BOOK_GLOSSARY.add(w.lower())
                    elif isinstance(data, list):
                        for item in data:
                            for w in str(item).split():
                                CUSTOM_BOOK_GLOSSARY.add(w.lower())
                print(f"[*] Loaded custom book glossary from {p} ({len(CUSTOM_BOOK_GLOSSARY)} terms)", flush=True)
            except Exception as e:
                print(f"[!] Error loading glossary {p}: {e}", flush=True)

VI_DIACRITICS_REGEX = re.compile(r'[àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]')

# Hyphenated spelled-out acronyms: P-M-I, W-B-S, K-P-I, P-M-B-O-K, S-W-O-T, A-I, I-T
HYPHENATED_ACRONYM_REGEX = re.compile(r'^[a-zA-Z](-[a-zA-Z])+$')

# Standard uppercase acronym: PMI, PMBOK, WBS, KPI, SLA, SWOT, PMP
ALLCAPS_ACRONYM_REGEX = re.compile(r'^[A-Z]{2,6}$')

# Morphological Suffixes (both singular and plural)
SUFFIX_REGEX = re.compile(r'(tion|sion|ment|ance|ence|able|ible|tive|sive|ship|ing|ed|al|ic|ical|ous|ity|ism|ist|logy|graphy|ture|ure|est|less|ness|hood|wise|ward|ful|fully|ly|ize|ise|ify|ate|ian|ious|eous)s?$', re.I)

# English initial consonant clusters
EN_PREFIX_CONSONANTS = re.compile(r'^(str|spr|scr|spl|squ|shr|thr|fl|fr|gl|gr|pl|pr|bl|br|cl|cr|dr|sk|sp|st|sm|sn|sc|sw|wr|kn|ps|rh|sch|chr|phr|tw|dw|wh)', re.I)

# English final consonant clusters or non-VN single final consonants
EN_FINAL_CONSONANTS = re.compile(r'(ct|ft|pt|lt|rt|st|sk|sp|mp|nd|nt|nk|rk|lk|rd|ld|rn|rm|lm|sm|ts|ks|ps|nce|nse|rce|rse|tch|dge|que|the|ble|ple|fle|gle|kle|tle|dle|ght|sh|th|ph|[bdfjklrsvwxz])$', re.I)

def is_english_token(word):
    clean_w = word.strip(".,?!:;()[]\"'").lower()
    if not clean_w:
        return False
    
    # 1. Any Vietnamese diacritics -> 100% VIETNAMESE
    if VI_DIACRITICS_REGEX.search(word):
        return False
    
    # 2. Custom book glossary
    if clean_w in CUSTOM_BOOK_GLOSSARY:
        return True

    # 3. Hyphenated spelled-out acronyms (P-M-I, W-B-S, K-P-I, A-I, I-T) -> 100% ENGLISH
    raw_clean = word.strip(".,?!:;()[]\"'")
    if HYPHENATED_ACRONYM_REGEX.match(raw_clean):
        return True
        
    # 4. Explicit tech acronyms like AI, IT
    if raw_clean in {'AI', 'IT'}:
        return True

    # 5. Built-in PM, Business, and Tech vocabulary -> 100% ENGLISH
    if clean_w in BUILTIN_PM_TERMS:
        return True

    # 6. Contains non-Vietnamese foreign letters (w, z, j, f)
    if re.search(r'[wzjf]', clean_w):
        return True

    # 7. If it is in the canonical Vietnamese syllables set and not in PM terms -> default VIETNAMESE!
    # (Prevents all-caps Vietnamese titles like 'BÀI HAI, VAI TRÒ' from being falsely treated as acronyms)
    if clean_w in VIETNAMESE_SYLLABLES_SET:
        return False

    # 8. Uppercase acronyms of 2-6 chars without accents (PMI, WBS, KPI, SLA, SWOT, PMP)
    if ALLCAPS_ACRONYM_REGEX.match(raw_clean):
        return True

    # 9. Suffix matching (only for words not in Vietnamese syllables)
    if SUFFIX_REGEX.search(clean_w):
        return True

    # 10. English consonant clusters
    if EN_PREFIX_CONSONANTS.search(clean_w) or EN_FINAL_CONSONANTS.search(clean_w):
        return True

    # 11. English vowel combinations (ea, ee, oo, ou, ei, ey, oy, au, aw, ow, ew)
    if re.search(r'(ea|ee|oo|ou|ei|ey|oy|au|aw|ow|ew)', clean_w):
        return True

    # 12. Double consonants
    if re.search(r'([b-df-hj-np-tv-z])\1', clean_w):
        return True

    # 13. System English dictionary (104k+ words)
    if clean_w in SYSTEM_ENGLISH_WORDS:
        return True

    return False

def is_speakable(text):
    return bool(re.search(r'[A-Za-z0-9àáảãạâăêôơưđÀÁẢÃẠÂĂÊÔƠƯĐ]', text))

def clean_speech_text(text, is_sentence_end=False):
    # Strip non-speakable Unicode bullet symbols and icons
    t = re.sub(r'[▶►▪●★▲◆■✓•–—…|/\\\\]', ' ', text)
    t = re.sub(r'\. \.\.\.\.\.\.', ' ', t)
    t = re.sub(r'\.{2,}', ' ', t)
    t = re.sub(r'[,.!?]+\s*([,.!?])', r'\1', t)

    # Detect original boundary punctuation
    stripped_raw = text.rstrip()
    has_terminal = bool(re.search(r'[.!?…]$', stripped_raw))
    has_comma = bool(re.search(r'[,;:]$', stripped_raw))

    t = re.sub(r'\s+', ' ', t).strip(' ,.')
    if not t:
        return ""

    if has_terminal or is_sentence_end:
        t += '.'
    elif has_comma:
        t += ','
    # If seamless in-sentence flow without punctuation: keep clean text without trailing period
    return t

def split_multilingual_segments(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    words = []
    is_line_end = []
    for line in lines:
        l_words = line.split()
        for idx, w in enumerate(l_words):
            words.append(w)
            is_line_end.append(idx == len(l_words) - 1)

    if not words:
        return []

    flags = [is_english_token(w) for w in words]

    # Pre-pass: Zero-drift clause-level English detection
    # Group tokens by clause boundaries (punctuation marks or line ends)
    clauses = []
    current_clause = []
    for idx, (w, lend) in enumerate(zip(words, is_line_end)):
        current_clause.append((idx, w))
        if lend or any(w.endswith(p) for p in [',', '.', '!', '?', ';', ':', '…']):
            clauses.append(current_clause)
            current_clause = []
    if current_clause:
        clauses.append(current_clause)

    for cl in clauses:
        cl_words = [w for idx, w in cl if w.strip(".,?!:;()[]\"'")]
        has_vi_diacritic = any(VI_DIACRITICS_REGEX.search(w) for w in cl_words)
        if not has_vi_diacritic and len(cl_words) >= 2:
            strict_en_count = sum(1 for idx, w in cl if flags[idx] and w.strip(".,?!:;()[]\"'"))
            all_en_compat = all(
                (w.strip(".,?!:;()[]\"'").lower() in AMBIGUOUS_SHARED_TOKENS or
                 w.strip(".,?!:;()[]\"'").lower() in SYSTEM_ENGLISH_WORDS or
                 w.strip(".,?!:;()[]\"'").lower() in BUILTIN_PM_TERMS or
                 flags[idx])
                for idx, w in cl if w.strip(".,?!:;()[]\"'")
            )
            if strict_en_count >= 1 and all_en_compat and (strict_en_count / len(cl_words)) >= 0.35:
                for idx, w in cl:
                    if w.strip(".,?!:;()[]\"'"):
                        flags[idx] = True

    # Leading article propagation: if a token is in {'the', 'a', 'an'} and followed by English token
    for i in range(len(words) - 1):
        if not flags[i] and words[i].strip(".,?!:;()[]\"'").lower() in {'the', 'a', 'an'} and flags[i+1]:
            if i == 0 or any(words[i-1].endswith(p) for p in [',', '.', '!', '?', ';', ':', '…']) or is_line_end[i-1]:
                flags[i] = True

    # Multi-token connector bridging:
    # Any span of 1 to 4 ambiguous/connector tokens between English tokens becomes English
    n = len(words)
    i = 0
    while i < n:
        if flags[i]:
            j = i + 1
            while j < n and j <= i + 4 and not flags[j]:
                cw = words[j].strip(".,?!:;()[]\"'").lower()
                if (cw in AMBIGUOUS_SHARED_TOKENS or cw in SYSTEM_ENGLISH_WORDS) and not VI_DIACRITICS_REGEX.search(words[j]):
                    j += 1
                else:
                    break
            if j < n and flags[j] and j > i + 1:
                for k in range(i + 1, j):
                    flags[k] = True
                i = j
                continue
        i += 1


    segments = []
    curr_tokens = []
    curr_is_en = flags[0]

    for w, flag in zip(words, flags):
        if not curr_tokens:
            curr_is_en = flag
            curr_tokens.append(w)
        elif flag == curr_is_en:
            curr_tokens.append(w)
        else:
            segments.append(("en" if curr_is_en else "vi", " ".join(curr_tokens)))
            curr_tokens = [w]
            curr_is_en = flag

    if curr_tokens:
        segments.append(("en" if curr_is_en else "vi", " ".join(curr_tokens)))

    filtered = []
    total_segs = len(segments)
    for idx, (lang, seg_str) in enumerate(segments):
        is_last = (idx == total_segs - 1)
        stripped_raw = seg_str.rstrip()
        has_comma = bool(re.search(r'[,;:]$', stripped_raw))
        has_terminal = bool(re.search(r'[.!?…]$', stripped_raw))
        has_dramatic_pause = (". ......" in seg_str or "......" in seg_str)

        clean_str = clean_speech_text(seg_str, is_sentence_end=is_last)
        if is_speakable(clean_str):
            if has_dramatic_pause:
                pause_type = "dramatic_pause"
            elif has_comma:
                pause_type = "emphasis"
            elif has_terminal or is_last:
                pause_type = "terminal"
            else:
                pause_type = "seamless"
            filtered.append((lang, clean_str, pause_type))

    return filtered

def get_system_proxy():
    return os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or None

def is_valid_audio_mp3(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) < 500:
        return False
    try:
        with open(file_path, "rb") as f:
            head = f.read(512)
            if any(b in head.lower() for b in [b"<html", b"<!doctype", b"<body", b"502 bad gateway", b"403 forbidden", b"access denied"]):
                return False
        cmd = [FFMPEG_EXE, "-i", file_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return "Audio:" in res.stderr
    except Exception:
        return False

def normalize_edge_param(param_str, unit):
    if not param_str:
        return f"+0{unit}"
    p = str(param_str).strip()
    if not (p.startswith('+') or p.startswith('-')):
        p = f"+{p}"
    return p

async def synthesize_speech_voice(text, voice, pitch="+0Hz", rate="-10%", temp_out=None, proxy=None, retries=5, sem=None):
    if proxy is None:
        proxy = get_system_proxy()
    clean_text = clean_speech_text(text)
    if not clean_text or not is_speakable(clean_text):
        return False

    p = normalize_edge_param(pitch, "Hz")
    r = normalize_edge_param(rate, "%")
    seg_timeout = max(30.0, len(clean_text) * 0.08 + 20.0)

    for attempt in range(1, retries + 1):
        try:
            if sem:
                async with sem:
                    await asyncio.sleep(0.12)
                    comm = edge_tts.Communicate(clean_text, voice, pitch=p, rate=r, proxy=proxy)
                    await asyncio.wait_for(comm.save(temp_out), timeout=seg_timeout)
            else:
                comm = edge_tts.Communicate(clean_text, voice, pitch=p, rate=r, proxy=proxy)
                await asyncio.wait_for(comm.save(temp_out), timeout=seg_timeout)
            if is_valid_audio_mp3(temp_out):
                return True
        except Exception as e:
            if attempt < retries:
                print(f"       [!] Edge-TTS attempt {attempt}/{retries} retry for '{clean_text[:25]}...': {e}", flush=True)
            if attempt == retries:
                print(f"       [!] Edge-TTS attempt {retries}/{retries} failed for '{clean_text[:25]}...': {e}. Trying fallback...", flush=True)
                # Fallback with gender preservation
                try:
                    fallback_voice = "vi-VN-HoaiMyNeural" if ("HoaiMy" in voice or "Emma" in voice) else "vi-VN-NamMinhNeural"
                    if sem:
                        async with sem:
                            comm = edge_tts.Communicate(clean_text, fallback_voice, pitch="+0Hz", rate=r, proxy=proxy)
                            await asyncio.wait_for(comm.save(temp_out), timeout=seg_timeout)
                    else:
                        comm = edge_tts.Communicate(clean_text, fallback_voice, pitch="+0Hz", rate=r, proxy=proxy)
                        await asyncio.wait_for(comm.save(temp_out), timeout=seg_timeout)
                    if is_valid_audio_mp3(temp_out):
                        return True
                except Exception as fe:
                    print(f"       [!] Fallback failed for '{clean_text[:25]}...': {fe}", flush=True)
            await asyncio.sleep(2.5 * attempt)
    return False

async def synthesize_segment(text, lang, temp_out, retries=5, sem=None):
    voice = SECONDARY_VOICE_EN if lang == "en" else PRIMARY_VOICE_VN
    clean_text = clean_speech_text(text)
    rate = get_adaptive_en_rate(clean_text) if lang == "en" else PRIMARY_RATE_VN
    return await synthesize_speech_voice(clean_text, voice, pitch="+0Hz", rate=rate, temp_out=temp_out, retries=retries, sem=sem)


TIMBRE_EQ_FILTERS = {
    "chest_resonance": "equalizer=f=160:t=q:w=1.2:g=5,equalizer=f=300:t=q:w=1:g=2.5,equalizer=f=3500:t=q:w=1:g=-3",
    "warm_authority": "equalizer=f=280:t=q:w=1:g=3.5,equalizer=f=2200:t=q:w=1:g=2,equalizer=f=4500:t=q:w=1:g=-2.5",
    "sharp_cunning": "highpass=f=220,equalizer=f=2800:t=q:w=1.5:g=4.5,equalizer=f=5500:t=q:w=1:g=3",
    "aged_gravel": "equalizer=f=420:t=q:w=1:g=4.5,lowpass=f=4200,equalizer=f=1200:t=q:w=1:g=-3",
    "youth_bright": "highpass=f=280,equalizer=f=3800:t=q:w=1.2:g=4.5,equalizer=f=6500:t=q:w=1:g=2.5",
    "servile_flatterer": "highpass=f=320,equalizer=f=2600:t=q:w=1:g=4,equalizer=f=4800:t=q:w=1:g=3.5",
    "tyrant_arrogant": "equalizer=f=190:t=q:w=1:g=4.5,equalizer=f=1800:t=q:w=1.5:g=4,equalizer=f=4000:t=q:w=1:g=2",
    "tragic_grief": "equalizer=f=320:t=q:w=1.2:g=4,equalizer=f=1600:t=q:w=1:g=-3.5,lowpass=f=4800",
    "epic_narrator": "equalizer=f=2500:t=q:w=1:g=3,equalizer=f=200:t=q:w=1:g=2",
    "elegiac_narrator": "equalizer=f=400:t=q:w=1:g=2.5,equalizer=f=3000:t=q:w=1:g=-2",
    "suspense_narrator": "highpass=f=150,equalizer=f=3500:t=q:w=1:g=3",
    "contemplative_narrator": "equalizer=f=250:t=q:w=1:g=3,lowpass=f=6000",
    "poetic_recitation": "equalizer=f=250:t=q:w=1:g=3.5,equalizer=f=3500:t=q:w=1:g=-2,lowpass=f=7500",
    "melancholic_social": "equalizer=f=350:t=q:w=1:g=3,equalizer=f=2500:t=q:w=1:g=-2.5",
    "satirical_ironic": "highpass=f=180,equalizer=f=2800:t=q:w=1:g=3,equalizer=f=5000:t=q:w=1:g=2",
    "existential_interior": "equalizer=f=200:t=q:w=1:g=3,equalizer=f=4000:t=q:w=1:g=-3",
    "scholarly_warmth": "equalizer=f=280:t=q:w=1:g=2.5,equalizer=f=3000:t=q:w=1:g=-1.5",
    "wuxia_heroic": "equalizer=f=220:t=q:w=1:g=3,equalizer=f=2200:t=q:w=1:g=2.5",
    "intimate_narrator": ""
}

def process_audio_segment_ffmpeg(in_mp3, out_wav, pause_type=None, pad_sec=None, prepend_silence_sec=0.0, timbre_eq=None):
    """
    Two-Stage Broadcast Leveling (Stage 1: Per-Segment Leveling):
    - start_threshold=-50dB: Preserves full natural vocal decay tail (avoids clipping Vietnamese word endings).
    - timbre_eq: Applies targeted DSP Formant EQ shaping (supports preset name or direct parametric filter string).
    - loudnorm=I=-16:TP=-1.5:LRA=5: Normalizes each dialogue or narration line individually.
    - apad=pad_dur={pad_sec}: Natural pause cushion:
        * dramatic_pause (1.50s): Headings, section markers, poem intros/outros (. ......).
        * terminal (0.45s): Sentence ends.
        * emphasis (0.22s): Punctuation/comma or dialogue lead-in.
        * seamless (0.08s): Smooth handoff in continuous speech.
    - prepend_silence_sec: Prepends silence (e.g. 1.50s) if the chunk starts with dramatic pause (. ......).
    """
    if pad_sec is None:
        if pause_type == "dramatic_pause":
            pad_sec = 1.50
        elif pause_type == "terminal":
            pad_sec = 0.45
        elif pause_type == "emphasis":
            pad_sec = 0.22
        else: # seamless
            pad_sec = 0.08

    af_parts = [
        # Gentle silence trimming that preserves 100% natural vocal decay, breath out, and vowel release:
        # Avoids cutting speech tail abruptly (which causes 'hơi chưa ra hết đã bị ngắt')
        "silenceremove=start_periods=1:start_duration=0.05:start_threshold=-55dB:start_silence=0.05",
        "silenceremove=stop_periods=-1:stop_duration=0.25:stop_threshold=-55dB:stop_silence=0.20"
    ]
    if timbre_eq:
        if timbre_eq in TIMBRE_EQ_FILTERS:
            eq_filter = TIMBRE_EQ_FILTERS[timbre_eq]
            if eq_filter:
                af_parts.append(eq_filter)
        elif any(timbre_eq.startswith(prefix) for prefix in ("equalizer=", "highpass=", "lowpass=", "volume=", "bass=", "treble=", "firequalizer=")):
            af_parts.append(timbre_eq)

    af_parts.append("loudnorm=I=-16:TP=-1.5:LRA=5")
    if pad_sec > 0:
        af_parts.append(f"apad=pad_dur={pad_sec:.2f}")

    filter_graph = ",".join(af_parts)
    if prepend_silence_sec > 0:
        delay_ms = int(prepend_silence_sec * 1000)
        filter_graph = f"adelay={delay_ms}|{delay_ms}," + filter_graph

    cmd = [
        FFMPEG_EXE, "-y", "-i", in_mp3,
        "-af", filter_graph,
        "-ar", "48000", "-ac", "1",
        out_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def concat_audio_segments(wav_files, final_mp3):
    """
    Two-Stage Broadcast Leveling (Stage 2: Master Chunk Leveling):
    - Concat all segment WAV files via ffmpeg demuxer.
    - Apply EBU R128 loudnorm ONCE on the full chunk: loudnorm=I=-16:TP=-1.5:LRA=6.
    - Output 192k MP3.
    """
    valid_wavs = [w for w in wav_files if os.path.exists(w) and os.path.getsize(w) > 500]
    if not valid_wavs:
        return False

    list_txt = final_mp3 + ".concat.txt"
    with open(list_txt, "w", encoding="utf-8") as f:
        for w in valid_wavs:
            f.write(f"file '{os.path.abspath(w)}'\n")

    cmd = [
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
        "-i", list_txt,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=6",
        "-b:a", "192k",
        final_mp3
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False
    finally:
        if os.path.exists(list_txt):
            os.remove(list_txt)

async def synthesize_script_chunk(script_path, output_mp3, segments_override=None, force_rebuild=True, sem=None):
    with open(script_path, "r", encoding="utf-8") as f:
        full_text = f.read().strip()
    if not full_text:
        return None

    word_count = len(full_text.split())
    # Minimum expected duration: ~160 wpm at 60% threshold
    min_expected_sec = max(5.0, (word_count / 160.0) * 60.0 * 0.6)

    if not force_rebuild and os.path.exists(output_mp3) and os.path.getsize(output_mp3) > 10000:
        actual_dur = get_audio_duration(output_mp3)
        if actual_dur >= min_expected_sec:
            return output_mp3
        print(f"       [!] Existing chunk {os.path.basename(output_mp3)} too short ({actual_dur:.1f}s < {min_expected_sec:.1f}s). Rebuilding...", flush=True)

    if segments_override:
        segments = [(item["lang"], item["text"], item.get("pause_type", "seamless")) for item in segments_override]
    else:
        segments = split_multilingual_segments(full_text)

    chunk_dir = os.path.dirname(output_mp3)
    temp_wavs = []
    failed_segments = 0

    for idx, seg_item in enumerate(segments):
        lang = seg_item[0]
        seg_text = seg_item[1]
        pause_type = seg_item[2] if len(seg_item) > 2 else "seamless"

        if not seg_text.strip():
            continue
        raw_mp3 = os.path.join(chunk_dir, f"_temp_{idx}.mp3")
        norm_wav = os.path.join(chunk_dir, f"_temp_{idx}.wav")

        success = await synthesize_segment(seg_text, lang, raw_mp3, sem=sem)
        if success:
            try:
                process_audio_segment_ffmpeg(raw_mp3, norm_wav, pause_type=pause_type)
                temp_wavs.append(norm_wav)
            except Exception as e:
                print(f"       [!] Error processing segment {idx} with FFmpeg: {e}", flush=True)
                failed_segments += 1
            finally:
                if os.path.exists(raw_mp3):
                    os.remove(raw_mp3)
        else:
            print(f"       [!] Failed to synthesize segment {idx}: {seg_text[:60]}...", flush=True)
            failed_segments += 1

    if failed_segments > 0 or len(temp_wavs) == 0:
        print(f"       [!] Chunk synthesis incomplete: {failed_segments} segment(s) failed out of {len(segments)}.", flush=True)
        for tw in temp_wavs:
            if os.path.exists(tw):
                os.remove(tw)
        return None

    concat_audio_segments(temp_wavs, output_mp3)
    for tw in temp_wavs:
        if os.path.exists(tw):
            os.remove(tw)

    if os.path.exists(output_mp3):
        actual_dur = get_audio_duration(output_mp3)
        if actual_dur < min_expected_sec:
            print(f"       [!] CRITICAL SANITY CHECK FAILED for {os.path.basename(output_mp3)}: Duration {actual_dur:.1f}s is below expected minimum {min_expected_sec:.1f}s ({word_count} words).", flush=True)
            return None
        return output_mp3
    return None

def split_long_theatrical_line(line_item, max_chars=400):
    txt = line_item.get("text", "").strip()
    if len(txt) <= max_chars or not any(c.isalnum() for c in txt):
        return [line_item]
    raw_parts = re.split(r'(?<=[.!?])\s+', txt)
    sentences = []
    for rp in raw_parts:
        if len(rp) <= max_chars:
            sentences.append(rp)
        else:
            sub_parts = re.split(r'(?<=[,;])\s+', rp)
            sub_curr = ""
            for sp in sub_parts:
                if not sub_curr:
                    sub_curr = sp
                elif len(sub_curr) + len(sp) + 1 <= max_chars:
                    sub_curr += " " + sp
                else:
                    sentences.append(sub_curr)
                    sub_curr = sp
            if sub_curr:
                sentences.append(sub_curr)
    result = []
    curr = ""
    for s in sentences:
        if not curr:
            curr = s
        elif len(curr) + len(s) + 1 <= max_chars:
            curr += " " + s
        else:
            result.append(curr)
            curr = s
    if curr:
        result.append(curr)
    expanded = []
    for i, part in enumerate(result):
        item = dict(line_item)
        item["text"] = part
        if i < len(result) - 1:
            item["lead_in_pause"] = "0.45s"
        expanded.append(item)
    return expanded

async def synthesize_theatrical_chunk(chunk_id, lines, output_mp3, force_rebuild=False, sem=None):
    """
    Synthesizes a theatrical multi-character audio chunk using the exact Step 08A casting specs:
    - Parallel speech download via Semaphore
    - Individual line loudness leveling (-16 LUFS, LRA 5, -50dB cutoff)
    - Pacing cushions (. ...... 1.5s, dialogue lead-in 0.22s, sentence 0.45s)
    - Master chunk loudness leveling (-16 LUFS, LRA 6, TP <= -1.5 dBTP)
    """
    if not lines:
        return None

    # Expand any overly long lines into natural sentence-level segments to avoid Edge-TTS payload dropouts
    expanded_lines = []
    for l in lines:
        expanded_lines.extend(split_long_theatrical_line(l, max_chars=400))
    lines = expanded_lines

    word_count = sum(len(line.get("text", "").split()) for line in lines)
    min_expected_sec = max(5.0, (word_count / 160.0) * 60.0 * 0.6)

    if not force_rebuild and os.path.exists(output_mp3) and os.path.getsize(output_mp3) > 10000:
        actual_dur = get_audio_duration(output_mp3)
        if actual_dur >= min_expected_sec:
            return output_mp3
        print(f"       [!] Existing chunk {os.path.basename(output_mp3)} too short ({actual_dur:.1f}s < {min_expected_sec:.1f}s). Rebuilding...", flush=True)

    chunk_dir = os.path.dirname(output_mp3)
    proxy = get_system_proxy()

    async def fetch_line(idx, line_item):
        raw_mp3 = os.path.join(chunk_dir, f"_temp_c{chunk_id}_l{idx}.mp3")
        txt = line_item.get("text", "").strip()
        if not any(c.isalnum() for c in txt):
            # Pure silence/pause line! Generate pure silence directly via ffmpeg
            pad_val = line_item.get("lead_in_pause", "1.20s")
            try:
                silence_dur = min(1.20, max(0.45, float(str(pad_val).replace("s", "").strip())))
            except Exception:
                silence_dur = 1.20
            if not os.path.exists(raw_mp3) or os.path.getsize(raw_mp3) < 500:
                cmd = [
                    FFMPEG_EXE, "-y", "-f", "lavfi",
                    "-i", f"anullsrc=r=48000:cl=mono:d={silence_dur}",
                    "-acodec", "libmp3lame", "-b:a", "48k", raw_mp3
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return idx, os.path.exists(raw_mp3), raw_mp3

        # Reuse existing valid line if already synthesized during retry
        if os.path.exists(raw_mp3) and is_valid_audio_mp3(raw_mp3):
            return idx, True, raw_mp3
        if os.path.exists(raw_mp3):
            try:
                os.remove(raw_mp3)
            except Exception:
                pass

        v = line_item.get("voice", PRIMARY_VOICE_VN)
        p = line_item.get("pitch", "+0Hz")
        r = line_item.get("rate", "-10%")
        ok = await synthesize_speech_voice(txt, v, pitch=p, rate=r, temp_out=raw_mp3, proxy=proxy, sem=sem)
        return idx, ok, raw_mp3

    temp_wavs = []
    chunk_success = False

    for chunk_attempt in range(1, 4):
        fetch_results = []
        for i, line in enumerate(lines):
            res = await fetch_line(i, line)
            fetch_results.append(res)
            await asyncio.sleep(0.12)

        fetch_map = {idx: (ok, mp3) for idx, ok, mp3 in fetch_results}
        temp_wavs = []
        failed_lines = 0

        for i, line in enumerate(lines):
            ok, raw_mp3 = fetch_map[i]
            norm_wav = os.path.join(chunk_dir, f"_temp_c{chunk_id}_l{i}.wav")
            if not ok or not os.path.exists(raw_mp3):
                failed_lines += 1
                print(f"       [!] Chunk {chunk_id} Line {i} ({line.get('speaker')}) failed to synthesize: ok={ok}, exists={os.path.exists(raw_mp3) if raw_mp3 else False}, text={repr(line.get('text', '')[:40])}", flush=True)
                continue

            txt = line.get("text", "")
            if not any(c.isalnum() for c in txt.strip()):
                cmd = [FFMPEG_EXE, "-y", "-i", raw_mp3, "-ar", "48000", "-ac", "1", norm_wav]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(norm_wav):
                    temp_wavs.append(norm_wav)
                continue

            stripped = txt.rstrip()
            prepend_silence = 1.20 if (i == 0 and ". ......" in txt[:20]) else 0.0

            next_txt = lines[i+1].get("text", "").strip() if i < len(lines) - 1 else ""
            next_is_pure_pause_marker = (next_txt == ". ......") or (bool(next_txt) and not any(c.isalnum() for c in next_txt))

            # Determine handoff transition cushion to next line:
            # The gap between line i and line i+1 adopts the lead-in pause of line i+1
            next_line = lines[i+1] if i < len(lines) - 1 else None
            custom_pad = None
            if next_line and not next_is_pure_pause_marker:
                custom_pad = next_line.get("lead_in_pause") or line.get("lead_in_pause")
            else:
                custom_pad = line.get("lead_in_pause")

            if ". ......" in stripped[-20:]:
                # Current line itself ends with pause marker → apply full pause (capped at 1.20s)
                pad_sec = 1.20
            elif next_is_pure_pause_marker:
                # Next line IS the silence marker → it will add its own silence, so apply minimal micro-gap
                pad_sec = 0.08
            elif custom_pad:
                try:
                    pad_sec = float(str(custom_pad).replace("s", "").strip())
                except Exception:
                    pad_sec = 0.55
            elif line.get("type") == "dialogue":
                next_type = next_line.get("type") if next_line else None
                curr_emo = line.get("emotion", "")
                next_emo = next_line.get("emotion", "") if next_line else ""
                if next_type == "dialogue":
                    if any(e in (next_emo, curr_emo) for e in ("cuong_no", "de_doa_tham_hiem", "bang_hoang_chet_lang")) or any(punct in stripped[-3:] for punct in ("!", "!?")):
                        pad_sec = 0.48
                    elif any(e in (next_emo, curr_emo) for e in ("hoi_hop_thi_thao", "doc_thoai_dan_vat", "dau_don_trang_troi", "met_moi_buong_xuoi")):
                        pad_sec = 0.80
                    else:
                        pad_sec = 0.58
                else:
                    pad_sec = 0.60 if stripped.endswith(("!", "?")) else 0.52
            elif line.get("type") == "poem":
                pad_sec = 0.55
            elif stripped.endswith((".", "!", "?")):
                pad_sec = 0.55
            elif stripped.endswith((",", ";", ":")):
                pad_sec = 0.45
            else:
                pad_sec = 0.48

            # When switching speakers (character handoff or narrator-dialogue shift),
            # guarantee at least 0.48s so previous speaker's breath and release are completely finished!
            if next_line and not next_is_pure_pause_marker:
                curr_spk = line.get("speaker")
                next_spk = next_line.get("speaker")
                if curr_spk != next_spk:
                    pad_sec = max(0.48, pad_sec)

            if not next_is_pure_pause_marker:
                pad_sec = max(0.45, min(1.20, pad_sec))

            teq = line.get("timbre_eq")
            try:
                process_audio_segment_ffmpeg(raw_mp3, norm_wav, pad_sec=pad_sec, prepend_silence_sec=prepend_silence, timbre_eq=teq)
                temp_wavs.append(norm_wav)
            except Exception as e:
                print(f"       [!] Error processing theatrical segment {i} FFmpeg: {e}", flush=True)
                failed_lines += 1

        if failed_lines == 0 and len(temp_wavs) == len(lines):
            chunk_success = True
            break
        else:
            print(f"       [!] Theatrical chunk {chunk_id} incomplete: {failed_lines} line(s) failed out of {len(lines)}. Retrying (attempt {chunk_attempt}/3)...", flush=True)
            for tw in temp_wavs:
                if os.path.exists(tw):
                    os.remove(tw)
            if chunk_attempt < 3:
                await asyncio.sleep(2.0 * chunk_attempt)

    if not chunk_success or len(temp_wavs) == 0:
        print(f"       [!] Theatrical chunk {chunk_id} failed after 3 attempts.", flush=True)
        for tw in temp_wavs:
            if os.path.exists(tw):
                os.remove(tw)
        return None

    concat_audio_segments(temp_wavs, output_mp3)
    for tw in temp_wavs:
        if os.path.exists(tw):
            os.remove(tw)

    # Clean up temp raw mp3 files
    for i in range(len(lines)):
        rmp3 = os.path.join(chunk_dir, f"_temp_c{chunk_id}_l{i}.mp3")
        if os.path.exists(rmp3):
            os.remove(rmp3)

    if os.path.exists(output_mp3):
        actual_dur = get_audio_duration(output_mp3)
        if actual_dur < min_expected_sec:
            print(f"       [!] CRITICAL SANITY CHECK FAILED for {os.path.basename(output_mp3)}: Duration {actual_dur:.1f}s < {min_expected_sec:.1f}s ({word_count} words).", flush=True)
            return None
        return output_mp3
    return None

async def synthesize_chapter_tts(chap_dir, chap_name, force_rebuild=False, sem=None):
    parent_dir = os.path.dirname(chap_dir)
    load_custom_glossary(parent_dir)
    load_custom_glossary(chap_dir)

    audio_dir = os.path.join(chap_dir, "audio_chunks")
    os.makedirs(audio_dir, exist_ok=True)

    if sem is None:
        sem = asyncio.Semaphore(4)

    theatrical_path = os.path.join(chap_dir, "theatrical_script.json")
    is_theatrical = os.path.exists(theatrical_path)

    created_chunks = []
    durations = {}

    if is_theatrical:
        with open(theatrical_path, "r", encoding="utf-8") as f:
            theatrical_data = json.load(f)

        chunk_groups = {}
        for item in theatrical_data:
            cid = item.get("chunk_id", 1)
            chunk_groups.setdefault(cid, []).append(item)

        chunk_ids = sorted(chunk_groups.keys())
        total_dialogue = sum(1 for item in theatrical_data if item.get("type") == "dialogue")
        print(f"[*] Step 08B Theatrical TTS Synthesis for {chap_name}: {len(chunk_ids)} chunks ({len(theatrical_data)} lines, {total_dialogue} dialogue)...", flush=True)

        for cid in chunk_ids:
            c_lines = chunk_groups[cid]
            out_mp3 = os.path.join(audio_dir, f"chunk_{cid}.mp3")
            w_count = sum(len(l.get("text", "").split()) for l in c_lines)
            min_expected_sec = max(5.0, (w_count / 160.0) * 60.0 * 0.6)
            dur_sec = get_audio_duration(out_mp3) if os.path.exists(out_mp3) else 0.0

            if not force_rebuild and os.path.exists(out_mp3) and dur_sec >= min_expected_sec:
                created_chunks.append(out_mp3)
                durations[f"chunk_{cid}.mp3"] = dur_sec
                print(f"    -> [SKIP/EXISTING] Chunk {cid} ({len(c_lines)} lines | {dur_sec/60:.2f} min | {os.path.getsize(out_mp3)} bytes): {out_mp3}", flush=True)
                continue

            print(f"    -> [SYNTHESIZING] Chunk {cid} ({len(c_lines)} lines | {w_count} words)...", flush=True)
            res = await synthesize_theatrical_chunk(cid, c_lines, out_mp3, force_rebuild=force_rebuild, sem=sem)
            if res and os.path.exists(out_mp3):
                actual_dur = get_audio_duration(out_mp3)
                created_chunks.append(out_mp3)
                durations[f"chunk_{cid}.mp3"] = actual_dur
                print(f"       [PASSED] Chunk {cid} ({len(c_lines)} lines | {actual_dur/60:.2f} min | {os.path.getsize(out_mp3)} bytes)", flush=True)
            else:
                print(f"       [!] FAILED to synthesize chunk {cid}: {chap_name}", flush=True)

    else:
        # Standard Non-Fiction flow
        manifest_path = os.path.join(audio_dir, ".speech_segments.json")
        manifest = {}
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                print(f"[*] Loaded AI Speech Segments Manifest from {manifest_path} ({len(manifest)} chunks)", flush=True)
            except Exception as e:
                print(f"[!] Could not load speech manifest: {e}", flush=True)
        else:
            try:
                from ai_multilingual_analyzer import analyze_chapter_manifest
            except ImportError:
                from core.ai_multilingual_analyzer import analyze_chapter_manifest
            print("[*] Generating AI Speech Segments Manifest before synthesis...", flush=True)
            manifest = analyze_chapter_manifest(chap_dir)

        kich_ban_dir = os.path.join(chap_dir, "kich-ban")
        target_script_dir = kich_ban_dir if (os.path.isdir(kich_ban_dir) and any(re.match(r'^Kich-ban-\d+\.txt$', f) for f in os.listdir(kich_ban_dir))) else chap_dir

        script_files = sorted([
            os.path.join(target_script_dir, f) for f in os.listdir(target_script_dir)
            if re.match(r'^Kich-ban-\d+\.txt$', f)
        ], key=lambda x: int(re.search(r'Kich-ban-(\d+)\.txt$', os.path.basename(x)).group(1)))

        print(f"[*] Step 08 Dual-Voice TTS Synthesis for {chap_name}: {len(script_files)} chunks...", flush=True)

        for s_path in script_files:
            s_filename = os.path.basename(s_path)
            chunk_num = int(re.search(r'Kich-ban-(\d+)\.txt$', s_filename).group(1))
            out_mp3 = os.path.join(audio_dir, f"chunk_{chunk_num}.mp3")

            dur_sec = get_audio_duration(out_mp3) if os.path.exists(out_mp3) else 0.0
            with open(s_path, "r", encoding="utf-8") as f:
                w_count = len(f.read().split())
            min_expected_sec = max(5.0, (w_count / 160.0) * 60.0 * 0.6)

            if not force_rebuild and os.path.exists(out_mp3) and dur_sec >= min_expected_sec:
                created_chunks.append(out_mp3)
                durations[f"chunk_{chunk_num}.mp3"] = dur_sec
                print(f"    -> [SKIP/EXISTING] Chunk {chunk_num} ({s_filename} | {dur_sec/60:.2f} min | {os.path.getsize(out_mp3)} bytes): {out_mp3}", flush=True)
                continue

            chunk_override = manifest.get(s_filename)
            en_count = sum(1 for item in chunk_override if item["lang"] == "en") if chunk_override else 0
            print(f"    -> [SYNTHESIZING] Chunk {chunk_num} ({s_filename} | {w_count} words | {en_count} English segments)...", flush=True)
            res = await synthesize_script_chunk(s_path, out_mp3, segments_override=chunk_override, force_rebuild=force_rebuild, sem=sem)
            if res and os.path.exists(out_mp3):
                actual_dur = get_audio_duration(out_mp3)
                created_chunks.append(out_mp3)
                durations[f"chunk_{chunk_num}.mp3"] = actual_dur
                print(f"       [PASSED] Chunk {chunk_num} ({s_filename} | {actual_dur/60:.2f} min | {os.path.getsize(out_mp3)} bytes)", flush=True)
            else:
                print(f"       [!] FAILED to synthesize chunk {chunk_num}: {s_path}", flush=True)

    duration_json = os.path.join(chap_dir, ".chunks_duration.json")
    with open(duration_json, "w", encoding="utf-8") as f:
        json.dump(durations, f, indent=2)

    await _update_manifest_step8(chap_dir, chap_name, created_chunks, durations, is_theatrical=is_theatrical)

    return created_chunks

MANIFEST_LOCK = asyncio.Lock()

async def _update_manifest_step8(chap_dir, chap_name, created_chunks, durations, is_theatrical=False):
    parent_dir = os.path.dirname(os.path.abspath(chap_dir))
    manifest_path = os.path.join(parent_dir, ".session_manifest.json")
    if not os.path.exists(manifest_path):
        return
    async with MANIFEST_LOCK:
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            for chap in manifest.get("chapters", []):
                if chap.get("folder") == chap_name:
                    chap["step_8_status"] = "completed"
                    chap["total_audio_chunks"] = len(created_chunks)
                    chap["audio_chunks_dir"] = f"{chap_name}/audio_chunks"
                    tot_dur = sum(durations.values())
                    chap["total_audio_duration_seconds"] = round(tot_dur, 2)
                    chap["total_audio_duration_minutes"] = round(tot_dur / 60, 2)
                    if is_theatrical:
                        chap["theatrical_script"] = f"{chap_name}/theatrical_script.json"
                    else:
                        chap["speech_segments_manifest"] = f"{chap_name}/audio_chunks/.speech_segments.json"
                    break
            all_step8_done = all(c.get("step_8_status") == "completed" for c in manifest.get("chapters", []))
            if all_step8_done:
                manifest["pipeline_stage"] = "08_tts_synthesized"
                manifest["step_8_status"] = "completed"

            tmp_path = manifest_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, manifest_path)
            print(f"[*] Updated Session Manifest for Step 08: {manifest_path}", flush=True)
        except Exception as e:
            print(f"[!] Warning: Could not update manifest for step 8: {e}", flush=True)

def get_audio_duration(mp3_path):
    cmd = [FFMPEG_EXE, "-i", mp3_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    match = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', res.stderr)
    if match:
        h, m, s = match.groups()
        return float(h)*3600 + float(m)*60 + float(s)
    return 180.0

async def process_batch_chapters(book_dir, target_chapters, force_rebuild=False, concurrency=8, chapter_workers=3):
    sem = asyncio.Semaphore(concurrency)
    chap_sem = asyncio.Semaphore(chapter_workers)
    print(f"\n=======================================================")
    print(f" STEP 08: BATCH THEATRICAL TTS SYNTHESIS FOR {len(target_chapters)} CHAPTERS")
    print(f" Request Concurrency: {concurrency} | Chapter Workers: {chapter_workers}")
    print(f" Proxy: {get_system_proxy()}")
    print(f"=======================================================\n")

    total_chaps = len(target_chapters)

    async def worker(idx, chap):
        async with chap_sem:
            chap_folder = chap.get("folder", "")
            c_dir = os.path.join(book_dir, chap_folder)

            # Check if already completed and valid
            if not force_rebuild and chap.get("step_8_status") == "completed":
                audio_dir = os.path.join(c_dir, "audio_chunks")
                tot_chunks = chap.get("total_audio_chunks", 0)
                if os.path.isdir(audio_dir) and tot_chunks > 0:
                    chunk_files = [f for f in os.listdir(audio_dir) if f.startswith("chunk_") and f.endswith(".mp3")]
                    if len(chunk_files) == tot_chunks:
                        print(f"[{idx}/{total_chaps}] Chapter {chap_folder} already completed ({tot_chunks} chunks). Skipping.", flush=True)
                        return

            print(f"\n[{idx}/{total_chaps}] Processing chapter: {chap_folder}...", flush=True)
            try:
                await synthesize_chapter_tts(c_dir, chap_folder, force_rebuild=force_rebuild, sem=sem)
            except Exception as e:
                print(f"[!] Error processing {chap_folder}: {e}", flush=True)

    tasks = [worker(i, c) for i, c in enumerate(target_chapters, start=1)]
    await asyncio.gather(*tasks)

    print(f"\n[✓] Finished batch processing for {len(target_chapters)} chapters.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Step 08: Universal Seamless Dual-Voice TTS & Theatrical Synthesizer")
    parser.add_argument("--chap_dir", type=str, help="Direct path to chapter directory")
    parser.add_argument("--book_dir", type=str, help="Path to book directory")
    parser.add_argument("--chapter", type=str, help="Chapter folder name")
    parser.add_argument("--all", action="store_true", help="Process all chapters in book manifest")
    parser.add_argument("--from_chap", type=int, help="Start chapter index (1-based)")
    parser.add_argument("--to_chap", type=int, help="End chapter index (1-based)")
    parser.add_argument("--concurrency", type=int, default=2, help="Max concurrent Edge-TTS synthesis tasks (default: 2)")
    parser.add_argument("--chapter_workers", type=int, default=1, help="Max chapters being synthesized concurrently (default: 1)")
    parser.add_argument("--force_rebuild", action="store_true", help="Force rebuild existing audio chunks")
    args = parser.parse_args()

    if args.chap_dir:
        c_dir = os.path.abspath(args.chap_dir)
        c_name = os.path.basename(c_dir)
        asyncio.run(synthesize_chapter_tts(c_dir, c_name, force_rebuild=args.force_rebuild, sem=asyncio.Semaphore(args.concurrency)))
    elif args.book_dir and args.chapter:
        c_dir = os.path.abspath(os.path.join(args.book_dir, args.chapter))
        c_name = args.chapter
        asyncio.run(synthesize_chapter_tts(c_dir, c_name, force_rebuild=args.force_rebuild, sem=asyncio.Semaphore(args.concurrency)))
    elif args.book_dir and (args.all or args.from_chap or args.to_chap):
        manifest_path = os.path.join(args.book_dir, ".session_manifest.json")
        if not os.path.exists(manifest_path):
            print(f"[!] Manifest not found in {args.book_dir}")
            sys.exit(1)
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        chaps = manifest.get("chapters", [])
        if args.from_chap or args.to_chap:
            start_i = (args.from_chap - 1) if args.from_chap else 0
            end_i = args.to_chap if args.to_chap else len(chaps)
            chaps = chaps[start_i:end_i]
        asyncio.run(process_batch_chapters(args.book_dir, chaps, force_rebuild=args.force_rebuild, concurrency=args.concurrency, chapter_workers=args.chapter_workers))
    else:
        chap = "00-Preface"
        c_dir = os.path.join("Kich-ban-clipchamp/ProcessGroupsPracticeGuide", chap)
        c_name = chap
        asyncio.run(synthesize_chapter_tts(c_dir, c_name, force_rebuild=args.force_rebuild))


