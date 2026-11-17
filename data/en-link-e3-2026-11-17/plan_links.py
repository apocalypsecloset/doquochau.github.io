"""Freeze real EN/VI paragraphs for individual editorial review; never generate sentences."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
import internal_link_audit_en as A
rows=json.loads((D/'inventory.json').read_text(encoding='utf-8'))
by={r['en']:r for r in rows};reverse={r['en']:r['vi'] for r in rows if r['vi']}
soups={};paragraphs={}
vis=A.parse(str(ROOT),'blog');vprose,_=A.extract(vis,['article.article-content'])
protected=A.MODULES|{'seo-faq','faq-section','ac-blog-app-box'}
for r in rows:
 p=r['en'];raw=(ROOT/p).read_bytes().decode('utf-8');s=BeautifulSoup(raw,'html.parser');soups[p]=s
 art=s.select_one('article.editorial') or s.select_one('main.en-hub') or s.article or s.main
 starts=[0]
 for m in re.finditer('\n',raw):starts.append(m.end())
 items=[]
 headings={id(h):i for i,h in enumerate(art.select('h2,h3'))}
 for i,node in enumerate(art.select('p')):
  ancestors=[node,*node.parents];classes={c for n in ancestors if getattr(n,'attrs',None) for c in n.get('class',[])}
  txt=node.get_text(' ',strip=True)
  if classes&protected or node.find_parent(['a','blockquote','table','figure']) or node.find('img') or len(txt.split())<18 or A.BAD.search(txt):continue
  start=starts[node.sourceline-1]+node.sourcepos;end=raw.index('</p>',start)+4
  old=raw[start:end];assert old.startswith('<p') and raw.count(old)==1,(p,i)
  heading=node.find_previous(['h2','h3']);items.append(dict(index=i,old=old,text=txt,heading=heading.get_text(' ',strip=True) if heading else '',heading_id=heading.get('id','') if heading else '',heading_ordinal=headings.get(id(heading),-1)))
 assert items,p
 paragraphs[p]=items
(D/'paragraphs.json').write_text(json.dumps(paragraphs,ensure_ascii=False,indent=2),encoding='utf-8')

stops=set('what how the a an to for of and with in is are by guide guides outfit outfits women womens style clothing fashion'.split())
plan=[]
for r in rows:
 if r['hub']:continue
 for target in r['missing']:
  title=soups[target].h1.get_text(' ',strip=True)
  tokens={t for t in re.findall(r'[a-z]+',title.lower()) if t not in stops and len(t)>2}
  ps=paragraphs[r['en']];length=max(p['index'] for p in ps)+1
  vctx='';va='';vheading_id='';vheading_ordinal=-1
  if r['vi']:
   hit=next(((tx,ctx) for t,tx,ctx,hl in vprose[r['vi']] if t==reverse.get(target)),None)
   if hit:
    va,vctx=hit;vs=vis[r['vi']]
    node=next((n for n in vs.select('p,li,td,blockquote,figcaption') if n.get_text(' ',strip=True)==vctx),None)
    if node:
     h=node.find_previous(['h2','h3']);vheading_id=h.get('id','') if h else ''
     vb=vs.select_one('article.article-content') or vs.main
     hs={id(x):i for i,x in enumerate(vb.select('h2,h3'))};vheading_ordinal=hs.get(id(h),-1)
  matching=[p for p in ps if (vheading_id and p['heading_id']==vheading_id) or (not vheading_id and vheading_ordinal>=0 and p['heading_ordinal']==vheading_ordinal)]
  if matching:ps=matching
  def score(p):
   words=set(re.findall(r'[a-z]+',p['text'].lower()));ratio=p['index']/length
   return 3*len(words&tokens)+(2 if .18<=ratio<=.8 else 0)-abs(ratio-.48)
  chosen=max(ps,key=score)
  plan.append(dict(id=len(plan),source=r['en'],target=target,target_title=title,paragraph=chosen['index'],vi_context=vctx,vi_anchor=va))

# The two English-only originals keep distinct intents and receive their own contextual routes.
special=[
 ('goth-vs-grunge-style','how-to-style-gothic-graphic-tees',7),
 ('goth-vs-grunge-style','grunge-outfits-women-layering',6),
 ('how-to-style-gothic-graphic-tees','goth-vs-grunge-style',7),
 ('how-to-style-gothic-graphic-tees','alternative-t-shirt-outfits-women',3),
]
for source,target,index in special:
 p='en/blog/'+source+'.html';t='en/blog/'+target+'.html';assert any(x['index']==index for x in paragraphs[p])
 plan.append(dict(id=len(plan),source=p,target=t,target_title=soups[t].h1.get_text(' ',strip=True),paragraph=index,vi_context='English-only original; no VI source pair.',vi_anchor=''))
(D/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Planned links',len(plan),'files',len({p['source'] for p in plan}),'max additions',max(collections.Counter(p['source'] for p in plan).values()))
review=[]
for p in plan:
 para=next(x for x in paragraphs[p['source']] if x['index']==p['paragraph'])
 review.append(f"ID {p['id']} | {p['source']} -> {p['target']} | paragraph {p['paragraph']}\nTARGET: {p['target_title']}\nEN: {para['old']}\nVI: {p['vi_context']}\n")
(D/'review.txt').write_text('\n'.join(review),encoding='utf-8')
