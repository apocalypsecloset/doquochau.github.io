"""Freeze relationships and exact prose paragraphs for phase-four editorial work."""
import collections,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from internal_link_audit import HUBS,STYLE_SUBHUBS,MODULE_CLASSES,cluster,resolve

ROOT=Path(__file__).resolve().parents[1]
pages={}
parents=set(HUBS.values())|set(STYLE_SUBHUBS)
for path in sorted((ROOT/'blog').glob('*.html')):
    raw=path.read_bytes().decode('utf8')
    if re.search(r'http-equiv="refresh"',raw,re.I):continue
    s=BeautifulSoup(raw,'html.parser');art=s.select_one('article.article-content') or s.find('main')
    offsets=[0]
    for line in raw.splitlines(keepends=True):offsets.append(offsets[-1]+len(line))
    paragraphs=[];prose=[];anyl=set()
    for p in art.find_all('p'):
        classes=set(p.get('class',[]))
        for par in p.parents:
            if par is art:break
            classes.update(par.get('class',[]))
        if classes&(MODULE_CLASSES|{'seo-faq'}) or p.find_parent('a') or p.find('img') or len(p.get_text().split())<20:continue
        start=offsets[p.sourceline-1]+p.sourcepos;end=raw.index('</p>',start)+4
        h=p.find_previous(['h2','h3'])
        paragraphs.append(dict(old=raw[start:end],start=start,heading=h.get_text(' ',strip=True) if h else ''))
    for a in art.select('a[href]'):
        target=resolve(a['href'],'blog/'+path.name)
        if not target or target=='blog/'+path.name:continue
        anyl.add(target)
        context=None;classes=set()
        for par in a.parents:
            if par is art:break
            classes.update(par.get('class',[]))
            if context is None and par.name in ('p','li','td','blockquote','figcaption'):context=par
        if context and not(classes & MODULE_CLASSES) and not a.find('img'):
            prose.append(dict(target=target,anchor=a.get_text(' ',strip=True),context=context.get_text(' ',strip=True)))
    pages[path.stem]=dict(cluster=cluster(path.stem),title=s.h1.get_text(' ',strip=True),description=s.select_one('meta[name=description]')['content'],paragraphs=paragraphs,prose=prose,any_out=sorted(anyl))
inbound=collections.defaultdict(set)
for slug,p in pages.items():
    for a in p['prose']:
        if a['target'].startswith('blog/'):inbound[a['target'][5:-5]].add(slug)
for slug,p in pages.items():
    out={a['target'][5:-5] for a in p['prose'] if a['target'].startswith('blog/') and a['target'][5:-5] in pages}
    p['prose_out']=sorted(out);p['prose_in']=sorted(inbound[slug])
    p['real_siblings']=sorted(t for t in out if t not in parents and pages[t]['cluster']==p['cluster'])
(ROOT/'tools/phase4_inventory.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
for c in HUBS:
    orphans=[s for s,p in pages.items() if p['cluster']==c and not p['prose_in']]
    siblings=[s for s,p in pages.items() if p['cluster']==c and not p['real_siblings']]
    print(c,'ORPHANS',len(orphans),':',', '.join(orphans))
    print(c,'NO CHILD SIBLING',len(siblings),':',', '.join(siblings))
print('THIN:',[(s,len(p['prose_out'])) for s,p in pages.items() if len(p['prose_out'])<2])
