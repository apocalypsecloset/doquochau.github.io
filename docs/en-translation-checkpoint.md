# Translation checkpoint — 2026-11-03

- Latest content release: PR #37, master `e4dd2bf4b44ed01ae7cc1efe75f84c71dcf49f3c`.
- **89/216 full translation pairs published and production-verified; 127 pending.** Two EN-only originals are additional: 91 English Journal cards.
- Batch25: 18,395 English words, 247 headings, 61 original image placements, 10 tables, 39 FAQs. All 66 distinct image endpoints passed HTTP/MIME checks.
- All 24 completed manifest release gates pass. Twenty desktop/mobile views have no page overflow; mobile tables scroll within their wrappers and FAQ opens correctly.
- Ten VI source files match baseline outside marked bilingual additions. All 216 VI sitemap URLs retained. Journal has 91 unique sequential cards in the actual reading grid.
- Cloudflare preview and production both byte-match all 22 release files. Initial production checks were early; final checks after deployment pass. Four exposed master checks succeeded; no Workers check was exposed for this release.
- No GSC query × page access. Editorial intent screening only; no confirmed cannibalization, URL deletion or consolidation.
- Homepage/POD/Fourthwall/shop/routing and PR #9 untouched.
- Evidence: `docs/en-translation-batch25.md`, `docs/qa/en-batch25-*.json`, `data/en-translations/batch25.json`.

## Latest ten English URLs

- https://apocalypsecloset.com/en/blog/what-are-mary-jane-shoes.html
- https://apocalypsecloset.com/en/blog/how-to-style-leg-warmers.html
- https://apocalypsecloset.com/en/blog/coquette-vs-dark-coquette.html
- https://apocalypsecloset.com/en/blog/what-is-indie-sleaze.html
- https://apocalypsecloset.com/en/blog/what-is-techwear.html
- https://apocalypsecloset.com/en/blog/cyber-y2k-style-outfits.html
- https://apocalypsecloset.com/en/blog/what-is-visual-kei.html
- https://apocalypsecloset.com/en/blog/devilcore-aesthetic-outfits.html
- https://apocalypsecloset.com/en/blog/morute-aesthetic-outfits.html
- https://apocalypsecloset.com/en/blog/gurokawa-creepy-cute-outfits.html

## Batch26 working queue

Ten source pages selected and read for specialist intent differentiation; none of batch26 is published or wired into the sitemap until all translations and QA pass. Partial source-index TSV work must remain draft-only.

- `/blog/phoi-do-voi-chan-vay-da.html` → `/en/blog/how-to-style-leather-skirts.html`
- `/blog/phoi-do-voi-ao-khoac-jean-nu.html` → `/en/blog/womens-denim-jacket-outfits.html`
- `/blog/phoi-do-voi-ao-gile-nu.html` → `/en/blog/womens-vest-layering-outfits.html`
- `/blog/phoi-do-voi-chan-vay-xep-ly.html` → `/en/blog/how-to-style-pleated-skirts.html`
- `/blog/phoi-do-voi-vay-ngan-nu.html` → `/en/blog/alternative-mini-skirt-outfits.html`
- `/blog/slip-dress-la-gi-cach-phoi.html` → `/en/blog/how-to-style-slip-dresses.html`
- `/blog/ballet-flats-la-gi-cach-phoi.html` → `/en/blog/how-to-style-ballet-flats.html`
- `/blog/outfit-nu-ca-tinh-di-concert.html` → `/en/blog/alternative-concert-outfits-for-women.html`
- `/blog/phoi-do-voi-ao-blazer-den-nu.html` → `/en/blog/womens-black-blazer-outfits.html`
- `/blog/cach-chon-tui-cho-outfit-nu-ca-tinh.html` → `/en/blog/choosing-bags-for-alternative-outfits.html`

Resume by reading current master, this checkpoint, the 216-row tracker and guardrails. Reconcile concurrent releases. Preserve all existing slugs. Complete the entire next batch and run static, image, schema, link, desktop/mobile and VI-preservation QA before PR/merge. Do not regenerate earlier published EN files solely to refresh links.
