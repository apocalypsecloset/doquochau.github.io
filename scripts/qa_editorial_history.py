"""Run immutable release contracts on their pinned predecessor checkout.

Current HTML is checked by qa_topical_editorial.py, both live link audits and
qa_site.py. This runner does not normalize, patch or bypass an old assertion.
"""
import hashlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tarfile

ROOT = Path(__file__).resolve().parents[1]
BASE = '97ba710f3e23cde22c9dc72b87052b507049ddaa'
ALLOWED = {
    'qa_batch40.py', 'qa_en_link_e15.py', 'qa_en_link_e4.py',
    'qa_en_link_fix.py', 'qa_link_fix.py', 'qa_en_translations.py',
    'qa_privacy_policies.py', 'qa_storefront_ux.py', 'qa_blog_repair.py',
    'qa_schema_pod_performance.py', 'qa_audit_followup.py', 'qa_r2_image_seo.py',
}

def main():
    os.environ['PYTHONUTF8'] = '1'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    name = Path(sys.argv[1]).name
    if name not in ALLOWED:
        raise SystemExit('Unsupported historical contract: ' + name)
    key = hashlib.sha256(str(ROOT).encode()).hexdigest()[:12]
    checkout = Path(os.environ.get('RUNNER_TEMP', tempfile.gettempdir())) / ('ac-history-archive-' + key + '-' + BASE[:8])
    if not checkout.exists():
        # No transport, shell, smudge filter or remote credentials are needed.
        archive = subprocess.check_output(['git', 'archive', '--format=tar', BASE], cwd=ROOT)
        checkout.mkdir(parents=True)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(checkout, filter='data')
    if not (checkout/'.git/ac-history-ready').is_file():
        subprocess.run(['git', 'init', '-q', str(checkout)], check=True)
        objects = subprocess.check_output(['git', 'rev-parse', '--git-path', 'objects'], cwd=ROOT, text=True).strip()
        objects = (ROOT / objects).resolve() if not Path(objects).is_absolute() else Path(objects)
        info = checkout / '.git/objects/info'; info.mkdir(exist_ok=True)
        (info/'alternates').write_text(objects.as_posix() + '\n', encoding='utf8', newline='\n')
        (checkout/'.git/HEAD').write_text(BASE + '\n', encoding='ascii', newline='\n')
        subprocess.run(['git', '-C', str(checkout), 'read-tree', BASE], check=True)
        (checkout/'.git/ac-history-ready').write_text(BASE, encoding='ascii')
    # Git archive follows the source checkout's EOL conversion on Windows.
    # Normalizing text in this independent index also accepts LF archives on CI.
    subprocess.run(['git', '-C', str(checkout), 'config', 'core.autocrlf', 'true'], check=True)
    actual = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != BASE or subprocess.check_output(['git', '-C', str(checkout), 'status', '--porcelain']).strip():
        raise SystemExit('Historical checkout is not the clean pinned predecessor')
    print('Historical contract on immutable predecessor ' + BASE, flush=True)
    result = subprocess.run([sys.executable, '-X', 'utf8', str(checkout / 'scripts' / name), *sys.argv[2:]], cwd=checkout)
    raise SystemExit(result.returncode)

if __name__ == '__main__':
    main()
