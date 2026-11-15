"""Apply only visually reviewed, image-specific bilingual alt descriptions."""
import json,re,html,hashlib
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from en_translate import source,VI
from en_translate_hubs import source as hub_source
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'docs/schema-pod-performance-2026-11-15'
rows=json.loads((D/'reviewed-alts.json').read_text());mapping={r['url']:r for r in rows};alt_en={r['vi']:r['en'] for r in rows};saved={};configs=[]
for path in sorted((ROOT/'data/en-translations').glob('batch*.json')):
 cs=json.loads(path.read_text());configs.append((path,cs))
 for c in cs:
  key=c['vi_slug']
  if key in saved:continue
  raw,s,parts,texts=(hub_source if c.get('source_kind')=='hub' else source)(key)
  file=ROOT/'data/en-translations'/f'{key}.tsv';entries={int(k):v for k,v in (l.split('\t',1) for l in file.read_text().splitlines() if l)}
  saved[key]={'translations':{texts[i]:v for i,v in entries.items() if i<len(texts)},'sha':c['source_sha256']}
changes=[]
for p in list((ROOT/'blog').glob('*.html'))+list((ROOT/'en/blog').glob('*.html')):
 rel=p.relative_to(ROOT).as_posix();raw=p.read_text();lang='en' if rel.startswith('en/') else 'vi'
 def replace(m):
  node=BeautifulSoup(m[0],'html.parser').img;src=urljoin('https://apocalypsecloset.com/'+rel,node.get('src',''));row=mapping.get(src)
  if not row or node.get('alt')==row[lang]:return m[0]
  changes.append({'page':rel,'src':src,'before':node.get('alt',''),'after':row[lang]})
  return re.sub(r'alt="[^"]*"','alt="'+html.escape(row[lang],quote=True)+'"',m[0])
 raw=re.sub(r'<img\b[^>]*>',replace,raw)
 s=BeautifulSoup(raw,'html.parser');og=s.select_one('meta[property="og:image"]');row=mapping.get(og['content']) if og else None
 if row:
  for m in list(re.finditer(r'<meta\b[^>]*>',raw)):
   n=BeautifulSoup(m[0],'html.parser').meta
   if n.get('property',n.get('name')) in ['og:image:alt','twitter:image:alt']:raw=raw.replace(m[0],re.sub(r'content="[^"]*"','content="'+html.escape(row[lang],quote=True)+'"',m[0]),1)
 if raw!=p.read_text():p.write_text(raw)
locks=[]
for path,cs in configs:
 for c in cs:
  key=c['vi_slug'];raw,s,parts,texts=(hub_source if c.get('source_kind')=='hub' else source)(key);old=saved[key]['translations'];missing=[];entries=[]
  for i,t in enumerate(texts):
   translated=old.get(t,alt_en.get(t))
   if translated is not None:entries.append(f'{i}\t{translated}')
   elif VI.search(t):missing.append((i,t))
  assert not missing,(key,missing)
  (ROOT/'data/en-translations'/f'{key}.tsv').write_text('\n'.join(entries)+'\n')
  h=hashlib.sha256(raw.encode()).hexdigest();locks.append({'manifest':path.relative_to(ROOT).as_posix(),'vi_slug':key,'before':c['source_sha256'],'after':h});c['source_sha256']=h
  en=ROOT/'en/blog'/f"{c['en_slug']}.html";enraw=en.read_text();enraw=re.sub(r'data-source-sha256="[^"]*"','data-source-sha256="'+h+'"',enraw);en.write_text(enraw)
 path.write_text(json.dumps(cs,ensure_ascii=False,indent=2)+'\n')
(D/'alt-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n');(D/'source-locks.json').write_text(json.dumps(locks,indent=2)+'\n');print(json.dumps({'reviewed_images':len(rows),'changed_alt_occurrences':len(changes),'changed_pages':len({c['page'] for c in changes})},indent=2))
