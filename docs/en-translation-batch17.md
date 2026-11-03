# English translation release 17 — Capsule Wardrobe (2026-11-03)

## Scope
- VI original `/blog/capsule-wardrobe-la-gi.html` → EN counterpart `/en/blog/what-is-a-capsule-wardrobe.html`.
- Expected post-merge: **45/216** full VI→EN translations, **171 pending**, plus two English-only originals.
- Primary search intent: how a capsule wardrobe works and how to build one with distinctive dark-fashion foundations, distinct from Minimalist Style or product shopping.

## Full translation and source lock
- Original VI SHA-256 `348413ac11b842ff8582ae83f3148acc070a9e9bb9b266f88581ae0cd0028c0e`; VI content/metadata/canonical byte-identical outside marked hreflang and visible language link.
- 117 source text and alt-image segments translated, including full source tables, editorial guides, practical shopping criteria, seasonal notes for Vietnam, all 3 FAQ answers and original historical references.
- Exact structural parity: 15 H2, 3 H3, one 3-column comparison table with 5 rows, 6 original editorial images (including cover) in the same src order, 5 figures/captions, 18 list entries, one blockquote and three FAQs.
- Three visible FAQs exactly match FAQPage JSON-LD. Original external sources (Vogue and Washington Post) preserved.

## Bilingual SEO QA
- One English H1, EN self canonical, reciprocal VI/EN hreflang, BlogPosting/FAQPage/Breadcrumb schema.
- Sitemap retains all 216 VI blog URLs and has 47 EN blog URLs total (45 translated pairs plus two original English articles); no duplicates.
- No broken in-page anchors or linked local HTML destinations missing from sitemap. English Journal links to new EN page.
- Cloudflare Pages successful on branch head 82e1655d9d839a25b170ca85caba63add698d6bb.

## Not independently verified
- Live mobile 390px / desktop 1440px visual rendering, production HTTP/images, standalone Python QA and Search Console query×page overlap. Workers preview failed as on previous branches despite no Worker changes.
- No changes to shop, POD, checkout, homepage, Fourthwall, or original Vietnamese SEO metadata.
