# English translation batch29 — 2026-11-04

Ten complete source-locked translations. Baseline: 119 published pairs (PR #44 production verified); this release will bring that to 129 only after deployment verification. Two EN-only originals remain additional.

| Vietnamese source | English counterpart | Primary intent |
| --- | --- | --- |
| `/blog/badgirl-outfit-di-cafe.html` | `/en/blog/alternative-cafe-outfits-women.html` | Café seating, lighting, venue design and seven formulas; narrower than general going-out or night-out guides |
| `/blog/outfit-di-dam-cuoi-nu-ca-tinh.html` | `/en/blog/alternative-wedding-guest-outfits-women.html` | Personal alternative styling within the actual wedding invitation and dress code; not generic night-out |
| `/blog/outfit-di-bien-cho-nu-ca-tinh.html` | `/en/blog/alternative-beach-outfits-women.html` | Beach activities, heat, wind, sand and packing; not general summer outfit overview |
| `/blog/outfit-san-bay-nu.html` | `/en/blog/airport-outfits-women.html` | Travel duration, seated movement, layers and baggage; distinguish everyday sporty styling |
| `/blog/femme-fatale-aesthetic-la-gi.html` | `/en/blog/femme-fatale-aesthetic-style-guide.html` | Character and visual-code aesthetic guide; distinguish broad dark feminine mood and practical dark feminine outfit specialist |
| `/blog/quan-cap-tre-la-gi.html` | `/en/blog/what-are-low-rise-pants.html` | Waist rise definition and fit; distinguish specific denim/cargo styles and styling formulas |
| `/blog/croptop-la-gi.html` | `/en/blog/what-is-a-crop-top.html` | Cropped-length definition and construction; existing crop-top outfit article remains styling target |
| `/blog/phoi-do-voi-quan-legging-nu.html` | `/en/blog/leggings-outfit-ideas-women.html` | Close-fitting stretch leggings and layering/coverage choices; not jogger/athleisure overview |
| `/blog/phoi-do-voi-quan-parachute-nu.html` | `/en/blog/parachute-pants-outfits-women.html` | Parachute fabric, adjustable volume and proportions; definition article remains separate |
| `/blog/quan-baggy-phoi-voi-ao-gi.html` | `/en/blog/baggy-pants-outfits-women.html` | Roomy trouser volume and top lengths; distinguish baggy definition, wide-leg and straight-leg specialists |

## Editorial and SEO review

- Full body, H1/H2/H3, tables, captions, alt text, FAQ, internal links and metadata are translated. 20,329 English article words, 237 headings, 64 original image placements, 19 tables and 36 FAQs. All 66 distinct HTTP image endpoints return 200/image MIME.
- Café is specific to seating/interiors/light/duration; wedding guest guidance follows actual host requirements; beach and airport focus on different activities. No invented current venue, airline or screening policies, prices or availability claims.
- Crop-top and low-rise definitions remain separate from crop-top and trouser outfit specialists. Baggy/parachute/legging specialists use actual construction and volume; broader wide-leg and straight-leg targets remain distinct. Femme Fatale is explicitly an editorial noir-inspired interpretation within a broader Dark Feminine vocabulary.
- GSC query × page data is unavailable. These are editorial intent distinctions; no confirmed cannibalization diagnosis or URL consolidation.
- Original images and references are retained. Café and leggings examples are honestly labelled as proportion studies where they do not show the exact formula or leggings. Low-rise photo examples cannot establish measured rise. Wedding Closet examples are not presented as complete wedding outfits; baggy examples do not imply identical physical jeans or measured A/B results.
- No body-shape exclusions or universal fabric/footwear comfort guarantees. Coverage is a choice. Actual construction, lining, weave, recovery, conditions and movement matter.
- Historical checks: ASU FIDM Museum's [Louella Ballerino crop top, 1946](https://fidmmuseum.org/learn/articles/louella-ballerino-crop-top-1946), source reference preserved; FIT [2000–2009 timeline](https://fashionhistory.fitnyc.edu/2000-2009/) for early-2000s low-rise context; Christa van Raalte's *The Femme Fatale on Screen* at [Bournemouth University](https://eprints.bournemouth.ac.uk/34724/3/IEGMC301_Raalte_EDITED%20(Oct%2027).pdf) for the limited historical introduction. Fashion formulas are editorial suggestions, not claims derived from those historical sources.

## QA

- All ten VI documents match baseline bytes outside marked reciprocal hreflang/EN-link additions. All 216 original VI sitemap URLs, source canonical/title/meta/body remain.
- All 28 manifest gates pass, including full source/tag/reference/image parity, FAQ/schema, internal targets/fragments, self-canonical, reciprocal vi/en alternates, sitemap and Journal sequence/grid.
- All 131 EN pages have one H1 and self-canonical, with no duplicate title, description or canonical values. This metadata check does not determine query-level cannibalization.
- Twenty desktop/mobile browser views (1440px/390px frames) have no body overflow. Tables remain inside horizontal scrolling wrappers. Baggy mobile FAQ opens to a complete visible answer.
- 32 links in 18 older EN pages now point to completed counterparts; every link to each page's own Vietnamese original remains. Refresh guards preserve other content, metadata and images and keep schema references consistent.
- Sitemap synchronization now uses each new translation's declared publication date; the ten batch28 EN lastmod entries are corrected to November 4. VI lastmod values remain unchanged.
- Homepage/POD/Fourthwall/shop/routing/PR #9 untouched. Preview and production verification are required before recording the ten as published.

Evidence: `docs/qa/en-batch29-*.json`; complete translations: `data/en-translations/batch29.json` and ten TSV files.
