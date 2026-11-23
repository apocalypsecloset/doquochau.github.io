# Bilingual blog CTA update - 23 November 2026

The three positions now serve different reading stages:

- Top: a compact text invitation to explore the two original designs. No product-photo banner or repeated pricing before the article delivers its advice.
- Middle: one relevant design, a styling suggestion, an explicit USD starting price and a size/details link to that exact Fourthwall product. The description and fit note remain visible on mobile.
- End: two compact product cards with artwork descriptions and explicit size/price links. The Vietnamese copy is written naturally rather than translated from a slogan. Shipping/tax and made-to-order notes avoid delivery or return promises.

Product imagery, product names and price amounts are unchanged. Product choice prioritizes specific style topics, and keyword matching respects word boundaries and Vietnamese accents. Broad informational articles use a general invitation rather than a claim that a particular tee is necessary for the article's subject.

Same-site catalog links use /#shop, preserving the original acquisition source. Direct Fourthwall product links retain the existing placement/campaign parameters. This change does not introduce a new analytics integration or claim a measured conversion lift.

## Regenerate

From the site repository root:

```powershell
python -X utf8 tools/blog-cta/test_cta.py
python -X utf8 tools/blog-cta/inject_cta.py --lang all --write --keep-app-box
```

848 articles are eligible: 423 VI and 425 EN. Six short articles keep top/end CTAs without forcing a middle interruption. The 71 hub, archive and nonstandard pages are left unchanged. CSS version: 20261123cta2.

The review is a focused CTA/reading-experience use of seo-sxo and seo-content, not a new site-wide SEO ranking audit. Search spot-checks show styling/how-to content around graphic-tee and romantic-goth queries; no controlled Google top-10, PAA or conversion dataset was available. The audience assumptions come from the brand brief and page content, not invented user research.

Preview checks cover Vietnamese/English at 390px and 1280px, all three placements. Cookies are dismissed with necessary-only in ephemeral preview contexts. The production cookie UI is unchanged. Article body, metadata, language links and JSON-LD are compared against HEAD outside the CTA blocks and stylesheet cache token.
