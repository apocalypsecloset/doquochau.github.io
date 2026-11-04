# Translation checkpoint — 2026-11-04

- Latest published content: PR #44, master `3f0ee619d4c65697ddf67d84c4e7262002fed97a`.
- **119/216 full translation pairs published and production-verified; 97 not yet published.** Two EN-only originals are additional.
- Batch28 preview and production both match all 53 release files. All five master checks succeeded, including Workers Builds; branch Worker failure did not include diagnostics. Evidence: `docs/en-translation-batch28.md` and `docs/qa/en-batch28-*.json`.
- Batch29 has ten full translations, all locally QA-passed, awaiting PR preview, normal merge and deployed-file verification. Do not count them as published. Tracker: 119 MERGED, 10 COMPLETE_QA_PASSED, 87 PENDING. No empty/partial EN pages were created.
- Batch29: 20,329 English article words, 64 original image placements, 19 tables, 36 FAQs; all 28 manifest gates and 66 HTTP image endpoints pass. Twenty desktop/mobile views have no page overflow, and mobile FAQ interaction passes. See `docs/en-translation-batch29.md`.
- Every VI source URL/slug/title/meta/canonical/body/image stays intact except marked bilingual additions. All 216 VI sitemap URLs remain. Homepage, POD, Fourthwall, shop, routing and PR #9 untouched.
- No GSC query × page access: editorial screening only, no confirmed cannibalization or URL deletion/consolidation.

## Resume

Read current master, this checkpoint, the 216-row tracker and `docs/en-translation-seo-guardrails.md`. Reconcile concurrent merges. If batch29 is still open, inspect its latest head/checks, compare preview files, normal-merge only after QA, verify production, then update publication status. Full source-locked translations are in `data/en-translations/batch29.json` plus the ten corresponding TSV files. Intent plans are evidence only, never public EN stubs. Continue subsequent batches of 10–20 with full source review, intent differentiation, complete translation, guarded internal-link refresh, static/schema/image/source-preservation and desktop/mobile QA. Preserve each original-language link. Record durable publication counts and URLs only after verification.
