"""Validate original image identities and exact preservation of everything else."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import original_image_release as RELEASE
from fix_blog_image_seo import cover, getmeta

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://apocalypsecloset.com/'
TAGS = re.compile(r'<(?:img|source)\b[^>]*>', re.I)


def mask(raw):
    def replace(m):
        n = BeautifulSoup(m.group(), 'html.parser').find()
        for key in ['src', 'srcset', 'sizes']:
            n.attrs.pop(key, None)
        return str(n)
    raw = TAGS.sub(replace, raw)
    def meta(m):
        n = BeautifulSoup(m.group(), 'html.parser').meta
        return '' if n.get('property', n.get('name', '')) in ['og:image', 'twitter:image', 'og:image:width', 'og:image:height'] else m.group()
    return re.sub(r'<meta\b[^>]*>', meta, raw, flags=re.I)


def main():
    errors = RELEASE.validate()
    def check(ok, message):
        if not ok: errors.append(message)
    assets = json.loads((ROOT / 'data/blog-image-seo-2026-11-18/assets.json').read_text(encoding='utf8'))
    origins = {a['origin']: a for a in assets}
    variants = {urljoin(BASE, v['url']): a['origin'] for a in assets for v in a['variants']}
    pages = 0; images = 0; sources = 0; used = set()
    for path in RELEASE.release()['files']:
        if not path.endswith('.html'): continue
        raw = (ROOT / path).read_text(encoding='utf8')
        before = RELEASE.predecessor(path, raw)
        check(mask(before) == mask(raw), path + ': non-image markup, metadata, scripts or prose changed')
        old_tags = TAGS.findall(before); new_tags = TAGS.findall(raw)
        check(len(old_tags) == len(new_tags), path + ': image/source inventory changed')
        for old, new in zip(old_tags, new_tags):
            n = BeautifulSoup(new, 'html.parser').find()
            o = BeautifulSoup(old, 'html.parser').find()
            if '/assets/images/blog-responsive/' not in old:
                check(old == new, path + ': unrelated image/source changed')
                continue
            if o.name == 'img':
                expected = variants.get(urljoin(BASE + path, o.get('src', '')))
                actual = n.get('src', '')
                check(expected is not None and actual == expected, path + ': original image identity changed')
                check(not n.has_attr('srcset') and not n.has_attr('sizes'), path + ': obsolete responsive attributes')
                a = origins.get(actual)
                if a:
                    check(n.get('width') == str(a['width']) and n.get('height') == str(a['height']), path + ': inaccurate dimensions')
                check(bool(n.get('alt')), path + ': missing image alt')
                used.add(actual); images += 1
            else:
                expected = {variants.get(urljoin(BASE + path, x.strip().split()[0])) for x in o.get('srcset', '').split(',') if x.strip()}
                check(len(expected) == 1 and None not in expected and n.get('srcset') in expected, path + ': picture source identity changed')
                check(not n.has_attr('sizes'), path + ': obsolete source sizes')
                sources += 1
        check('/assets/images/blog-responsive/' not in raw, path + ': deleted variant still referenced')
        soup = BeautifulSoup(raw, 'html.parser')
        old_soup = BeautifulSoup(before, 'html.parser')
        for key in ['og:image', 'twitter:image']:
            old_url = getmeta(old_soup, key)
            check(getmeta(soup, key) == variants.get(old_url, old_url), path + ': social image identity changed')
        original_og = origins.get(getmeta(soup, 'og:image'))
        if '/assets/images/blog-responsive/' in getmeta(old_soup, 'og:image') and original_og:
            for k in ['width', 'height']:
                check(getmeta(soup, 'og:image:' + k) == str(original_og[k]), path + ': social image dimensions mismatch')
        pages += 1
    all_paths = sorted(p for p in ROOT.rglob('*.html') if not {'.git', 'node_modules', '.venv'} & set(p.parts))
    for p in all_paths:
        check('/assets/images/blog-responsive/' not in p.read_text(encoding='utf8'), p.relative_to(ROOT).as_posix() + ': dangling variant URL')
    folder = ROOT / 'assets/images/blog-responsive'
    check(not folder.exists() or not any(p.is_file() for p in folder.rglob('*')), 'Responsive image files remain')
    journal = BeautifulSoup((ROOT / 'en/blog.html').read_text(encoding='utf8'), 'html.parser')
    cards = journal.select('#latest .cards a.card, .journal-featured-card')
    check(len(cards) == 445, 'English card count changed')
    for c in cards:
        images_in_card = c.select('img.journal-thumbnail')
        check(len(images_in_card) == 1, 'Missing/duplicate English thumbnail')
        if len(images_in_card) != 1: continue
        target = c['href'].lstrip('/')
        page = BeautifulSoup((ROOT / target).read_text(encoding='utf8'), 'html.parser')
        expected = getmeta(page, 'og:image')
        if expected not in origins:
            cv = cover(page); expected = urljoin(BASE + target, cv['src']) if cv else ''
        check(images_in_card[0]['src'] == expected, 'Thumbnail mismatches target article: ' + target)
    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf8')
    check('/assets/images/blog-responsive/' not in sitemap, 'Sitemap references deleted variants')
    # Unknown bytes must not be accepted by the historical adapter.
    sample = next(p for p in RELEASE.release()['files'] if p.endswith('.html'))
    raw = (ROOT / sample).read_text(encoding='utf8')
    try:
        RELEASE.predecessor(sample, raw + '<!-- unknown -->')
        check(False, 'Adapter accepted unknown successor bytes')
    except ValueError:
        pass
    check(mask(raw) != mask(raw + '<p>Unreviewed prose</p>'), 'Preservation gate does not detect prose changes')
    report = {'changed_html': pages, 'restored_image_occurrences': images, 'restored_picture_sources': sources,
              'original_image_urls': len(used), 'deleted_files': len(RELEASE.retired()),
              'english_thumbnail_cards': len(cards), 'errors': errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__': sys.exit(main())
