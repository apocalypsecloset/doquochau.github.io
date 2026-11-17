"""Supply four missing sitewide variants through reviewed existing prose and two sentences."""
import collections,csv,html,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
ledger=json.loads((D/'anchor_patches.json').read_text(encoding='utf-8'))
assert sum(len(json.loads(r['labels'])) for r in ledger)==175,'Finish all reviewed frequency repairs first.'
assert not (D/'variety_patches.json').exists()
choices=[
 {'source':'en/blog/fairycore-style-guide.html','needle':'Cottagecore','kind':'anchor-label',
  'old_label':'Cottagecore','new_label':'The Cottagecore rural aesthetic','target':'en/blog/cottagecore-style-guide.html'},
 {'source':'en/blog/fashion-aesthetic-directory.html','needle':'The burnout article is broader reading','kind':'link-wrap',
  'old_label':'wardrobe example','new_label':'wardrobe example','target':'en/blog/understanding-job-burnout.html'},
 {'source':'en/blog/what-is-grunge-style-vs-punk.html','needle':'Do not identify grunge through one item alone.','kind':'context-addition',
  'sentence':'For the other comparison, use <a href="/en/blog/goth-vs-grunge-style.html" hreflang="en">Goth versus Grunge outfit cues</a> to distinguish dark color from the shapes and textures around it.'},
 {'source':'en/blog/alternative-t-shirt-outfits-women.html','needle':'Fit changes the result.','kind':'context-addition',
  'sentence':'For a specifically Gothic treatment, compare <a href="/en/blog/how-to-style-gothic-graphic-tees.html" hreflang="en">Gothic graphic tee outfit proportions</a> while retaining the same shirt as the starting point.'},
]
updates={};entries=[];tables={}
for row in choices:
 source=row['source'];raw=(ROOT/source).read_bytes().decode('utf-8');s=BeautifulSoup(raw,'html.parser');ps=[p for p in s.select('p') if row['needle'] in p.get_text()];assert len(ps)==1,source;p=ps[0]
 lines=[0]+[m.end() for m in re.finditer('\n',raw)];start=lines[p.sourceline-1]+p.sourcepos;end=raw.index('</p>',start)+4;before=raw[start:end]
 if row['kind']=='anchor-label':
  old='>'+row['old_label']+'</a>';new='>'+html.escape(row['new_label'])+'</a>';assert before.count(old)==1;after=before.replace(old,new,1)
  row['labels']=json.dumps([{'target':row['target'],'old':row['old_label'],'new':row['new_label']}])
 elif row['kind']=='link-wrap':
  assert before.count(row['old_label'])==1
  link='<a href="/'+row['target']+'" hreflang="en">'+row['new_label']+'</a>';after=before.replace(row['old_label'],link,1)
 else:
  sentence=row['sentence'];assert before.count(row['needle'])==1;after=before.replace(row['needle'],row['needle']+' '+sentence,1)
 row.update(vi_source=(s.select_one('link[hreflang="vi"]').get('href','').replace('https://apocalypsecloset.com/','') if s.select_one('link[hreflang="vi"]') else ''),en_before=before,en_after=after)
 assert raw.count(before)==1;updates[source]=raw.replace(before,after,1).encode('utf-8')
 table='data/en-translations/internal-links/e4/'+Path(source).stem+'.variety.tsv';buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(row),delimiter='\t',lineterminator='\n');w.writeheader();w.writerow(row);tables[table]=buf.getvalue().encode('utf-8');row['tsv']=table;entries.append(row)
def audit():
 r=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT)],capture_output=True,encoding='utf-8');assert r.returncode in (0,1)
 items=re.findall(r'^\[(PASS|FAIL)\] E(\d+) [^\n]*?(?:  \((\d+)\))?$',r.stdout,re.M);assert len(items)==14
 return r.stdout,{n:int(c or 0) for state,n,c in items}
print(json.dumps({'files':4,'new_contextual_links':3,'existing_anchor_variants':1,'apply':'--apply' in sys.argv}))
if '--apply' not in sys.argv:sys.exit(0)
before_log,before=audit();backup={p:(ROOT/p).read_bytes() for p in updates}
try:
 for p,raw in updates.items():(ROOT/p).write_bytes(raw)
 after_log,after=audit();assert all(after[g]<=before[g] for g in before),(before,after)
except BaseException:
 for p,raw in backup.items():(ROOT/p).write_bytes(raw)
 raise
for p,raw in tables.items():assert not (ROOT/p).exists();(ROOT/p).write_bytes(raw)
(D/'variety_patches.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'variety_audit_after.txt').write_text(after_log,encoding='utf-8');print(json.dumps({'after':after}))
