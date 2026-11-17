#!/usr/bin/env python3
"""EN internal-link audit (read-only). Compares /en/blog/*.html with the VI originals.

Usage:  python scripts/internal_link_audit_en.py [--root .] [--csv data/audit_en_pages.csv]
Exit 1 if any gate FAILS. Needs: beautifulsoup4, lxml.
Cluster of an EN page = cluster of its VI counterpart (from hreflang vi).
"""
import argparse, collections, csv, glob, os, re, sys
from urllib.parse import unquote, urljoin, urlparse
from bs4 import BeautifulSoup
from internal_link_audit import RULES as VI_RULES, HUBS as CURRENT_VI_HUBS, cluster as vi_cluster

DOMAIN = 'apocalypsecloset.com'
# User-approved classification alignment. EN hubs are found through hreflang;
# use the same reviewed topical map as VI, including Outfit-core.
VI_HUBS = dict(CURRENT_VI_HUBS)
STYLE_SUBHUBS = ['goth', 'punk-grunge', 'egirl', 'dark-feminine', 'badgirl', 'baddie-streetwear']
# The fourteen gate implementations and thresholds below are unchanged.
RULES = list(VI_RULES)

def cluster(slug):
    return vi_cluster(slug)

MODULES = {'ac-reading-path','ac-locale-link','ac-sources','article-nav','article-tags','share-links','related-outfit-grid',
    'ac-pinterest-links','toc','article-toc','micro-cta','ac-topic-route','ac-parent-links','buy-filter','hub-locale','ac-mini-links'}
BAD = re.compile(r'\bhub\b|pillar page|cornerstone|topic cluster|supporting article|money page', re.I)
GENERIC = re.compile(r'^(click here|read more|learn more|see more|here|this (article|post|page|guide)|link|more)\b', re.I)
VNCHARS = re.compile('[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]', re.I)
SWITCH = re.compile(r'vietnamese original|read the vietnamese|xem bản tiếng việt', re.I)

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

def hreflang(soup, lang):
    for l in soup.find_all('link', rel='alternate'):
        if l.get('hreflang') == lang and l.get('href'):
            return urlparse(l['href']).path.lstrip('/')

def parse(root, folder):
    pages = {}
    for f in glob.glob(os.path.join(root, folder, '*.html')):
        rel = os.path.relpath(f, root).replace(os.sep, '/')
        html = open(f, encoding='utf8', errors='replace').read()
        if re.search(r'http-equiv="refresh"', html, re.I): continue
        pages[rel] = BeautifulSoup(html, 'lxml')
    return pages

def extract(pages, body_sel, self_check=True):
    prose, anyl, bodies = {}, {}, {}
    for p, s in pages.items():
        art = None
        for sel in body_sel:
            art = s.select_one(sel)
            if art: break
        art = art or s.find('main')
        pr, an = [], set()
        if art:
            for al in art.find_all('a', href=True):
                t = resolve(al['href'], p)
                if not t or t == p: continue
                txt = al.get_text(' ', strip=True)
                an.add(t)
                cls, ctx = set(), None
                for par in al.parents:
                    if par is art: break
                    cls |= set(par.get('class', []))
                    if ctx is None and par.name in ('p', 'li', 'td', 'blockquote', 'figcaption'): ctx = par
                if cls & MODULES or ctx is None or al.find('img') or SWITCH.search(txt): continue
                pr.append((t, txt, ctx.get_text(' ', strip=True), al.get('hreflang')))
        prose[p], anyl[p] = pr, an
    return prose, anyl

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--root', default='.'); ap.add_argument('--csv', default='')
    a = ap.parse_args(); root = a.root
    allfiles = set()
    for r, _, fs in os.walk(root):
        if '/.git' in r or '/node_modules' in r: continue
        for f in fs: allfiles.add(os.path.relpath(os.path.join(r, f), root).replace(os.sep, '/'))
    en = parse(root, 'en/blog'); vi = parse(root, 'blog')
    en_prose, en_any = extract(en, ['article.editorial', 'main.en-hub', 'article'])
    vi_prose, vi_any = extract(vi, ['article.article-content'])
    hubs_en = {p for p, s in en.items() if s.select_one('main.en-hub')}
    arts = [p for p in en if p not in hubs_en]
    # mapping VI<->EN via hreflang
    en2vi = {p: hreflang(s, 'vi') for p, s in en.items()}
    vi2en = {v: p for p, v in en2vi.items() if v and v in vi}
    slug = lambda p: p.split('/')[-1][:-5]
    cl = {p: cluster(slug(en2vi[p])) if en2vi.get(p) else None for p in en}
    inb = collections.defaultdict(set)
    for p, ls in en_prose.items():
        for t, *_ in ls: inb[t].add(p)

    gates = []
    def gate(name, bad): gates.append((name, not bad, len(bad), bad[:6]))

    broken = [f'{p} -> {t}' for p in en for t in en_any[p] if t not in allfiles and t not in en and t not in vi]
    gate('E1 link gãy', broken)
    gate('E2 bài EN <2 link ngữ cảnh tới bài EN khác', [p for p in arts if len({t for t, *_ in en_prose[p] if t in en}) < 2])
    gate('E3 bài EN không có link ngữ cảnh vào từ bài EN khác', [p for p in arts if not inb[p]])
    # hubs via hreflang
    bad_hub = []
    for c in sorted({v for v in cl.values() if v}):
        vh = VI_HUBS.get(c)
        if not vh: bad_hub.append(f'{c}: chưa khai báo hub VI trong VI_HUBS'); continue
        eh = vi2en.get(f'blog/{vh}.html')
        if not eh: bad_hub.append(f'{c}: hub VI {vh} chưa có bản EN (hreflang)'); continue
        hubset = {eh}
        if c == 'Aesthetic/Style':
            hubset |= {vi2en[f'blog/{x}.html'] for x in STYLE_SUBHUBS if f'blog/{x}.html' in vi2en}
        kids = [p for p in arts if cl[p] == c and p not in hubset]
        down = set().union(*[en_any[x] for x in hubset])
        md = [slug(k) for k in kids if k not in down]; mu = [slug(k) for k in kids if not (hubset & en_any[k])]
        if md: bad_hub.append(f'{c}: hub EN thiếu {len(md)} bài con (vd {md[:2]})')
        if mu: bad_hub.append(f'{c}: {len(mu)} bài con EN không link lên hub (vd {mu[:2]})')
    gate('E4 hub EN trỏ đủ xuống con + con trỏ lên hub', bad_hub)
    nosib = []
    for c in {v for v in cl.values() if v}:
        kids = [p for p in arts if cl[p] == c]
        if len(kids) < 3: continue
        nosib += [slug(k) for k in kids if not {t for t, *_ in en_prose[k] if t in kids}]
    gate('E5 bài EN không có link ngang cùng cụm', nosib)
    # PARITY with VI: every VI contextual target that has an EN twin must appear in the EN page
    low = []
    for v, ls in vi_prose.items():
        e = vi2en.get(v)
        if not e or e in hubs_en: continue
        want = {vi2en[t] for t, *_ in ls if t in vi2en and vi2en[t] != e}
        if not want: continue
        have = en_any[e]
        miss = [slug(w) for w in want if w not in have]
        if len(want) - len(miss) < 0.8 * len(want): low.append(f'{slug(e)}: thiếu {len(miss)}/{len(want)} link so với bản VI (vd {miss[:2]})')
    gate('E6 parity với VI: EN phải có ≥80% link tới bản EN của các đích VI', low)
    twin = {v for v in vi2en}
    leak = [f'{slug(p)} -> {t}' for p in arts for t, tx, c, hl in en_prose[p] if t in twin and t != en2vi.get(p)]
    gate('E7 link ngữ cảnh EN còn trỏ sang bản VI dù đã có bản EN', leak)
    PROPER = re.compile(r'áo dài|hội an|huế|đà lạt|đà nẵng|bà nà|hà giang|sa pa|việt nam|tết|hạ long|phú quốc|café|cafe', re.I)
    viet = [f'{slug(p)}: {tx}' for p in arts for t, tx, c, hl in en_prose[p]
            if t != en2vi.get(p) and VNCHARS.search(PROPER.sub('', tx))]
    gate('E8 anchor EN chứa ký tự tiếng Việt (ngoài tên riêng)', viet)
    gate('E9 chữ hub/pillar/cornerstone trong câu có link', [f'{slug(p)}: "{BAD.search(c).group()}" in: {c[:80]}' for p in arts for t, tx, c, hl in en_prose[p] if BAD.search(c)])
    gate('E10 anchor generic/rỗng', [f'{slug(p)}: {tx}' for p in arts for t, tx, c, hl in en_prose[p] if GENERIC.match(tx) or not tx])
    dup = [f'{slug(p)} -> {slug(t)}' for p in arts for t, n in collections.Counter(t for t, *_ in en_prose[p]).items() if n > 1 and t in en]
    gate('E11 một đích bị link >1 lần trong cùng bài', dup)
    ac = collections.Counter((t, tx.lower()) for p in arts for t, tx, c, hl in en_prose[p] if t in en)
    gate('E12 cùng anchor lặp >5 lần cho cùng 1 đích', [f'{n}x "{tx}" -> {slug(t)}' for (t, tx), n in ac.most_common() if n > 5])
    gate('E13 bài EN có >12 link tới bài EN khác', [slug(p) for p in arts if len({t for t, *_ in en_prose[p] if t in en}) > 12])
    # hreflang pairing sanity
    originals = [p for p in arts if not en2vi.get(p)]
    gate('E14 bài EN không ghép được bản VI (ngoài 2 bài EN gốc đã biết)',
         [p for p in originals if slug(p) not in ('how-to-style-gothic-graphic-tees', 'goth-vs-grunge-style')])
    print('=' * 78)
    cnt = [len({t for t, *_ in en_prose[p] if t in en}) for p in arts]
    print(f'EN: {len(arts)} bài + {len(hubs_en)} hub | VI: {len(vi)} trang | ghép được VI↔EN: {len(vi2en)}')
    print(f'Link ngữ cảnh tới bài EN khác/bài: min {min(cnt)}, TB {sum(cnt)/len(cnt):.1f}, max {max(cnt)}')
    print('=' * 78)
    fails = 0
    for name, ok, n, ex in gates:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ('' if ok else f'  ({n})'))
        if not ok:
            fails += 1
            for e in ex: print('        -', e)
    print('=' * 78); print('KẾT QUẢ:', 'ĐẠT TẤT CẢ' if not fails else f'{fails} gate chưa đạt')
    if a.csv:
        with open(a.csv, 'w', newline='', encoding='utf8') as fh:
            w = csv.writer(fh); w.writerow(['en_slug', 'vi_slug', 'cluster', 'unique_prose_out_en', 'prose_in_en'])
            for p in sorted(arts):
                w.writerow([slug(p), slug(en2vi[p]) if en2vi.get(p) else '', cl[p] or '',
                            len({t for t, *_ in en_prose[p] if t in en}), len(inb[p])])
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
