# English translation batch 04 — 2026-11-03

Baseline master: `6d4c082a2c0e7aa623b8b39c4f5f3febbf9e2be4` (PR #12 merged).

## Progress
Before this batch: 22/216 translations published. This batch adds ten complete English counterparts. After merge: **32/216 complete, 184 pending**, plus two original English articles (34 English articles total). Publication does not establish Google indexing or search performance.

## Source-to-English mapping and primary intent
| Vietnamese source | English counterpart | Primary intent |
|---|---|---|
| `/blog/cybergoth.html` | `/en/blog/cybergoth-style-outfits.html` | Cybergoth specialist history and six outfits; three-way comparison retains comparison intent |
| `/blog/scene-style-la-gi.html` | `/en/blog/scene-style-fashion.html` | Scene historical definition and modern Scene outfits, distinct from Emo and later E-Girl pillar |
| `/blog/phong-cach-egirl-la-gi.html` | `/en/blog/what-is-egirl-style.html` | E-Girl definition and comprehensive wardrobe pillar; hub navigation and budget/accessory shopping specialists remain distinct |
| `/blog/phoi-do-layering-nu.html` | `/en/blog/alternative-layering-outfits-women.html` | General alternative layering geometry and removable layer system; mesh and hoodie specialists remain item-specific |
| `/blog/cach-giat-do-den-khong-phai-mau.html` | `/en/blog/how-to-wash-black-clothes.html` | Black textile laundering and fading diagnosis, separate from black outfit styling and summer thermal comfort |
| `/blog/goth-nails-mau-nail-phong-cach-goth.html` | `/en/blog/goth-nail-designs.html` | Goth manicure designs, shape and outfit coordination, distinct from general Goth definition |
| `/blog/kieu-toc-goth-goth-hairstyle-nu.html` | `/en/blog/goth-hairstyles-women.html` | Goth haircut and styling silhouette specialist, separate from hair-dye technique and Punk hair |
| `/blog/xay-tu-do-dark-aesthetic.html` | `/en/blog/build-a-dark-aesthetic-wardrobe.html` | Long-term dark wardrobe foundation and purchase order; fixed-budget capsule and beginner style discovery remain separate |
| `/blog/phoi-do-alt-fashion-cho-nguoi-moi.html` | `/en/blog/alternative-fashion-for-beginners.html` | Five-step beginner action workflow and silhouette discovery; not broad alt definition or long-term capsule planning |
| `/blog/phu-kien-alt-fashion-thiet-yeu.html` | `/en/blog/alternative-fashion-accessories.html` | Eight-category alternative accessory selection; E-Girl accessory seller and shopping guide remains narrower |

## QA
- 20,290 English words; 65 original editorial images; 13 tables; 45 FAQ answers.
- Source hashes and paragraph/list/heading/table/caption/image parity pass. No Vietnamese body or alt text remains. Canonical, metadata, one H1, valid JSON-LD, reciprocal hreflang, unique IDs, internal paths and fragments, sitemap and Journal discovery pass.
- All ten Vietnamese originals match baseline byte-for-byte after stripping only the marked English alternate and language-switch additions. All 216 Vietnamese sitemap blog URLs remain; no duplicate sitemap entries.
- All ten pages rendered in the browser at desktop 1440px and mobile 390px. Document scroll width matches client width in all twenty checks. Scene tables retain 650px content within a 341px horizontally scrollable container; FAQ expansion works.
- Goth nails uses heading-and-paragraph FAQs in the original. The generator now recognizes this format without changing its source structure and emits all four English questions and answers in FAQPage schema. QA compares actual visible questions and answers with schema, including existing disclosure FAQs.
- Earlier batch02 and batch03 regressions pass. Fourteen earlier English pages receive counterpart links where complete EN targets now exist.
- All 77 original and responsive image endpoints return HTTP 200 and image MIME types.
- Original images, responsive image URLs and external reference links remain unchanged. Individual label instructions take precedence in the laundry guide; no universal no-fading guarantee or household dye-lock claim is introduced.
- No homepage, shop UI, Fourthwall, Worker, routing or PR #9 changes.

## SEO screening
No GSC query × page dataset is available. Intent distinctions are editorial screening, not confirmed cannibalization. Cybergoth's detailed history and outfits remain separate from the existing three-way subtype comparison. E-Girl's definition pillar remains separate from its navigation hub and pending budget/accessory shopping guides. General layering differs from mesh coverage and hoodie styling. The beginner workflow differs from long-term wardrobe planning and a fixed-budget capsule. Goth hair styling differs from hair-dye techniques. No VI URL was deleted, merged, redirected or noindexed.

## Reference cross-check
The laundry guide's existing Whirlpool reference was checked against the manufacturer's published recommendations on inside-out washing, cool water, appropriate gentle cycles and low-heat or air drying:
https://www.whirlpool.com/blog/washers-and-dryers/how-to-keep-clothes-from-fading.html
Original reference URLs remain unchanged. Temperature terminology is not treated as a universal 30°C definition.

## Evidence and reproduction
Evidence lives in `docs/qa/en-batch04-*.json`.
```sh
python scripts/en_translate.py generate batch04
python scripts/qa_en_translations.py batch04
python scripts/qa_en_translations.py batch02
python scripts/qa_en_translations.py batch03
python scripts/qa_en_images.py batch04 /tmp/en04-images.json
```

## Remaining queue
184 articles remain after this batch is merged. Continue complete translations in batches of 10–20, prioritizing alternative garments, graphic tees, Punk, Grunge and dark wardrobes. Topic hubs require navigation-specific treatment rather than another definition pillar.
