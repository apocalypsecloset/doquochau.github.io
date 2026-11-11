# Full English translation batch 23 — 2026-11-03

Baseline master: `c11d2f9eaf67395f5b3b7a8883b8314044becec1`. Published: **59/216**, 157 pending. This PR adds ten complete counterparts; after publication: **69/216**, 147 pending, plus two EN-only originals.

## Mapping and intent

| VI source | EN counterpart | Primary intent |
|---|---|---|
| `/blog/arm-warmers-la-gi-cach-phoi.html` | `/en/blog/how-to-style-arm-warmers.html` | Detachable arm sleeve styling and fit, not knitting patterns or general alternative accessories |
| `/blog/choker-nu-la-gi-cach-phoi.html` | `/en/blog/how-to-style-chokers.html` | Neckline-specific choker styling, separate from general accessories and waist belts |
| `/blog/fishnet-tights-la-gi-cach-phoi.html` | `/en/blog/how-to-style-fishnet-tights.html` | Fishnet leg pattern and coverage specialist, separate from mesh tops and general Goth definition |
| `/blog/combat-boots-hay-platform-boots.html` | `/en/blog/combat-boots-vs-platform-boots.html` | Combat upper versus platform sole comparison and buying decision; boot outfit specialist remains separate |
| `/blog/quan-cargo-vai-du-hay-kaki.html` | `/en/blog/nylon-vs-twill-cargo-pants.html` | Cargo fabric selection comparison; cargo definition, outfits and seller-shopping guide separate |
| `/blog/phoi-do-voi-quan-jeans-ong-rong-nu.html` | `/en/blog/wide-leg-jeans-outfits-dark-y2k.html` | Denim-specific wide-leg wash/rise/hem styling; general non-denim wide trousers and flares remain distinct |
| `/blog/phoi-do-voi-quan-ong-loe-nu.html` | `/en/blog/flared-pants-outfits-women.html` | Fitted upper leg widening near knee: flare-specific outfit geometry, not general wide legs |
| `/blog/phoi-do-voi-quan-jogger-nu.html` | `/en/blog/jogger-outfits-women.html` | Jogger outfit construction around cuff taper and layers; jogger definition and airport outfits separate |
| `/blog/phoi-do-voi-ao-bomber-nu.html` | `/en/blog/bomber-jacket-outfits-women.html` | Bomber outfit volume and layer geometry; bomber seller/fit buying guide separate |
| `/blog/phoi-do-voi-chan-vay-dai-den.html` | `/en/blog/long-black-skirt-outfits.html` | Long black skirt color-specific outfit capsule; general long skirt form and midi definition separate |

## QA

- 16,056 English words, 64 original editorial images, 10 tables, 30 FAQ answers. All 70 original/responsive image endpoints return HTTP 200 and image MIME.
- Full source hashes, paragraphs, list items, headings, tables/cells, captions, image order/alt, and visible FAQ/schema parity pass. Metadata, one H1, unique IDs, local links/fragments, self canonical, reciprocal hreflang, Journal and sitemap pass. All 216 VI sitemap URLs retained without duplicates.
- All 22 existing manifest checks pass. Ten VI originals match baseline byte for byte after stripping only marked EN additions. No VI title, meta, canonical, slug, body or image changes.
- Twenty browser views at 1440px and 390px: no horizontal document overflow. Mobile images fit; tables scroll within containers. Arm warmer FAQ opens and answer renders correctly.
- Corrected EN choker heading to nine outfit directions to match the nine retained formulas. Reviewed internal-link sentences and clarified cargo fabric terminology without dropping original content.
- Combat uppers and platform soles can coexist. Footwear comfort depends on construction and fit. Cargo fabric behavior depends on weave, finish and lining; synthetic sheen does not establish waterproofing. Body proportions are styling choices rather than bans.
- GSC query × page unavailable: intent review is editorial screening only, with no confirmed cannibalization, redirects, deletion or consolidation. Definition hubs, item guides, comparisons and shopping guides remain separate.
- Homepage, POD, Fourthwall, shop UI, checkout, Worker and PR #9 untouched.

## Evidence

`docs/qa/en-batch23-{static,images,regressions,responsive}.json`; full translations in `data/en-translations/*.tsv`, mapping in `batch23.json`, 216-row inventory updated. Release/deployment checks will be recorded in the PR before merge; publication must be verified afterward.

## Publication result

Merged PR #33 as `3a8ccd5db87ee9e80311a74a17efef2d0c65fe5a`. All five master checks succeeded afterward, including Workers Builds. Production initially returned pre-deploy responses; the final 22-file check passes byte for byte for all ten EN/VI pairs, Journal and sitemap. Tracker now records **69 MERGED, 147 PENDING**. Final evidence: `docs/qa/en-batch23-production-verified.json`.
