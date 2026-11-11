# English translation release 08 — women's cargo pants (2026-11-03)

## Scope and primary intent
- Original: `/blog/phoi-do-voi-quan-cargo-nu.html`
- English: `/en/blog/womens-cargo-pants-outfits.html`
- After merge: **36/216** Vietnamese-to-English translations completed, **180 pending**, plus the two pre-existing EN originals.
- Intent: ten practical cargo outfit formulas, **not** cargo definition, material selection or purchase guide. Editorial intent screening only; no GSC query/page overlap evidence.

## Complete content
- **177 distinct text and image-alt segments** translated and source-locked via `data/en-translations/phoi-do-voi-quan-cargo-nu.tsv` and `batch08.json`.
- Ten outfit formulas, two tables (11 rows, 8 headers and 36 cells), 15 H2, four figures/captions, five original images including cover, 21 list items and five FAQ answers.
- All original internal and external references preserved; completed VI article links route to available English versions.

## Static SEO QA performed
- The Vietnamese original matches the previous master byte-for-byte after removing only marked reciprocal hreflang and visible EN switch.
- Exactly one EN H1, EN self-canonical, reciprocal VI/EN alternates, BlogPosting/FAQPage/BreadcrumbList JSON-LD.
- All five visible FAQ answers match the FAQPage schema.
- All five original image src paths preserved in order and provided with English alt text.
- All source structure counts above match English counts.
- No broken local fragments or HTML destinations absent from sitemap, no duplicate sitemap URLs.
- **216 Vietnamese** sitemap blog URLs retained; **38 English** blog URLs (36 translated pairs + 2 original English editorials).
- English Journal links to the actual completed EN page.

## CI and limits
- Cloudflare Pages build for commit ca3f2c2ffc755f94d5af792fb7f4c5f33efc500b succeeded.
- Workers Builds status on branch should be checked separately; the translation does not change Worker or routing files.
- Existing standalone Python QA script, actual 390px/1440px browser rendering, image endpoint HTTP checks, GSC query×page and production URL contents were **not** independently tested in this session. No claim of those gates passing.
- No homepage, POD, shop, Fourthwall, or original Vietnamese SEO field changes.

## Next
Continue 180 remaining Vietnamese articles, prioritize related cargo accessories and graphic tees with one distinct primary search intent per EN URL.
