# English translation release 19 — Minimalist Fashion (2026-11-03)

## Source and unique search intent
- VI `/blog/minimalist-style-la-gi.html` → EN `/en/blog/what-is-minimalist-fashion.html`
- After merge: **47/216 translated pairs**, **169 pending**, plus two English-only originals.
- Search intent: minimalist outfit styling and visual design principles, clearly different from the capsule wardrobe organization method, Sustainable Fashion lifecycle evaluation and Quiet Luxury fabric-quality emphasis.

## Source lock and parity
- Original VI SHA-256: `9bce53df317989da899d7b76b6e34605a25753d7beddcf7da5d958bff829743c`.
- 130 original text and image-alt units fully translated. 16 H2, 5 figures and captions, 6 original article images in source order with English alt, 26 list elements and five full FAQ answers retained.
- Original legacy `hero-img-wrap apcl-standard-cover` is preserved. Original FAQ `<details>` is normalized to `<details class="seo-faq-item">` only in the EN version for consistent styling and structured-data extraction.
- Vietnamese original remains byte-for-byte unchanged after removing only the marked alternate hreflang and visible English switch.
- Five visible FAQs exactly match FAQPage JSON-LD. Original Vogue and Merriam-Webster source links unchanged.

## Static SEO and deployment QA
- One EN H1, self canonical, reciprocal VI/EN alternate hreflang, BlogPosting/FAQPage/Breadcrumb JSON-LD.
- English Journal includes page and all 216 VI blog sitemap URLs remain. 49 EN blog URLs total (47 translations + two originals), with no duplicates, broken local anchors or HTML destinations missing from sitemap.
- Internal EN links to already published Capsule Wardrobe, Sustainable Fashion and Outfit definitions.
- Cloudflare Pages succeeded for branch content commit bd3a6f349b6588d14b67a95218966eec5b39339c.

## Not independently tested
- Standalone Python QA, actual 390px/1440px browser rendering, production image HTTP, GSC query×page overlap. Workers Builds branch preview failure is recurrent, no Worker/checkout files changed.
- No changes to POD, Fourthwall, shop, homepage, or original VI slug/title/meta/canonical.
