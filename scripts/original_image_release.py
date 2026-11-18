"""Exact successors for restoring original image URLs and retiring variants."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/original-images-2026-11-18/release.json'


def digest(raw):
    return hashlib.sha256(raw.replace('\r\n', '\n').encode('utf8')).hexdigest()


@lru_cache(maxsize=1)
def release():
    return json.loads(MANIFEST.read_text(encoding='utf8')) if MANIFEST.exists() else {'files': {}, 'additions': {}, 'deleted': {}}


@lru_cache(maxsize=1)
def originals():
    paths = list(release()['files'])
    if not paths:
        return {}
    refs = ''.join(release()['baseline'] + ':' + p + '\n' for p in paths)
    data = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=ROOT, input=refs.encode())
    result = {}
    offset = 0
    for path in paths:
        end = data.index(b'\n', offset)
        header = data[offset:end].split()
        if len(header) != 3 or header[1] != b'blob':
            raise ValueError('Missing original-image predecessor: ' + path)
        size = int(header[2]); offset = end + 1
        result[path] = data[offset:offset+size].decode('utf8').replace('\r\n', '\n')
        offset += size + 1
    return result


def predecessor(path, raw):
    row = release()['files'].get(path)
    if not row:
        return raw
    if digest(raw) != row['after']:
        raise ValueError('Unreviewed original-image successor: ' + path)
    old = originals()[path]
    if digest(old) != row['before']:
        raise ValueError('Original-image predecessor hash mismatch: ' + path)
    return old


def additions():
    return set(release()['additions']) | ({MANIFEST.relative_to(ROOT).as_posix()} if MANIFEST.exists() else set())


def retired():
    return set(release()['deleted'])


def validate():
    errors = []
    if not MANIFEST.exists():
        return errors
    for path in release()['files']:
        try:
            predecessor(path, (ROOT / path).read_text(encoding='utf8'))
        except Exception as exc:
            errors.append(str(exc))
    for path, sha in release()['additions'].items():
        file = ROOT / path
        if not file.is_file() or digest(file.read_text(encoding='utf8')) != sha:
            errors.append('Unreviewed original-image addition: ' + path)
    tree = subprocess.check_output(['git', 'ls-tree', '-r', release()['baseline'], '--', 'assets/images/blog-responsive'], cwd=ROOT, text=True)
    expected = {line.split('\t', 1)[1]: line.split('\t', 1)[0].split()[2] for line in tree.splitlines()}
    if set(expected) != retired():
        errors.append('Retired image inventory differs from pinned predecessor')
    for path, row in release()['deleted'].items():
        file = (ROOT / path).resolve()
        if not file.is_relative_to((ROOT / 'assets/images/blog-responsive').resolve()):
            errors.append('Retirement outside approved image directory: ' + path)
        if file.exists() or row['git_blob'] != expected.get(path):
            errors.append('Retired image still present or unrecognized: ' + path)
    return errors
