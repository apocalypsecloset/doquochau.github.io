# Translation checkpoint — 2026-11-04

- Latest published content: PR #51, master `df422586825d1eaf9a7e0b7c3d86e3faf713332e`.
- **159/216 full translation pairs published and production-verified; 57 pending.** Two additional EN-only originals make 161 English Journal cards.
- Batch32 adds ten complete translations: Business Casual, Smart Casual, Power Dressing, Preppy, Ivy, Classic, Casual Chic, Quiet Luxury, Old Money and Balletcore. All 1,662 indexed source text/alt segments are translated: 19,663 English article words, 181 headings, 51 original image placements, 13 tables and 46 FAQs.
- All 43 preview files and 43 production files match the reviewed local files byte-for-byte. All five checks on the production-master content commit succeeded. Evidence: `docs/qa/en-batch32-preview.json`, `en-batch32-production.json`, `en-batch32-release-checks.json`. Actual branch/master conclusions are separate; no override used.
- All 31 manifest gates pass. All ten VI sources match unmarked baseline bytes; all 216 original VI sitemap URLs remain. VI URL/slug/title/meta/canonical/body/images are preserved except marked bilingual additions.
- All 161 EN pages have one H1, self-canonical and unique titles/descriptions/canonicals. All 56 HTTP image endpoints pass. Twenty desktop/mobile views have no body overflow, all 13 tables scroll in wrappers, and the mobile Business Casual jeans FAQ opens with its complete visible answer. Old Money's long H1 wraps in the mobile viewport.
- Guarded maintenance promotes 47 links in 21 older EN pages. Each page's own VI links remain; these touches are not additional translations. The final scan finds zero eligible links and zero skipped pages.
- No GSC query × page access. Intent screening is editorial only: no confirmed cannibalization diagnosis, deletion, consolidation, redirect or noindex changes. Historical/reporting limits and garment-performance caveats are in `docs/en-translation-batch32.md`.
- Homepage/POD/Fourthwall/shop/routing/PR #9 untouched. Earlier evidence remains in batch28–31 reports; checkpoint149 was persisted through PR #50.

## Latest ten published English URLs

- https://apocalypsecloset.com/en/blog/business-casual-women-guide.html
- https://apocalypsecloset.com/en/blog/smart-casual-women-guide.html
- https://apocalypsecloset.com/en/blog/power-dressing-style-guide.html
- https://apocalypsecloset.com/en/blog/preppy-style-guide.html
- https://apocalypsecloset.com/en/blog/ivy-style-guide.html
- https://apocalypsecloset.com/en/blog/classic-style-women-guide.html
- https://apocalypsecloset.com/en/blog/casual-chic-style-guide.html
- https://apocalypsecloset.com/en/blog/quiet-luxury-style-guide.html
- https://apocalypsecloset.com/en/blog/old-money-style-guide.html
- https://apocalypsecloset.com/en/blog/balletcore-style-guide.html

## Next work

The CSV's 57 PENDING rows are the authoritative remaining inventory. No batch33 EN stubs or publication claims exist. Prioritize remaining alternative fit/proportion guides, boot maintenance and shopping decision guides before broader aesthetic expansions, after full-source and intent review. A provisional extraction attempt found `mua-sam-alt-fashion` unsupported by the current standard extractor; inspect its full layout before adding an adapter, preserving the entire article and all VI bytes. This is an implementation prerequisite for a future source, not a confirmed SEO defect.

## Resume

Fetch current master and reconcile concurrent work. Read this checkpoint, the full 216-row CSV and SEO guardrails before choosing 10–20 targets. Preserve VI URLs/title/meta/canonical/body/images except marked bilingual additions. Recheck English intent ownership against all existing pages. Read entire originals and references; translate every source text/alt segment with SHA locks. Generate all complete EN pages before sync; refresh links and run source/HTML/schema/image/metadata/canonical/hreflang/sitemap/Journal and desktop/mobile QA. Verify preview before normal PR merge, wait for deployment, compare production files and persist a checkpoint. Never count provisional plans, partial pages or maintenance touches as translations.


## Batch33 prepared — publication pending

Ten complete translations are locally implemented and QA passed: plus size, petite, slim frame, fuller stomach, pear shape, inverted triangle, petite baggy buying, boot odor, boot break-in and Shopee baby-tee buying. See `docs/en-translation-batch33.md`, its complete manifest/TSVs and QA evidence. Tracker: 159 MERGED, 10 COMPLETE_QA_PASSED, 47 PENDING. The production-verified count remains 159 until preview, normal merge, deployment checks and exact production comparison succeed. No partial EN stubs. Resume by completing this release before choosing another batch.
