"""Check phase-one scope, immutable content, and byte-preserving replacements."""
import collections, json, re, subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
BASELINE='9e16c2012f417cf5e4634b1c771a2c5d773e1ee8'
patches=json.loads((ROOT/'tools/phase1_patches.json').read_text(encoding='utf8'))
byfile=collections.defaultdict(list)
for p in patches:byfile[p['file']].append(p)
changed=subprocess.check_output(['git','diff','--name-only',BASELINE],cwd=ROOT,text=True).splitlines()
assert all(re.fullmatch(r'blog/[^/]+\.html',f) or f.startswith('tools/') or f=='CODEX_TASK.md' for f in changed),changed
changed=[f for f in changed if f.startswith('blog/')]
assert set(changed)==set(byfile),(set(changed)-set(byfile),set(byfile)-set(changed))
protected=['title','h1','meta','link[rel=canonical]','script[type="application/ld+json"]','img','h2','h3','h4','.toc','.article-toc','.ac-reading-path','.seo-faq','.ac-sources']
for file,ps in byfile.items():
    old=subprocess.check_output(['git','show',BASELINE+':'+file],cwd=ROOT).decode('utf8')
    new=(ROOT/file).read_bytes().decode('utf8')
    # Git stores LF; this Windows checkout uses CRLF. Compare in checkout form.
    if '\r\n' in new and '\r\n' not in old:
        old=old.replace('\n','\r\n')
    expected=old
    for p in ps:
        assert expected.count(p['old'])==1,(file,'nonunique old string')
        expected=expected.replace(p['old'],p['new'],1)
    assert new==expected,(file,'unexpected byte changes')
    a,b=BeautifulSoup(old,'lxml'),BeautifulSoup(new,'lxml')
    for selector in protected:
        assert [str(n) for n in a.select(selector)]==[str(n) for n in b.select(selector)],(file,selector)
    for p in ps:
        oldp,newp=BeautifulSoup(p['old'],'html.parser'),BeautifulSoup(p['new'],'html.parser')
        for anchor in newp.select('a[href]'):
            href=anchor['href']
            if href.startswith('/blog/'):
                assert (ROOT/href[1:]).is_file(),(file,href)
report=dict(changed_blog_files=len(byfile),exact_paragraph_replacements=len(patches),metadata_and_protected_sections_preserved=True,byte_changes_limited_to_reviewed_spans=True)
(ROOT/'tools/phase1_verification.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
