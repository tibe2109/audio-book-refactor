import subprocess

def run(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

core_names = [
    "antigravity_audiobook_pipeline.py",
    "theatrical_voice_director.py",
    "universal_audiobook_workflow.py",
    "audio_smart_aggregator_bgm.py",
    "batch_author_translator.py",
    "extract_pdf_structure.py",
    "refine_script_prosody.py",
    "vietnamese_syllables.py",
    "ai_multilingual_analyzer.py",
    "format_all_script_structures.py",
    "seamless_dual_voice_splicer.py",
    "audiobook_script_processor.py"
]

print("=== SEARCHING GIT LOG FOR CORE SCRIPT NAMES ===")
for name in core_names:
    log = run(f'git log --all --full-history -- "*{name}"')
    if log:
        print(f"FOUND IN GIT: {name}")
        print(run(f'git log --all --full-history --oneline -- "*{name}"'))
    else:
        print(f"NOT IN GIT: {name}")
