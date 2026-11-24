#!/usr/bin/env python3
"""
Inject 3 shop CTAs (top / mid / end) into Apocalypse Closet blog posts.

Safe by default: nothing in the site is changed unless you pass --write.
Re-running is idempotent (old CTA blocks are replaced, never duplicated).

Examples (run from the site root, i.e. the folder that contains index.html):
  python tools/blog-cta/inject_cta.py --sample 5 --out /tmp/cta-preview   # preview, site untouched
  python tools/blog-cta/inject_cta.py --lang en --write                   # all EN posts
  python tools/blog-cta/inject_cta.py --lang all --write                  # EN + VI (also removes the app box)
  python tools/blog-cta/inject_cta.py --lang all --remove --write         # rollback: strip every CTA
"""
import argparse, hashlib, html as html_utils, json, re, shutil, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARK = "ac-cta"
MID_POSITION = "<!-- ac-bcta-mid-position -->"
CSS_SOURCE = HERE.parents[1] / "assets" / "css" / "blog-shop-cta.css"
CSS_CONTENT = CSS_SOURCE.read_text(encoding="utf-8")
CSS_HASH = hashlib.sha256(CSS_CONTENT.encode("utf-8")).hexdigest()[:12]
CSS_FILENAME = "blog-shop-cta." + CSS_HASH + ".css"
CSS_HREF = "/assets/css/" + CSS_FILENAME + "?cta-version=" + CSS_HASH
CSS_LINK_RE = r'\s*<link\b[^>]*href="/assets/css/blog-shop-cta(?:\.[a-f0-9]{12})?\.css[^>]*>\s*'
CSS_INLINE_RE = r'\s*<style\b(?=[^>]*\bid="ac-blog-cta-style")[^>]*>.*?</style>\s*'
CSS_INLINE_CONTENT = re.sub(r'\s*\n\s*', ' ', re.sub(r'/\*.*?\*/', '', CSS_CONTENT, flags=re.S)).strip()
assert '</style' not in CSS_INLINE_CONTENT.lower()
CSS_INLINE = f'<style id="ac-blog-cta-style" data-css-version="{CSS_HASH}">{CSS_INLINE_CONTENT}</style>'
FONT_HREF = "/assets/fonts/be-vietnam-pro-extrabold.woff2"
FONT_PRELOAD = f'<link rel="preload" href="{FONT_HREF}" as="font" type="font/woff2" crossorigin>'
BLOCKS = ("top", "mid", "end")
DEPTH_TAGS = r"div|section|details|table|ul|ol|blockquote|figure|aside|nav|article"


def load_template():
    raw = (HERE / "template.html").read_text(encoding="utf-8")
    out = {}
    for name in BLOCKS:
        m = re.search(rf"<!--@{name}-->(.*?)<!--@/{name}-->", raw, re.S)
        out[name] = m.group(1).strip()
    return out


def sub_optional(html, name, keep):
    pat = re.compile(rf"<!--@{name}-->(.*?)<!--@/{name}-->", re.S)
    return pat.sub(lambda m: m.group(1) if keep else "", html)


def fill(html, values):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: html_utils.escape(str(values.get(m.group(1), "")), quote=True), html)


def normalized(value):
    value = value.lower().replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", value) if not unicodedata.combining(c))


def matches_keyword(hay, word):
    return bool(re.search(r"(?<!\w)" + re.escape(normalized(word)) + r"(?!\w)", hay))


def pick_product(cfg, slug, title):
    hay = normalized(f"{slug} {title}")
    for pid, words in cfg["product_by_keyword"].items():
        if any(matches_keyword(hay, w) for w in words):
            return pid
    return cfg["default_product"]


def url(cfg, pid, medium, slug, anchor=None):
    if anchor is not None:
        return '/' + anchor
    if cfg.get("link_mode") == "home":
        return "/" + cfg.get("home_anchor", "#shop")
    p = cfg["products"][pid]
    if cfg.get("link_mode") in ("fourthwall", "product"):
        # Legacy mode names must also stay on our own product pages.
        return p['product_url']
    # Same-site links keep the visitor's original acquisition source.
    return f"/{anchor or p['home_anchor']}"


def strip_blocks(html):
    return re.sub(rf"\s*<!-- {MARK}:(\w+) -->.*?<!-- /{MARK}:\1 -->\s*", "", html, flags=re.S)


def wrap(name, body):
    return f"\n<!-- {MARK}:{name} -->\n{body}\n<!-- /{MARK}:{name} -->\n"


def depth_at(html, start, positions):
    """Open-container depth (div/section/details/...) at each position, counted from start."""
    events = [(m.start(), -1 if m.group(1) else 1)
              for m in re.finditer(rf"<(/?)({DEPTH_TAGS})\b", html[start:])]
    out, d, i = [], 0, 0
    for pos in positions:
        while i < len(events) and start + events[i][0] < pos:
            d += events[i][1]; i += 1
        out.append(d)
    return out


def find_mid(html, start):
    """Position of an <h2> at the article's top level, ~55% through the body."""
    tail_markers = [html.find(x, start) for x in
                    ('class="seo-faq"', 'class="ac-reading-path"', "</article>")]
    end = min([p for p in tail_markers if p != -1] or [len(html)])
    cands = [start + m.start() for m in re.finditer(r"<h2[\s>]", html[start:end])]
    cands = [c for c in cands if "faq-title" not in html[c:c + 80]]
    if len(cands) < 4:
        return None
    depths = depth_at(html, start, cands)
    mode = max(set(depths), key=depths.count)      # depth shared by the real section headings
    valid = [i for i in range(2, len(cands)) if depths[i] == mode]
    if not valid:
        return None
    target = max(2, round(len(cands) * 0.55))
    return cands[min(valid, key=lambda k: abs(k - target))]


def process(path, lang, cfg, tpl, opts):
    html = path.read_text(encoding="utf-8")
    if not opts.remove:
        # Restyling or removing a related module must not move/drop an existing middle CTA.
        html = re.sub(r'\s*<!-- ac-cta:mid -->.*?<!-- /ac-cta:mid -->\s*', MID_POSITION, html, count=1, flags=re.S)
    html = strip_blocks(html)
    if opts.remove:
        html = re.sub(CSS_LINK_RE, "", html)
        html = re.sub(CSS_INLINE_RE, "", html, flags=re.S)
        html = re.sub(r'\s*<link\b[^>]*href="/assets/fonts/be-vietnam-pro-extrabold\.woff2"[^>]*>', "", html)
        return html, {"removed": True}

    intro = re.search(r'<section[^>]*class="[^"]*ac-article-intro[^"]*"[^>]*>.*?</section>', html, re.S)
    if not intro and re.search(r'<article\b', html):
        intro = re.search(r'<p\b[^>]*class="[^"]*\bintro\b[^"]*"[^>]*>.*?</p>', html, re.S)
    if not intro or "</article>" not in html:
        return None, {"skip": "no intro section / no </article> (hub or non-standard page)"}

    slug = path.stem
    title_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1)) if title_m else slug
    pid = pick_product(cfg, slug, title)
    a_id, b_id = list(cfg["products"])[:2]
    P, A, B = cfg["products"][pid], cfg["products"][a_id], cfg["products"][b_id]
    t = cfg["copy"][lang]

    if lang == "en" and opts.move_vi_link:
        m = re.search(r'<p><a href="([^"]+)" hreflang="vi" lang="vi">Read the Vietnamese original</a></p>', html)
        if m:
            html = html.replace(m.group(0), "", 1)
        html = html.replace(" · ENGLISH TRANSLATION", "", 1)

    hay = normalized(f"{slug} {title}")
    for rule in cfg.get("topic_lines", {}).get(lang, []):
        if any(matches_keyword(hay, w) for w in rule["keywords"]):
            t = dict(t, **{k: rule[k] for k in ("top_line", "mid_text", "mid_kicker") if k in rule})
            break

    def price(product):
        amount = re.search(r"\$[\d,.]+", product["price"])
        return (("Từ " if lang == "vi" else "From ") + amount.group(0) + " USD") if amount else product["price"]
    v = dict(t, p_name=P["name"], p_img=P["img"], p_price=price(P), p_description=P["description"][lang],
             a_name=A["name"], a_img=A["img"], a_alt=A["alt"], a_price=price(A), a_description=A["description"][lang],
             b_name=B["name"], b_img=B["img"], b_alt=B["alt"], b_price=price(B), b_description=B["description"][lang],
             url_top=url(cfg, pid, "top", slug),
             url_mid=url(cfg, pid, "mid", slug),
             url_end=url(cfg, pid, "end", slug, "#shop"),
             url_end_a=url(cfg, a_id, "end", slug), url_end_b=url(cfg, b_id, "end", slug),
             form_action=cfg.get("email_form_action", ""))
    out = {}
    for name in BLOCKS:
        h = tpl[name]
        if name == "end":
            h = sub_optional(h, "form", bool(v["form_action"]))
        out[name] = wrap(name, fill(h, v).strip())

    # VI: remove the old "App phoi do" box
    if lang == "vi" and not opts.keep_app_box:
        html = re.sub(r'<a\b[^>]*ac-blog-app-box[^>]*>.*?</a>', "", html, count=1, flags=re.S)

    preserved_mid = html.find(MID_POSITION)
    if preserved_mid != -1:
        html = html.replace(MID_POSITION, "", 1)
    intro = re.search(r'<section[^>]*class="[^"]*ac-article-intro[^"]*"[^>]*>.*?</section>', html, re.S)
    if not intro:
        intro = re.search(r'<p\b[^>]*class="[^"]*\bintro\b[^"]*"[^>]*>.*?</p>', html, re.S)
    main = re.search(r'<main\b[^>]*>', html)
    heading = re.search(r'<h1\b', html)
    pos_top = main.end() if main and main.end() < intro.start() else heading.start()
    pos_mid = preserved_mid if preserved_mid != -1 else find_mid(html, intro.end())
    rp = html.find('class="ac-reading-path"')
    if rp != -1:
        pos_end = html.rfind("<nav", 0, rp + 1)
    else:
        pos_end = html.rfind("</article>")

    # insert from the back so earlier offsets stay valid
    inserts = [(pos_end, "end")] + ([(pos_mid, "mid")] if pos_mid else []) + [(pos_top, "top")]
    for pos, name in inserts:
        html = html[:pos] + out[name] + html[pos:]
    # Load approved component rules after the article styles; one font preload.
    html = re.sub(CSS_LINK_RE, "\n", html)
    html = re.sub(CSS_INLINE_RE, "\n", html, flags=re.S)
    html = re.sub(r'\s*<link\b[^>]*href="/assets/fonts/be-vietnam-pro-extrabold\.woff2"[^>]*>\s*', "\n", html)
    html = re.sub(r'\s*</head>', lambda m: '\n' + FONT_PRELOAD + '\n' + CSS_INLINE + '\n</head>', html, count=1)
    return html, {"product": pid, "mid": bool(pos_mid)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="site root (folder with index.html)")
    ap.add_argument("--lang", choices=["en", "vi", "all"], default="en")
    ap.add_argument("--sample", type=int, help="only the first N eligible posts (preview)")
    ap.add_argument("--files", nargs="*", help="only these post filenames (e.g. what-is-goth-style.html)")
    ap.add_argument("--out", help="write modified copies here instead of touching the site")
    ap.add_argument("--write", action="store_true", help="modify the site files in place")
    ap.add_argument("--remove", action="store_true", help="strip all CTA blocks (rollback)")
    ap.add_argument("--keep-app-box", action="store_true", help="VI: do not remove the app-phoi-do box")
    ap.add_argument("--move-vi-link", action="store_true",
                    help="EN: remove the top 'ENGLISH TRANSLATION' label and 'Read the Vietnamese original' link")
    opts = ap.parse_args()

    root = Path(opts.root).resolve()
    if not (root / "index.html").exists():
        sys.exit(f"index.html not found in {root} - run from the site root or pass --root")
    if not (opts.out or opts.write):
        print("DRY RUN: nothing will be written. Use --out DIR to preview or --write to apply.\n")

    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    tpl = load_template()
    dirs = {"en": root / "en" / "blog", "vi": root / "blog"}
    langs = ["en", "vi"] if opts.lang == "all" else [opts.lang]

    stats = {"done": 0, "skipped": 0, "no_mid": 0}
    skipped = []
    for lang in langs:
        files = sorted(dirs[lang].glob("*.html"))
        if opts.files:
            files = [f for f in files if f.name in opts.files]
        n = 0
        for f in files:
            if opts.sample and n >= opts.sample:
                break
            new, info = process(f, lang, cfg, tpl, opts)
            if new is None:
                stats["skipped"] += 1
                skipped.append((f.relative_to(root).as_posix(), info["skip"]))
                continue
            n += 1
            stats["done"] += 1
            if not opts.remove and not info.get("mid"):
                stats["no_mid"] += 1
            if opts.write:
                f.write_text(new, encoding="utf-8")
            elif opts.out:
                dest = Path(opts.out) / f.relative_to(root)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(new, encoding="utf-8")
            print(f"{'OK  ' if True else ''}{f.relative_to(root).as_posix():70s} {info}")

    css_src = HERE.parents[1] / "assets" / "css" / "blog-shop-cta.css"
    css_dst = (root / "assets" / "css" / "blog-shop-cta.css")
    if css_src.exists() and css_src != css_dst:
        if opts.write and not opts.remove:
            shutil.copyfile(css_src, css_dst)
        elif opts.out:
            d = Path(opts.out) / "assets" / "css"; d.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(css_src, d / css_src.name)

    # Articles embed these rules inline; standalone CSS is only a preview export.
    if not opts.remove and opts.out:
        fingerprinted_css = Path(opts.out) / "assets" / "css" / CSS_FILENAME
        fingerprinted_css.parent.mkdir(parents=True, exist_ok=True)
        fingerprinted_css.write_text(CSS_CONTENT, encoding="utf-8", newline="\n")

    # Preview exports and alternate roots need the same self-hosted font assets.
    if not opts.remove:
        for filename in ("be-vietnam-pro-extrabold.woff2", "BeVietnamPro-OFL.txt"):
            src = HERE.parents[1] / "assets" / "fonts" / filename
            dst = (Path(opts.out) if opts.out else root) / "assets" / "fonts" / filename
            if src.exists() and src.resolve() != dst.resolve() and (opts.write or opts.out):
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)

    print(f"\nProcessed: {stats['done']}  Skipped: {stats['skipped']}  Posts without a mid CTA (too few sections): {stats['no_mid']}")
    for p, why in skipped[:12]:
        print(f"  skipped {p}: {why}")
    if len(skipped) > 12:
        print(f"  ... and {len(skipped) - 12} more skipped")


if __name__ == "__main__":
    main()
