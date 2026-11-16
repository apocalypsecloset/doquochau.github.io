from privacy_release import original as privacy_original
"""Verify the authorized schema, image and performance maintenance on real pages."""
import json,re,hashlib,subprocess,sys,collections
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fix_schema_consistency import faq_pairs
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'docs/schema-pod-performance-2026-11-15';BASE='https://apocalypsecloset.com';ORG=BASE+'/#organization';WEB=BASE+'/#website';errors=[];counts=collections.Counter()
reviewed=json.loads((D/'reviewed-html.json').read_text());altrows=json.loads((D/'reviewed-alts.json').read_text());alts={r['url']:r for r in altrows};changes=json.loads((D/'alt-changes.json').read_text())
def check(ok,msg):
 if not ok:errors.append(msg)
def nodes(obj):
 if isinstance(obj,dict):
  yield obj
  for v in obj.values():yield from nodes(v)
 elif isinstance(obj,list):
  for v in obj:yield from nodes(v)
def types(n):return n.get('@type',[]) if isinstance(n.get('@type'),list) else [n.get('@type')]
for p in sorted(ROOT.rglob('*.html')):
 if '.git' in p.parts:continue
 rel=p.relative_to(ROOT).as_posix();raw=p.read_text();s=BeautifulSoup(raw,'html.parser');can=s.select_one('link[rel=canonical]');meta=s.select_one('meta[name=description]');
 if not can or not meta or not s.h1:continue
 url=can['href'];lang=s.html.get('lang','').split('-')[0];description=meta['content'];headline=s.h1.get_text(' ',strip=True);allnodes=[]
 for tag in s.select('script[type="application/ld+json"]'):allnodes+=list(nodes(json.loads(tag.get_text())))
 for n in allnodes:
  if any(x in ['Article','BlogPosting'] for x in types(n)):
   check(n.get('headline')==headline,rel+': headline/H1');check(n.get('description')==description,rel+': schema/meta description');check(n.get('inLanguage')==lang,rel+': article language');check(n.get('url')==url,rel+': article URL');counts['articles']+=1
 for tag in s.select('meta[property="og:description"],meta[name="twitter:description"]'):check(tag['content']==description,rel+': social description')
 orgs=[n for n in allnodes if n.get('@id')==ORG and 'Organization' in types(n)];check(len(orgs)==1,rel+': exactly one Organization definition')
 sites=[n for n in allnodes if n.get('@id')==WEB and 'WebSite' in types(n)];check(len(sites)==1 and sites[0].get('inLanguage')==['vi','en'],rel+': bilingual WebSite')
 for n in allnodes:
  if n.get('@type')=='BreadcrumbList':
   last=n['itemListElement'][-1]['item'];check((last.get('@id') if isinstance(last,dict) else last)==url,rel+': breadcrumb URL')
 pairs=faq_pairs(s);faqs=[n for n in allnodes if n.get('@type')=='FAQPage']
 if pairs:
  check(len(faqs)==1,rel+': one FAQ schema for visible FAQ')
  if faqs:
   actual=[(q['name'],q['acceptedAnswer']['text']) for q in faqs[0]['mainEntity']];check(actual==pairs,rel+': exact visible FAQ parity');counts['faq_pages']+=1
 for im in s.select('img[src]'):
  src=urljoin(url,im['src']);row=alts.get(src)
  if row:check(im.get('alt')==row['en' if lang=='en' else 'vi'],rel+': reviewed image alt '+src);counts['reviewed_alt_occurrences']+=1
 if rel in reviewed:
  check(hashlib.sha256(privacy_original(rel,raw).encode()).hexdigest()==reviewed[rel]['after'],rel+': reviewed HTML changed')
  old=BeautifulSoup(subprocess.check_output(['git','show','22b72f2:'+rel],cwd=ROOT,text=True),'html.parser')
  for selector,attr in [('link[rel=canonical]','href'),('meta[name=robots]','content')]:check([n.get(attr) for n in s.select(selector)]==[n.get(attr) for n in old.select(selector)],rel+': original '+selector)
  check(s.title.get_text()==old.title.get_text(),rel+': original title');check(headline==old.h1.get_text(' ',strip=True),rel+': original H1')
  if rel not in ['index.html','about.html','en/about.html','privacy.html','en/privacy.html'] and s.main and old.main:check(s.main.get_text(' ',strip=True)==old.main.get_text(' ',strip=True),rel+': main visible text preserved')
 counts['pages']+=1
check(len(altrows)==871,'All 871 reviewed assets represented');check(len(changes)==1742,'Expected bilingual reviewed alt placements')
for row in altrows:check(row['width']>0 and row['height']>0 and len(row['sha256'])==64,'Reviewed image decode evidence '+row['url'])
css=json.loads((D/'css.json').read_text())
for bundle,inputs in css['bundles'].items():
 check((ROOT/bundle).is_file(),'Missing compiled CSS '+bundle)
 # The compilation records every original source in cascade order, retaining source files.
 for item in inputs:
  if 'path'in item:check((ROOT/item['path']).is_file(),'Missing CSS source '+item['path'])
headers=(ROOT/'_headers').read_text()
for h in ['Strict-Transport-Security','X-Content-Type-Options: nosniff','Referrer-Policy: strict-origin-when-cross-origin','Permissions-Policy','Content-Security-Policy-Report-Only']:check(h in headers,'Missing '+h)
check('\n  Content-Security-Policy:' not in headers,'Unreviewed enforcing CSP')
report={'counts':dict(counts),'reviewed_assets':len(altrows),'reviewed_html':len(reviewed),'compiled_css_pages':len(css['pages']),'errors':errors};print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
