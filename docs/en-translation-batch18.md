# Translation release 18 — Sustainable Fashion (2026-11-03)

## Scope
- Source VI: `/blog/sustainable-fashion.html`
- English: `/en/blog/what-is-sustainable-fashion.html`
- After merge: **46/216** complete translations, **170 pending**, plus two pre-existing original English blog articles.
- Distinct search intent: clothing sustainability across its lifecycle and how to evaluate environmental/social claims, not capsule wardrobe selection or product shopping.

## Complete source QA
- Original VI source SHA-256: `7135485461c06d45027458d7ed8eaeb08c063bfec0ecaa852dacf46a6f0f58b3`. Original Vietnamese page unchanged byte-for-byte except the clearly marked English hreflang and language-switch UI.
- **166 source-locked text/image-alt units** translated, with 13 H2, 11 H3, 5 figures/captions, 6 original article images and translated alts, 20 list elements and 4 FAQ questions.
- Complete lifecycle stages and claims checklist, 5 misconceptions, certifications with scope limitations, practical purchasing hierarchy, Vietnam climate relevance and references to UNEP, EEA, EU Commission, GOTS and OEKO-TEX retained.
- Four visible FAQs match FAQPage JSON-LD exactly. Original external sources preserved and original article image src sequence untouched.

## Static bilingual SEO
- Exactly one English H1, EN self-canonical, reciprocal en/vi hreflang, BlogPosting/FAQPage/BreadcrumbList schema.
- English Journal includes the page. Sitemap retains 216 original VI blog URLs and 48 EN blog URLs (46 translated pairs and two original English articles), no duplicates or missing linked local HTML destinations.
- No broken in-page anchors. Crosslink to existing English Dark Aesthetic wardrobe guide.
- Cloudflare Pages successfully completed on branch commit 4bd23a5b289c9732afd9dda28cfc5ca41ee8dea2.

## Remaining QA limitations
- Standalone Python translation QA, live production HTTP/image availability, mobile/desktop browser render and GSC query×page overlap were not run independently here. Workers Builds feature preview failed; no Worker files were changed.
- No edits to original Vietnamese SEO title/meta/slug/canonical, shop/POD/checkout, homepage or Fourthwall.
