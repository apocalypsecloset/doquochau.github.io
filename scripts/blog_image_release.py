"""Exact successor records for the image-only release and earlier contracts.

The new image QA inspects current HTML. Older byte-preservation contracts get
their exact predecessor only after this successor's content hash is verified.
Unknown edits never receive a predecessor view.
"""
from functools import lru_cache
import hashlib,json,subprocess
from pathlib import Path
from fix_blog_image_seo import baseline
import search_metadata_release as SEARCH_METADATA
import original_image_release as ORIGINAL_IMAGES
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'data/blog-image-seo-2026-11-18/release.json'

@lru_cache(maxsize=1)
def release():return json.loads(MANIFEST.read_text(encoding='utf8')) if MANIFEST.exists() else {'files':{},'additions':{}}

def digest(raw):return hashlib.sha256(raw.encode('utf8')).hexdigest()

def file_digest(path):
 raw=path.read_bytes()
 if path.suffix!='.webp':
  try:raw=SEARCH_METADATA.predecessor(path.relative_to(ROOT).as_posix(),raw.decode('utf8').replace('\r\n','\n')).encode('utf8')
  except UnicodeDecodeError:pass
 return hashlib.sha256(raw).hexdigest()

@lru_cache(maxsize=1)
def originals():return baseline(list(release()['files']),release()['baseline'])

def original(path):return originals()[path]

def predecessor(path,raw):
 raw=SEARCH_METADATA.predecessor(path,raw)
 row=release()['files'].get(path)
 if not row:return raw
 if digest(raw)!=row['after']:raise ValueError('Unreviewed image-release successor: '+path)
 before=original(path)
 if digest(before)!=row['before']:raise ValueError('Image-release predecessor hash mismatch: '+path)
 return before

def additions():return set(release()['additions']) | ({MANIFEST.relative_to(ROOT).as_posix()} if MANIFEST.exists() else set())

def validate():
 errors=ORIGINAL_IMAGES.validate()
 for path,row in release()['files'].items():
  try:predecessor(path,(ROOT/path).read_text(encoding='utf8'))
  except Exception as exc:errors.append(str(exc))
 for path,sha in release()['additions'].items():
  if path in ORIGINAL_IMAGES.retired():continue
  p=ROOT/path
  if not p.is_file() or file_digest(p)!=sha:errors.append('Unknown image-release addition: '+path)
 return errors
