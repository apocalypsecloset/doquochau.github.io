"""Inspect actual VI/EN directory cards and freeze missing EN navigation targets."""
import json,sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
import internal_link_audit_en as A
vi=A.parse(str(ROOT),'blog'); en=A.parse(str(ROOT),'en/blog')
v2e={A.hreflang(s,'vi'):p for p,s in en.items() if A.hreflang(s,'vi') in vi}
main_hubs={p for p,s in en.items() if s.select_one('main.en-hub')}
parents={c:v2e['blog/'+v+'.html'] for c,v in A.VI_HUBS.items()}
styleparents={v2e['blog/'+v+'.html'] for v in A.STYLE_SUBHUBS}
result=[]
for cluster,source in parents.items():
 if cluster in ('Phoi-mau','Cham-soc','Dia-diem-dip','Toc-lam-dep'):continue
 vpath=A.hreflang(en[source],'vi');vs=vi[vpath];es=en[source]
 vb=vs.select_one('article.article-content') or vs.main
 eb=es.select_one('main.en-hub') or es.article
 cards={A.resolve(a['href'],source) for a in eb.select('a[href]') if a.find('h3')}
 desired={p for v,p in v2e.items() if A.cluster(Path(v).stem)==cluster and p not in main_hubs and p!=source and p not in styleparents}
 missing=sorted(desired-cards)
 groups={}
 for target in missing:
  vtarget=A.hreflang(en[target],'vi')
  va=next((a for a in vb.select('a[href]') if A.resolve(a['href'],vpath)==vtarget and a.find('h3')),None)
  vh=va.find_previous('h2') if va else None
  heading_id=vh.get('id') if vh else None
  eh=eb.find('h2',id=heading_id) if heading_id else None
  if eh is None:
   eh=eb.select_one('h2#internet-alt-aesthetics') if cluster=='Aesthetic/Style' else eb.find('h2')
  assert eh is not None,source
  heading_key=eh.get('id') or eh.get_text(' ',strip=True)
  group=groups.setdefault(heading_key,{'heading':str(eh),'targets':[],'vi_context':[]})
  group['targets'].append({'target':target,'title':en[target].h1.get_text(' ',strip=True),
                          'description':en[target].select_one('meta[name=description]')['content']})
  if vh and vh.parent:
   p=va.find_previous('p')
   if p:
    text=p.get_text(' ',strip=True)
    if text not in group['vi_context']:group['vi_context'].append(text)
 result.append({'source':source,'vi_source':vpath,'cluster':cluster,'desired':sorted(desired),'existing_cards':len(cards),
                'missing':len(missing),'groups':groups})
(D/'navigation_plan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for row in result:
 print(row['cluster'],row['source'],'cards',row['existing_cards'],'missing',row['missing'])
 for key,g in row['groups'].items():
  print(' ',key,':',', '.join(t['title'] for t in g['targets']))
  print(' VI:', ' | '.join(g['vi_context'])[:700])
