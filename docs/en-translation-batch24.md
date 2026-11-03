# Complete English collection hubs: batch24 — 2026-11-03

Baseline master `66158f6fc49e73ccba73f6afe42111caedb7d155`: **69 published / 216, 147 pending**. This batch adds ten complete hubs: **79/216 after publication, 137 pending**. The two EN-only originals are additional.

## Mapping and unique navigation intent

| VI source | EN counterpart | Primary intent |
|---|---|---|
| `/blog/goth.html` | `/en/blog/goth-guides.html` | Goth collection navigation; definition pillar, substyles and graphic tee styling remain separate |
| `/blog/egirl.html` | `/en/blog/egirl-alt-girl-guides.html` | Alt Girl umbrella and E-Girl collection navigation; E-Girl definition and Scene or Y2K specialists separate |
| `/blog/punk-grunge.html` | `/en/blog/punk-grunge-guides.html` | Punk and Grunge collection navigation, not another Goth vs Grunge or Grunge vs Punk comparison |
| `/blog/dark-feminine.html` | `/en/blog/dark-feminine-guides.html` | Dark Feminine collection navigation, separate from seven-formula outfit specialist and editorial essay |
| `/blog/baddie-streetwear.html` | `/en/blog/baddie-streetwear-guides.html` | Baddie streetwear collection navigation, separate from Badgirl definition, occasion outfits and item specialists |
| `/blog/phoi-do-theo-item.html` | `/en/blog/womens-item-styling-guides.html` | Top-level garment-guide directory; routes to category hubs rather than duplicating individual item answers |
| `/blog/phoi-do-theo-ao-nu.html` | `/en/blog/womens-tops-styling-guides.html` | Upper-body garment navigation; tee article and gothic graphic tee specialist retain distinct styling intents |
| `/blog/phoi-do-theo-quan-nu.html` | `/en/blog/womens-trouser-styling-guides.html` | Trouser category navigation; construction definitions, fabric comparisons and outfit formulas remain separate |
| `/blog/phoi-do-theo-chan-vay-vay-nu.html` | `/en/blog/womens-skirt-dress-styling-guides.html` | Skirt and dress category navigation; long black, denim, mini, midi and pleated specialists retain own targets |
| `/blog/phoi-do-theo-giay-nu.html` | `/en/blog/womens-footwear-guides.html` | Footwear navigation across definition, comparison, styling and care; combat-platform comparison remains separate |

## Complete translation and SEO review

- Full main DOM translated, including all introductions, routes, headings, card titles/descriptions, captions, image alt, gallery summaries and accessibility labels. All 124 guide cards and 153 image placements remain. All source references remain.
- 8,356 English words; 203 H2/H3 headings. Source-hash lock and paragraph/list/card/heading/figure/caption/gallery parity pass. Ten VI sources byte-identical after stripping only marked EN alternate and language-link additions.
- Every English hub has a self canonical, reciprocal VI/EN hreflang, one H1, English metadata, and CollectionPage/ItemList plus breadcrumb schema. ItemList names, order, URLs and count match visible cards. No fabricated BlogPosting or FAQ schema. All 216 VI sitemap URLs retained; all ten counterparts appear in the English Journal and sitemap.
- Internal links select completed English counterparts; remaining Vietnamese articles and outfit tools are explicitly labelled. Broken skip links were detected and corrected before publication.
- Goth hub directs to Goth definition, subtype specialists and existing graphic-tee guide where linked by source; it does not duplicate the definition pillar. Punk/Grunge hub routes to the separate Grunge-vs-Punk comparison, preserving the original Goth-vs-Grunge comparison. Tops directory remains navigation rather than a second graphic-tee styling article.
- No GSC query × page access. These are editorial intent distinctions, not a confirmed cannibalization diagnosis. No VI URL deletion, consolidation, noindex, redirects, or title/meta changes.
- Avoided carrying forward unsupported claims that Y2K is the hottest 2026 trend or that Indie Sleaze is replacing it; retained the corresponding style topics. Budget mentions are illustrative VND plans, not verified current prices.

## Implementation and QA

- New source-specific extraction and generation support main-only hubs, preserving full collection content and original image URLs/srcset. Existing article-only generator remains unchanged.
- Batch wiring supports either article or main, inserts missing VI self hreflang only inside a marked addition, and preflights all counterparts before editing source files.
- Standard QA dispatches hub batches to the collection release gate; all prior article manifest regressions pass.
- Browser QA: twenty views at 1440px and 390px, one H1 each, no horizontal document overflow. Cards render in three desktop columns and one mobile column. Goth gallery expands; mobile image width 305px within its container.
- Evidence: `docs/qa/en-batch24-{static,regressions,responsive}.json`. Image endpoint and deployment results are recorded separately when complete.
- Scope excludes homepage, POD, Fourthwall, shop/checkout UI, Worker/routing and PR #9.

## Reproduction

```sh
python scripts/en_translate_hubs.py generate batch24
python scripts/sync_en_batch.py batch24
python scripts/qa_en_translations.py batch24
python scripts/qa_en_images.py batch24 /tmp/en24-images.json
```

Image QA complete: **139/139** distinct original/responsive image endpoints return HTTP 200 and image MIME. Evidence: `docs/qa/en-batch24-images.json`.
