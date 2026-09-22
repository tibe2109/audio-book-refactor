import urllib.request
import json
import html
import re
from html.parser import HTMLParser
import sys
import os
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
        # Clean up excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

def html_to_markdown(raw_html):
    parser = HTMLToMarkdown()
    parser.feed(raw_html)
    return parser.get_markdown()

# Test with CUMrZ
cookies = get_coursera_cookies()
cookie_str = '; '.join(f'{k}={v}' for k, v in cookies.items())
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Cookie': cookie_str,
    'x-csrf3-token': cookies.get('CSRF3-Token', ''),
    'x-coursera-application': 'ondemand',
    'x-requested-with': 'XMLHttpRequest'
}

course_id = 'ru_BPAp9EeuMRxJm6C8Z2w'
supp_id = 'CUMrZ'

url = f'https://www.coursera.org/api/onDemandSupplements.v1/{course_id}~{supp_id}?includes=asset&fields=openCourseAssets.v1(typeName),openCourseAssets.v1(definition)'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    assets = data.get('linked', {}).get('openCourseAssets.v1', [])
    if assets:
        raw_html = assets[0].get('definition', {}).get('renderableHtmlWithMetadata', {}).get('renderableHtml', '')
        md = html_to_markdown(raw_html)
        print("Converted Markdown preview (first 400 chars):")
        print(md[:400])
        print("\nLength of markdown:", len(md))
