"""Check actual published pages, every authorized edit and unknown successor rejection."""
import json,re,subprocess,sys
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from bs4 import BeautifulSoup
from blog_repair_release import ROOT,BASE,D,CSS,digest,repair,original,mapping
from translation_inventory import catalog_urls
from fix_schema_consistency import faq_pairs
errors=[];counts=Counter();manifest=json.loads((D/'reviewed-html.json').read_text())
def check(ok,msg):
 if not ok:errors.append(msg)
for path,row in manifest.items():
 raw=(ROOT/path).read_text();old=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True);s=BeautifulSoup(raw,'html.parser');o=BeautifulSoup(old,'html.parser')
 check(digest(old)==row['before'] and digest(raw)==row['after'],path+': exact release hashes')
 expected,changes=repair(path,old)
 check(raw==expected and changes==row['changes'],path+': only deterministic scoped edits')
 check(original(path,raw)==old,path+': historical predecessor')
 check(original(path,raw+' ')==raw+' ',path+': unknown edits must fail historical hashes')
 for sel in ['title','h1','meta','link[rel=canonical]','link[hreflang]','img','script']:
  check([str(n) for n in s.select(sel)]==[str(n) for n in o.select(sel)],path+': preserved '+sel)
 check(s.html.attrs==o.html.attrs,path+': HTML language')
 check([str(n) for n in s.select('a[lang=vi]')]==[str(n) for n in o.select('a[lang=vi]')],path+': original-language switches preserved')
 counts.update(changes)
for url in sorted(catalog_urls('vi')|catalog_urls('en')):
 path=urlsplit(url).path.lstrip('/');s=BeautifulSoup((ROOT/path).read_text(),'html.parser');main=s.main or s.article;en=path.startswith('en/')
 counts['published_pages']+=1
 caps=[n.get_text(' ',strip=True) for n in main.select('figcaption') if not n.select('a')]
 check(len(caps)==len(set(caps)),path+': duplicate plain caption')
 if en:
  for a in (s.article or s.main).select('a[href]'):
   u=urlsplit(urljoin(url,a['href']))
   if u.netloc=='apocalypsecloset.com' and u.path in mapping() and a.get('lang')!='vi' and a.get_text(' ',strip=True)!='Read the Vietnamese original' and mapping()[u.path]!='/'+path:
    check(False,path+': VI link with EN counterpart '+a['href'])
  app=s.select_one('.ac-blog-app-box')
  if app:
   check(bool(s.select_one('link[href="'+CSS+'"]')),path+': compact app stylesheet')
   check(s.h1 in app.find_all_previous('h1'),path+': article title before app link')
 if 'capsule-wardrobe' in path:
  pairs=faq_pairs(s);check(len(pairs)==3,path+': single FAQ with 3 questions')
  for question,answer in pairs:
   check(sum(n.get_text(' ',strip=True)==question for n in main.select('h3,summary'))==1,path+': unique FAQ question')
   check(sum(n.get_text(' ',strip=True)==answer for n in main.select('p'))==1,path+': unique FAQ answer')
  nodes=[]
  for n in s.select('script[type="application/ld+json"]'):
   j=json.loads(n.get_text());nodes.extend(j.get('@graph',[j]))
  faqs=[n for n in nodes if n.get('@type')=='FAQPage']
  check(len(faqs)==1 and [(q['name'],q['acceptedAnswer']['text']) for q in faqs[0]['mainEntity']]==pairs,path+': exact FAQ schema parity')
check(counts['links']==571,'Expected 571 repaired links')
check(counts['faq_consolidated']==2,'Both FAQ languages')
check(counts['compact_en_app_cta']==232,'Expected 232 EN app links')
print(json.dumps({'pages_changed':len(manifest),'counts':dict(counts),'errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
