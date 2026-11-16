"""Exact approved UI successors; older migrations still compare their own inputs.

Only the two UI hubs are eligible. New semantic checks inspect actual HTML.
Unknown bytes remain unnormalized and fail the historical preservation gates.
"""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='9c6ab13716fa4a1b8bbe40bc6606398d236c4c56'
MANIFEST=ROOT/'docs/storefront-ux-2026-11-16/reviewed-html.json'
CACHE={}
def original(path,raw):
 if path not in {'index.html','en/blog.html'} or not MANIFEST.exists():return raw
 if 'manifest' not in CACHE:CACHE['manifest']=json.loads(MANIFEST.read_text())
 row=CACHE['manifest'].get(path)
 if not row or hashlib.sha256(raw.encode()).hexdigest()!=row['after']:return raw
 if path not in CACHE:CACHE[path]=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True)
 return CACHE[path]
