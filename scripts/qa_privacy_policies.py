"""Check the real consent migration, unchanged editorial bytes and policy parity."""
from storefront_ux_release import original as ux_original
import hashlib,json,re,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup
from privacy_release import ROOT,BASE,D,migrate,POLICIES,CORE
errors=[];review=json.loads((D/'reviewed-html.json').read_text());content=json.loads((D/'content.json').read_text());count=0
for p in ROOT.rglob('*.html'):
 if '.git' in p.parts:continue
 rel=p.relative_to(ROOT).as_posix();raw=p.read_text();s=BeautifulSoup(raw,'html.parser');count+=1
 if rel!='google209e25d9de6b2414.html' and raw.count(CORE)!=1:errors.append(rel+': early consent bootstrap count')
 if s.select('script[src*="googletagmanager.com"],script[src*="google-analytics.com"]'):errors.append(rel+': unconditional Google script')
 for t in s.find_all('script'):
  if re.search(r'gtag\s*\(\s*["\x27](?:config|js)["\x27]',t.get_text()):errors.append(rel+': legacy inline Google initializer')
 if rel in review:
  raw=ux_original(rel,raw)
  old=subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT,text=True);o=BeautifulSoup(old,'html.parser')
  if hashlib.sha256(raw.encode()).hexdigest()!=review[rel]['after']:errors.append(rel+': reviewed bytes changed')
  if hashlib.sha256(old.encode()).hexdigest()!=review[rel]['before']:errors.append(rel+': baseline lock')
  for sel,attr in [('title',None),('h1',None),('link[rel=canonical]','href'),('meta[name=description]','content'),('meta[name=robots]','content')]:
   values=lambda x:[n.get(attr) if attr else n.get_text(' ',strip=True) for n in x.select(sel)]
   if values(s)!=values(o):errors.append(rel+': original SEO changed '+sel)
  if rel not in ['privacy.html','en/privacy.html']:
   expected=migrate(old)
   if rel=='index.html':expected=expected.replace('<li><a href="/en/privacy.html">Privacy policy</a></li>','<li><a href="/en/privacy.html">Privacy policy</a></li>\n<li><a href="/en/terms.html">Terms</a></li><li><a href="/en/shipping.html">Shipping</a></li><li><a href="/en/returns.html">Returns &amp; refunds</a></li>',1)
   if rel=='index.html':expected=expected.replace('<div id="ac-product-information" class="ac-product-information" aria-live="polite"></div>','<div id="ac-product-information" class="ac-product-information" aria-live="polite"></div>\n<p id="ac-pod-policy-note">The standard made-to-order return policy does not limit mandatory consumer rights. Read <a href="/en/returns.html">Returns &amp; refunds</a> and <a href="/en/shipping.html">Shipping</a> before ordering.</p>',1)
   if raw!=expected:errors.append(rel+': change beyond exact consent migration')
 if rel in POLICIES:
  lang='en' if rel.startswith('en/') else 'vi';key=p.stem;sections=content['privacy'] if key=='privacy' else content['policies'][key]['sections']
  actual=s.select('[data-policy-section]')
  if [n['data-policy-section'] for n in actual]!=[n['id'] for n in sections]:errors.append(rel+': policy section parity')
  for n,c in zip(actual,sections):
   expected=BeautifulSoup(c[lang][1],'html.parser').get_text(' ',strip=True)
   if n.p.get_text(' ',strip=True)!=expected:errors.append(rel+': policy content differs from bilingual source '+c['id'])
  for prefix in ['/','/en/']:
   if not s.select_one('link[hreflang="'+('en' if prefix=='/en/' else 'vi')+'"][href="https://apocalypsecloset.com'+prefix+key+'.html"]'):errors.append(rel+': reciprocal alternate')
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
for p in POLICIES:
 if 'https://apocalypsecloset.com/'+p not in urls:errors.append(p+': sitemap')
print(json.dumps({'html_checked':count,'existing_hash_locks':len(review),'bilingual_policy_pages':len(POLICIES),'errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
