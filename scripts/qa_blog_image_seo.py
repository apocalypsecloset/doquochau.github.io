"""Verify current image fixes, actual variants and exact non-image preservation."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
from urllib.parse import urljoin,urlsplit
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import search_metadata_release as SEARCH_METADATA
from fix_blog_image_seo import ROOT,DATA,BASE,cover,content_images,getmeta,baseline

errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def sha(b):return hashlib.sha256(b).hexdigest()

def image_only_view(raw,path):
 s=BeautifulSoup(raw,'html.parser');cv=cover(s)
 if cv and cv.get('data-src'):
  raw=re.sub(r'<noscript>\s*<img\b[^>]*class="[^"]*apcl-standard-cover-image[^>]*>\s*</noscript>','',raw,count=1)
 raw=re.sub(r'  var cover=document\.querySelector\(\x27\.ac-deferred-cover\[data-src\]\x27\);[\s\S]*?  io\.observe\(cover\);\n','',raw,count=1)
 raw=re.sub(r'<img\b[^>]*class="journal-thumbnail"[^>]*>','',raw)
 raw=raw.replace('<link rel="stylesheet" href="/assets/css/blog-image-seo-20261118.css">\n','')
 def meta(m):
  n=BeautifulSoup(m.group(),'html.parser').meta;k=n.get('property',n.get('name',''))
  return '' if k in ['og:image','twitter:image'] or k.startswith(('og:image:','twitter:image:')) else m.group()
 raw=re.sub(r'<meta\b[^>]*>\n?',meta,raw)
 def img(m):
  n=BeautifulSoup(m.group(),'html.parser').find()
  for k in ['src','srcset','width','height','sizes','loading','fetchpriority','decoding','data-src'] if n.name=='img' else ['srcset']:
   n.attrs.pop(k,None)
  return str(n)
 raw=re.sub(r'<(?:img|source)\b[^>]*>',img,raw)
 bad=getmeta(s,'og:image')
 if bad.startswith('https://apocalypsecloset.comdata:'):
  real=urljoin(BASE+path,cv.get('data-src',cv.get('src')))
  raw=raw.replace(bad,real)
 def schema(m):
  text=m.group();opening=text[:text.index('>')+1];obj=json.loads(text[len(opening):text.rindex('</script>')])
  def walk(node):
   if isinstance(node,dict):
    return {k:walk(v) for k,v in node.items() if not (node.get('@type')=='ImageObject' and k in ['width','height'])}
   if isinstance(node,list):return [walk(v) for v in node]
   return node
  return opening+json.dumps(walk(obj),ensure_ascii=False,separators=(',',':'))+'</script>'
 raw=re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>',schema,raw)
 raw=re.sub(r'(?m)^([^\n]*<(?:img|source)\b[^\n]*?)[ \t]+$',r'\1',raw)
 return raw

def main():
 manifest=json.loads((DATA/'html-changes.json').read_text(encoding='utf8'))
 predecessors=baseline(list(manifest['files']),manifest['baseline'])
 assets=json.loads((DATA/'assets.json').read_text(encoding='utf8'));byorigin={r['origin']:r for r in assets};variants={urljoin(BASE,v['url']):v for a in assets for v in a['variants']}
 origin_for_variant={urljoin(BASE,v['url']):a['origin'] for a in assets for v in a['variants']}
 for a in assets:
  check(len({v['width'] for v in a['variants']})>=2,'Missing real width alternatives '+a['origin'])
  for v in a['variants']:
   check(v['bytes']<=(50 if v['width']<=320 else 160 if v['width']<=640 else 200)*1024,'Variant exceeds budget '+v['url'])
   if not v['origin']:
    file=ROOT/v['url'].lstrip('/');check(file.is_file(),'Missing variant '+v['url'])
    if file.exists():check(sha(file.read_bytes())==v['sha256'],'Variant hash changed '+v['url'])
    if file.exists():
     from PIL import Image
     with Image.open(file) as image:
      image.load();check(image.size==(v['width'],v['height']),'Decoded variant dimensions '+v['url'])
 print('Verified all generated asset hashes and decoded dimensions',file=sys.stderr,flush=True)
 urls=[];page_count=0;img_count=0;source_count=0
 for path,row in manifest['files'].items():
  raw=(ROOT/path).read_text(encoding='utf8');reviewed_image_raw=SEARCH_METADATA.predecessor(path,raw);check(sha(reviewed_image_raw.encode())==row['after'],'Unexpected successor '+path)
  old=predecessors[path];check(sha(old.encode())==row['before'],'Unexpected predecessor '+path)
  if not path.endswith('.html'):continue
  check(image_only_view(old,path)==image_only_view(reviewed_image_raw,path),'Non-image HTML/prose/navigation changed '+path)
  s=BeautifulSoup(raw,'html.parser');page_count+=1
  if page_count%100==0:print('Verified HTML preservation:',page_count,file=sys.stderr,flush=True)
  old_soup=BeautifulSoup(old,'html.parser')
  def identities(soup):
   result=[]
   for n in content_images(soup):
    if 'journal-thumbnail' in n.get('class',[]):continue
    u=urljoin(BASE+path,n.get('data-src',n.get('src','')))
    result.append((origin_for_variant.get(u,u),n.get('alt')))
   return result
  check(identities(old_soup)==identities(s),'Editorial image identity/order/alt changed '+path)
  if path not in ['blog.html','en/blog.html']:
   check(bool(getmeta(s,'og:image:alt')),path+': missing OG alt')
   for key in ['og:image','twitter:image']:
    value=getmeta(s,key);check(value.startswith(BASE) and 'data:' not in value,path+': malformed '+key)
   check(not s.select('.ac-deferred-cover[data-src]'),path+': deferred cover')
   cv=cover(s)
   if cv and getmeta(s,'og:type')=='article':
    check(cv.get('loading')=='eager' and cv.get('fetchpriority')=='high',path+': cover loading priority')
   for script in s.select('script[type="application/ld+json"]'):
    try:
     j=json.loads(script.get_text());check('comdata:' not in script.get_text(),path+': malformed schema image')
     def schema_dims(node):
      if isinstance(node,dict):
       a=byorigin.get(node.get('url','')) if node.get('@type')=='ImageObject' else None
       if a:
        for k in ['width','height']:
         if k in node:check(node[k]==a[k],path+': schema '+k+' differs from actual origin')
       for value in node.values():schema_dims(value)
      elif isinstance(node,list):
       for value in node:schema_dims(value)
     schema_dims(j)
    except ValueError:check(False,path+': invalid JSON-LD')
  for n in content_images(s):
   u=urljoin(BASE+path,n.get('src',''))
   if u.endswith('.svg'):continue
   img_count+=1;check(bool(n.get('alt')),path+': missing image alt')
   check(bool(n.get('width') and n.get('height')),path+': missing image dimensions')
   check(bool(n.get('sizes')),path+': missing sizes')
   entries=[x.strip().split() for x in n.get('srcset','').split(',') if x.strip()]
   check(len(entries)>=2,path+': missing responsive widths '+u)
   for entry in entries:
    check(len(entry)==2,path+': invalid srcset entry')
    if len(entry)!=2:continue
    v=variants.get(urljoin(BASE+path,entry[0]));check(v is not None,path+': unverified responsive candidate '+entry[0])
    if v:check(entry[1]==str(v['width'])+'w',path+': inaccurate width descriptor '+entry[0])
   check(u in variants,path+': unverified fallback '+u)
   original=byorigin.get(origin_for_variant.get(u,u))
   if original:
    check(n.get('width')==str(original['width']) and n.get('height')==str(original['height']),path+': inaccurate HTML aspect dimensions')
  for n in s.select('picture source[srcset]'):
   source_count+=1;check(len(n['srcset'].split(','))>=2,path+': picture source overrides responsive image with one size')
 # Every listing card, including the three featured cards, must expose a thumbnail.
 s=BeautifulSoup((ROOT/'en/blog.html').read_text(encoding='utf8'),'html.parser')
 cards=s.select('#latest .cards a.card, .journal-featured-card')
 check(len(cards)==445,'English card inventory changed')
 check(all(len(c.select('img.journal-thumbnail'))==1 for c in cards),'Missing/duplicate English thumbnails')
 for card in cards:
  target=urlsplit(urljoin(BASE,card['href'])).path.lstrip('/')
  page=BeautifulSoup((ROOT/target).read_text(encoding='utf8'),'html.parser')
  cv=cover(page);og=getmeta(page,'og:image');image=card.select_one('img.journal-thumbnail')
  if not image:continue
  got=origin_for_variant.get(urljoin(BASE,image['src']))
  expected=origin_for_variant.get(og,og)
  if expected not in byorigin:expected=origin_for_variant.get(urljoin(BASE+target,cv['src']))
  check(got==expected,'Thumbnail does not match target article '+target)
 oldmap=ET.fromstring(subprocess.check_output(['git','show',manifest['baseline']+':sitemap.xml'],cwd=ROOT))
 current=ET.parse(ROOT/'sitemap.xml').getroot();ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
 check([n.text for n in oldmap.findall('s:url/s:loc',ns)]==[n.text for n in current.findall('s:url/s:loc',ns)],'Sitemap page URL inventory/order changed')
 for before,after in zip(oldmap,current):
  def fields(n):return [(c.tag,c.text) for c in n if c.tag!='{'+ns['i']+'}image']
  check(fields(before)==fields(after),'Non-image sitemap data changed')
  loc=after.find('s:loc',ns).text;path=urlsplit(loc).path.lstrip('/')
  if path.startswith(('blog/','en/blog/')):
   s=BeautifulSoup((ROOT/path).read_text(encoding='utf8'),'html.parser')
   actual={n.text for n in after.findall('i:image/i:loc',ns)}
   expected=set()
   for n in content_images(s):
    u=urljoin(BASE+path,n['src']);origin=origin_for_variant.get(u,u)
    expected.add(origin)
   check(actual==expected,path+': sitemap differs from actual on-page original image identities')
 report=dict(changed_html=page_count,checked_images=img_count,picture_sources=source_count,english_thumbnail_cards=len(cards),verified_origins=len(assets),generated_variants=sum(not v['origin'] for a in assets for v in a['variants']),errors=errors)
 print(json.dumps(report,ensure_ascii=False,indent=2))
 (DATA/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return bool(errors)

if __name__=='__main__':
 import original_image_release as ORIGINAL_IMAGES
 if ORIGINAL_IMAGES.MANIFEST.exists():
  from qa_original_images import main as original_images_main
  sys.exit(original_images_main())
 sys.exit(main())
