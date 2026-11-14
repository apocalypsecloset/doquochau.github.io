# R2 images and sitemap publication — 2026-11-15

Approved scope: 220 Vietnamese articles and their 220 existing English counterparts, resolved through current hreflang links. User authorized sitemap publication and merge after verification.

## Images

All 1,205 expected production image URLs were fetched after the latest upload: HTTP 200, Content-Type image/webp, x-ac-storage r2. Every file decoded at 1080×1920. See `url-audit.json` for SHA-256 and results. This verifies the exact public paths, not an inventory of unrelated bucket objects.

2,380 image insertions (1,190 per language). Existing images and covers remain. New image src URLs use the production domain so branch previews load the same R2 resources. Existing CSS classes are reused; body images load lazily, covers eagerly with high priority. Captions/alt are localized conservative topic labels.

22 comments intentionally remain: 10 duplicate-image positions and one clearly off-topic position per language. No duplicate mapped image hash is inserted within an article.

| VI slug | Unfilled positions per language | Reason |
|---|---:|---|
| cach-that-khan-quang-co-dai-cho-nu | 2 | identical image content |
| chan-vay-do-do-ket-hop-voi-ao-mau-gi | 1 | identical image content |
| chan-vay-hoa-nhi-dang-dai-phoi-voi-ao-gi | 1 | cover/body identical content |
| dam-cham-bi-co-dien | 3 | identical image content |
| kieu-toc-mac-ao-dai | 1 | identical image content |
| phoi-do-voi-ao-long-cuu | 2 | identical image content |
| quan-the-thao-nu | 1 | Bermuda photo is off topic |

All 32 temporary substitutes were visually reviewed in two contact sheets. Sherpa, scarf, skirt and polka-dot photos broadly match their topics; duplicates are omitted. Sweatpants, raglan/singlet and sneaker photos illustrate casual styling, without claiming running/gym performance. The clearly off-topic Bermuda photo is withheld. Full visual semantic review of the other 1,173 images is not claimed.

## Sitemap and indexability

Added 436 missing URLs; two VI/EN pairs already existed. All 440 URLs appear exactly once, with lastmod 2026-11-15. The 436 newly published pages change robots from noindex, follow to index, follow to align with their sitemap inclusion. Preview-domain noindex headers stay enabled. Sitemap now contains 1,029 URLs.

All other bytes outside the inserted image figures and explicitly approved robots change remain identical to original master on 440 articles. Slugs, canonicals, titles, descriptions, hreflang, CTA, original images, article text and CSS are unchanged. See `preservation-qa.json`.

`data/r2-220-publication.json` explicitly lists approved new publications. Sitemap gates require the union of the original translation inventory and these 220 pairs, with uniqueness and canonical checks; original 216-row inventory remains untouched. Batch39 source locks are refreshed for Solarpunk and White on White. Reindexed TSV preserves all 247 preexisting translations.

## Evidence and deployment

- `publication-qa.json`: new sitemap URLs, per-article robots and image URL changes.
- `static-publication-qa.json`: 1,044 HTML pages checked, 1,029 sitemap URLs, 605 original metadata records preserved, zero errors.
- `insertions.json`: relative image identities and original slot positions; final inserted src uses https://apocalypsecloset.com plus each image identity.
- `article-report.json`: insertion counts and intentionally unresolved slots.
- `preservation-qa.json`: exact permitted-change and mapped-image uniqueness checks.
- `preview-html-qa.json` and `batch39-qa.json` record the initial integration verification, before sitemap publication.

Initial Pages preview deployed successfully and all 440 HTML responses matched reviewed bytes. Image src URLs were subsequently made absolute to fix preview-only R2 404s. Final branch build/render and production checks are recorded in the PR discussion.

Workers Builds also fails on original master 74fc9528ea65cdf778c91824d6b58dac47243797, while Pages and Website quality succeed. This is a preexisting separate build failure, not introduced by this PR; no checks are disabled or bypassed.
