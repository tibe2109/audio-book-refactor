import urllib.request
import json
import sys
import os
sys.path.insert(0, os.path.abspath('scratch'))
from test_coursera import get_coursera_cookies

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
url = f"https://www.coursera.org/api/onDemandCourseMaterials.v2/?q=slug&slug={course_slug}&includes=modules,lessons,items&fields=moduleIds,onDemandCourseMaterialModules.v1(name,slug,description,lessonIds),onDemandCourseMaterialLessons.v1(name,slug,elementIds),onDemandCourseMaterialItems.v2(name,slug,contentSummary)"

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

modules = {m['id']: m for m in data.get('linked', {}).get('onDemandCourseMaterialModules.v1', [])}
lessons = {l['id']: l for l in data.get('linked', {}).get('onDemandCourseMaterialLessons.v1', [])}
items = {it['id']: it for it in data.get('linked', {}).get('onDemandCourseMaterialItems.v2', [])}

root_module_ids = data['elements'][0]['moduleIds']
print(f"Total Modules: {len(root_module_ids)}")

all_lectures = []
all_supplements = []

for m_idx, m_id in enumerate(root_module_ids):
    m = modules.get(m_id, {})
    m_name = m.get('name', 'Unknown Module')
    print(f"\n--- Module {m_idx+1}: {m_name} ---")
    for l_id in m.get('lessonIds', []):
        l = lessons.get(l_id, {})
        l_name = l.get('name', 'Unknown Lesson')
        print(f"  Lesson: {l_name}")
        for it_id in l.get('itemIds', []):
            it = items.get(it_id, {})
            t = it.get('contentSummary', {}).get('typeName')
            it_name = it.get('name', 'Unknown Item')
            if t == 'lecture':
                all_lectures.append((m_idx+1, m_name, l_name, it_name, it_id, it.get('slug')))
                print(f"    [VIDEO] {it_name} (id: {it_id})")
            elif t == 'supplement':
                all_supplements.append((m_idx+1, m_name, l_name, it_name, it_id, it.get('slug')))
                print(f"    [READING] {it_name} (id: {it_id})")

print(f"\nSummary:")
print(f"Total Lectures: {len(all_lectures)}")
print(f"Total Supplements: {len(all_supplements)}")

# Check duplicate names
lecture_names = [x[3] for x in all_lectures]
supp_names = [x[3] for x in all_supplements]
import collections
dup_lectures = [item for item, count in collections.Counter(lecture_names).items() if count > 1]
dup_supps = [item for item, count in collections.Counter(supp_names).items() if count > 1]
print("Duplicate Lecture names:", dup_lectures)
print("Duplicate Supplement names:", dup_supps)
