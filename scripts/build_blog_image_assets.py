"""Download audited origins and build actual, decoded responsive WebP files."""
import sys,argparse,tempfile
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parents[1]
from PIL import Image,ImageOps
from concurrent.futures import ThreadPoolExecutor,as_completed
import urllib.request, json, hashlib,io,time,re

options=argparse.ArgumentParser(description=__doc__)
options.add_argument('--cache',type=Path,default=Path(tempfile.gettempdir())/'ac-blog-image-originals')
args=options.parse_args()
ROOT=BASE_DIR
CACHE=args.cache;CACHE.mkdir(parents=True,exist_ok=True)
DEST=ROOT/'assets/images/blog-responsive';DEST.mkdir(parents=True,exist_ok=True)
DATA=ROOT/'data/blog-image-seo-2026-11-18';DATA.mkdir(parents=True,exist_ok=True)
audited=json.loads((DATA/'assets.json').read_text(encoding='utf8'))
urls=sorted({r['origin'] for r in audited})
known_files={v['url'].split('/')[-1]:v['sha256'] for r in audited for v in r['variants'] if not v['origin']}
known_origins={r['origin']:r['sha256'] for r in audited}
if not all(u.startswith('https://apocalypsecloset.com/images/') and '.webp' in u for u in urls):
 raise SystemExit('Unexpected image origin in the verified manifest')

def make(url):
 key=hashlib.sha256(url.encode()).hexdigest()[:12]
 file=CACHE/(key+'.webp')
 if not file.exists():
  for attempt in range(3):
   try:
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; ImageAudit/1.0)'})
    with urllib.request.urlopen(req,timeout=40) as r:
     if r.status!=200 or 'image/webp' not in r.headers.get('Content-Type',''):raise ValueError('Unexpected image response')
     raw=r.read()
    with Image.open(io.BytesIO(raw)) as im:im.load()
    file.write_bytes(raw);break
   except Exception:
    if attempt==2:raise
 raw=file.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=known_origins[url]:raise ValueError('Origin bytes differ from reviewed image: '+url)
 with Image.open(io.BytesIO(raw)) as original:
  original.load(); im=ImageOps.exif_transpose(original)
  if im.mode not in ('RGB','RGBA'):im=im.convert('RGB')
  width,height=im.size
  meta={k:im.info[k] for k in ('exif','xmp','icc_profile') if im.info.get(k)}
  stem=re.sub('[^a-z0-9-]+','-',url.split('/')[-1].split('?')[0].removesuffix('.webp').lower()).strip('-')
  variants=[]
  largest=min(960,width) if len(raw)>200*1024 else width
  for w in sorted({min(320,width),min(640,width),largest}):
   h=round(height*w/width); cap=(50 if w<=320 else 160 if w<=640 else 200)*1024
   if w==width and len(raw)<=cap:
    variants.append(dict(url=url,width=w,height=h,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),origin=True));continue
   while True:
    name=f'{stem}-{key}-{w}w.webp'; target=DEST/name
    if target.exists():
     data=target.read_bytes()
     if name not in known_files or hashlib.sha256(data).hexdigest()!=known_files[name]:
      raise ValueError('Unexpected existing derivative: '+str(target))
    else:
     image=im if w==width else im.resize((w,h),Image.Resampling.LANCZOS)
     for quality in [82,78,74]:
      buf=io.BytesIO();image.save(buf,format='WEBP',quality=quality,method=6,**meta);data=buf.getvalue()
      if len(data)<=cap:break
    if len(data)<=cap: break
    if w<=640: raise ValueError(f'Compression budget unmet: {url} {w}: {len(data)}')
    w=max(640,int(w*.9));h=round(height*w/width)
   if not target.exists():target.write_bytes(data)
   data=target.read_bytes()
   with Image.open(target) as verified:
    verified.load()
    if verified.size!=(w,h):raise ValueError('Wrong dimensions '+str(target))
   variants.append(dict(url='/assets/images/blog-responsive/'+name,width=w,height=h,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),origin=False))
 return dict(origin=url,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),width=width,height=height,variants=variants,metadata_fields=sorted(meta))

results=[];fail=[];start=time.time()
with ThreadPoolExecutor(max_workers=10) as pool:
 futures={pool.submit(make,u):u for u in urls}
 for future in as_completed(futures):
  try:results.append(future.result())
  except Exception as exc:fail.append(dict(url=futures[future],error=str(exc))); print('FAILED',fail[-1],flush=True)
  if (len(results)+len(fail))%100==0: print(f'Prepared {len(results)}/{len(urls)}, failed {len(fail)}, elapsed {time.time()-start:.0f}s',flush=True)
results.sort(key=lambda r:r['origin'])
(DATA/'assets.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(CACHE/'asset-build-errors.json').write_text(json.dumps(fail,indent=2),encoding='utf8')
print(json.dumps(dict(origins=len(results),failures=len(fail),generated=sum(not v['origin'] for r in results for v in r['variants']),bytes=sum(v['bytes'] for r in results for v in r['variants'] if not v['origin']))),flush=True)
sys.exit(bool(fail))
