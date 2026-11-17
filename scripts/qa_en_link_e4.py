"""Prove current E4 HTML from exact TSVs, preservation and all unchanged link gates."""
import collections,csv,html,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
import internal_link_audit_en as A
import en_e4_release as E4
from en_link_fix_release import english_previous
ROOT=E4.ROOT;M=E4.manifest();assert M and M['phase']=='E4'
assert M['baseline']=='9880f3f07c1b8898590cdd2afa3f323c497e4def'
errors=[]
def check(ok,message):
 if not ok:errors.append(message)
old=E4.predecessors();en=A.parse(str(ROOT),'en/blog');vi=A.parse(str(ROOT),'blog')
ep,ea=A.extract(en,['article.editorial','main.en-hub','article']);vp,_=A.extract(vi,['article.article-content'])
v2e={A.hreflang(s,'vi'):p for p,s in en.items() if A.hreflang(s,'vi') in vi}
check(set(old)==set(en)==set(M['baseline_en_hashes']),'Complete immutable 442-page EN inventory')
check({p.relative_to(ROOT).as_posix() for p in (ROOT/'data/en-translations/internal-links/e4').glob('*.tsv')}==set(M['tables']),'Every E4 TSV explicitly pinned')
for path in en:
 check(E4.digest(old[path])==M['baseline_en_hashes'][path],path+': original E3 baseline hash')
 if path not in M['files']:check((ROOT/path).read_text(encoding='utf-8')==old[path],path+': unchanged outside approved E4 scope')
renamed=removed=terms=added=0
for path,row in M['files'].items():
 raw=(ROOT/path).read_text(encoding='utf-8');before=old[path]
 check(E4.digest(before)==row['before_sha256'],path+': immutable predecessor')
 check(E4.qualified(path,raw),path+': actual HTML, TSV and VI hashes')
 check(E4.previous(path,raw)==before,path+': exact successor only')
 check(E4.previous(path,raw+' ')==raw+' ',path+': unknown HTML mutation rejected')
 check(row['vi_source']==(A.hreflang(en[path],'vi') or ''),path+': correct actual VI counterpart')
 expected=before
 for table in row['tsvs']:
  content=(ROOT/table).read_text(encoding='utf-8');check(E4.digest(content)==M['tables'][table]['sha256'],table+': updated TSV hash')
  rows=list(csv.DictReader(io.StringIO(content),delimiter='\t'));check(len(rows)==M['tables'][table]['rows'],table+': TSV row count')
  for r in rows:
   check(r['source']==path and r['vi_source']==row['vi_source'],table+': corresponding EN and VI')
   a,b=r['en_before'].replace('\r\n','\n'),r['en_after'].replace('\r\n','\n')
   check(expected.count(a)==1,table+': exact unique before span')
   if expected.count(a)==1:expected=expected.replace(a,b,1)
   kind=r['kind'];pa,pb=BeautifulSoup(a,'html.parser'),BeautifulSoup(b,'html.parser')
   links=lambda s:collections.Counter(n['href'] for n in s.select('a[href]'))
   if kind=='duplicate-or-density':
    unlinked=lambda s:re.sub(r'<a\b[^>]*>(.*?)</a\s*>',lambda m:m[1],s,flags=re.S|re.I)
    check(unlinked(a)==unlinked(b) and not links(pb)-links(pa),table+': only redundant wrappers removed')
    removed+=sum((links(pa)-links(pb)).values())
   elif kind=='terminology':
    translated=a
    for first,last in json.loads(r['choices']):
     check(translated.count(first)==1,table+': reviewed literal terminology');translated=translated.replace(first,last,1)
    check(translated==b and links(pa)==links(pb),table+': only reviewed wording changes');terms+=1
   elif kind=='anchor-label':
    labels=json.loads(r['labels']);hits=[]
    def relabel(match):
     span=match[0];anchor=BeautifulSoup(span,'html.parser').a
     for label in labels:
      if A.resolve(anchor.get('href'),path)==label['target'] and anchor.get_text(' ',strip=True)==label['old']:
       check(2<=len(label['new'].split())<=6 and not A.GENERIC.match(label['new']) and not A.BAD.search(label['new']),table+': short specific English anchor')
       hits.append(label);return span[:span.index('>')+1]+html.escape(label['new'])+span[span.rfind('</'):]
     return span
    computed=re.sub(r'<a\b[^>]*>.*?</a\s*>',relabel,a,flags=re.S|re.I)
    check(computed==b and len(hits)==len(labels) and links(pa)==links(pb),table+': only reviewed anchor text changes');renamed+=len(labels)
   elif kind=='context-addition':
    check(b.replace(' '+r['sentence'],'',1)==a,table+': only individually authored sentence added')
    new=BeautifulSoup(r['sentence'],'html.parser').select('a[href]');check(len(new)==1,table+': one new contextual link');added+=len(new)
    for anchor in new:check(anchor.get('hreflang')=='en' and 2<=len(anchor.get_text(' ',strip=True).split())<=6,table+': new English anchor')
   elif kind=='link-wrap':
    link='<a href="/'+r['target']+'" hreflang="en">'+r['new_label']+'</a>'
    check(a.count(r['old_label'])==1 and a.replace(r['old_label'],link,1)==b,table+': existing relevant text linked without rewriting');added+=1
   else:check(False,table+': unrecognized edit type '+kind)
 check(expected==raw,path+': full actual HTML replayed from E4 TSV only')
 a,b=BeautifulSoup(before,'html.parser'),BeautifulSoup(raw,'html.parser')
 for selector in ['title','meta','link','img','h1','h2','h3','h4','script','.toc','#toc','.article-toc','.seo-faq','.faq-section','#faq','.faq','.ac-reading-path','.ac-sources','.hub-locale','.ac-locale-link']:
  check([str(n) for n in a.select(selector)]==[str(n) for n in b.select(selector)],path+': original protected '+selector)
 switches=lambda s:[str(a) for a in s.select('a[href]') if A.SWITCH.search(a.get_text(' ',strip=True))]
 check(switches(a)==switches(b),path+': original-language switches unchanged')
 old_links=collections.Counter(n['href'] for n in a.select('a[href]'));new_links=collections.Counter(n['href'] for n in b.select('a[href]'))
 for href in new_links-old_links:
  target=A.resolve(href,path);check(target in en and (ROOT/target).is_file(),path+': real internal EN destination '+href)
  if target in en:check(not en[target].select_one('meta[http-equiv="refresh" i]'),path+': no redirect target')
 # Cumulative E3+E4 budget, using the exact E2 view retained by the release chain.
 e2=BeautifulSoup(english_previous(path,raw),'lxml');earlier,_=A.extract({path:e2},['article.editorial','main.en-hub','article'])
 original_targets={t for t,*_ in earlier[path] if t in en};current_targets={t for t,*_ in ep[path] if t in en}
 check(len(current_targets-original_targets)<=4,path+': cumulative four-new-contextual-target budget')

check(removed==M['removed_redundant_anchor_occurrences']==100,'Exactly 99 duplicate wrappers and one excess target removed')
check(renamed==M['renamed_frequency_anchors']+M['additional_existing_anchor_variants']==176,'All individually reviewed anchor labels applied')
check(terms==25,'All 25 reviewed terminology paragraphs applied')
check(added==M['new_contextual_links']==3,'Exactly three relevant contextual variants added')
variants=collections.defaultdict(set)
for path,soup in en.items():
 for anchor in soup.select('a[href]'):
  target=A.resolve(anchor['href'],path);label=anchor.get_text(' ',strip=True)
  if target in en and target!=path and label:variants[target].add(label.lower())
for target in en:check(len(variants[target])>=3,target+': at least three sitewide anchor variants (same scope as VI verification)')
for source,links in vp.items():
 target=v2e.get(source)
 if not target or en[target].select_one('main.en-hub'):continue
 wanted={v2e[t] for t,*_ in links if t in v2e and v2e[t]!=target};actual={t for t,*_ in ep[target]}
 check(wanted<=actual,target+': all contextual VI-to-EN relationships retained')
for script in ['internal_link_audit.py','internal_link_audit_en.py']:
 baseline=subprocess.check_output(['git','show',M['baseline']+':scripts/'+script],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
 check((ROOT/'scripts'/script).read_text(encoding='utf-8')==baseline,script+': every original gate and threshold unchanged')
for release in ['release-manifest.json','batch40-release.json','en-e3-release.json']:
 name='docs/link-fix-2026-11-17/'+release
 baseline=subprocess.check_output(['git','show',M['baseline']+':'+name],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
 check((ROOT/name).read_text(encoding='utf-8')==baseline,name+': all earlier release hashes unchanged')
check(not subprocess.check_output(['git','diff','--name-only',M['baseline'],'--','blog','docs/qa'],cwd=ROOT).strip(),'All VI HTML and historical QA evidence unchanged')
result=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT)],capture_output=True,encoding='utf-8')
check(result.returncode==0 and len(re.findall(r'^\[PASS\] E\d+ ',result.stdout,re.M))==14,'All fourteen actual-current EN gates pass unchanged')
print(json.dumps({'phase':'E4','changed_en_files':len(M['files']),'updated_tsvs':len(M['tables']),'removed_anchor_occurrences':removed,
 'renamed_anchors':renamed,'terminology_paragraphs':terms,'new_contextual_links':added,'sitewide_destinations_with_three_variants':len(variants),
 'contextual_vi_parity':'100%','all_fourteen_audit_gates':'PASS' if result.returncode==0 else 'FAIL',
 'old_hashes_and_protected_fields_unchanged':True,'errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
