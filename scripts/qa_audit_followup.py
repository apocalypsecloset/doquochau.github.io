"""Check audit fixes against the exact pre-maintenance publication."""
import re,json,subprocess,sys,html
from pathlib import Path
from bs4 import BeautifulSoup
from audit_metadata import approved
ROOT=Path(__file__).resolve().parents[1];BASELINE='490cb5f';D=ROOT/'docs/audit-followup-2026-11-15';errors=[];checked=0
before=json.loads((D/'before.json').read_text());duplicates={r['page']:r['image'] for r in json.loads((D/'duplicate-images.json').read_text())}
paths=set(subprocess.check_output(['git','diff','--name-only',BASELINE],cwd=ROOT,text=True).splitlines())
def body(raw,path,old=False):
 raw=raw[raw.index('<body'):]
 raw=re.sub(r'<script\b[^>]*\bsrc=[\"\x27]https://static\.cloudflareinsights\.com/[^>]*></script>','',raw,flags=re.I)
 raw=raw.replace('href="/en/"','href="/"').replace('https://twitter.com/intent/tweet','https://x.com/intent/post')
 raw=re.sub(r'<span class="dot"></span><span class="ac-publication-date">[\s\S]*?</time></span>','',raw)
 raw=re.sub(r'<figure class="article-figure ac-audit-cover">[\s\S]*?</figure>','',raw)
 if old and path in duplicates:
  matches=[m for m in re.finditer(r'<img\b[^>]*>',raw) if BeautifulSoup(m.group(),'html.parser').img.get('src')==duplicates[path]]
  assert len(matches)==2,path
  m=matches[-1];raw=raw[:m.start()]+raw[m.end():]
 return raw
for path in sorted(paths):
 if not path.endswith('.html'):continue
 raw=(ROOT/path).read_text();old=subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT,text=True);s=BeautifulSoup(raw,'html.parser');o=BeautifulSoup(old,'html.parser')
 if body(raw,path)!=body(old,path,True):errors.append(path+': body changed outside exact permitted repairs')
 for selector,attr in [('link[rel=canonical]','href'),('meta[name=robots]','content')]:
  if [n.get(attr) for n in s.select(selector)]!=[n.get(attr) for n in o.select(selector)]:errors.append(path+': changed '+selector)
 for selector,field,attr in [('title','title',None),('meta[name=description]','description','content')]:
  a=[n.get(attr) if attr else n.get_text() for n in s.select(selector)];expected=[approved(path,field,n.get(attr) if attr else n.get_text()) for n in o.select(selector)]
  if a!=expected:errors.append(path+': unapproved '+field)
 if s.html.get('lang')!=o.html.get('lang'):errors.append(path+': page language')
 if path.startswith('en/') and len(s.title.get_text())>65:errors.append(path+': long title remains')
 if path.startswith('en/blog/') and len(s.select_one('meta[name=description]')['content'])>165:errors.append(path+': long description remains')
 if 'static.cloudflareinsights.com/' in raw or 'href="/en/"' in raw or 'https://twitter.com/intent/tweet' in raw:errors.append(path+': old mechanical issue')
 if path.startswith(('blog/','en/blog/')):
  nodes=[]
  for tag in s.select('script[type="application/ld+json"]'):
   j=json.loads(tag.get_text());nodes+=j.get('@graph',[j])
  for n in nodes:
   if n.get('@type') in ['BlogPosting','Article'] and (not n.get('datePublished') or not n.get('dateModified')):errors.append(path+': missing article date')
  # Every newly added FAQ must be an exact copy of visible questions and answers.
  added=s.select('script[type="application/ld+json"]')
  if '"FAQPage"' not in old:
   faq=next((n for n in nodes if n.get('@type')=='FAQPage'),None)
   if faq:
    pairs=[]
    for section in s.select('.seo-faq'):
     for detail in section.select('details'):
      if detail.summary and detail.p:pairs.append((detail.summary.get_text(' ',strip=True),detail.p.get_text(' ',strip=True)))
     if not section.select('details'):
      for q in section.select('h3'):
       a=q.find_next_sibling('p')
       if a:pairs.append((q.get_text(' ',strip=True),a.get_text(' ',strip=True)))
    actual=[(q['name'],q['acceptedAnswer']['text']) for q in faq['mainEntity']]
    if actual!=pairs:errors.append(path+': FAQ visible/schema mismatch')
 checked+=1
print(json.dumps({'baseline':BASELINE,'html_checked':checked,'errors':errors},indent=2));sys.exit(bool(errors))
