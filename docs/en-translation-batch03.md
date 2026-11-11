# English translation batch 03 — 2026-11-03

Baseline master: `adad4ef303104ab07aa5a92090e5a43e85ce00ae` (PR #11 merged).

## Progress
- Before this PR: 12/216 translations published.
- This batch: 10 complete English translations, fully QA-passed.
- After merge: **22/216 complete, 194 pending**, plus two existing English originals (24 English articles total).
- Completion does not imply Google indexing or verified search performance.

## Source-to-English mapping and primary intent
| Vietnamese source | English counterpart | Primary intent |
|---|---|---|
| `/blog/nu-goth-la-gi-phong-cach-nu-goth.html` | `/en/blog/nu-goth-style-outfits.html` | Internet-era modern nu goth, fitted/oversized contrasts and selected hardware; distinct from trad, soft and corporate goth |
| `/blog/vampire-goth-la-gi-vampire-goth-aesthetic.html` | `/en/blog/vampire-goth-style-outfits.html` | Vampire cinema/mythology and controlled dark opulence; romantic goth remains broader historical romance |
| `/blog/pastel-goth-cyber-goth-mall-goth-la-gi.html` | `/en/blog/pastel-goth-vs-cybergoth-vs-mall-goth.html` | Three-way subtype comparison; future cybergoth specialist owns detailed cybergoth history and outfits |
| `/blog/phong-cach-emo-la-gi.html` | `/en/blog/what-is-emo-style.html` | Emo definition and musical-era distinctions; not general alt or e-girl pillar |
| `/blog/dark-academia-la-gi-phoi-do-badgirl.html` | `/en/blog/dark-academia-outfits-alternative-style.html` | Academic tailoring and muted textured wardrobe with alternative edge, unlike dark feminine general outfit formulas |
| `/blog/phoi-do-voi-ao-luoi-nu.html` | `/en/blog/what-to-wear-with-mesh-tops.html` | Mesh item-specific layering and coverage; not generic graphic-tee specialist or general layering guide |
| `/blog/form-oversize-la-gi.html` | `/en/blog/what-is-oversized-fit.html` | Oversized fit definition and shopping measurements; hoodie page owns hoodie outfit construction |
| `/blog/ao-hoodie-oversize-nu-phoi-voi-gi.html` | `/en/blog/oversized-hoodie-outfits-women.html` | Hoodie-specific outfit formulas, hood/hem and outer-layer geometry; not oversized definition |
| `/blog/dark-feminine-outfit-phoi-do.html` | `/en/blog/dark-feminine-outfit-ideas.html` | Practical seven-formula outfit construction; future dark feminine definition and navigation hub retain distinct roles |
| `/blog/mac-do-den-mua-he-co-nong-khong.html` | `/en/blog/is-black-clothing-hotter-in-summer.html` | Color and thermal comfort/fabric fit, not summer outfit recipes or black-clothing laundry |

## QA
- 19,151 English words; 71 original editorial images; 15 tables; 44 FAQ answers.
- Source hash and full paragraph/list/heading/table/caption/FAQ/image parity; English title/meta, one H1, valid JSON-LD, local link/anchor targets, unique IDs, canonical, reciprocal vi/en alternates, sitemap and Journal discovery all pass.
- All 79 original/responsive image endpoints return HTTP 200 and image MIME types.
- All 10 articles rendered in the cloud browser at desktop 1440px and mobile 390px; no horizontal overflow. Mobile mesh comparison tables keep 650px content inside 341px scrollable containers; FAQ expansion verified.
- All ten Vietnamese source files remain byte-for-byte identical to baseline after stripping only the marked EN alternate and language-switch additions. No VI title, meta, canonical, content, image or URL changed.
- All 216 Vietnamese sitemap blog URLs remain; sitemap contains no duplicates.
- Five earlier English articles receive only counterpart-link updates where this batch now supplies an English target. Batch02 regression QA passes; no new layouts applied to earlier content.
- The original PMC reference is preserved and its generic English label corrected to its actual paper title. Summer heat/UV statements were cross-checked against Nature's original robe study, the cited PMC research and ARPANSA; no unsupported color-temperature guarantee retained.
- No homepage, Fourthwall, shop UI, Worker, routing or PR #9 changes.

Evidence: `docs/qa/en-batch03-static.json`, `en-batch03-images.json`, `en-batch03-responsive.json`, `en-batch03-regression-batch02.json`.

## Source verification for heat and UV
- https://www.nature.com/articles/283373a0 — original 1980 robe experiment; retained source link.
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8833350/ — Slip versus Slop: A Head-to-Head Comparison of UV-Protective Clothing to Sunscreen; retained source link.
- https://www.arpansa.gov.au/understanding-radiation/radiation-sources/more-radiation-sources/sun-protection-clothing — independent official cross-check of dye, weave, thickness and stretching factors, not a replacement for original sources.

## SEO limits
No GSC query × page dataset was available. Intent distinctions are editorial screening, not a confirmed cannibalization diagnosis. No deletion, merge, redirect or noindex of any VI URL. Subtype comparison remains separate from the pending detailed Cybergoth guide; oversized fit remains separate from hoodie outfits; mesh coverage/layering remains separate from the existing graphic-tee guide. Untranslated references remain clearly labelled Vietnamese rather than linking to nonexistent EN pages.

## Reproduction
```sh
python scripts/en_translate.py generate batch03
python scripts/qa_en_translations.py batch03
python scripts/qa_en_translations.py batch02
python scripts/qa_en_images.py batch03 /tmp/en03-images.json
```
The generator and wiring/QA helpers now accept a batch manifest. TSV translations remain source-hash locked and generation refuses missing Vietnamese segments. No placeholder pages or automatic untranslated fallbacks are emitted.

## Remaining queue
194 source articles still require complete translations and per-batch QA. Next priorities: E-Girl, detailed Cybergoth, Scene, general layering, dark-clothing care, goth beauty and the navigation hubs. Keep hubs distinct from definition pillars and comparisons.
