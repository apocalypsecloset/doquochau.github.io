"""Check current metadata and independently prove the restricted edit surface."""
import collections
import html
import json
from pathlib import Path
import re
import subprocess
import sys
from bs4 import BeautifulSoup
import search_metadata_release as RELEASE
import original_image_release as ORIGINAL_IMAGES

ROOT = Path(__file__).resolve().parents[1]
META = {'description', 'og:title', 'og:description', 'twitter:title', 'twitter:description'}
SUFFIX = re.compile(r'\s*[|—–-]\s*(?:AC|Apocalypse Closet)\s*$', re.I)
SCHEMA = re.compile(r'<script\b[^>]*type=[\x22\x27]application/ld\+json[\x22\x27][^>]*>(.*?)</script>', re.I | re.S)
TYPES = {'Article', 'BlogPosting', 'NewsArticle', 'WebPage', 'CollectionPage', 'AboutPage', 'ContactPage'}


def schema_view(obj, canonical):
    if isinstance(obj, list):
        return [schema_view(v, canonical) for v in obj]
    if not isinstance(obj, dict):
        return obj
    node = dict(obj)
    types = node.get('@type', [])
    types = [types] if isinstance(types, str) else types
    if set(types) & TYPES:
        keys = ['headline', 'description'] if set(types) & {'Article', 'BlogPosting', 'NewsArticle'} else ['name', 'description']
        for k in keys:
            node.pop(k, None)
    if 'BreadcrumbList' in types:
        node['itemListElement'] = [dict(v) for v in node.get('itemListElement', [])]
        for item in node['itemListElement']:
            target = item.get('item')
            target = target.get('@id', target.get('url')) if isinstance(target, dict) else target
            if target == canonical:
                item.pop('name', None)
    return {k: schema_view(v, canonical) for k, v in node.items()}


def protected_view(raw):
    head = raw
    soup = BeautifulSoup(head, 'html.parser')
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    canonical = canonical.get('href', '') if canonical else ''
    head = re.sub(r'(<title\b[^>]*>).*?(</title>)', r'\1REVIEWED TITLE\2', head, count=1, flags=re.I | re.S)
    def meta(m):
        n = BeautifulSoup(m.group(), 'html.parser').meta
        key = n.get('property', n.get('name', '')).lower()
        return '' if key in META else m.group()
    head = re.sub(r'<meta\b[^>]*>', meta, head, flags=re.I)
    def schema(m):
        opening = m.group()[:m.group().index('>')+1]
        value = schema_view(json.loads(m.group(1)), canonical)
        return opening + json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '</script>'
    return SCHEMA.sub(schema, head)


def main():
    errors = RELEASE.validate()
    def check(ok, msg):
        if not ok:
            errors.append(msg)
    manifest = RELEASE.release()
    plans = json.loads((ROOT / 'data/search-metadata-2026-11-18/proposals.json').read_text(encoding='utf8'))
    check(len(plans) == 174, 'Expected all 174 reviewed GSC pages')
    check(dict(collections.Counter(p['language'] for p in plans)) == {'VN': 140, 'EN': 34}, 'Expected VN/EN coverage')
    check(len({p['path'] for p in plans}) == 174, 'Duplicate proposal path')
    check(len({p['title_after'].casefold() for p in plans}) == 174, 'Duplicate proposed title')
    check(len({p['description_after'].casefold() for p in plans}) == 174, 'Duplicate proposed description')
    selected = {p['path']: p for p in plans}
    changed_html = 0
    for path, row in manifest['files'].items():
        if not path.endswith('.html'):
            continue
        raw = (ROOT / path).read_text(encoding='utf8')
        old = RELEASE.predecessor(path, raw)
        changed_html += 1
        check(protected_view(old) == protected_view(ORIGINAL_IMAGES.predecessor(path, raw)), path + ': unrelated head/schema/canonical/links/images changed')
        soup = BeautifulSoup(raw, 'html.parser')
        title = soup.title.get_text()
        desc = soup.find('meta', attrs={'name': 'description'})
        description = desc.get('content', '') if desc else ''
        check(title == row['fields']['title']['new'], path + ': wrong title')
        if path in selected:
            plan = selected[path]
            check(description == plan['description_after'], path + ': wrong description')
            check(80 <= len(description) <= 200, path + ': description length outside reviewed range')
            check(not re.search(r'[\u200b-\u200f\ufeff]', title + description), path + ': invisible text')
            for key, value in [('description', description), ('og:title', title), ('twitter:title', title), ('og:description', description), ('twitter:description', description)]:
                nodes = [n for n in soup.find_all('meta') if n.get('property', n.get('name', '')).lower() == key]
                check(len(nodes) == 1 and nodes[0].get('content') == value, path + ': missing/duplicate/out-of-sync ' + key)
        else:
            check(title == SUFFIX.sub('', row['fields']['title']['old']), path + ': suffix-only title unexpectedly rewritten')
            before = BeautifulSoup(old, 'html.parser').find('meta', attrs={'name': 'description'})
            check(description == (before.get('content', '') if before else ''), path + ': unselected description rewritten')
        for script in soup.select('script[type="application/ld+json"]'):
            obj = json.loads(script.get_text())
            def walk(node):
                if isinstance(node, dict):
                    types = node.get('@type', [])
                    types = [types] if isinstance(types, str) else types
                    if set(types) & TYPES:
                        field = 'headline' if set(types) & {'Article', 'BlogPosting', 'NewsArticle'} else 'name'
                        check(node.get(field) == title, path + ': schema title mismatch')
                        if path in selected:
                            check(node.get('description') == description, path + ': schema description mismatch')
                    for value in node.values(): walk(value)
                elif isinstance(node, list):
                    for value in node: walk(value)
            walk(obj)
    paths = subprocess.check_output(['git', 'ls-files', '*.html'], cwd=ROOT, text=True).splitlines()
    suffixes = []
    for path in paths:
        soup = BeautifulSoup((ROOT / path).read_text(encoding='utf8'), 'html.parser')
        if path == 'index.html':
            check(soup.title.get_text().endswith(' | Apocalypse Closet'), 'Root homepage lost brand')
            continue
        if soup.title and SUFFIX.search(soup.title.get_text()):
            suffixes.append(path)
        for n in soup.find_all('meta'):
            if n.get('property', n.get('name', '')).lower() in {'og:title', 'twitter:title'}:
                check(not SUFFIX.search(n.get('content', '')), path + ': social title still has suffix')
    check(not suffixes, 'Brand suffix remains on child pages: ' + ', '.join(suffixes))
    # Verify that the historical adapter rejects unreviewed changes rather than
    # accepting arbitrary metadata/body edits under a path-only allowlist.
    sample = plans[0]['path']
    raw = (ROOT / sample).read_text(encoding='utf8')
    try:
        RELEASE.predecessor(sample, raw + '\n<!-- unreviewed edit -->')
        check(False, 'Historical adapter accepted unknown successor bytes')
    except ValueError:
        pass
    check(protected_view(raw) != protected_view(raw.replace('</body>', '<p>Unreviewed</p></body>', 1)), 'Body preservation check failed to detect mutation')
    print(json.dumps({'reviewed_gsc_pages': len(plans), 'changed_html': changed_html,
        'language_counts': dict(collections.Counter(p['language'] for p in plans)),
        'remaining_child_title_suffixes': len(suffixes), 'body_and_non_metadata_preservation': not errors,
        'errors': errors}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
