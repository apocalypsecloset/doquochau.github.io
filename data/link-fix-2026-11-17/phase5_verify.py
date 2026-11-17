"""Final preservation, metadata uniqueness, scope, and five core-link checks."""
import collections
import csv
import json
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = '9e16c20'
NEW = ['phoi-mau-quan-ao-nu', 'chon-trang-phuc-nu-theo-dia-diem-va-dip',
       'cach-cham-soc-do-nu', 'chon-toc-va-makeup-theo-trang-phuc']
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)
def protected(raw):
    s = BeautifulSoup(raw, 'html.parser')
    selectors = ['title', 'h1', 'meta', 'link[rel=canonical]', 'script[type="application/ld+json"]',
                 'img', 'h2', 'h3', 'h4', '.toc', '#toc', '.ac-reading-path', '.seo-faq', '.ac-sources']
    return {sel: [str(n) for n in s.select(sel)] for sel in selectors}

names = git('ls-tree', '-r', '--name-only', BASE, 'blog').decode().splitlines()
names = [p for p in names if p.endswith('.html')]
refs = [BASE + ':' + p for p in names] + ['985f5e3:blog/' + p + '.html' for p in NEW]
paths = names + ['blog/' + p + '.html' for p in NEW]
data = subprocess.run(['git', 'cat-file', '--batch'], input=('\n'.join(refs)+'\n').encode(),
                      capture_output=True, check=True, cwd=ROOT).stdout
pos = 0
for path in paths:
    end = data.index(b'\n', pos)
    size = int(data[pos:end].split()[-1])
    old = data[end+1:end+1+size].decode('utf-8')
    pos = end + size + 2
    before = protected(old)
    after = protected((ROOT/path).read_text(encoding='utf-8'))
    for sel in before:
        # Phase 3 adds child cards with their own images/headings. Original nodes remain intact.
        if sel in ['img', 'h2', 'h3', 'h4']:
            assert not (collections.Counter(before[sel]) - collections.Counter(after[sel])), (path,sel)
        else:
            assert before[sel] == after[sel], (path,sel)

unique = collections.defaultdict(lambda: collections.defaultdict(list))
real = []
for p in (ROOT/'blog').glob('*.html'):
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    if s.select_one('meta[http-equiv="refresh" i]'): continue
    real.append(p)
    for field, value in [('title', s.title.get_text(strip=True)), ('h1', s.h1.get_text(' ',strip=True)),
                         ('description', s.select_one('meta[name=description]')['content']),
                         ('canonical', s.select_one('link[rel=canonical]')['href'])]:
        unique[field][value].append(p.name)
duplicates = {field: {v: ps for v, ps in values.items() if len(ps)>1} for field,values in unique.items()}
assert not any(duplicates.values()), duplicates
core = {}
for slug, dest in [('goth','goth'),('egirl','egirl'),('baddie-streetwear','baddie-streetwear'),
                   ('dark-feminine','dark-feminine'),('punk-grunge','punk')]:
    s = BeautifulSoup((ROOT/'blog'/f'{slug}.html').read_text(encoding='utf-8'),'html.parser')
    links = [a for p in s.select('main p') for a in p.select('a[href]')
             if a['href'].startswith('/style/') or a['href'].split('#')[0]=='/phoi-do-nu-ca-tinh.html']
    assert len(links)==1 and links[0]['href']==f'/style/{dest}.html', (slug,links)
    assert 2<=len(links[0].get_text(' ',strip=True).split())<=6
    core[slug] = links[0]['href']
patches = json.loads((ROOT/'tools/phase5_patches.json').read_text(encoding='utf-8'))
for p in patches:
    old = git('show','b4f5a52:'+p['file']).decode('utf-8')
    now = (ROOT/p['file']).read_text(encoding='utf-8')
    assert old.count(p['old'])==1 and now==old.replace(p['old'],p['new'],1)
changed = git('diff','--name-only',BASE).decode().splitlines()
assert all(p.startswith('tools/') or (p.startswith('blog/') and p.endswith('.html')) or
           p in ['sitemap.xml','blog.html','search-index.js','CODEX_TASK.md'] for p in changed), changed
log = (ROOT/'tools/link_changes.csv').read_bytes()
prior = git('show','b4f5a52:tools/link_changes.csv')
assert log.replace(b'\r\n', b'\n').startswith(prior.replace(b'\r\n', b'\n'))
rows = list(csv.DictReader(log.decode('utf-8-sig').splitlines()))
assert len(rows)==1328
report = dict(original_blog_files_protected=len(names), new_guides_protected=len(NEW),
              real_vi_articles=len(real), duplicate_metadata=duplicates, core_contextual_links=core,
              exact_phase5_replacements=2, new_phase5_links=2, change_log_rows=len(rows), scope_pass=True)
(ROOT/'tools/phase5_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
