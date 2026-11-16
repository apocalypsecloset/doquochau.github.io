"""Verify the authorized UI changes without relaxing SEO or article preservation."""
import hashlib,json,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
from storefront_ux_release import BASE,MANIFEST
ROOT=Path(__file__).resolve().parents[1];errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
manifest=json.loads(MANIFEST.read_text())
check(set(manifest)=={'index.html','en/blog.html'},'Only authorized hubs in UI manifest')
for path,row in manifest.items():
 raw=(ROOT/path).read_text();old=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True)
 check(hashlib.sha256(raw.encode()).hexdigest()==row['after'],path+': UI release hash')
 check(hashlib.sha256(old.encode()).hexdigest()==row['before'],path+': UI baseline hash')
 s=BeautifulSoup(raw,'html.parser');o=BeautifulSoup(old,'html.parser')
 for sel,attr in [('title',None),('h1',None),('link[rel=canonical]','href'),('meta[name=description]','content'),('meta[name=robots]','content'),('link[hreflang]','href')]:
  values=lambda doc:[n.get(attr) if attr else n.get_text(' ',strip=True) for n in doc.select(sel)]
  check(values(s)==values(o),path+': immutable SEO '+sel)
 check(not any(n.get('src','').startswith('http:') for n in s.select('script[src]')),path+': insecure script')
 if path=='en/blog.html':
  cards=lambda soup:[str(n) for n in soup.select('#latest .cards a.card')]
  check(cards(s)==cards(o),'Journal original 438 cards and order unchanged')
  check(len(s.select('.journal-topics button'))==5,'Five Journal filters')
 else:
  check(len(s.select('#ac-product-grid .ac-static-product'))==2,'Two real static products')
  check(len(s.select('#style-the-drop .ac-guide-card'))==3,'Three relevant style guides')
  check(all(n.get('href')=='#size-guide' for n in s.select('[data-size-guide]')),'Size links resolve to guide')
  check(len(s.select('#size-guide [data-measurements=cm] tbody tr'))==7,'Seven cm sizes')
  check(len(s.select('#size-guide [data-measurements=in] tbody tr'))==7,'Seven inch sizes')
  check('LAYOUT PREVIEW' not in raw,'No demo inventory')
  for n in s.select('#style-the-drop a[href]'):
   check((ROOT/n['href'].split('#')[0].lstrip('/')).is_file(),'Style guide target exists: '+n['href'])
# No article edits can hide behind the hub-only history normalization.
changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=ROOT,text=True).splitlines()
from blog_repair_release import original as blog_original
for p in changed:
 if p.startswith(('blog/','en/blog/')):
  current=(ROOT/p).read_text();expected=subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT,text=True)
  check(blog_original(p,current)==expected,p+': article changed beyond reviewed bilingual repairs')
print(json.dumps({'ui_pages':len(manifest),'errors':errors},indent=2));sys.exit(bool(errors))
