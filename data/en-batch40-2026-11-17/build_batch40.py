"""Adapt four new collection sources; no existing EN article/TSV is rewritten."""
import collections,copy,hashlib,html,json,re,sys
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from bs4 import BeautifulSoup,NavigableString
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(D))
from english_content import TRANSLATIONS
from en_translate_hubs import source,generate
from internal_link_audit import cluster
from fix_schema_consistency import BRAND,SITE
def english_names(value):
 for old,new in [('Đà Lạt','Da Lat'),('Bà Nà','Ba Na'),('Áo Dài','Ao Dai'),('áo dài','ao dai'),('Tết','Tet'),('xám','xam')]:value=value.replace(old,new)
 return value
SETTINGS=[
 ('Phoi-mau','phoi-mau-quan-ao-nu','womens-color-coordination-guides',"Women's Color Coordination Guides",'Choose clothing colors by shade, contrast, fabric and proportion, with guides for matching tops, trousers and skirts from the wardrobe you own.','Color guides used in the examples','These focused guides bring the examples above into the same directory, so you can compare an individual shade or a tonal outfit before changing another part of the combination.'),
 ('Dia-diem-dip','chon-trang-phuc-nu-theo-dia-diem-va-dip','occasion-destination-outfit-guides','Outfit Guides by Occasion and Destination','Plan outfits for travel, cafes, concerts, weddings and Tet by considering movement, weather, venue requirements and the clothes you already own.','More situations to plan around','These additional situations connect the practical checks above with a more specific day out, season or destination. Use the actual itinerary to choose which guide to open.'),
 ('Cham-soc','cach-cham-soc-do-nu','womens-clothing-care-guides',"Women's Clothing Care Guides",'Find clothing care guides for washing, storage, leather, boots, fit adjustments and hems, using garment labels and construction to choose the next step.','Everyday adjustments and care tasks','The remaining guides focus on the small adjustments mentioned in the text, from a stable tuck to a useful lace pattern. Choose the task after checking whether the item already fits.'),
 ('Toc-lam-dep','chon-toc-va-makeup-theo-trang-phuc','alternative-hair-makeup-guides','Alternative Hair and Makeup Guides','Coordinate alternative hair, makeup and nails with necklines, clothing colors and occasions, with practical guides for choosing a manageable level of detail.','Cuts, color and finishing details','Browse the individual cuts, color ideas and finishing options discussed above. Each guide addresses a different choice, so you can keep the rest of the outfit settled while exploring one change.'),
]
configs=[];mapping={};metadata={}
for p in sorted((ROOT/'en/blog').glob('*.html')):
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'lxml');a=s.select_one('link[hreflang=vi]')
 if a:mapping[urlsplit(a['href']).path]='/'+p.relative_to(ROOT).as_posix()
 metadata['/'+p.relative_to(ROOT).as_posix()]=(english_names(s.h1.get_text(' ',strip=True)),english_names(s.select_one('meta[name=description]')['content']))
for cl,vi,en,title,desc,heading,intro in SETTINGS:mapping['/blog/'+vi+'.html']='/en/blog/'+en+'.html'

for cl,vi,en,title,desc,heading,intro in SETTINGS:
 raw,s,main,texts=source(vi)
 rows=json.loads((D/(vi+'.source.json')).read_text(encoding='utf-8'))
 assert [r['vi'] for r in rows]==texts,'Frozen source segments changed'
 manual=TRANSLATIONS[vi];assert set(manual)=={r['id'] for r in rows if r['en'] is None},vi
 translated={r['id']:english_names(manual.get(r['id'],r['en'])) for r in rows}
 assert all(v and '\t' not in v and '\n' not in v for v in translated.values())
 (ROOT/'data/en-translations'/(vi+'.tsv')).write_text(''.join(str(i)+'\t'+translated[i]+'\n' for i in range(len(texts))),encoding='utf-8')
 configs.append(dict(vi_slug=vi,en_slug=en,title=title,description=desc,primary_intent=intro,
                     role='CATEGORY_HUB',source_kind='hub',source_sha256=hashlib.sha256(raw.encode()).hexdigest(),published_date='2026-11-17'))
(ROOT/'data/en-translations/batch40.json').write_text(json.dumps(configs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

parity={};added_cards={}
for c,settings in zip(configs,SETTINGS):
 cl,vi,en,title,desc,heading,intro=settings
 p=generate(c);s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for a in s.main.select('a[href]'):
  if a.find_parent(class_='hub-locale'):continue
  u=urlsplit(urljoin('https://apocalypsecloset.com/en/blog/'+en+'.html',a['href']))
  if u.path in mapping:
   a['href']=mapping[u.path]+('#'+u.fragment if u.fragment else '');a['hreflang']='en'
   a.attrs.pop('lang',None);a.attrs.pop('title',None)
   for n in list(a.descendants):
    if isinstance(n,NavigableString) and str(n).endswith(' (Vietnamese)'):n.replace_with(str(n)[:-13])
 # Build the source-parity contract first; schema always matches its visible cards.
 schema=s.select_one('script[type="application/ld+json"]');graph=json.loads(schema.string)['@graph']
 graph.extend([copy.deepcopy(BRAND),copy.deepcopy(SITE)])
 def sync_schema():
  cards=s.main.select('a.hub-card[href]');collection=next(n for n in graph if n.get('@type')=='CollectionPage')
  collection['description']=c['description'];collection['mainEntity']={'@type':'ItemList','numberOfItems':len(cards),'itemListElement':[{'@type':'ListItem','position':i+1,'name':a.h3.get_text(' ',strip=True),'url':'https://apocalypsecloset.com'+a['href']} for i,a in enumerate(cards)]}
  schema.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)
 sync_schema();parity['en/blog/'+en+'.html']=str(s)+'\n'
 have={a['href'] for a in s.main.select('a.hub-card[href]')}
 kids=sorted(mapping['/blog/'+p.stem+'.html'] for p in (ROOT/'blog').glob('*.html') if p.stem!=vi and cluster(p.stem)==cl and '/blog/'+p.stem+'.html' in mapping)
 missing=[k for k in kids if k not in have];added_cards['en/blog/'+en+'.html']=missing
 if missing:
  section=s.new_tag('section',attrs={'class':'batch40-additional-guides'});h=s.new_tag('h2');h.string=heading;section.append(h)
  paragraph=s.new_tag('p');paragraph.string=intro;section.append(paragraph)
  grid=s.new_tag('div',attrs={'class':'hub-grid'})
  for target in missing:
   t,description=metadata[target];a=s.new_tag('a',href=target,hreflang='en',attrs={'class':'hub-card'})
   body=s.new_tag('div',attrs={'class':'hub-card-body'});h=s.new_tag('h3');h.string=t;body.append(h);paragraph=s.new_tag('p');paragraph.string=description;body.append(paragraph);a.append(body);grid.append(a)
  section.append(grid);s.main.append(section)
 sync_schema();assert {a['href'] for a in s.main.select('a.hub-card[href]')}==set(kids),(vi,kids)
 authored=copy.copy(s.main)
 for n in authored.select('.hub-card,.hub-locale'):n.decompose()
 words=len(authored.get_text(' ',strip=True).split());assert words>=1000,(vi,words)
 p.write_text(str(s)+'\n',encoding='utf-8');print(en,'authored words',words,'cards',len(kids),'extra cards',len(missing))
 # Only two marked head tags are added to VI. No locale button or body edit.
 vp=ROOT/'blog'/(vi+'.html');vraw=vp.read_bytes().decode('utf-8');start='<!-- AC-EN-BATCH40-START -->';end='<!-- AC-EN-BATCH40-END -->'
 if start not in vraw:
  block=start+'<link rel="alternate" hreflang="vi" href="https://apocalypsecloset.com/blog/'+vi+'.html"><link rel="alternate" hreflang="en" href="https://apocalypsecloset.com/en/blog/'+en+'.html">'+end
  assert vraw.count('</head>')==1;vp.write_bytes(vraw.replace('</head>',block+'</head>',1).encode('utf-8'))

(D/'source_parity_snapshots_v2.json').write_text(json.dumps(parity,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'added_cards.json').write_text(json.dumps(added_cards,ensure_ascii=False,indent=2),encoding='utf-8')

# Exact Journal grid insertion; keep all other source bytes and existing card fields.
p=ROOT/'en/blog.html';raw=p.read_text(encoding='utf-8')
from journal_order import grid,cards
a,b=grid(raw,'en');previous=cards(raw,'en');assert len(previous)==438,'Generate E2 only from E1 Journal'
new=[]
for i,c in enumerate(configs,1):
 new.append('<a class="card" data-published="2026-11-17" href="/en/blog/'+c['en_slug']+'.html"><span class="eyebrow">'+f'{i:02d}'+' / CATEGORY HUB</span><h3>'+html.escape(c['title'])+'</h3><p>'+html.escape(c['description'])+'</p><span class="read">READ THE GUIDE ↗</span></a>')
for i,card in enumerate(previous,5):new.append(re.sub(r'(<span class="eyebrow">)\d+(\s*/)',lambda m:m[1]+f'{i:02d}'+m[2],card,count=1))
p.write_text(raw[:a]+'\n'+'\n'.join(new)+'\n'+raw[b:],encoding='utf-8')
p=ROOT/'sitemap.xml';raw=p.read_text(encoding='utf-8')
for c in configs:
 url='https://apocalypsecloset.com/en/blog/'+c['en_slug']+'.html';assert '<loc>'+url+'</loc>' not in raw
 raw=raw.replace('</urlset>','  <url>\n    <loc>'+url+'</loc>\n    <lastmod>2026-11-17</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.7</priority>\n  </url>\n</urlset>')
p.write_text(raw,encoding='utf-8')
