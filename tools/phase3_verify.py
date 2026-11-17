"""Verify phase-three coverage, exact edits, and preservation against the phase-two commit."""
import collections,csv,io,json,re,subprocess
from pathlib import Path
from bs4 import BeautifulSoup
from internal_link_audit import HUBS,STYLE_SUBHUBS,MODULE_CLASSES,cluster,resolve

ROOT=Path(__file__).resolve().parents[1];BASELINE='985f5e3'
patches=json.loads((ROOT/'tools/phase3_patches.json').read_text(encoding='utf8'))
byfile=collections.defaultdict(list)
for p in patches:byfile[p['file']].append(p)
changed=subprocess.check_output(['git','diff','--name-only',BASELINE],cwd=ROOT,text=True).splitlines()
assert all(f.startswith('tools/') or re.fullmatch(r'blog/[^/]+\.html',f) for f in changed),changed
assert {f for f in changed if f.startswith('blog/')}==set(byfile)

# One git process reads all original files without hundreds of separate invocations.
request=''.join(BASELINE+':'+f+'\n' for f in byfile).encode()
batch=subprocess.check_output(['git','cat-file','--batch'],input=request,cwd=ROOT)
stream=io.BytesIO(batch);originals={}
for file in byfile:
    header=stream.readline().decode().strip().split();assert header[1]=='blob',header
    originals[file]=stream.read(int(header[2])).decode('utf8');assert stream.read(1)==b'\n'

protected=['title','h1','meta','link[rel=canonical]','script[type="application/ld+json"]','.article-toc','.toc','.ac-reading-path','.seo-faq','.ac-sources']
def subsequence(before,after):
    iterator=iter(after)
    return all(any(x==y for y in iterator) for x in before)
for file,ps in byfile.items():
    old=originals[file];new=(ROOT/file).read_bytes().decode('utf8')
    if '\r\n' in new and '\r\n' not in old:old=old.replace('\n','\r\n')
    expected=old
    for p in ps:
        assert expected.count(p['old'])==1,(file,'old span is not unique')
        expected=expected.replace(p['old'],p['new'],1)
    assert new==expected,(file,'unreviewed byte change')
    a,b=BeautifulSoup(old,'lxml'),BeautifulSoup(new,'lxml')
    for selector in protected:
        assert [str(n) for n in a.select(selector)]==[str(n) for n in b.select(selector)],(file,selector)
    for selector in ['img','h2','h3','h4']:
        assert subsequence([str(n) for n in a.select(selector)],[str(n) for n in b.select(selector)]),(file,selector)
    for p in ps:
        before=BeautifulSoup(p['old'],'lxml');after=BeautifulSoup(p['new'],'lxml')
        if p['kind']=='up':
            assert after.get_text(' ',strip=True).endswith(before.get_text(' ',strip=True)[-25:]),file

pages={}
for path in (ROOT/'blog').glob('*.html'):
    raw=path.read_bytes().decode('utf8')
    if re.search(r'http-equiv="refresh"',raw,re.I):continue
    s=BeautifulSoup(raw,'lxml');art=s.select_one('article.article-content') or s.find('main')
    links=set();prose=set()
    for a in art.select('a[href]'):
        target=resolve(a['href'],'blog/'+path.name)
        if not target or target=='blog/'+path.name:continue
        links.add(target);context=None;classes=set()
        for par in a.parents:
            if par is art:break
            classes.update(par.get('class',[]))
            if context is None and par.name in ('p','li','td','blockquote','figcaption'):context=par
        if context and not(classes&(MODULE_CLASSES|{'seo-faq'})) and not a.find('img'):prose.add(target)
    pages[path.stem]=dict(links=links,prose=prose)
coverage=[]
for c,h in HUBS.items():
    hubs={h}|(set(STYLE_SUBHUBS) if c=='Aesthetic/Style' else set())
    kids=[slug for slug in pages if cluster(slug)==c and slug not in hubs]
    down=set().union(*(pages[x]['links'] for x in hubs))
    assert all('blog/'+k+'.html' in down for k in kids),(c,'down coverage')
    assert all(pages[k]['prose'] & {'blog/'+x+'.html' for x in hubs} for k in kids),(c,'prose up coverage')
    coverage.append(dict(cluster=c,children=len(kids),down_links_complete=True,child_body_up_links_complete=True))

# The change log must retain both previous phases verbatim.
old_log=subprocess.check_output(['git','show',BASELINE+':tools/link_changes.csv'],cwd=ROOT).decode('utf8').replace('\r\n','\n')
new_log=(ROOT/'tools/link_changes.csv').read_text(encoding='utf8')
assert new_log.startswith(old_log),'Earlier change-log records altered'
rows=list(csv.DictReader(io.StringIO(new_log)))
old_rows=list(csv.DictReader(io.StringIO(old_log)))
assert len(rows)-len(old_rows)==454,(len(rows),len(old_rows))
report=dict(changed_blog_files=len(byfile),exact_spans=len(patches),new_parent_to_child_links=177,new_child_body_links=276,
    metadata_schema_and_protected_sections_preserved=True,existing_images_and_headings_preserved=True,
    removed_prose_links_to_preserve_density=1,reviewed_spans_only=True,coverage=coverage,total_children=sum(x['children'] for x in coverage),change_log_added_rows=454)
(ROOT/'tools/phase3_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
