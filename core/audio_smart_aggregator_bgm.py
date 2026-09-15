#!/usr/bin/env python3
# ==============================================================================
# Step 09 & 10: Audio Smart Aggregator & BGM Dynamic Mastering
# Skills: arf_09_audio_smart_aggregator, arf_10_bgm_dynamic_mixer
# ==============================================================================
import os
import re
import json
import argparse
import subprocess
import shutil
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def get_audio_duration(file_path):
    cmd = [FFMPEG_EXE, "-i", file_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    match = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', res.stderr)
    if match:
        h, m, s = match.groups()
        return float(h)*3600 + float(m)*60 + float(s)
    return 0.0

def partition_chunks_equitable(chunk_files, durations, target_sec=1800.0, hard_cap_max_sec=2100.0):
    """
    Equitable Distribution Algorithm for Audiobook Partitioning.
    Guarantees:
      1. Every part duration <= hard_cap_max_sec (35 mins).
      2. Avoids greedy starvation (no short leftover chunks).
      3. Minimizes variance around ideal target (total_duration / N).
    """
    total_dur = sum(durations)
    if total_dur <= hard_cap_max_sec:
        return [chunk_files]

    num_parts = max(2, round(total_dur / target_sec))
    n = len(chunk_files)

    for k_parts in range(num_parts, n + 1):
        target = total_dur / k_parts
        memo = {}

        def solve(idx, rem):
            if rem == 1:
                part_dur = sum(durations[idx:])
                if part_dur > hard_cap_max_sec:
                    return (float("inf"), [])
                cost = (part_dur - target) ** 2
                return (cost, [[idx, n]])

            state = (idx, rem)
            if state in memo:
                return memo[state]

            best_cost = float("inf")
            best_splits = []
            curr_dur = 0.0

            for next_idx in range(idx + 1, n - rem + 2):
                curr_dur += durations[next_idx - 1]
                if curr_dur > hard_cap_max_sec:
                    break
                rest_cost, rest_splits = solve(next_idx, rem - 1)
                if rest_cost != float("inf"):
                    total_cost = (curr_dur - target) ** 2 + rest_cost
                    if total_cost < best_cost:
                        best_cost = total_cost
                        best_splits = [[idx, next_idx]] + rest_splits

            memo[state] = (best_cost, best_splits)
            return memo[state]

        cost, splits = solve(0, k_parts)
        if cost != float("inf"):
            result_parts = []
            for s_idx, e_idx in splits:
                result_parts.append(chunk_files[s_idx:e_idx])
            return result_parts

    # Fallback to greedy if exact dynamic partition not found
    print("[!] Fallback to greedy partitioning")
    parts, curr_p, curr_d = [], [], 0.0
    for cf, d in zip(chunk_files, durations):
        if curr_d + d > hard_cap_max_sec and curr_p:
            parts.append(curr_p)
            curr_p = [cf]
            curr_d = d
        else:
            curr_p.append(cf)
            curr_d += d
    if curr_p:
        parts.append(curr_p)
    return parts

def smart_aggregate_audio(chap_dir, chap_name):
    """
    Step 09: Audio Smart Aggregator
    Analyzes all audio chunks in chap_dir/audio_chunks, computes equitable partitions,
    and losslessly concatenates into Full_{chap_name}_Part{Y}.mp3.
    """
    audio_dir = os.path.join(chap_dir, "audio_chunks")
    if not os.path.exists(audio_dir):
        print(f"[!] audio_chunks directory not found in {chap_dir}")
        return []

    chunk_files = sorted([
        os.path.join(audio_dir, f) for f in os.listdir(audio_dir)
        if re.match(r'^chunk_\d+\.mp3$', f)
    ], key=lambda x: int(re.search(r'^chunk_(\d+)\.mp3$', os.path.basename(x)).group(1)))

    if not chunk_files:
        print(f"[!] No audio chunks found in {audio_dir}")
        return []

    print(f"\n=========================================================")
    print(f" STEP 09: Audio Smart Aggregator for {chap_name}")
    print(f"=========================================================")

    # Step 1: Scan & Calculate Durations
    durations = [get_audio_duration(cf) for cf in chunk_files]
    total_duration = sum(durations)

    print(f"[*] Step 1: Scanned {len(chunk_files)} audio chunks:")
    print(f"    -> Total Audio Duration: {total_duration:.2f}s ({total_duration/60:.2f} minutes)")

    # Step 2: Equitable Distribution Partitioning
    parts = partition_chunks_equitable(chunk_files, durations)
    print(f"\n[*] Step 2: Formulated Equitable Distribution Plan ({len(parts)} Part(s)):")

    partition_plan = []
    for p_idx, p_chunks in enumerate(parts, 1):
        p_durs = [durations[chunk_files.index(c)] for c in p_chunks]
        p_tot = sum(p_durs)
        c_start = os.path.basename(p_chunks[0])
        c_end = os.path.basename(p_chunks[-1])
        print(f"    -> Part {p_idx}: {len(p_chunks)} chunks ({c_start} .. {c_end}) | Duration: {p_tot:.2f}s ({p_tot/60:.2f} mins)")
        partition_plan.append({
            "part_index": p_idx,
            "chunk_count": len(p_chunks),
            "start_chunk": c_start,
            "end_chunk": c_end,
            "duration_seconds": round(p_tot, 2),
            "duration_minutes": round(p_tot / 60, 2),
            "chunks": [os.path.basename(c) for c in p_chunks]
        })

    # Determine centralized Full output directory for the entire book
    book_dir = os.path.dirname(os.path.abspath(chap_dir))
    book_name = os.path.basename(book_dir)
    full_output_dir = os.path.join(book_dir, f"Full-{book_name}")
    os.makedirs(full_output_dir, exist_ok=True)

    # Step 3: Concat Execution
    print(f"\n[*] Step 3: Executing Stream-Copy Audio Concatenation via FFmpeg...")
    print(f"    -> Output Directory (Full without music): {full_output_dir}")
    full_output_files = []

    for p_idx, p_chunks in enumerate(parts, 1):
        part_suffix = f"Part{p_idx}" if len(parts) > 1 else "Part1"
        full_mp3 = os.path.join(full_output_dir, f"Full_{chap_name}_{part_suffix}.mp3")
        list_txt = full_mp3 + ".concat.txt"

        with open(list_txt, "w", encoding="utf-8") as f:
            for c in p_chunks:
                f.write(f"file '{os.path.abspath(c)}'\n")

        cmd_concat = [
            FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
            "-i", list_txt,
            "-c", "copy",
            full_mp3
        ]
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        if os.path.exists(list_txt):
            os.remove(list_txt)

        # Clean up legacy Full file in chap_dir if it exists
        legacy_full = os.path.join(chap_dir, f"Full_{chap_name}_{part_suffix}.mp3")
        if os.path.exists(legacy_full) and os.path.abspath(legacy_full) != os.path.abspath(full_mp3):
            try:
                os.remove(legacy_full)
            except Exception:
                pass

        # Step 4: Post-Execution Validation
        if not os.path.exists(full_mp3):
            raise RuntimeError(f"Failed to produce concatenated audio file: {full_mp3}")

        file_size_mb = os.path.getsize(full_mp3) / (1024 * 1024)
        actual_dur = get_audio_duration(full_mp3)
        expected_dur = partition_plan[p_idx - 1]["duration_seconds"]
        dur_delta = abs(actual_dur - expected_dur)
        if dur_delta > 2.0:
            raise RuntimeError(
                f"Audio concatenation integrity check failed for {os.path.basename(full_mp3)}: "
                f"Actual duration ({actual_dur:.2f}s) differs from expected chunk sum ({expected_dur:.2f}s) "
                f"by {dur_delta:.2f}s (> 2.0s allowed threshold). Possible audio truncation!"
            )

        print(f"    -> [✓] Part {p_idx} Created in Full-{book_name}: {os.path.basename(full_mp3)}")
        print(f"           Duration: {actual_dur:.2f}s ({actual_dur/60:.2f} mins) | Delta: {dur_delta:.2f}s | Size: {file_size_mb:.2f} MB")

        full_output_files.append({
            "part_index": p_idx,
            "file_name": os.path.basename(full_mp3),
            "file_path": full_mp3,
            "duration_seconds": round(actual_dur, 2),
            "duration_minutes": round(actual_dur / 60, 2),
            "file_size_mb": round(file_size_mb, 2),
            "chunks": [os.path.basename(c) for c in p_chunks]
        })

    # Update manifest if present
    _update_manifest_step9(chap_dir, chap_name, full_output_files, total_duration)

    return full_output_files

def _update_manifest_step9(chap_dir, chap_name, full_output_files, total_duration):
    """Update parent .session_manifest.json with Step 09 details."""
    parent_dir = os.path.dirname(os.path.abspath(chap_dir))
    manifest_path = os.path.join(parent_dir, ".session_manifest.json")
    if not os.path.exists(manifest_path):
        return

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        for chap in manifest.get("chapters", []):
            if chap.get("folder") == chap_name:
                chap["step_9_status"] = "completed"
                chap["status"] = "audio_aggregated"
                chap["total_full_parts"] = len(full_output_files)
                chap["full_audio_files"] = [f["file_name"] for f in full_output_files]
                chap["full_parts_details"] = full_output_files
                break

        manifest["full_output_folder"] = f"Full-{os.path.basename(parent_dir)}"
        manifest["step_9_status"] = "in_progress"
        # Check if all completed
        all_done = all(c.get("step_9_status") == "completed" for c in manifest.get("chapters", []))
        if all_done:
            manifest["step_9_status"] = "completed"
            manifest["pipeline_stage"] = "09_audio_aggregated"

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"[*] Updated Session Manifest: {manifest_path}")
    except Exception as e:
        print(f"[!] Warning: Could not update manifest: {e}")

def resolve_bgm_file(bgm_file="nhac-nen.mp3"):
    """
    Resolves BGM audio file path in priority order:
    1. Direct file path if exists (absolute or relative to CWD)
    2. File inside bgm_audio_library/ directory (e.g. bgm_audio_library/<bgm_file>)
    3. Project root directory fallback (e.g. nhac-nen.mp3)
    4. First .mp3 in bgm_audio_library/ if default requested and nhac-nen.mp3 not found
    """
    if not bgm_file:
        return None
    # 1. Direct path
    if os.path.exists(bgm_file):
        return os.path.abspath(bgm_file)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 2. Inside bgm_audio_library/ or root
    for base in [os.getcwd(), project_root]:
        candidate_lib = os.path.join(base, "bgm_audio_library", bgm_file)
        if os.path.exists(candidate_lib):
            return os.path.abspath(candidate_lib)
        candidate_direct = os.path.join(base, bgm_file)
        if os.path.exists(candidate_direct):
            return os.path.abspath(candidate_direct)

    # 3. Fallback: first .mp3 in bgm_audio_library
    for base in [os.getcwd(), project_root]:
        lib_dir = os.path.join(base, "bgm_audio_library")
        if os.path.exists(lib_dir):
            mp3s = sorted([os.path.join(lib_dir, f) for f in os.listdir(lib_dir) if f.lower().endswith(".mp3")])
            if mp3s:
                return os.path.abspath(mp3s[0])

    return None

def dynamic_bgm_mixer(chap_dir, chap_name, full_parts=None, bgm_file="nhac-nen.mp3"):
    """
    Step 10: Dynamic BGM Dynamic Mastering (AI Music Director)
    Mixes BGM with dynamic ducking (-20dB), volume retention, and True Seamless Part Cut rules:
      - Part 1: 3.0s Fade-in at start, raw cut at end (no fade-out).
      - Middle parts: Raw cut entry and exit (no fade-in/out).
      - Last part: Raw cut entry, 5.0s Fade-out at end.
      - Continuous BGM timeline offset across parts.
    """
    book_dir = os.path.dirname(os.path.abspath(chap_dir))
    book_name = os.path.basename(book_dir)
    full_output_dir = os.path.join(book_dir, f"Full-{book_name}")
    final_output_dir = os.path.join(book_dir, f"Final-{book_name}")
    os.makedirs(final_output_dir, exist_ok=True)

    if full_parts is None:
        # Search Full-[book_name] first, fallback to chap_dir
        search_dirs = [full_output_dir, chap_dir]
        full_files = []
        for s_dir in search_dirs:
            if os.path.exists(s_dir):
                found = sorted([
                    os.path.join(s_dir, f) for f in os.listdir(s_dir)
                    if f.startswith(f"Full_{chap_name}") and f.endswith(".mp3")
                ], key=lambda x: int(re.search(r'Part(\d+)', x).group(1)) if re.search(r'Part(\d+)', x) else 1)
                if found:
                    full_files = found
                    break
    else:
        full_files = [p["file_path"] if isinstance(p, dict) else p for p in full_parts]

    if not full_files:
        print(f"[!] No Full audio files found for {chap_name} to mix BGM (searched {full_output_dir} and {chap_dir})")
        return []

    print(f"\n=========================================================")
    print(f" STEP 10: Dynamic BGM Mastering (AI Music Director) for {chap_name}")
    print(f"=========================================================")
    print(f"    -> Output Directory (Final with music): {final_output_dir}")

    final_master_files = []
    total_parts = len(full_files)
    bgm_path = resolve_bgm_file(bgm_file)

    if not bgm_path:
        print(f"[!] BGM file not found (checked '{bgm_file}' and 'bgm_audio_library/'). Will export unmixed masters.")
    else:
        print(f"    -> Selected BGM Track: {bgm_path}")

    # Timeline Architect: track cumulative offset across parts
    current_bgm_offset = 0.0

    for p_idx, full_mp3 in enumerate(full_files, 1):
        part_suffix = f"Part{p_idx}" if total_parts > 1 else "Part1"
        final_mp3 = os.path.join(final_output_dir, f"Final_Audio_{chap_name}_{part_suffix}.mp3")
        part_duration = get_audio_duration(full_mp3)

        is_first_part = (p_idx == 1)
        is_last_part = (p_idx == total_parts)

        bgm_start = current_bgm_offset
        bgm_end = current_bgm_offset + part_duration
        current_bgm_offset += part_duration

        print(f"\n[*] Mastering Part {p_idx}/{total_parts}: {os.path.basename(full_mp3)}")
        print(f"    -> Speech Duration: {part_duration:.2f}s ({part_duration/60:.2f} mins)")
        print(f"    -> BGM Timeline Window: {bgm_start:.2f}s ➔ {bgm_end:.2f}s")

        if bgm_path:
            # Seamless Part Cut Rules:
            # Part 1: Fade-in 3.0s, NO fade-out
            # Middle: NO fade-in, NO fade-out
            # Last: NO fade-in, Fade-out 5.0s
            bgm_filters = [
                f"atrim=start={bgm_start:.2f}:end={bgm_end:.2f}",
                "asetpts=PTS-STARTPTS",
                "volume=0.10"
            ]

            if is_first_part:
                bgm_filters.append("afade=t=in:ss=0:d=3.0")
                print("    -> Applied: 3.0s Fade-In (Part 1 Start)")
            else:
                print("    -> Applied: Raw Continuous Cut Entry (No Fade-In)")

            if is_last_part:
                bgm_filters.append(f"afade=t=out:st={max(0.0, part_duration - 5.0):.2f}:d=5.0")
                print("    -> Applied: 5.0s Fade-Out (Final Outro End)")
            else:
                print("    -> Applied: Raw Continuous Cut Exit (No Fade-Out)")

            bgm_chain = ",".join(bgm_filters)

            # Voice preservation: loudnorm broadcast standard (Spotify/Audible/YouTube -16 LUFS)
            filter_complex = (
                f"[0:a]aformat=channel_layouts=stereo[voice];"
                f"[1:a]{bgm_chain}[bgm];"
                f"[voice][bgm]amix=inputs=2:duration=first:weights=1 1:normalize=0,"
                f"loudnorm=I=-16:TP=-1.5:LRA=6[out]"
            )

            cmd_mix = [
                FFMPEG_EXE, "-y",
                "-i", full_mp3,
                "-stream_loop", "-1",  # Loop BGM infinitely to match any part duration
                "-i", bgm_path,
                "-filter_complex", filter_complex,
                "-map", "[out]",
                "-b:a", "192k",
                "-ar", "48000",
                final_mp3
            ]
        else:
            cmd_mix = [
                FFMPEG_EXE, "-y",
                "-i", full_mp3,
                "-b:a", "192k",
                "-ar", "48000",
                final_mp3
            ]

        subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Validate master file
        if not os.path.exists(final_mp3):
            raise RuntimeError(f"Master file failed to generate: {final_mp3}")

        # Clean up legacy Final file in chap_dir if it exists
        legacy_final = os.path.join(chap_dir, f"Final_Audio_{chap_name}_{part_suffix}.mp3")
        if os.path.exists(legacy_final) and os.path.abspath(legacy_final) != os.path.abspath(final_mp3):
            try:
                os.remove(legacy_final)
            except Exception:
                pass

        sz_mb = os.path.getsize(final_mp3) / (1024 * 1024)
        out_dur = get_audio_duration(final_mp3)
        print(f"    -> [✓] MASTER RENDER COMPLETE in Final-{book_name}: {os.path.basename(final_mp3)}")
        print(f"           Duration: {out_dur:.2f}s ({out_dur/60:.2f} mins) | Size: {sz_mb:.2f} MB")

        final_master_files.append({
            "part_index": p_idx,
            "file_name": os.path.basename(final_mp3),
            "file_path": final_mp3,
            "duration_seconds": round(out_dur, 2),
            "duration_minutes": round(out_dur / 60, 2),
            "file_size_mb": round(sz_mb, 2)
        })

    # Update manifest for Step 10
    _update_manifest_step10(chap_dir, chap_name, final_master_files)

    return final_master_files

def _update_manifest_step10(chap_dir, chap_name, final_master_files):
    """Update parent .session_manifest.json with Step 10 completion details."""
    parent_dir = os.path.dirname(os.path.abspath(chap_dir))
    manifest_path = os.path.join(parent_dir, ".session_manifest.json")
    if not os.path.exists(manifest_path):
        return

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        for chap in manifest.get("chapters", []):
            if chap.get("folder") == chap_name:
                chap["step_10_status"] = "completed"
                chap["status"] = "bgm_mastered"
                chap["final_master_files"] = [f["file_name"] for f in final_master_files]
                chap["final_master_details"] = final_master_files
                break

        manifest["final_output_folder"] = f"Final-{os.path.basename(parent_dir)}"
        manifest["step_10_status"] = "in_progress"
        all_done = all(c.get("step_10_status") == "completed" for c in manifest.get("chapters", []))
        if all_done:
            manifest["step_10_status"] = "completed"
            manifest["pipeline_stage"] = "10_bgm_mastered"

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"[*] Updated Session Manifest: {manifest_path}")
    except Exception as e:
        print(f"[!] Warning: Could not update manifest for step 10: {e}")

def aggregate_and_mix_bgm(chap_dir, chap_name, bgm_file="nhac-nen.mp3"):
    """Combined Step 09 and Step 10 execution."""
    full_parts = smart_aggregate_audio(chap_dir, chap_name)
    if not full_parts:
        return []
    return dynamic_bgm_mixer(chap_dir, chap_name, full_parts, bgm_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 09 & 10 Audio Aggregator and BGM Mixer")
    parser.add_argument("--chap_dir", type=str, required=True, help="Path to chapter directory")
    parser.add_argument("--chap_name", type=str, required=True, help="Chapter folder/slug name")
    parser.add_argument("--step", type=str, choices=["9", "10", "all"], default="9", help="Which step to run: 9, 10, or all")
    parser.add_argument("--bgm", type=str, default="nhac-nen.mp3", help="BGM file path")
    args = parser.parse_args()

    if args.step == "9":
        smart_aggregate_audio(args.chap_dir, args.chap_name)
    elif args.step == "10":
        dynamic_bgm_mixer(args.chap_dir, args.chap_name, bgm_file=args.bgm)
    else:
        aggregate_and_mix_bgm(args.chap_dir, args.chap_name, bgm_file=args.bgm)

