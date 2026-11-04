# Translation checkpoint — 2026-11-04

- Latest published content: PR #45, master `4762abb52ff2d35ae95ae5853ee88b16a3eb4e8e`.
- **129/216 full translation pairs published and production-verified; 87 pending.** Two EN-only originals are additional: 131 English Journal cards.
- This work completed batches28–29: 20 full translations, 38,241 English article words, 132 original image placements, 36 tables and 86 FAQs. Each batch has full source-preservation, schema/link/canonical/hreflang, image, desktop/mobile, preview and production evidence.
- Batch28: PR #44, `3f0ee619d4c65697ddf67d84c4e7262002fed97a`; all 53 preview/production files match and all five master checks succeeded.
- Batch29: PR #45; all 40 preview/production files match. All 28 manifest gates and 66 HTTP image endpoints pass. Twenty desktop/mobile views have no body overflow; mobile FAQ interaction passes. Master checks are recorded in `docs/qa/en-batch29-release-checks.json`.
- The 216-row tracker contains exactly 129 MERGED and 87 PENDING, with no incomplete EN pages. All original VI sitemap URLs remain. VI titles, metadata, canonicals, URLs, bodies and images remain byte-identical outside marked bilingual additions for these batches.
- Full translations and source locks: `data/en-translations/batch28.json`, `batch29.json` and their TSV files. Evidence: `docs/en-translation-batch28.md`, `docs/en-translation-batch29.md`, `docs/qa/en-batch28-*.json`, `docs/qa/en-batch29-*.json`.
- Guarded link maintenance promoted 99 links in 31+18 older-page touches across these releases. Those are maintenance touches, not extra translations or necessarily distinct pages. Every original-language link stays. No eligible completed-counterpart links remain after the final scan.
- All 131 EN pages have one H1 and self-canonical, with unique titles, descriptions and canonicals. No GSC query × page access: editorial screening only, no confirmed cannibalization diagnosis or URL consolidation.
- Homepage/POD/Fourthwall/shop/routing/PR #9 untouched. Branch Workers failures lacked diagnostic details; preserve the actual branch/master distinction in reports.

## Latest ten published English URLs

- https://apocalypsecloset.com/en/blog/alternative-cafe-outfits-women.html
- https://apocalypsecloset.com/en/blog/alternative-wedding-guest-outfits-women.html
- https://apocalypsecloset.com/en/blog/alternative-beach-outfits-women.html
- https://apocalypsecloset.com/en/blog/airport-outfits-women.html
- https://apocalypsecloset.com/en/blog/femme-fatale-aesthetic-style-guide.html
- https://apocalypsecloset.com/en/blog/what-are-low-rise-pants.html
- https://apocalypsecloset.com/en/blog/what-is-a-crop-top.html
- https://apocalypsecloset.com/en/blog/leggings-outfit-ideas-women.html
- https://apocalypsecloset.com/en/blog/parachute-pants-outfits-women.html
- https://apocalypsecloset.com/en/blog/baggy-pants-outfits-women.html

## Batch30 ready for release

Ten full translations are implemented and locally QA-passed in `data/en-translations/batch30.json`. They are not counted as published yet. Tracker: 129 MERGED, 10 COMPLETE_QA_PASSED, 77 PENDING. See `docs/en-translation-batch30.md` and its QA evidence. Next: PR preview comparison, normal merge, production verification and publication checkpoint.

## Resume

Read current master, this checkpoint, the full 216-row tracker and `docs/en-translation-seo-guardrails.md`; reconcile concurrent merges before choosing the next batch. Preserve all existing VI URLs/slug/title/meta/canonical/body except bilingual additions. Translate full batches of 10–20. After all EN files exist and sync is complete, run the guarded internal-link refresh, then static/schema/image/source-preservation and desktop/mobile QA. Normal-merge only after QA; verify preview and deployed files before marking publication. Never count provisional plans, empty EN stubs or maintenance link changes as translations. For current shopping, prices or availability, check current primary sources rather than carrying old claims forward.
