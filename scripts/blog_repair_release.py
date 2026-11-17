"""Deterministic, bounded bilingual blog repairs and exact historical successors."""
import hashlib,html,json,re,subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin,urlsplit,urlunsplit
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
BASE='7465236e399e127d785f6579cc839c10d2f74ecc'
D=ROOT/'docs/blog-repair-2026-11-17'
CSS='/assets/css/blog-reading-en.css?v=20261117'
CACHE={}
def digest(raw):return hashlib.sha256(raw.encode()).hexdigest()
def mapping():
 if 'mapping' not in CACHE:
  from translation_inventory import catalog_urls
  CACHE['mapping']={}
  for url in catalog_urls('vi'):
   s=BeautifulSoup((ROOT/urlsplit(url).path.lstrip('/')).read_text(),'html.parser')
   alt=s.select_one('link[hreflang=en]')
   if alt:CACHE['mapping'][urlsplit(url).path]=urlsplit(alt['href']).path
 return CACHE['mapping']
def repair(path,raw):
 if not path.startswith(('blog/','en/blog/')):return raw,{}
 s=BeautifulSoup(raw,'html.parser');changes={};en=path.startswith('en/')
 if en:
  mapp=mapping();count=0
  def anchor(m):
   nonlocal count
   a=BeautifulSoup(m[0],'html.parser').a;href=a.get('href','');u=urlsplit(urljoin('https://apocalypsecloset.com/'+path,href))
   if u.netloc!='apocalypsecloset.com' or u.path not in mapp:return m[0]
   if a.get('lang')=='vi' or a.get_text(' ',strip=True)=='Read the Vietnamese original' or mapp[u.path]=='/'+path:return m[0]
   # Only article content, never navigation or explicitly marked language switches.
   article=s.article or s.main
   if not any(x.get('href')==href and x.get_text(' ',strip=True)==a.get_text(' ',strip=True) for x in article.select('a[href]')):return m[0]
   target=mapp[u.path]
   if u.fragment:
    dest=BeautifulSoup((ROOT/target.lstrip('/')).read_text(),'html.parser')
    assert dest.find(id=u.fragment),(path,href)
   opening,rest=m[0].split('>',1)
   new=urlunsplit(('', '',target,u.query,u.fragment))
   opening=re.sub(r'(\bhref\s*=\s*)(["\x27]).*?\2',lambda n:n[1]+n[2]+html.escape(new,quote=True)+n[2],opening,flags=re.S)
   opening=re.sub(r'\s+title\s*=\s*(["\x27])Vietnamese reference\1','',opening)
   if re.search(r'\bhreflang\s*=',opening):opening=re.sub(r'(\bhreflang\s*=\s*)(["\x27]).*?\2',lambda n:n[1]+n[2]+'en'+n[2],opening)
   else:opening+=' hreflang="en"'
   count+=1;return opening+'>'+rest
  raw=re.sub(r'<a\b[^>]*>.*?</a\s*>',anchor,raw,flags=re.S|re.I)
  if count:changes['links']=count
 # Remove redundant generic caption instances. Retain the first and all unique/link captions.
 seen=set();removed=[]
 def caption(m):
  cap=BeautifulSoup(m[0],'html.parser').figcaption;text=cap.get_text(' ',strip=True)
  if text in seen and not cap.select('a,[id]') and not cap.get('id'):
   removed.append(text);return ''
  seen.add(text);return m[0]
 raw=re.sub(r'<figcaption\b[^>]*>.*?</figcaption\s*>',caption,raw,flags=re.S|re.I)
 if removed:changes['captions_removed']=len(removed)
 if path in ['blog/capsule-wardrobe-la-gi.html','en/blog/what-is-a-capsule-wardrobe.html']:
  # Retain the in-flow FAQ and its illustration, remove the duplicate accordion.
  raw,n=re.subn(r'<section\b[^>]*class="seo-faq"[^>]*>.*?</section>','',raw,flags=re.S);assert n==1
  start=raw.index('<h2 id="faq-nhanh-ve-capsule-wardrobe">');end=raw.index('<h2 id="outfit-trong-closet-lien-quan">',start)
  raw=raw[:start]+'<section id="faq-title" class="seo-faq" aria-labelledby="faq-nhanh-ve-capsule-wardrobe">'+raw[start:end]+'</section>'+raw[end:]
  changes['faq_consolidated']=True
 if en and s.select_one('.ac-blog-app-box'):
  # Preserve the functional link and tracking marker, move it below the article title.
  match=re.search(r'<a\b[^>]*class="ac-blog-app-box"[^>]*>.*?</a>',raw,re.S);assert match,path
  banner=match[0];raw=raw[:match.start()]+raw[match.end():]
  raw,n=re.subn(r'(<h1\b[^>]*>.*?</h1>)',lambda m:m[0]+'\n'+banner,raw,count=1,flags=re.S);assert n==1
  raw=raw.replace('</head>',f'<link rel="stylesheet" href="{CSS}">\n</head>',1)
  changes['compact_en_app_cta']=True
 return raw,changes

def original(path,raw):
 from en_link_fix_release import english_previous
 raw=english_previous(path,raw)
 manifest=D/'reviewed-html.json'
 if not manifest.exists():return raw
 if 'review' not in CACHE:CACHE['review']=json.loads(manifest.read_text())
 row=CACHE['review'].get(path)
 if not row or digest(raw)!=row['after']:return raw
 key='base:'+path
 if key not in CACHE:CACHE[key]=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True)
 assert digest(CACHE[key])==row['before'],path
 return CACHE[key]
if __name__=='__main__':
 existing=D/'reviewed-html.json'
 if existing.exists():
  reviewed=json.loads(existing.read_text())
  assert all(digest((ROOT/path).read_text())==row['after'] for path,row in reviewed.items()),'Release changed; inspect and QA before replaying'
  print(json.dumps({'already_applied':True,'pages':len(reviewed)}));raise SystemExit(0)
 manifest={};counts=Counter()
 for p in sorted(list((ROOT/'blog').glob('*.html'))+list((ROOT/'en/blog').glob('*.html'))):
  path=p.relative_to(ROOT).as_posix();raw=p.read_text();after,changes=repair(path,raw)
  if raw!=after:
   manifest[path]={'before':digest(raw),'after':digest(after),'changes':changes};p.write_text(after);counts.update(changes)
 (D/'reviewed-html.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'pages':len(manifest),'changes':dict(counts)},indent=2))
