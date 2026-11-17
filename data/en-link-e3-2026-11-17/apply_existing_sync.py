"""Synchronize the English sentence for already-present VI links; add no destinations."""
import collections,csv,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
plan=json.loads((D/'existing_link_sync_plan.json').read_text(encoding='utf-8'))
copy={int(k):text for k,text in csv.reader((D/'existing_link_sync.tsv').open(encoding='utf-8'),delimiter='\t')}
ledger_path=D/'existing_link_sync_patches.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else []
done={r['id'] for r in ledger};rows=[r for r in plan if r['id'] not in done][:25]
def counts(out):
 rows=re.findall(r'^\[(PASS|FAIL)\] E(\d+) [^\n]*?(?:  \((\d+)\))?$',out,re.M);assert len(rows)==14
 return {n:int(c or 0) for state,n,c in rows}
def audit():
 r=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT)],capture_output=True,encoding='utf-8');assert r.returncode in (0,1)
 return r.stdout,counts(r.stdout)
updates={};tables={};entries=[]
for row in rows:
 p=ROOT/row['source'];raw=p.read_bytes().decode('utf-8');before=row['en_before'];after=copy[row['id']]
 assert raw.count(before)==1,row['source']
 a,b=BeautifulSoup(before,'html.parser'),BeautifulSoup(after,'html.parser')
 links=lambda s:collections.Counter(n['href'] for n in s.select('a[href]'))
 assert links(a)==links(b),row['source']
 for link in b.select('a[href^="/en/blog/"]'):assert 2<=len(link.get_text(' ',strip=True).split())<=6,(row['id'],link)
 current=raw.replace(before,after,1);a,b=BeautifulSoup(raw,'html.parser'),BeautifulSoup(current,'html.parser')
 for sel in ['title','meta','link','img','h1','h2','h3','h4','script','.toc','#toc','.article-toc','.seo-faq','.faq-section']:
  assert [str(n) for n in a.select(sel)]==[str(n) for n in b.select(sel)],(row['source'],sel)
 entry={**row,'kind':'existing-link-sentence','en_after':after}
 table=io.StringIO(newline='');w=csv.DictWriter(table,fieldnames=list(entry),delimiter='\t',lineterminator='\n');w.writeheader();w.writerow(entry)
 name='data/en-translations/internal-links/'+p.stem+'.existing-link.tsv'
 assert not (ROOT/name).exists();tables[name]=table.getvalue().encode('utf-8');updates[row['source']]=current.encode('utf-8')
 entry['tsv']=name;entries.append(entry)
print(json.dumps({'files':len(updates),'apply':'--apply' in sys.argv}))
if '--apply' not in sys.argv or not rows:sys.exit(0)
before_log,before=audit();backup={p:(ROOT/p).read_bytes() for p in updates}
try:
 for p,raw in updates.items():(ROOT/p).write_bytes(raw)
 after_log,after=audit();assert all(after[g]<=before[g] for g in before),(before,after)
except BaseException:
 for p,raw in backup.items():(ROOT/p).write_bytes(raw)
 raise
for p,raw in tables.items():(ROOT/p).write_bytes(raw)
ledger+=entries;ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/('existing_sync_%02d_audit.txt'%len(ledger))).write_text(after_log,encoding='utf-8')
print(json.dumps({'files_done':len(ledger),'after_gates':after}))
