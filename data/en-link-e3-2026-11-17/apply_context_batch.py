"""Replay individually reviewed sentences into exact frozen paragraphs, at most 25 files.

Default is read-only. No translation source hash or legacy QA is modified here.
"""
import argparse, collections, csv, hashlib, html, importlib.util, io, json, re, subprocess, sys
from html.parser import HTMLParser
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]; D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
import internal_link_audit_en as audit
BASE='a0272175089f56498bfecc40961a21baeb46fcf2'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def readjson(path): return json.loads(path.read_text(encoding='utf-8'))
plan=readjson(D/'plan.json'); paragraphs=readjson(D/'paragraphs.json')
spec=importlib.util.spec_from_file_location('reviewed',D/'reviewed_sentences.py')
reviewed=importlib.util.module_from_spec(spec);spec.loader.exec_module(reviewed)
sentences=dict(reviewed.SENTENCES)
for path in sorted(D.glob('sentences_*.tsv')):
 for key,text in csv.reader(path.open(encoding='utf-8'),delimiter='\t'):
  key=int(key);assert key not in sentences,key
  assert text.count('[')==text.count(']')==1,(key,text)
  anchor=text[text.index('[')+1:text.index(']')]
  markup='<a href="/'+plan[key]['target']+'" hreflang="en">'+html.escape(anchor)+'</a>'
  sentences[key]=text[:text.index('[')]+markup+text[text.index(']')+1:]

class Boundary(HTMLParser):
 def __init__(self,raw):
  super().__init__(convert_charrefs=False);self.raw=raw;self.stack=[];self.cut=None
  self.lines=[0]+[m.end() for m in re.finditer('\n',raw)];self.feed(raw)
 def handle_starttag(self,tag,attrs): self.stack.append(tag)
 def handle_endtag(self,tag):
  if tag in self.stack: self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
 def handle_data(self,data):
  if self.cut is not None or self.stack!=['p']:return
  m=re.search(r'[.!?](?=\s+\S)',data)
  if m:
   line,col=self.getpos();self.cut=self.lines[line-1]+col+m.end()

def protected(raw):
 soup=BeautifulSoup(raw,'html.parser')
 selectors=['title','meta','link','img','h1','h2','h3','h4','script[type="application/ld+json"]',
            '.toc','.article-toc','.seo-faq','.faq-section','.hub-locale','.ac-locale-link']
 return {sel:[str(n) for n in soup.select(sel)] for sel in selectors}

def gate_counts(output):
 rows=re.findall(r'^\[(PASS|FAIL)\] E(\d+) [^\n]*?(?:  \((\d+)\))?$',output,re.M)
 assert len(rows)==14,output
 return {n:int(count or 0) for state,n,count in rows}

def run_audit():
 r=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT)],capture_output=True,encoding='utf-8')
 assert r.returncode in (0,1),(r.returncode,r.stderr)
 return r.stdout,gate_counts(r.stdout)

ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');ap.add_argument('--limit',type=int,default=25)
args=ap.parse_args(); assert 1<=args.limit<=25
ledger_path=D/'context_batches.json';ledger=readjson(ledger_path) if ledger_path.exists() else []
done={f['source'] for b in ledger for f in b['files']}
by=collections.defaultdict(list)
for row in plan:by[row['source']].append(row)
ready=[p for p,rows in by.items() if p not in done and all(r['id'] in sentences for r in rows)][:args.limit]

# Account for all authored anchors against the unchanged E2 inventory, including earlier batches.
baseline=readjson(D/'inventory.json'); frequencies=collections.Counter()
for row in baseline:
 for target,anchor,context,lang in row['prose']:frequencies[target,anchor.lower()]+=1
for key,sentence in sentences.items():
 row=plan[key];a=BeautifulSoup(sentence,'html.parser').find_all('a')
 assert len(a)==1 and a[0]['href']=='/'+row['target'] and a[0]['hreflang']=='en',key
 anchor=a[0].get_text(' ',strip=True)
 assert 2<=len(anchor.split())<=6 and not audit.GENERIC.match(anchor),(key,anchor)
 assert not audit.BAD.search(BeautifulSoup(sentence,'html.parser').get_text()),key
 assert (ROOT/row['target']).is_file(),row['target']
 frequencies[row['target'],anchor.lower()]+=1
 assert frequencies[row['target'],anchor.lower()]<=5,(key,anchor,frequencies[row['target'],anchor.lower()])

files=[];updates={};tables={}
for source in ready:
 raw=(ROOT/source).read_bytes();old=raw.decode('utf-8')
 original=subprocess.check_output(['git','show',BASE+':'+source],cwd=ROOT).decode('utf-8')
 assert old.replace('\r\n','\n')==original.replace('\r\n','\n'),source
 rows=by[source];assert len(rows)<=4
 groups=collections.defaultdict(list)
 for row in rows:groups[reviewed.PARAGRAPH.get(row['id'],row['paragraph'])].append(row)
 current=old;patches=[];entries=[]
 for index,items in groups.items():
  before=next(p['old'] for p in paragraphs[source] if p['index']==index)
  assert current.count(before)==1,(source,index)
  offset=Boundary(before).cut
  if offset is None:offset=before.index('>')+1;insert=' '.join(sentences[r['id']] for r in items)+' '
  else:insert=' '+' '.join(sentences[r['id']] for r in items)
  after=before[:offset]+insert+before[offset:]
  assert after.replace(insert,'',1)==before
  current=current.replace(before,after,1);patches.append({'paragraph':index,'before':before,'after':after})
  for row in items:
   a=BeautifulSoup(sentences[row['id']],'html.parser').a
   entries.append({'id':row['id'],'source':source,'vi_source':next(r['vi'] or '' for r in baseline if r['en']==source),
    'vi_context':row['vi_context'],'vi_anchor':row['vi_anchor'],'target':row['target'],
    'anchor':a.get_text(' ',strip=True),'sentence':sentences[row['id']],'paragraph':index,'en_before':before,'en_after':after})
 assert protected(old)==protected(current),source
 for tag in ['p','li','table','td','th','details','figcaption']:
  assert len(BeautifulSoup(old,'html.parser').select(tag))==len(BeautifulSoup(current,'html.parser').select(tag)),(source,tag)
 table=io.StringIO(newline='');writer=csv.DictWriter(table,fieldnames=list(entries[0]),delimiter='\t',lineterminator='\n')
 writer.writeheader();writer.writerows(entries)
 tablepath='data/en-translations/internal-links/'+Path(source).stem+'.tsv'
 tables[tablepath]=table.getvalue().encode('utf-8');updates[source]=current.encode('utf-8')
 files.append({'source':source,'before_sha256':sha(raw),'after_sha256':sha(updates[source]),'tsv':tablepath,
               'tsv_sha256':sha(tables[tablepath]),'link_ids':[r['id'] for r in rows],'patches':patches})
print(json.dumps({'authored':len(sentences),'total':len(plan),'previously_applied_files':len(done),'ready_files':len(ready),'new_links':sum(len(f['link_ids']) for f in files),'apply':args.apply}))
if not args.apply or not ready:sys.exit(0)
before_log,before_gates=run_audit();backups={p:(ROOT/p).read_bytes() for p in updates}
try:
 for path,raw in updates.items():(ROOT/path).write_bytes(raw)
 after_log,after_gates=run_audit()
 assert all(after_gates[g]<=before_gates[g] for g in before_gates),(before_gates,after_gates)
except BaseException:
 for path,raw in backups.items():(ROOT/path).write_bytes(raw)
 raise
for path,raw in tables.items():
 p=ROOT/path;assert not p.exists(),path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
number=len(ledger)+1
batch={'batch':number,'baseline':BASE,'before_gates':before_gates,'after_gates':after_gates,'files':files}
ledger.append(batch);ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/('context_batch_%02d_before.txt'%number)).write_text(before_log,encoding='utf-8')
(D/('context_batch_%02d_after.txt'%number)).write_text(after_log,encoding='utf-8')
print(json.dumps({'batch':number,'after_gates':after_gates,'files':len(files)}))
