# Translation checkpoint — 2026-11-04

- Latest published content: PR #47, master `2441619bfbf2d13cbcbc581fafa54fe6b973a1a2`.
- **139/216 full translation pairs published and production-verified; 77 pending.** Two EN-only originals are additional: 141 English Journal cards.
- This continuation completed batches28–30: 30 full translations, 57,034 English article words, 193 original image placements, 52 tables and 134 FAQs. Each batch has source-preservation, schema/link/canonical/hreflang, image, desktop/mobile, preview and production evidence.
- Batch28: PR #44, `3f0ee619d4c65697ddf67d84c4e7262002fed97a`; all 53 preview/production files match and all five master checks succeeded.
- Batch29: PR #45, `4762abb52ff2d35ae95ae5853ee88b16a3eb4e8e`; all 40 preview/production files match and all five master checks succeeded. PR #46 persisted checkpoint129.
- Batch30: PR #47; all 41 preview/production files match and all five master checks succeeded. All 29 manifest gates and 71 HTTP image endpoints pass. Twenty desktop/mobile views have no body overflow; mobile FAQ interaction passes.
- The 216-row tracker contains exactly 139 MERGED and 77 PENDING, with no incomplete public EN pages. All original VI sitemap URLs remain. VI titles, metadata, canonicals, URLs, bodies and images remain byte-identical outside marked bilingual additions for these batches.
- Full translations and source locks: `data/en-translations/batch28.json`, `batch29.json`, `batch30.json` and their TSV files. Evidence: `docs/en-translation-batch28.md`, `docs/en-translation-batch29.md`, `docs/en-translation-batch30.md` and `docs/qa/en-batch28-*.json` through `en-batch30-*.json`.
- Guarded link maintenance promoted 138 links across 31+18+19 older-page touches in these releases. Those are maintenance touches, not extra translations or necessarily distinct pages. Every original-language link stays. The final read-only scan finds zero eligible links and zero skipped pages.
- All 141 EN pages have one H1 and self-canonical, with unique titles, descriptions and canonicals. No GSC query × page access: editorial screening only, no confirmed cannibalization diagnosis or URL consolidation.
- Homepage/POD/Fourthwall/shop/routing/PR #9 untouched. Branch Workers failures lacked diagnostic details; reports distinguish them from successful production-master checks.

## Latest ten published English URLs

- https://apocalypsecloset.com/en/blog/what-are-parachute-pants.html
- https://apocalypsecloset.com/en/blog/what-are-baggy-pants.html
- https://apocalypsecloset.com/en/blog/what-are-jogger-pants.html
- https://apocalypsecloset.com/en/blog/what-is-athleisure.html
- https://apocalypsecloset.com/en/blog/acubi-style-guide.html
- https://apocalypsecloset.com/en/blog/gorpcore-style-guide.html
- https://apocalypsecloset.com/en/blog/downtown-girl-style-guide.html
- https://apocalypsecloset.com/en/blog/model-off-duty-style-guide.html
- https://apocalypsecloset.com/en/blog/sporty-chic-style-guide.html
- https://apocalypsecloset.com/en/blog/blokecore-style-guide.html

## Batch31 unpublished checkpoint

The ten-topic provisional queue is `data/en-intent-plans/batch31.json`: Office Siren, Avant-garde, Rockabilly, Light Academia, Fairycore, Angelcore, Mermaidcore, Mori Kei, Ouji and Cottagecore. All remain PENDING. Office Siren has a full 188-entry text/alt draft at `data/en-translation-drafts/batch31/office-siren-la-gi.tsv`; index coverage passes, but generated-page/publication QA is not complete. The other nine are outline-only plans. No batch31 public EN pages or hreflang additions exist; drafts do not increase the 139 published count. See the draft README for source lock, reference dates and editorial cautions.

## Resume

Read current master, this checkpoint, the full 216-row tracker and `docs/en-translation-seo-guardrails.md`; reconcile concurrent merges before choosing the next batch. Preserve all existing VI URLs/slug/title/meta/canonical/body except bilingual additions. Translate full batches of 10–20. Recheck source hashes and target intents for the batch31 drafts. After all EN files exist and sync is complete, run the guarded internal-link refresh, then static/schema/image/source-preservation and desktop/mobile QA. Normal-merge only after QA; verify preview and deployed files before marking publication. Never count provisional plans, incomplete pages or maintenance link changes as translations. Check current primary sources for shopping, prices or availability rather than carrying old claims forward.
