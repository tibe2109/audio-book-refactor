import os
import sys
import re
import json
import time
import html
import urllib.request
import urllib.parse
from html.parser import HTMLParser

# Import cookie getter
sys.path.insert(0, os.path.abspath('scratch'))
from test_coursera import get_coursera_cookies

class HTMLToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.href = None
        self.in_pre = False
        self.list_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            self.output.append(f"\n\n{'#' * level} ")
        elif tag == 'p':
            self.output.append("\n\n")
        elif tag == 'br':
            self.output.append("\n")
        elif tag in ['strong', 'b']:
            self.output.append("**")
        elif tag in ['em', 'i']:
            self.output.append("*")
        elif tag == 'code':
            if not self.in_pre:
                self.output.append("`")
        elif tag == 'pre':
            self.in_pre = True
            self.output.append("\n\n```\n")
        elif tag == 'a':
            self.href = attrs_dict.get('href', '')
            self.output.append("[")
        elif tag in ['ul', 'ol']:
            self.list_depth += 1
            self.output.append("\n")
        elif tag == 'li':
            self.output.append(f"\n{'  ' * (self.list_depth - 1)}- ")
        elif tag == 'blockquote':
            self.output.append("\n\n> ")
        elif tag == 'hr':
            self.output.append("\n\n---\n\n")

    def handle_endtag(self, tag):
        if tag in ['strong', 'b']:
            self.output.append("**")
        elif tag in ['em', 'i']:
            self.output.append("*")
        elif tag == 'code':
            if not self.in_pre:
                self.output.append("`")
        elif tag == 'pre':
            self.in_pre = False
            self.output.append("\n```\n\n")
        elif tag == 'a':
            if self.href:
                self.output.append(f"]({self.href})")
            else:
                self.output.append("]")
            self.href = None
        elif tag in ['ul', 'ol']:
            self.list_depth = max(0, self.list_depth - 1)
            self.output.append("\n")
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.output.append("\n\n")

    def handle_data(self, data):
        self.output.append(data)

    def get_markdown(self):
        text = ''.join(self.output)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

def html_to_markdown(raw_html):
    parser = HTMLToMarkdown()
    parser.feed(raw_html)
    return parser.get_markdown()

def clean_filename(name):
    # Replace invalid chars with -
    name = re.sub(r'[:/\\?*"<>|]', ' - ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'\s+-\s+-', ' -', name)
    return name

def fetch_url_with_retry(req, max_retries=5, delay=2):
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode('utf-8')
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                raise e

def main():
    dest_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Docs/Project Execution - Running the Project"
    os.makedirs(dest_dir, exist_ok=True)

    print("Step 1: Extracting Coursera cookies from Chrome...")
    cookies = get_coursera_cookies()
    cookie_str = '; '.join(f'{k}={v}' for k, v in cookies.items())
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Cookie': cookie_str,
        'x-csrf3-token': cookies.get('CSRF3-Token', ''),
        'x-coursera-application': 'ondemand',
        'x-requested-with': 'XMLHttpRequest'
    }

    course_slug = "project-execution-google"
    course_id = "ru_BPAp9EeuMRxJm6C8Z2w"

    print(f"\nStep 2: Fetching course syllabus & materials for '{course_slug}'...")
    url_mat = f"https://www.coursera.org/api/onDemandCourseMaterials.v2/?q=slug&slug={course_slug}&includes=modules,lessons,items&fields=moduleIds,onDemandCourseMaterialModules.v1(name,slug,description,lessonIds),onDemandCourseMaterialLessons.v1(name,slug,elementIds,itemIds),onDemandCourseMaterialItems.v2(name,slug,contentSummary,timeCommitment)"
    req_mat = urllib.request.Request(url_mat, headers=headers)
    mat_data = json.loads(fetch_url_with_retry(req_mat))

    modules_dict = {m['id']: m for m in mat_data.get('linked', {}).get('onDemandCourseMaterialModules.v1', [])}
    lessons_dict = {l['id']: l for l in mat_data.get('linked', {}).get('onDemandCourseMaterialLessons.v1', [])}
    items_dict = {it['id']: it for it in mat_data.get('linked', {}).get('onDemandCourseMaterialItems.v2', [])}

    root_module_ids = mat_data['elements'][0]['moduleIds']
    print(f"Loaded {len(root_module_ids)} modules.")

    course_manifest = {
        "course_title": "Project Execution: Running the Project",
        "course_slug": course_slug,
        "course_id": course_id,
        "source_url": "https://www.coursera.org/learn/project-execution-google/home/module/1",
        "modules": []
    }

    full_course_md_parts = [
        "# Project Execution: Running the Project\n\n"
        "> Google Project Management Certificate - Course 4\n"
        "> Source: https://www.coursera.org/learn/project-execution-google/home/module/1\n\n"
        "---\n"
    ]

    total_lectures_saved = 0
    total_supplements_saved = 0

    for m_idx, m_id in enumerate(root_module_ids):
        m = modules_dict.get(m_id, {})
        m_name = m.get('name', f'Module {m_idx+1}')
        clean_m_name = clean_filename(m_name)
        module_folder_name = f"{m_idx+1:02d} - {clean_m_name}"
        module_dir = os.path.join(dest_dir, module_folder_name)
        os.makedirs(module_dir, exist_ok=True)
        subtitles_dir = os.path.join(module_dir, "subtitles")
        os.makedirs(subtitles_dir, exist_ok=True)

        print(f"\n=======================================================")
        print(f"MODULE {m_idx+1}/{len(root_module_ids)}: {m_name}")
        print(f"Folder: {module_folder_name}")
        print(f"=======================================================")

        module_info = {
            "module_number": m_idx + 1,
            "module_id": m_id,
            "module_name": m_name,
            "folder_name": module_folder_name,
            "description": m.get('description', ''),
            "lessons": []
        }

        full_course_md_parts.append(f"\n# Module {m_idx+1}: {m_name}\n\n{m.get('description', '')}\n\n---\n")

        item_counter = 1

        for l_id in m.get('lessonIds', []):
            l = lessons_dict.get(l_id, {})
            l_name = l.get('name', 'Unknown Lesson')
            print(f"\n  [Lesson] {l_name}")

            lesson_info = {
                "lesson_id": l_id,
                "lesson_name": l_name,
                "items": []
            }

            full_course_md_parts.append(f"\n## Lesson: {l_name}\n")

            for it_id in l.get('itemIds', []):
                it = items_dict.get(it_id, {})
                it_name = it.get('name', 'Unknown Item')
                content_type = it.get('contentSummary', {}).get('typeName')
                clean_it_name = clean_filename(it_name)

                if content_type == 'lecture':
                    # VIDEO
                    txt_filename = f"{item_counter:02d} - {clean_it_name}.txt"
                    srt_filename = f"{item_counter:02d} - {clean_it_name}.srt"
                    txt_path = os.path.join(module_dir, txt_filename)
                    srt_path = os.path.join(subtitles_dir, srt_filename)

                    print(f"    [{item_counter:02d}] [VIDEO] {it_name} ...", end="", flush=True)

                    try:
                        # Fetch video data
                        vid_url = f"https://www.coursera.org/api/onDemandLectureVideos.v1/{course_id}~{it_id}?includes=video&fields=onDemandVideos.v1(subtitlesTxt,subtitles)"
                        req_vid = urllib.request.Request(vid_url, headers=headers)
                        vid_data = json.loads(fetch_url_with_retry(req_vid))
                        video_obj = vid_data.get('linked', {}).get('onDemandVideos.v1', [{}])[0]

                        # 1. Fetch transcript txt
                        txt_url = video_obj.get('subtitlesTxt', {}).get('en')
                        if txt_url:
                            if not txt_url.startswith('http'):
                                txt_url = f"https://www.coursera.org{txt_url}"
                            req_txt = urllib.request.Request(txt_url, headers=headers)
                            transcript_text = fetch_url_with_retry(req_txt)
                        else:
                            transcript_text = ""

                        # 2. Fetch srt
                        srt_url = video_obj.get('subtitles', {}).get('en')
                        if srt_url:
                            if not srt_url.startswith('http'):
                                srt_url = f"https://www.coursera.org{srt_url}"
                            req_srt = urllib.request.Request(srt_url, headers=headers)
                            srt_text = fetch_url_with_retry(req_srt)
                        else:
                            srt_text = ""

                        # Write txt file
                        with open(txt_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {it_name}\n\n")
                            f.write(transcript_text.strip() + "\n")

                        # Write srt file
                        if srt_text:
                            with open(srt_path, 'w', encoding='utf-8') as f:
                                f.write(srt_text.strip() + "\n")

                        word_count = len(transcript_text.split())
                        print(f" Saved ({word_count} words)")
                        total_lectures_saved += 1

                        lesson_info["items"].append({
                            "type": "lecture",
                            "order": item_counter,
                            "name": it_name,
                            "id": it_id,
                            "txt_file": f"{module_folder_name}/{txt_filename}",
                            "srt_file": f"{module_folder_name}/subtitles/{srt_filename}",
                            "word_count": word_count
                        })

                        full_course_md_parts.append(f"\n### {item_counter:02d}. [VIDEO] {it_name}\n\n{transcript_text.strip()}\n")

                    except Exception as e:
                        print(f" ERROR: {e}")

                    item_counter += 1
                    time.sleep(0.5)

                elif content_type == 'supplement':
                    # READING
                    md_filename = f"{item_counter:02d} - {clean_it_name}.md"
                    md_path = os.path.join(module_dir, md_filename)

                    print(f"    [{item_counter:02d}] [READING] {it_name} ...", end="", flush=True)

                    try:
                        supp_url = f"https://www.coursera.org/api/onDemandSupplements.v1/{course_id}~{it_id}?includes=asset&fields=openCourseAssets.v1(typeName),openCourseAssets.v1(definition)"
                        req_supp = urllib.request.Request(supp_url, headers=headers)
                        supp_data = json.loads(fetch_url_with_retry(req_supp))
                        assets = supp_data.get('linked', {}).get('openCourseAssets.v1', [])

                        raw_html = ""
                        if assets:
                            raw_html = assets[0].get('definition', {}).get('renderableHtmlWithMetadata', {}).get('renderableHtml', '')

                        md_content = html_to_markdown(raw_html)

                        with open(md_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {it_name}\n\n")
                            f.write(md_content + "\n")

                        word_count = len(md_content.split())
                        print(f" Saved ({word_count} words)")
                        total_supplements_saved += 1

                        lesson_info["items"].append({
                            "type": "supplement",
                            "order": item_counter,
                            "name": it_name,
                            "id": it_id,
                            "md_file": f"{module_folder_name}/{md_filename}",
                            "word_count": word_count
                        })

                        full_course_md_parts.append(f"\n### {item_counter:02d}. [READING] {it_name}\n\n{md_content}\n")

                    except Exception as e:
                        print(f" ERROR: {e}")

                    item_counter += 1
                    time.sleep(0.5)

            module_info["lessons"].append(lesson_info)

        course_manifest["modules"].append(module_info)

    # Save Full Combined Course Transcript Markdown
    full_course_md_path = os.path.join(dest_dir, "Full_Course_Transcript.md")
    with open(full_course_md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(full_course_md_parts) + "\n")
    print(f"\nSaved combined course markdown to: Full_Course_Transcript.md")

    # Save JSON Manifest
    json_path = os.path.join(dest_dir, "course_structure.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(course_manifest, f, ensure_ascii=False, indent=2)
    print(f"Saved course structure JSON to: course_structure.json")

    # Save README.md Table of Contents
    readme_path = os.path.join(dest_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# Project Execution: Running the Project\n\n")
        f.write("> **Khóa học**: Google Project Management Professional Certificate — Course 4\n")
        f.write("> **Nguồn**: [Coursera - Project Execution: Running the Project](https://www.coursera.org/learn/project-execution-google/home/module/1)\n")
        f.write(f"> **Tổng số bài**: {total_lectures_saved} Video Lectures (.txt, .srt) + {total_supplements_saved} Readings (.md)\n\n")
        f.write("## Danh mục các Module & Tài liệu\n\n")

        for m in course_manifest["modules"]:
            f.write(f"### Module {m['module_number']}: [{m['module_name']}]({urllib.parse.quote(m['folder_name'])})\n\n")
            if m['description']:
                f.write(f"> *{m['description']}*\n\n")
            f.write("| STT | Loại | Tên bài học | Số từ | Đường dẫn file |\n")
            f.write("| :---: | :---: | :--- | :---: | :--- |\n")
            for les in m["lessons"]:
                for it in les["items"]:
                    badge = "🎬 Video" if it["type"] == "lecture" else "📖 Reading"
                    file_link = it.get("txt_file") or it.get("md_file")
                    f.write(f"| {it['order']:02d} | {badge} | **{it['name']}** | {it['word_count']} từ | [`{os.path.basename(file_link)}`]({urllib.parse.quote(file_link)}) |\n")
            f.write("\n")

        f.write("## Tệp tổng hợp\n\n")
        f.write("- 📄 **Toàn bộ nội dung khóa học gộp**: [`Full_Course_Transcript.md`](Full_Course_Transcript.md)\n")
        f.write("- 📊 **Dữ liệu cấu trúc JSON**: [`course_structure.json`](course_structure.json)\n")

    print(f"Saved README.md table of contents to: README.md")

    print(f"\n=======================================================")
    print(f"DOWNLOAD SUMMARY:")
    print(f"  Total Video Lectures: {total_lectures_saved}/61")
    print(f"  Total Readings: {total_supplements_saved}/29")
    print(f"  Total Items Saved: {total_lectures_saved + total_supplements_saved}/90")
    print(f"=======================================================")

if __name__ == '__main__':
    main()
