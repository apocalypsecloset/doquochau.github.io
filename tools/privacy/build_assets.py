"""Build content-addressed consent assets and update HTML references."""
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def build():
    css = (ROOT / 'assets/css/privacy-consent.css').read_text(encoding='utf8')
    css_name = 'privacy-consent.' + hashlib.sha256(css.encode()).hexdigest()[:12] + '.css'
    (ROOT / 'assets/css' / css_name).write_text(css, encoding='utf8', newline='\n')
    js = (ROOT / 'assets/js/privacy-consent.js').read_text(encoding='utf8')
    js = js.replace('/assets/css/privacy-consent.css?v=20261116a', '/assets/css/' + css_name)
    assert '/assets/css/' + css_name in js
    js_name = 'privacy-consent.' + hashlib.sha256(js.encode()).hexdigest()[:12] + '.js'
    (ROOT / 'assets/js' / js_name).write_text(js, encoding='utf8', newline='\n')
    pattern = re.compile(r'(/assets/js/)privacy-consent(?:\.[a-f0-9]{12})?\.js(?:\?[^"\'<>\s]*)?')
    references = 0
    for page in ROOT.rglob('*.html'):
        original = page.read_bytes().decode('utf8')
        updated, count = pattern.subn(lambda m: m[1] + js_name, original)
        references += count
        if updated != original:
            page.write_bytes(updated.encode('utf8'))
    print(f'{references} HTML references; {css_name}; {js_name}')


if __name__ == '__main__':
    build()
