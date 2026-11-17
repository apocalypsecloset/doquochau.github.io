# Exact VI link-fix successors — E0b

User-approved checkpoint after E0. Baseline: `9e16c2012f417cf5e4634b1c771a2c5d773e1ee8`; reviewed five-phase VI result: `6d8a9c4f13b59bc12e0db087a2779fbcfa2480db`.

`release-manifest.json` adds exact successor SHA-256 values for 426 existing VI articles, four new VI hubs and the VI Journal. It does not replace any earlier manifest or source hash. Hashes pin UTF-8 LF Git content and explicitly pin its CRLF checkout form; no whitespace trimming, DOM serialization or open-ended body normalization is accepted.

## Independent release gate

`python scripts/qa_link_fix.py` reconstructs the 426 existing articles from the baseline using the original exact old/new patch spans recorded in the reviewed VI commit. The four new pages start from their first creation commit, `985f5e3`. Every span must match a full before/after text pair in `link_changes.csv`. Twelve navigation-introduction spans previously present only in patch evidence were appended to the CSV; all previous records remain untouched.

The gate checks:

- Exact before/after hashes, unique old spans and exact replay: no unlogged change to any other byte.
- Original title/H1/meta/canonical/hreflang/JSON-LD/TOC/reading path/FAQ/sources are identical.
- Every original image and heading remains intact in its original order. The previous VI release added 159 images and 159 headings inside navigation cards; those additions are accepted only inside the exact logged spans. This is preservation of original nodes, not a claim that the total node count never increased.
- Every new or replaced link destination exists internally, fragments resolve and destinations are not redirect stubs.
- The Journal retains all 423 original cards unchanged and adds exactly the four approved hub URLs, for exactly 427 cards.
- All historical reviewed manifests, EN HTML, translation manifests and TSVs remain unchanged. An extra-character mutation is rejected by the successor recognizer.

The asset-map-backed image lists in the Vải and Kính sitemap entries are synchronized with their actual navigation cards. All 19 previously missing URLs already had HTTP-200 evidence and SHA-256 values in the existing asset map. No image hash or asset evidence was invented and no existing image was changed.

## Historical QA is separate from EN translation sources

`link_fix_release.historical(path, raw)` is used only at the historical-preservation comparison points of five QA scripts. It recognizes only a file's exact after hash and returns its exact old Git blob, whose before hash is checked too. Unknown successor bytes are returned unchanged and fail the old locks. The four exact new-hub contracts are checked by the independent release gate instead of looking for nonexistent historical blobs.

The original assertions remain enabled. `translation_inventory.sitemap_vi_urls()` includes only the four exact approved new VI hub successors; the original 216-row tracker and 218-pair inventory remain unchanged. This fixes inventory equality without accepting any new translation source hash.

**No successor has been added to `en_translate.source`, `en_translate_hubs.source`, `privacy_release.original`, `storefront_ux_release.original`, `blog_repair_release.original` or `reviewed_maintenance.predecessor`.** `en_source_successors` is empty and the new gate requires it to remain empty in E0b. All 215 original source locks remain intact; 210 still reject the updated VI sources. Thus 36 of 37 translation batches must remain red until E3 updates the corresponding TSV and EN HTML under a separately approved release. Batch19 has no changed source and may pass.

Website quality now exposes independent VI/general and English translation jobs. There is no `continue-on-error`, success substitution or skipped failed batch. All translation batches run and the EN job exits nonzero while any fail. This makes a green VI job distinguishable from the intentionally unresolved EN translation contract.

## User-approved next-phase decisions — not executed in E0b

- Stop and report VI/general CI at E0b. E1 cleanup and E2 hub creation follow only after that checkpoint; do not start E3 without explicit approval.
- Use batch40; batch39 already contains Solarpunk and White on White.
- EN hub slugs: `womens-color-coordination-guides`, `occasion-destination-outfit-guides`, `womens-clothing-care-guides`, `alternative-hair-makeup-guides`.
- Received the user's revised `internal_link_audit_en (1).py` and copied it byte-for-byte to `scripts/internal_link_audit_en.py` (SHA-256 `446ae17c22190d7de3851af134736dccf774430c528ef1ddaf4b14fabfa40e4c`). E7/E8 exempt each page's own VI original. The original E0 baseline and audit script remain archived unchanged; the revised audit output is recorded separately.

E0 evidence is in `data/en-link-e0-2026-11-17/`; E0b command outputs are in `data/en-link-e0b-2026-11-17/`. Work artifacts have not yet been moved out of `tools/` (E1).

## E1 archive locations

The active audits are now `scripts/internal_link_audit.py` and `scripts/internal_link_audit_en.py`. The VI task is `docs/CODEX_TASK.md`; historical work files and `link_changes.csv` are archived byte-for-byte under `data/link-fix-2026-11-17/`. References to `tools/` inside frozen patch evidence and old reports describe their original Git locations, not runnable current entrypoints. No new `/tools/*` header rule was added. Local dependencies moved to ignored `.venv/site-packages`.
