# Own-shop migration — November 20, 2026

All 848 articles (423 Vietnamese and 425 English) promote Apocalypse Closet tees.
All article CTA images and buttons now open the homepage shop section (/#shop).
The homepage catalog opens the named product pages on apocalypsecloset.com.
Fourthwall supplies the existing API and checkout; product browsing stays on the main domain.
Six short articles retain top and final CTAs without a middle block.

Affiliate URLs, disclosures and tags were removed from published HTML, outfit data
and journal payloads. The 136 outfit pages preserve the illustrated garments as
styling references, with a separate link to the original tee shop. The outfit app
keeps its recommendations and quick view, with a shop link in the drawer.
Privacy and terms copy no longer describes an affiliate channel.

## Maintenance

From the repository root:

```powershell
python -X utf8 tools/blog-cta/remove_affiliate.py
python -X utf8 tools/blog-cta/remove_affiliate.py --write
python -X utf8 tools/blog-cta/verify_own_shop.py
```

Verification prints JSON to stdout. Use --report PATH to save a local report;
generated reports are not tracked or published with the website.

The migration defaults to a dry run and is idempotent. The CTA injector now
supports the four English editorial articles with paragraph introductions.
`config.json` uses `link_mode: product` for direct product-card destinations.

Verification compares article headings, canonical and language links, outfit
counts, and styling references with Git HEAD. It scans published sources for
affiliate remnants and checks JSON, structured data and local script paths.
The machine-readable result is `own-shop-verification.json`.

DOM checks also passed on representative Vietnamese and English articles and an
outfit page. The app produced three recommendations, opened quick view and
displayed its own-shop link. Seven changed JavaScript files passed `node --check`.
Visual browser QA was unavailable because the preview browser could not reach
the local server. These changes have not been deployed.
