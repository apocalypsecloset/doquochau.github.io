# English translation batch26 — 2026-11-03

Status: published through PR #39, master `6a8c3288f7f76a0c83e094147d4786067a949b28`. Now 99/216 translation pairs production-verified, 117 pending. Two EN-only originals are additional (101 Journal cards).

## Source and intent mapping

| Vietnamese source | English counterpart | Primary intent |
|---|---|---|
| `/blog/phoi-do-voi-chan-vay-da.html` | `/en/blog/how-to-style-leather-skirts.html` | Leather-skirt material and shape styling; leather care and buying guides remain separate |
| `/blog/phoi-do-voi-ao-khoac-jean-nu.html` | `/en/blog/womens-denim-jacket-outfits.html` | Denim-jacket outerwear wash and layering; leather jackets and denim-bottom specialists remain separate |
| `/blog/phoi-do-voi-ao-gile-nu.html` | `/en/blog/womens-vest-layering-outfits.html` | Sleeveless knit and tailored vest layering; Dark Academia and Office Siren broader aesthetic guides separate |
| `/blog/phoi-do-voi-chan-vay-xep-ly.html` | `/en/blog/how-to-style-pleated-skirts.html` | Pleat construction, volume and hem specialist; tennis, A-line and general long-skirt articles separate |
| `/blog/phoi-do-voi-vay-ngan-nu.html` | `/en/blog/alternative-mini-skirt-outfits.html` | Mini-length alternative outfit styling; denim, leather and tennis skirt material-specific guides separate |
| `/blog/slip-dress-la-gi-cach-phoi.html` | `/en/blog/how-to-style-slip-dresses.html` | Slip-dress construction and layering; bodycon and babydoll silhouette specialists separate |
| `/blog/ballet-flats-la-gi-cach-phoi.html` | `/en/blog/how-to-style-ballet-flats.html` | Unstrapped ballet-flat construction and styling; Mary Jane instep straps and Balletcore aesthetic distinct |
| `/blog/outfit-nu-ca-tinh-di-concert.html` | `/en/blog/alternative-concert-outfits-for-women.html` | Concert occasion and movement requirements; gothic graphic tee product styling and general going-out guides separate |
| `/blog/phoi-do-voi-ao-blazer-den-nu.html` | `/en/blog/womens-black-blazer-outfits.html` | Black-blazer silhouette and layering specialist; Corporate Goth workwear and Office Siren aesthetic separate |
| `/blog/cach-chon-tui-cho-outfit-nu-ca-tinh.html` | `/en/blog/choosing-bags-for-alternative-outfits.html` | Bag selection and carrying-position specialist; general accessory directory and occasion styling separate |

## Editorial and completeness checks

- All source-index text segments, headings, lists, table cells, captions, image alts, FAQs, reference labels and relevant metadata translated. No stubs or partial pages. Images, reference URLs and source content-node counts retained.
- Leather-skirt and blazer Closet images are explicitly identified as texture/silhouette comparisons rather than exact garment examples. Denim-jacket examples distinguish denim bottoms from the biker-jacket outerwear comparison. Mini-skirt examples distinguish direct skirt looks from jeans-based upper-body references.
- Graphic tees in leather-skirt, denim, mini and concert formulas provide contextual garment/occasion examples. The existing gothic graphic tee specialist remains the primary EN target for that product-specific styling intent.
- Pleated skirts focus on fold construction across lengths; general mini styling focuses on hem length and outfit relationships. Slip dresses focus on drape and layering rather than bodycon or babydoll construction.
- Ballet flats remain separate from the Mary Jane instep-strap guide and Balletcore aesthetic. Hybrid shoes are acknowledged; toe shape alone does not guarantee fit.
- Bags focus on carrying position, capacity, shape and visual weight; shopping and general accessory-directory intents remain separate.
- Concert guidance is generic rather than an event-policy lookup. No specific bag dimensions, current venue rules or forecast are asserted; readers are directed to their event organizer's current official information. Tested shoes and actual movement take priority over category-wide comfort claims.
- Body size and height are not presented as bans on garment choices; proportions are optional visual goals. Unsupported universal styling claims and source SEO-planning language are edited into reader-facing clothing guidance.
- No GSC query × page access. Shared words are screening signals only; no confirmed cannibalization and no URL deletion, consolidation or canonical reassignment.

## EN-only source-order repair

The VI blazer source has reversed inserted recipe headings/paragraphs and misplaced colors, dress and climate headings. EN groups each recipe heading with its original paragraph and presents formulas 1–6 in reading order. Color, dress and climate headings precede their associated content. Every paragraph, heading, figure and original image order is retained; VI bytes remain unchanged outside marked bilingual additions.

## QA

- {'en_words': 18766, 'headings': 205, 'images': 68, 'tables': 15, 'faqs': 50, 'source_text_segments': 1766}
 - All 25 manifest release gates pass. All ten VI sources byte-match baseline after stripping only marked EN alternate/language links.
- Self-canonicals, reciprocal vi/en alternates, translated title/meta, BlogPosting and FAQ parity, local internal hrefs/fragments, external sources, sitemap discovery and Journal links pass. All 216 VI sitemap URLs retained.
- Journal has 101 unique sequential cards in its actual reading grid (99 translation drafts or published pairs plus two EN-only originals).
- Twenty desktop/mobile browser views have no page horizontal overflow. All mobile tables scroll in their wrappers; concert FAQ opens and shows its complete answer.
- Evidence: `docs/qa/en-batch26-static.json`, `en-batch26-regressions.json`, `en-batch26-responsive.json`, `en-batch26-blazer-order.json`, `en-batch26-images.json`.
- Homepage, POD, Fourthwall, shop, routing configuration and PR #9 untouched.

## Deployment verification

- Cloudflare Pages preview succeeds; all 22 release files match validated bytes. Normal expected-head squash merge completed.
- Initial production checks preceded deployment completion and found temporary 404/stale responses; after deployment all 22 files match byte for byte. Four exposed master checks (Cloudflare Pages, build, deploy, report-build-status) succeed. No Workers check appeared for this release.
- Evidence: `docs/qa/en-batch26-preview.json`, `docs/qa/en-batch26-production-verified.json`.
