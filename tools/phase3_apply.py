"""Apply frozen reviewed replacements with an audit after every batch."""
import collections,csv,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
patches=json.loads((ROOT/'tools/phase3_patches.json').read_text(encoding='utf8'))
groups=collections.OrderedDict()
for p in sorted(patches,key=lambda p:p['kind']!='down'):groups.setdefault(p['file'],[]).append(p)

def read_counts(text):
    result={}
    for line in text.splitlines():
        m=re.match(r'\[(PASS|FAIL)\] (G\d+) ',line)
        if m:
            n=re.search(r'\((\d+)\)$',line);result[m[2]]=int(n[1]) if n else 0
    assert len(result)==11,text
    return result

log_path=ROOT/'tools/phase3_batches.json'
log=json.loads(log_path.read_text(encoding='utf8')) if log_path.exists() else []
completed={f for b in log for f in b['files']}
previous=log[-1]['gates'] if log else read_counts((ROOT/'tools/audit_phase3_before.txt').read_text(encoding='utf8'))
files=list(groups)
# Complete parent navigation first, then child prose in groups of about 25 files.
parents=[f for f in files if f not in completed and any(p['kind']=='down' for p in groups[f])]
children=[f for f in files if f not in parents and f not in completed]
batches=([parents] if parents else [])+[children[i:i+25] for i in range(0,len(children),25)]
for number,batch in enumerate(batches,len(log)+1):
    backups={}
    for file in batch:
        path=ROOT/file;raw=path.read_bytes();backups[file]=raw;text=raw.decode('utf8')
        for p in groups[file]:
            assert text.count(p['old'])==1,(file,p.get('id'))
            text=text.replace(p['old'],p['new'],1)
        path.write_bytes(text.encode('utf8'))
    label=f'phase3_batch_{number:02d}'
    run=subprocess.run([sys.executable,'tools/internal_link_audit.py','--root','.','--csv',f'tools/audit_{label}.csv'],cwd=ROOT,capture_output=True,text=True,encoding='utf8')
    (ROOT/f'tools/audit_{label}.txt').write_text(run.stdout+run.stderr,encoding='utf8')
    counts=read_counts(run.stdout)
    worse={g:(previous[g],n) for g,n in counts.items() if n>previous[g]}
    if worse:
        for file,raw in backups.items():(ROOT/file).write_bytes(raw)
        raise RuntimeError(f'Batch {number} rolled back: {worse}')
    log.append(dict(batch=number,files=batch,gates=counts))
    (ROOT/'tools/phase3_batches.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf8')
    previous=counts
    print(f'Batch {number}: {len(batch)} files; '+', '.join(f'{g}={n}' for g,n in counts.items()),flush=True)

from phase3_log import write_log
write_log()
assert previous['G4']==0,previous
print('Phase-three coverage complete; change log appended.',flush=True)
