"""Apply reviewed exact paragraph replacements in batches, auditing each batch."""
import collections, csv, json, os, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
patches=json.loads((ROOT/'tools/phase1_patches.json').read_text(encoding='utf8'))
groups=collections.defaultdict(list)
for p in patches:groups[p['file']].append(p)

def audit(label):
    result=subprocess.run([sys.executable,'tools/internal_link_audit.py','--root','.','--csv',f'tools/audit_{label}.csv'],cwd=ROOT,capture_output=True,text=True,encoding='utf8')
    (ROOT/f'tools/audit_{label}.txt').write_text(result.stdout+result.stderr,encoding='utf8')
    # Explicit line parsing also tolerates changes in prose wording.
    counts={}
    for line in result.stdout.splitlines():
        m=re.match(r'\[(PASS|FAIL)\] (G\d+) ',line)
        if m:
            n=re.search(r'\((\d+)\)$',line)
            counts[m[2]]=int(n[1]) if n else 0
    assert len(counts)==11,(result.returncode,result.stdout,result.stderr)
    return counts

previous=audit('phase1_start')
files=list(groups)
log=[]
for batch,start in enumerate(range(0,len(files),25),1):
    backups={}
    for file in files[start:start+25]:
        path=ROOT/file;raw=path.read_bytes();text=raw.decode('utf8');backups[file]=raw
        for p in groups[file]:
            assert text.count(p['old'])==1,(file,p['ids'])
            text=text.replace(p['old'],p['new'],1)
        path.write_bytes(text.encode('utf8'))
    counts=audit(f'phase1_batch_{batch:02d}')
    worse={g:(previous[g],n) for g,n in counts.items() if n>previous[g]}
    if worse:
        for file,raw in backups.items():(ROOT/file).write_bytes(raw)
        raise RuntimeError(f'Batch {batch} rolled back: {worse}')
    log.append(dict(batch=batch,files=files[start:start+25],gates=counts))
    (ROOT/'tools/phase1_batches.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf8')
    previous=counts
    print(f'Batch {batch}: {len(backups)} files; '+', '.join(f'{g}={n}' for g,n in counts.items()),flush=True)

rows=json.loads((ROOT/'tools/phase1_inventory.json').read_text(encoding='utf8'))
byid={r['id']:r for r in rows}
from bs4 import BeautifulSoup
with (ROOT/'tools/link_changes.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.writer(f);w.writerow(['file','đích','anchor','câu_trước','câu_sau'])
    for p in patches:
        before=BeautifulSoup(p['old'],'html.parser');after=BeautifulSoup(p['new'],'html.parser')
        w.writerow([p['file'],' | '.join(dict.fromkeys(byid[i]['target'] for i in p['ids'])),' | '.join(a.get_text(' ',strip=True) for a in after.find_all('a')),before.get_text(' ',strip=True),after.get_text(' ',strip=True)])
print('All phase-one batches applied; editorial log written.',flush=True)
