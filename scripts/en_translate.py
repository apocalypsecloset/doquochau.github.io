"""Generate English pages only from complete, source-hash-locked editorial translations."""
from bs4 import BeautifulSoup, Comment
from pathlib import Path
import hashlib,json,re,sys,posixpath,csv,copy
from datetime import date
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
VI=re.compile('[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]',re.I)
def source(slug):
 raw=(ROOT/'blog'/f'{slug}.html').read_text()
 raw=re.sub(r'<!-- AC-EN-BATCH[0-9]{2}-START -->.*?<!-- AC-EN-BATCH[0-9]{2}-END -->','',raw,flags=re.S)
 s=BeautifulSoup(raw,'html.parser')
 body=s.select_one('article.article-content')
 if body is None and s.select_one('article#main-content > div.article-content'):
  # Preserve the complete wrapped article, including hero details and trailing references.
  # Split out the three opening parts once; never restrict extraction to the inner div.
  body=copy.deepcopy(s.select_one('article#main-content'))
  for selector in ['h1','.ac-article-intro','.apcl-standard-cover']:
   node=body.select_one(selector);assert node is not None,slug;node.decompose()
 parts=[s.h1,s.select_one('.ac-article-intro'),s.select_one('.apcl-standard-cover'),body]
 assert all(parts),slug
 texts=[]
 for p in parts:
  for n in p.descendants:
   if isinstance(n,str) and not isinstance(n,Comment) and n.strip() and n.strip() not in texts:texts.append(n.strip())
  for img in p.select('img'):
   if img.get('alt','').strip() and img['alt'].strip() not in texts:texts.append(img['alt'].strip())
 return raw,s,parts,texts
if __name__=='__main__' and sys.argv[1]=='extract':
 for slug in sys.argv[2:]:
  raw,s,parts,texts=source(slug)
  print('SOURCE',slug,'SHA256',hashlib.sha256(raw.encode()).hexdigest())
  for i,t in enumerate(texts): print(f'{i}\t{t}')

def faq_pairs(article):
 pairs=[]
 for section in article.select('.seo-faq'):
  for detail in section.select('details'):
   pairs.append((detail.summary,detail.p))
  if not section.select('details'):
   for question in section.select('h3'):
    answer=question.find_next_sibling('p')
    assert answer is not None,'FAQ heading without answer'
    pairs.append((question,answer))
 return pairs

def generate(config):
 slug=config['vi_slug']; raw,s,parts,texts=source(slug)
 assert hashlib.sha256(raw.encode()).hexdigest()==config['source_sha256'],f'Source changed: {slug}'
 entries={int(k):v for k,v in (l.rstrip('\n').split('\t',1) for l in (ROOT/'data/en-translations'/f'{slug}.tsv').read_text().splitlines() if l)}
 missing=[(i,t) for i,t in enumerate(texts) if VI.search(t) and i not in entries]
 assert not missing,f'Untranslated source segments in {slug}: {missing}'
 assert all(0<=i<len(texts) and v.strip() for i,v in entries.items())
 trans={t:entries.get(i,t) for i,t in enumerate(texts)}
 for part in parts:
  for n in list(part.descendants):
   if isinstance(n,str) and not isinstance(n,Comment) and n.strip():
    v=trans[n.strip()];n.replace_with((' ' if n[:1].isspace() else '')+v+(' ' if n[-1:].isspace() else ''))
  for img in part.select('img'):
   img['alt']=trans[img['alt'].strip()]
  for n in [part]+list(part.find_all()):
   for attr in ['aria-label','title']:
    if attr in n.attrs and VI.search(n[attr]):
     n[attr]={'Mục lục bài viết':'On this page','Tóm tắt nhanh':'At a glance','Hướng dẫn đọc tiếp':'Further reading','Bảng thông tin':'Information table'}.get(n[attr], 'Article navigation')
 # A translated fragment may start with a word where VI began with punctuation.
 # Keep words separated across inline tags without changing any content nodes.
 for part in parts:
  for n in list(part.descendants):
   if not isinstance(n,str) or isinstance(n,Comment) or not n:continue
   v=str(n);before=n.previous_sibling;after=n.next_sibling
   if getattr(before,'name',None) and before.get_text()[-1:].isalnum() and v[:1].isalnum():v=' '+v
   if getattr(after,'name',None) and after.get_text()[:1].isalnum() and v[-1:].isalnum():v+=' '
   if v!=str(n):n.replace_with(v)
 mapping={urlsplit(r['vi_url']).path:urlsplit(r['en_url']).path for r in csv.DictReader((ROOT/'data/en-216-keyword-intent-audit.csv').open()) if r['en_url']}
 for manifest in sorted((ROOT/'data/en-translations').glob('batch[0-9][0-9].json')):
  for c in json.loads(manifest.read_text()):mapping['/blog/'+c['vi_slug']+'.html']='/en/blog/'+c['en_slug']+'.html'
 for p in parts:
  for a in p.select('a[href]'):
   h=a['href']
   if h=='/' and (slug,a.get_text(strip=True)) in {('phoi-do-nu-ca-tinh-di-choi','the original outfit collection'),('phoi-do-nu-ca-tinh-cho-nu-lun','the original alternative outfit collection')}:
    # The source predates the POD homepage; route this EN reference to the retained outfit directory.
    h='/phoi-do-nu-ca-tinh.html'
   if h.startswith('#') or urlsplit(h).scheme and urlsplit(h).netloc!='apocalypsecloset.com':continue
   parsed=urlsplit(h)
   path=posixpath.normpath('/'+parsed.path[3:] if h.startswith('../') else parsed.path)
   a['href']=mapping.get(path,path)+('?' + parsed.query if parsed.query else '')+('#' + parsed.fragment if parsed.fragment else '')
   if path in mapping:a['hreflang']='en'
   elif path!='/' and (ROOT/path.lstrip('/')).is_file():
    a['lang']='vi';a['hreflang']='vi';a['title']='Vietnamese reference';a.append(' (Vietnamese)')
 article=parts[3];article['class']=['editorial'];article['data-source-sha256']=config['source_sha256']
 if slug=='phoi-do-voi-ao-blazer-den-nu':
  # Repair reversed source insertions in EN only, preserving every content node.
  colors=article.find(id='colors');colors_first=colors.find_previous_sibling('p')
  dresses=article.find(id='dress');dress_first=dresses.find_previous_sibling('p').find_previous_sibling('p')
  formulas=article.find(id='formulas');formula_image=formulas.find_next_sibling('figure')
  recipes=[]
  for h in article.find_all('h3',recursive=False):
   if re.match(r'^[1-6]\.',h.get_text()):
    paragraph=h.find_previous_sibling('p');assert paragraph is not None
    image=h.find_next_sibling('figure') if h.get_text().startswith('2.') else None
    recipes.append((int(h.get_text()[0]),h,paragraph,image))
  assert len(recipes)==6
  first_recipe=recipes[0][2]
  formulas.extract();first_recipe.insert_before(formulas)
  formula_image.extract()
  anchor_node=formulas
  for number,h,paragraph,image in sorted(recipes,key=lambda x:x[0]):
   h.extract();paragraph.extract();anchor_node.insert_after(h);h.insert_after(paragraph);anchor_node=paragraph
   if image is not None:image.extract();anchor_node.insert_after(image);anchor_node=image
  anchor_node.insert_after(formula_image)
  colors.extract();colors_first.insert_before(colors)
  dresses.extract();dress_first.insert_before(dresses)
  climate=article.find(id='climate');first=climate.find_previous_sibling('p').find_previous_sibling('p')
  climate.extract();first.insert_before(climate)
 if slug=='techwear-la-gi':
  # Source insertions placed these headings after their two introductory paragraphs.
  # Move only EN headings; retain all paragraphs, images and VI source bytes.
  for section_id in ['visual-code-techwear','gorpcore-va-techwear-cung-ky-thuat-khac-diem-xuat-phat']:
   heading=article.find(id=section_id)
   first=heading.find_previous_sibling('p').find_previous_sibling('p')
   assert first is not None
   heading.extract();first.insert_before(heading)
 if slug=='witch-aesthetic-whimsigoth-la-gi':
  # The VI source has a pre-existing reversed insertion order. Repair EN order only.
  starter=article.find(id='starter-wardrobe-whimsigoth');formulas=article.find(id='cong-thuc-whimsigoth')
  hs=[n for n in article.select('h3') if re.match(r'^[1-4]\.',n.get_text())]
  assert len(hs)==4
  pairs=[(h,h.find_previous_sibling('p')) for h in hs]
  one=next(h for h in hs if h.get_text().startswith('1.'))
  priority=one.find_next_sibling('p');start=priority.find_next_sibling('p')
  mistakes=next(h for h in article.select('h2') if 'Five Whimsigoth Styling' in h.get_text())
  mistake_list=formulas.find_next_sibling('ul');anchor=mistakes.find_next_sibling('h2')
  sequence=[starter,start,priority,formulas]
  for h,p in sorted(pairs,key=lambda pair:pair[0].get_text()):sequence.extend([h,p])
  sequence.extend([mistakes,mistake_list])
  for n in sequence:n.extract()
  for n in sequence:anchor.insert_before(n)

 if slug=='y2k-la-gi-phong-cach-y2k-nu':
  # Repair reversed source insertions in EN only; retain every original content node.
  headings=[h for h in article.select('h3') if re.match(r'^[1-5]\.',h.get_text())]
  assert len(headings)==5
  pairs=[(h,h.find_previous_sibling('p')) for h in headings]
  intro=next(h for h in headings if h.get_text().startswith('1.')).find_next_sibling('p')
  section=article.find(id='cong-thuc-phoi-do-y2k-nu')
  anchor=article.find(id='y2k-va-dark-y2k-khac-nhau-o-dau')
  sequence=[section,intro]
  for h,paragraph in sorted(pairs,key=lambda pair:pair[0].get_text()):sequence.extend([h,paragraph])
  for node in sequence:node.extract()
  for node in sequence:anchor.insert_before(node)
  pastel=article.find(id='y2k-khong-chi-la-pastel')
  paragraph=pastel.find_previous_sibling('p');paragraph.extract();pastel.insert_after(paragraph)

 # Reuse the established English shell, never the Vietnamese shop or shared navigation.
 template=BeautifulSoup((ROOT/'en/blog/soft-goth-style-outfits.html').read_text(),'html.parser')
 url='https://apocalypsecloset.com/en/blog/'+config['en_slug']+'.html';vi='https://apocalypsecloset.com/blog/'+slug+'.html'
 template.title.string=config['title']+' | Apocalypse Closet'
 for m in template.select('meta'):
  key=m.get('name',m.get('property',''))
  if key in ['description','og:description','twitter:description']:m['content']=config['description']
  elif key in ['og:title','twitter:title']:m['content']=config['title']
  elif key=='og:url':m['content']=url
  elif key in ['og:image','twitter:image']:m['content']='https://apocalypsecloset.com'+parts[2].img['src']
 for l in template.select('link[rel=canonical]'):l['href']=url
 for l in template.select('link[rel=alternate]'):l.decompose()
 for lang,href in [('en',url),('vi',vi)]:
  l=template.new_tag('link',rel='alternate',hreflang=lang,href=href);template.head.append(l)
 for j in template.select('script[type="application/ld+json"]'):j.decompose()
 published=config.get('published_date','2026-11-03')
 graph=[{'@type':'BlogPosting','headline':config['title'],'description':config['description'],'inLanguage':'en','datePublished':published,'dateModified':published,'mainEntityOfPage':{'@type':'WebPage','@id':url},'isBasedOn':{'@id':vi},'image':['https://apocalypsecloset.com'+i['src'] for p in parts for i in p.select('img')],'author':{'@type':'Organization','name':'Apocalypse Closet','url':'https://apocalypsecloset.com/'},'publisher':{'@type':'Organization','name':'Apocalypse Closet','url':'https://apocalypsecloset.com/','logo':{'@type':'ImageObject','url':'https://apocalypsecloset.com/Logo-Apocalypse-Closet.webp'}}}]
 faq=[]
 for question,answer in faq_pairs(article):
  faq.append({'@type':'Question','name':question.get_text(' ',strip=True),'acceptedAnswer':{'@type':'Answer','text':answer.get_text(' ',strip=True)}})
 if faq:graph.append({'@type':'FAQPage','inLanguage':'en','mainEntity':faq})
 graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':u} for i,(name,u) in enumerate([('Shop','https://apocalypsecloset.com/'),('Journal','https://apocalypsecloset.com/en/blog.html'),(config['title'],url)])]})
 j=template.new_tag('script',type='application/ld+json');j.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False);template.head.append(j)
 main=template.select_one('main .wrap');main.clear()
 for p in [parts[0],parts[1],parts[2]]:article.insert(0,p.extract())
 # Reverse insertion above must retain H1 -> intro -> cover.
 for p in parts[:3]:p.extract()
 for i,p in enumerate(parts[:3]):article.insert(i,p)
 meta=template.new_tag('p',attrs={'class':'article-meta'});meta.string='APOCALYPSE CLOSET EDITORIAL · ENGLISH TRANSLATION · '+date.fromisoformat(published).strftime('%B %-d, %Y').upper();article.insert(0,meta)
 switch=template.new_tag('p');a=template.new_tag('a',href=vi,lang='vi',hreflang='vi');a.string='Read the Vietnamese original';switch.append(a);article.insert(1,switch)
 main.append(article)
 for f in article.select('figure'):f['class']=['article-figure']
 for t in article.select('table'):t['class']=['article-table'];t.wrap(template.new_tag('div',attrs={'class':'article-table-scroll'}))
 for n in article.select('.article-toc'):n['class']=['article-toc-en']
 # Inline related-look images use the same established figure layout.
 for n in article.select('.related-outfit-card'):n['class']=['article-figure']
 css=template.new_tag('link',rel='stylesheet',href='/assets/css/en-translations.css?v=20261103b');template.head.append(css)
 out=ROOT/'en/blog'/f"{config['en_slug']}.html";out.write_text(str(template)+'\n')
 return out
if __name__=='__main__' and sys.argv[1]=='generate':
 for c in json.loads((ROOT/'data/en-translations'/((sys.argv[2] if len(sys.argv)>2 else 'batch02')+'.json')).read_text()):
  print(generate(c).relative_to(ROOT))
