"""Compile individually reviewed prose and navigation into exact old/new replacements."""
import collections, html, json, re
from html.parser import HTMLParser
from pathlib import Path
from bs4 import BeautifulSoup
from internal_link_audit import BAD_PHRASES,GENERIC
from phase3_choices import UP,PARAGRAPH
from phase3_down import DOWN

ROOT=Path(__file__).resolve().parents[1]
inventory=json.loads((ROOT/'tools/phase3_inventory.json').read_text(encoding='utf8'))
assert set(UP)=={r['id'] for r in inventory['up']}
patches=[]

class SentenceBoundary(HTMLParser):
    def __init__(self,raw):
        super().__init__(convert_charrefs=False);self.stack=[];self.boundary=None;self.offsets=[0]
        for line in raw.splitlines(keepends=True):self.offsets.append(self.offsets[-1]+len(line))
        self.feed(raw)
    def handle_starttag(self,tag,attrs):
        if tag not in {'br','img','hr','input','meta','link','wbr'}:self.stack.append(tag)
    def handle_endtag(self,tag):
        if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
    def handle_data(self,data):
        if self.boundary is None and self.stack==['p']:
            m=re.search(r'[.!?](?=\s+\S)',data)
            if m:
                line,col=self.getpos();self.boundary=self.offsets[line-1]+col+m.end()

for r in inventory['up']:
    selected=PARAGRAPH.get(r['id'],r['candidate']);old=r['paragraphs'][selected]['old'];sentence=UP[r['id']]
    soup=BeautifulSoup(sentence,'html.parser');anchors=soup.select('a[href]');assert len(anchors)==1,r['id']
    a=anchors[0];anchor=a.get_text(' ',strip=True)
    assert 2<=len(anchor.split())<=6,(r['id'],anchor)
    assert not GENERIC.match(anchor) and not BAD_PHRASES.search(soup.get_text()),r['id']
    assert a['href'].startswith('/blog/') and (ROOT/a['href'][1:]).is_file(),r['id']
    permitted=inventory['coverage'][r['cluster']]['hubs']
    assert a['href'][6:-5] in permitted,(r['id'],a['href'],permitted)
    boundary=SentenceBoundary(old).boundary
    if boundary is None:
        boundary=old.index('>')+1;new=old[:boundary]+sentence+' '+old[boundary:]
    else:new=old[:boundary]+' '+sentence+old[boundary:]
    assert not BAD_PHRASES.search(BeautifulSoup(new,'html.parser').get_text()),(r['id'],new)
    patches.append(dict(file='blog/'+r['slug']+'.html',old=old,new=new,kind='up',id=r['id'],
        links=[dict(target=a['href'],anchor=anchor)]))

def raw_span(raw,node):
    lines=raw.splitlines(keepends=True);start=sum(len(s) for s in lines[:node.sourceline-1])+node.sourcepos
    if node.name=='section':
        depth=0
        for m in re.finditer(r'</?section\b[^>]*>',raw[start:],re.I):
            depth+=-1 if m[0].startswith('</') else 1
            if depth==0:return start,start+m.end()
        raise ValueError('Unclosed section')
    end=raw.index('</'+node.name+'>',start)+len(node.name)+3
    return start,end

def getmeta(slug):
    s=BeautifulSoup((ROOT/f'blog/{slug}.html').read_bytes(),'lxml')
    return s.title.get_text(),s.select_one('meta[name=description]')['content'],s.select_one('meta[property="og:image"]')['content'],s

def card(slug,fallback):
    title,desc,image,s=getmeta(slug)
    im=s.select_one('meta[property="og:image:alt"]');alt=im['content'] if im else title
    width=s.select_one('meta[property="og:image:width"]');height=s.select_one('meta[property="og:image:height"]')
    width=width['content'] if width else '1080';height=height['content'] if height else '1920'
    e=html.escape
    anchor_style=' style="display:block;min-width:0;text-decoration:none;border:1px solid #343434;padding:12px"' if fallback else ''
    img_style=' style="display:block;width:100%;height:auto"' if fallback else ''
    return f'<a class="hub-card" href="/blog/{slug}.html"{anchor_style}><img src="{e(image,quote=True)}" alt="{e(alt,quote=True)}" width="{width}" height="{height}" loading="lazy" decoding="async"{img_style}><div class="hub-card-body"><h3>{e(title)}</h3><p>{e(desc)}</p></div></a>'

containers=collections.OrderedDict();selected=collections.defaultdict(list)
for c,heading,lead,kids in DOWN:
    selected[c]+=kids;hub=inventory['coverage'][c]['hub'];file='blog/'+hub+'.html'
    raw=(ROOT/file).read_bytes().decode('utf8');s=BeautifulSoup(raw,'html.parser')
    h=s.find(id=heading) or next((h for h in s.find_all('h2') if h.get_text(' ',strip=True)==heading),None)
    assert h is not None,(c,heading)
    art=s.select_one('article.article-content');fallback=art is not None
    if fallback:
        # Insert at the end of this existing topic section, before the next H2.
        candidates=[]
        for n in h.next_siblings:
            if getattr(n,'name',None)=='h2':break
            if getattr(n,'name',None)=='p':candidates.append(n)
        assert candidates,(c,heading)
        container=candidates[-1]
    else:container=h.find_parent('section')
    start,end=raw_span(raw,container);key=(file,start,end)
    if key not in containers:containers[key]=dict(old=raw[start:end],parts=[],links=[],fallback=fallback)
    data=containers[key]
    prose=BeautifulSoup(lead,'html.parser');prose_targets={a['href'][6:-5] for a in prose.select('a[href]')}
    assert prose_targets<=set(kids),(c,prose_targets-set(kids))
    for a in prose.select('a[href]'):
        assert 2<=len(a.get_text().split())<=6,(c,a.get_text())
    cards=[card(k,fallback) for k in kids if k not in prose_targets]
    style=' style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin:20px 0"' if fallback else ''
    data['parts'].append('<div class="hub-copy">'+lead+'</div>'+(f'<div class="hub-grid"{style}>'+''.join(cards)+'</div>' if cards else ''))
    for k in kids:
        anchor=next((a.get_text(' ',strip=True) for a in prose.select('a') if a['href']=='/blog/'+k+'.html'),None) or getmeta(k)[0]
        data['links'].append(dict(target='/blog/'+k+'.html',anchor=anchor))
for c,d in inventory['coverage'].items():
    assert collections.Counter(selected[c])==collections.Counter(d['missing_down']),(c,set(d['missing_down'])-set(selected[c]),set(selected[c])-set(d['missing_down']))
for (file,start,end),data in containers.items():
    addition='\n'+'\n'.join(data['parts'])+'\n';old=data['old']
    if data['fallback']:new=old+addition
    else:
        at=old.rindex('</section>');new=old[:at]+addition+old[at:]
    patches.append(dict(file=file,old=old,new=new,kind='down',links=data['links']))

# This shopping guide already has 12 prose destinations. Keep the text of the
# broad summer-weather reference while making room for the required parent link.
file='blog/mua-sam-alt-fashion.html'
raw=(ROOT/file).read_bytes().decode('utf8')
s=BeautifulSoup(raw,'html.parser')
a=s.find('a',href='../blog/mac-do-den-mua-he-co-nong-khong.html')
old=raw_span(raw,a.find_parent('p'));old=raw[old[0]:old[1]]
anchor='<a href="../blog/mac-do-den-mua-he-co-nong-khong.html">cách mặc đồ đen mùa hè</a>'
assert old.count(anchor)==1
new=old.replace(anchor,'cách mặc đồ đen mùa hè')
patches.append(dict(file=file,old=old,new=new,kind='unwrap',links=[dict(target='/blog/mac-do-den-mua-he-co-nong-khong.html',anchor='cách mặc đồ đen mùa hè')]))
for p in patches:
    raw=(ROOT/p['file']).read_bytes().decode('utf8');assert raw.count(p['old'])==1,(p['file'],'nonunique span')
byfile=collections.defaultdict(list)
for p in patches:byfile[p['file']].append(p)
for file,ps in byfile.items():
    raw=(ROOT/file).read_bytes().decode('utf8')
    spans=sorted((raw.index(p['old']),raw.index(p['old'])+len(p['old'])) for p in ps)
    assert all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),(file,'overlapping replacements')
(ROOT/'tools/phase3_patches.json').write_text(json.dumps(patches,ensure_ascii=False,indent=2),encoding='utf8')
print('Up links:',len(UP),'Down links:',sum(len(p['links']) for p in patches if p['kind']=='down'),'Files:',len(byfile),'Exact spans:',len(patches))
