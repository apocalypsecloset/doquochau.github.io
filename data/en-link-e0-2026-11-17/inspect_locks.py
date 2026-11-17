"""E0 evidence only: reproduce legacy source normalization without changing locks."""
import collections
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from privacy_release import original
from bs4 import BeautifulSoup
def digest(raw):return hashlib.sha256(raw.encode()).hexdigest()
def source_raw(path,raw):
    return re.sub(r'<!-- AC-EN-BATCH[0-9]{2}-START -->.*?<!-- AC-EN-BATCH[0-9]{2}-END -->','',original(path,raw),flags=re.S)
configs=[]
for p in sorted((ROOT/'data/en-translations').glob('batch*.json')):
    if p.stem=='batch05b':continue
    configs += [dict(c,batch=p.stem) for c in json.loads(p.read_text(encoding='utf-8'))]
paths=sorted({'blog/'+c['vi_slug']+'.html' for c in configs})
raws=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=('\n'.join('9e16c20:'+p for p in paths)+'\n').encode(),capture_output=True,check=True).stdout
pos=0;old={}
for path in paths:
    end=raws.index(b'\n',pos);size=int(raws[pos:end].split()[-1]);old[path]=raws[end+1:end+1+size].decode('utf-8');pos=end+size+2
rows=[];cache={}
for c in configs:
    path='blog/'+c['vi_slug']+'.html'
    if path not in cache:
        raw=(ROOT/path).read_text(encoding='utf-8')
        cache[path]=(digest(source_raw(path,raw)),digest(source_raw(path,old[path])),digest(raw),digest(old[path]))
    actual,before,current_raw,old_raw=cache[path]
    rows.append(dict(batch=c['batch'],vi_slug=c['vi_slug'],en_slug=c['en_slug'],kind=c.get('source_kind','article'),
                     expected_source_sha256=c['source_sha256'],actual_source_sha256=actual,
                     before_vi_fix_source_sha256=before,source_lock_matches=actual==c['source_sha256'],
                     prior_source_lock_matches=before==c['source_sha256'],vi_raw_changed=current_raw!=old_raw))
(OUT/'source_hash_locks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'source_hash_locks.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(config_entries=len(rows),unique_vi_files=len(paths),batches=len(set(r['batch'] for r in rows)),
             mismatch_entries=sum(not r['source_lock_matches'] for r in rows),
             mismatch_unique_files=len({r['vi_slug'] for r in rows if not r['source_lock_matches']}),
             preexisting_mismatch_entries=sum(not r['prior_source_lock_matches'] for r in rows),
             changed_vi_source_files=sum(a[2]!=a[3] for a in cache.values()),
             affected_batches=dict(collections.Counter(r['batch'] for r in rows if not r['source_lock_matches'])))
(OUT/'source_hash_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
