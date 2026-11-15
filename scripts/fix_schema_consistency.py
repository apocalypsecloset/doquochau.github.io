"""Synchronize primary-page metadata and explicit bilingual brand entities."""
import json,re,html
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];BASE='https://apocalypsecloset.com';ORG=BASE+'/#organization';WEB=BASE+'/#website'
BRAND={'@type':['Organization','OnlineStore'],'@id':ORG,'name':'Apocalypse Closet','url':BASE+'/','description':'Independent graphic apparel project with a made-to-order Fourthwall storefront and Vietnamese and English alternative fashion guides.','logo':{'@type':'ImageObject','url':BASE+'/Logo-Apocalypse-Closet.webp','width':88,'height':88},'email':'apocalypsecloset@gmail.com','sameAs':['https://www.instagram.com/apocalypse.closet/','https://www.pinterest.com/apocalypsecloset/','https://www.tiktok.com/@apocalypse.closet','https://github.com/apocalypsecloset']}
SITE={'@type':'WebSite','@id':WEB,'url':BASE+'/','name':'Apocalypse Closet','publisher':{'@id':ORG},'inLanguage':['vi','en']}
META={'index.html':'Shop original gothic graphic tees and dark streetwear by Apocalypse Closet. Made to order, with secure Fourthwall checkout and alternative fashion guides.','about.html':'Apocalypse Closet kết hợp áo graphic in theo đơn qua Fourthwall với blog thời trang Việt–Anh, hướng dẫn phối đồ và bộ sưu tập outfit tham khảo.'}
def faq_pairs(s):
 pairs=[]
 for sec in s.select('.seo-faq,.faq-section'):
  if sec.select('details'):
   for d in sec.select('details'):
    if d.summary and d.p:pairs.append((d.summary.get_text(' ',strip=True),d.p.get_text(' ',strip=True)))
  else:
   for h in sec.select('h3'):
    a=h.find_next_sibling('p')
    if a:pairs.append((h.get_text(' ',strip=True),a.get_text(' ',strip=True)))
 return pairs

def fix():
 counts={};meta_file=ROOT/'docs/schema-pod-performance-2026-11-15/metadata.json';meta_changes=json.loads(meta_file.read_text()) if meta_file.exists() else {}
 def inc(k,n=1):counts[k]=counts.get(k,0)+n
 for p in sorted(ROOT.rglob('*.html')):
  if '.git' in p.parts:continue
  rel=p.relative_to(ROOT).as_posix();raw=p.read_text();s=BeautifulSoup(raw,'html.parser');can=s.select_one('link[rel=canonical]');m=s.select_one('meta[name=description]')
  if not can or not m or not s.h1:continue
  url=can['href'];lang=s.html.get('lang','en').split('-')[0];desc=META.get(rel,m['content']);h1=s.h1.get_text(' ',strip=True)
  if desc!=m['content']:meta_changes[rel]={'description':{'old':m['content'],'new':desc}}
  def sync_meta(match):
   t=BeautifulSoup(match[0],'html.parser').meta;key=t.get('name',t.get('property'))
   if key in ['description','og:description','twitter:description'] and t.get('content')!=desc:
    inc('meta_description');return re.sub(r'content="[^"]*"','content="'+html.escape(desc,quote=True)+'"',match[0])
   return match[0]
  raw=re.sub(r'<meta\b[^>]*>',sync_meta,raw)
  nodes=[];scripts=[m for m in re.finditer(r'<script\b[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>',raw) if BeautifulSoup(m[0],'html.parser').script.get('id')!='ac-product-schema']
  for match in scripts:
   t=BeautifulSoup(match[0],'html.parser').script;j=json.loads(t.get_text());nodes+=j.get('@graph',[j]) if isinstance(j,dict) else j
  def walk(n,root=False):
   if isinstance(n,list):return [walk(v) for v in n]
   if not isinstance(n,dict):return n
   n=dict(n);tp=n.get('@type');types=tp if isinstance(tp,list) else [tp]
   if n.get('@id')==ORG or ('Organization' in types and n.get('name')=='Apocalypse Closet'):
    return {'@id':ORG}
   if 'WebSite' in types and (n.get('@id')==WEB or n.get('url')==BASE+'/'):return {'@id':WEB}
   if any(t in ['Article','BlogPosting'] for t in types):
    for key,v in [('headline',h1),('description',desc),('inLanguage',lang),('url',url)]:
     if n.get(key)!=v:inc(key);n[key]=v
   if any(t in ['WebPage','AboutPage','ContactPage','CollectionPage','ProfilePage','SearchResultsPage'] for t in types) and (root or n.get('@id') in [url,url+'#page'] or n.get('url')==url):
    n['inLanguage']=lang
    n['description']=desc
   return {k:walk(v) for k,v in n.items() if k!='@context'}
  transformed=[walk(n,True) for n in nodes];transformed=[n for n in transformed if n!={'@id':ORG} and n!={'@id':WEB}]
  # One stable definition per document; nested references retain the same entity ID.
  transformed += [BRAND,SITE]
  pairs=faq_pairs(s)
  if pairs and not any(n.get('@type')=='FAQPage' for n in transformed):
   transformed.append({'@type':'FAQPage','@id':url+'#faq','inLanguage':lang,'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in pairs]});inc('new_faq')
  indexable=not any('noindex' in n.get('content','') for n in s.select('meta[name=robots]'))
  if indexable and url!=BASE+'/' and not any(n.get('@type')=='BreadcrumbList' for n in transformed):
   parts=[('Shop' if lang=='en' else 'Trang chủ',BASE+'/')]
   if '/blog/' in url:parts.append(('Journal' if lang=='en' else 'Blog',BASE+('/en/blog.html' if lang=='en' else '/blog.html')))
   elif '/outfits/' in url:parts.append(('Outfit',BASE+'/phoi-do-nu-ca-tinh.html'))
   elif '/style/' in url:parts.append(('Phong cách',BASE+'/phoi-do-nu-ca-tinh.html'))
   parts.append((h1,url));transformed.append({'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':dest} for i,(name,dest) in enumerate(parts)]});inc('breadcrumb')
  markup='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':transformed},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>'
  # Keep original script positions irrelevant to layout; all JSON-LD shares one graph.
  if scripts:
   start=scripts[0].start();raw=re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>',lambda m:m[0] if BeautifulSoup(m[0],'html.parser').script.get('id')=='ac-product-schema' else '',raw);raw=raw[:start]+markup+raw[start:]
  else:raw=raw.replace('</head>',markup+'\n</head>',1)
  if raw!=p.read_text():p.write_text(raw);inc('pages')
 D=ROOT/'docs/schema-pod-performance-2026-11-15';(D/'metadata.json').write_text(json.dumps(meta_changes,ensure_ascii=False,indent=2)+'\n');print(json.dumps(counts,indent=2))
if __name__=='__main__':fix()
