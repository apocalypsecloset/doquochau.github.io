"""Compile only literal, individually reviewed anchor labels into exact paragraph patches."""
import collections,csv,html,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));import internal_link_audit_en as A
data=json.loads((D/'after_cleanup.json').read_text(encoding='utf-8'));plan=json.loads((D/'rename_plan.json').read_text(encoding='utf-8'))
choices={}
for path in sorted(D.glob('anchors_*.tsv')):
 for key,label in csv.reader(path.open(encoding='utf-8'),delimiter='\t'):
  key=int(key);assert key not in choices;choices[key]=label
assert set(choices)=={r['id'] for r in plan},(len(choices),len(plan))
counts=collections.Counter((r['target'],r['anchor'].lower()) for r in data['anchors'] if r['target'] in data['pages'] and not data['pages'][r['source']]['hub'])
for row in plan:
 label=choices[row['id']];assert not row['protected'];assert 2<=len(label.split())<=6 and not A.GENERIC.match(label) and not A.BAD.search(label),(row['id'],label)
 counts[row['target'],row['anchor'].lower()]-=1;counts[row['target'],label.lower()]+=1
assert max(counts.values())<=5,[((t,a),n) for (t,a),n in counts.items() if n>5]
groups=collections.defaultdict(list)
for row in plan:groups[row['source']].append(row)
ledger_path=D/'anchor_patches.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else []
done={r['source'] for r in ledger};ready=[p for p in groups if p not in done][:25]
updates={};entries=[];tables={}
for source in ready:
 raw=(ROOT/source).read_bytes().decode('utf-8');original=raw;containers=collections.defaultdict(list)
 for row in groups[source]:containers[row['container_start']].append(row)
 for start,items in sorted(containers.items(),reverse=True):
  tag=items[0]['container_tag'];end=raw.index('</'+tag,start);end=raw.index('>',end)+1;before=raw[start:end];after=before
  assert original.count(before)==1,(source,start)
  for row in sorted(items,key=lambda r:r['start'],reverse=True):
   offset=row['start']-start;old=row['old'];assert after[offset:offset+len(old)]==old,(source,row['id'])
   replacement=old[:old.index('>')+1]+html.escape(choices[row['id']])+old[old.rfind('</'):]
   after=after[:offset]+replacement+after[offset+len(old):]
  raw=raw[:start]+after+raw[end:]
  entries.append({'source':source,'vi_source':data['pages'][source]['vi'] or '','kind':'anchor-label','en_before':before,'en_after':after,
                  'labels':json.dumps([{'id':r['id'],'target':r['target'],'old':r['anchor'],'new':choices[r['id']]} for r in items],ensure_ascii=False)})
 a,b=BeautifulSoup(original,'html.parser'),BeautifulSoup(raw,'html.parser')
 for sel in ['title','meta','link','img','h1','h2','h3','h4','script','.toc','#toc','.article-toc','.seo-faq','.faq-section','#faq','.faq','.ac-reading-path','.ac-sources']:
  assert [str(n) for n in a.select(sel)]==[str(n) for n in b.select(sel)],(source,sel)
 updates[source]=raw.encode('utf-8');local=[r for r in entries if r['source']==source];buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(local[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(local)
 table='data/en-translations/internal-links/e4/'+Path(source).stem+'.anchors.tsv';tables[table]=buf.getvalue().encode('utf-8')
 for r in local:r['tsv']=table
def audit():
 r=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT)],capture_output=True,encoding='utf-8');assert r.returncode in (0,1)
 items=re.findall(r'^\[(PASS|FAIL)\] E(\d+) [^\n]*?(?:  \((\d+)\))?$',r.stdout,re.M);assert len(items)==14
 return r.stdout,{n:int(c or 0) for state,n,c in items}
print(json.dumps({'files':len(ready),'anchors':sum(len(groups[p]) for p in ready),'previous_files':len(done),'apply':'--apply' in sys.argv}))
if '--apply' not in sys.argv or not ready:sys.exit(0)
before_log,before=audit();backup={p:(ROOT/p).read_bytes() for p in updates}
try:
 for p,raw in updates.items():(ROOT/p).write_bytes(raw)
 after_log,after=audit();assert all(after[g]<=before[g] for g in before),(before,after)
except BaseException:
 for p,raw in backup.items():(ROOT/p).write_bytes(raw)
 raise
for p,raw in tables.items():assert not (ROOT/p).exists();(ROOT/p).write_bytes(raw)
ledger.extend(entries);ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
number=len(done)+len(ready);(D/('anchors_%03d_audit.txt'%number)).write_text(after_log,encoding='utf-8');print(json.dumps({'files_done':number,'after':after}))
