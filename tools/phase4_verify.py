"""Verify phase-four edits and the stronger semantic relationships beyond the audit gates."""
import collections,csv,io,json,re,subprocess
from pathlib import Path
from bs4 import BeautifulSoup
from internal_link_audit import HUBS,STYLE_SUBHUBS,MODULE_CLASSES,cluster,resolve,GENERIC
from phase4_relations import PAIRS,DIRECTED

ROOT=Path(__file__).resolve().parents[1];BASELINE='bddd970'
patches=json.loads((ROOT/'tools/phase4_patches.json').read_text(encoding='utf8'))
before=json.loads((ROOT/'tools/phase4_inventory.json').read_text(encoding='utf8'))
byfile=collections.defaultdict(list)
for p in patches:byfile[p['file']].append(p)
changed=subprocess.check_output(['git','diff','--name-only',BASELINE],cwd=ROOT,text=True).splitlines()
assert all(f.startswith('tools/') or re.fullmatch(r'blog/[^/]+\.html',f) for f in changed),changed
assert {f for f in changed if f.startswith('blog/')}==set(byfile)
request=''.join(BASELINE+':'+f+'\n' for f in byfile).encode()
stream=io.BytesIO(subprocess.check_output(['git','cat-file','--batch'],input=request,cwd=ROOT))
originals={}
for file in byfile:
    header=stream.readline().decode().strip().split();assert header[1]=='blob',header
    originals[file]=stream.read(int(header[2])).decode('utf8');assert stream.read(1)==b'\n'
protected=['title','h1','meta','link[rel=canonical]','script[type="application/ld+json"]','img','h2','h3','h4','.article-toc','.toc','.ac-reading-path','.seo-faq','.ac-sources']
for file,ps in byfile.items():
    old=originals[file];new=(ROOT/file).read_bytes().decode('utf8')
    if '\r\n' in new and '\r\n' not in old:old=old.replace('\n','\r\n')
    expected=old
    for p in ps:
        assert expected.count(p['old'])==1,(file,'old string is not unique')
        expected=expected.replace(p['old'],p['new'],1)
    assert expected==new,(file,'unreviewed byte changes')
    a,b=BeautifulSoup(old,'lxml'),BeautifulSoup(new,'lxml')
    for selector in protected:
        assert [str(n) for n in a.select(selector)]==[str(n) for n in b.select(selector)],(file,selector)

pages={};variants=collections.defaultdict(set)
for path in (ROOT/'blog').glob('*.html'):
    raw=path.read_bytes().decode('utf8');s=BeautifulSoup(raw,'lxml')
    for a in s.select('a[href]'):
        t=resolve(a['href'],'blog/'+path.name);anchor=a.get_text(' ',strip=True)
        if t and t.startswith('blog/') and t[5:-5] in before and t!='blog/'+path.name and anchor:
            variants[t[5:-5]].add(anchor.lower())
    if re.search(r'http-equiv="refresh"',raw,re.I):continue
    art=s.select_one('article.article-content') or s.find('main');out=set();all_out=set()
    for a in art.select('a[href]'):
        t=resolve(a['href'],'blog/'+path.name)
        if not t or t=='blog/'+path.name:continue
        all_out.add(t);classes=set();context=None
        for par in a.parents:
            if par is art:break
            classes.update(par.get('class',[]))
            if context is None and par.name in ('p','li','td','blockquote','figcaption'):context=par
        if context and not(classes&MODULE_CLASSES) and not a.find('img') and t.startswith('blog/') and t[5:-5] in before:out.add(t[5:-5])
    pages[path.stem]=dict(out=out,all_out=all_out,cluster=cluster(path.stem))
assert len(pages)==440
parents=set(HUBS.values())|set(STYLE_SUBHUBS);incoming=collections.defaultdict(set);budget=[]
for source,p in pages.items():
    assert 2<=len(p['out'])<=12,(source,'outgoing count')
    assert any(t not in parents and pages[t]['cluster']==p['cluster'] for t in p['out']),(source,'missing genuine child sibling')
    added=p['out']-set(before[source]['prose_out']);assert len(added)<=3,(source,'new-link budget')
    if added:budget.append(dict(source=source,added=len(added)))
    assert len(variants[source])>=3,(source,'anchor variants')
    for t in p['out']:incoming[t].add(source)
assert all(incoming[s] for s in pages)
for a,b in PAIRS:
    assert b in pages[a]['out'] and a in pages[b]['out'],('reciprocal relationship',a,b)
for a,b in DIRECTED:assert b in pages[a]['out'],(a,b)

place_checks=[]
for s,p in pages.items():
    if p['cluster']!='Dia-diem-dip' or s in parents:continue
    reciprocal=[t for t in p['out'] if s in pages[t]['out'] and (pages[t]['cluster'] in {'Ao','Quan','Vay-dam','Giay','Phu-kien'} or (pages[t]['cluster']=='Phoi-mau' and t.startswith(('ao-','quan-','chan-vay-'))))]
    assert reciprocal,(s,'missing reciprocal item relationship')
    place_checks.append(dict(source=s,items=sorted(reciprocal)))
fabric_checks=[]
for a,b in PAIRS:
    if pages[a]['cluster']=='Vai' and pages[b]['cluster']=='Cham-soc':fabric_checks.append(dict(fabric=a,care=b))
assert len({x['fabric'] for x in fabric_checks})==17
for c,h in HUBS.items():
    hubs={h}|(set(STYLE_SUBHUBS) if c=='Aesthetic/Style' else set())
    down=set().union(*(pages[x]['all_out'] for x in hubs))
    for k,p in pages.items():
        if p['cluster']==c and k not in hubs:
            assert 'blog/'+k+'.html' in down,(c,k,'lost down link')
            assert p['out']&hubs,(c,k,'lost prose up link')
old_log=subprocess.check_output(['git','show',BASELINE+':tools/link_changes.csv'],cwd=ROOT).decode('utf8').replace('\r\n','\n')
new_log=(ROOT/'tools/link_changes.csv').read_text(encoding='utf8');assert new_log.startswith(old_log)
added_rows=list(csv.DictReader(io.StringIO(new_log)))[len(list(csv.DictReader(io.StringIO(old_log)))):]
assert len(added_rows)==365
report=dict(changed_blog_files=len(byfile),exact_paragraph_replacements=len(patches),new_contextual_links=365,
    metadata_schema_images_headings_and_protected_sections_preserved=True,reviewed_spans_only=True,
    pages_with_two_to_twelve_contextual_destinations=len(pages),pages_with_incoming_contextual_links=len(incoming),
    pages_with_non_parent_sibling_links=len(pages),max_new_links_per_page=max(x['added'] for x in budget),
    destinations_with_three_anchor_variants=len(pages),reciprocal_fabric_care_pairs=fabric_checks,
    places_with_reciprocal_item_links=place_checks,phase3_parent_child_coverage_preserved=True,change_log_added_rows=365)
(ROOT/'tools/phase4_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k not in ['reciprocal_fabric_care_pairs','places_with_reciprocal_item_links']},ensure_ascii=False,indent=2))
print('Fabric-care pairs:',len(fabric_checks),'Place-item checks:',len(place_checks))
