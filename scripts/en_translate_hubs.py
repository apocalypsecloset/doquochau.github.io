"""Complete, hash-locked English collection hubs; no article-only extraction."""
from pathlib import Path
from bs4 import BeautifulSoup,Comment
from urllib.parse import urlsplit
import csv,json,hashlib,re,posixpath,sys
from en_translate import ROOT,VI

def source(slug):
 raw=(ROOT/'blog'/f'{slug}.html').read_text()
 raw=re.sub(r'<!-- AC-EN-BATCH[0-9]{2}-START -->.*?<!-- AC-EN-BATCH[0-9]{2}-END -->','',raw,flags=re.S)
 s=BeautifulSoup(raw,'html.parser');main=s.main;assert main and main.h1
 texts=[]
 for n in main.descendants:
  if isinstance(n,str) and not isinstance(n,Comment) and n.strip() and n.strip() not in texts:texts.append(n.strip())
 for n in [main]+list(main.find_all()):
  for attr in ['alt','title','aria-label']:
   t=n.get(attr,'').strip()
   if t and t not in texts:texts.append(t)
 return raw,s,main,texts

def memory():
 mem={}
 for p in sorted((ROOT/'data/en-translations').glob('*.tsv')):
  try:
   from en_translate import source as article_source
   _,_,_,texts=article_source(p.stem)
  except AssertionError:
   try:_,_,_,texts=source(p.stem)
   except (AssertionError,FileNotFoundError):continue
  for line in p.read_text().splitlines():
   if not line:continue
   k,v=line.split('\t',1);k=int(k)
   if k<len(texts):mem.setdefault(texts[k],set()).add(v)
 return {k:next(iter(v)) for k,v in mem.items() if len(v)==1}

def generate(c):
 raw,original,main,texts=source(c['vi_slug']);assert hashlib.sha256(raw.encode()).hexdigest()==c['source_sha256']
 entries={int(k):v for k,v in (line.split('\t',1) for line in (ROOT/'data/en-translations'/f"{c['vi_slug']}.tsv").read_text().splitlines() if line)}
 missing=[(i,t) for i,t in enumerate(texts) if VI.search(t) and i not in entries];assert not missing,missing
 tr={t:entries.get(i,t) for i,t in enumerate(texts)}
 for n in list(main.descendants):
  if isinstance(n,str) and not isinstance(n,Comment) and n.strip():n.replace_with((' ' if n[:1].isspace() else '')+tr[n.strip()]+(' ' if n[-1:].isspace() else ''))
 for n in [main]+list(main.find_all()):
  for attr in ['alt','title','aria-label']:
   if n.get(attr,'').strip():n[attr]=tr[n[attr].strip()]
 mapping={urlsplit(r['vi_url']).path:urlsplit(r['en_url']).path for r in csv.DictReader((ROOT/'data/en-216-keyword-intent-audit.csv').open()) if r['en_url']}
 for p in (ROOT/'data/en-translations').glob('batch*.json'):
  for x in json.loads(p.read_text()):mapping['/blog/'+x['vi_slug']+'.html']='/en/blog/'+x['en_slug']+'.html'
 for a in main.select('a[href]'):
  h=a['href'];u=urlsplit(h)
  if h.startswith('#') or u.scheme and u.netloc!='apocalypsecloset.com':continue
  path=posixpath.normpath(posixpath.join('/blog/',u.path)) if not u.path.startswith('/') else u.path
  if path=='/blog.html':path='/en/blog.html'
  path=mapping.get(path,path);a['href']=path+('?' + u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
  if path.startswith('/en/'):a['hreflang']='en'
  elif path!='/':a['lang']='vi';a['hreflang']='vi';a['title']='Vietnamese reference';a.append(' (Vietnamese)')
 template=BeautifulSoup((ROOT/'en/blog/soft-goth-style-outfits.html').read_text(),'html.parser')
 url='https://apocalypsecloset.com/en/blog/'+c['en_slug']+'.html';vi='https://apocalypsecloset.com/blog/'+c['vi_slug']+'.html'
 template.title.string=c['title']+' | Apocalypse Closet'
 for m in template.select('meta'):
  key=m.get('name',m.get('property',''))
  if key in ['description','og:description','twitter:description']:m['content']=c['description']
  elif key in ['og:title','twitter:title']:m['content']=c['title']
  elif key=='og:url':m['content']=url
  elif key=='og:type':m['content']='website'
  elif key in ['og:image','twitter:image']:m['content']=original.select_one('meta[property="og:image"]')['content']
 template.select_one('link[rel=canonical]')['href']=url
 for l in template.select('link[rel=alternate]'):l.decompose()
 for lang,href in [('en',url),('vi',vi)]:template.head.append(template.new_tag('link',rel='alternate',hreflang=lang,href=href))
 for j in template.select('script[type="application/ld+json"]'):j.decompose()
 # Preserve the full collection DOM, cards, images, source links and extra galleries.
 target=template.main;target.replace_with(main);main['data-source-sha256']=c['source_sha256'];main['class']=['en-hub'];main['id']='main-content'
 template.select_one('.skip')['href']='#main-content'
 for n in main.select('.hub-card img,figure img'):n['style']='max-width:100%;height:auto'
 switch=template.new_tag('p',attrs={'class':'hub-locale'});a=template.new_tag('a',href=vi,lang='vi',hreflang='vi');a.string='Read the Vietnamese original';switch.append(a);main.insert(0,switch)
 for t in main.select('table'):t.wrap(template.new_tag('div',attrs={'class':'article-table-scroll'}))
 cards=main.select('a.hub-card[href]')
 items=[{'@type':'ListItem','position':i+1,'name':a.h3.get_text(' ',strip=True),'url':'https://apocalypsecloset.com'+a['href']} for i,a in enumerate(cards) if a.h3]
 graph=[{'@type':'CollectionPage','@id':url,'url':url,'name':c['title'],'description':c['description'],'inLanguage':'en','isBasedOn':{'@id':vi},'dateModified':'2026-11-03','mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':items}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':u} for i,(name,u) in enumerate([('Shop','https://apocalypsecloset.com/'),('Journal','https://apocalypsecloset.com/en/blog.html'),(c['title'],url)])]}]
 j=template.new_tag('script',type='application/ld+json');j.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False);template.head.append(j)
 template.head.append(template.new_tag('link',rel='stylesheet',href='/assets/css/en-hubs.css?v=20261103'))
 out=ROOT/'en/blog'/f"{c['en_slug']}.html";out.write_text(str(template)+'\n');return out

if __name__=='__main__':
 if sys.argv[1]=='extract':
  mem=memory()
  for slug in sys.argv[2:]:
   raw,_,_,texts=source(slug);p=ROOT/'data/en-translations'/f'{slug}.tsv'
   if not p.exists():p.write_text(''.join(f'{i}\t{mem[t]}\n' for i,t in enumerate(texts) if t in mem))
   done={int(l.split('\t',1)[0]) for l in p.read_text().splitlines() if l}
   print('SOURCE',slug,'SHA256',hashlib.sha256(raw.encode()).hexdigest())
   for i,t in enumerate(texts):
    if i not in done:print(f'{i}\t{t}')
 elif sys.argv[1]=='generate':
  for c in json.loads((ROOT/'data/en-translations'/(sys.argv[2]+'.json')).read_text()):print(generate(c).relative_to(ROOT))
