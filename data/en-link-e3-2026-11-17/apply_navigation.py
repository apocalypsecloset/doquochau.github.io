"""Add reviewed, image-free child cards through exact spans; retain all existing nodes."""
import csv,hashlib,html,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
from navigation_copy import INTRO
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pos(raw,node):
 lines=[0]+[m.end() for m in re.finditer('\n',raw)]
 return lines[node.sourceline-1]+node.sourcepos
def audit():
 r=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT)],capture_output=True,encoding='utf-8')
 assert r.returncode in (0,1),r.stderr
 rows=re.findall(r'^\[(PASS|FAIL)\] E(\d+) [^\n]*?(?:  \((\d+)\))?$',r.stdout,re.M)
 assert len(rows)==14
 return r.stdout,{n:int(count or 0) for state,n,count in rows}
plan=json.loads((D/'navigation_plan.json').read_text(encoding='utf-8'))
assert not (D/'navigation_patches.json').exists(),'Navigation already applied; verify the recorded patches instead.'
updates={};tables={};patches=[]
for row in plan:
 source=row['source'];raw=(ROOT/source).read_bytes().decode('utf-8');original=raw
 # Period-specific guides belong beside the historical references.
 if row['cluster']=='Aesthetic/Style':
  moved=[t for t in row['groups']['internet-alt-aesthetics']['targets'] if Path(t['target']).stem in ('1920s-fashion','victorian-fashion')]
  row['groups']['internet-alt-aesthetics']['targets']=[t for t in row['groups']['internet-alt-aesthetics']['targets'] if t not in moved]
  row['groups']['retro-historical']['targets']+=moved
 entries=[]
 for key,g in row['groups'].items():
  s=BeautifulSoup(raw,'html.parser');h=s.find('h2',id=key) or next(n for n in s.select('h2') if n.get_text(' ',strip=True)==key)
  if h.parent.name=='section':
   node=h.parent;assert not node.select('section')
   start=pos(raw,node);end=raw.index('</section>',start)+len('</section>');before=raw[start:end];offset=before.rindex('</section>')
  else:
   start=pos(raw,h);nxt=h.find_next_sibling('h2')
   end=pos(raw,nxt) if nxt else raw.index('</article>',start)
   before=raw[start:end];offset=len(before)
  cards=[]
  for t in g['targets']:
   assert (ROOT/t['target']).is_file()
   cards.append('<a class="hub-card" href="/'+t['target']+'" hreflang="en" style="display:block;padding:16px;border:1px solid currentColor;border-radius:10px;text-decoration:none;min-width:0"><h3>'+html.escape(t['title'])+'</h3><p>'+html.escape(t['description'])+'</p></a>')
  block='\n<div data-en-link-fix="E3"><p>'+html.escape(INTRO[row['cluster'],key])+'</p><div class="hub-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:16px">\n'+'\n'.join(cards)+'\n</div></div>\n'
  after=before[:offset]+block+before[offset:]
  assert raw.count(before)==1,(source,key)
  raw=raw.replace(before,after,1)
  entry={'kind':'navigation','source':source,'vi_source':row['vi_source'],'heading':key,'vi_context':'\n'.join(g['vi_context']),
         'targets_json':json.dumps([t['target'] for t in g['targets']]),'en_before':before,'en_after':after}
  entries.append(entry);patches.append(entry)
 # Synchronize only CollectionPage.mainEntity with visible hub-card links.
 s=BeautifulSoup(raw,'html.parser')
 for script in s.select('script[type="application/ld+json"]'):
  data=json.loads(script.string);changed=False
  for node in data.get('@graph',[data]):
   if node.get('@type')!='CollectionPage':continue
   body=s.select_one('main.en-hub') or s.main
   cards=body.select('a.hub-card[href]')
   items=[{'@type':'ListItem','position':i+1,'name':a.h3.get_text(' ',strip=True),'url':'https://apocalypsecloset.com'+a['href']} for i,a in enumerate(cards)]
   node['mainEntity']={'@type':'ItemList','numberOfItems':len(items),'itemListElement':items};changed=True
  if changed:
   start=pos(raw,script);end=raw.index('</script>',start)+len('</script>');before=raw[start:end]
   after=before[:before.index('>')+1]+json.dumps(data,ensure_ascii=False,indent=2)+'</script>'
   assert raw.count(before)==1;raw=raw.replace(before,after,1)
   e={'kind':'itemlist','source':source,'vi_source':row['vi_source'],'heading':'CollectionPage.mainEntity','vi_context':'','targets_json':'[]','en_before':before,'en_after':after}
   entries.append(e);patches.append(e)
 a,b=BeautifulSoup(original,'html.parser'),BeautifulSoup(raw,'html.parser')
 for sel in ['title','meta','link','img','h1','.toc','#toc','.article-toc','.seo-faq','.faq-section']:
  assert [str(n) for n in a.select(sel)]==[str(n) for n in b.select(sel)],(source,sel)
 cleaned=BeautifulSoup(raw,'html.parser')
 for n in cleaned.select('[data-en-link-fix="E3"]'):n.decompose()
 for sel in ['h2','h3','h4','p','li','table','details']:
  assert [str(n) for n in a.select(sel)]==[str(n) for n in cleaned.select(sel)],(source,sel)
 graph=lambda soup:[json.loads(j.string) for j in soup.select('script[type="application/ld+json"]')]
 ga,gb=graph(a),graph(b)
 for graphs in (ga,gb):
  for data in graphs:
   for n in data.get('@graph',[data]):
    if n.get('@type')=='CollectionPage':n.pop('mainEntity',None)
 assert ga==gb,source
 table=io.StringIO(newline='');w=csv.DictWriter(table,fieldnames=list(entries[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(entries)
 tablepath='data/en-translations/internal-links/'+Path(source).stem+'.navigation.tsv'
 tables[tablepath]=table.getvalue().encode('utf-8');updates[source]=raw.encode('utf-8')
 for e in entries:e['tsv']=tablepath
print(json.dumps({'files':len(updates),'cards':sum(r['missing'] for r in plan),'patches':len(patches),'apply':'--apply' in sys.argv}))
if '--apply' not in sys.argv:sys.exit(0)
before_log,before=audit();backups={p:(ROOT/p).read_bytes() for p in updates}
try:
 for p,raw in updates.items():(ROOT/p).write_bytes(raw)
 after_log,after=audit();assert all(after[g]<=before[g] for g in before),(before,after)
except BaseException:
 for p,raw in backups.items():(ROOT/p).write_bytes(raw)
 raise
for p,raw in tables.items():assert not (ROOT/p).exists();(ROOT/p).write_bytes(raw)
(D/'navigation_patches.json').write_text(json.dumps(patches,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'navigation_audit_before.txt').write_text(before_log,encoding='utf-8');(D/'navigation_audit_after.txt').write_text(after_log,encoding='utf-8')
print(json.dumps({'before':before,'after':after}))
