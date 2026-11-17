"""Apply the frozen exact replacements in audited batches, with rollback on regression."""
import collections,csv,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
patches=json.loads((ROOT/'tools/phase4_patches.json').read_text(encoding='utf8'))
groups=collections.OrderedDict()
for p in patches:groups.setdefault(p['file'],[]).append(p)
def counts(text):
    out={}
    for line in text.splitlines():
        m=re.match(r'\[(PASS|FAIL)\] (G\d+) ',line)
        if m:
            n=re.search(r'\((\d+)\)$',line);out[m[2]]=int(n[1]) if n else 0
    assert len(out)==11,text
    return out
history_path=ROOT/'tools/phase4_batches.json'
history=json.loads(history_path.read_text(encoding='utf8')) if history_path.exists() else []
done={f for b in history for f in b['files']}
previous=history[-1]['gates'] if history else counts((ROOT/'tools/audit_phase4_before.txt').read_text(encoding='utf8'))
files=[f for f in groups if f not in done]
for number,start in enumerate(range(0,len(files),25),len(history)+1):
    batch=files[start:start+25];backups={}
    for file in batch:
        path=ROOT/file;raw=path.read_bytes();backups[file]=raw;text=raw.decode('utf8')
        for p in groups[file]:
            assert text.count(p['old'])==1,(file,p['paragraph'])
            text=text.replace(p['old'],p['new'],1)
        path.write_bytes(text.encode('utf8'))
    label=f'phase4_batch_{number:02d}'
    run=subprocess.run([sys.executable,'tools/internal_link_audit.py','--root','.','--csv',f'tools/audit_{label}.csv'],cwd=ROOT,capture_output=True,text=True,encoding='utf8')
    (ROOT/f'tools/audit_{label}.txt').write_text(run.stdout+run.stderr,encoding='utf8')
    current=counts(run.stdout);worse={g:(previous[g],n) for g,n in current.items() if n>previous[g]}
    if worse:
        for file,raw in backups.items():(ROOT/file).write_bytes(raw)
        raise RuntimeError(f'Batch {number} rolled back: {worse}')
    history.append(dict(batch=number,files=batch,gates=current));previous=current
    history_path.write_text(json.dumps(history,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'Batch {number}: {len(batch)} files; '+', '.join(f'{g}={n}' for g,n in current.items()),flush=True)
assert all(n==0 for n in previous.values()),previous

# The earlier phases remain byte-for-byte intact, and repeating the completed
# phase cannot silently drop records from a later phase.
baseline=subprocess.check_output(['git','show','bddd970:tools/link_changes.csv'],cwd=ROOT)
current=(ROOT/'tools/link_changes.csv').read_bytes()
prefix=next((p for p in [baseline,baseline.replace(b'\n',b'\r\n')] if current.startswith(p)),None)
assert prefix is not None
prior_count=len(list(csv.reader(io.StringIO(prefix.decode('utf8')))))
current_count=len(list(csv.reader(io.StringIO(current.decode('utf8')))))
assert current_count in (prior_count,prior_count+365)
output=io.StringIO(newline='');w=csv.writer(output);n=0
for p in patches:
    before=BeautifulSoup(p['old'],'html.parser').get_text(' ',strip=True)
    after=BeautifulSoup(p['new'],'html.parser').get_text(' ',strip=True)
    for a in p['links']:
        w.writerow([p['file'],'/blog/'+a['target']+'.html',a['anchor'],before,after]);n+=1
assert n==365,n
(ROOT/'tools/link_changes.csv').write_bytes(prefix+output.getvalue().encode('utf8'))
print('All 11 gates PASS; phase-four change log written.',flush=True)
