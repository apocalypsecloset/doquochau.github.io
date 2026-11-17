"""Prove the exact VI link release, immutable originals and unreleased EN locks."""
import collections
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urljoin, urlsplit
from bs4 import BeautifulSoup
from link_fix_release import ROOT, manifest, digest, historical, added_successor, batch40_previous, approved_file_bytes

M = manifest()
assert M['baseline']=='9e16c2012f417cf5e4634b1c771a2c5d773e1ee8'
assert M['vi_release_commit']=='6d8a9c4f13b59bc12e0db087a2779fbcfa2480db'
assert M['new_hub_creation_commit']=='985f5e3'
assert set(M['patch_sources'])=={f'tools/phase{p}_patches.json' for p in [1,3,4,5]}
errors = []
def check(ok, message):
    if not ok:errors.append(message)
def git(*args):return subprocess.check_output(['git', *args], cwd=ROOT)
def blobs(refs):
    result = subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=('\n'.join(refs)+'\n').encode(),capture_output=True,check=True)
    stream=io.BytesIO(result.stdout);out={}
    for ref in refs:
        head=stream.readline().split();assert len(head)==3 and head[1]==b'blob', (ref,head)
        out[ref]=stream.read(int(head[2])).decode('utf-8').replace('\r\n','\n');assert stream.read(1)==b'\n'
    return out
def text(raw):return BeautifulSoup(raw,'lxml').get_text(' ',strip=True)
def sequence(before,after):
    it=iter(after)
    return all(any(x==y for y in it) for x in before)

refs=[]
for path,row in M['files'].items():
    refs.append((M['baseline'] if row['kind']=='modified' else M['new_hub_creation_commit'])+':'+path)
refs += [M['vi_release_commit']+':'+p for p in M['patch_sources']]
refs += [M['vi_release_commit']+':tools/link_changes.csv']
old=blobs(refs)
scope={line.split('\t')[1]:'added' if line.startswith('A\t') else 'modified'
       for line in git('diff','--name-status',M['baseline'],M['vi_release_commit'],'--','blog').decode().splitlines()}
check({p:r['kind'] for p,r in M['files'].items() if p.startswith('blog/')}==scope,'Exact reviewed VI file coverage')
all_vi=git('ls-tree','-r','--name-only',M['vi_release_commit'],'--','blog').decode().splitlines()
all_vi=[p for p in all_vi if p.endswith('.html')]
check({p.relative_to(ROOT).as_posix() for p in (ROOT/'blog').glob('*.html')}==set(all_vi),'No unregistered VI file additions or deletions')
unchanged=[p for p in all_vi if p not in scope]
frozen_vi=blobs([M['vi_release_commit']+':'+p for p in unchanged])
for p in unchanged:check((ROOT/p).read_text(encoding='utf-8')==frozen_vi[M['vi_release_commit']+':'+p],p+': unchanged VI file remains untouched')
logpath=next(p for p in [ROOT/'tools/link_changes.csv',ROOT/'data/link-fix-2026-11-17/link_changes.csv'] if p.is_file())
log=logpath.read_text(encoding='utf-8-sig')
check(digest(log)==M['log_sha256'],'Exact reviewed change log hash')
check(log.startswith(old[M['vi_release_commit']+':tools/link_changes.csv']),'Historical log records unchanged')
rows=list(csv.DictReader(io.StringIO(log)))
check(len(rows)==M['log_rows'],'Exact log row count')
pairs=collections.defaultdict(set)
for r in rows:pairs[r['file']].add((text(r['câu_trước']),text(r['câu_sau'])))

expected={p:old[(M['baseline'] if r['kind']=='modified' else M['new_hub_creation_commit'])+':'+p]
          for p,r in M['files'].items() if p.startswith('blog/')}
initial=dict(expected)
span_count=0;new_links=0;target_soups={}
for path,sha in M['patch_sources'].items():
    payload=old[M['vi_release_commit']+':'+path]
    check(digest(payload)==sha,path+': pinned original patch data')
    for p in json.loads(payload):
        before=p['old'].replace('\r\n','\n');after=p['new'].replace('\r\n','\n')
        check(expected[p['file']].count(before)==1,p['file']+': unique old span')
        check((text(before),text(after)) in pairs[p['file']],p['file']+': full changed span documented in CSV')
        expected[p['file']]=expected[p['file']].replace(before,after,1);span_count+=1
        a,b=BeautifulSoup(before,'lxml'),BeautifulSoup(after,'lxml')
        links=lambda s:collections.Counter(n['href'] for n in s.select('a[href]'))
        for href,count in (links(b)-links(a)).items():
            u=urlsplit(urljoin('https://apocalypsecloset.com/'+p['file'],href))
            check(u.netloc=='apocalypsecloset.com',p['file']+': new link must be internal '+href)
            target=unquote(u.path).lstrip('/') or 'index.html'
            if target.endswith('/'):target+='index.html'
            exists=(ROOT/target).is_file();check(exists,p['file']+': missing target '+href)
            if exists and target.endswith('.html'):
                if target not in target_soups:target_soups[target]=BeautifulSoup((ROOT/target).read_text(encoding='utf-8'),'lxml')
                check(not target_soups[target].select_one('meta[http-equiv="refresh" i]'),p['file']+': redirect target '+href)
                if u.fragment:check(target_soups[target].find(id=unquote(u.fragment)) is not None,p['file']+': missing fragment '+href)
            new_links+=count

protected=['title','h1','meta','link[rel=canonical]','link[hreflang]',
           'script[type="application/ld+json"]','.toc','#toc','.article-toc',
           '.ac-reading-path','.seo-faq','.ac-sources']
modified=added=extra_images=extra_headings=0
for path,row in M['files'].items():
    raw=(ROOT/path).read_bytes();actual=raw.decode('utf-8').replace('\r\n','\n');current=batch40_previous(path,actual)
    check(approved_file_bytes(path,raw),path+': exact successor file SHA-256')
    check(digest(current)==row['after_sha256'],path+': exact successor text SHA-256')
    check(historical(path,actual+' ')==actual+' ',path+': unknown trailing-byte mutation rejected')
    check(not added_successor(path,actual+' '),path+': unknown new-file mutation rejected')
    if path=='blog.html':
        before=BeautifulSoup(old[M['baseline']+':'+path],'lxml');after=BeautifulSoup(current,'lxml')
        oldcards={a['href']:str(a) for a in before.select('#post-grid a.post-card')}
        newcards={a['href']:str(a) for a in after.select('#post-grid a.post-card')}
        wanted={'/'+p for p,r in M['files'].items() if r['kind']=='added'}
        check(set(newcards)-set(oldcards)==wanted and len(newcards)==427 and len(oldcards)==423,'Exactly four approved VI Journal cards')
        check(all(newcards.get(k)==v for k,v in oldcards.items()),'Every original Journal card remains intact')
        continue
    check(current==expected[path],path+': no edits outside exact logged spans')
    before=BeautifulSoup(initial[path],'lxml');after=BeautifulSoup(current,'lxml')
    for sel in protected:
        check([str(n) for n in before.select(sel)]==[str(n) for n in after.select(sel)],path+': original protected '+sel)
    for sel in ['img','h2','h3','h4']:
        b=[str(n) for n in before.select(sel)];a=[str(n) for n in after.select(sel)]
        check(sequence(b,a),path+': original '+sel+' nodes and order unchanged')
        extras=collections.Counter(a)-collections.Counter(b)
        for node,num in extras.items():
            check(sum(str(n)==node and n.find_parent('a',class_='hub-card') is not None for n in after.select(sel))>=num,
                  path+': added image/heading only in logged navigation cards')
        if sel=='img':extra_images+=sum(extras.values())
        else:extra_headings+=sum(extras.values())
    if row['kind']=='modified':
        modified+=1;check(digest(initial[path])==row['before_sha256'],path+': original hash retained')
        check(historical(path,current)==initial[path],path+': exact historical successor recognized')
    else:added+=1;check(added_successor(path,current),path+': exact added-hub contract')

# Sitemap must list the real card images, each backed by the existing asset map.
entries={n.find('{*}loc').text:n for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url')}
assets={r['url']:r for r in json.loads((ROOT/'docs/image-seo-2026-11-15/assets-qa.json').read_text(encoding='utf-8'))}
ns='{http://www.google.com/schemas/sitemap-image/1.1}'
for repair in M['image_sitemap_repairs']:
    actual=[n.find(ns+'loc').text for n in entries['https://apocalypsecloset.com/'+repair['file']].findall(ns+'image')]
    check(actual==repair['images'],repair['file']+': exact image sitemap successor')
    for url,sha in repair['asset_map_sha256'].items():
        check(url in assets and assets[url]['status']==200 and assets[url]['sha256']==sha,repair['file']+': existing image evidence '+url)

# Crucially, no normalization is inserted into the translation-source call chain.
# Original source locks, TSVs and EN HTML remain frozen until explicit E3 approval.
assert M['en_source_successors']=={},'E0b must not release translation-source successors'
names=git('ls-tree','-r','--name-only',M['vi_release_commit'],'--','data/en-translations','en/blog').decode().splitlines()
history=git('ls-tree','-r','--name-only',M['vi_release_commit'],'--','docs').decode().splitlines()
history=[p for p in history if p.endswith('/reviewed-html.json') or p.endswith('/source-hashes.json')]
names+=history
freeze=blobs([M['vi_release_commit']+':'+p for p in names])
for p in names:check((ROOT/p).read_text(encoding='utf-8')==freeze[M['vi_release_commit']+':'+p],p+': EN/TSV/manifest frozen before E3')
check(not git('diff','--name-only',M['vi_release_commit'],'--','docs/qa').strip(),'Existing docs/qa evidence unchanged')
from privacy_release import original as translation_original
source_mismatches=0;source_count=0
for p in sorted((ROOT/'data/en-translations').glob('batch*.json')):
    if p.stem in ['batch05b','batch40']:continue # E2 has a separate new-source contract, never re-baselines an old batch.
    for c in json.loads(p.read_text(encoding='utf-8')):
        path='blog/'+c['vi_slug']+'.html'
        raw=translation_original(path,(ROOT/path).read_text(encoding='utf-8'))
        raw=re.sub(r'<!-- AC-EN-BATCH[0-9]{2}-START -->.*?<!-- AC-EN-BATCH[0-9]{2}-END -->','',raw,flags=re.S)
        source_count+=1;source_mismatches+=digest(raw)!=c['source_sha256']
check((source_count,source_mismatches)==(215,210),'Translation source locks must still reject the 210 unreleased VI successors')

report=dict(modified_vi_articles=modified,new_vi_hubs=added,exact_logged_spans=span_count,
            new_or_replaced_internal_link_occurrences_checked=new_links,original_protected_nodes_unchanged=True,
            added_navigation_card_images=extra_images,added_navigation_card_headings=extra_headings,
            source_hash_entries=source_count,unreleased_source_hash_mismatches=source_mismatches,
            historical_hashes_unchanged=True,errors=errors)
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
