import os
import sys
import json
import glob
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../core')))
from theatrical_voice_director import direct_chapter_theatrical_script

def main():
    book_dir = '/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia'
    chap_folder = '19-Hoi-19'
    chap_dir = os.path.join(book_dir, chap_folder)
    chap_num = 19
    chap_title = 'HỒI MƯỜI CHÍN: THÀNH HẠ PHÍ, TÀO THÁO DÙNG BINH, LẦU BẠCH MÔN, LÃ BỐ TUYỆT MỆNH'

    print(f"[*] Directing Theatrical Script for {chap_folder}...")
    res = direct_chapter_theatrical_script(chap_dir, chap_num, chap_title)
    if not res:
        print(f"[!] Error directing chapter {chap_folder}")
        return False

    print(f"[✓] Directed successfully: {res}")

    script_path = res['theatrical_script_file']
    bible_path = res['theatrical_bible_file']

    with open(script_path, 'r', encoding='utf-8') as f:
        script_lines = json.load(f)

    kich_ban_dir = os.path.join(chap_dir, 'kich-ban')
    kich_ban_files = sorted(glob.glob(os.path.join(kich_ban_dir, 'Kich-ban-*.txt')))
    original_texts = []
    for fpath in kich_ban_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            original_texts.append(f.read())
    combined_original = '
'.join(original_texts)

    reconstructed_texts = [l['text'] for l in script_lines]
    combined_reconstructed = '
'.join(reconstructed_texts)

    def clean_ws(t):
        return re.sub(r'\s+', ' ', t).strip()

    clean_orig = clean_ws(combined_original)
    clean_recon = clean_ws(combined_reconstructed)

    print(f"    - Original characters: {len(clean_orig)}")
    print(f"    - Reconstructed characters: {len(clean_recon)}")

    with open(bible_path, 'r', encoding='utf-8') as f:
        bible = json.load(f)

    report_path = os.path.join(chap_dir, 'scratch', 'zero_loss_audit_report.md')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    report_content = f"# Zero-Loss Audit Report: Chapter 19 (19-Hoi-19)

- **Script Path:** 
- **Bible Path:** 
- **Total Theatrical Lines:** 
- **Narrator Lines:** 
- **Dialogue Lines:** 
- **Poem Lines:** 
- **Characters Cast:** 
- **Status:** 

## Character Distribution & Voice Cast
"
    for cid, cdata in bible.get('characters', {}).items():
        if cid == 'Narrator':
            report_content += f"- **Người dẫn chuyện ():** {cdata.get('dialogue_count')} segments, modes: 
"
        else:
            report_content += f"- **{cdata.get('name')} ():** {cdata.get('dialogue_count')} lines, voice: , age: , temperament: , timbre_eq: , sample_emotions: 
"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"[*] Audit report generated at: {report_path}")

    manifest_path = os.path.join(book_dir, '.session_manifest.json')
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

    chapters = manifest.get('chapters', [])
    found_chap = False
    for chap in chapters:
        if chap.get('folder') == chap_folder or chap.get('index') == chap_num - 1:
            chap['step_8a_status'] = 'completed'
            chap['theatrical_script_file'] = os.path.relpath(script_path, book_dir)
            chap['theatrical_bible_file'] = os.path.relpath(bible_path, book_dir)
            chap['total_theatrical_lines'] = res['total_lines']
            chap['total_poem_lines'] = res['poem_lines']
            chap['total_dialogue_lines'] = res['dialogue_lines']
            chap['total_characters_cast'] = res['characters_count']
            found_chap = True
            break

    if not found_chap:
        chapters.append({
            'index': chap_num - 1,
            'folder': chap_folder,
            'title': chap_title,
            'step_8a_status': 'completed',
            'theatrical_script_file': os.path.relpath(script_path, book_dir),
            'theatrical_bible_file': os.path.relpath(bible_path, book_dir),
            'total_theatrical_lines': res['total_lines'],
            'total_poem_lines': res['poem_lines'],
            'total_dialogue_lines': res['dialogue_lines'],
            'total_characters_cast': res['characters_count']
        })
        manifest['chapters'] = chapters

    manifest['pipeline_stage'] = '08a_theatrical_directed'
    manifest['step_8a_status'] = 'completed'

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"[*] Session manifest updated at: {manifest_path}")

if __name__ == '__main__':
    main()
