"""Original 216 pairs stay separate from explicitly listed later translations."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows():
    original=list(csv.DictReader((ROOT/'data/en-216-keyword-intent-audit.csv').open()))
    assert len(original)==216,'The original inventory must stay at 216 pairs'
    extra=ROOT/'data/en-translation-extensions.csv'
    return original+(list(csv.DictReader(extra.open())) if extra.exists() else [])
def normalize_approved_maintenance(text):
    """Only the audited retired footer fragment is normalized for legacy source parity."""
    return text.replace('/#outfit-grid','/phoi-do-nu-ca-tinh.html#chon-phong-cach')
