# English translation release 05B — source-audited

## Scope
- Baseline 33/216 completed translations.
- Release one complete English counterpart `/en/blog/womens-leather-jacket-outfits.html` from `/blog/phoi-do-voi-ao-khoac-da-nu.html`.
- After merge: **34/216**, with **182 pending**. Original two English-only editorial articles remain separate.

## QA evidence before merge
- All 102 unique source text and image-alt segments mapped to English; source SHA-256 in batch05b.json locks the Vietnamese original.
- Article structural parity: 13 H2, 7 figures/captions, 8 images including cover, 15 list items, 1 blockquote, 5 details including four FAQ responses, and two additive English editorial paragraphs.
- English page has exactly one H1, self canonical, reciprocal VI/EN hreflang, verified visible FAQ answers matching FAQPage schema, BlogPosting and Breadcrumb schemas.
- The source VI file is byte-for-byte preserved outside marked EN hreflang and visible EN language switch. No changes to Vietnamese title, URL, canonical, meta, images, CTA or content.
- 216 VI blog entries retained in sitemap; 36 EN blog URLs after this release (34 translated + 2 pre-existing English originals). English Journal entry present; zero duplicate sitemap URLs.
- No missing linked HTML URLs from sitemap or local anchor fragments; original external references retained; all image alts present.
- Cloudflare Pages build completed successfully on head 27d11c8070b80a6f1027a47229dfedaf3915ed8a. Workers Builds failed on this branch and earlier baseline; no Worker/checkout/shop/router changes here.

## Limits and follow-up
The session verified source and structural SEO checks using GitHub connector, **not** the standalone Python QA scripts, browser mobile rendering, live deployment responses, image HTTP responses or GSC query-by-page overlap. Those remain external checks, not passed claims.

Maintain current 34 published translations and translate the remaining 182 in source-locked, intent-reviewed batches. Do not create empty EN stubs or modify existing VI SEO fields.
