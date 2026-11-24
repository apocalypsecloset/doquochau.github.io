# Approved bilingual blog CTA layout - 23 November 2026

The three positions now serve different reading stages:

- Top: the first child of main, below the menu and before the H1. A compact banner with the topic-selected tee, localized USD starting price and purchase invitation. Desktop width is capped at 540px; the self-hosted Be Vietnam Pro ExtraBold face keeps English and Vietnamese glyphs consistent. The owner confirmed there is no promotion, so no discount or urgency claim is displayed.
- Middle: one relevant design, a styling suggestion and localized USD starting price. The description and fit note remain visible on mobile. Its red brand strip, wine background and cream button match the approved first CTA.
- End: two compact product cards with artwork descriptions and explicit size/price links, using the same red/wine/cream palette. The Vietnamese copy is written naturally rather than translated from a slogan. Shipping/tax and made-to-order notes avoid delivery or return promises.

Product imagery, product names and price amounts are unchanged. Product choice prioritizes specific style topics, and keyword matching respects word boundaries and Vietnamese accents. Broad informational articles use a general invitation rather than a claim that a particular tee is necessary for the article's subject.

Top and middle CTA images/buttons open the topic-selected product page on apocalypsecloset.com. Grunge topics select Silent Chaos and romantic gothic topics select Thorn Heart. Each end product card links to its own product page; only the compare-both button uses /#shop. Internal UTM parameters are not added. Only checkout opens Fourthwall. Desktop H1 width is capped at 640px. This change does not introduce analytics or claim measured conversion lift.

## Regenerate

From the site repository root:

```powershell
python -X utf8 tools/blog-cta/test_cta.py
python -X utf8 tools/blog-cta/inject_cta.py --lang all --write --keep-app-box
```

848 articles are eligible: 423 VI and 425 EN. Six short articles keep top/end CTAs without forcing a middle interruption. The 71 hub, archive and nonstandard pages are left unchanged. The generator emits one font preload and loads its component stylesheet after the article styles. Preview exports include the font and license.

Edit assets/css/blog-shop-cta.css as the single stylesheet source. The generator hashes its normalized content and embeds the component rules once in each article head as style#ac-blog-cta-style, after article styles. The hash is recorded in data-css-version. Comments/newlines are compacted while spaces inside font-family names are preserved.

This critical CSS is delivered with the HTML because the production edge repeatedly retained stale CSS/404 asset responses, including versioned requests. Articles no longer request an external CTA stylesheet. The self-hosted font still uses one preload. Standalone CSS exports remain available with --out for compatibility; --write does not create unused fingerprinted CSS files in the published site. The source stays editable in one place.

Existing middle-CTA positions are preserved when regenerating after content cleanup. Standalone Look recommendation modules and their TOC entries have been removed from 64 VI and 66 EN articles; other article examples and guide links are retained.

Font source: https://github.com/google/fonts/tree/main/ofl/bevietnampro . The complete ExtraBold font is converted to WOFF2 without subsetting. Copyright and SIL OFL 1.1 text are included in assets/fonts/BeVietnamPro-OFL.txt.

The review is a focused CTA/reading-experience use of seo-sxo and seo-content, not a new site-wide SEO ranking audit. Search spot-checks show styling/how-to content around graphic-tee and romantic-goth queries; no controlled Google top-10, PAA or conversion dataset was available. The audience assumptions come from the brand brief and page content, not invented user research.

Validation covers all article URLs, CTA order and destinations, repeat generation, unchanged article content/schema and representative mobile/desktop renders. Font glyph coverage is verified in the browser. Cookies are dismissed with necessary-only in ephemeral preview contexts; the production cookie UI is unchanged. The owner approved the sample and authorized the full rollout.
