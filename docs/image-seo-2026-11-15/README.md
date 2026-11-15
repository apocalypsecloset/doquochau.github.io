# Image SEO repair — 2026-11-15

Baseline: master `f0be5d3535c63433f75efc9dd67614767ae8109c` (PR #67). Scope: the approved 220 Vietnamese articles and 220 existing English counterparts.

## Result

- 440 pages have real editorial photography in OG, Twitter large-image cards and Article/BlogPosting ImageObject metadata, with localized alt/caption and actual dimensions. Solarpunk keeps its existing visible SVG cover diagram; its social/schema image uses the first actual editorial photograph.
- 440 existing sitemap URL entries now include their actual on-page editorial images using image:image/image:loc. No page URLs are added or removed. Total sitemap remains 1,029 page URLs. This batch has 2,384 image references representing 1,192 distinct assets (1,191 WebP photos and one existing SVG diagram).
- 2,382 image alt texts and available captions receive reviewed VI/EN descriptions. Removed generic labels such as Hình minh họa, Ảnh minh họa, Fashion illustration and Cover illustration from image alt/caption. Language in article prose that discusses example images remains when semantically relevant.
- Reviewed 1,190 originally inserted image files in 22 contact sheets, plus the White on White replacement cover individually. The descriptions identify visible subjects and close-ups/comparison views; similar subjects may share descriptions. They do not assert sports performance, metal purity, authenticity or fiber certification from appearance alone.
- Five legacy White on White URLs returned HTTP 404. Their five broken body figures per language are removed, and the broken cover is replaced by the existing, separately reviewed R2 cover white-on-white-outfits.webp. Both languages now have one cover and five distinct body photos. No R2 objects are renamed, deleted, overwritten or generated.

## Preservation and scope

Titles, meta descriptions, canonicals, hreflang, robots, article text outside image captions, all links/CTA and CSS remain unchanged. Image source/loading/dimension attributes stay unchanged except the explicitly documented White on White 404 repair. Existing healthy images are retained. Existing 11 omitted duplicate/off-topic slots per language remain omitted.

No resized derivatives or srcset variants are invented; the existing verified WebP sources remain in use. Search indexing, image ranking and Core Web Vitals improvements are not guaranteed or claimed.

## Reproduction and evidence

- `image-descriptions.json`: filename-keyed bilingual descriptions, reviewed subject and view classification.
- `visual-review.tsv`, `review-manifest.json`: compact review audit for the original 1,190 images. The replacement cover was reviewed separately and is included in image-descriptions.json.
- `changes.json`: per-page metadata cover and exact sitemap image list.
- `assets-qa.json`: current asset availability, decoded dimensions and hashes. The five retired 404 URLs are no longer referenced.
- `qa.json`, `static-qa.json`, `translation-qa.json`: scoped preservation/image gates, static site QA and complete translation/hub checks.
- `scripts/fix_r2_image_seo.py`: deterministic application of the reviewed text, White on White repair, metadata and sitemap entries.
- `scripts/qa_r2_image_seo.py`: verifies all 440 pages, original SEO fields/body/CTA, image sources and exact sitemap coverage. Added to the existing Website quality workflow; no existing gate is removed or bypassed.

Batch39 source hashes and text-segment TSV indices are refreshed for Solarpunk and White on White. Existing non-image text translations are retained; only image-caption/alt segments and retired 404 captions change.
