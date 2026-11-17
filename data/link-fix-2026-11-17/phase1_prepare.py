import collections, html, json, re
from pathlib import Path
from bs4 import BeautifulSoup
from phase1_choices import ANCHORS, TEXT, PARAGRAPHS, KEEP_DUPLICATES, DENSE_REMOVE

ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'tools/phase1_inventory.json').read_text(encoding='utf8'))
remove=set(DENSE_REMOVE)
for r in rows:
    if 'duplicate' in r['flags'] and r['id'] not in KEEP_DUPLICATES:
        remove.add(r['id'])
groups=collections.defaultdict(list)
for r in rows: groups[r['file'],r['cs']].append(r)
patches=[]
remaining=[]
for (file,cs), rs in groups.items():
    old=rs[0]['context'];new=old
    for r in sorted(rs,key=lambda r:r['start'],reverse=True):
        replacement=r['old']
        if r['id'] in remove:
            replacement=re.sub(r'^<a\b[^>]*>|</a>$','',replacement)
        elif r['id'] in ANCHORS:
            anchor=ANCHORS[r['id']]
            assert 2 <= len(anchor.split()) <= 6,(r['id'],anchor)
            if re.fullmatch(r'<p\b[^>]*>\s*', old[:r['start']-cs]):
                anchor=anchor[0].upper()+anchor[1:]
            replacement='<a href="/'+r['target']+'">'+html.escape(anchor)+'</a>'
        start=r['start']-cs;end=r['end']-cs
        assert new[start:end]==r['old'],r['id']
        new=new[:start]+replacement+new[end:]
    for r in rs:
        for a,b in TEXT.get(r['id'],[]):
            assert new.count(a)==1,(r['id'],a,new)
            new=new.replace(a,b)
    full=[PARAGRAPHS[r['id']] for r in rs if r['id'] in PARAGRAPHS]
    assert len(full)<=1
    if full:new=full[0]
    if new!=old:
        patches.append(dict(file=file,old=old,new=new,ids=[r['id'] for r in rs]))
    for r in rs:
        if r['id'] not in remove and not full:
            r=dict(r);r['anchor']=ANCHORS.get(r['id'],r['anchor']);r['context']=new
            remaining.append(r)

(ROOT/'tools/phase1_patches.json').write_text(json.dumps(patches,ensure_ascii=False,indent=2),encoding='utf8')
counts=collections.Counter()
print('PATCHES',len(patches),'FILES',len({p['file'] for p in patches}),'UNWRAP',len(remove))
for r in remaining:
    if r['target'].startswith('blog/'):
        key=(r['target'],r['anchor'].lower());counts[key]+=1
        if counts[key]>5:print(r['id'],r['file'][5:-5],'=>',r['target'][5:-5],r['anchor'],'|',BeautifulSoup(r['context'],'html.parser').get_text(' ',strip=True))
print('UNRESOLVED PHRASES / GENERIC')
for r in remaining:
    if re.search(r'\bhub\b|trang trụ cột|bổ trợ cho|cụm chủ đề|item guide',r['context'],re.I) or re.match(r'^(xem thêm|đọc thêm|tại đây)',r['anchor'],re.I):
        print(r['id'],r['file'],r['context'])
