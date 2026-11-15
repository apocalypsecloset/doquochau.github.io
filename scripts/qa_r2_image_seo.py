"""Verify image text, metadata, sitemap coverage and scoped content preservation."""
import json,re,sys,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from bs4 import BeautifulSoup
from fix_r2_image_seo import article_nodes
PRESERVE='--preserve-baseline' in sys.argv
ROOT=Path(__file__).resolve().parents[1];BASE='https://apocalypsecloset.com';D=ROOT/'docs/image-seo-2026-11-15';errors=[];results=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def signatures(s):
 return {key:[str(n) for n in s.select(sel)] for key,sel in [('title','title'),('description','meta[name=description]'),('canonical','link[rel=canonical]'),('hreflang','link[hreflang]'),('robots','meta[name=robots]')]}
def schema_without_article_images(s):
 data=[json.loads(n.get_text()) for n in s.select('script[type="application/ld+json"]')]
 for entry in data:
  for node in article_nodes(entry):node.pop('image',None)
 return data
def article_text_without_captions(s):
 main=s.find('main')
 for n in main.select('figcaption'):n.decompose()
 return main.get_text(' ',strip=True)
sm=ET.parse(ROOT/'sitemap.xml').getroot();entries={n.find('{*}loc').text:n for n in sm.findall('{*}url')};image_ns='{http://www.google.com/schemas/sitemap-image/1.1}'
asset_map={r['url']:r for r in json.loads((D/'assets-qa.json').read_text())}
for row in json.loads((ROOT/'data/r2-220-publication.json').read_text()):
 for lang in ['vi','en']:
  url=row[lang+'_url'];path=urlsplit(url).path.lstrip('/');raw=(ROOT/path).read_text();s=BeautifulSoup(raw,'html.parser');main=s.find('main');oldraw=subprocess.check_output(['git','show','f0be5d3535c63433f75efc9dd67614767ae8109c:'+path],cwd=ROOT,text=True);old=BeautifulSoup(oldraw,'html.parser')
  if PRESERVE:check(signatures(s)==signatures(old),path+': preserved SEO fields')
  if PRESERVE:check(schema_without_article_images(s)==schema_without_article_images(old),path+': schema fields unchanged except Article image')
  if PRESERVE:check([str(n) for n in main.select('a')]==[str(n) for n in old.find('main').select('a')],path+': links and CTA unchanged')
  old_images=old.find('main').select('img');images=main.select('img')
  if path in ['blog/white-on-white.html','en/blog/white-on-white-outfit-guide.html']:
   old_images=[im for im in old_images if not re.fullmatch(r'/images/blog/white-on-white-0[1-5]\.webp',im.get('src',''))]
   images_to_compare=[im for im in images if not im.get('src','').endswith('/blog-covers/white-on-white-outfits.webp')]
   if PRESERVE:check(len(images_to_compare)==len(old_images),path+': only known 404 images removed')
  else:
   images_to_compare=images
   if PRESERVE:check(len(images)==len(old_images),path+': image count')
  for n,o in zip(images_to_compare,old_images):
   if PRESERVE:check({k:v for k,v in n.attrs.items() if k!='alt'}=={k:v for k,v in o.attrs.items() if k!='alt'},path+': image source/loading/dimensions preserved')
  editorial=[im for im in images if any(k in im.get('src','') for k in ['/images/','/assets/editorial/'])];expected=list(dict.fromkeys(urljoin(BASE+'/',im['src']) for im in editorial));actual=[n.find(image_ns+'loc').text for n in entries[url].findall(image_ns+'image')]
  check(actual==expected,path+': exact image sitemap coverage/order')
  check(len(actual)==len(set(actual)),path+': duplicate sitemap images')
  for u in actual:check(asset_map.get(u,{}).get('status')==200,path+': missing verified image asset '+u)
  hashes=[asset_map.get(u,{}).get('sha256') for u in actual]
  check(None not in hashes and len(hashes)==len(set(hashes)),path+': duplicate image content within article')
  for im in editorial:
   check(bool(im.get('alt','').strip()),path+': missing image alt')
   check(not re.search(r'ảnh minh họa|hình minh họa|cover illustration|fashion illustration',im.get('alt',''),re.I),path+': generic image alt')
  for cap in main.select('figcaption'):check(not re.search(r'ảnh minh họa|hình minh họa|cover illustration|fashion illustration',cap.get_text(),re.I),path+': generic image caption')
  og=s.select_one('meta[property="og:image"]')['content'];tw=s.select_one('meta[name="twitter:image"]')['content'];check(og in expected and og==tw and 'Logo-' not in og,path+': real OG/Twitter image')
  cover=next(im for im in editorial if urljoin(BASE+'/',im['src'])==og)
  check(s.select_one('meta[property="og:image:alt"]')['content']==cover['alt'],path+': OG alt')
  check(s.select_one('meta[name="twitter:image:alt"]')['content']==cover['alt'],path+': Twitter alt')
  check(s.select_one('meta[name="twitter:card"]')['content']=='summary_large_image',path+': Twitter card')
  nodes=[]
  for script in s.select('script[type="application/ld+json"]'):nodes.extend(article_nodes(json.loads(script.get_text())))
  check(bool(nodes),path+': article schema')
  for node in nodes:
   image=node.get('image',{});check(isinstance(image,dict) and image.get('url')==og,path+': schema image matches cover')
   check(image.get('width')==int(cover['width']) and image.get('height')==int(cover['height']),path+': schema dimensions')
  if PRESERVE:check(article_text_without_captions(s)==article_text_without_captions(old),path+': body text unchanged outside image captions')
  results.append({'file':path,'editorial_images':len(expected),'image_sitemap_entries':len(actual),'cover':og})
report={'preservation_baseline_checked':PRESERVE,'articles':len(results),'image_sitemap_entries':sum(r['image_sitemap_entries'] for r in results),'errors':errors,'results':results}
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
