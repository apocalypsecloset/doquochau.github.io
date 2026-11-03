# Translation checkpoint — 2026-11-03

- Latest content release: PR #39, master `6a8c3288f7f76a0c83e094147d4786067a949b28`.
- **99/216 full translation pairs published and production-verified; 117 pending.** Two EN-only originals are additional: 101 Journal cards.
- Batch26: 18,766 English words, 205 headings, 68 original image placements, 15 tables and 50 FAQs. All 70 distinct original/responsive/shell image endpoints pass HTTP 200/image MIME.
- All 25 completed manifest gates pass. Twenty desktop/mobile views have no page overflow; tables scroll inside wrappers and concert FAQ opens with complete content.
- EN-only blazer source-order repair retains all content and image order. Ten VI pages byte-match baseline outside marked bilingual additions. All 216 VI sitemap URLs retained.
- Preview and final production checks both byte-match all 22 release files. Initial early checks saw deployment lag; final checks pass. Four exposed master checks succeeded; no Workers check appeared for this release.
- No GSC query × page access; editorial overlap screening only. No confirmed cannibalization, URL deletion or consolidation.
- Homepage/POD/Fourthwall/shop/routing/PR #9 untouched.
- Evidence: `docs/en-translation-batch26.md`, `docs/qa/en-batch26-*.json`, `data/en-translations/batch26.json`.

## Latest ten English URLs

- https://apocalypsecloset.com/en/blog/how-to-style-leather-skirts.html
- https://apocalypsecloset.com/en/blog/womens-denim-jacket-outfits.html
- https://apocalypsecloset.com/en/blog/womens-vest-layering-outfits.html
- https://apocalypsecloset.com/en/blog/how-to-style-pleated-skirts.html
- https://apocalypsecloset.com/en/blog/alternative-mini-skirt-outfits.html
- https://apocalypsecloset.com/en/blog/how-to-style-slip-dresses.html
- https://apocalypsecloset.com/en/blog/how-to-style-ballet-flats.html
- https://apocalypsecloset.com/en/blog/alternative-concert-outfits-for-women.html
- https://apocalypsecloset.com/en/blog/womens-black-blazer-outfits.html
- https://apocalypsecloset.com/en/blog/choosing-bags-for-alternative-outfits.html

## Batch27 working queue

Ten specialist sources selected; source-index TSV translations in progress. No batch27 page is published or added to sitemap before the whole batch passes QA.

- `/blog/phoi-do-voi-quan-jean-ong-suong-nu.html` → `/en/blog/womens-straight-leg-jeans-outfits.html`
- `/blog/phoi-do-voi-chan-vay-dai.html` → `/en/blog/how-to-style-long-skirts.html`
- `/blog/phoi-do-voi-chan-vay-chu-a.html` → `/en/blog/how-to-style-a-line-skirts.html`
- `/blog/quan-ong-rong-nu-phoi-voi-ao-gi.html` → `/en/blog/womens-wide-leg-trouser-outfits.html`
- `/blog/bodycon-dress-la-gi-cach-phoi.html` → `/en/blog/how-to-style-bodycon-dresses.html`
- `/blog/babydoll-dress-la-gi-cach-phoi.html` → `/en/blog/how-to-style-babydoll-dresses.html`
- `/blog/giay-loafer-nu-la-gi-cach-phoi.html` → `/en/blog/womens-loafer-outfit-ideas.html`
- `/blog/phoi-do-voi-ao-so-mi-nu.html` → `/en/blog/womens-shirt-outfit-ideas.html`
- `/blog/chan-vay-tennis-phoi-voi-ao-gi.html` → `/en/blog/tennis-skirt-outfit-ideas.html`
- `/blog/chan-vay-bi-ngo-phoi-voi-ao-gi.html` → `/en/blog/bubble-skirt-outfit-ideas.html`

Resume from current master, this checkpoint, the 216-row tracker and guardrails. Reconcile concurrent publications; retain existing slugs. Complete all source-index segments, generate the full batch, then run static, image, schema, local links, VI preservation, desktop/mobile, preview and production checks. Never count drafts as published.
