"""Release gate for complete translated collection hubs and their bilingual routes."""
import json,csv,re,sys,hashlib,subprocess,posixpath
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from en_translate_hubs import ROOT,source,VI
import xml.etree.ElementTree as ET
configs=json.loads((ROOT/'data/en-translations'/(sys.argv[1]+'.json')).read_text());errors=[];results=[]
def check(ok,msg):
 if not ok:errors.append(msg)
external=lambda root:sorted(a['href'] for a in root.select('a[href]') if urlsplit(a['href']).scheme and urlsplit(a['href']).netloc!='apocalypsecloset.com')
for c in configs:
 slug=c['en_slug'];raw,vi,orig,texts=source(c['vi_slug']);s=BeautifulSoup((ROOT/'en/blog'/f'{slug}.html').read_text(),'html.parser');a=s.main
 url='https://apocalypsecloset.com/en/blog/'+slug+'.html';viurl='https://apocalypsecloset.com/blog/'+c['vi_slug']+'.html'
 check(hashlib.sha256(raw.encode()).hexdigest()==c['source_sha256'],slug+': source hash')
 check(s.html['lang']=='en' and len(s.select('h1'))==1,slug+': language/H1')
 check(s.title.get_text()==c['title']+' | Apocalypse Closet',slug+': title')
 check(s.select_one('meta[name=description]')['content']==c['description'],slug+': meta')
 for k in ['og:description','twitter:description']:check(s.select_one('meta[property="'+k+'"],meta[name="'+k+'"]')['content']==c['description'],slug+': '+k)
 check(s.select_one('link[rel=canonical]')['href']==url,slug+': self canonical')
 check(not s.select('meta[name=robots][content*=noindex]'),slug+': indexability')
 for lang,href in [('en',url),('vi',viurl)]:check(bool(s.select_one(f'link[rel=alternate][hreflang={lang}][href="{href}"]')),slug+': alternate '+lang)
 for tag in ['p','h1','h2','h3','li','table','tr','td','th','figure','figcaption','details','summary']:
  check(len(a.select(tag))==len(orig.select(tag))+(1 if tag=='p' else 0),slug+': '+tag+' parity')
 check(len(a.select('.hub-card'))==len(orig.select('.hub-card')),slug+': card parity')
 for attr in ['src','srcset','sizes','width','height']:
  check([i.get(attr) for i in a.select('img')]==[i.get(attr) for i in orig.select('img')],slug+': original images '+attr)
 clean=lambda t:re.sub(r'caf[ée]s?|décor','',t,flags=re.I)
 check(not VI.search(clean(a.get_text())),slug+': Vietnamese body')
 check(all(i.get('alt') and not VI.search(clean(i['alt'])) for i in a.select('img')),slug+': alt')
 check(not any(VI.search(clean(n.get(attr,''))) for n in a.find_all() for attr in ['title','aria-label']),slug+': translated attributes')
 check(external(a)==external(orig),slug+': original external sources')
 ids=[n['id'] for n in s.select('[id]')];check(len(ids)==len(set(ids)),slug+': unique IDs')
 for l in s.select('a[href],link[rel=stylesheet]'):
  h=l['href'];u=urlsplit(h)
  if u.scheme and u.netloc!='apocalypsecloset.com':continue
  if h.startswith('#'):check(u.fragment in ids,slug+': fragment '+h);continue
  p=u.path
  if p and p!='/':
   f=ROOT/p.lstrip('/');check(f.is_file(),slug+': missing path '+h)
   if u.fragment and f.is_file() and f.suffix=='.html':check(bool(BeautifulSoup(f.read_text(),'html.parser').find(id=u.fragment)),slug+': target anchor '+h)
 graph=json.loads(s.select_one('script[type="application/ld+json"]').string)['@graph'];collection=next(n for n in graph if n['@type']=='CollectionPage');items=collection['mainEntity']['itemListElement'];cards=a.select('a.hub-card[href]')
 check(collection['url']==url and collection['inLanguage']=='en',slug+': collection schema')
 check(collection['mainEntity']['numberOfItems']==len(cards)==len(items),slug+': ItemList count')
 check([(i['position'],i['name'],i['url']) for i in items]==[(i+1,x.h3.get_text(' ',strip=True),'https://apocalypsecloset.com'+x['href']) for i,x in enumerate(cards)],slug+': schema/visible card parity')
 check(not any(n['@type'] in ['BlogPosting','FAQPage'] for n in graph),slug+': correct collection type')
 current=(ROOT/'blog'/f"{c['vi_slug']}.html").read_text();v=BeautifulSoup(current,'html.parser')
 check(v.select_one('link[rel=canonical]')['href']==viurl,slug+': VI self canonical')
 for lang,href in [('en',url),('vi',viurl)]:check(bool(v.select_one(f'link[rel=alternate][hreflang={lang}][href="{href}"]')),slug+': reciprocal '+lang)
 baseline=subprocess.check_output(['git','show','HEAD:blog/'+c['vi_slug']+'.html'],cwd=ROOT).decode()
 baseline=re.sub(r'<!-- AC-EN-BATCH24-START -->.*?<!-- AC-EN-BATCH24-END -->','',baseline,flags=re.S)
 check(re.sub(r'<!-- AC-EN-BATCH24-START -->.*?<!-- AC-EN-BATCH24-END -->','',current,flags=re.S)==baseline,slug+': byte-exact VI preservation')
 results.append(dict(vi_slug=c['vi_slug'],en_slug=slug,source_segments=len(texts),en_words=len(a.get_text(' ',strip=True).split()),cards=len(cards),images=len(a.select('img')),headings=len(a.select('h2,h3'))))
rows=list(csv.DictReader((ROOT/'data/en-216-keyword-intent-audit.csv').open()));check(len(rows)==216,'216 source rows')
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')];check(len(urls)==len(set(urls)),'sitemap duplicates');check(len([u for u in urls if '/blog/' in u and '/en/' not in u])==216,'216 VI sitemap URLs')
journal=(ROOT/'en/blog.html').read_text()
index=BeautifulSoup(journal,'html.parser');cards=index.select('a.card');grid_cards=index.select('#latest .cards a.card')
check(len(cards)==len(grid_cards),'Journal cards must all be in the reading grid')
check(len({a['href'] for a in cards})==len(cards),'Duplicate Journal cards')
check([int(a.select_one('.eyebrow').get_text().split('/')[0]) for a in grid_cards]==list(range(1,len(cards)+1)),'Journal card sequence')
for c in configs:
 check('https://apocalypsecloset.com/en/blog/'+c['en_slug']+'.html' in urls,c['en_slug']+': sitemap')
 check('/en/blog/'+c['en_slug']+'.html' in journal,c['en_slug']+': Journal')
print(json.dumps(dict(results=results,errors=errors),indent=2));sys.exit(bool(errors))
