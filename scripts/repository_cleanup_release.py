"""Validate a bounded removal-only cleanup against the merged site baseline."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = '51035256000a09c8879fd1577d6b44a23a025948'
MANIFEST = ROOT / 'data/repository-cleanup-2026-11-18.json'
ADAPTER = 'scripts/qa_topical_editorial.py'
ADDITIONS = {
    'data/repository-cleanup-2026-11-18.json',
    'docs/repository-cleanup-2026-11-18.md',
    'scripts/repository_cleanup_release.py',
    'scripts/qa_repository_cleanup.py',
}
ONE_TIME_SCRIPTS = {
    'scripts/apply_reviewed_alts.py', 'scripts/compact_journal_search.py',
    'scripts/compile_article_css.py', 'scripts/fix_audit_followup.py',
}

def blob_hash(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def checkout_hashes(raw):
    result = {blob_hash(raw)}
    if b'\0' not in raw:
        try:
            raw.decode('utf8')
            result.add(blob_hash(raw.replace(b'\r\n', b'\n')))
        except UnicodeDecodeError:
            pass
    return result

@lru_cache(maxsize=1)
def validate():
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    manifest = json.loads(MANIFEST.read_text(encoding='utf8'))
    check(manifest['baseline'] == BASE, 'Cleanup predecessor must remain pinned')
    raw_tree = subprocess.check_output(['git', 'ls-tree', '-rz', BASE], cwd=ROOT)
    tree = {}
    for record in raw_tree.split(b'\0'):
        if not record: continue
        header, path = record.split(b'\t', 1)
        tree[path.decode('utf8')] = header.split()[2].decode('ascii')
    deleted = {r['path']:r for r in manifest['deletions']}
    check(len(deleted) == len(manifest['deletions']), 'Retirement paths must be unique')
    for path, row in deleted.items():
        target = (ROOT / path).resolve()
        check(target.is_relative_to(ROOT.resolve()) and '..' not in Path(path).parts, 'Retirement outside repository: ' + path)
        check(path in tree and row['git_blob'] == tree.get(path), 'Unknown predecessor blob: ' + path)
        check(not target.exists(), 'Retired file is still present: ' + path)
        allowed = (
            path.startswith('assets/css/') and path.endswith('.css')
            or path in ONE_TIME_SCRIPTS
            or path.startswith('data/') and Path(path).suffix in {'.json', '.csv', '.txt', '.py', '.cjs', '.tsv'}
        )
        check(allowed and not path.startswith(('data/en-translations/', 'data/topical-editorial-2026-11-17/')), 'Protected or out-of-scope retirement: ' + path)
    # No editing HTML, live scripts, retained CSS, fonts, images, or old QA evidence.
    for path, sha in tree.items():
        if path in deleted: continue
        file = ROOT / path
        check(file.is_file(), 'Retained file missing: ' + path)
        if not file.is_file(): continue
        if path == ADAPTER:
            expected = manifest['modified_files'][path]
            check(expected['before_git_blob'] == sha, 'Editorial adapter baseline changed')
            check(hashlib.sha256(file.read_text(encoding='utf8').encode()).hexdigest() == expected['after_sha256'], 'Unknown editorial adapter change')
        else:
            check(sha in checkout_hashes(file.read_bytes()), 'File changed outside removal scope: ' + path)
    known = set(tree) - set(deleted) | ADDITIONS
    listed = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT).decode('utf8').split('\0')
    actual = {p for p in listed if p and (ROOT/p).is_file()}
    check(actual == known, 'Unregistered additions or deletions: ' + ', '.join(sorted(actual ^ known)))

    retired_css = {p for p in deleted if p.endswith('.css')}
    retained_code = {p for p in tree if p not in deleted and (p.endswith(('.html', '.css', '.js', '.py', '.cjs')) or p.startswith('.github/'))}
    for source in retained_code:
        if source == ADAPTER: continue
        text = (ROOT/source).read_text(encoding='utf8')
        if source.endswith(('.html', '.css', '.js')) and not source.startswith(('docs/', 'data/', 'cloudflare/')):
            for path in retired_css:
                check(Path(path).name not in text, source + ': still references retired stylesheet ' + path)
        if source.startswith('scripts/') or source.startswith('.github/'):
            for path in deleted:
                check(path not in text and Path(path).name not in text, source + ': still consumes retired file ' + path)
    # EN templates and externally deployed commerce infrastructure are consumers too.
    for path in ['assets/css/en-hubs.css', 'assets/css/en-translations.css', 'cloudflare/fourthwall-proxy.js', 'cloudflare/README.md', 'login.html', '404.html', 'google209e25d9de6b2414.html', '9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c.txt']:
        check(path not in deleted and (ROOT/path).is_file(), 'Explicitly retained dependency missing: ' + path)
    # Preserve the source-existence assertion; historical checks read their pinned checkout.
    check('Missing CSS source' in (ROOT/'scripts/qa_schema_pod_performance.py').read_text(), 'Historical CSS-source assertion removed')
    report = {
        'baseline':BASE, 'deleted_files':len(deleted),
        'removed_checkout_bytes':sum(r['checkout_bytes'] for r in deleted.values()),
        'removed_git_blob_bytes':sum(r['git_bytes'] for r in deleted.values()),
        'retained_baseline_files':len(tree)-len(deleted),
        'html_and_live_assets':'byte-equivalent to merged baseline' if not errors else 'see errors',
        'historical_css_source_assertion':'preserved', 'errors':errors,
    }
    return report, (set(deleted) | ADDITIONS | {ADAPTER}) if not errors else set()
