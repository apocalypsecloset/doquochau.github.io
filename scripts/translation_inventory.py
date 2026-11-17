"""Original 216 pairs stay separate from explicitly listed later translations."""
import csv,json
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

def publication_rows():
    """The explicitly approved 220 R2 article pairs, including two prior publications."""
    published=json.loads((ROOT/'data/r2-220-publication.json').read_text())
    assert len(published)==220,'Expected 220 approved R2 article pairs'
    for lang in ['vi','en']:
        assert len({r[lang+'_url'] for r in published})==220,'Duplicate publication URL'
    return published

def sitemap_vi_urls():
    """Require all original pairs and every explicitly approved publication."""
    from link_fix_release import added_vi_urls
    return {r['vi_url'] for r in rows()} | {r['vi_url'] for r in publication_rows()} | added_vi_urls()

def catalog_urls(lang):
    """Every published translation plus the two original English-only articles."""
    assert lang in ['vi','en']
    urls={r[lang+'_url'] for r in rows()+publication_rows()}
    if lang=='en':
        urls.update('https://apocalypsecloset.com/en/blog/'+slug+'.html' for slug in ['how-to-style-gothic-graphic-tees','goth-vs-grunge-style'])
    return urls
