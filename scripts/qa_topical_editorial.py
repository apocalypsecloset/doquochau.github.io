"""Check actual current pages, exact bilingual patches and explicit topology."""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
import internal_link_audit as VI
import internal_link_audit_en as EN
import blog_image_release as IMAGE_RELEASE
import search_metadata_release as SEARCH_METADATA
import original_image_release as ORIGINAL_IMAGES

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/topical-editorial-2026-11-17'
BASE = '97ba710f3e23cde22c9dc72b87052b507049ddaa'
errors = []

def check(ok, message):
    if not ok:
        errors.append(message)

def digest(raw):
    return hashlib.sha256(raw.encode('utf8')).hexdigest()

def baseline(paths):
    refs = [BASE + ':' + p for p in paths]
    raw = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=ROOT, input=('\n'.join(refs) + '\n').encode())
    result = {}; offset = 0
    for path in paths:
        end = raw.index(b'\n', offset); header = raw[offset:end].split()
        assert len(header) == 3 and header[1] == b'blob', (path, header)
        size = int(header[2]); offset = end + 1
        result[path] = raw[offset:offset+size].decode('utf8').replace('\r\n', '\n'); offset += size + 1
    return result

def resolve(href, page):
    u = urlsplit(urljoin('https://apocalypsecloset.com/' + page, href))
    if u.scheme not in ('http', 'https') or u.hostname not in ('apocalypsecloset.com', 'www.apocalypsecloset.com'):
        return None
    target = unquote(u.path).lstrip('/')
    if not target or target.endswith('/'):
        target += 'index.html'
    return target, unquote(u.fragment)

names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT, text=True).splitlines()
html_names = [p for p in names if p.endswith('.html')]
old = baseline(html_names)
actual_current = {p.relative_to(ROOT).as_posix(): p.read_text(encoding='utf8') for p in ROOT.rglob('*.html') if not {'.git', 'node_modules'} & set(p.parts)}
image_release_errors = IMAGE_RELEASE.validate()
check(not image_release_errors, 'Exact image release successors: ' + '; '.join(image_release_errors))
metadata_release_errors = SEARCH_METADATA.validate()
check(not metadata_release_errors, 'Exact search metadata successors: ' + '; '.join(metadata_release_errors))
# Image QA checks real current markup and preservation independently. The earlier
# exact editorial replay retains its original image/head/script predecessor.
current = {p: IMAGE_RELEASE.predecessor(p, raw) for p, raw in actual_current.items()}
check(set(old) == set(current), 'HTML inventory changed without publication review')
patches = json.loads((DATA / 'patches.json').read_text(encoding='utf8'))
expected = dict(old)
for i, patch in enumerate(patches):
    p = patch['source']; a = patch['before']; b = patch['after']
    check(p in expected and a != b and expected[p].count(a) == 1, f'Patch {i}: unique exact predecessor')
    if p in expected and expected[p].count(a) == 1:
        expected[p] = expected[p].replace(a, b, 1)
check(expected == current, 'Current HTML must exactly replay all reviewed changes, including unchanged pages')
changed = {p for p in current if current[p] != old.get(p)}
changed_paths = subprocess.check_output(['git', 'diff', '--name-only', BASE], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).splitlines()
new_code = {'scripts/qa_topical_editorial.py', 'scripts/qa_editorial_history.py', 'data/topical-map.json', 'docs/topical-editorial-2026-11-17.md'}
cleanup_paths = set()
if (ROOT/'data/repository-cleanup-2026-11-18.json').is_file():
    from repository_cleanup_release import validate as validate_cleanup
    cleanup_report, cleanup_paths = validate_cleanup()
    check(not cleanup_report['errors'], 'Exact repository cleanup: ' + '; '.join(cleanup_report['errors']))
for path in changed_paths:
    check(path in changed or path in new_code or path in cleanup_paths or path in IMAGE_RELEASE.additions() or path in IMAGE_RELEASE.release()['files'] or path in SEARCH_METADATA.additions() or path in SEARCH_METADATA.release()['files'] or path in ORIGINAL_IMAGES.additions() or path in ORIGINAL_IMAGES.release()['files'] or path == '.github/workflows/site-quality.yml' or path.startswith('data/topical-editorial-2026-11-17/'), path + ': historical evidence, scripts and unrelated assets must remain unchanged')
soups = {p: BeautifulSoup(raw, 'lxml') for p, raw in actual_current.items()}
protected = ['title', 'meta', 'link', 'h1', 'h2', 'h3', 'h4', 'img', 'script', '.article-toc', '.ac-reading-path', '.seo-faq', '.ac-sources']
for p in changed:
    before = BeautifulSoup(old[p], 'lxml')
    reviewed_editorial = BeautifulSoup(current[p], 'lxml')
    for selector in protected:
        check([str(n) for n in before.select(selector)] == [str(n) for n in reviewed_editorial.select(selector)], p + ': preserved ' + selector)
    for n in soups[p].select('script[type="application/ld+json"]'):
        try: json.loads(n.get_text())
        except ValueError: check(False, p + ': invalid JSON-LD')

vi = {p:s for p,s in soups.items() if p.startswith('blog/') and not s.select_one('meta[http-equiv="refresh" i]')}
en = {p:s for p,s in soups.items() if p.startswith('en/blog/') and not s.select_one('meta[http-equiv="refresh" i]')}
vp, _ = EN.extract(vi, ['article.article-content'])
ep, _ = EN.extract(en, ['article.editorial', 'main.en-hub', 'article'])
mapping = {EN.hreflang(s, 'vi'):p for p,s in en.items() if EN.hreflang(s, 'vi')}
check(set(mapping) == set(vi) and len(mapping) == 440, 'Every VI page has its actual EN counterpart')
prose = {**vp, **ep}; incoming = collections.defaultdict(set)
for p, rows in prose.items():
    for t, *_ in rows:
        if t in prose: incoming[t].add(p)
for p in prose:
    check(len(incoming[p]) >= 2, p + ': fewer than two independent contextual referrers')
reviewed_dense = {(r['source'], r['context']): r for r in json.loads((DATA/'dense-reviewed-exceptions.json').read_text(encoding='utf8'))}
for p, links in prose.items():
    grouped = collections.Counter(context for target, anchor, context, *_ in links if target in prose)
    for context, count in grouped.items():
        check(count <= 3 or (p, context) in reviewed_dense, p + ': unreviewed paragraph with more than three blog links')
        if p.startswith('blog/'):
            check(not re.search(r'\bpillar\b|xem chọn\b|dùng tra\b', context, re.I), p + ': awkward or implementation-facing link wording')
for p, rows in vp.items():
    want = {mapping[t] for t, *_ in rows if t in mapping and t != p}
    have = {t for t, *_ in ep[mapping[p]]}
    check(want <= have, p + ': actual contextual relationships missing from EN')
all_hubs = {'blog/' + x + '.html' for x in list(VI.HUBS.values()) + VI.STYLE_SUBHUBS}
for p in vi:
    if p in all_hubs: continue
    peers = {t for t, *_ in vp[p] if t in vi and t not in all_hubs and VI.cluster(Path(t).stem) == VI.cluster(Path(p).stem)}
    check(bool(peers), p + ': no actual leaf-to-leaf link in its reviewed group')

edges = collections.defaultdict(set)
ids = {p:{n['id'] for n in s.select('[id]')} for p,s in soups.items()}
stubs = {p for p,s in soups.items() if s.select_one('meta[http-equiv="refresh" i]')}
anchors = 0
for p,s in soups.items():
    for a in s.select('a[href]'):
        dest = resolve(a['href'], p)
        if dest is None: continue
        anchors += 1; t, fragment = dest
        check((ROOT/t).is_file(), p + ': missing internal target ' + a['href'])
        if t in soups:
            edges[p].add(t)
            check(not fragment or fragment in ids[t], p + ': missing fragment ' + a['href'])
        check(t not in stubs or t == p, p + ': link to redirect stub ' + t)
registry = json.loads((ROOT/'data/topical-map.json').read_text(encoding='utf8'))
rows = registry['pages']; records = {r['url'].lstrip('/'):r for r in rows}
check(len(records) == len(rows) and set(records) == set(prose), 'Explicit map covers each actual blog URL exactly once; unknown URLs cannot default to Aesthetic')
for p,row in records.items():
    check(row['primary_topic'] and row['intent'] and row['classification_basis'], p + ': explicit classification')
    parent = row['parent'].lstrip('/')
    check(parent in soups and parent != p, p + ': valid distinct parent')
    check(p in edges[parent] and parent in edges[p], p + ': reciprocal actual parent navigation')
    if row['locale'] == 'vi':
        twin = records[mapping[p]]
        check(row['primary_topic'] == twin['primary_topic'] and row['intent'] == twin['intent'], p + ': bilingual map intent agreement')
check(records['blog/the-art-of-burning-out.html']['primary_topic'] == 'lifestyle-and-wardrobe-decisions', 'Burnout must not default to an aesthetic')
for slug in ['auth-la-gi', 'like-auth-la-gi', 'local-brand-la-gi', 'boutique-la-gi', 'sold-out-la-gi']:
    check(records['blog/'+slug+'.html']['primary_topic'] == 'shopping-and-terminology', slug + ': purchase terminology is not an item shape')

dist = {'index.html':0}; queue = collections.deque(['index.html'])
while queue:
    p = queue.popleft()
    for t in edges[p]:
        if t not in dist: dist[t] = dist[p] + 1; queue.append(t)
sitemap = {resolve(n.text, 'index.html')[0] for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')}
check(sitemap <= set(dist), 'Every sitemap URL is reachable through actual HTML anchors')

# Run unmodified link gates against real current files, never a predecessor view.
gates = {}
for script, expected_passes in [('internal_link_audit.py', 11), ('internal_link_audit_en.py', 15)]:
    r = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT/'scripts'/script), '--root', str(ROOT)], capture_output=True, encoding='utf8')
    count = len(re.findall(r'^\[PASS\]', r.stdout, re.M))
    check(r.returncode == 0 and count == expected_passes, script + ': all current gates pass unchanged\n' + r.stdout if r.returncode else script + ': gate count')
    gates[script] = {'exit':r.returncode, 'passed':count}
previous_soups = {p:BeautifulSoup(old[p], 'lxml') if p in changed else s for p,s in {**vi,**en}.items()}
oldvp, _ = EN.extract({p:s for p,s in previous_soups.items() if p in vi}, ['article.article-content'])
oldep, _ = EN.extract({p:s for p,s in previous_soups.items() if p in en}, ['article.editorial', 'main.en-hub', 'article'])
pair_counts = {}
for locale, before_links, after_links in [('vi', oldvp, vp), ('en', oldep, ep)]:
    before_pairs = {(p,t) for p,ls in before_links.items() for t,*_ in ls if t in prose}
    after_pairs = {(p,t) for p,ls in after_links.items() for t,*_ in ls if t in prose}
    pair_counts[locale] = {'before':len(before_pairs), 'after':len(after_pairs), 'new':len(after_pairs-before_pairs), 'removed':len(before_pairs-after_pairs)}
report = {'baseline':BASE, 'actual_html_pages':len(current), 'changed_html_pages':len(changed), 'exact_patch_steps':len(patches), 'explicit_map_urls':len(records), 'internal_anchor_occurrences':anchors, 'minimum_contextual_referrers':min(len(incoming[p]) for p in prose), 'contextual_blog_relationships':pair_counts, 'VI_to_EN_contextual_parity':'100%' if not any('missing from EN' in e for e in errors) else 'FAIL', 'sitemap_urls':len(sitemap), 'maximum_sitemap_depth':max(dist.get(p,-1) for p in sitemap), 'protected_fields':'all unchanged' if not any(': preserved ' in e for e in errors) else 'FAIL', 'current_link_gates':gates, 'errors':errors}
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
