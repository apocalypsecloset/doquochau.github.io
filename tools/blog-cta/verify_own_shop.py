"""Verify the own-shop migration against the current Git HEAD."""
import io
import json
import re
import subprocess
import tarfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors = []
stats = Counter()
data_files = [ROOT / 'outfits.js', *sorted((ROOT / 'assets/js').glob('style-outfits-*.js'))]
archive = subprocess.check_output(['git', '-C', str(ROOT), 'archive', 'HEAD', 'blog', 'en/blog', 'outfits',
                                   *[p.relative_to(ROOT).as_posix() for p in data_files]])
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    before = {m.name: tar.extractfile(m).read().decode('utf8') for m in tar if m.isfile()}
products = json.loads((ROOT / 'tools/blog-cta/config.json').read_text(encoding='utf8'))['products']
product_urls = {p['fourthwall'] for p in products.values()}


class Check(HTMLParser):
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a':
            href = a.get('href', '')
            if 'sponsored' in a.get('rel', '') or re.search(r's\.shopee\.vn|shope\.ee|isclix|accesstrade', href):
                errors.append(f'{name}: affiliate anchor')
        if tag == 'script' and a.get('src', '').startswith('/'):
            if not (ROOT / a['src'].split('?')[0].lstrip('/')).exists():
                errors.append(f'{name}: missing script {a["src"]}')


for name in subprocess.check_output(['git', '-C', str(ROOT), 'ls-files'], text=True).splitlines():
    p = ROOT / name
    if p.suffix not in ('.html', '.js', '.json') or name.startswith(('docs/', 'data/', 'tools/', 'cloudflare/')):
        continue
    h = p.read_text(encoding='utf8')
    stats['files_scanned'] += 1
    if re.search(r'affiliate|tiếp thị liên kết|s\.shopee\.vn|shope\.ee|\bsponsored\b', h, re.I):
        errors.append(f'{name}: affiliate residue')
    if p.suffix == '.json':
        json.loads(h)
    if p.suffix != '.html':
        continue
    Check().feed(h)
    for body in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        json.loads(body)
    old = before.get(name)
    if not old:
        continue
    if '<article' in h and p.parent in (ROOT / 'blog', ROOT / 'en/blog'):
        lang = 'en' if name.startswith('en/') else 'vi'
        stats[f'{lang}_articles'] += 1
        for marker in ('top', 'end'):
            if h.count(f'<!-- ac-cta:{marker} -->') != 1:
                errors.append(f'{name}: invalid {marker} CTA count')
        if h.count('blog-shop-cta.css') != 1:
            errors.append(f'{name}: CTA CSS count')
        if '<!-- ac-cta:mid -->' not in h:
            stats['short_articles_without_mid'] += 1
        for tag in ('h1', 'h2', 'h3', 'table', 'details'):
            if len(re.findall(fr'<{tag}\b', old)) != len(re.findall(fr'<{tag}\b', h)):
                errors.append(f'{name}: changed {tag} count')
        # Titles and canonical/language relationships must survive the migration.
        for pattern in (r'<title>.*?</title>', r'<link\b[^>]*\brel="(?:canonical|alternate)"[^>]*>', r'<link\b[^>]*\bhreflang="[^"]+"[^>]*>'):
            if re.findall(pattern, old, re.S) != re.findall(pattern, h, re.S):
                errors.append(f'{name}: changed metadata')
        for block in re.findall(r'<!-- ac-cta:(?:mid|end) -->.*?<!-- /ac-cta:(?:mid|end) -->', h, re.S):
            for u in re.findall(r'href="([^"]+)"', block):
                if not (u.startswith('/?utm_source=blog') or u.split('?')[0] in product_urls):
                    errors.append(f'{name}: unexpected shop target {u}')
        stats['direct_product_links'] += h.count('href="https://shop.apocalypsecloset.com/products/')
    if name.startswith('outfits/'):
        stats['outfit_pages'] += 1
        if h.count('class="item-link"') != old.count('class="item-link"'):
            errors.append(f'{name}: lost styling references')
        if re.search(r'<a\b[^>]*class="item-link"', h):
            errors.append(f'{name}: garment still presented as a purchase link')
        if 'Xem áo thiết kế của Apocalypse Closet' not in h:
            errors.append(f'{name}: missing own-shop route')

for p in data_files:
    h = p.read_text(encoding='utf8')
    start = re.search(r'(?:const\s+outfits\s*=|window\.outfits\s*=)\s*', h).end()
    # These JavaScript data literals allow trailing commas, unlike JSON.
    data, _ = json.JSONDecoder().raw_decode(re.sub(r',(\s*[}\]])', r'\1', h[start:]))
    old_h = before[p.relative_to(ROOT).as_posix()]
    old_start = re.search(r'(?:const\s+outfits\s*=|window\.outfits\s*=)\s*', old_h).end()
    old_data, _ = json.JSONDecoder().raw_decode(re.sub(r',(\s*[}\]])', r'\1', old_h[old_start:]))
    if len(data) != len(old_data):
        errors.append(f'{p.name}: changed outfit count')
    stats['data_outfits_checked'] += len(data)
    for outfit, old_outfit in zip(data, old_data):
        if len(outfit['detail']['items']) != len(old_outfit['detail']['items']) or any('link' in item for item in outfit['detail']['items']):
            errors.append(f'{p.name}: changed garment count or remaining sales URL')

report = {'stats': dict(stats), 'errors': errors}
(ROOT / 'tools/blog-cta/own-shop-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
