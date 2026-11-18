"""Apply the verified responsive asset manifest without rewriting article prose."""
import hashlib,html,json,re,subprocess
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/blog-image-seo-2026-11-18'
BASE='https://apocalypsecloset.com/'
BASELINE='166c8047'

def baseline(paths,ref=BASELINE):
 refs=''.join(ref+':'+p+'\n' for p in paths)
 data=subprocess.check_output(['git','cat-file','--batch'],cwd=ROOT,input=refs.encode());offset=0;result={}
 for p in paths:
  end=data.index(b'\n',offset);header=data[offset:end].split()
  if len(header)!=3 or header[1]!=b'blob':raise ValueError('Missing pinned predecessor '+p)
  size=int(header[2]);offset=end+1;result[p]=data[offset:offset+size].decode('utf8');offset+=size+1
 return result

def attr(tag,key,value):
 pattern=r'(?<![\w:-])'+re.escape(key)+r'\s*=\s*(?:"[^"]*"|\x27[^\x27]*\x27|[^\s>]+)'
 if value is None:return re.sub(r'\s+'+pattern,'',tag,flags=re.I)
 new=key+'="'+html.escape(str(value),quote=True)+'"'
 if re.search(pattern,tag,re.I):return re.sub(pattern,lambda _:new,tag,count=1,flags=re.I)
 return re.sub(r'\s*/?>$',lambda m:' '+new+m.group(),tag,count=1)

def digest(raw):return hashlib.sha256(raw.encode('utf8')).hexdigest()
def getmeta(s,key):
 n=s.find('meta',attrs={'property':key}) or s.find('meta',attrs={'name':key})
 return n.get('content','') if n else ''
def setmeta(raw,key,value):
 for m in re.finditer(r'<meta\b[^>]*>',raw,re.I):
  n=BeautifulSoup(m.group(),'html.parser').meta
  if n.get('property',n.get('name'))==key:
   return raw[:m.start()]+attr(m.group(),'content',value)+raw[m.end():]
 tag='<meta '+('property' if key.startswith('og:') else 'name')+'="'+key+'" content="'+html.escape(str(value),quote=True)+'">\n'
 return raw.replace('</head>',tag+'</head>',1)
def absolute(path,url):return urljoin(BASE+path,url)
def content_images(s):return [i for i in s.select('main img, article img') if not i.find_parent(['noscript','header','footer','nav'])]
def cover(s):
 imgs=content_images(s)
 for i in imgs:
  if any(re.search(r'(^|[ -])(cover|hero)([ -]|$)',' '.join(n.get('class',[]))) for n in [i,*i.parents] if getattr(n,'attrs',None)):return i
 return imgs[0] if imgs else None

def main():
 assets=json.loads((DATA/'assets.json').read_text(encoding='utf8')); byurl={a['origin']:a for a in assets}
 def variants(a):return ', '.join(v['url']+' '+str(v['width'])+'w' for v in a['variants'])
 def fallback(a):return min(a['variants'],key=lambda v:abs(v['width']-640))
 paths=[p.relative_to(ROOT).as_posix() for folder in ['blog','en/blog'] for p in sorted((ROOT/folder).glob('*.html'))]+['blog.html','en/blog.html']
 before=baseline(paths)
 soups={p:BeautifulSoup(raw,'html.parser') for p,raw in before.items()}
 alts={}
 for p,s in soups.items():
  lang='en' if p.startswith('en/') else 'vi'
  for i in content_images(s):
   u=absolute(p,i.get('data-src',i.get('src','')))
   if i.get('alt'):alts.setdefault((u,lang),i['alt'])
 modified={}; pageinfo={}
 for p,raw in before.items():
  s=soups[p]; cv=cover(s);lang='en' if p.startswith('en/') else 'vi'
  has_article=bool(s.find('meta',attrs={'property':'og:type','content':'article'}))
  realcv=absolute(p,cv.get('data-src',cv.get('src',''))) if cv else ''
  originalog=getmeta(s,'og:image');og=absolute(p,originalog) if originalog else ''
  if og.startswith('https://apocalypsecloset.comdata:'):og=realcv
  oga=byurl.get(og)
  ogalt=getmeta(s,'og:image:alt') or alts.get((og,lang)) or (cv.get('alt','') if cv else '')
  if og and ogalt:
   finalog=absolute(p,oga['variants'][-1]['url']) if oga else og
   for key in ['og:image','twitter:image']:raw=setmeta(raw,key,finalog)
   for key in ['og:image:alt','twitter:image:alt']:raw=setmeta(raw,key,ogalt)
   if oga:
    largest=oga['variants'][-1]
    raw=setmeta(raw,'og:image:width',largest['width']);raw=setmeta(raw,'og:image:height',largest['height'])
    raw=setmeta(raw,'og:image:type','image/webp')
  # Update only existing ImageObject dimensions and the known malformed URL.
  def fixschema(m):
   text=m.group();opening=text[:text.index('>')+1];payload=text[len(opening):text.rindex('</script>')]
   obj=json.loads(payload)
   def walk(node):
    if isinstance(node,dict):
     node=dict(node)
     if node.get('@type')=='ImageObject' and node.get('url') in byurl:
      a=byurl[node['url']]
      if 'width' in node:node['width']=a['width']
      if 'height' in node:node['height']=a['height']
     return {k:walk(v) for k,v in node.items()}
    if isinstance(node,list):return [walk(v) for v in node]
    return realcv if isinstance(node,str) and node.startswith('https://apocalypsecloset.comdata:') else node
   updated=walk(obj)
   if updated==obj:return text
   return opening+json.dumps(updated,ensure_ascii=False,separators=(',',':'))+'</script>'
  raw=re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>',fixschema,raw)
  deferred=bool(cv and cv.get('data-src'))
  if deferred:
   raw=re.sub(r'<noscript>\s*<img\b[^>]*class="[^"]*apcl-standard-cover-image[^>]*>\s*</noscript>','',raw,count=1)
   raw=re.sub(r'  var cover=document\.querySelector\(\x27\.ac-deferred-cover\[data-src\]\x27\);[\s\S]*?  io\.observe\(cover\);\n','',raw,count=1)
  # Tag order is stable; use origin DOM ancestry to distinguish cards from body photos.
  contexts={}
  for i in s.find_all('img'):
   u=absolute(p,i.get('data-src',i.get('src','')))
   card=any(set(n.get('class',[])) & {'hub-card','related-outfit-card','card-cover'} for n in i.parents if getattr(n,'attrs',None))
   contexts.setdefault(u,card)
  def updateimg(m):
   tag=m.group();i=BeautifulSoup(tag,'html.parser').img
   u=absolute(p,i.get('data-src',i.get('src','')));a=byurl.get(u)
   if not a:return tag
   v=fallback(a);tag=attr(tag,'src',v['url']);tag=attr(tag,'srcset',variants(a))
   tag=attr(tag,'width',a['width']);tag=attr(tag,'height',a['height'])
   if not i.get('sizes'):
    sizes='(max-width: 650px) calc(100vw - 40px), (max-width: 950px) calc(50vw - 40px), 360px' if contexts.get(u) else '(max-width: 890px) calc(100vw - 40px), 850px' if lang=='en' else '(max-width: 768px) calc(100vw - 32px), 780px'
    tag=attr(tag,'sizes',sizes)
   tag=attr(tag,'decoding','async')
   if u==realcv and has_article:
    tag=attr(tag,'loading','eager');tag=attr(tag,'fetchpriority','high');tag=attr(tag,'data-src',None)
   return tag
  raw=re.sub(r'<img\b[^>]*>',updateimg,raw,flags=re.I)
  def updatesource(m):
   tag=m.group();n=BeautifulSoup(tag,'html.parser').source
   first=n.get('srcset','').split(',')[0].strip().split(' ')[0]
   a=byurl.get(absolute(p,first))
   return attr(tag,'srcset',variants(a)) if a else tag
  raw=re.sub(r'<source\b[^>]*>',updatesource,raw,flags=re.I)
  pageinfo[p]=dict(cover=realcv,og=og,og_alt=ogalt,lang=lang)
  modified[p]=raw
 # English featured and all catalogue cards get a real image from their target page.
 raw=modified['en/blog.html']
 def thumbnail(m):
  card=m.group();n=BeautifulSoup(card,'html.parser').a
  if not n or not (set(n.get('class',[])) & {'card','journal-featured-card'}):return card
  target=urlsplit(absolute('en/blog.html',n.get('href',''))).path.lstrip('/')
  info=pageinfo.get(target)
  if not info:return card
  u=info['og'] if info['og'] in byurl else info['cover'];a=byurl[u];v=fallback(a)
  alt=info['og_alt'] or alts[(u,'en')]
  tag='<img class="journal-thumbnail" src="'+v['url']+'" srcset="'+html.escape(variants(a),quote=True)+'" sizes="(max-width: 650px) calc(100vw - 88px), (max-width: 950px) calc(50vw - 80px), 495px" width="'+str(a['width'])+'" height="'+str(a['height'])+'" alt="'+html.escape(alt,quote=True)+'" loading="lazy" decoding="async">'
  return card.replace('>', '>'+tag,1)
 raw=re.sub(r'<a\b[^>]*>[\s\S]*?</a>',thumbnail,raw)
 raw=raw.replace('</head>','<link rel="stylesheet" href="/assets/css/blog-image-seo-20261118.css">\n</head>',1)
 modified['en/blog.html']=raw
 # Add the actual editorial origins to each blog URL; do not invent new page URLs.
 sitemap=subprocess.check_output(['git','show',BASELINE+':sitemap.xml'],cwd=ROOT).decode('utf8')
 def sitemapblock(m):
  block=m.group();loc=re.search(r'<loc>(.*?)</loc>',block)
  if not loc:return block
  p=urlsplit(html.unescape(loc[1])).path.lstrip('/')
  if p not in soups or p in ['blog.html','en/blog.html']:return block
  urls=[]
  for i in content_images(soups[p]):
   u=absolute(p,i.get('data-src',i.get('src','')))
   if u.startswith(BASE) and u not in urls:urls.append(u)
  if not urls:return block
  block=re.sub(r'\s*<image:image>[\s\S]*?</image:image>','',block)
  addition=''.join('<image:image><image:loc>'+html.escape(u)+'</image:loc></image:image>' for u in urls)
  return block.replace('</url>',addition+'</url>')
 modified['sitemap.xml']=re.sub(r'<url\b[^>]*>[\s\S]*?</url>',sitemapblock,sitemap)
 before['sitemap.xml']=sitemap
 changes={}
 for p,raw in modified.items():
  raw=re.sub(r'(?m)^([^\n]*<(?:img|source)\b[^\n]*?)[ \t]+$',r'\1',raw)
  if raw!=before[p]:
   (ROOT/p).write_text(raw,encoding='utf8',newline='\n');changes[p]=dict(before=digest(before[p]),after=digest(raw))
 (DATA/'html-changes.json').write_text(json.dumps(dict(baseline=BASELINE,files=changes),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps(dict(changed_files=len(changes),thumbnails=len(re.findall('class="journal-thumbnail"',modified['en/blog.html']))),indent=2))

if __name__=='__main__':main()
