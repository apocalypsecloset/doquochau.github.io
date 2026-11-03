"""Check original and srcset image endpoints without replacing editorial assets."""
from bs4 import BeautifulSoup
from pathlib import Path
import json,subprocess,concurrent.futures,sys
from urllib.parse import urljoin
ROOT=Path(__file__).resolve().parents[1]
configs=json.loads((ROOT/'data/en-translations'/(sys.argv[1]+'.json')).read_text());urls=set()
for c in configs:
 s=BeautifulSoup((ROOT/'en/blog'/f"{c['en_slug']}.html").read_text(),'html.parser')
 for img in s.select('img'):
  if not img['src'].startswith('data:'):urls.add(urljoin('https://apocalypsecloset.com/',img['src']))
  for v in img.get('srcset','').split(','):
   if v.strip():urls.add(urljoin('https://apocalypsecloset.com/',v.strip().split()[0]))
def check(url):
 p=subprocess.run(['curl','-sS','-I','-L','--max-time','25','-o','/dev/null','-w','%{http_code}\t%{content_type}',url],capture_output=True,text=True)
 fields=p.stdout.split('\t');return {'url':url,'status':fields[0] if fields else '', 'type':fields[1] if len(fields)>1 else '', 'error':p.stderr if p.returncode else ''}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,sorted(urls)))
Path(sys.argv[2]).write_text(json.dumps(results,indent=2)+'\n')
failed=[r for r in results if r['status']!='200' or not r['type'].startswith('image/')]
print(len(results),'images;',len(failed),'failed');sys.exit(bool(failed))
