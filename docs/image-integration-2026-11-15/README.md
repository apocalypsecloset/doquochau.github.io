# R2 image integration — 2026-11-15

Base: `74fc9528ea65cdf778c91824d6b58dac47243797` (`master`).

All 1,205 expected public paths were fetched with GET after the latest upload. Every response is HTTP 200, Content-Type image/webp, x-ac-storage r2. All bodies decode as WebP at 1080 × 1920. SHA-256 values are recorded. This verifies the 1,205 exact public object paths; it does not enumerate unrelated bucket objects or prove their absence.

## Changes

- 220 VI and 220 existing EN counterparts resolved from current VI hreflang links.
- 2,380 insertions: 1,190 per language. Existing covers in Solarpunk and White on White remain unchanged. Existing White on White body images remain unchanged.
- Only COVER_IMAGE_SLOT / IMAGE_SLOT comments are replaced. Existing CSS classes are reused. Body images load lazily; new covers use eager loading and high priority. Intrinsic dimensions match decoded files.
- All head bytes stay identical, including title, description, canonical, robots, hreflang, OG/Twitter and schema. All bytes outside exact image-slot replacements stay identical, preserving CTA, article text, links, layout templates and existing images.
- Captions and alt text are localized, conservative topic labels. They do not assert unverified garment details or sporting performance.

## Intentionally unresolved

22 comments remain across both languages: 10 duplicate-content positions and one off-topic position per language. No duplicate image content is inserted within an article. Hash equality catches duplicates even when filenames differ.

| VI article slug | Unfilled positions per language | Reason |
|---|---:|---|
| cach-that-khan-quang-co-dai-cho-nu | 2 | identical image content |
| chan-vay-do-do-ket-hop-voi-ao-mau-gi | 1 | identical image content |
| chan-vay-hoa-nhi-dang-dai-phoi-voi-ao-gi | 1 | cover/body identical content |
| dam-cham-bi-co-dien | 3 | identical image content |
| kieu-toc-mac-ao-dai | 1 | identical image content |
| phoi-do-voi-ao-long-cuu | 2 | cover/body or body/body identical content |
| quan-the-thao-nu | 1 | source photo shows Bermuda shorts, not athletic pants |

The 32 temporary substitutions were visually reviewed in two contact sheets. Sherpa, scarf, skirt and polka-dot photographs match broad topics; repeated content is omitted. Sweatpants images show casual styling; athletic-top substitutes are casual raglan/singlet outfits. Running/gym shoe substitutes show casual sneakers; suitability for running or gym use cannot be established from the pictures. Captions describe the visible casual categories and do not certify performance. These substitutions remain editorial review items. The clearly off-topic Bermuda photo is withheld.

## QA evidence

- `url-audit.json`: all public GET results, dimensions and SHA-256.
- `insertions.json`: exact file, original slot and inserted image path.
- `article-report.json`: 440 article results, retained existing positions, unresolved positions.
- `preservation-qa.json`: all 440 files pass byte-preservation checks and mapped-image content uniqueness.
- `source-mapping.csv`: supplied mapping with local source-machine paths removed.
- `git diff --check`: passes.

A local Chromium render could not start because the execution environment rejects its process socket. Responsive rendering and deployed branch checks must be verified before merge. No merge performed. Full visual semantic review of the other 1,173 images is not claimed; all 1,205 files were decoded and technically checked.

## Branch publication checks

Initial commit `2335e9dcccd6b89ee10e41f98de23017a5519466`: Cloudflare Pages deployment succeeded at https://ccbd2d4f.doquochau-github-io.pages.dev . All 440 deployed HTML files were fetched and match reviewed local bytes (`preview-html-qa.json`). A sample relative image request on this preview domain returns 404, while the exact production-domain image returns HTTP 200 from R2; preview image routing is therefore not equivalent to production. A responsive visual pass is still pending.

The Website quality shop tests and static site check passed. Translation gates passed through batch38; batch39 failed only the two source hashes for Solarpunk and White on White, which changed when image comments were replaced. Both source locks are refreshed and both TSV tables are reindexed against exact source strings, preserving all preexisting translations and adding only localized image labels. No test is removed or bypassed. The batch39 check now passes locally (`batch39-qa.json`). Existing EN data-source-sha256 attributes retain their historical translation provenance; no extra HTML changes are made.

A separate Workers Builds check failed without diagnostic annotations on the initial branch commit. Do not represent this as an all-green release or merge until that check and visual review are resolved.
