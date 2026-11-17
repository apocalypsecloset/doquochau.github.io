"""Remove redundant anchor wrappers only, in audited batches of at most 25 files."""
import collections,csv,io,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));from bs4 import BeautifulSoup
data=json.loads((D/'inventory.json').read_text(encoding='utf-8'));rows=data['anchors'];pages=data['pages']
counts=collections.Counter((r['target'],r['anchor'].lower()) for r in rows)
remove=[];keep=[]
for group in data['duplicates']:
 ids=group['ids'];protected=[i for i in ids if rows[i]['protected']]
 assert len(protected)<=1,group
 if protected:chosen=protected[0]
 elif group['source']=='en/blog/what-is-goth-style.html' and group['target']=='en/blog/buying-goth-clothing-women.html':chosen=2982
 else:chosen=min(ids,key=lambda i:(counts[rows[i]['target'],rows[i]['anchor'].lower()],i))
 keep.append(chosen);remove.extend(i for i in ids if i!=chosen)
# The only thirteenth target is additional navigation; all twelve VI targets remain.
remove.append(2983)
assert all(not rows[i]['protected'] for i in remove)
groups=collections.defaultdict(list)
for i in remove:groups[rows[i]['source']].append(rows[i])
ledger_path=D/'duplicate_patches.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else []
done={r['source'] for r in ledger};ready=[p for p in groups if p not in done][:25]
def audit():
 r=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT)],capture_output=True,encoding='utf-8');assert r.returncode in (0,1),r.stderr
 items=re.findall(r'^\[(PASS|FAIL)\] E(\d+) [^\n]*?(?:  \((\d+)\))?$',r.stdout,re.M);assert len(items)==14
 return r.stdout,{n:int(count or 0) for state,n,count in items}
updates={};entries=[];tables={}
for source in ready:
 raw=(ROOT/source).read_bytes().decode('utf-8');original=raw;containers=collections.defaultdict(list)
 for row in groups[source]:containers[row['container_start']].append(row)
 for start,items in sorted(containers.items(),reverse=True):
  tag=items[0]['container_tag'];end=raw.index('</'+tag,start);end=raw.index('>',end)+1
  before=raw[start:end];after=before
  assert original.count(before)==1,(source,start)
  for row in sorted(items,key=lambda r:r['start'],reverse=True):
   offset=row['start']-start;assert after[offset:offset+len(row['old'])]==row['old']
   anchor=row['old'];inner=anchor[anchor.index('>')+1:anchor.rfind('</')]
   after=after[:offset]+inner+after[offset+len(anchor):]
  assert BeautifulSoup(before,'html.parser').get_text()==BeautifulSoup(after,'html.parser').get_text()
  raw=raw[:start]+after+raw[end:]
  entries.append({'source':source,'vi_source':pages[source]['vi'] or '','kind':'duplicate-or-density','en_before':before,'en_after':after,'removed_ids':json.dumps([r['id'] for r in items])})
 updates[source]=raw.encode('utf-8')
 local=[r for r in entries if r['source']==source];buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(local[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(local)
 table='data/en-translations/internal-links/e4/'+Path(source).stem+'.duplicates.tsv';tables[table]=buf.getvalue().encode('utf-8')
 for r in local:r['tsv']=table
print(json.dumps({'files':len(ready),'removed_occurrences':sum(len(groups[p]) for p in ready),'previous_files':len(done),'apply':'--apply' in sys.argv}))
if '--apply' not in sys.argv or not ready:sys.exit(0)
before_log,before=audit();backup={p:(ROOT/p).read_bytes() for p in updates}
try:
 for p,raw in updates.items():(ROOT/p).write_bytes(raw)
 after_log,after=audit();assert all(after[g]<=before[g] for g in before),(before,after)
except BaseException:
 for p,raw in backup.items():(ROOT/p).write_bytes(raw)
 raise
for p,raw in tables.items():
 path=ROOT/p;assert not path.exists();path.parent.mkdir(exist_ok=True);path.write_bytes(raw)
ledger.extend(entries);ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
number=len(done)+len(ready);(D/('duplicates_%03d_audit.txt'%number)).write_text(after_log,encoding='utf-8')
print(json.dumps({'after':after,'files_done':number}))
