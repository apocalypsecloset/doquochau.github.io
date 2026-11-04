# Translation checkpoint — 2026-11-04

- Latest published content: PR #49, master `796fd146ee310ab63d1e3b0b3cfc0b0e6c6f6bf4`.
- **149/216 full translation pairs published and production-verified; 67 pending.** Two additional EN-only originals make 151 English Journal cards.
- Batch31 adds ten full translations: Office Siren, Avant-garde, Rockabilly, Light Academia, Fairycore, Angelcore, Mermaidcore, Mori Kei, Ouji and Cottagecore. All 1,527 indexed source text/alt segments are translated: 19,688 English article words, 263 headings, 61 original image placements, three tables and 25 FAQs.
- All 35 preview files and 35 production files match the reviewed local files byte-for-byte. All five checks on the production-master content commit succeeded. Evidence: `docs/qa/en-batch31-preview.json`, `en-batch31-production.json`, `en-batch31-release-checks.json`. Branch/master conclusions are recorded separately; no override was used.
- All 30 manifest gates pass. All ten original VI files are byte-identical outside marked bilingual additions; all 216 original VI sitemap URLs remain. VI URL/slug/title/meta/canonical/body/images are preserved.
- All 151 EN pages have one H1, self-canonical and unique title/description/canonical. All 66 distinct HTTP image endpoints pass. Twenty desktop/mobile views have no body overflow, tables scroll, and the mobile Office Siren glasses FAQ opens with a complete visible answer. Mobile Cottagecore H1 wraps inside the viewport.
- Guarded maintenance promotes 21 links in 13 older EN pages; each page's own VI links remain. Those touches are not extra translations. The final scan finds zero eligible links and zero skipped pages.
- No GSC query × page access is available. Intent screening is editorial only; no confirmed cannibalization diagnosis, deletion, consolidation, redirect or noindex changes. Community-history limits and dated trend reporting are documented in `docs/en-translation-batch31.md`.
- Homepage/POD/Fourthwall/shop/routing/PR #9 untouched. Earlier release details remain in batch28–30 reports; checkpoint139 was persisted through PR #48. The old Office Siren draft is archived; use the reviewed normal manifest.

## Latest ten published English URLs

- https://apocalypsecloset.com/en/blog/office-siren-style-guide.html
- https://apocalypsecloset.com/en/blog/avant-garde-fashion-guide.html
- https://apocalypsecloset.com/en/blog/rockabilly-style-guide.html
- https://apocalypsecloset.com/en/blog/light-academia-style-guide.html
- https://apocalypsecloset.com/en/blog/fairycore-style-guide.html
- https://apocalypsecloset.com/en/blog/angelcore-style-guide.html
- https://apocalypsecloset.com/en/blog/mermaidcore-style-guide.html
- https://apocalypsecloset.com/en/blog/mori-kei-style-guide.html
- https://apocalypsecloset.com/en/blog/ouji-fashion-guide.html
- https://apocalypsecloset.com/en/blog/cottagecore-style-guide.html

## Next batch32: provisional, not translated

`data/en-intent-plans/batch32.json` records ten PENDING sources: Business Casual, Smart Casual, Power Dressing, Preppy, Ivy, Classic, Casual Chic, Quiet Luxury, Old Money and Balletcore. These are outline-screened plans only. Full-source editorial review, translation and all publication gates remain. No EN stubs or bilingual additions exist for this next queue, and it does not increase the 149 count.

## Resume

Fetch current master and reconcile concurrent work. Read this checkpoint, the 216-row CSV and SEO guardrails before choosing targets. Preserve VI URLs, title, metadata, self-canonical, body and images except marked bilingual additions. Translate complete batches of 10–20 with source SHA locks. Recheck next-batch target intents against all existing EN pages; read entire originals and references before drafting. Generate all complete EN pages before sync; then refresh links and run source/HTML/schema/image/metadata/canonical/hreflang/sitemap/Journal and desktop/mobile QA. Verify preview before normal PR merge, wait for production deployment, compare released files and persist a checkpoint. Never count plans, partial pages or maintenance touches as translations.
