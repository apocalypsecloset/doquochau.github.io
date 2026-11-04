# English translation batch31 — 2026-11-04

Baseline: master `424bc599b8038c9f015dcb3847602be49167226d`, 139/216 published translation pairs plus two EN-only originals. This batch implements ten complete translations; they are not counted as published until preview, normal PR merge and production verification.

## Intent ownership

| Vietnamese source | English counterpart | Primary intent boundary |
| --- | --- | --- |
| `/blog/office-siren-la-gi.html` | `/en/blog/office-siren-style-guide.html` | Fashion aesthetic around tailored lines, neckline and accessories; separate from Corporate Goth workplace specialist and actual business dress codes |
| `/blog/avant-garde-fashion-la-gi.html` | `/en/blog/avant-garde-fashion-guide.html` | Experimental fashion concepts, shape and construction; separate from any single dark aesthetic or product outfit specialist |
| `/blog/rockabilly.html` | `/en/blog/rockabilly-style-guide.html` | Rockabilly cultural and visual references; distinguish Punk, generic vintage and broad 1950s fashion |
| `/blog/light-academia-la-gi.html` | `/en/blog/light-academia-style-guide.html` | Light Academia visual vocabulary and outfits; distinguish existing Dark Academia and general preppy/academic style |
| `/blog/fairycore-la-gi.html` | `/en/blog/fairycore-style-guide.html` | Fairy-inspired nature imagery and styling; distinguish existing Fairy Grunge/Fairy Goth and broader Cottagecore |
| `/blog/angelcore-la-gi.html` | `/en/blog/angelcore-style-guide.html` | Angelic/ethereal visual styling; distinguish fairy/nature references and darker aesthetic collections |
| `/blog/mermaidcore-la-gi.html` | `/en/blog/mermaidcore-style-guide.html` | Aquatic aesthetic colors/surfaces and outfits; separate from mermaid-skirt garment construction and beach occasion guide |
| `/blog/mori-kei.html` | `/en/blog/mori-kei-style-guide.html` | Mori Kei cultural and layered forest-inspired wardrobe references; distinguish Cottagecore and Fairycore labels |
| `/blog/ouji-fashion.html` | `/en/blog/ouji-fashion-guide.html` | Japanese princely fashion vocabulary and proportions; distinguish Victorian Goth and Lolita-related comparisons |
| `/blog/cottagecore-la-gi.html` | `/en/blog/cottagecore-style-guide.html` | Rural/romantic visual wardrobe vocabulary; distinguish Mori Kei history, Fairycore imagery and Dark Academia |

## Editorial completeness and review

- All 1,527 indexed source text/alt segments are covered by nonempty translations with source SHA256 locks. Full body, H1/H2/H3, tables, captions, FAQs, metadata and internal anchor text are translated. The rendered articles total 19,688 English words, 263 headings, 61 original image placements, three tables and 25 FAQs. No empty or partial EN pages.
- The ten targets were screened against the tracker and existing EN articles. Office Siren remains a tailored internet-aesthetic definition; Corporate Goth retains Goth-workwear intent. Avant-garde focuses on experimental form, not the broader Alt overview. Rockabilly retains its music/cultural context, distinct from general vintage or a 1950s survey. Light Academia does not replace the Dark Academia specialist. Fairycore is separate from Fairy Grunge/Fairy Goth, Angelcore uses celestial imagery, Mermaidcore aquatic surfaces, Mori Kei Japanese forest-inspired layering, Ouji prince coordination and Cottagecore rural romantic imagery. These are overlapping editorial descriptions, not rigid taxonomies.
- All original images, image order, source attributes and external reference URLs remain. Existing repeated cover placements in Avant-garde remain as in the VI source. Dark Feminine camisole/jeans, asymmetric-top/denim and corset/cargo Looks are identified as related proportion or palette references, not complete officewear or Cottagecore uniforms.
- Fabric/fiber names do not establish ventilation, cooling, grip, comfort or durability. Actual weight, weave/knit, finish, lining, ease and conditions are distinguished. Brief movement checks are not laboratory tests or evidence of all-day comfort. Body type, gender, price and exposure are not aesthetic eligibility requirements.
- The archived Office Siren draft remains historical; the reviewed current TSV is in `data/en-translations/`. The French reference title is rendered in English while its original URL remains.

## Source verification and limits

- Original Office Siren Vogue/Vogue France reports were read during the prior drafting checkpoint; their 2024 reporting is identified as dated context, not current workplace policy or a current trend forecast.
- [The Met: Rei Kawakubo](https://www.metmuseum.org/exhibitions/listings/2017/rei-kawakubo) and [Manus × Machina](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina) provide exhibition context. [The Museum at FIT](https://www.fitnyc.edu/museum/about/index.php) is general institutional context, not proof of every internet aesthetic label.
- [FIT's 1950s timeline](https://fashionhistory.fitnyc.edu/1950-1959/) supports the limited period clothing discussion. [Rock Hall's Sun Records archive](https://library.rockhall.com/sun_records) and [Sun Records history](https://sunrecords.com/history/) were checked for the limited rockabilly music context; no single exact invention day is asserted.
- [Vogue's aesthetic-culture essay](https://www.vogue.com/article/do-i-have-an-aesthetic) and [FIT Exhibitionism](https://exhibitions.fitnyc.edu/exhibitionism/) provide broader context. Outfit systems and label boundaries are the site's editorial interpretation. [Vogue's original Afropunk coverage](https://www.vogue.com/article/afropunk-2023-street-style) is dated 2023 reporting, not a universal definition.
- Preserved [Mermaidcore runway/beauty report](https://www.vogue.com/article/mermaidcore-2024) is dated September 2023 despite its URL; the [beauty report](https://www.vogue.com/article/mermaidcore-beauty-trend) is dated October 2022. Neither is used as a current forecast.
- Original [Tokyo Fashion 2009 photographs](https://tokyofashion.com/mori-girl-fashion-in-harajuku/) and [2010 photographs](https://tokyofashion.com/japanese-mori-girls-in-wonder-rocket-fashion/) directly document layered Mori Girl outfits. Community accounts of the 2006 Mixi/Choco origin remain explicitly attributed and unverified as a single definitive origin. Natural Kei terminology varies; no unsupported exact founding date or exclusive definition is asserted.
- The preserved [Wunderwelt wardrobe-change](https://libre.wunderwelt.jp/en/15354/) and [alteration](https://libre.wunderwelt.jp/en/13126/) articles are general Lolita editorials, not proof of every Ouji historical claim. The [LolitaFetch editorial](https://lolitafetch.com/blogs/magazine/ouji-fashion-new-arrivals-edit) is a retailer's style perspective, not definitive historical authority or a current stock/price recommendation. Community-wiki references are retained with their limits.
- Cottagecore references retain dated commentary and dress examples. No current product prices, stock, shopping terms, venue or workplace policies are asserted.

## QA

- All ten VI sources match baseline bytes after removing only marked bilingual additions. Original VI titles, metadata, canonical, URLs/slugs, body and images remain. All 216 original VI sitemap URLs remain. Homepage/POD/Fourthwall/shop/routing/PR #9 untouched.
- All 30 manifest gates pass: source/tag/image/reference parity, FAQ/schema, HTML IDs, local targets and fragments, title/meta, self-canonical, reciprocal vi/en, sitemap and sequential unique Journal cards. All 151 EN pages have one H1, self-canonical and unique title/description/canonical.
- All 66 distinct HTTP image endpoints return 200 with image MIME. Twenty live browser views at desktop1440/mobile390 have no body overflow; images remain within article widths and all three tables use horizontal scrolling wrappers. The mobile Office Siren glasses FAQ opens and displays its complete answer. Mobile Cottagecore's long H1 wraps within the viewport.
- Guarded internal-link maintenance promotes 21 links in 13 older EN pages; original-language links remain. Those maintenance touches are not additional translations. Other metadata, bodies and assets are guarded; schema references follow visible link changes where required.
- No GSC query × page access is available: overlap screening is editorial only. No confirmed cannibalization diagnosis, deletion, consolidation, redirect or noindex change.

Evidence: `docs/qa/en-batch31-*.json`. Source-locked full translations: `data/en-translations/batch31.json` and ten TSV files. Preview and production checks remain required before marking publication.

## Release confirmation

PR #49 merged normally as `796fd146ee310ab63d1e3b0b3cfc0b0e6c6f6bf4` from reviewed head `aa8973fcfea94a5371c10593981aa512c6a8d986`; no check override. All 35 preview files and all 35 production files match byte-for-byte: ten new EN pages, ten VI pages, thirteen maintained older EN pages, Journal and sitemap. All five production-master checks succeeded; actual branch checks are recorded separately in `docs/qa/en-batch31-release-checks.json`. Final guarded link scan finds zero eligible links and zero skipped pages. The tracker now has 149 MERGED and 67 PENDING, plus two additional EN-only originals (151 Journal cards).
