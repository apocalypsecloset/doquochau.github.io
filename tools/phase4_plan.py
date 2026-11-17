"""Build a review queue from human-selected edges; never generates link sentences."""
import collections,json,re,unicodedata
from pathlib import Path
from bs4 import BeautifulSoup
from phase4_relations import PAIRS,DIRECTED
from internal_link_audit import HUBS,STYLE_SUBHUBS,BAD_PHRASES

ROOT=Path(__file__).resolve().parents[1]
pages=json.loads((ROOT/'tools/phase4_inventory.json').read_text(encoding='utf8'))
edges=set(DIRECTED)
for a,b in PAIRS:edges.update(((a,b),(b,a)))
edges=sorted((a,b) for a,b in edges if b not in pages[a]['prose_out'])
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s.lower().replace('đ','d')) if unicodedata.category(c)!='Mn')
stop={'phoi','cach','theo','trang','phong','cach','phu','hop','nhung','gi','la','voi','cho','cua','nu','the','and','outfit','guide','do','ao','quan','vay','dam'}
used=collections.defaultdict(collections.Counter);plan=[]
plan_path=ROOT/'tools/phase4_plan.json'
previous=json.loads(plan_path.read_text(encoding='utf8')) if plan_path.exists() else []
prior={(r['source'],r['target']):r for r in previous}
next_id=max((r['id'] for r in previous),default=-1)+1
for source,target in edges:
    old=prior.get((source,target))
    if old:i=old['id']
    else:i=next_id;next_id+=1
    a,b=pages[source],pages[target]
    words={w for w in re.findall(r'[a-z0-9]+',norm(target+' '+b['title'])) if len(w)>2 and w not in stop}
    candidates=[]
    for j,p in enumerate(a['paragraphs']):
        if len(a['paragraphs'])>=6 and not int(len(a['paragraphs'])*0.15)<=j<max(1,int(len(a['paragraphs'])*0.8)):
            continue
        text=BeautifulSoup(p['old'],'html.parser').get_text(' ',strip=True)
        if BAD_PHRASES.search(text):continue
        tokens=set(re.findall(r'[a-z0-9]+',norm(text+' '+p['heading'])))
        # Select a passage to read, not an editorial decision about the final wording.
        score=3*len(tokens&words)-used[source][j]*7
        if j==0:score-=1
        candidates.append((score,-abs(j-len(a['paragraphs'])//2),j))
    assert candidates,source
    j=old['paragraph'] if old else max(candidates)[2];used[source][j]+=1
    plan.append(dict(id=i,source=source,target=target,paragraph=j,title=b['title'],description=b['description']))
plan.sort(key=lambda r:r['id'])
(ROOT/'tools/phase4_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
out={s:set(p['prose_out']) for s,p in pages.items()}
incoming=collections.defaultdict(set)
for a,b in edges:out[a].add(b)
for a,targets in out.items():
    for b in targets:incoming[b].add(a)
parents=set(HUBS.values())|set(STYLE_SUBHUBS)
degree=collections.Counter(a for a,b in edges)
print('PROPOSED',len(edges),'EDGES',len(degree),'SOURCE FILES')
print('OVER NEW-LINK BUDGET:',[(s,n) for s,n in degree.items() if n>3])
print('OVER 12 PROSE TARGETS:',[(s,len(ts)) for s,ts in out.items() if len(ts)>12])
print('REMAINING ORPHANS:',[s for s in pages if not incoming[s]])
print('REMAINING REAL SIBLINGS:',[s for s,p in pages.items() if not any(t not in parents and pages[t]['cluster']==p['cluster'] for t in out[s])])
print('REMAINING THIN:',[s for s in pages if len(out[s])<2])
for r in plan:
    print(f"\n{r['id']} {r['source']} -> {r['target']} [p{r['paragraph']}]\n{pages[r['source']]['paragraphs'][r['paragraph']]['old']}")
