"""Compile the reviewed phase-four sentences into unique, exact paragraph replacements."""
import collections,copy,json,re
from html.parser import HTMLParser
from pathlib import Path
from bs4 import BeautifulSoup
from phase4_choices import SENTENCES,PARAGRAPH
from internal_link_audit import BAD_PHRASES,GENERIC,HUBS,STYLE_SUBHUBS

ROOT=Path(__file__).resolve().parents[1]
pages=json.loads((ROOT/'tools/phase4_inventory.json').read_text(encoding='utf8'))
plan=json.loads((ROOT/'tools/phase4_plan.json').read_text(encoding='utf8'))
assert set(SENTENCES)=={r['id'] for r in plan}

class Boundary(HTMLParser):
    def __init__(self,raw):
        super().__init__(convert_charrefs=False);self.stack=[];self.at=None;self.offsets=[0]
        for line in raw.splitlines(keepends=True):self.offsets.append(self.offsets[-1]+len(line))
        self.feed(raw)
    def handle_starttag(self,tag,attrs):
        if tag not in {'br','img','hr','input','meta','link','wbr'}:self.stack.append(tag)
    def handle_endtag(self,tag):
        if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
    def handle_data(self,data):
        if self.at is None and self.stack==['p']:
            m=re.search(r'[.!?](?=\s+\S)',data)
            if m:
                line,col=self.getpos();self.at=self.offsets[line-1]+col+m.end()

groups=collections.OrderedDict();new_out={s:set(p['prose_out']) for s,p in pages.items()}
anchor_map={s:set(x) for s,x in json.loads((ROOT/'tools/phase4_anchor_baseline.json').read_text(encoding='utf8')).items()}
counts=collections.Counter((r['target'],r['anchor'].lower()) for p in pages.values() for r in p['prose'])
for r in plan:
    i=r['id'];source=r['source'];target=r['target'];sentence=SENTENCES[i]
    soup=BeautifulSoup(sentence,'html.parser');a=soup.select('a[href]');assert len(a)==1,i;a=a[0]
    anchor=a.get_text(' ',strip=True)
    assert a['href']=='/blog/'+target+'.html',(i,a['href'])
    assert 2<=len(anchor.split())<=6,(i,anchor)
    assert not GENERIC.match(anchor) and not BAD_PHRASES.search(soup.get_text(' ',strip=True)),i
    assert target not in pages[source]['prose_out'],(i,'duplicate target')
    paragraph=PARAGRAPH.get(i,r['paragraph']);p=pages[source]['paragraphs'][paragraph]
    key=(source,paragraph)
    if key not in groups:groups[key]=dict(old=p['old'],sentences=[],links=[])
    groups[key]['sentences'].append(sentence)
    groups[key]['links'].append(dict(target=target,anchor=anchor,id=i))
    new_out[source].add(target);anchor_map.setdefault(target,set()).add(anchor.lower())
    counts['blog/'+target+'.html',anchor.lower()]+=1
    assert counts['blog/'+target+'.html',anchor.lower()]<=5,(i,anchor,'anchor frequency')

patches=[]
for (source,paragraph),g in groups.items():
    old=g['old'];boundary=Boundary(old).at;addition=' '.join(g['sentences'])
    if boundary is None:
        boundary=old.index('>')+1;new=old[:boundary]+addition+' '+old[boundary:]
    else:new=old[:boundary]+' '+addition+old[boundary:]
    assert not BAD_PHRASES.search(BeautifulSoup(new,'html.parser').get_text(' ',strip=True)),source
    raw=(ROOT/f'blog/{source}.html').read_bytes().decode('utf8')
    assert raw.count(old)==1,(source,'nonunique paragraph')
    patches.append(dict(file='blog/'+source+'.html',paragraph=paragraph,old=old,new=new,links=g['links']))
degree=collections.Counter(r['source'] for r in plan)
assert max(degree.values())<=3,degree
assert all(2<=len(ts)<=12 for ts in new_out.values())
inbound=collections.defaultdict(set)
for source,targets in new_out.items():
    for t in targets:inbound[t].add(source)
assert all(inbound[s] for s in pages)
parents=set(HUBS.values())|set(STYLE_SUBHUBS)
assert all(any(t not in parents and pages[t]['cluster']==p['cluster'] for t in new_out[s]) for s,p in pages.items())
missing_variants=[s for s in pages if len(anchor_map.get(s,set()))<3]
assert not missing_variants,missing_variants
(ROOT/'tools/phase4_patches.json').write_text(json.dumps(patches,ensure_ascii=False,indent=2),encoding='utf8')
print('Reviewed links:',len(plan),'Files:',len(degree),'Paragraphs:',len(patches))
print('Simulation PASS: density, new-link budgets, genuine child siblings, incoming links, and three anchor variants.')
