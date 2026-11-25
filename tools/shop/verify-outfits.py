from pathlib import Path
import json,re,subprocess
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT.parent/'seo-reports/fixes-20261125'
notes=json.loads(Path(__file__).with_name('outfit-notes.json').read_text(encoding='utf-8'))
def parse(text):
    soup=BeautifulSoup(text,'lxml')
    primary=soup.select_one('main')
    for x in primary.select('script,style,noscript,nav,footer,header,form,aside,.toc,.table-of-contents'):x.decompose()
    words=re.findall(r'\w+',primary.get_text(' ',strip=True).lower())
    shingles={' '.join(words[i:i+5]) for i in range(max(0,len(words)-4))}
    return soup,shingles
sets={}
for file in sorted((ROOT/'outfits').glob('*.html')):
    source=file.read_text(encoding='utf-8');soup,shingles=parse(source);sets[file.stem]=shingles
    if file.stem not in notes:continue
    assert len(soup.select('.outfit-styling-notes'))==1
    assert soup.select_one('#outfit-styling-title').get_text()==notes[file.stem]['heading']
    old=subprocess.check_output(['git','show','origin/master:outfits/'+file.name],cwd=ROOT).decode('utf-8')
    before=BeautifulSoup(old,'lxml')
    for selector in ['title','h1','meta[name="description"]','link[rel="canonical"]']:
        assert str(soup.select_one(selector))==str(before.select_one(selector)),(file.name,selector)
    assert [a.get('href') for a in soup.select('.items-list a')]==[a.get('href') for a in before.select('.items-list a')]
    assert [i.get('src') for i in soup.select('.slider-track img')]==[i.get('src') for i in before.select('.slider-track img')]
    for script in soup.select('script[type="application/ld+json"]'):json.loads(script.string)
pairs=[];slugs=list(sets)
for i,a in enumerate(slugs):
    for b in slugs[i+1:]:
        union=sets[a]|sets[b];j=len(sets[a]&sets[b])/len(union) if union else 0
        if j>=.8:pairs.append({'a':a,'b':b,'jaccard':round(j,4)})
assert not pairs,pairs
output={'passed':True,'outfit_pages':len(slugs),'edited_pages':len(notes),'pairs_above_0_8':pairs,'checks':['Metadata, canonical, H1, item links and gallery image sources retained','JSON-LD parses','136-page main-text 5-token similarity check below 0.8 for every pair; heuristic only']}
(OUT/'outfit-verification.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS:',len(notes),'edited pages;',len(slugs),'outfits; no pairs >= 0.8; metadata/images/item links retained')
