"""Recognize only exact, reviewed successor bytes for earlier preservation gates.

New semantic/image/content checks still inspect the actual current pages. Unknown
changes do not receive this historical-baseline normalization.
"""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE='22b72f2c41d301ca56de7e133a618231dd2f1e46'
p=ROOT/'docs/schema-pod-performance-2026-11-15/reviewed-html.json'
REVIEWED=json.loads(p.read_text()) if p.exists() else {}
CACHE={}
def predecessor(path,raw):
 row=REVIEWED.get(path)
 if not row or hashlib.sha256(raw.encode()).hexdigest()!=row['after']:return raw
 if path not in CACHE:CACHE[path]=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True)
 return CACHE[path]
