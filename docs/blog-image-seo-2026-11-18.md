# Blog image fixes — 2026-11-18

The English journal previously exposed 442 catalogue links and three featured
links as text-only cards. Articles had covers, but one translated page used a
malformed data-URI placeholder in its social and structured image metadata.
Most photographs had no choice of responsive widths, and some declared
dimensions did not match the decoded files.

## Result

- All 445 English catalogue/featured cards have a real, localized thumbnail,
  dimensions, lazy loading and responsive candidates. Catalogue URLs, order,
  dates, search, topic filters and pagination stay unchanged.
- The 848 articles and 34 collections use verified responsive photographs.
  Nine redirect stubs remain redirect stubs. The two existing SVG instances
  remain vectors and do not need raster derivatives.
- Fixed OG, Twitter and schema image metadata for
  `en/blog/alternative-going-out-outfits-women.html`. Its real cover loads from
  HTML immediately. The Vietnamese counterpart also no longer relies on a
  JavaScript-delayed placeholder or duplicate no-script figure.
- Filled missing localized OG/Twitter image descriptions from existing image
  descriptions. Synchronized HTML/OG and existing ImageObject dimensions with
  the decoded images. Images, their descriptions and their ordering are
  preserved; photos are resized, never cropped or replaced in article content.
- Image sitemap entries now describe the actual editorial origins on every
  published blog page. Page URLs, order, lastmod and other sitemap fields stay
  unchanged. The original R2 files remain available and are not overwritten.

## Files and delivery

`data/blog-image-seo-2026-11-18/assets.json` records 2,283 original WebP URLs,
their SHA-256, decoded dimensions and actual variants. The site includes 4,942
new static WebP files, 321,050,302 bytes (about 306.2 MiB), under
`assets/images/blog-responsive/`. Both languages share these files. They work
on the existing static hosting, without enabling a new paid transformation
service or configuring bucket credentials.

The width choices are 320, 640 and a larger existing/optimized source, without
upscaling. Smaller original images use their actual widths. Existing files
larger than 200 KiB receive a compressed larger derivative; quality is at
least 74, with further downscaling when necessary to meet the budget.

- Every 320-pixel candidate is under 50 KiB (largest about 49.9 KiB).
- Every 640-pixel candidate is under 160 KiB (largest about 158.1 KiB).
- Every raster candidate served by the new srcsets is under 200 KiB.
- Across the 2,283-URL inventory, the sum of default 640-pixel fallback bytes
  is 48.5% smaller than the sum of original bytes. This is an asset comparison,
  not a measured page-load or Core Web Vitals improvement.

`src` remains a real image URL when JavaScript is disabled. `<picture>` source
attributes are updated too, so an older one-size source cannot override the
responsive `<img>`. Existing explicit layout sizes are retained; new values
match article and card layouts. The new English card styles are scoped to its
journal and featured sections.

Existing EXIF, XMP and ICC data are carried into derivatives when present.
No authorship, copyright ownership or generation-source labels are invented.

## Verification and preservation

Run with Python dependencies from `scripts/requirements-images.txt`:

```text
python scripts/qa_blog_image_seo.py
python scripts/qa_topical_editorial.py
python scripts/qa_repository_cleanup.py
python scripts/qa_site.py
node --test scripts/test_shop.cjs scripts/test_journal.cjs scripts/test_privacy.cjs
```

The image QA decodes and hashes every generated file, checks real srcset width
descriptors, fallback existence, the original identity/order/alt of each image,
social metadata, schema dimensions, all 445 target-page thumbnails and exact
sitemap coverage. It compares each changed HTML page against pinned
`166c8047`, allowing only the explicit image changes, thumbnail insertion and
removal of the two delayed-cover loaders/fallbacks. Article prose, headings,
navigation, links, metadata outside image fields and other scripts are checked
for preservation.
Existing trailing spaces on changed image lines are removed; other editorial
whitespace is preserved. Text successor hashes normalize Windows line endings;
binary image hashes always verify the exact file bytes.

Earlier editorial and cleanup assertions retain their pinned predecessors.
`blog_image_release.py` accepts only exact successor hashes registered in
`release.json`; unknown edits fail. Current topology/link checks still run
against current HTML, and the new image QA runs independently in Website
quality. The existing journal historical pin is retained through its exact
image successor record; functional tests use the actual current DOM.

To reproduce the asset files with the reviewed originals:

```text
python scripts/build_blog_image_assets.py --cache PATH_TO_ORIGINAL_CACHE
python scripts/fix_blog_image_seo.py
```

The build verifies origin and existing derivative hashes before reuse. Changes
to origin content require a new review rather than silently substituting a
different photograph. Regenerating a release also requires updating its exact
successor records after review.

Visual QA covers the English journal at desktop and 390-pixel mobile widths,
including actual loaded candidates, responsive layout, representative image
quality, and the repaired going-out article. This release does not claim that
Google has indexed every image or that field Core Web Vitals have improved.
