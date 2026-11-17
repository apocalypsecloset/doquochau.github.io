"""Exact E4-to-E3 successors; immutable earlier releases remain separate."""
import hashlib,json,subprocess
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RELEASE=ROOT/'docs/link-fix-2026-11-17/en-e4-release.json'
def digest(raw):return hashlib.sha256(raw.replace('\r\n','\n').encode('utf-8')).hexdigest()
@lru_cache(maxsize=1)
def manifest():return json.loads(RELEASE.read_text(encoding='utf-8')) if RELEASE.exists() else None
@lru_cache(maxsize=1)
def predecessors():
 m=manifest()
 if not m:return {}
 refs=[m['baseline']+':'+p for p in m['baseline_en_hashes']]
 raw=subprocess.check_output(['git','cat-file','--batch'],input=('\n'.join(refs)+'\n').encode(),cwd=ROOT);result={};offset=0
 for ref in refs:
  end=raw.index(b'\n',offset);header=raw[offset:end].split();assert len(header)==3,(ref,header)
  size=int(header[2]);offset=end+1;result[ref.split(':',1)[1]]=raw[offset:offset+size].decode('utf-8').replace('\r\n','\n');offset+=size+1
 return result
def qualified(path,raw):
 m=manifest();row=m['files'].get(path) if m else None
 if not row or digest(raw)!=row['after_sha256'] or row['before_sha256']==row['after_sha256']:return False
 for table in row['tsvs']:
  p=ROOT/table
  if not p.is_file() or digest(p.read_text(encoding='utf-8'))!=m['tables'][table]['sha256']:return False
 if row['vi_source']:
  p=ROOT/row['vi_source']
  if not p.is_file() or digest(p.read_text(encoding='utf-8'))!=row['vi_source_sha256']:return False
 return bool(row['tsvs'])
def previous(path,raw):
 if not qualified(path,raw):return raw
 before=predecessors()[path];assert digest(before)==manifest()['files'][path]['before_sha256'],path
 return before
