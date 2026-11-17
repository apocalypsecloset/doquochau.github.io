"""Prepare additive VI successor evidence and the approved image-sitemap repair."""
import collections
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / 'docs/link-fix-2026-11-17'
D.mkdir(exist_ok=True)
BASE = '9e16c2012f417cf5e4634b1c771a2c5d773e1ee8'
FIX = '6d8a9c4f13b59bc12e0db087a2779fbcfa2480db'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
def text(s):return BeautifulSoup(s,'lxml').get_text(' ',strip=True)
def canon(b):return b.decode('utf-8').replace('\r\n','\n')

# Add only the twelve full navigation spans missing from the old per-link log.
logpath = ROOT/'tools/link_changes.csv'
log = logpath.read_bytes()
rows = list(csv.DictReader(io.StringIO(log.decode('utf-8-sig'))))
pairs = collections.defaultdict(set)
for row in rows:pairs[row['file']].add((text(row['câu_trước']),text(row['câu_sau'])))
out = io.StringIO(newline='');writer = csv.writer(out);extra = []
patches = json.loads(git('show',FIX+':tools/phase3_patches.json'))
for p in patches:
    if (text(p['old']),text(p['new'])) in pairs[p['file']]:continue
    assert p['kind']=='down',p['file']
    writer.writerow([p['file'],' | '.join(l['target'] for l in p['links']),
                     ' | '.join(l['anchor'] for l in p['links']),p['old'],p['new']])
    extra.append(p['file'])
if extra:
    assert len(extra)==12,len(extra)
    logpath.write_bytes(log+out.getvalue().encode('utf-8'))

# Keep source formatting and existing sitemap bytes; only replace these image lists.
assets = {r['url']:r for r in json.loads((ROOT/'docs/image-seo-2026-11-15/assets-qa.json').read_text(encoding='utf-8'))}
sitemap = (ROOT/'sitemap.xml').read_bytes().decode('utf-8')
repairs = []
for path in ['blog/cac-loai-vai.html','blog/cach-chon-kinh-phu-hop-voi-khuon-mat-nu.html']:
    raw = (ROOT/path).read_bytes().decode('utf-8')
    main = BeautifulSoup(raw,'lxml').main
    images = list(dict.fromkeys(urljoin('https://apocalypsecloset.com/',n['src']) for n in main.select('img')
                                if '/images/' in n['src'] or '/assets/editorial/' in n['src']))
    assert all(u in assets and assets[u]['status']==200 and len(assets[u]['sha256'])==64 for u in images),path
    url = 'https://apocalypsecloset.com/'+path
    chunks = [m for m in re.finditer(r'<url>.*?</url>',sitemap,re.S) if '<loc>'+url+'</loc>' in m.group()]
    assert len(chunks)==1,path
    old = chunks[0].group()
    new = re.sub(r'\s*<image:image>.*?</image:image>','',old,flags=re.S)
    entries = ''.join('\n    <image:image><image:loc>'+u+'</image:loc></image:image>' for u in images)
    new = new.replace('</url>',entries+'\n  </url>')
    sitemap = sitemap.replace(old,new,1)
    repairs.append(dict(file=path,images=images,asset_map_sha256={u:assets[u]['sha256'] for u in images}))
(ROOT/'sitemap.xml').write_bytes(sitemap.encode('utf-8'))

changes = git('diff','--name-status',BASE,FIX,'--','blog').decode().splitlines()
files = {}
for line in changes:
    status,path = line.split('\t')
    after = canon((ROOT/path).read_bytes())
    before = canon(git('show',BASE+':'+path)) if status=='M' else None
    files[path] = dict(kind='modified' if status=='M' else 'added',
                       before_sha256=sha(before.encode()) if before is not None else None,
                       after_sha256=sha(after.encode()),after_crlf_sha256=sha(after.replace('\n','\r\n').encode()))
# blog.html has only the four reviewed added cards; historical gates also lock its bytes.
path='blog.html';before=canon(git('show',BASE+':'+path));after=canon((ROOT/path).read_bytes())
files[path]=dict(kind='modified',before_sha256=sha(before.encode()),after_sha256=sha(after.encode()),
                 after_crlf_sha256=sha(after.replace('\n','\r\n').encode()))
sources = {}
for phase in [1,3,4,5]:
    p=f'tools/phase{phase}_patches.json';sources[p]=sha(git('show',FIX+':'+p))
release = dict(version=1,baseline=BASE,vi_release_commit=FIX,
               hash_encoding='UTF-8; exact LF Git bytes and explicitly pinned CRLF checkout bytes',
               files=files,patch_sources=sources,new_hub_creation_commit='985f5e3',
               log_sha256=sha(canon(logpath.read_bytes()).encode()),
               log_rows=len(list(csv.DictReader(io.StringIO(logpath.read_text(encoding='utf-8'))))),
               image_sitemap_repairs=repairs,en_source_successors={})
dest=D/'release-manifest.json'
if dest.exists():assert json.loads(dest.read_text(encoding='utf-8'))==release,'Existing release manifest is immutable'
else:dest.write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Pinned',len(files),'files; appended log spans',len(extra),'; repaired two sitemap image lists.')
