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

A separate reviewed change promotes completed English counterparts in older EN articles/collections. Original-language links are preserved, including both handcrafted initial translations. This maintenance adds no translations to the count. See `docs/en-internal-link-refresh.md`; production verification status is recorded there. PR #42 (`1109ede1c781c3d03e9ff556b1e0cb153290fb26`) is merged; all 82 updated EN files byte-match preview and production. All four exposed master checks pass.

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

## Batch28 ready for release

Ten full translations are implemented and locally QA-passed in `data/en-translations/batch28.json`. They are not counted as published yet. See `docs/en-translation-batch28.md` and `docs/qa/en-batch28-*.json`. All 63 distinct HTTP image endpoints pass. The 10 VI sources preserve every byte outside bilingual additions. Preview/deployment verification and publication checkpoint are next.

## Resume procedure

Read current master, this checkpoint, the full 216-row tracker and guardrails; reconcile concurrent publications. Preserve all existing slugs and Vietnamese source metadata/body outside bilingual additions. Translate full batches of 10–20. After all EN pages exist and sync is complete, run `refresh_en_internal_links.py --apply --report <batch evidence path>` before regression QA, so older English pages link to newly available counterparts. The helper preserves every link to each page's own VI original. QA all changed HTML, schemas, links, original image assets and mobile/desktop behavior before PR/merge. Verify preview and deployed files before recording publication. For current shopping/price/availability guidance, use verified current primary sources rather than carrying old product claims forward.

## Batch28 wrapped source adapter

The full wrapped night-out article is now extracted without losing trailing content or duplicating its H1, intro or cover. Source preservation and tag-count parity are recorded in `docs/qa/en-batch28-wrapped-extraction.json`. No Vietnamese source structure changes were made.

## Session completion evidence

- Batches25–27 published 30 full English translations: 52,326 English words, 197 original image placements, 32 tables and 128 FAQs. Each batch passed source-preservation, schema/link/canonical/hreflang, image, desktop/mobile, preview and deployed-file checks.
- Internal maintenance promoted 354 links in 82 EN pages; all original-language links remain intact. The two handcrafted initial translations and the two EN-only originals were not modified. No remaining eligible completed-counterpart references were found on a second helper run.
- All 111 EN files have one H1 and a self-canonical, without duplicate title, meta description or canonical values. This does not establish or exclude query-level cannibalization; GSC access is still unavailable.
- Durable inventory: `data/en-216-keyword-intent-audit.csv` contains exactly 109 MERGED and 107 PENDING rows. The 216 original VI URLs match the VI sitemap set.
