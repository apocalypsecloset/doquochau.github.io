# English translation batch25 — 2026-11-03

Status: published through PR #37, master `e4dd2bf4b44ed01ae7cc1efe75f84c71dcf49f3c`. Now 89/216 translation pairs merged and production-verified; 127 pending. Two EN-only originals are additional (91 Journal cards).

## Source and intent mapping

| Vietnamese source | English counterpart | Primary intent |
|---|---|---|
| `/blog/giay-mary-jane-la-gi.html` | `/en/blog/what-are-mary-jane-shoes.html` | Footwear construction and styling specialist; broader footwear directory and boot comparison separate |
| `/blog/leg-warmers-la-gi-cach-phoi.html` | `/en/blog/how-to-style-leg-warmers.html` | Lower-leg volume and footwear accessory specialist; arm warmers and Balletcore definition distinct |
| `/blog/coquette-la-gi-dark-coquette.html` | `/en/blog/coquette-vs-dark-coquette.html` | Coquette definition plus pastel/dark comparison; Dark Feminine hub and outfit specialist separate |
| `/blog/indie-sleaze-la-gi.html` | `/en/blog/what-is-indie-sleaze.html` | Retrospective indie nightlife styling and photography; Grunge-Punk and Y2K definitions distinct |
| `/blog/techwear-la-gi.html` | `/en/blog/what-is-techwear.html` | Function-first technical clothing evaluation; Cyber Y2K visual styling and Gorpcore outdoor context separate |
| `/blog/cyber-y2k-la-gi.html` | `/en/blog/cyber-y2k-style-outfits.html` | Futuristic millennium visual styling; general Y2K, Dark Y2K comparison and functional techwear separate |
| `/blog/visual-kei-la-gi.html` | `/en/blog/what-is-visual-kei.html` | Japanese music-scene visual presentation specialist; Goth and Scene retain their own cultural targets |
| `/blog/devil-core.html` | `/en/blog/devilcore-aesthetic-outfits.html` | Infernal motif-led micro-aesthetic; general Goth, Emo and mystical Whimsigoth separate |
| `/blog/morute.html` | `/en/blog/morute-aesthetic-outfits.html` | Morbid-cute aged texture and community usage; Coquette, Soft Goth and Gurokawa motif system distinct |
| `/blog/gurokawa.html` | `/en/blog/gurokawa-creepy-cute-outfits.html` | Kawaii-grotesque graphics and DIY styling; Morute aged texture and Pastel Goth specialist separate |

## Editorial checks

- All body segments, H1/H2/H3, tables, lists, captions, image alts, FAQs and references translated; no English placeholders. Original image order, external source URLs and source node counts retained.
- Mary Jane examples distinguish the actual strapped shoe in Look #22 from the two boot comparisons; toe shape and platform height do not guarantee fit or comfort.
- Coquette/Dark Coquette ornamental styling remains separate from the Dark Feminine hub and practical outfit specialist. Corsets are optional, and palette does not imply age or autonomy.
- Indie Sleaze covers retrospective music/nightlife/photography references. Revival claims are qualified rather than presented as universal current adoption.
- Techwear evaluates function and product specifications; Cyber Y2K evaluates futuristic visual references. Water beading alone is not proof of waterproof construction.
- Visual Kei retains Japanese music-scene context and variable visual personas rather than being equated with Japanese Goth.
- Devilcore is treated as informal motif-led community usage. Morute emphasizes aged/delicate contrast; Gurokawa emphasizes cute/grotesque graphics and DIY. Origins and community boundaries are qualified, without health or body-type requirements.
- No GSC query × page access. These are editorial intent distinctions and overlap candidates only; no confirmed cannibalization and no merged/deleted URLs.

## Source verification

Primary/first-party resources cross-checked during editorial work (original article references remain unchanged):

- [American Duchess footwear history](https://blog.americanduchess.com/2022/08/the-history-of-mary-jane-shoes.html) and [CHARLES & KEITH Mary Jane guide](https://www.charleskeith.com/sg/guides/mary-janes.html).
- Vogue first-party reporting: [Coquette](https://www.vogue.com/article/coquette-aesthetic-explainer), [post-Y2K references](https://www.vogue.com/article/what-comes-after-y2k), [Indie Sleaze debate](https://www.vogue.com/article/indie-sleaze-revival-vogue-fashion-writers-debate).
- [GORE-TEX FAQ](https://www.gore-tex.com/support/frequently-asked-questions), [DWR explanation](https://www.goretexprofessional.com/uk/support/dwr), [ACRONYM product construction example](https://acrnm.com/P24TS-DC_SS25).
- [Ken McLeod Visual Kei research](https://journals.sagepub.com/doi/10.1177/1103308813506145) and [IDEA 361 creator feature](https://www.idea-mag.com/en/idea_magazine/361/).
- Aesthetics Wiki is identified as community documentation rather than a formal taxonomy. A current Devilcore warning banner was not independently verified and is not asserted in the translation.

## Implementation and QA

- EN-only repair moves two Techwear headings ahead of their associated introductory paragraphs; no paragraphs or images removed.
- Translator preserves word boundaries across inline tags where punctuation-led VI fragments become word-led English. Existing published English pages are not regenerated.
- Ten VI pages match baseline byte for byte after removing only marked English alternate/language-switch additions. All 216 VI sitemap URLs retained.
- All 24 manifest release gates pass. {'en_words': 18395, 'headings': 247, 'images': 61, 'tables': 10, 'faqs': 39, 'source_text_segments': 1664}
 - Journal has 91 unique numbered cards in its reading grid, including two EN-only originals.
- Twenty browser views at 1440px/390px show no page horizontal overflow. Mobile tables scroll inside their wrappers; one mobile FAQ expanded and visually inspected.
- Evidence: `docs/qa/en-batch25-static.json`, `en-batch25-regressions.json`, `en-batch25-responsive.json`; `en-batch25-images.json`: all 66 distinct original, responsive and shell image endpoints return HTTP 200 with image MIME.
- Homepage, POD, Fourthwall, shop layout, routing configuration and PR #9 untouched.

## Deployment verification

- Cloudflare Pages PR preview succeeded. All 22 files (ten EN, ten VI, Journal and sitemap) match validated bytes.
- Normal squash merge used the expected PR head and unchanged master base.
- The first production check ran before deployment completed and saw temporary 404/stale responses. After deployment, all 22 files match byte for byte. Four exposed master checks (Cloudflare Pages, build, deploy, report-build-status) succeeded. No Workers check appeared in the exposed results for this release; no all-five-check claim is made.
- Evidence: `docs/qa/en-batch25-preview.json`, `docs/qa/en-batch25-production-verified.json`.
