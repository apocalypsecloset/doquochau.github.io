# Full English translation batch 22 — 2026-11-03

Baseline: `ad33fd74b5acf6b0f225ea889e7634d12dd11e53`, with 49 published translation pairs and 167 pending. This batch adds ten complete counterparts: **59/216 after merge, 157 pending**, plus two existing EN originals.

The earlier local batch05 draft was superseded by intervening master publications. Five overlapping drafts were excluded. Published English slugs remain unchanged; no duplicate counterparts were created.

## Mapping and primary intent
| Vietnamese source | English counterpart | Primary intent |
|---|---|---|
| `/blog/alt-fashion-la-gi-va-tai-sao-no-quan-trong.html` | `/en/blog/what-is-alt-style.html` | Broad alternative-style definition and cultural umbrella; beginner action workflow and navigation dictionary remain distinct |
| `/blog/cach-phoi-do-den-khong-nham-chan.html` | `/en/blog/black-outfits-women-texture-proportions.html` | All-black outfit technique and seven approaches; laundry, thermal comfort and general multilayer geometry remain separate |
| `/blog/y2k-dark-aesthetic-khac-gi-y2k-thuong.html` | `/en/blog/dark-y2k-vs-y2k.html` | Dark Y2K versus broader Y2K styling comparison; Cyber Y2K specialist retains futuristic definition intent |
| `/blog/tu-do-alt-fashion-1-trieu.html` | `/en/blog/alternative-wardrobe-vnd-one-million.html` | Fixed VND budget allocation model with reuse, not current price listings or broad long-term wardrobe foundations |
| `/blog/kieu-toc-punk-nu.html` | `/en/blog/punk-hairstyles-women.html` | Punk cut and styling silhouette specialist; Goth hair and general dye technique retain separate targets |
| `/blog/that-lung-dinh-tan-phoi-do.html` | `/en/blog/how-to-style-studded-belts.html` | Studded belt waist hardware specialist; general accessories and choker guide remain separate |
| `/blog/phoi-do-voi-quan-short-nu.html` | `/en/blog/shorts-outfits-women.html` | Shorts-specific outfit proportions; trousers and mini skirt guides remain distinct |
| `/blog/y2k-la-gi-phong-cach-y2k-nu.html` | `/en/blog/what-is-y2k-fashion.html` | Mainstream Y2K definition and wardrobe; Dark Y2K comparison and Cyber Y2K specialist separate |
| `/blog/cach-bao-quan-do-da-nu.html` | `/en/blog/leather-jacket-clothing-care.html` | Leather and coated-clothing care; leather styling, boot odor and shopping remain separate |
| `/blog/nhuom-toc-dark-aesthetic.html` | `/en/blog/dark-aesthetic-hair-color.html` | Hair coloring and maintenance; Goth and Punk haircut specialists separate |

## QA and repairs
- 16,732 English words; 60 original editorial images; 8 tables; 39 FAQ answers. All 71 original/responsive image endpoints passed HTTP 200 and image MIME checks.
- Full source-hash and paragraph, list, heading, table, caption, image and visible FAQ/schema parity pass. One H1, metadata, self canonical, reciprocal hreflang, local paths/fragments, unique IDs, Journal and sitemap discovery pass. All 216 VI sitemap URLs remain, without duplicate sitemap entries.
- Ten VI originals are byte-identical to baseline after removing only the marked EN alternate and language-link additions. VI URLs, titles, meta, canonical, article content and images remain unchanged.
- All existing manifest regressions pass after targeted EN fixes: six older pages had a Vietnamese information-table aria-label; four had invalid relative blog links. These are corrected in EN only, using existing counterparts where available. No published slug changes.
- The 17 intervening master articles also pass all 107 original/responsive image endpoint checks (HTTP 200 and image MIME).
- Browser checks cover the 17 intervening master articles and ten new articles at 1440px and 390px: 54 views, one H1 each, no horizontal document overflow. Budget tables scroll within mobile containers; hair-color FAQ expands correctly.
- Existing VI Y2K source insertions place five outfit paragraphs before headings in reverse order, and leave the pastel section empty. EN-only ordering repairs place each formula under its heading in ascending order and move the relevant paragraph beneath the pastel heading, retaining all content and images.
- No homepage, POD, Fourthwall, checkout, shop UI, Worker, routing or PR #9 changes.

## Editorial and source review
- GSC query × page access is unavailable. Intent distinctions are editorial screening, not confirmed cannibalization. Definition pillars, comparison, item guides and fixed-budget planning remain separate. No URL consolidation, redirects, deletion or noindex.
- Hair color: distinguish strand testing from skin allergy testing; do not assume a 15-minute universal test, no fading, bleaching for every dark tint, a skin-tone prohibition, or purple shampoo correcting every unwanted cast. FDA/AAD primary guidance checked. Full original color, maintenance, home/salon and hairstyle topics retained.
- Leather: material-specific instructions override universal oil, vinegar, powder, dwell-time and conditioning schedules. Genuine leather, PU, suede and nubuck remain separate; conditioner does not repair all cracks. Existing care topics retained with conditional advice based on manufacturer guidance.
- Budget percentages are illustrative allocations, not current product prices. Body types are not treated as styling prohibitions.

Primary cross-checks:
- https://www.fda.gov/cosmetics/resources-consumers-cosmetics/cosmetics-safety-qa-hair-dyes
- https://www.aad.org/public/everyday-care/hair-scalp-care/hair/coloring-perming-tips
- https://www.schottnyc.com/pages/repairs
- https://www.drmartens.com/us/en/dms-world/care/leather-and-suede-care
Original image and external reference URLs preserved. No long quotations added.

## Evidence
`docs/qa/en-batch22-*.json` records static/source checks, all manifest regressions, images and responsive checks. The 216-row CSV records each source URL, EN counterpart and editorial intent status.

## Reproduction
```sh
python scripts/en_translate.py generate batch22
python scripts/qa_en_translations.py batch22
python scripts/qa_en_images.py batch22 /tmp/en22-images.json
```

Continue the remaining 157 articles in complete audited batches of 10–20. Keep the pending navigation hubs distinct from definition articles. Publication is not a claim of Google indexing or ranking.
