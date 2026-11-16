"""Exact reviewed consent-only successors for historical editorial hash gates."""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='0e12619ad14c7cd373fe9526e8929d07c433fa79'
D=ROOT/'docs/privacy-pod-2026-11-16'
CORE='<script src="/assets/js/privacy-consent.js?v=20261116a"></script>'
POLICIES={'privacy.html','en/privacy.html','terms.html','en/terms.html','shipping.html','en/shipping.html','returns.html','en/returns.html'}
CACHE={}
def migrate(raw):
 def script(m):
  tag=m.group();start=tag[:tag.index('>')+1]
  if re.search(r'src=["\x27]https://[^"\x27]*(?:googletagmanager\.com|google-analytics\.com)',start):return ''
  if re.search(r'gtag\s*\(\s*["\x27](?:config|js)["\x27]',tag):
   assert len(tag)<1400,'Review unexpected mixed application/analytics script'
   return ''
  return tag
 raw=re.sub(r'<script\b[^>]*>[\s\S]*?</script>',script,raw,flags=re.I)
 raw=re.sub(r'(analytics-enhancements\.min\.js)(?:\?v=[\w-]+)?',r'\1?v=20261116privacy',raw)
 raw=re.sub(r'(<head\b[^>]*>)',r'\1\n'+CORE,raw,count=1,flags=re.I)
 return raw

def original(path,raw):
 manifest=D/'reviewed-html.json'
 if not manifest.exists():return raw
 if 'manifest' not in CACHE:CACHE['manifest']=json.loads(manifest.read_text())
 row=CACHE['manifest'].get(path)
 if not row or hashlib.sha256(raw.encode()).hexdigest()!=row['after']:return raw
 if path not in CACHE:CACHE[path]=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True)
 return CACHE[path]
