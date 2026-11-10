"""Render the actual README with GitHub's Markdown API; requires an authenticated gh CLI."""
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
request = json.dumps({'text': (ROOT / 'README.md').read_text(), 'mode': 'gfm', 'context': 'Mounesh-S/Mounesh-S'})
rendered = subprocess.run(['gh', 'api', 'markdown', '--input', '-'], input=request, text=True, capture_output=True, check=True).stdout
# The Markdown API omits heading IDs; GitHub's page adds these separately.
def heading(match):
    level, attributes, content = match.groups()
    label = html.unescape(re.sub('<[^>]*>', '', content)).lower()
    slug = re.sub(r'[^\w\- ]', '', label).replace(' ', '-')
    return f'<h{level}{attributes} id="{slug}">{content}</h{level}>'
rendered = re.sub(r'<h([1-6])([^>]*)>(.*?)</h\1>', heading, rendered)
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mounesh · The Emperor’s Log</title><link rel="stylesheet" href="assets/readme-preview.css">
<style>body{margin:0;background:#0d1117;color:#f0f6fc}.markdown-body{box-sizing:border-box;max-width:926px;margin:32px auto;padding:32px;border:1px solid #3d444d;border-radius:6px}.markdown-body img{height:auto}.markdown-body p a,.markdown-body li a{text-decoration:underline}.markdown-body a:focus-visible,.markdown-body summary:focus-visible{outline:2px solid #4493f8;outline-offset:4px}@media(prefers-color-scheme:light){body{background:#fff;color:#1f2328}.markdown-body{border-color:#d1d9e0}}@media(max-width:767px){.markdown-body{margin:0;padding:16px;border:0;border-radius:0}}</style></head><body><main class="markdown-body">'''+rendered+'''</main></body></html>'''
(ROOT / 'readme-preview.html').write_text(page)
print('Rendered the actual README with GitHub Markdown into readme-preview.html.')
