# English translation release 07 — Punk Makeup (2026-11-03)

## Scope
- VI source: `/blog/punk-makeup-dark-aesthetic.html`
- EN page: `/en/blog/punk-makeup-dark-aesthetic-guide.html`
- Progress after merge: **35/216** complete translations, **181 pending**; two earlier original EN guides remain separate.
- Primary intent: actionable punk makeup techniques; clothing history, Goth definition, Grunge fashion and E-Girl guides retain separate intents.

## Source-complete content
- All **159 distinct text and image-alt segments** translated and source-locked in `data/en-translations/`.
- Six complete makeup formulas, 12 H2, nine H3, four figures and captions, six original images including the cover, two tables (10 total rows), 21 list items, one blockquote, five FAQs and the original three external references.
- English Journal and sitemap include only the actual completed page.
- Original Vietnamese source byte-identical after stripping only marked VI/EN alternates and visible language switch.

## Static QA performed
- One EN H1, self canonical, reciprocal language alternates, BlogPosting, FAQPage and BreadcrumbList JSON-LD.
- All five visible FAQ answers match structured data.
- No missing internal HTML destinations from the sitemap or broken local fragment anchors; all original external links retained.
- All six source image paths preserved and English alt attributes populated.
- All original 216 VI sitemap entries remain, 37 EN entries (35 paired translations + two prior English originals), no duplicates.
- The existing QA script was narrowly updated to treat the proper French brand name L'Oréal as an allowed proper noun (as it already did for French words such as cafés); this does not relax the prohibition on Vietnamese copy.

## Deployment and remaining checks
Cloudflare Pages succeeded for the initial translation commit e2fd908f7e20909eddfe8800a3b42e584a1fd33b. Workers Builds failed on that branch, also observed on earlier master builds; this article changes no Worker, shop or routing files. Check the latest commit and post-merge builds separately.

The standalone Python QA script, browser at 390px/1440px, HTTP image endpoints and GSC query×page cannibalization have **not** been executed in this session; do not present these as passed.

## Follow-up
Continue 181 pending articles in complete source-locked batches, prioritize cargo/graphic tees and alternative outfits. Preserve existing Vietnamese SEO metadata, images, URLs and POD checkout flows.
