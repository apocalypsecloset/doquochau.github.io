"""Apply reviewed image text and image discovery metadata to the approved 220 pairs."""
import json,re,html,hashlib
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];BASE='https://apocalypsecloset.com';D=ROOT/'docs/image-seo-2026-11-15'
def article_nodes(x):
 if isinstance(x,dict):
  kinds=x.get('@type',[]);kinds=[kinds] if isinstance(kinds,str) else kinds
  if any(t in kinds for t in ['Article','BlogPosting','NewsArticle']):yield x
  for v in x.values():yield from article_nodes(v)
 elif isinstance(x,list):
  for v in x:yield from article_nodes(v)
def set_meta(raw,key,value,kind='property'):
 pattern=r'<meta\b[^>]*>';count=0
 def change(m):
  nonlocal count
  tag=m.group();s=BeautifulSoup(tag,'html.parser').meta
  if s.get(kind)!=key:return tag
  count+=1
  return re.sub(r'\bcontent\s*=\s*([\"\']).*?\1',lambda m:'content="'+html.escape(str(value),quote=True)+'"',tag,count=1,flags=re.S)
 raw=re.sub(pattern,change,raw,flags=re.I)
 assert count<=1,(key,count)
 if not count:raw=raw.replace('</head>','<meta '+kind+'="'+key+'" content="'+html.escape(str(value),quote=True)+'">\n</head>',1)
 return raw

def apply():
 desc=json.loads((D/'image-descriptions.json').read_text());pairs=json.loads((ROOT/'data/r2-220-publication.json').read_text());report=[];sitemap_images={}
 for row in pairs:
  for lang in ['vi','en']:
   url=row[lang+'_url'];path=urlsplit(url).path.lstrip('/');file=ROOT/path;raw=file.read_text();count=0
   if path in ['blog/white-on-white.html','en/blog/white-on-white-outfit-guide.html']:
    def repair(m):
     frag=m.group();f=BeautifulSoup(frag,'html.parser');im=f.find('img')
     if not im or not re.fullmatch(r'/images/blog/white-on-white-0[1-5]\.webp',im.get('src','')):return frag
     if 'apcl-standard-cover' in f.figure.get('class',[]) or im.get('loading')=='eager':
      u=BASE+'/images/blog-covers/white-on-white-outfits.webp';text=html.escape(desc['white-on-white-outfits.webp'][lang],quote=True)
      klass='article-figure' if lang=='en' else 'apcl-standard-cover'
      return '<figure class="'+klass+'"><img src="'+u+'" width="1080" height="1920" alt="'+text+'" loading="eager" fetchpriority="high" decoding="async"><figcaption>'+text+'</figcaption></figure>'
     return ''
    raw=re.sub(r'<figure\b[^>]*>.*?</figure>',repair,raw,flags=re.S)
    if lang=='en' and 'src="'+BASE+'/images/blog-covers/white-on-white-outfits.webp"' not in raw:
     text=html.escape(desc['white-on-white-outfits.webp'][lang],quote=True)
     cover_html='<figure class="article-figure"><img src="'+BASE+'/images/blog-covers/white-on-white-outfits.webp" width="1080" height="1920" alt="'+text+'" loading="eager" fetchpriority="high" decoding="async"><figcaption>'+text+'</figcaption></figure>'
     raw=raw.replace('</section>','</section>'+cover_html,1)


   def figure(m):
    nonlocal count
    frag=m.group();s=BeautifulSoup(frag,'html.parser');im=s.find('img')
    if not im:return frag
    name=Path(urlsplit(im.get('src','')).path).name
    if name not in desc or not im.get('src','').startswith(BASE+'/images/'):return frag
    text=desc[name][lang];escaped=html.escape(text,quote=True)
    frag=re.sub(r'(<img\b[^>]*\balt=)([\"\']).*?\2',lambda x:x[1]+'"'+escaped+'"',frag,count=1,flags=re.S)
    frag=re.sub(r'(<figcaption\b[^>]*>).*?(</figcaption>)',lambda x:x[1]+escaped+x[2],frag,count=1,flags=re.S)
    if name=='white-on-white-outfits.webp':frag=re.sub(r'<figcaption\b[^>]*>.*?</figcaption>','',frag,flags=re.S)
    count+=1;return frag
   raw=re.sub(r'<figure\b[^>]*>.*?</figure>',figure,raw,flags=re.S)
   soup=BeautifulSoup(raw,'html.parser');main=soup.find('main');assert main,path
   images=[im for im in main.select('img[src]') if any(k in im['src'] for k in ['/images/','/assets/editorial/'])]
   cover=soup.select_one('.apcl-standard-cover img')
   if not cover or urlsplit(cover['src']).path.endswith('.svg'):cover=next(im for im in images if not urlsplit(im['src']).path.endswith('.svg'))
   cover_url=urljoin(BASE+'/',cover['src']);width=int(cover['width']);height=int(cover['height']);alt=cover.get('alt','')
   for key,value in [('og:image',cover_url),('og:image:width',width),('og:image:height',height),('og:image:alt',alt),('og:image:type','image/webp')]:raw=set_meta(raw,key,value)
   for key,value in [('twitter:image',cover_url),('twitter:image:alt',alt),('twitter:card','summary_large_image')]:raw=set_meta(raw,key,value,'name')
   nodes=0
   def schema(m):
    nonlocal nodes
    data=json.loads(m[2]);updated=False
    for node in article_nodes(data):
     node['image']={'@type':'ImageObject','url':cover_url,'width':width,'height':height,'caption':alt};nodes+=1;updated=True
    return m[1]+json.dumps(data,ensure_ascii=False)+m[3] if updated else m.group()
   raw=re.sub(r'(<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>)(.*?)(</script>)',schema,raw,flags=re.S);assert nodes,path
   file.write_text(raw)
   urls=list(dict.fromkeys(urljoin(BASE+'/',im['src']) for im in images));sitemap_images[url]=urls
   report.append({'file':path,'image_text_updates':count,'cover':cover_url,'cover_width':width,'cover_height':height,'image_sitemap_urls':urls,'article_nodes_updated':nodes})
 sitemap=(ROOT/'sitemap.xml').read_text();matched=set()
 def entry(m):
  s=m.group();loc=re.search(r'<loc>(.*?)</loc>',s).group(1)
  if loc not in sitemap_images:return s
  matched.add(loc);s=re.sub(r'\s*<image:image>.*?</image:image>','',s,flags=re.S)
  tags=''.join('\n    <image:image>\n      <image:loc>'+html.escape(u)+'</image:loc>\n    </image:image>' for u in sitemap_images[loc])
  return s.replace('\n  </url>',tags+'\n  </url>')
 sitemap=re.sub(r'<url>.*?</url>',entry,sitemap,flags=re.S);assert matched==set(sitemap_images)
 (ROOT/'sitemap.xml').write_text(sitemap);(D/'changes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('Updated articles',len(report),'image texts',sum(r['image_text_updates'] for r in report),'image sitemap references',sum(len(v) for v in sitemap_images.values()))
if __name__=='__main__':apply()
