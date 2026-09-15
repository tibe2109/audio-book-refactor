#!/usr/bin/env python3
# ==============================================================================
# Step 08: Universal AI Multilingual Semantic Analyzer
# Skill: arf_08_tts_neural_bgm_mixer
# ==============================================================================
# Purpose: AI directly analyzes script content, dynamically extracts English
# terminology, titles, acronyms, and foreign vocabulary based on contextual
# semantics, and generates .speech_segments.json BEFORE audio synthesis.
# ==============================================================================

import os
import re
import json
import argparse
from typing import List, Dict, Tuple

try:
    from vietnamese_syllables import VIETNAMESE_SYLLABLES_SET
except ImportError:
    try:
        from core.vietnamese_syllables import VIETNAMESE_SYLLABLES_SET
    except ImportError:
        VIETNAMESE_SYLLABLES_SET = set()

# Regex for Vietnamese diacritics
VI_DIACRITICS_REGEX = re.compile(
    r'[àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]'
)

# Acronym patterns
HYPHENATED_ACRONYM = re.compile(r'^[a-zA-Z](-[a-zA-Z])+$')
ALLCAPS_ACRONYM = re.compile(r'^[A-Z]{2,6}$')

# System English dictionary
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

# Common English connectors & functional particles
ENGLISH_CONNECTORS = {
    'and', 'or', 'of', 'for', 'in', 'on', 'at', 'to', 'with', 'by', 'from',
    'the', 'a', 'an', 'as', 'is', 'are', 'it', 'its', 'their', 'this', 'that',
    'into', 'about', 'over', 'through', 'between', 'under', 'via', 'vs'
}

# Ambiguous tokens that could be VN unaccented syllable or short EN word
AMBIGUOUS_SHARED_TOKENS = {
    'a', 'an', 'in', 'on', 'at', 'to', 'do', 'so', 'no', 'can', 'may', 'bay',
    'lay', 'day', 'chat', 'con', 'ca', 'ma', 'la', 'ra', 'va', 'di', 'me', 'he',
    'be', 'of', 'for', 'the', 'as', 'by', 'with', 'from', 'up', 'out', 'is',
    'are', 'it', 'or', 'and', 'vs', 'via'
}

# Universal Foreign Morphological Affixes
FOREIGN_SUFFIXES = re.compile(
    r'(tion|sion|ment|ance|ence|able|ible|tive|sive|ship|ing|ed|al|ic|ical|ous|ity|ism|ist|logy|graphy|ture|ure|est|less|ness|hood|wise|ward|ful|fully|ly|ize|ise|ify|ate|ian|ious|eous)s?$',
    re.I
)
FOREIGN_PREFIXES = re.compile(
    r'^(str|spr|scr|spl|squ|shr|thr|fl|fr|gl|gr|pl|pr|bl|br|cl|cr|dr|sk|sp|st|sm|sn|sc|sw|wr|kn|ps|rh|sch|chr|phr|tw|dw|wh)',
    re.I
)
FOREIGN_ENDINGS = re.compile(
    r'(ct|ft|pt|lt|rt|st|sk|sp|mp|nd|nt|nk|rk|lk|rd|ld|rn|rm|lm|sm|ts|ks|ps|nce|nse|rce|rse|tch|dge|que|the|ble|ple|fle|gle|kle|tle|dle|ght|sh|th|ph|[bdfjklrsvwxz])$',
    re.I
)

def clean_token(token: str) -> str:
    return token.strip(".,?!:;()[]\"'“”‘’—–")

def is_foreign_token(word: str, custom_glossary: set = None) -> bool:
    clean_w = clean_token(word).lower()
    raw_clean = clean_token(word)
    if not clean_w:
        return False

    # 1. Any Vietnamese diacritics -> 100% Vietnamese
    if VI_DIACRITICS_REGEX.search(word):
        return False

    # 2. Custom project glossary
    if custom_glossary and clean_w in custom_glossary:
        return True

    # 3. Hyphenated spelled-out acronyms (P-M-I, W-B-S, K-P-I, A-I, I-T) -> 100% English
    if HYPHENATED_ACRONYM.match(raw_clean):
        return True

    # 4. Explicit tech acronyms (AI, IT, CV, HR)
    if raw_clean in {'AI', 'IT', 'CV', 'HR', 'DNA'}:
        return True

    # 5. Non-Vietnamese characters (w, z, j, f)
    if re.search(r'[wzjf]', clean_w):
        return True

    # 6. If it's a known unaccented Vietnamese syllable -> default Vietnamese
    # (Prevents all-caps Vietnamese titles from false acronym trigger)
    if clean_w in VIETNAMESE_SYLLABLES_SET:
        return False

    # 7. All-caps acronyms of 2-6 chars without accents (PMI, WBS, KPI, SLA, SWOT, PMP, PMO)
    if ALLCAPS_ACRONYM.match(raw_clean):
        return True

    # 8. Foreign Morphological Suffixes
    if FOREIGN_SUFFIXES.search(clean_w):
        return True

    # 9. Foreign Consonant Clusters (Prefixes & Final clusters)
    if FOREIGN_PREFIXES.search(clean_w) or FOREIGN_ENDINGS.search(clean_w):
        return True

    # 10. Foreign Diphthongs & Double Consonants
    if re.search(r'(ea|ee|oo|ou|ei|ey|oy|au|aw|ow|ew)', clean_w):
        return True
    if re.search(r'([b-df-hj-np-tv-z])\1', clean_w):
        return True

    # 11. System English Dictionary Lookup
    if clean_w in SYSTEM_ENGLISH_WORDS:
        return True

    return False

def clean_speech_text(text: str, is_sentence_end: bool = False) -> str:
    # Strip non-speakable Unicode bullet symbols and icons
    t = re.sub(r'[▶►▪●★▲◆■✓•–—…|/\\\\]', ' ', text)
    t = t.replace('. ......', ', ')
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

def is_speakable(text: str) -> bool:
    return bool(re.search(r'[A-Za-z0-9àáảãạâăêôơưđÀÁẢÃẠÂĂÊÔƠƯĐ]', text))

def analyze_script_to_segments(text: str, custom_glossary: set = None) -> List[Dict[str, str]]:
    """
    Parses a single script into dynamic language segments:
    [{'lang': 'vi', 'text': '...'}, {'lang': 'en', 'text': '...'}]
    """
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

    flags = [is_foreign_token(w, custom_glossary) for w in words]

    # Pre-pass: Clause-level English title and phrase detection
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
        cl_words = [w for idx, w in cl if clean_token(w)]
        has_vi_diacritic = any(VI_DIACRITICS_REGEX.search(w) for w in cl_words)
        if not has_vi_diacritic and len(cl_words) >= 2:
            strict_foreign_count = sum(1 for idx, w in cl if flags[idx] and clean_token(w))
            all_compat = all(
                (clean_token(w).lower() in AMBIGUOUS_SHARED_TOKENS or
                 clean_token(w).lower() in SYSTEM_ENGLISH_WORDS or
                 flags[idx])
                for idx, w in cl if clean_token(w)
            )
            # If at least 1 strict foreign token and all tokens compatible, and ratio >= 35%
            if strict_foreign_count >= 1 and all_compat and (strict_foreign_count / len(cl_words)) >= 0.35:
                for idx, w in cl:
                    if clean_token(w):
                        flags[idx] = True

    # Leading article propagation: if a token is in {'the', 'a', 'an'} and followed by foreign token
    for i in range(len(words) - 1):
        if not flags[i] and clean_token(words[i]).lower() in {'the', 'a', 'an'} and flags[i+1]:
            if i == 0 or any(words[i-1].endswith(p) for p in [',', '.', '!', '?', ';', ':', '…']) or is_line_end[i-1]:
                flags[i] = True

    # Multi-token connector bridging:
    # Any span of 1 to 4 connector/ambiguous words between foreign tokens becomes foreign
    n = len(words)
    i = 0
    while i < n:
        if flags[i]:
            j = i + 1
            while j < n and j <= i + 4 and not flags[j]:
                cw = clean_token(words[j]).lower()
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

    output_segments = []
    total_segs = len(segments)
    for idx, (lang, seg_str) in enumerate(segments):
        is_last = (idx == total_segs - 1)
        stripped_raw = seg_str.rstrip()
        has_comma = bool(re.search(r'[,;:]$', stripped_raw))
        has_terminal = bool(re.search(r'[.!?…]$', stripped_raw))

        clean_str = clean_speech_text(seg_str, is_sentence_end=is_last)
        if is_speakable(clean_str):
            pause_type = "emphasis" if has_comma else ("terminal" if (has_terminal or is_last) else "seamless")
            output_segments.append({"lang": lang, "text": clean_str, "pause_type": pause_type})

    return output_segments

def analyze_chapter_manifest(chap_dir: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Analyzes all Kich-ban-*.txt scripts in a chapter, creates and saves
    audio_chunks/.speech_segments.json.
    """
    audio_dir = os.path.join(chap_dir, "audio_chunks")
    os.makedirs(audio_dir, exist_ok=True)

    # Load custom book glossary if available
    custom_glossary = set()
    for gp in [os.path.join(chap_dir, "custom_phonetics.json"),
               os.path.join(os.path.dirname(chap_dir), "custom_phonetics.json"),
               os.path.join(chap_dir, "pmbok_custom_phonetics.json"),
               os.path.join(os.path.dirname(chap_dir), "pmbok_custom_phonetics.json")]:
        if os.path.exists(gp):
            try:
                with open(gp, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    if isinstance(d, dict):
                        for k in d.keys():
                            for w in k.split():
                                custom_glossary.add(w.lower())
                    elif isinstance(d, list):
                        for item in d:
                            for w in str(item).split():
                                custom_glossary.add(w.lower())
                print(f"[*] Loaded custom glossary from {gp} ({len(custom_glossary)} terms)", flush=True)
            except Exception as e:
                print(f"[!] Error reading glossary {gp}: {e}", flush=True)

    kich_ban_dir = os.path.join(chap_dir, "kich-ban")
    target_script_dir = kich_ban_dir if (os.path.isdir(kich_ban_dir) and any(re.match(r'^Kich-ban-\d+\.txt$', f) for f in os.listdir(kich_ban_dir))) else chap_dir

    script_files = sorted([
        f for f in os.listdir(target_script_dir)
        if re.match(r'^Kich-ban-\d+\.txt$', f)
    ], key=lambda x: int(re.search(r'Kich-ban-(\d+)\.txt$', x).group(1)))

    manifest = {}
    stats_terms = set()

    for sf in script_files:
        sf_path = os.path.join(target_script_dir, sf)
        with open(sf_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        segments = analyze_script_to_segments(text, custom_glossary)
        manifest[sf] = segments
        for seg in segments:
            if seg["lang"] == "en":
                stats_terms.add(seg["text"])

    manifest_path = os.path.join(audio_dir, ".speech_segments.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[*] AI Semantic Analysis Complete for {os.path.basename(chap_dir)}:", flush=True)
    print(f"    - Scripts Analyzed: {len(script_files)} files", flush=True)
    print(f"    - Unique English Terms/Phrases Extracted: {len(stats_terms)} phrases", flush=True)
    print(f"    - Speech Segments Manifest: {manifest_path}", flush=True)

    return manifest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Multilingual Semantic Analyzer")
    parser.add_argument("--chap_dir", required=True, type=str, help="Path to chapter folder")
    args = parser.parse_args()

    analyze_chapter_manifest(os.path.abspath(args.chap_dir))
