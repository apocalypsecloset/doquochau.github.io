"""Read-only E0 runner: original QA commands, complete stdout/stderr, no bypasses."""
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT/'tools/.python-deps')
env['PYTHONUTF8'] = '1'
env['PYTHONIOENCODING'] = 'utf-8'
tracked = subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
snapshot = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked if p and (ROOT/p).is_file()}
(OUT/'tracked_before.json').write_text(json.dumps(snapshot,indent=2),encoding='utf-8')
jobs = [
    ('audit_vi', ['tools/internal_link_audit.py','--root','.']),
    ('qa_link_fix', ['scripts/qa_link_fix.py']),
]
for name in ['qa_privacy_policies','qa_schema_pod_performance','qa_blog_repair',
             'qa_storefront_ux','qa_site','qa_audit_followup','qa_r2_image_seo']:
    jobs.append((name,['scripts/'+name+'.py']))
for p in sorted((ROOT/'data/en-translations').glob('batch*.json')):
    if p.stem == 'batch05b':continue
    jobs.append(('translations_'+p.stem,['scripts/qa_en_translations.py',p.stem]))
    configs=json.loads(p.read_text(encoding='utf-8'))
    if any(c.get('source_kind')=='hub' for c in configs):
        args=['scripts/qa_en_hubs.py',p.stem]
        if not all(c.get('source_kind')=='hub' for c in configs):args+=['--hubs-only']
        jobs.append(('hubs_'+p.stem,args))

def run(job):
    name,args=job
    start=time.monotonic()
    r=subprocess.run([sys.executable,'-X','utf8',*args],cwd=ROOT,env=env,capture_output=True)
    (OUT/(name+'.stdout.txt')).write_bytes(r.stdout)
    (OUT/(name+'.stderr.txt')).write_bytes(r.stderr)
    try:parsed=json.loads(r.stdout.decode('utf-8-sig'))
    except (ValueError,UnicodeError):parsed=None
    row=dict(name=name,command=[sys.executable,'-X','utf8',*args],exit_code=r.returncode,
             seconds=round(time.monotonic()-start,1),report=parsed)
    print(f'{name}: exit {r.returncode}, {row["seconds"]}s',flush=True)
    return row

results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for row in pool.map(run,jobs):
        results.append(row)
        (OUT/'qa_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
changed=[p for p,h in snapshot.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
(OUT/'tracked_preservation.json').write_text(json.dumps(dict(changed=changed,tracked_files=len(snapshot)),indent=2),encoding='utf-8')
assert not changed,changed
print(f'Completed {len(results)} checks; tracked files unchanged.',flush=True)

