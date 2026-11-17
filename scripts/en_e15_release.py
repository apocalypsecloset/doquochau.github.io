"""Exact E15 successors; old releases and source locks stay immutable."""
import hashlib,json,subprocess
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(raw):return hashlib.sha256(raw.replace('\r\n','\n').encode('utf-8')).hexdigest()
@lru_cache(maxsize=1)
def manifest():return json.loads((ROOT/'docs/link-fix-2026-11-17/en-e15-release.json').read_text(encoding='utf-8'))
@lru_cache(maxsize=None)
def predecessor(path):return subprocess.check_output(['git','show',manifest()['baseline']+':'+path],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
def qualified(path,raw):
 row=manifest()['files'].get(path)
 if not row or digest(raw)!=row['after_sha256'] or row['before_sha256']==row['after_sha256']:return False
 for t in row['tsvs']:
  if not (ROOT/t).is_file() or digest((ROOT/t).read_text(encoding='utf-8'))!=manifest()['tables'][t]['sha256']:return False
 v=row['vi_source']
 if v and (not (ROOT/v).is_file() or digest((ROOT/v).read_text(encoding='utf-8'))!=row['vi_source_sha256']):return False
 return bool(row['tsvs'])
def previous(path,raw):
 if not qualified(path,raw):return raw
 before=predecessor(path);assert digest(before)==manifest()['files'][path]['before_sha256'],path
 return before
def audit_previous(path,raw):
 row=manifest()['audit']
 if path!=row['path'] or digest(raw)!=row['after_sha256']:return raw
 before=predecessor(path);assert digest(before)==row['before_sha256']
 return before
