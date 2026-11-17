"""Independent checks of actual E2 pages; legacy source-parity normalization is exact."""
import collections,copy,csv,hashlib,json,re,subprocess,sys
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup,Comment
from link_fix_release import ROOT,batch40_manifest,digest,hub_contract,batch40_previous
from en_translate_hubs import source,VI
from internal_link_audit import cluster

M=batch40_manifest();assert M and M['phase']=='E2' and M['translation_source_successors']=={}
configs=json.loads((ROOT/'data/en-translations/batch40.json').read_text(encoding='utf-8'))
expected=[('Phoi-mau','womens-color-coordination-guides',41),('Dia-diem-dip','occasion-destination-outfit-guides',23),
          ('Cham-soc','womens-clothing-care-guides',11),('Toc-lam-dep','alternative-hair-makeup-guides',9)]
assert len(configs)==4 and [c['en_slug'] for c in configs]==[x[1] for x in expected]
errors=[];results=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def git(path):return subprocess.check_output(['git','show',M['baseline']+':'+path],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
for p,row in M['files'].items():
 raw=(ROOT/p).read_bytes();check(hashlib.sha256(raw).hexdigest() in [row['after_sha256'],row['after_crlf_sha256']],p+': exact E2 successor')
 if row['kind']=='modified':
  check(digest(git(p))==row['before_sha256'],p+': original before hash')
  check(batch40_previous(p,raw.decode().replace('\r\n','\n'))==git(p),p+': exact predecessor')
  check(batch40_previous(p,raw.decode().replace('\r\n','\n')+' ')==raw.decode().replace('\r\n','\n')+' ',p+': unknown mutation rejected')
for p,sha in M['data_sha256'].items():check(digest((ROOT/p).read_text(encoding='utf-8'))==sha,p+': new TSV/manifest exact hash')
snapshots=json.loads((ROOT/M['parity_snapshots']).read_text(encoding='utf-8'))
mapping={}
for p in (ROOT/'blog').glob('*.html'):
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'lxml');a=s.select_one('link[hreflang=en]')
 if a:mapping[p.stem]=urlsplit(a['href']).path

for c,(cl,en,count) in zip(configs,expected):
 path='en/blog/'+en+'.html';raw=(ROOT/path).read_text(encoding='utf-8');s=BeautifulSoup(raw,'html.parser');main=s.main
 check(digest(snapshots[path])==M['parity_sha256'][path],path+': source-parity snapshot hash')
 contract=hub_contract(path,raw);check(contract==snapshots[path],path+': exact complete-directory successor recognized')
 check(hub_contract(path,raw+' ')==raw+' ',path+': arbitrary EN mutation rejected')
 base=BeautifulSoup(contract,'html.parser');normalized=BeautifulSoup(raw,'html.parser')
 for section in normalized.select('.batch40-additional-guides'):section.decompose()
 script=normalized.select_one('script[type="application/ld+json"]');base_script=base.select_one('script[type="application/ld+json"]')
 graph=json.loads(script.get_text());oldgraph=json.loads(base_script.get_text())
 nodes=graph['@graph'];collection=next(n for n in nodes if n.get('@type')=='CollectionPage')
 cards=normalized.main.select('a.hub-card[href]')
 collection['mainEntity']={'@type':'ItemList','numberOfItems':len(cards),'itemListElement':[{'@type':'ListItem','position':i+1,'name':a.h3.get_text(' ',strip=True),'url':'https://apocalypsecloset.com'+a['href']} for i,a in enumerate(cards)]}
 check(graph==oldgraph,path+': only ItemList extends the translated source contract')
 script.string=base_script.get_text();check(str(normalized)==str(base),path+': no edits outside the declared added cards/ItemList')
 kids={mapping[p.stem] for p in (ROOT/'blog').glob('*.html') if p.stem!=c['vi_slug'] and cluster(p.stem)==cl and p.stem in mapping}
 actual=main.select('a.hub-card[href]');targets=[a['href'] for a in actual]
 check(len(kids)==count and len(targets)==count and set(targets)==kids,path+': full child-card coverage')
 check(all(a.get('hreflang')=='en' and (ROOT/a['href'].lstrip('/')).is_file() for a in actual),path+': real EN child destinations')
 actual_graph=json.loads(s.select_one('script[type="application/ld+json"]').get_text())['@graph']
 itemlist=next(n for n in actual_graph if n.get('@type')=='CollectionPage')['mainEntity']
 check(itemlist['numberOfItems']==count,path+': actual ItemList count')
 check([(x['position'],x['name'],x['url']) for x in itemlist['itemListElement']]==[(i+1,a.h3.get_text(' ',strip=True),'https://apocalypsecloset.com'+a['href']) for i,a in enumerate(actual)],path+': actual schema/card parity')
 check(not VI.search(re.sub(r'caf[ée]s?|décor','',main.get_text(),flags=re.I)),path+': English body')
 authored=copy.copy(main)
 for n in authored.select('.hub-card,.hub-locale'):n.decompose()
 words=len(authored.get_text(' ',strip=True).split());check(words>=1000,path+': at least 1000 authored words excluding cards')
 vi='blog/'+c['vi_slug']+'.html';before=git(vi);current=(ROOT/vi).read_text(encoding='utf-8')
 marked=re.findall(r'<!-- AC-EN-BATCH40-START -->.*?<!-- AC-EN-BATCH40-END -->',current,re.S)
 check(len(marked)==1 and current.index(marked[0])<current.index('</head>'),vi+': one head-only marked addition')
 check(re.sub(r'<!-- AC-EN-BATCH40-START -->.*?<!-- AC-EN-BATCH40-END -->','',current,flags=re.S)==before,vi+': every other VI byte unchanged')
 for lang,url in [('vi','https://apocalypsecloset.com/'+vi),('en','https://apocalypsecloset.com/'+path)]:
  check(bool(s.select_one('link[hreflang="'+lang+'"][href="'+url+'"]')),path+': hreflang '+lang)
  check(bool(BeautifulSoup(current,'html.parser').select_one('link[hreflang="'+lang+'"][href="'+url+'"]')),vi+': hreflang '+lang)
 source_raw,_,_,texts=source(c['vi_slug']);check(digest(source_raw)==c['source_sha256'],vi+': brand-new source lock')
 tsv={int(k):v for k,v in (line.split('\t',1) for line in (ROOT/'data/en-translations'/(c['vi_slug']+'.tsv')).read_text(encoding='utf-8').splitlines())}
 check(set(tsv)==set(range(len(texts))),path+': complete TSV segment indices')
 present={str(n).strip() for n in base.main.descendants if isinstance(n,str) and not isinstance(n,Comment)}
 present|={n.get(attr) for n in base.main.find_all() for attr in ['alt','title','aria-label'] if n.get(attr)}
 check(all(value in present for value in tsv.values()),path+': every TSV translation present in the source-parity HTML')
 results.append(dict(vi_slug=c['vi_slug'],en_slug=en,authored_words=words,child_cards=count,tsv_segments=len(tsv)))

# Journal: exactly four new dated cards, with every old field retained except its new ordinal.
before=BeautifulSoup(git('en/blog.html'),'html.parser');after=BeautifulSoup((ROOT/'en/blog.html').read_text(encoding='utf-8'),'html.parser')
old={a['href']:a for a in before.select('#latest .cards a.card')};new={a['href']:a for a in after.select('#latest .cards a.card')}
wanted={'/en/blog/'+c['en_slug']+'.html' for c in configs}
check(len(old)==438 and len(new)==442 and set(new)-set(old)==wanted,'Journal: exactly four new EN cards')
for i,(href,a) in enumerate(old.items(),5):
 expected_card=copy.copy(a);eyebrow=expected_card.select_one('.eyebrow');eyebrow.string=re.sub(r'^\d+\s*/',f'{i:02d} /',eyebrow.get_text())
 check(str(new.get(href))==str(expected_card),'Journal: original card preserved '+href)
check(all(new[href].get('data-published')=='2026-11-17' for href in wanted),'Journal: actual publication date')
print(json.dumps(dict(results=results,old_translation_source_successors_released=0,errors=errors),ensure_ascii=False,indent=2));sys.exit(bool(errors))
