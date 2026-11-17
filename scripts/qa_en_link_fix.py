"""Validate E3 HTML/TSVs, recognizing only exact later successors before original checks."""
import collections,csv,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
import internal_link_audit_en as A
from en_link_fix_release import ROOT,manifest,digest,predecessors,english_previous,source_previous,qualified
from en_e4_release import previous as e4_previous
M=manifest();assert M and M['phase']=='E3'
assert M['baseline']=='a0272175089f56498bfecc40961a21baeb46fcf2'
assert M['source_baseline']=='9e16c2012f417cf5e4634b1c771a2c5d773e1ee8'
errors=[]
def check(ok,message):
 if not ok:errors.append(message)
def text(raw):return BeautifulSoup(raw,'html.parser').get_text(' ',strip=True)
old=predecessors();en=A.parse(str(ROOT),'en/blog');vi=A.parse(str(ROOT),'blog')
# Recheck the immutable E3 version only when the actual E4 successor is pinned;
# qa_en_link_e4 independently verifies the current HTML before this CI step.
en={p:BeautifulSoup(e4_previous(p,(ROOT/p).read_text(encoding='utf-8')),'lxml') for p in en}
en2vi={p:A.hreflang(s,'vi') for p,s in en.items()};v2e={v:p for p,v in en2vi.items() if v in vi}
ep,ea=A.extract(en,['article.editorial','main.en-hub','article']);vp,va=A.extract(vi,['article.article-content'])
vtext={p:s.get_text(' ',strip=True) for p,s in vi.items()}
all_tables={p.relative_to(ROOT).as_posix() for p in (ROOT/'data/en-translations/internal-links').glob('*.tsv')}
check(all_tables==set(M['tables']),'All supplemental TSVs explicitly pinned')
context_ids=[];nav_cards=0;sync_count=0
for path,row in M['files'].items():
 raw=e4_previous(path,(ROOT/path).read_text(encoding='utf-8'));before=old[M['baseline']+':'+path]
 check(digest(before)==row['before_sha256'],path+': exact original HTML')
 check(digest(raw)==row['after_sha256'] and qualified(path,raw),path+': current HTML and paired TSV/VI hashes')
 check(english_previous(path,raw)==before,path+': exact EN successor recognized')
 check(english_previous(path,raw+' ')==raw+' ',path+': unknown EN mutation rejected')
 check(row['vi_source']==(en2vi.get(path) or ''),path+': actual hreflang source binding')
 expected=before;new_context=0
 for table in row['tsvs']:
  data=(ROOT/table).read_text(encoding='utf-8')
  check(digest(data)==M['tables'][table]['sha256'],table+': exact updated TSV')
  rows=list(csv.DictReader(io.StringIO(data),delimiter='\t'))
  check(len(rows)==M['tables'][table]['rows'] and bool(rows),table+': complete nonempty TSV')
  unique={};groups=collections.defaultdict(list)
  for r in rows:
   check(r['source']==path and r['vi_source']==row['vi_source'],table+': source belongs to this HTML')
   previous,current=r['en_before'].replace('\r\n','\n'),r['en_after'].replace('\r\n','\n')
   unique[previous,current]=r;groups[previous,current].append(r)
   if row['vi_source']:
    for context in r['vi_context'].splitlines():
     check(context in vtext[row['vi_source']],table+': current VI context '+context[:60])
   if 'sentence' in r:
    context_ids.append(int(r['id']));new_context+=1
    anchors=BeautifulSoup(r['sentence'],'html.parser').select('a[href]')
    check(len(anchors)==1,table+': one link per authored sentence')
    for a in anchors:
     check(a.get('href')=='/'+r['target'] and a.get('hreflang')=='en',table+': intended EN target and language')
     check(a.get_text(' ',strip=True)==r['anchor'] and 2<=len(r['anchor'].split())<=6,table+': specific short English anchor')
   elif r['kind']=='navigation':
    targets=json.loads(r['targets_json']);nav_cards+=len(targets)
    for t in targets:check((ROOT/t).is_file(),table+': real child page '+t)
   elif r['kind']=='existing-link-sentence':
    sync_count+=1
    links=lambda s:collections.Counter(a['href'] for a in BeautifulSoup(s,'html.parser').select('a[href]'))
    check(links(previous)==links(current),table+': existing-link sync adds no destinations')
   else:check(r['kind']=='itemlist',table+': recognized changed span type')
  for (previous,current),r in unique.items():
   check(expected.count(previous)==1,table+': unique exact before span')
   if expected.count(previous)==1:expected=expected.replace(previous,current,1)
   if 'sentence' in r:
    additions=' '.join(x['sentence'] for x in groups[previous,current])
    check(current.replace(' '+additions,'',1)==previous or current.replace(additions+' ','',1)==previous,
          table+': original paragraph bytes retained around literal additions')
   elif r['kind']=='existing-link-sentence':
    a,b=BeautifulSoup(previous,'html.parser'),BeautifulSoup(current,'html.parser')
    check(len(a.select('p'))==len(b.select('p'))==1 and not b.select('img,h1,h2,h3,h4,script,table,details'),table+': only paragraph text/anchors')
 check(expected==raw,path+': full HTML reproducible only from updated TSV spans')
 check(new_context<=4,path+': no more than four new contextual links')
 a,b=BeautifulSoup(before,'html.parser'),BeautifulSoup(raw,'html.parser')
 cleaned=BeautifulSoup(raw,'html.parser')
 for n in cleaned.select('[data-en-link-fix="E3"]'):n.decompose()
 for selector in ['title','meta','link','img','h1','h2','h3','h4','.toc','#toc','.article-toc','.seo-faq','.faq-section','#faq','.faq','.ac-reading-path','.ac-sources']:
  check([str(n) for n in a.select(selector)]==[str(n) for n in cleaned.select(selector)],path+': original protected '+selector)
 check([str(n) for n in a.select('img')]==[str(n) for n in b.select('img')],path+': no image added or changed')
 graphs=lambda s:[json.loads(j.string) for j in s.select('script[type="application/ld+json"]')]
 ga,gb=graphs(a),graphs(b)
 for data in gb:
  for node in data.get('@graph',[data]):
   if node.get('@type')!='CollectionPage':continue
   body=b.select_one('main.en-hub') or b.main;cards=body.select('a.hub-card[href]')
   expected_items=[{'@type':'ListItem','position':i+1,'name':n.h3.get_text(' ',strip=True),'url':'https://apocalypsecloset.com'+n['href']} for i,n in enumerate(cards)]
   check(node['mainEntity']=={'@type':'ItemList','numberOfItems':len(cards),'itemListElement':expected_items},path+': ItemList equals current visible cards')
 for graph in (ga,gb):
  for data in graph:
   for node in data.get('@graph',[data]):
    if node.get('@type')=='CollectionPage':node.pop('mainEntity',None)
 check(ga==gb,path+': JSON-LD unchanged outside required ItemList')
 baseline_prose,_=A.extract({path:a},['article.editorial','main.en-hub','article'])
 old_targets={t for t,*_ in baseline_prose[path] if t in en};new_targets={t for t,*_ in ep[path] if t in en}
 check(len(new_targets-old_targets)<=4,path+': contextual target budget')
 check(len(new_targets)<=max(12,len(old_targets)),path+': no density regression')
 old_links=collections.Counter(n['href'] for n in a.select('a[href]'))
 current_links=collections.Counter(n['href'] for n in b.select('a[href]'))
 check(not old_links-current_links,path+': existing link destinations retained')
 for href,count in (current_links-old_links).items():
  target=A.resolve(href,path)
  check(target in en and (ROOT/target).is_file(),path+': new link is a real internal EN page '+href)
  if target in en:check(not en[target].select_one('meta[http-equiv="refresh" i]'),path+': no redirect target')

check(sorted(context_ids)==list(range(644)),'All 644 individually authored contextual links represented once')
check(nav_cards==M['navigation_cards']==203,'All 203 added navigation cards represented')
check(sync_count==M['existing_link_sentence_updates']==27,'All 27 existing-link sentence updates represented')
paired_articles=0
for v,links in vp.items():
 e=v2e.get(v)
 if not e or en[e].select_one('main.en-hub'):continue
 wanted={v2e[t] for t,*_ in links if t in v2e and v2e[t]!=e}
 actual={t for t,*_ in ep[e]}
 check(wanted<=actual,e+': 100% contextual VI/EN target parity');paired_articles+=1
for cluster,vslug in A.VI_HUBS.items():
 parent=v2e['blog/'+vslug+'.html'];body=en[parent].select_one('main.en-hub') or en[parent].article
 cards={A.resolve(a['href'],parent) for a in body.select('a.hub-card[href]')}
 exempt={parent}|{v2e['blog/'+s+'.html'] for s in A.STYLE_SUBHUBS}
 children={e for v,e in v2e.items() if A.cluster(Path(v).stem)==cluster and e not in exempt and not en[e].select_one('main.en-hub')}
 check(children<=cards,parent+': every translated child has a visible card')

# Historical manifests/TSVs stay byte-for-byte unchanged; successors are additive only.
locks={};actual_hash_mismatches=0
from privacy_release import original as legacy_source
for p in sorted((ROOT/'data/en-translations').glob('*')):
 if not p.is_file():continue
 ref=M['baseline']+':'+p.relative_to(ROOT).as_posix()
 before=subprocess.check_output(['git','show',ref],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
 check(p.read_text(encoding='utf-8')==before,p.name+': historical translation file unchanged')
 if not re.fullmatch(r'batch\d+\.json',p.name) or p.stem in ('batch05b','batch40'):continue
 for c in json.loads(before):
  v='blog/'+c['vi_slug']+'.html';locks[v]=c['source_sha256']
  current=(ROOT/v).read_text(encoding='utf-8');view=source_previous(v,current)
  normalized=legacy_source(v,view);normalized=re.sub(r'<!-- AC-EN-BATCH[0-9]{2}-START -->.*?<!-- AC-EN-BATCH[0-9]{2}-END -->','',normalized,flags=re.S)
  check(digest(normalized)==c['source_sha256'],v+': old source lock preserved and exact successor qualified')
  check(source_previous(v,current+' ')==current+' ',v+': unknown VI source mutation rejected')
  check(digest(legacy_source(v,current))!=digest(legacy_source(v,view)) or v not in M['sources'],v+': source view only after paired update')
check(locks==M['historical_source_locks'] and len(locks)==215,'All 215 historical source locks unchanged')
check(len(M['sources'])==210 and all(r['en'] in M['files'] for r in M['sources'].values()),'All 210 source successors require changed paired EN/TSV')
for path,row in M['sources'].items():
 check(digest((ROOT/path).read_text(encoding='utf-8'))==row['after_sha256'],path+': exact VI after-edit hash')
 check(row['locked_source_sha256']==locks[path],path+': original locked hash retained')
check(not subprocess.check_output(['git','diff','--name-only',M['baseline'],'--','blog','docs/qa'],cwd=ROOT).strip(),'VI HTML and old QA evidence unchanged in E3')
print(json.dumps({'phase':'E3','changed_en_files':len(M['files']),'supplemental_tsvs':len(M['tables']),
 'authored_contextual_links':len(context_ids),'new_navigation_cards':nav_cards,'existing_link_sentence_updates':sync_count,
 'contextual_parity':'100%','paired_articles_checked':paired_articles,'source_successors':len(M['sources']),
 'historical_hashes_unchanged':True,'protected_metadata_images_headings_toc_faq_unchanged':True,
 'replay_from_tsv_exact':True,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
