"""Replace reviewed technical jargon only; retain URLs and all other paragraph bytes."""
import collections,csv,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
from word_choices import CHOICES
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));import internal_link_audit_en as A
data=json.loads((D/'inventory.json').read_text(encoding='utf-8'));updates={};entries=[];tables={}
assert not (D/'word_patches.json').exists()
norm=lambda s:re.sub(r'\s+','',s)
for i,choices in CHOICES.items():
 row=data['anchors'][i];source=row['source'];raw=updates.get(source,(ROOT/source).read_bytes().decode('utf-8'));s=BeautifulSoup(raw,'html.parser')
 nodes=[p for p in s.select('p') if norm(p.get_text(' ',strip=True))==norm(row['context'])];assert len(nodes)==1,(i,source)
 p=nodes[0];lines=[0]+[m.end() for m in re.finditer('\n',raw)];start=lines[p.sourceline-1]+p.sourcepos;end=raw.index('</p>',start)+4
 before=raw[start:end];after=before
 for old,new in choices:assert after.count(old)==1,(i,old);after=after.replace(old,new,1)
 assert not A.BAD.search(BeautifulSoup(after,'html.parser').get_text(' ',strip=True)),i
 links=lambda x:collections.Counter(a['href'] for a in BeautifulSoup(x,'html.parser').select('a[href]'))
 assert links(before)==links(after),i
 assert raw.count(before)==1;updates[source]=raw.replace(before,after,1)
 entries.append({'source':source,'vi_source':data['pages'][source]['vi'] or '','kind':'terminology','en_before':before,'en_after':after,'choices':json.dumps(choices,ensure_ascii=False)})
for source in updates:
 local=[r for r in entries if r['source']==source];buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(local[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(local)
 table='data/en-translations/internal-links/e4/'+Path(source).stem+'.words.tsv';tables[table]=buf.getvalue().encode('utf-8')
 for r in local:r['tsv']=table
assert len(updates)<=25
def audit():
 r=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT)],capture_output=True,encoding='utf-8');assert r.returncode in (0,1)
 items=re.findall(r'^\[(PASS|FAIL)\] E(\d+) [^\n]*?(?:  \((\d+)\))?$',r.stdout,re.M);assert len(items)==14
 return r.stdout,{n:int(c or 0) for state,n,c in items}
print(json.dumps({'paragraphs':len(entries),'files':len(updates),'apply':'--apply' in sys.argv}))
if '--apply' not in sys.argv:sys.exit(0)
before_log,before=audit();backup={p:(ROOT/p).read_bytes() for p in updates}
try:
 for p,raw in updates.items():(ROOT/p).write_bytes(raw.encode('utf-8'))
 after_log,after=audit();assert all(after[g]<=before[g] for g in before),(before,after)
except BaseException:
 for p,raw in backup.items():(ROOT/p).write_bytes(raw)
 raise
for p,raw in tables.items():assert not (ROOT/p).exists();(ROOT/p).write_bytes(raw)
(D/'word_patches.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'words_audit_after.txt').write_text(after_log,encoding='utf-8');print(json.dumps({'after':after}))
