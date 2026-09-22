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
course_id = "ru_BPAp9EeuMRxJm6C8Z2w"

# Get materials list to find sample lecture and sample supplement
url_mat = f"https://www.coursera.org/api/onDemandCourseMaterials.v2/?q=slug&slug={course_slug}&includes=items&fields=onDemandCourseMaterialItems.v2(name,slug,contentSummary)"
req = urllib.request.Request(url_mat, headers=headers)
with urllib.request.urlopen(req) as resp:
    mat_data = json.loads(resp.read().decode('utf-8'))

items = mat_data.get('linked', {}).get('onDemandCourseMaterialItems.v2', [])
sample_lecture = next((it for it in items if it.get('contentSummary', {}).get('typeName') == 'lecture'), None)
sample_supplement = next((it for it in items if it.get('contentSummary', {}).get('typeName') == 'supplement'), None)

print("Sample Lecture:", sample_lecture['name'], sample_lecture['id'])
print("Sample Supplement:", sample_supplement['name'], sample_supplement['id'])

# 1. Test Lecture APIs
lecture_id = sample_lecture['id']
for endpoint in [
    f"https://www.coursera.org/api/onDemandLectureVideos.v1/{lecture_id}?includes=subtitles,video",
    f"https://www.coursera.org/api/onDemandVideos.v1/{course_id}~{lecture_id}?includes=subtitles",
    f"https://www.coursera.org/api/onDemandVideoCopies.v1/{course_id}~{lecture_id}",
    f"https://www.coursera.org/api/openCourseItemPromptResponses.v1/{course_id}~{lecture_id}"
]:
    try:
        r = urllib.request.Request(endpoint, headers=headers)
        with urllib.request.urlopen(r) as res:
            d = json.loads(res.read().decode('utf-8'))
            print(f"[SUCCESS] Lecture endpoint: {endpoint}")
            print("  Top keys:", list(d.keys()))
            if 'elements' in d and d['elements']:
                print("  Element keys:", list(d['elements'][0].keys()))
            if 'linked' in d:
                print("  Linked keys:", list(d['linked'].keys()))
    except Exception as e:
        print(f"[FAIL] Lecture endpoint {endpoint}: {e}")

# 2. Test Supplement APIs
supp_id = sample_supplement['id']
for endpoint in [
    f"https://www.coursera.org/api/onDemandSupplements.v1/{course_id}~{supp_id}",
    f"https://www.coursera.org/api/onDemandSupplementMaterials.v1/{course_id}~{supp_id}",
    f"https://www.coursera.org/api/openCourseItemPromptResponses.v1/{course_id}~{supp_id}",
    f"https://www.coursera.org/api/onDemandCourseMaterialItems.v2/{course_id}~{supp_id}"
]:
    try:
        r = urllib.request.Request(endpoint, headers=headers)
        with urllib.request.urlopen(r) as res:
            d = json.loads(res.read().decode('utf-8'))
            print(f"[SUCCESS] Supplement endpoint: {endpoint}")
            print("  Top keys:", list(d.keys()))
            if 'elements' in d and d['elements']:
                print("  Element keys:", list(d['elements'][0].keys()))
                el = d['elements'][0]
                for k in ['content', 'body', 'text', 'html']:
                    if k in el:
                        print(f"  Found '{k}' in element! Len: {len(str(el[k]))}, preview: {str(el[k])[:150]}")
    except Exception as e:
        print(f"[FAIL] Supplement endpoint {endpoint}: {e}")
