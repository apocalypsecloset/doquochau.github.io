"""Promote VI references to completed EN counterparts; preserve original-language switches."""
from pathlib import Path
from urllib.parse import urlsplit
import csv,json,re,sys,html
from bs4 import BeautifulSoup,NavigableString
ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='scripts' else Path.cwd()
sys.path.insert(0,str(ROOT/'scripts'))
from en_translate import faq_pairs
mapping={urlsplit(r['vi_url']).path:urlsplit(r['en_url']).path for r in csv.DictReader((ROOT/'data/en-216-keyword-intent-audit.csv').open()) if r['en_url'] and (ROOT/urlsplit(r['en_url']).path.lstrip('/')).is_file()}
apply='--apply' in sys.argv;results=[];skipped=[]
for path in sorted((ROOT/'en/blog').glob('*.html')):
 raw=path.read_text();s=BeautifulSoup(raw,'html.parser');body=s.select_one('main.en-hub') or s.article
 if body is None:continue
 changes=[]
 for a in body.select('a[href]'):
  u=urlsplit(a['href']);old=a['href'];text=a.get_text(' ',strip=True)
  if text=='Read the Vietnamese original' or a.find_parent(class_='hub-locale'):continue
  if u.netloc and u.netloc!='apocalypsecloset.com' or u.path not in mapping:continue
  target=mapping[u.path]
  if target=='/'+str(path.relative_to(ROOT)):continue # Keep every original-language link, including handcrafted initial pages.
  if u.fragment and not BeautifulSoup((ROOT/target.lstrip('/')).read_text(),'html.parser').find(id=u.fragment):
   skipped.append(dict(path=str(path.relative_to(ROOT)),href=old,reason='EN fragment absent; keep VI reference'));continue
  a['href']=target+('?' +u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
  a['hreflang']='en'
  if a.get('lang')=='vi':del a['lang']
  if a.get('title')=='Vietnamese reference':del a['title']
  for n in list(a.descendants):
   if isinstance(n,NavigableString) and str(n).endswith(' (Vietnamese)'):n.replace_with(str(n)[:-13])
  changes.append(dict(old=old,new=a['href'],label=a.get_text(' ',strip=True)))
 if not changes:continue
 schema_updates=[]
 for script in s.select('script[type="application/ld+json"]'):
  data=json.loads(script.string);graph=data.get('@graph',[data]);changed=False
  for node in graph:
   if node.get('@type')=='FAQPage' and s.article is not None:
    pairs=faq_pairs(s.article)
    if pairs:
     node['mainEntity']=[{'@type':'Question','name':q.get_text(' ',strip=True),'acceptedAnswer':{'@type':'Answer','text':ans.get_text(' ',strip=True)}} for q,ans in pairs];changed=True
   if node.get('@type')=='CollectionPage' and s.select_one('main.en-hub'):
    cards=s.select('main.en-hub a.hub-card[href]');items=[{'@type':'ListItem','position':i+1,'name':a.h3.get_text(' ',strip=True),'url':'https://apocalypsecloset.com'+a['href']} for i,a in enumerate(cards) if a.h3]
    node['mainEntity']={'@type':'ItemList','numberOfItems':len(items),'itemListElement':items};changed=True
  if changed:
   original_data=json.loads(script.string)
   if original_data!=data:schema_updates.append((original_data,data))
 # Edit only anchor spans and changed JSON-LD bodies; preserve surrounding source bytes.
 def replace_anchor(match):
  chunk=match.group();a=BeautifulSoup(chunk,'html.parser').a
  if a is None or not a.get('href') or a.get_text(' ',strip=True)=='Read the Vietnamese original':return chunk
  old=a['href'];change=next((c for c in changes if c['old']==old and c['label']==a.get_text(' ',strip=True).removesuffix(' (Vietnamese)')),None)
  if change is None:return chunk
  opening,rest=chunk.split('>',1)
  opening=re.sub(r"(\bhref\s*=\s*)([\"']).*?\2",lambda m:m[1]+m[2]+html.escape(change['new'],quote=True)+m[2],opening,count=1,flags=re.S|re.I)
  opening=re.sub(r"\s+lang\s*=\s*([\"'])vi\1",'',opening,flags=re.I)
  opening=re.sub(r"\s+title\s*=\s*([\"'])Vietnamese reference\1",'',opening,flags=re.I)
  if re.search(r'\bhreflang\s*=',opening,re.I):opening=re.sub(r"(\bhreflang\s*=\s*)([\"']).*?\2",lambda m:m[1]+m[2]+'en'+m[2],opening,count=1,flags=re.S|re.I)
  else:opening+=' hreflang="en"'
  return opening+'>'+rest.replace(' (Vietnamese)','')
 updated=re.sub(r'<a\b[^>]*>.*?</a\s*>',replace_anchor,raw,flags=re.S|re.I)
 def replace_schema(match):
  whole=match.group();opening,rest=whole.split('>',1);body,closing=rest.rsplit('</',1)
  try:original=json.loads(body)
  except json.JSONDecodeError:return whole
  for old,new in schema_updates:
   if original==old:return opening+'>'+json.dumps(new,ensure_ascii=False,indent=2 if '\n' in body.strip() else None)+'</'+closing
  return whole
 updated=re.sub(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script\s*>',replace_schema,updated,flags=re.S|re.I)
 before=BeautifulSoup(raw,'html.parser');after=BeautifulSoup(updated,'html.parser')
 assert after.title.get_text()==before.title.get_text()
 assert [dict(n.attrs) for n in after.select('meta,link,img')]==[dict(n.attrs) for n in before.select('meta,link,img')]
 for tag in ['h1','h2','h3','p','li','table','td','th','details','figcaption']:
  assert len(after.select(tag))==len(before.select(tag)),(path,tag)
 assert before.body.get_text().replace(' (Vietnamese)','')==after.body.get_text().replace(' (Vietnamese)',''),path
 original=[a['href'] for a in before.select('a[href]') if a.get_text(' ',strip=True)=='Read the Vietnamese original'];current=[a['href'] for a in after.select('a[href]') if a.get_text(' ',strip=True)=='Read the Vietnamese original'];assert original==current
 own_vi={vi for vi,en in mapping.items() if en=='/'+str(path.relative_to(ROOT))}
 assert [a['href'] for a in before.select('a[href]') if urlsplit(a['href']).path in own_vi]==[a['href'] for a in after.select('a[href]') if urlsplit(a['href']).path in own_vi],path
 expected=[a['href'] for a in s.select('a[href]')];assert expected==[a['href'] for a in after.select('a[href]')],path
 for script in after.select('script[type="application/ld+json"]'):json.loads(script.string)
 if apply:path.write_text(updated)
 results.append(dict(path=str(path.relative_to(ROOT)),links=changes))

report=dict(applied=apply,pages=len(results),links=sum(len(r['links']) for r in results),changes=results,skipped=skipped)
if '--report' in sys.argv:
 dest=Path(sys.argv[sys.argv.index('--report')+1]);dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:report[k] for k in ['applied','pages','links','skipped']},ensure_ascii=False))
