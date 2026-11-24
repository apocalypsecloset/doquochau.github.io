"""Migrate the published site to own-shop commerce. Dry run unless --write."""
import argparse
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AFF_URL = re.compile(r'https?://(?:s\.shopee\.vn|shope\.ee|go\.isclix\.com|[^/"\s]*accesstrade[^/"\s]*)[^"\s<>]*', re.I)
SHOP = '/?utm_source=outfits&utm_medium=shop-link#shop'
POLICY_EDITS = {
    '<h2>Đơn hàng Fourthwall và link Shopee</h2>': '<h2>Đơn hàng Fourthwall</h2>',
    '<h2>Fourthwall orders and Shopee links</h2>': '<h2>Fourthwall orders</h2>',
    'đơn hàng Fourthwall và Shopee có chính sách riêng.': 'đơn hàng Fourthwall có chính sách riêng.',
    'Fourthwall and Shopee orders have separate policies.': 'Fourthwall orders have separate policies.',
    'Một số link Shopee là affiliate; sau khi nhấp, Shopee hoặc mạng affiliate có thể dùng cookie và dữ liệu giới thiệu để ghi nhận hoa hồng. ': '',
    'Some Shopee links are affiliate links; after a click, Shopee or its affiliate network may use cookies and referral data for commission attribution. ': '',
    ' Link Shopee là sản phẩm bên ngoài, có thể là affiliate; người bán/Shopee xử lý giao dịch đó. Hai kênh mua hàng có chính sách riêng.': '',
    ' Shopee links lead to external items and may be affiliate links; Shopee/the seller handles those purchases under separate policies.': '',
}


def clean_anchor(m):
    attrs, body = m.group(1), m.group(2)
    if not AFF_URL.search(attrs):
        return m.group(0)
    # Outfit garments remain styling references. They are not products sold by us.
    attrs = re.sub(r'\s+(?:href|target|rel|aria-label)="[^"]*"', '', attrs)
    body = re.sub(r'<div class="item-arrow item-shop-cta">.*?</div>', '', body, flags=re.S)
    return f'<div{attrs}>{body}</div>'


def clean_html(html, is_outfit):
    html = re.sub(r'<span\b[^>]*class="ac-affiliate-note"[^>]*>.*?</span>', '', html, flags=re.S)
    html = re.sub(r'<a\b([^>]*)>(.*?)</a>', clean_anchor, html, flags=re.S)
    html = re.sub(r'\s*#Affiliate\b', '', html, flags=re.I)
    html = re.sub(r'<a\b[^>]*href="[^"\s]*[?&]tag=Affiliate"[^>]*>Affiliate</a>', '', html, flags=re.I)
    for old, new in POLICY_EDITS.items():
        html = html.replace(old, new)
    html = html.replace('Affiliate destinations, prices, stock, vouchers and sellers may change.', 'Product listings, prices, stock, vouchers and sellers may change.')
    html = html.replace('Link affiliate, giá, tồn kho, voucher và người bán có thể thay đổi.', 'Listing sản phẩm, giá, tồn kho, voucher và người bán có thể thay đổi.')
    if is_outfit:
        html = html.replace('Chọn món bạn cần để xem sản phẩm phù hợp trên Shopee.', 'Tham khảo các món trong look và tận dụng trang phục bạn đã có.')
        html = html.replace('DANH SÁCH MUA ĐỒ', 'CÁC MÓN TRONG LOOK')
        html = html.replace('Nếu không cần mua đủ 6 món, hãy ưu tiên ba món này trước;', 'Hãy tận dụng trang phục sẵn có và bắt đầu với ba món này;')
        html = re.sub(r'<p class="shop-disclosure">.*?</p>',
                      '<p class="shop-disclosure">Các món trong ảnh là gợi ý phối đồ. '
                      f'<a href="{SHOP}">Xem áo thiết kế của Apocalypse Closet</a>.</p>', html, flags=re.S)
    return html


def product_links(html, cfg):
    """Product cards go to the named product; collection buttons keep the shop route."""
    def block(m):
        body = m.group(0)
        if m.group(1) == 'mid':
            pid = next((pid for pid, p in cfg['products'].items()
                        if f'class="ac-bcta__title">{p["name"]}</p>' in body), None)
            if pid:
                body = re.sub(r'href="([^"]+)"', lambda a: direct(a, pid), body)
        elif m.group(1) == 'end':
            def tile(t):
                pid = next(pid for pid, p in cfg['products'].items() if p['name'] in t.group(0))
                return re.sub(r'href="([^"]+)"', lambda a: direct(a, pid), t.group(0))
            body = re.sub(r'<a class="ac-bcta__tile".*?</a>', tile, body, flags=re.S)
        return body
    def direct(m, pid):
        u = urlsplit(m.group(1).replace('&amp;', '&'))
        query = '?' + u.query.replace('&', '&amp;') if u.query else ''
        return 'href="' + cfg['products'][pid]['product_url'] + query + '"'
    return re.sub(r'<!-- ac-cta:(\w+) -->.*?<!-- /ac-cta:\1 -->', block, html, flags=re.S)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    cfg_path = HERE / 'config.json'
    cfg = json.loads(cfg_path.read_text(encoding='utf8'))
    cfg['link_mode'] = 'product'
    spec = importlib.util.spec_from_file_location('inject', HERE / 'inject_cta.py')
    inject = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inject)
    opts = SimpleNamespace(remove=False, move_vi_link=True, keep_app_box=False)
    tpl = inject.load_template()
    changed, added, removed = [], [], 0
    files = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files'], text=True).splitlines()
    for f in files:
        p = ROOT / f
        if p.suffix not in ('.html', '.js', '.json') or f.startswith(('docs/', 'data/', 'tools/', 'cloudflare/')):
            continue
        old = p.read_text(encoding='utf8')
        new = old
        if p.suffix == '.html':
            new = clean_html(new, f.startswith('outfits/'))
            if f in ('privacy.html', 'en/privacy.html', 'terms.html', 'en/terms.html'):
                new = new.replace('Cập nhật ngày 16/11/2026.', 'Cập nhật ngày 20/11/2026.').replace('Updated November 16, 2026.', 'Updated November 20, 2026.')
            if p.parent in (ROOT / 'blog', ROOT / 'en/blog') and '<article' in new:
                if '<!-- ac-cta:top -->' not in new:
                    # Process the cleaned source through a temporary read adapter.
                    class Source:
                        stem = p.stem
                        def read_text(self, **kwargs): return new
                    result, info = inject.process(Source(), 'en' if f.startswith('en/') else 'vi', cfg, tpl, opts)
                    if result is None:
                        raise ValueError(f'Article without a supported intro: {f}')
                    new = result
                    added.append(f)
                new = product_links(new, cfg)
            # Bust caches for modified data and app scripts.
            new = re.sub(r'((?:style-outfits-[\w-]+|outfits|outfit-stylist-v2)\.js)\?[^"\s<>]+', r'\1?v=20261120-ownshop', new)
        elif p.suffix == '.js':
            new = re.sub(r',\s*"link"\s*:\s*"' + AFF_URL.pattern + r'"', '', new, flags=re.I)
            new = new.replace('Nhấn vào từng mục để xem chi tiết sản phẩm.', 'Tham khảo các món để phối cùng trang phục bạn đã có.')
            new = new.replace('XEM SẢN PHẨM TRONG LOOK →', 'XEM CHI TIẾT LOOK →').replace('ĐẾN PHẦN MUA ITEM', 'XEM CÁC MÓN PHỐI ĐỒ')
            if f == 'assets/js/outfit-stylist-v2.js':
                new = new.replace('XEM CÁC MÓN PHỐI ĐỒ</a></div>', 'XEM CÁC MÓN PHỐI ĐỒ</a><a href="' + SHOP + '">XEM ÁO APOCALYPSE CLOSET</a></div>')
        elif f.startswith('assets/journal/'):
            new = re.sub(r'\s*#Affiliate\b', '', new, flags=re.I)
        if AFF_URL.search(new):
            raise ValueError(f'Unhandled affiliate URL in {f}')
        removed += len(AFF_URL.findall(old))
        if old != new:
            changed.append(f)
            if args.write:
                p.write_bytes(new.encode('utf8'))
    if args.write:
        cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'mode': 'write' if args.write else 'dry-run', 'changed': len(changed),
                      'affiliate_urls_removed': removed, 'articles_added': added}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
