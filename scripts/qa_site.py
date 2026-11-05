"""Static release checks; image routes hosted outside Git are intentionally excluded."""
import csv,json,re,subprocess,sys,xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import unquote,urljoin,urlsplit
from bs4 import BeautifulSoup
from translation_inventory import rows
ROOT=Path(__file__).resolve().parents[1];BASE='https://apocalypsecloset.com';errors=[]
def check(ok,message):
 if not ok:errors.append(message)
pages={p.relative_to(ROOT).as_posix():BeautifulSoup(p.read_text(),'html.parser') for p in ROOT.rglob('*.html') if '.git' not in p.parts and 'node_modules' not in p.parts}
ids={p:{n['id'] for n in s.select('[id]')} for p,s in pages.items()}
def target(url,page):
 u=urlsplit(urljoin(BASE+'/'+page,url))
 if u.netloc not in ['apocalypsecloset.com','www.apocalypsecloset.com']:return None
 p=unquote(u.path).lstrip('/')
 if not p or p.endswith('/'):p+='index.html'
 return p,unquote(u.fragment)
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
check(len(urls)==len(set(urls)),'Duplicate sitemap URL')
titles=[];descriptions=[]
for url in urls:
 p,_=target(url,'index.html');check(p in pages,'Missing sitemap page '+url)
 if p not in pages:continue
 s=pages[p];can=s.select('link[rel=canonical]');title=s.select('title');description=s.select('meta[name=description]')
 check(len(s.select('h1'))==1,p+': H1 count');check(len(can)==1 and can[0].get('href')==url,p+': canonical')
 check(len(title)==1 and bool(title[0].get_text(strip=True)),p+': title');check(len(description)==1 and bool(description[0].get('content')),p+': description')
 check(not any('noindex' in m.get('content','').lower() for m in s.select('meta[name=robots]')),p+': sitemap meta noindex')
 if title:titles.append(title[0].get_text())
 if description:descriptions.append(description[0].get('content'))
check(len(titles)==len(set(titles)),'Duplicate sitemap titles');check(len(descriptions)==len(set(descriptions)),'Duplicate sitemap descriptions')
for p,s in pages.items():
 allids=[n['id'] for n in s.select('[id]')];check(len(allids)==len(set(allids)),p+': duplicate ID')
 for n in s.select('a[href],link[rel=stylesheet],script[src]'):
  h=n.get('href',n.get('src',''));t=target(h,p)
  if not t or h.startswith(('mailto:','tel:','javascript:','data:')):continue
  dest,fragment=t
  check((ROOT/dest).is_file(),p+': missing HTML/CSS/JS target '+h)
  if fragment and dest in ids:check(fragment in ids[dest],p+': missing fragment '+h)
 for script in s.select('script[type="application/ld+json"]'):
  try:json.loads(script.get_text())
  except Exception:errors.append(p+': JSON-LD parse error')
 if p.startswith('en/') and p!='en/index.html':
  check(bool(s.select('script[src*="analytics-enhancements.min.js"]')),p+': missing GA4 loader')
 for alternate in s.select('link[hreflang]'):
  t=target(alternate.get('href',''),p)
  if not t:continue
  dest,_=t;check(dest in pages,p+': missing hreflang target')
  if dest not in pages:continue
  lang=s.html.get('lang') if s.html else None;canonical=s.select_one('link[rel=canonical]')
  if lang and canonical:check(any(a.get('href')==canonical['href'] and a.get('hreflang')==lang for a in pages[dest].select('link[hreflang]')),p+': nonreciprocal hreflang')
for row in rows():
 en,_=target(row['en_url'],'index.html');vi,_=target(row['vi_url'],'index.html')
 check(en in pages and vi in pages,'Missing bilingual pair '+row['vi_url'])
 check(row['en_url'] in urls and row['vi_url'] in urls,'Bilingual sitemap pair '+row['vi_url'])
check(len(rows())==218,'Expected original 216 plus two explicit extensions')
check(len(list(csv.DictReader((ROOT/'data/en-216-keyword-intent-audit.csv').open())))==216,'Original inventory altered')
headers=(ROOT/'_headers').read_text();block=''
for line in headers.splitlines():
 if not line.strip() or line.lstrip().startswith('#'):continue
 if not line[0].isspace():block=line.strip()
 elif 'noindex' in line.lower():check('.pages.dev/' in block,'Production-wide noindex header')
check('https://:project.pages.dev/*' in headers and 'https://:version.:project.pages.dev/*' in headers,'Preview noindex protection')
journal=pages['en/blog.html'];cards=journal.select('#latest .cards a.card')
check(len(cards)==220 and len({a['href'] for a in cards})==220,'English Journal count/duplicates')
check([int(a.select_one('.eyebrow').get_text().split('/')[0]) for a in cards]==list(range(1,221)),'English Journal order')
# Keep this check scoped to immutable SEO fields of existing pages. Content maintenance is checked separately.
baseline='a43f1b532bc7939f91fd4ef32472acf7215f1cd6'
result=subprocess.run(['git','cat-file','-e',baseline],cwd=ROOT,capture_output=True)
preserved=0
if result.returncode==0:
 names=subprocess.check_output(['git','ls-tree','-r','--name-only',baseline],cwd=ROOT,text=True).splitlines()
 for p in names:
  if not p.endswith('.html') or p not in pages:continue
  old=BeautifulSoup(subprocess.check_output(['git','show',baseline+':'+p],cwd=ROOT,text=True),'html.parser');new=pages[p]
  for selector,attr in [('title',None),('meta[name=description]','content'),('link[rel=canonical]','href')]:
   before=[n.get(attr) if attr else n.get_text() for n in old.select(selector)];after=[n.get(attr) if attr else n.get_text() for n in new.select(selector)]
   check(before==after,p+': changed original '+selector)
  check([n.get_text(' ',strip=True) for n in old.select('h1')]==[n.get_text(' ',strip=True) for n in new.select('h1')],p+': changed H1')
  preserved+=1
else:errors.append('Missing immutable audit baseline for preservation check')
report=dict(html_pages=len(pages),sitemap_urls=len(urls),bilingual_pairs=len(rows()),english_journal_cards=len(cards),existing_page_metadata_preserved=preserved,errors=errors)
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
