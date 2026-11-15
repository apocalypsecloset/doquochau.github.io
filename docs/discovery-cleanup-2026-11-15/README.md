# Journal discovery and regression cleanup — 2026-11-15

Base: 447892106762e15b17be5c3145a81b470706fcec (merged image SEO PR #68).

## Corrections

- Publish all 436 Vietnamese and 438 English journal links as ordinary HTML anchors; retain current cards and add the 218 missing cards in each language.
- Preserve Vietnamese filters, search and pagination; add English progressive search and pagination, keeping every card available without JavaScript.
- Add related-reading links to six topic hubs in each language, outside the locked article main content. Every newly published article now has static incoming links.
- Replace the confirmed 404 White on White index thumbnail with its existing, verified cover.
- Use actual article images and measured dimensions for the two original English articles' Open Graph/Twitter metadata; correct their body image dimensions.
- Update lastmod for changed public pages. Preserve sitemap URL inventory and image entries, URL slugs, canonical, SEO titles, descriptions, CTA and original article content.
- Replace hardcoded journal counts with manifest-driven URL checks; require incoming article links; add a functional journal pagination/search test to CI.

## Validation

- Site gate: 1,044 HTML pages; 1,029 sitemap URLs; no errors.
- R2 image SEO gate: 440 articles; 2,384 image sitemap entries; no errors.
- All translated article/hub manifest gates pass.
- Five Node tests pass, including journal discovery and existing storefront behavior.
- The 11 intentionally omitted image positions per language remain omitted for documented duplicate/off-topic reasons.

Remote HTTP asset verification and deployment checks are recorded in the PR before merge.
