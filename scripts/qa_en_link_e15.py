"""Verify actual EN links everywhere, exact TSV replay and immutable earlier hashes."""
import csv,io,json,re,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
import internal_link_audit_en as A
import en_e15_release as E
R=E.ROOT;M=E.manifest();errors=[]
def check(ok,message):
 if not ok:errors.append(message)
check(M['baseline']=='1dd10834efa9aaef5cff197cd2ff298172bbc9a4','Fixed merged E4 baseline')
en={p.relative_to(R).as_posix():BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser') for p in (R/'en').rglob('*.html')}
mapping={A.hreflang(s,'vi'):p for p,s in en.items() if A.hreflang(s,'vi')}
def special(t):return t.rstrip('/').split('/')[-1].removesuffix('.html') in ('outfits','style','phoi-do-nu-ca-tinh','app-phoi-do')
promoted=labelled=0
for path,row in M['files'].items():
 before=E.predecessor(path);raw=(R/path).read_text(encoding='utf-8');expected=before
 check(E.digest(before)==row['before_sha256'] and E.qualified(path,raw),path+': exact HTML, TSV, source hashes')
 check(E.previous(path,raw)==before and E.previous(path,raw+' ')==raw+' ',path+': reject unrecognized successors')
 for table in row['tsvs']:
  for t in csv.DictReader(io.StringIO((R/table).read_text(encoding='utf-8')),delimiter='\t'):
   check(t['source']==path and t['vi_source']==row['vi_source'],table+': corresponding source')
   a,b=t['en_before'],t['en_after'];check(expected.count(a)==1,table+': unique paragraph');expected=expected.replace(a,b,1)
   check(a.replace(t['old_anchor'],t['new_anchor'],1)==b,table+': only reviewed anchor changes')
   old,new=BeautifulSoup(t['old_anchor'],'html.parser').a,BeautifulSoup(t['new_anchor'],'html.parser').a
   if t['kind']=='promote':
    target=mapping.get(A.resolve(old['href'],path));check(target and new['href']=='/'+target and (R/target).is_file() and new.get('hreflang')=='en',table+': real paired EN target')
    check(old.get_text()==new.get_text()=='styling an A-line skirt',table+': reviewed natural English label unchanged');promoted+=1
   elif t['kind']=='label-exception':
    check(special(A.resolve(old['href'],path)) and old.attrs==new.attrs and new.get_text()==old.get_text()+' (Vietnamese)',table+': only disclose the approved VI exception');labelled+=1
   else:check(False,table+': unknown edit')
 check(expected==raw,path+': full HTML replayed from updated TSV')
 s=BeautifulSoup(before,'html.parser')
 for selector in ['title','meta','link','img','h1','h2','h3','h4','script','.toc','#toc','.article-toc','.seo-faq','.faq-section','#faq','.faq']:
  check([str(n) for n in s.select(selector)]==[str(n) for n in en[path].select(selector)],path+': protected '+selector+' unchanged')
 for script in en[path].select('script[type="application/ld+json"]'):json.loads(script.get_text())
 own=A.hreflang(s,'vi')
 original=lambda sp:[str(a) for a in sp.select('a[href]') if A.resolve(a['href'],path)==own or a.get_text(' ',strip=True)=='Read the Vietnamese original']
 check(original(s)==original(en[path]),path+': preserve original-language links')
remaining=untranslated=0
for path,s in en.items():
 own=A.hreflang(s,'vi')
 for a in s.select('a[href]'):
  target=A.resolve(a['href'],path);label=a.get_text(' ',strip=True)
  if not target or target==own or label=='Read the Vietnamese original':continue
  if special(target):check('(vietnamese)' in label.lower(),path+': label VI-only destination');continue
  if target.startswith('blog/') and target in mapping:remaining+=1;check(False,path+': untranslated navigation link '+target)
  elif target.startswith('blog/') and a.find_parent(['p','li','td','th','figcaption','blockquote']):untranslated+=1;check(False,path+': untranslated prose destination '+target)
check(promoted==M['promoted_links']==1 and labelled==M['labelled_vi_exceptions']==8,'Exactly one promotion and eight exception labels')
check(not subprocess.check_output(['git','diff','--name-only',M['baseline'],'--','blog','docs/qa'],cwd=R).strip(),'VI and historical QA evidence unchanged')
changed=set(subprocess.check_output(['git','diff','--name-only',M['baseline'],'--','en'],cwd=R).decode().splitlines())
check(changed==set(M['files']),'No EN page changed outside the nine reviewed paragraphs')
for name in ['release-manifest.json','batch40-release.json','en-e3-release.json','en-e4-release.json']:
 path='docs/link-fix-2026-11-17/'+name;check((R/path).read_text(encoding='utf-8')==E.predecessor(path),path+': all historical hashes intact')
supplied=(R/'data/en-links-e15-2026-11-17/supplied_audit_en.py').read_text(encoding='utf-8')
block=supplied[supplied.index('    # E15:'):supplied.index('    PROPER =')]
audit=M['audit']['path'];expected=E.predecessor(audit).replace('    PROPER =',block+'    PROPER =',1)
check((R/audit).read_text(encoding='utf-8')==expected,'Only exact supplied E15 added; reviewed RULES/HUBS and fourteen gates unchanged')
print(json.dumps({'changed_EN_pages':len(M['files']),'promoted_links':promoted,'VI_exception_labels_added':labelled,'remaining_VI_links_with_EN_twins':remaining,'untranslated_prose_links':untranslated,'EN_pages_scanned':len(en),'JSON_LD_changes_needed':0,'historical_hashes_preserved':True,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
