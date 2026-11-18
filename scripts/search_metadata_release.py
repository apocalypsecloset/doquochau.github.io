"""Exact reviewed search-metadata successors; unknown edits never normalize."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess
import original_image_release as ORIGINAL_IMAGES

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/search-metadata-2026-11-18/release.json'


def digest(raw):
    return hashlib.sha256(raw.replace('\r\n', '\n').encode('utf8')).hexdigest()


@lru_cache(maxsize=1)
def release():
    return json.loads(MANIFEST.read_text(encoding='utf8')) if MANIFEST.exists() else {'files': {}, 'additions': {}}


@lru_cache(maxsize=1)
def originals():
    paths = list(release()['files'])
    if not paths:
        return {}
    refs = ''.join(release()['baseline'] + ':' + p + '\n' for p in paths)
    data = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=ROOT, input=refs.encode())
    offset = 0
    result = {}
    for path in paths:
        end = data.index(b'\n', offset)
        header = data[offset:end].split()
        if len(header) != 3 or header[1] != b'blob':
            raise ValueError('Missing metadata predecessor: ' + path)
        size = int(header[2])
        offset = end + 1
        result[path] = data[offset:offset+size].decode('utf8').replace('\r\n', '\n')
        offset += size + 1
    return result


def predecessor(path, raw):
    raw = ORIGINAL_IMAGES.predecessor(path, raw)
    row = release()['files'].get(path)
    if not row:
        return raw
    if digest(raw) != row['after']:
        raise ValueError('Unreviewed metadata successor: ' + path)
    before = originals()[path]
    if digest(before) != row['before']:
        raise ValueError('Metadata predecessor hash mismatch: ' + path)
    return before


def additions():
    return set(release()['additions']) | ({MANIFEST.relative_to(ROOT).as_posix()} if MANIFEST.exists() else set())


def validate():
    errors = []
    for path in release()['files']:
        try:
            predecessor(path, (ROOT / path).read_text(encoding='utf8'))
        except Exception as exc:
            errors.append(str(exc))
    for path, expected in release()['additions'].items():
        p = ROOT / path
        if not p.is_file() or digest(ORIGINAL_IMAGES.predecessor(path, p.read_text(encoding='utf8'))) != expected:
            errors.append('Unreviewed metadata addition: ' + path)
    return errors
