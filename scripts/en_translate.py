"""Generate English pages only from complete, source-hash-locked editorial translations."""
from bs4 import BeautifulSoup, Comment
from pathlib import Path
import hashlib,json,re,sys,posixpath,csv
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
VI=re.compile('[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]',re.I)
def source(slug):
 raw=(ROOT/'blog'/f'{slug}.html').read_text()
 raw=re.sub(r'<!-- AC-EN-BATCH[0-9]{2}-START -->.*?<!-- AC-EN-BATCH[0-9]{2}-END -->','',raw,flags=re.S)
 s=BeautifulSoup(raw,'html.parser')
 parts=[s.h1,s.select_one('.ac-article-intro'),s.select_one('.apcl-standard-cover'),s.select_one('article.article-content')]
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
     n[attr]={'Mục lục bài viết':'On this page','Tóm tắt nhanh':'At a glance','Hướng dẫn đọc tiếp':'Further reading'}.get(n[attr], 'Article navigation')
 mapping={urlsplit(r['vi_url']).path:urlsplit(r['en_url']).path for r in csv.DictReader((ROOT/'data/en-216-keyword-intent-audit.csv').open()) if r['en_url']}
 for manifest in sorted((ROOT/'data/en-translations').glob('batch[0-9][0-9].json')):
  for c in json.loads(manifest.read_text()):mapping['/blog/'+c['vi_slug']+'.html']='/en/blog/'+c['en_slug']+'.html'
 for p in parts:
  for a in p.select('a[href]'):
   h=a['href']
   if h.startswith('#') or urlsplit(h).scheme and urlsplit(h).netloc!='apocalypsecloset.com':continue
   parsed=urlsplit(h)
   path=posixpath.normpath('/'+parsed.path[3:] if h.startswith('../') else parsed.path)
   a['href']=mapping.get(path,path)+('?' + parsed.query if parsed.query else '')+('#' + parsed.fragment if parsed.fragment else '')
   if path in mapping:a['hreflang']='en'
   elif path!='/' and (ROOT/path.lstrip('/')).is_file():
    a['lang']='vi';a['hreflang']='vi';a['title']='Vietnamese reference';a.append(' (Vietnamese)')
 article=parts[3];article['class']=['editorial'];article['data-source-sha256']=config['source_sha256']
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
 graph=[{'@type':'BlogPosting','headline':config['title'],'description':config['description'],'inLanguage':'en','datePublished':'2026-11-03','dateModified':'2026-11-03','mainEntityOfPage':{'@type':'WebPage','@id':url},'isBasedOn':{'@id':vi},'image':['https://apocalypsecloset.com'+i['src'] for p in parts for i in p.select('img')],'author':{'@type':'Organization','name':'Apocalypse Closet','url':'https://apocalypsecloset.com/'},'publisher':{'@type':'Organization','name':'Apocalypse Closet','url':'https://apocalypsecloset.com/','logo':{'@type':'ImageObject','url':'https://apocalypsecloset.com/Logo-Apocalypse-Closet.webp'}}}]
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
 meta=template.new_tag('p',attrs={'class':'article-meta'});meta.string='APOCALYPSE CLOSET EDITORIAL · ENGLISH TRANSLATION · NOVEMBER 3, 2026';article.insert(0,meta)
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
