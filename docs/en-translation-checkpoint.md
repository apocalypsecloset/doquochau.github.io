# Translation checkpoint — 2026-11-04

- Latest content release: PR #41, master `f1471c263c4596af0cc9749314309f35b2b778ad`.
- **109/216 full translation pairs published and production-verified; 107 pending.** Two EN-only originals are additional: 111 English Journal cards.
- This work session completed batches25–27: 30 full translations through PRs #37, #39 and #41. Each has its own intent mapping, source preservation, static/schema/link/image/responsive evidence, preview and production reports.
- Batch27: 15,165 English words, 266 headings, 68 original image placements, seven tables, 39 FAQs. All 65 distinct image endpoints pass HTTP/MIME checks.
- All 26 completed manifest gates pass. Twenty browser views at 1440px/390px show no page overflow; tables scroll within wrappers and the bodycon FAQ opens with a visible complete answer.
- Ten VI sources match baseline outside marked English alternate/language-link additions. All 216 VI sitemap URLs remain. Journal cards are unique, sequential, and inside the reading grid.
- Preview and final production reports match all 22 release files. Initial early checks saw deployment lag; final checks pass. Four exposed master checks succeeded. No Workers check appeared for this release.
- No GSC query × page access. Editorial overlap screening only; no confirmed cannibalization, URL deletion or consolidation.
- Homepage, POD, Fourthwall, shop, routing and PR #9 untouched.
- Evidence: `docs/en-translation-batch27.md`, `docs/qa/en-batch27-*.json`, `data/en-translations/batch27.json`.

## Internal English link refresh

A separate reviewed change promotes completed English counterparts in older EN articles/collections. Original-language links are preserved, including both handcrafted initial translations. This maintenance adds no translations to the count. See `docs/en-internal-link-refresh.md`; production verification status is recorded there.

## Latest ten published English URLs

- https://apocalypsecloset.com/en/blog/womens-straight-leg-jeans-outfits.html
- https://apocalypsecloset.com/en/blog/how-to-style-long-skirts.html
- https://apocalypsecloset.com/en/blog/how-to-style-a-line-skirts.html
- https://apocalypsecloset.com/en/blog/womens-wide-leg-trouser-outfits.html
- https://apocalypsecloset.com/en/blog/how-to-style-bodycon-dresses.html
- https://apocalypsecloset.com/en/blog/how-to-style-babydoll-dresses.html
- https://apocalypsecloset.com/en/blog/womens-loafer-outfit-ideas.html
- https://apocalypsecloset.com/en/blog/womens-shirt-outfit-ideas.html
- https://apocalypsecloset.com/en/blog/tennis-skirt-outfit-ideas.html
- https://apocalypsecloset.com/en/blog/bubble-skirt-outfit-ideas.html

## Proposed batch28: ten pending sources

No batch28 English pages or placeholder URLs have been created. Confirm current source and intent before choosing final English slugs.

- `/blog/phoi-do-voi-chan-vay-jean-ngan.html`
- `/blog/phoi-do-voi-chan-vay-jean-dai.html`
- `/blog/phoi-do-voi-chan-vay-xoe.html`
- `/blog/phoi-do-voi-chan-vay-duoi-ca.html`
- `/blog/phoi-do-voi-ao-tre-vai-nu.html`
- `/blog/ao-ong-nu-phoi-voi-gi.html`
- `/blog/phoi-do-nu-ca-tinh-mua-he.html`
- `/blog/phoi-do-nu-ca-tinh-di-choi.html`
- `/blog/outfit-di-choi-dem-badgirl.html`
- `/blog/phoi-do-voi-quan-tay-ong-suong-nu.html`

## Resume procedure

Read current master, this checkpoint, the full 216-row tracker and guardrails; reconcile concurrent publications. Preserve all existing slugs and Vietnamese source metadata/body outside bilingual additions. Translate full batches of 10–20. After all EN pages exist and sync is complete, run `refresh_en_internal_links.py --apply --report <batch evidence path>` before regression QA, so older English pages link to newly available counterparts. The helper preserves every link to each page's own VI original. QA all changed HTML, schemas, links, original image assets and mobile/desktop behavior before PR/merge. Verify preview and deployed files before recording publication. For current shopping/price/availability guidance, use verified current primary sources rather than carrying old product claims forward.
