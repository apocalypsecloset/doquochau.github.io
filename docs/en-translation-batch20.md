# English release 20 — Midi Dress / Skirt Length (2026-11-03)

## Scope and SEO intent
- VI: `/blog/vay-midi-la-gi.html`
- EN: `/en/blog/what-is-midi-length.html`
- After merge: **48/216** full VI→EN pairs, **168 pending**, plus two English-only originals.
- Unique intent: identifying the meaning, length and silhouette of midi skirts/dresses. Separate from the pending 'What to wear with a midi skirt?' styling article.

## Source lock and complete parity
- Original Vietnamese SHA-256: `93fbd91e152ff9fc02ac9f17a469caca6c655c9341b4d8ec7afb7283783c4446`.
- 118 source-locked translated text and image-alt segments. Exact parity: 13 H2, 2 H3, one three-column comparison table (four rows), 2 figures/captions, 5 original article images, 17 list items and five FAQs.
- Image src sequence unchanged. English image alts including the original short-skirt examples are translated.
- **Important image accuracy:** Looks #53 and #113 feature shorter skirts, NOT midi skirts. The original visual disclaimer and the English explanation explicitly retain that distinction; no misleading midi claim is added.
- VI article/source/SEO byte-identical outside marked reciprocal EN alternate hreflang and visible English version switch.
- Five visible English FAQ questions/answers exactly match FAQPage JSON-LD.

## Bilingual SEO and QA
- One English H1, EN self-canonical, reciprocal VI/EN hreflang, BlogPosting/FAQPage/Breadcrumb schema.
- English Journal links to real EN article; sitemap retains all 216 VI blog URLs, and has 50 EN blog URLs total (48 translated pairs and two original EN guides). No duplicate URLs or missing linked local HTML destinations.
- No broken in-page fragments. Cloudflare Pages passed on branch content commit 154da8ff13539e7d8756d5430e9180fec6e6ecb9.

## Not independently verified
- Python QA runner, production HTTP/images, real mobile/desktop rendering and GSC query×page overlap not tested. Workers Builds branch preview recurrent failure, no Worker changes.
- Original Vietnamese URL, slug, title/meta/canonical and site POD/checkout/homepage unchanged.
