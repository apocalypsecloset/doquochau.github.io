"""Capture phase-three coverage and exact candidate paragraphs for editorial review."""
import collections, json, re
from pathlib import Path
from bs4 import BeautifulSoup
from internal_link_audit import HUBS,STYLE_SUBHUBS,cluster,resolve,MODULE_CLASSES

ROOT=Path(__file__).resolve().parents[1]
hubmap=dict(HUBS,**{'Outfit-core':'phoi-do-theo-item'})
pages={}
for path in sorted((ROOT/'blog').glob('*.html')):
    raw=path.read_bytes().decode('utf8')
    if re.search(r'http-equiv="refresh"',raw,re.I):continue
    pages[path.stem]=dict(raw=raw,soup=BeautifulSoup(raw,'html.parser'))
records=[];coverage={}
for c,h in hubmap.items():
    hubs={h}|(set(STYLE_SUBHUBS) if c=='Aesthetic/Style' else set())
    kids=[slug for slug in pages if cluster(slug)==c and slug not in hubs]
    down=set()
    for x in hubs:
        art=pages[x]['soup'].select_one('article.article-content') or pages[x]['soup'].find('main')
        down.update(resolve(a['href'],'blog/'+x+'.html') for a in art.select('a[href]'))
    missing=[x for x in kids if 'blog/'+x+'.html' not in down]
    coverage[c]=dict(hub=h,hubs=sorted(hubs),kids=kids,missing_down=missing,missing_up=[])
    for slug in kids:
        d=pages[slug];s=d['soup'];art=s.select_one('article.article-content') or s.find('main')
        up={'blog/'+x+'.html' for x in hubs}
        prose_up=False;any_up=False;ps=[]
        for a in art.select('a[href]'):
            if resolve(a['href'],'blog/'+slug+'.html') not in up:continue
            any_up=True;context=None;classes=set()
            for par in a.parents:
                if par is art:break
                classes.update(par.get('class',[]))
                if context is None and par.name in ('p','li','td','blockquote','figcaption'):context=par
            if context and not(classes & (MODULE_CLASSES|{'seo-faq'})) and not a.find('img'):prose_up=True
        if prose_up:continue
        coverage[c]['missing_up'].append(slug)
        lines=d['raw'].splitlines(keepends=True);offsets=[0]
        for line in lines:offsets.append(offsets[-1]+len(line))
        allp=art.find_all('p')
        for p in allp:
            classes=set(p.get('class',[]))
            for par in p.parents:
                if par is art:break
                classes.update(par.get('class',[]))
            text=p.get_text(' ',strip=True)
            if classes&(MODULE_CLASSES|{'seo-faq'}) or len(text.split())<30 or p.find('img') or p.find_parent('a'):continue
            start=offsets[p.sourceline-1]+p.sourcepos;end=d['raw'].index('</p>',start)+4
            ps.append(dict(start=start,old=d['raw'][start:end],heading=p.find_previous(['h2','h3']).get_text(' ',strip=True) if p.find_previous(['h2','h3']) else '',text=text))
        # A readable middle paragraph is a starting point only; the author can choose another.
        if not ps:raise ValueError(slug)
        i=min(len(ps)-1,max(1,len(ps)//3))
        records.append(dict(id=len(records),slug=slug,cluster=c,hub=h,has_module_up=any_up,title=s.h1.get_text(' ',strip=True),candidate=i,paragraphs=ps))
(ROOT/'tools/phase3_inventory.json').write_text(json.dumps(dict(coverage=coverage,up=records),ensure_ascii=False,indent=2),encoding='utf8')
for c,x in coverage.items():print(c,'DOWN',len(x['missing_down']),':',', '.join(x['missing_down']),'UP prose',len(x['missing_up']))
for x in records:
    p=x['paragraphs'][x['candidate']]
    print(f"\n{x['id']} {x['slug']} -> {x['hub']} [{x['candidate']}] {p['heading']}\n{p['old']}")
