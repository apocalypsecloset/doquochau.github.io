from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,urlunsplit
import re,json,hashlib,posixpath
R=Path.cwd();D=R/'docs/schema-pod-performance-2026-11-15';report=[];bundles={}
def rewrite(css,path):
 def url(m):
  val=m[2]
  if not val or val.startswith(('/','http:','https:','data:','#','//')):return m[0]
  u=urlsplit(val);new='/'+posixpath.normpath(posixpath.join(str(path.parent),u.path));return 'url('+m[1]+urlunsplit(('', '',new,u.query,u.fragment))+m[1]+')'
 css=re.sub(r'url\(\s*([\"\x27]?)([^\)\"\x27]+)\1\s*\)',url,css);return re.sub(r'@charset\s+[^;]+;','',css,flags=re.I)
for p in [R/'blog.html']+list((R/'blog').glob('*.html'))+list((R/'en/blog').glob('*.html')):
 raw=p.read_text();s=BeautifulSoup(raw,'html.parser');head=s.head
 if not head:continue
 tags=head.select('style,link[rel=stylesheet]')
 if len(tags)<2 or any(n.get('disabled') is not None or n.get('media','all') not in ['all','screen',''] for n in tags):continue
 css=[];sources=[]
 for n in tags:
  if n.name=='style':css.append(n.get_text());sources.append({'inline':hashlib.sha256(n.get_text().encode()).hexdigest()})
  else:
   href=n['href'];f=R/urlsplit(href).path.lstrip('/')
   if not href.startswith('/') or not f.is_file():break
   css.append(rewrite(f.read_text(),f.relative_to(R)));sources.append({'path':f.relative_to(R).as_posix()})
 else:
  joined='\n'.join(css)
  if re.search(r'@import\b',joined):continue
  digest=hashlib.sha256(joined.encode()).hexdigest()[:16];dest='assets/css/compiled/article-'+digest+'.css';(R/dest).parent.mkdir(parents=True,exist_ok=True);(R/dest).write_text(joined);bundles[dest]=sources
  # Regex spans maintain original body bytes, inline cascade order, comments and script content.
  hstart=raw.index('<head');hend=raw.index('</head>');headraw=raw[hstart:hend]
  pattern=r'<style\b[^>]*>[\s\S]*?</style>|<link\b[^>]*>'
  count=[0]
  def strip(m):
   node=BeautifulSoup(m[0],'html.parser').find()
   if node.name=='style' or node.name=='link' and 'stylesheet' in node.get('rel',[]):
    count[0]+=1;return f'<link rel="stylesheet" href="/{dest}">' if count[0]==1 else ''
   return m[0]
  changed=re.sub(pattern,strip,headraw,flags=re.I);assert count[0]==len(tags)
  result=raw[:hstart]+changed+raw[hend:];p.write_text(result);report.append({'page':p.relative_to(R).as_posix(),'before_html_bytes':len(raw.encode()),'after_html_bytes':len(result.encode()),'before_css_requests':len([n for n in tags if n.name=='link']),'after_css_requests':1,'bundle':dest})
if report:(D/'css.json').write_text(json.dumps({'pages':report,'bundles':bundles},indent=2)+'\n')
print('pages',len(report),'bundles',len(bundles))
