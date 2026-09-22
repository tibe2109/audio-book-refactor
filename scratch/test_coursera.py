import dbus
import hashlib
import sqlite3
import shutil
import tempfile
import os
import re
import json
import urllib.request
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def get_coursera_cookies():
    bus = dbus.SessionBus()
    service = bus.get_object('org.freedesktop.secrets', '/org/freedesktop/secrets')
    secrets_iface = dbus.Interface(service, 'org.freedesktop.Secret.Service')
    res, session_path = secrets_iface.OpenSession('plain', dbus.String('', variant_level=1))
    col = bus.get_object('org.freedesktop.secrets', '/org/freedesktop/secrets/collection/login')
    items = dbus.Interface(col, 'org.freedesktop.DBus.Properties').Get('org.freedesktop.Secret.Collection', 'Items')

    chrome_pw = None
    for item_path in items:
        item = bus.get_object('org.freedesktop.secrets', item_path)
        if dbus.Interface(item, 'org.freedesktop.DBus.Properties').Get('org.freedesktop.Secret.Item', 'Label') == 'Chrome Safe Storage':
            chrome_pw = bytes(dbus.Interface(item, 'org.freedesktop.Secret.Item').GetSecret(session_path)[2])
            break

    if not chrome_pw:
        raise RuntimeError("Could not retrieve Chrome Safe Storage secret from Keyring.")

    key = hashlib.pbkdf2_hmac('sha1', chrome_pw, b'saltysalt', 1, 16)

    def decrypt_val(enc_val):
        if not enc_val: return ''
        if enc_val[:3] == b'v10':
            c = Cipher(algorithms.AES(key), modes.CBC(b' ' * 16), backend=default_backend()).decryptor()
            dec = c.update(enc_val[3:]) + c.finalize()
            return dec[:-dec[-1]].decode('utf-8', errors='ignore')
        elif enc_val[:3] == b'v11':
            c = Cipher(algorithms.AES(key), modes.CBC(b' ' * 16), backend=default_backend()).decryptor()
            dec = c.update(enc_val[3:]) + c.finalize()
            return dec[32:-dec[-1]].decode('utf-8', errors='ignore')
        return enc_val.decode('utf-8', errors='ignore')

    p = os.path.expanduser('~/.config/google-chrome/Default/Cookies')
    cookies = {}
    with tempfile.NamedTemporaryFile() as tmp:
        shutil.copy2(p, tmp.name)
        conn = sqlite3.connect(tmp.name)
        cur = conn.cursor()
        cur.execute("SELECT name, value, encrypted_value FROM cookies WHERE host_key LIKE '%coursera%'")
        for name, val, enc_val in cur.fetchall():
            cookies[name] = val if val else decrypt_val(enc_val)
    return cookies

def main():
    cookies = get_coursera_cookies()
    print(f"Loaded {len(cookies)} coursera cookies.")
    print("Has CAUTH:", bool(cookies.get('CAUTH')), "len:", len(cookies.get('CAUTH', '')))
    print("Has CSRF3-Token:", bool(cookies.get('CSRF3-Token')))

    cookie_str = '; '.join(f'{k}={v}' for k, v in cookies.items())
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Cookie': cookie_str,
        'x-csrf3-token': cookies.get('CSRF3-Token', ''),
        'x-coursera-application': 'ondemand',
        'x-requested-with': 'XMLHttpRequest'
    }

    # Test 1: Get course info
    course_slug = "project-execution-google"
    url1 = f"https://www.coursera.org/api/onDemandCourses.v1?q=slug&slug={course_slug}"
    req1 = urllib.request.Request(url1, headers=headers)
    try:
        with urllib.request.urlopen(req1) as resp:
            data1 = json.loads(resp.read().decode('utf-8'))
            print("Course API Response:")
            print(json.dumps(data1, indent=2)[:500])
            course_id = data1['elements'][0]['id']
            print("Course ID:", course_id)
    except Exception as e:
        print("Error on onDemandCourses:", e)
        course_id = None

    # Test 2: Get course materials
    url2 = f"https://www.coursera.org/api/onDemandCourseMaterials.v2/?q=slug&slug={course_slug}&includes=modules,lessons,items&fields=moduleIds,onDemandCourseMaterialModules.v1(name,slug,description,lessonIds),onDemandCourseMaterialLessons.v1(name,slug,elementIds),onDemandCourseMaterialItems.v2(name,slug,contentSummary)"
    req2 = urllib.request.Request(url2, headers=headers)
    try:
        with urllib.request.urlopen(req2) as resp:
            data2 = json.loads(resp.read().decode('utf-8'))
            print("Course Materials API Response:")
            print("Elements count:", len(data2.get('elements', [])))
            print("Linked keys:", list(data2.get('linked', {}).keys()))
            modules = data2.get('linked', {}).get('onDemandCourseMaterialModules.v1', [])
            print(f"Total Modules: {len(modules)}")
            for m in modules:
                print(f"  Module: {m.get('name')} (id: {m.get('id')}, lessons: {len(m.get('lessonIds', []))})")
            lessons = data2.get('linked', {}).get('onDemandCourseMaterialLessons.v1', [])
            print(f"Total Lessons: {len(lessons)}")
            items = data2.get('linked', {}).get('onDemandCourseMaterialItems.v2', [])
            print(f"Total Items: {len(items)}")
            # Count item types
            types = {}
            for it in items:
                t = it.get('contentSummary', {}).get('typeName', 'unknown')
                types[t] = types.get(t, 0) + 1
            print("Item types breakdown:", types)
    except Exception as e:
        print("Error on onDemandCourseMaterials:", e)

if __name__ == '__main__':
    main()
