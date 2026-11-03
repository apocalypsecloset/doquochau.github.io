"""Verify full source parity, routing and bilingual safety for translation batches."""
import sys,json,re,csv,hashlib,posixpath,subprocess
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from en_translate import VI,source,faq_pairs
configs=json.loads((ROOT/'data/en-translations'/((sys.argv[1] if len(sys.argv)>1 else 'batch02')+'.json')).read_text())
errors=[];results=[]
def check(ok,message):
 if not ok:errors.append(message)
for c in configs:
 slug=c['en_slug'];s=BeautifulSoup((ROOT/'en/blog'/f'{slug}.html').read_text(),'html.parser');a=s.article
 raw,original,parts,texts=source(c['vi_slug']);orig=parts[3]
 check(hashlib.sha256(raw.encode()).hexdigest()==c['source_sha256'],slug+': source hash')
 url='https://apocalypsecloset.com/en/blog/'+slug+'.html'
 check(s.html['lang']=='en',slug+': lang')
 check(len(s.select('h1'))==1,slug+': H1 count')
 check(s.select_one('link[rel=canonical]')['href']==url,slug+': canonical')
 check(s.title.get_text()==c['title']+' | Apocalypse Closet',slug+': title')
 check(s.select_one('meta[name=description]')['content']==c['description'],slug+': meta')
 for lang,href in [('en',url),('vi','https://apocalypsecloset.com/blog/'+c['vi_slug']+'.html')]:
  check(bool(s.select_one(f'link[rel=alternate][hreflang={lang}][href="{href}"]')),slug+': hreflang '+lang)
 check(len(a.select('p'))==len(orig.select('p'))+len(parts[1].select('p'))+2,slug+': paragraph parity')
 check(len(a.select('li'))==len(orig.select('li')),slug+': list item parity')
 check(len(a.select('blockquote'))==len(orig.select('blockquote')),slug+': blockquote parity')
 for tag in ['h2','h3','table','tr','th','td','details','figcaption']:
  check(len(a.select(tag))==len(orig.select(tag)),f'{slug}: {tag} parity {len(a.select(tag))}/{len(orig.select(tag))}')
 check([i['src'] for i in a.select('img')]==[i['src'] for p in parts[:3] for i in p.select('img')]+[i['src'] for i in orig.select('img')],slug+': images and order')
 check(not VI.search(re.sub(r"caf[ée]s?|décor|l[’']or[ée]al",'',a.get_text(),flags=re.I)),slug+': Vietnamese text remains')
 check(all(i.get('alt') and not VI.search(i['alt']) for i in a.select('img')),slug+': image alt')
 check(not any(VI.search(n.get(attr,'')) for n in a.find_all() for attr in ['title','aria-label']),slug+': Vietnamese attributes')
 ids=[n['id'] for n in s.select('[id]')];check(len(ids)==len(set(ids)),slug+': duplicate IDs')
 for l in s.select('a[href]')+s.select('link[rel=stylesheet]'):
  h=l['href'];u=urlsplit(h)
  if u.scheme and u.netloc!='apocalypsecloset.com':continue
  if h.startswith('#'):check(u.fragment in ids,slug+': broken anchor '+h);continue
  path=u.path
  if path and path!='/':
   f=ROOT/path.lstrip('/');check(f.is_file(),slug+': missing local target '+path)
   if u.fragment and f.is_file() and f.suffix=='.html':
    target=BeautifulSoup(f.read_text(),'html.parser');check(bool(target.find(id=u.fragment)),slug+': target fragment '+h)
 for j in s.select('script[type="application/ld+json"]'):
  data=json.loads(j.string);graph=data.get('@graph',[data]);bp=next((n for n in graph if n['@type']=='BlogPosting'),None)
  check(bp is not None and bp['inLanguage']=='en' and bp['mainEntityOfPage']['@id']==url,slug+': schema')
  faq=next((n for n in graph if n['@type']=='FAQPage'),None)
  if faq_pairs(orig):
   expected=[{'@type':'Question','name':q.get_text(' ',strip=True),'acceptedAnswer':{'@type':'Answer','text':ans.get_text(' ',strip=True)}} for q,ans in faq_pairs(a)]
   check(faq and faq['mainEntity']==expected and len(expected)==len(faq_pairs(orig)),slug+': FAQ schema parity')
 external=lambda x:sorted(l['href'] for l in x.select('a[href]') if urlsplit(l['href']).scheme and urlsplit(l['href']).netloc!='apocalypsecloset.com')
 check(external(a)==external(orig),slug+': external references')
 results.append({'vi_slug':c['vi_slug'],'en_slug':slug,'source_text_segments':len(texts),'en_words':len(a.get_text(' ',strip=True).split()),'headings':len(orig.select('h2,h3')),'images':len(a.select('img')),'tables':len(a.select('table')),'faqs':len(faq_pairs(a))})
# Migration safety checks across all 216 source URLs, not only the translated ten.
import xml.etree.ElementTree as ET
rows=list(csv.DictReader((ROOT/'data/en-216-keyword-intent-audit.csv').open()))
check(len(rows)==216,'Inventory must contain 216 URLs')
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
check(len(urls)==len(set(urls)),'Duplicate sitemap URLs')
check(len([u for u in urls if '/blog/' in u and '/en/' not in u])==216,'Original VI sitemap count')
journal=BeautifulSoup((ROOT/'en/blog.html').read_text(),'html.parser')
for c in configs:
 vi='https://apocalypsecloset.com/blog/'+c['vi_slug']+'.html';en='https://apocalypsecloset.com/en/blog/'+c['en_slug']+'.html'
 v=BeautifulSoup((ROOT/'blog'/f"{c['vi_slug']}.html").read_text(),'html.parser')
 check(bool(v.select_one(f'link[rel=alternate][hreflang=en][href="{en}"]')),c['vi_slug']+': VI reciprocal hreflang')
 check(v.select_one('link[rel=canonical]')['href']==vi,c['vi_slug']+': VI canonical')
 check(en in urls and vi in urls,c['vi_slug']+': sitemap pair')
 check(bool(journal.select_one(f'a[href="/en/blog/{c["en_slug"]}.html"]')),c['en_slug']+': journal discovery')
print(json.dumps({'results':results,'errors':errors},indent=2));sys.exit(bool(errors))
