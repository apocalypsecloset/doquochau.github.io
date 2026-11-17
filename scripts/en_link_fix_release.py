"""Exact, additive E3 successors, bound to current VI, updated TSVs and EN HTML."""
import hashlib,json,subprocess
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RELEASE=ROOT/'docs/link-fix-2026-11-17/en-e3-release.json'
def digest(raw):return hashlib.sha256(raw.replace('\r\n','\n').encode('utf-8')).hexdigest()
@lru_cache(maxsize=1)
def manifest():return json.loads(RELEASE.read_text(encoding='utf-8')) if RELEASE.exists() else None
@lru_cache(maxsize=1)
def predecessors():
 release=manifest()
 if not release:return {}
 refs=[release['baseline']+':'+p for p in release['files']]
 refs += [release['source_baseline']+':'+p for p in release['sources']]
 data=subprocess.check_output(['git','cat-file','--batch'],input=('\n'.join(refs)+'\n').encode(),cwd=ROOT)
 result={};offset=0
 for ref in refs:
  end=data.index(b'\n',offset);header=data[offset:end].split();assert len(header)==3,(ref,header)
  size=int(header[2]);offset=end+1;result[ref]=data[offset:offset+size].decode('utf-8').replace('\r\n','\n');offset+=size+1
 return result
def qualified(path,raw):
 release=manifest();row=release['files'].get(path) if release else None
 if not row or digest(raw)!=row['after_sha256']:return False
 if row['before_sha256']==row['after_sha256']:return False
 for table in row['tsvs']:
  p=ROOT/table
  if not p.is_file() or digest(p.read_text(encoding='utf-8'))!=release['tables'][table]['sha256']:return False
 if row['vi_source']:
  p=ROOT/row['vi_source']
  if not p.is_file() or digest(p.read_text(encoding='utf-8'))!=row['vi_source_sha256']:return False
 return bool(row['tsvs'])
def english_previous(path,raw):
 """Unknown EN, VI or TSV bytes cannot obtain a historical view."""
 if not qualified(path,raw):return raw
 release=manifest();before=predecessors()[release['baseline']+':'+path]
 assert digest(before)==release['files'][path]['before_sha256'],path
 return before
def source_previous(path,raw):
 """Release an old source only after its paired English and TSV update exists."""
 release=manifest();row=release['sources'].get(path) if release else None
 if not row or digest(raw)!=row['after_sha256']:return raw
 en=row['en'];current=(ROOT/en).read_text(encoding='utf-8')
 if not qualified(en,current) or release['files'][en]['vi_source']!=path:return raw
 before=predecessors()[release['source_baseline']+':'+path]
 assert digest(before)==row['before_sha256'],path
 return before
