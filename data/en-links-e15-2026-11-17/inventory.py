import sys,json,re,collections
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
import internal_link_audit_en as A
D=Path(__file__).parent
en={p.relative_to(R).as_posix():BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser') for p in (R/'en').rglob('*.html')}
mapping={A.hreflang(s,'vi'):p for p,s in en.items() if A.hreflang(s,'vi')}
special=lambda t:t.rstrip('/').split('/')[-1].removesuffix('.html') in ('outfits','style','phoi-do-nu-ca-tinh','app-phoi-do')
rows=[];exceptions=[]
for source,s in en.items():
 own=A.hreflang(s,'vi');raw=(R/source).read_text(encoding='utf-8');anchors=list(re.finditer(r'<a\b[^>]*>.*?</a\s*>',raw,re.I|re.S));nodes=s.select('a[href]')
 for i,a in enumerate(nodes):
  target=A.resolve(a['href'],source);label=a.get_text(' ',strip=True)
  if not target:continue
  if target==own or label=='Read the Vietnamese original':
   exceptions.append({'source':source,'anchor':str(a),'kind':'original'});continue
  if special(target):
   exceptions.append({'source':source,'anchor':str(a),'kind':'special','label':label});continue
  if not target.startswith('blog/'):continue
  matches=[m for m in anchors if (lambda n:n and n.get('href')==a['href'] and n.get_text(' ',strip=True)==label)(BeautifulSoup(m[0],'html.parser').a)]
  assert len(matches)==1,(source,a);m=matches[0]
  prose=a.find_parent(['p','li','td','th','figcaption','blockquote'])
  parent=a.find_parent(['p','li','article','main','section','div','nav','footer'])
  region=[]
  for n in a.parents:
   if n.name in ('nav','footer','header'):region.append(n.name)
   region.extend(n.get('class',[]))
  dest=mapping.get(target)
  rows.append({'id':len(rows),'source':source,'index':i,'old':a['href'],'target_vi':target,'target_en':dest,'label':label,'anchor':m[0],
   'context':parent.get_text(' ',strip=True)[:1500] if parent else label,'prose':bool(prose),'region':region,
   'target_title':en[dest].title.get_text(' ',strip=True) if dest else '', 'target_h1':en[dest].h1.get_text(' ',strip=True) if dest and en[dest].h1 else ''})
result={'mapping':mapping,'rows':rows,'exceptions':exceptions}
out=D/(sys.argv[1] if len(sys.argv)>1 else 'inventory_before.json');assert not out.exists();out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'en_pages':len(en),'paired':len(mapping),'links_to_convert':sum(bool(r['target_en']) for r in rows),'untranslated_prose_to_unwrap':sum(not r['target_en'] and r['prose'] for r in rows),'pages':len({r['source'] for r in rows}),'labels':dict(collections.Counter(r['label'] for r in rows))},ensure_ascii=False,indent=2))
