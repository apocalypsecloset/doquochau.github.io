# English translation batch27 — 2026-11-03

Status: ten full English translations complete; local editorial, static, image and responsive QA passed. Awaiting PR preview and production verification. Baseline: 99/216 published; ten QA-passed; 107 further sources pending.

## Source and intent mapping

| Vietnamese source | English counterpart | Primary intent |
|---|---|---|
| `/blog/phoi-do-voi-quan-jean-ong-suong-nu.html` | `/en/blog/womens-straight-leg-jeans-outfits.html` | Straight-leg denim silhouette specialist; wide-leg trousers and baggy fit remain separate |
| `/blog/phoi-do-voi-chan-vay-dai.html` | `/en/blog/how-to-style-long-skirts.html` | General long-length skirt proportions; midi, pleated and denim-specific specialists separate |
| `/blog/phoi-do-voi-chan-vay-chu-a.html` | `/en/blog/how-to-style-a-line-skirts.html` | A-line silhouette specialist; pleat construction, tennis skirts and general mini styling separate |
| `/blog/quan-ong-rong-nu-phoi-voi-ao-gi.html` | `/en/blog/womens-wide-leg-trouser-outfits.html` | General wide-leg trouser volume styling; straight jeans, cargos and baggy construction separate |
| `/blog/bodycon-dress-la-gi-cach-phoi.html` | `/en/blog/how-to-style-bodycon-dresses.html` | Close-fitting dress construction and styling; slip drape and babydoll volume distinct |
| `/blog/babydoll-dress-la-gi-cach-phoi.html` | `/en/blog/how-to-style-babydoll-dresses.html` | Adult babydoll dress silhouette specialist; Coquette aesthetic and slip/bodycon construction separate |
| `/blog/giay-loafer-nu-la-gi-cach-phoi.html` | `/en/blog/womens-loafer-outfit-ideas.html` | Loafer construction and styling specialist; Mary Jane straps and ballet-flat openness distinct |
| `/blog/phoi-do-voi-ao-so-mi-nu.html` | `/en/blog/womens-shirt-outfit-ideas.html` | Button-front shirt shape and styling specialist; vests, blazers and aesthetic-level guides distinct |
| `/blog/chan-vay-tennis-phoi-voi-ao-gi.html` | `/en/blog/tennis-skirt-outfit-ideas.html` | Tennis-inspired skirt silhouette and sporty styling; general pleated and mini-length guides distinct |
| `/blog/chan-vay-bi-ngo-phoi-voi-ao-gi.html` | `/en/blog/bubble-skirt-outfit-ideas.html` | Gathered bubble-hem volume specialist; A-line and pleated construction distinct |

## Editorial review

- Full source-index translation retains all original paragraphs, list items, headings, tables, captions, FAQs, image placements and source references. Metadata and image alts are English. No placeholder pages or omitted source sections.
- Straight-leg denim is distinguished by the worn outline rather than a retailer label. Wide-leg trousers cover volume across materials; the existing wide-leg denim and baggy specialists retain narrower construction intents.
- Long skirts cover length across materials. A-line covers gradual silhouette opening; pleated guides cover fold construction; tennis-inspired skirts cover sporty short pleats; bubble skirts cover the inward gathered hem. Related forms can overlap, but each article has a distinct editorial target.
- Bodycon covers close fit, fabric and movement without body-type restrictions. Babydoll covers high-starting adult dress volume; slip dresses retain their separate drape/layering target.
- Loafers cover slip-on construction, upper coverage, socks and shoe weight. Mary Jane instep straps and ballet-flat openness remain separate specialist targets; hybrid footwear is acknowledged.
- Shirts cover fit, fastening, tuck and layered use. Broader Office Siren/Academia/Goth guides and the vest/blazer specialists keep separate intents.
- Closet comparison captions identify unverified construction honestly: straight-jean controls are not automatically labeled straight fit, long-skirt comparisons use shorter skirts, A-line examples are not all verified A-lines, and tennis/bubble related looks are general outfit comparisons.
- Fashion tennis-inspired appearance is not presented as evidence of sports-performance suitability. Fit, opacity, lining, actual shoe construction and movement tests qualify broad comfort or material claims.
- Translation memory supplies only exact unambiguous source matches; article-specific wording is reviewed in context (for example the long-skirt table uses Construction group).
- No GSC query × page access: editorial overlap screening only. No confirmed cannibalization, URL consolidation, deletion or canonical reassignment.

## QA

- {'en_words': 15165, 'headings': 266, 'images': 68, 'tables': 7, 'faqs': 39, 'source_text_segments': 1476}
 - All 26 manifest release gates pass. All ten VI files match baseline bytes outside marked English alternate and visible language-link additions.
- Canonical, reciprocal hreflang, translated title/meta, BlogPosting/FAQ parity, local hrefs/fragments, reference URLs, sitemap and Journal discovery pass. All 216 VI sitemap URLs retained.
- Journal has 111 unique sequential cards in its actual reading grid: 109 published or QA-passed translation pairs plus two EN-only originals.
- Twenty desktop/mobile browser views have no page overflow. Mobile tables scroll within wrappers, images stay within the article width, and the bodycon FAQ opens with a visible complete answer.
- Image endpoints: see `docs/qa/en-batch27-images.json`; all tested URLs return HTTP 200 with image MIME.
- Evidence: `docs/qa/en-batch27-static.json`, `en-batch27-regressions.json`, `en-batch27-images.json`, `en-batch27-responsive.json`.
- Homepage, POD, Fourthwall, shop, routing and PR #9 untouched.
