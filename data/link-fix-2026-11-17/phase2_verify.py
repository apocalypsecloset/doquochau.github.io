"""Verify new collections, publication registrations, original content, and link limits."""
import collections, csv, json, re, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from bs4 import BeautifulSoup
from internal_link_audit import cluster, HUBS, BAD_PHRASES, GENERIC
from phase2_content import PAGES

ROOT=Path(__file__).resolve().parents[1]
BASELINE='581927e'
BASE='https://apocalypsecloset.com'
newfiles={'blog/'+p['slug']+'.html' for p in PAGES.values()}
changed=subprocess.check_output(['git','diff','--name-only',BASELINE],cwd=ROOT,text=True).splitlines()
allowed={'blog.html','sitemap.xml','search-index.js'}
assert all(f in allowed or f in newfiles or f.startswith('tools/') for f in changed),changed
oldfiles=subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE,'blog'],cwd=ROOT,text=True).splitlines()
assert not (set(changed)&set(oldfiles)),'An existing blog page changed'

soups={p.name:BeautifulSoup(p.read_bytes(),'lxml') for p in (ROOT/'blog').glob('*.html')}
site_soups=list(soups.values())
for path in ROOT.rglob('*.html'):
    rel=path.relative_to(ROOT)
    if rel.parts[0] not in ('blog','tools','.git','node_modules'):
        site_soups.append(BeautifulSoup(path.read_bytes(),'lxml'))
all_titles=collections.Counter(s.title.get_text(' ',strip=True) for s in site_soups if s.title)
all_h1=collections.Counter(s.h1.get_text(' ',strip=True) for s in site_soups if s.h1)
all_desc=collections.Counter(s.select_one('meta[name=description]')['content'] for s in site_soups if s.select_one('meta[name=description]'))
journal=BeautifulSoup((ROOT/'blog.html').read_bytes(),'lxml')
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
assert len(urls)==len(set(urls))
raw_index=(ROOT/'search-index.js').read_text(encoding='utf8')
index=json.loads(raw_index[raw_index.index('['):raw_index.rindex(']')+1])
old_index_raw=subprocess.check_output(['git','show',BASELINE+':search-index.js'],cwd=ROOT).decode('utf8')
old_index=json.loads(old_index_raw[old_index_raw.index('['):old_index_raw.rindex(']')+1])
assert index[4:]==old_index,'Existing search entries changed'
old_journal=BeautifulSoup(subprocess.check_output(['git','show',BASELINE+':blog.html'],cwd=ROOT),'lxml')
assert [str(a) for a in journal.select('#post-grid > a')[4:]]==[str(a) for a in old_journal.select('#post-grid > a')]
for selector in ['title','meta','h1','link[rel=canonical]','script[type="application/ld+json"]']:
    assert [str(x) for x in journal.select(selector)]==[str(x) for x in old_journal.select(selector)],selector
expected_filters={'Fashion Basics','Dress Code Desk','Care Guide','Beauty Guide'}
checks=[]
for c,p in PAGES.items():
    file='blog/'+p['slug']+'.html';s=soups[p['slug']+'.html'];url=BASE+'/'+file
    assert cluster(p['slug'])==c
    assert len(s.select('h1'))==1 and all_h1[s.h1.get_text(' ',strip=True)]==1
    assert all_titles[s.title.get_text(' ',strip=True)]==1
    assert all_desc[s.select_one('meta[name=description]')['content']]==1
    assert len(s.select('link[rel=canonical]'))==1 and s.select_one('link[rel=canonical]')['href']==url
    assert not s.select('link[hreflang]'),'Untranslated collection inherited language alternates'
    assert 'noindex' not in s.select_one('meta[name=robots]')['content']
    text=' '.join(n.get_text(' ',strip=True) for n in s.select('.hub-hero > p,[data-authored-copy]'))
    assert len(text.split())>=1200 and not BAD_PHRASES.search(text)
    ids=[n['id'] for n in s.select('[id]')];assert len(ids)==len(set(ids))
    kids={name[:-5] for name in soups if cluster(name[:-5])==c and name!=p['slug']+'.html'}
    main=s.find('main');targets={a['href'] for a in main.select('a[href]')}
    assert {'/blog/'+k+'.html' for k in kids}<=targets,(c,'child coverage')
    counts=collections.Counter(a['href'] for a in main.select('a[href^="/blog/"]'))
    assert max(counts.values())==1,(c,'duplicate destination')
    for a in main.select('[data-authored-copy] a'):
        anchor=a.get_text(' ',strip=True)
        assert 2<=len(anchor.split())<=6 and not GENERIC.match(anchor),anchor
    for a in s.select('a[href],link[href],script[src]'):
        href=a.get('href',a.get('src'));u=urlsplit(urljoin(url,href))
        if u.netloc in ('apocalypsecloset.com','www.apocalypsecloset.com'):
            dest=u.path.lstrip('/')
            if not dest or u.path.endswith('/'):dest+='index.html'
            if not u.path.startswith('/images/'):
                assert (ROOT/dest).exists(),(file,href)
            if u.fragment and dest==file:assert u.fragment in ids,(file,href)
    graph=json.loads(s.select_one('script[type="application/ld+json"]').string)['@graph']
    collection=next(g for g in graph if g['@type']=='CollectionPage')
    itemlist=collection['mainEntity'];assert itemlist['numberOfItems']==len(kids)
    assert {r['url'] for r in itemlist['itemListElement']}=={BASE+'/blog/'+k+'.html' for k in kids}
    assert next(g for g in graph if g['@type']=='BreadcrumbList')['itemListElement'][-1]['item']==url
    assert urls.count(url)==1
    cards=journal.select('#post-grid > a[href="/'+file+'"]');assert len(cards)==1
    assert cards[0]['data-category'] in expected_filters
    assert cards[0].select_one('.card-title').get_text()==p['title']
    parts=json.loads(cards[0]['data-search-parts']);assert parts==[0,' ',1,' ',2,' ',3]
    assert len([r for r in index if r['url']=='/'+file])==1
    checks.append(dict(cluster=c,words=len(text.split()),children=len(kids),all_children_linked=True,unique_metadata=True,registered=True))
report=dict(original_blog_pages_unchanged=len(oldfiles),new_pages=checks,journal_cards=len(journal.select('#post-grid > a')),existing_search_entries_preserved=len(old_index),sitemap_unique=True)
(ROOT/'tools/phase2_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
