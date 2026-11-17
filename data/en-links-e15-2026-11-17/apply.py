import csv,hashlib,json,re,subprocess
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[2];D=Path(__file__).parent;BASE='1dd10834efa9aaef5cff197cd2ff298172bbc9a4'
def digest(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
inv=json.loads((D/'inventory_before.json').read_text(encoding='utf-8'))
todo=[dict(r,kind='promote') for r in inv['rows'] if r['target_en']]
todo += [dict(r,kind='label-exception') for r in inv['exceptions'] if r['kind']=='special' and '(vietnamese)' not in r['label'].lower()]
dest=R/'docs/link-fix-2026-11-17/en-e15-release.json';assert not dest.exists()
release={'phase':'E15','baseline':BASE,'files':{},'tables':{},'promoted_links':1,'labelled_vi_exceptions':8,'untranslated_prose_unwrapped':0}
ledger=[]
for r in todo:
 p=r['source'];path=R/p;before=path.read_text(encoding='utf-8');assert before==subprocess.check_output(['git','show',BASE+':'+p],cwd=R).decode('utf-8').replace('\r\n','\n')
 anchors=list(re.finditer(r'<a\b[^>]*>.*?</a\s*>',before,re.S|re.I))
 match=[m for m in anchors if (lambda a:a and a.get('href')==(r['old'] if r['kind']=='promote' else BeautifulSoup(r['anchor'],'html.parser').a['href']) and a.get_text(' ',strip=True)==r['label'])(BeautifulSoup(m[0],'html.parser').a)]
 assert len(match)==1,p;old_anchor=match[0][0]
 if r['kind']=='promote':
  new_anchor='<a href="/'+r['target_en']+'" hreflang="en">'+r['label']+'</a>'
 else:new_anchor=old_anchor.replace(r['label'],r['label']+' (Vietnamese)',1)
 ps=[m[0] for m in re.finditer(r'<p\b[^>]*>.*?</p\s*>',before,re.S|re.I) if old_anchor in m[0]];assert len(ps)==1,p
 a=ps[0];b=a.replace(old_anchor,new_anchor,1);after=before.replace(a,b,1)
 old_soup,new_soup=BeautifulSoup(before,'html.parser'),BeautifulSoup(after,'html.parser')
 assert [str(n) for n in old_soup.select('script')]==[str(n) for n in new_soup.select('script')],p
 assert all(r['label'] not in n.get_text() for n in old_soup.select('script[type="application/ld+json"]')),p
 table='data/en-translations/internal-links/e15/'+path.stem+'.tsv';t=R/table;t.parent.mkdir(exist_ok=True)
 row={'source':p,'vi_source':next((v for v,e in inv['mapping'].items() if e==p),''),'kind':r['kind'],'en_before':a,'en_after':b,'old_anchor':old_anchor,'new_anchor':new_anchor}
 with t.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(row),delimiter='\t',lineterminator='\n');w.writeheader();w.writerow(row)
 path.write_text(after,encoding='utf-8');v=row['vi_source']
 release['files'][p]={'before_sha256':digest(before),'after_sha256':digest(after),'tsvs':[table],'vi_source':v,'vi_source_sha256':digest((R/v).read_text(encoding='utf-8')) if v else None}
 release['tables'][table]={'sha256':digest(t.read_text(encoding='utf-8')),'source':p};ledger.append(row)
audit='scripts/internal_link_audit_en.py';audit_old=subprocess.check_output(['git','show',BASE+':'+audit],cwd=R).decode('utf-8').replace('\r\n','\n')
release['audit']={'path':audit,'before_sha256':digest(audit_old),'after_sha256':digest((R/audit).read_text(encoding='utf-8'))}
dest.write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(D/'patches.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'changed_pages':len(ledger),'changed_link_occurrences':len(ledger),'promoted':1,'labelled_exceptions':8,'JSON_LD_changes':0}))
