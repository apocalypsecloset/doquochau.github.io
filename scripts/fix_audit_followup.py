"""Apply the scoped mechanical audit repairs; preserve source markup outside fixes."""
import json,re,html,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from journal_order import publication_dates
ROOT=Path(__file__).resolve().parents[1];BASE='https://apocalypsecloset.com'
REPORT=ROOT/'docs/audit-followup-2026-11-15'
SHORT_TITLES={
'quan-xanh-den-phoi-ao-mau-gi':'Dark Navy Pants: Top Colors and 7 Outfit Ideas for Women',
'normcore-style-guide':'Normcore Style: Ordinary Dressing and Repeatable Outfits',
'ao-anime-nu':'Women’s Anime Tops: Choose Prints and Style Everyday Outfits',
'dior-new-look-1947-silhouette':"Dior’s New Look: The Silhouette That Changed Fashion in 1947",
'di-du-dam-hoi-nen-mac-gi-nu':'Vietnamese Engagement Ceremony: Outfits for Women Guests',
'dam-hong':'Pink Dresses: Shades, Silhouettes and Accessories by Occasion',
'alternative-layering-outfits-women':"Women's Alternative Layering: Texture, Proportion and 6 Outfits"}
DESCRIPTIONS={
'polyester-la-gi':'Understand polyester, fabric structure, lining and moisture management. Choose for your activity and follow garment-specific care.',
'vay-da-hoi':'Choose evening dresses by dress code, silhouette, support and movement. Explore gala, prom and relaxed looks; check fit before buying or renting.',
'tie-dye':'Distinguish tie-dye from printed effects and other resist techniques. Choose colors, try five outfits and check production and care details.',
'like-auth-la-gi':'Understand like auth listings, authenticity, condition and quality. Check product evidence, ask six questions and find transparent alternatives.',
'boutique-la-gi':'Compare boutiques, brands and multi-brand shops by selection, information and service. Check measurements, sourcing and purchase terms.',
'auth-la-gi':'Understand authentic, replica and secondhand labels. Check sellers, item records and authentication, then assess condition, sizing and support.',
'pyjama':'Distinguish sleepwear, loungewear and pyjama-inspired outfits. Check fit and context, try four looks and understand pyjama-party invitations.',
'hime-cut':'Understand the hime cut’s side sections, fringe and longer back. Choose length, density and upkeep for your hair; discuss references with a stylist.',
'giay-di-bo-nu':'Choose walking shoes for your routes. Check fit on both feet, compare construction claims, review online sizing and style everyday outfits.',
'victorian-goth':'Explore Victorian Goth collars, structured bodices and layered skirts. Try three modern outfits and separate historical inspiration from reconstruction.',
'bong-tai-bac':'Choose silver earrings by material, construction and size. Compare shapes with hair and collars, then check backs, weight and finish-specific care.',
'giay-cao-got':'Choose high heels by surfaces, wear time and fit. Compare heel types, test straps and toe space, then style with trouser and skirt hems.',
'phong-cach-workwear':'Explore women’s workwear-inspired outfits with chore jackets, carpenter trousers and utility details. Separate styling from protective clothing.',
'blouse':'Compare blouses and shirts, collars and sleeves. Check five fit points, try four outfits and plan practical layers and fabric-specific care.',
'high-fashion':'Understand high fashion, Haute Couture and ready-to-wear in context. Analyze outfits through shape, surface, detail and presentation.',
'thoi-trang-thap-nien-90-o-viet-nam':'Explore 1990s fashion in Vietnam through photographs, calendar imagery and áo dài. Adapt details while distinguishing inspiration from reconstruction.',
'kinh-khong-gong':'Compare rimless glasses by shape, proportions, bridge color and fit. Try three outfit ideas and check the exact lens configuration.',
'vai-me':'Understand the Vietnamese vai me fabric label, texture and variable fibers. Check coverage, stretch, seams and care for everyday or activewear.',
'butterfly-haircut':'Compare long and short butterfly layers. Plan for hair density, tying and natural drying, prepare references and practice manageable styling.',
'ao-chong-nang-nu':'Check UV information, coverage in motion and room for layers. Compare sun jackets, outfit ideas, sizing and product-specific care requirements.',
'giay-cong-so-nu':'Compare loafers, Oxfords, Mary Janes, flats and low heels. Check commute needs and fit, coordinate hems and plan footwear for different workdays.'}

def write():
 dates=publication_dates(); counts={}; overrides={};changes={}
 old_override=REPORT/'metadata.json'
 if old_override.exists():overrides=json.loads(old_override.read_text())
 def count(k,n=1):counts[k]=counts.get(k,0)+n
 for p in sorted(ROOT.rglob('*.html')):
  if '.git' in p.parts:continue
  rel=p.relative_to(ROOT).as_posix();raw=p.read_text();old=raw;s=BeautifulSoup(raw,'html.parser');en=rel.startswith('en/');blog=rel.startswith(('blog/','en/blog/'))
  raw,n=re.subn(r'(?<=href=")/en/(?=")','/',raw);count('home_links',n)
  raw,n=re.subn(r'https://twitter\.com/intent/tweet','https://x.com/intent/post',raw);count('share_links',n)
  raw,n=re.subn(r'<script\b[^>]*\bsrc=[\"\x27]https://static\.cloudflareinsights\.com/[^>]*></script>','',raw,flags=re.I);count('hardcoded_beacons',n)
  if en and s.title and len(s.title.get_text())>65:
   title=s.title.get_text();core=SHORT_TITLES.get(p.stem,title.removesuffix(' | Apocalypse Closet'))
   new=core+' | AC' if len(core)<=60 else core
   assert len(new)<=65,(rel,new)
   raw=re.sub(r'<title>[\s\S]*?</title>','<title>'+html.escape(new)+'</title>',raw,count=1)
   for tag in s.select('meta[property="og:title"],meta[name="twitter:title"]'):
    # Keep other attributes and original serialization.
    for m in list(re.finditer(r'<meta\b[^>]*>',raw)):
     node=BeautifulSoup(m.group(),'html.parser').meta
     if node.get('property',node.get('name')) in ['og:title','twitter:title']:
      replacement=re.sub(r'content="[^"]*"','content="'+html.escape(new,quote=True)+'"',m.group())
      raw=raw.replace(m.group(),replacement,1)
   overrides.setdefault(rel,{})['title']={'old':title,'new':new};count('shorter_titles')
  if rel.startswith('en/blog/') and p.stem in DESCRIPTIONS and len(s.select_one('meta[name=description]')['content'])>165:
   before=s.select_one('meta[name=description]')['content'];new=DESCRIPTIONS[p.stem];assert len(new)<=165
   for m in list(re.finditer(r'<meta\b[^>]*>',raw)):
    node=BeautifulSoup(m.group(),'html.parser').meta
    if node.get('property',node.get('name')) in ['description','og:description','twitter:description']:
     raw=raw.replace(m.group(),re.sub(r'content="[^"]*"','content="'+html.escape(new,quote=True)+'"',m.group()),1)
   overrides.setdefault(rel,{})['description']={'old':before,'new':new};count('shorter_descriptions')
  if blog:
   def schema(m):
    data=json.loads(m[2]);nodes=data.get('@graph',[data]);changed=False
    for node in nodes:
     if node.get('@type') not in ['BlogPosting','Article']:continue
     url=BASE+'/'+rel
     if not node.get('datePublished') and dates.get(url):node['datePublished']=dates[url];changed=True
     if not node.get('dateModified') and dates.get(url):node['dateModified']=dates[url];changed=True
    if changed:count('dated_schema');return m[1]+json.dumps(data,ensure_ascii=False,separators=(',',':'))+m[3]
    return m[0]
   raw=re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)([\s\S]*?)(</script>)',schema,raw)
   # Match the existing recorded journal date; don't invent an earlier publication date.
   if (BASE+'/'+rel in dates) and not re.search(r'20\d\d',s.select_one('.article-meta-top').get_text() if s.select_one('.article-meta-top') else '2026'):
    d=dates[BASE+'/'+rel];label='Published' if en else 'Xuất bản';visible=f'<span class="dot"></span><span class="ac-publication-date">{label} <time datetime="{d}">{d}</time></span>'
    m=re.search(r'<div\b[^>]*class="article-meta-top"[^>]*>',raw)
    if m:
     end=raw.index('</div>',m.end());raw=raw[:end]+visible+raw[end:];count('visible_dates')
   # Mirror existing visible FAQ verbatim; never invent answers or eligibility.
   if '"FAQPage"' not in raw:
    qs=[]
    for section in s.select('.seo-faq'):
     for detail in section.select('details'):
      if detail.summary and detail.p:qs.append((detail.summary.get_text(' ',strip=True),detail.p.get_text(' ',strip=True)))
     if not section.select('details'):
      for q in section.select('h3'):
       a=q.find_next_sibling('p')
       if a:qs.append((q.get_text(' ',strip=True),a.get_text(' ',strip=True)))
    if qs:
     faq={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in qs]}
     raw=raw.replace('</head>','<script type="application/ld+json">'+json.dumps(faq,ensure_ascii=False,separators=(',',':'))+'</script>\n</head>',1);count('faq_schema')
  if rel in ['blog.html','en/blog.html']:
   links=''
   for lang,dest in [('vi','blog.html'),('en','en/blog.html')]:
    if not s.select_one(f'link[hreflang="{lang}"][href="{BASE}/{dest}"]'):links+=f'<link rel="alternate" hreflang="{lang}" href="{BASE}/{dest}">\n';count('hreflang')
   raw=raw.replace('</head>',links+'</head>',1)
  if rel in ['en/blog/goth-vs-grunge-style.html','en/blog/how-to-style-gothic-graphic-tees.html'] and not s.select_one('link[hreflang="en"]'):
   raw=raw.replace('</head>',f'<link rel="alternate" hreflang="en" href="{BASE}/{rel}">\n</head>',1);count('hreflang')
  if raw!=old:p.write_text(raw);changes[rel]={'before':hashlib.sha256(old.encode()).hexdigest(),'after':hashlib.sha256(raw.encode()).hexdigest()}
 REPORT.mkdir(parents=True,exist_ok=True)
 oldchanges=json.loads((REPORT/'changes.json').read_text()) if (REPORT/'changes.json').exists() else {}
 oldchanges.update(changes);(REPORT/'changes.json').write_text(json.dumps(oldchanges,indent=2)+'\n');(REPORT/'metadata.json').write_text(json.dumps(overrides,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(counts,indent=2))
if __name__=='__main__':write()
