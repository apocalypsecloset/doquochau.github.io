#!/usr/bin/env python3
"""Internal-link audit for apocalypsecloset.com (VI blog). Read-only.

Usage:  python tools/internal_link_audit.py [--root .] [--csv audit_pages.csv]
Exit code 1 if any gate FAILS. Requires: beautifulsoup4, lxml.
Add new hub slugs to HUBS below when you create them.
"""
import argparse, collections, csv, glob, os, re, sys, unicodedata
from urllib.parse import unquote, urljoin, urlparse
from bs4 import BeautifulSoup

DOMAIN = 'apocalypsecloset.com'

# cluster -> hub slug (file in /blog/). Fill in the new hubs as you create them.
HUBS = {
    'Aesthetic/Style': 'aesthetic-dictionary',
    'Ao': 'phoi-do-theo-ao-nu',
    'Quan': 'phoi-do-theo-quan-nu',
    'Vay-dam': 'phoi-do-theo-chan-vay-vay-nu',
    'Giay': 'phoi-do-theo-giay-nu',
    'Phu-kien': 'phu-kien-thoi-trang-nu-ca-tinh',
    'Vai': 'cac-loai-vai',
    'Kinh': 'cach-chon-kinh-phu-hop-voi-khuon-mat-nu',
    'Phoi-mau': 'phoi-mau-quan-ao-nu',
    'Dia-diem-dip': 'chon-trang-phuc-nu-theo-dia-diem-va-dip',
    'Cham-soc': 'cach-cham-soc-do-nu',
    'Toc-lam-dep': 'chon-toc-va-makeup-theo-trang-phuc',
}
STYLE_SUBHUBS = ['goth', 'punk-grunge', 'egirl', 'dark-feminine', 'badgirl', 'baddie-streetwear']
# Hub pages are navigation, so they are exempt from the "child" role in their own cluster.

RULES = [
 # Reviewed search intents: skin tone is not suede; Vietnamese "mau" can mean mẫu.
 ('Phoi-mau', r'^(da-ngam-mac-mau-gi|white-on-white)$'),
 ('Vay-dam', r'^(nhung-mau-dam-so-mi-dep-nhat|mau-dam-nhung-sang-trong)$'),
 ('Quan', r'^trouser-la-quan-gi$'),
 ('Outfit-core', r'^phoi-do-dang-(qua-le|tam-giac-nguoc)$'),
 ('Cham-soc', r'^(cach-bao-quan|cach-giat|cach-khu-mui|cach-lam-mem|cach-gap|cach-buoc-day|cach-len-lai|cach-so-vin|cach-xan-tay|mieng-lot)'),
 ('Phoi-mau', r'(phoi-quan-mau-gi|phoi-ao-mau-gi|phoi-voi-mau-gi|ket-hop-voi-mau-gi|mac-voi-quan-mau-gi|-la-mau-gi|^mau-|ket-hop-voi-ao-mau-gi|banh-xe-mau-sac)'),
 ('Vai', r'^(vai-|cac-loai-vai|chat-vai|polyester|chiffon|da-lon|tie-dye)'),
 ('Kinh', r'(kinh-|gong-|chon-kinh)'),
 ('Phu-kien', r'(bong-tai|nhan-|vong-tay|day-chuyen|choker|khuyen-tai|khan-quang|that-khan|that-lung|mu-|tui-|cravat|arm-warmers|leg-warmers|phu-kien|cach-chon-tui|fishnet)'),
 ('Toc-lam-dep', r'(kieu-toc|nhuom-toc|butterfly-haircut|hime-cut|goth-nails|punk-makeup)'),
 ('Dia-diem-dip', r'(^di-|outfit-di-|outfit-san-bay|outfit-tet|ao-dai-tet|chup-anh-ao-dai|mac-ao-dai|outfit-mua-dong|outfit-nu-ca-tinh-di-concert|phoi-do-nu-ca-tinh-di-choi|phoi-do-nu-ca-tinh-mua-he|badgirl-outfit-di-cafe|outfit-di-choi-dem|vay-di-du|rave-outfits|mac-do-den-mua-he)'),
 ('Giay', r'(^giay-|^dep-|boots|platform-shoes|ballet-flats|combat-boots)'),
 ('Quan', r'(^quan-|phoi-do-voi-quan|phoi-do-theo-quan|denim-on-denim)'),
 ('Vay-dam', r'(^vay-|^dam-|chan-vay|phoi-do-voi-vay|dress-la-gi|slip-dress|babydoll|bodycon|qipao|ao-dai-tim)'),
 ('Ao', r'(^ao-|phoi-do-voi-ao|phoi-do-theo-ao|blouse|outerwear|croptop|bo-vest|harrington|cuban-shirt|form-oversize|pyjama|phoi-ao-co-lo|corset-top)'),
 ('Outfit-core', r'(phoi-do-theo-item|outfit-la-gi|ootd-la-gi|moodboard|cach-chup-anh-ootd|capsule-wardrobe|layering|^set-|tu-do-alt|duoi-500k|cho-nguoi|nu-ca-tinh-cho|cach-phoi-do-den|cach-chon-size|mua-sam-alt|local-brand|auth-la-gi|like-auth|sold-out|boutique|unisex|dress-code)'),
]
def cluster(slug):
    for name, hub_slug in HUBS.items():
        if slug == hub_slug: return name
    if slug == 'phoi-do-theo-giay-nu': return 'Giay'
    if slug == 'phoi-do-theo-item': return 'Outfit-core'
    for n, r in RULES:
        if re.search(r, slug): return n
    return 'Aesthetic/Style'

MODULE_CLASSES = {'ac-reading-path','ac-locale-link','ac-sources','article-nav','article-tags','share-links',
    'related-outfit-grid','ac-pinterest-links','toc','article-toc','micro-cta','ac-topic-route','ac-parent-links',
    'badgirl-look-grid','ac-look-analysis','ac-mini-links','ac-primary-nav','ac-footer-grid'}
BAD_PHRASES = re.compile(r'\bhub\b|trang trụ cột|bổ trợ cho|cụm chủ đề', re.I)
GENERIC = re.compile(r'^(xem thêm|đọc thêm|tại đây|ở đây|click|bấm vào|bài viết này|đọc tiếp|xem ngay|link)\b', re.I)

def norm(s):
    s = unicodedata.normalize('NFD', s.lower().replace('đ', 'd'))
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')

def resolve(href, cur):
    if not href or href.startswith(('mailto:', 'tel:', 'javascript:', '#')): return None
    u = urlparse(href)
    if u.scheme in ('http', 'https'):
        if u.netloc.replace('www.', '') != DOMAIN: return None
        path = u.path
    elif u.netloc: return None
    else: path = urljoin('/' + cur, u.path)
    path = unquote(path)
    if path.endswith('/'): path += 'index.html'
    return path.lstrip('/')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--csv', default='')
    a = ap.parse_args()
    root = a.root
    allfiles = set()
    for r, _, fs in os.walk(root):
        if any(x in r for x in ('/.git', '/node_modules')): continue
        for f in fs: allfiles.add(os.path.relpath(os.path.join(r, f), root).replace(os.sep, '/'))

    pages, stubs = {}, set()
    for f in glob.glob(os.path.join(root, 'blog', '*.html')):
        rel = os.path.relpath(f, root).replace(os.sep, '/')
        html = open(f, encoding='utf8', errors='replace').read()
        if re.search(r'http-equiv="refresh"', html, re.I): stubs.add(rel); continue
        pages[rel] = BeautifulSoup(html, 'lxml')
    slug = lambda p: p[5:-5]
    cl = {p: cluster(slug(p)) for p in pages}

    prose = collections.defaultdict(list)   # src -> [(target, anchor, ctx)]
    anyl = collections.defaultdict(set)     # src -> targets (any module)
    broken = []
    for p, s in pages.items():
        art = s.select_one('article.article-content') or s.find('main')
        if not art: continue
        for al in art.find_all('a', href=True):
            t = resolve(al['href'], p)
            if not t or t == p: continue
            if t not in allfiles and t not in pages: broken.append((p, al['href']))
            if t in stubs: broken.append((p, al['href'] + '  (redirect stub)'))
            anyl[p].add(t)
            cls, ctx, mod = set(), None, False
            for par in al.parents:
                if par is art: break
                cls |= set(par.get('class', []))
                if ctx is None and par.name in ('p', 'li', 'td', 'blockquote', 'figcaption'): ctx = par
            if cls & MODULE_CLASSES or ctx is None or al.find('img'): continue
            prose[p].append((t, al.get_text(' ', strip=True), ctx.get_text(' ', strip=True)))

    inb_prose = collections.defaultdict(set)
    for p, ls in prose.items():
        for t, _, _ in ls: inb_prose[t].add(p)

    gates = []
    def gate(name, bad, detail=''):
        gates.append((name, len(bad) == 0, len(bad), bad[:6], detail))

    gate('G1 link gãy / link vào redirect', broken)
    thin = [p for p in pages if len({t for t, _, _ in prose[p] if t in pages}) < 2]
    gate('G2 bài có <2 link ngữ cảnh tới bài blog khác', thin)
    noin = [p for p in pages if not inb_prose[p]]
    gate('G3 bài không có link ngữ cảnh vào từ bài khác', noin)
    # hubs
    bad_hub = []
    for c in sorted(set(cl.values())):
        h = HUBS.get(c)
        if not h: bad_hub.append(f'{c}: CHƯA CÓ HUB'); continue
        hp = f'blog/{h}.html'
        if hp not in pages: bad_hub.append(f'{c}: hub {h} không tồn tại'); continue
        hubset = {hp}
        if c == 'Aesthetic/Style':  # nhiều hub con: từ điển + hub từng style
            hubset |= {f'blog/{x}.html' for x in STYLE_SUBHUBS if f'blog/{x}.html' in pages}
        kids = [p for p in pages if cl[p] == c and p not in hubset]
        down = set().union(*[anyl[x] for x in hubset])
        miss_down = [slug(k) for k in kids if k not in down]
        miss_up = [slug(k) for k in kids if not (hubset & anyl[k])]
        if miss_down: bad_hub.append(f'{c}: hub thiếu {len(miss_down)} bài con (vd {miss_down[:2]})')
        if miss_up: bad_hub.append(f'{c}: {len(miss_up)} bài con không link lên hub (vd {miss_up[:2]})')
    gate('G4 hub trỏ đủ xuống con + con trỏ lên hub', bad_hub)
    # sibling links
    nosib = []
    for c in set(cl.values()):
        kids = [p for p in pages if cl[p] == c]
        if len(kids) < 3: continue
        for k in kids:
            if len({t for t, _, _ in prose[k] if t in kids}) < 1: nosib.append(slug(k))
    gate('G5 bài không có link ngang cùng cụm trong thân bài', nosib)
    # colour pairs
    S = {slug(p) for p in pages}; bad_pair = []
    for s in S:
        m = re.match(r'ao-(.+)-(?:phoi-quan-mau-gi|mac-voi-quan-mau-gi)$', s)
        if not m: continue
        for q in S:
            if re.match(rf'quan-{re.escape(m.group(1))}-phoi-ao-mau-gi$', q):
                A, B = f'blog/{s}.html', f'blog/{q}.html'
                if B not in anyl[A] or A not in anyl[B]: bad_pair.append(f'{s} <-> {q}')
    gate('G6 cặp áo<->quần cùng màu chưa link hai chiều', bad_pair)
    # language / phrasing
    bp = [f'{slug(p)}: {c[:70]}' for p, ls in prose.items() for _, _, c in ls if BAD_PHRASES.search(c)]
    gate('G7 câu chứa link có chữ hub/trang trụ cột/bổ trợ', bp)
    gen = [f'{slug(p)}: {an}' for p, ls in prose.items() for _, an, _ in ls if GENERIC.match(an) or not an]
    gate('G8 anchor generic/rỗng', gen)
    dup = [f'{slug(p)} -> {slug(t)}' for p, ls in prose.items()
           for t, n in collections.Counter(t for t, _, _ in ls).items() if n > 1 and t in pages]
    gate('G9 một đích bị link >1 lần trong cùng bài', dup)
    ac = collections.Counter((t, an.lower()) for ls in prose.values() for t, an, _ in ls if t in pages)
    over = [f'{n}x "{an}" -> {slug(t)}' for (t, an), n in ac.most_common() if n > 5]
    gate('G10 cùng 1 anchor lặp >5 lần cho cùng 1 đích', over)
    many = [slug(p) for p, ls in prose.items() if len({t for t, _, _ in ls if t in pages}) > 12]
    gate('G11 bài có >12 link tới bài khác (quá dày)', many)

    # report
    print('=' * 78); print(f'Bài VI: {len(pages)} | stub redirect bỏ qua: {len(stubs)}')
    cnt = [len({t for t, _, _ in prose[p] if t in pages}) for p in pages]
    print(f'Link ngữ cảnh tới bài khác/bài: min {min(cnt)}, TB {sum(cnt)/len(cnt):.1f}, max {max(cnt)}')
    print(f'Cụm: ' + ', '.join(f'{c}={n}' for c, n in collections.Counter(cl.values()).most_common()))
    print('=' * 78)
    fails = 0
    for name, ok, n, ex, _ in gates:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ('' if ok else f'  ({n})'))
        if not ok:
            fails += 1
            for e in ex: print('        -', e)
    print('=' * 78); print('KẾT QUẢ:', 'ĐẠT TẤT CẢ' if not fails else f'{fails} gate chưa đạt')
    if a.csv:
        with open(a.csv, 'w', newline='', encoding='utf8') as fh:
            w = csv.writer(fh); w.writerow(['slug', 'cluster', 'unique_prose_out', 'prose_in', 'any_out'])
            for p in sorted(pages):
                w.writerow([slug(p), cl[p], len({t for t, _, _ in prose[p] if t in pages}), len(inb_prose[p]), len(anyl[p])])
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
