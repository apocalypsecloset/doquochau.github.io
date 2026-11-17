"""Exact VI link-fix successors for historical QA only, never translation sources."""
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / 'docs/link-fix-2026-11-17/release-manifest.json'
BATCH40 = ROOT / 'docs/link-fix-2026-11-17/batch40-release.json'

def digest(raw):
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

@lru_cache(maxsize=1)
def manifest():
    return json.loads(RELEASE.read_text(encoding='utf-8'))

@lru_cache(maxsize=None)
def git_text(ref, path):
    return subprocess.check_output(['git', 'show', ref + ':' + path], cwd=ROOT).decode('utf-8').replace('\r\n', '\n')

@lru_cache(maxsize=1)
def batch40_manifest():
    return json.loads(BATCH40.read_text(encoding='utf-8')) if BATCH40.exists() else None

def batch40_previous(path, raw):
    """Only the E2 head/Journal successors; never used by translation sources."""
    release=batch40_manifest()
    row=release['files'].get(path) if release else None
    if not row or row['kind']!='modified' or digest(raw)!=row['after_sha256']:return raw
    before=git_text(release['baseline'],path)
    assert digest(before)==row['before_sha256'],path
    return before

def approved_file_bytes(path, raw):
    release=batch40_manifest()
    row=(release['files'].get(path) if release else None) or manifest()['files'].get(path)
    return bool(row and hashlib.sha256(raw).hexdigest() in [row['after_sha256'],row['after_crlf_sha256']])

def hub_contract(path, raw):
    """Exact E2 full-directory successor of its fully translated source-parity DOM."""
    release=batch40_manifest()
    row=release['files'].get(path) if release else None
    if not row or row['kind']!='added' or digest(raw)!=row['after_sha256']:return raw
    snapshots=json.loads((ROOT/release['parity_snapshots']).read_text(encoding='utf-8'))
    result=snapshots[path]
    assert digest(result)==release['parity_sha256'][path],path
    return result

def hub_publication_rows():
    release=batch40_manifest()
    if not release:return []
    return release['pairs']

def historical(path, raw):
    """Recognize only a pinned existing-file successor; reject all unknown bytes."""
    raw = batch40_previous(path,raw)
    row = manifest()['files'].get(path)
    if not row or row['kind'] != 'modified' or digest(raw) != row['after_sha256']:
        return raw
    before = git_text(manifest()['baseline'], path)
    assert digest(before) == row['before_sha256'], path
    return before

def added_successor(path, raw):
    """New VI hubs have their own release gate, not a nonexistent old Git blob."""
    release=batch40_manifest()
    new=release['files'].get(path) if release else None
    if new and new['kind']=='added' and digest(raw)==new['after_sha256']:return True
    raw=batch40_previous(path,raw)
    row = manifest()['files'].get(path)
    return bool(row and row['kind'] == 'added' and digest(raw) == row['after_sha256'])

def added_vi_urls():
    """Explicit successor inventory; retains the immutable original pair trackers."""
    urls = set()
    for path, row in manifest()['files'].items():
        if row['kind'] == 'added' and path.startswith('blog/'):
            assert added_successor(path, (ROOT / path).read_text(encoding='utf-8')), path
            urls.add('https://apocalypsecloset.com/' + path)
    assert len(urls) == 4
    return urls
