# Website audit fixes — 2026-11-05

Baseline: `a43f1b532bc7939f91fd4ef32472acf7215f1cd6`. Original site URL, homepage title, existing titles/descriptions/canonicals/H1s and all 216 original translation pairs are preserved.

## Implemented

- Cloudflare `_headers`: `noindex,nofollow` is scoped to Pages production aliases and branch previews, never a catch-all custom-domain path. `_redirects` defines permanent aliases while existing meta-refresh HTML stays available for GitHub Pages.
- Retired `/#outfit-grid`: replace all 369 occurrences across 367 pages with `/phoi-do-nu-ca-tinh.html#chon-phong-cach`, an existing, useful outfit directory section.
- Add the production-host-gated GA4 loader to the English area, including new pages. The shared loader guards against duplicate initialization and handles initialization after window load. Article-click/scroll classification includes `/en/blog/`.
- Shop: separate Color and Size; retain exact available variant IDs, prices and stock; choose real variant/color images and thumbnails. If a multi-color listing has no color-bound media, show PHOTO PENDING rather than borrowing another color. Product-wide photos are a fallback only for single-color products.
- Bag: Update quantity and Remove controls, current totals, expired-cart handling, transient-error preservation and Retry. Failed update confirmation locks further edits until the cart reloads. Checkout uses the existing Fourthwall checkout domain and cart URL format.
- Ecommerce: `add_to_cart`/`remove_from_cart` value tracks the changed quantity, with product name, variant, price and currency. Add `view_item_list`, `view_item` and `begin_checkout`; no synthetic `purchase` event.
- Product details and quality/return text are displayed from the actual Fourthwall featured-product response using text-only DOM construction. Add size/order-help links without inventing a size chart, delivery date or return promise.
- Full Solarpunk and White on White English counterparts, source-locked TSVs, reciprocal language links, sitemap, VI/EN Journal discovery and Vietnamese search-index entries. Original inventory stays 216; two new pairs live in `data/en-translation-extensions.csv`.
- Solarpunk receives a labeled original SVG editorial diagram, not a claimed product photograph. White on White reuses an existing article image as cover. Add their social images and article image/date metadata. Original source introduction dates are taken from first repository records: Solarpunk `b931d593d9b9d2d3255e8bde13cdafbfdd7d2d7e`, White on White `07cd5a8bc649e4a554a4adbf5055fdbd0045d030` (2026-10-16); these do not establish when Google first crawled them.
- Complete missing Article images for the four early EN guides using actual relevant images. Remove markup from the two original EN schema headlines while keeping visible H1 and title unchanged.
- Change only the two audited above-fold article cover loading attributes from lazy to eager/high priority.
- English privacy/website terms page based on the existing Vietnamese policy, with reciprocal language links and Fourthwall cart/order context. Existing Vietnamese policy text is retained.
- Add source and storefront quality checks, GitHub Actions and ignore local Python/dependency caches.

## Verification

- 608 HTML pages, 593 sitemap URLs, 218 VI–EN pairs, 220 English Journal cards.
- Existing metadata and H1 preserved on all 605 baseline HTML files.
- Original 216 VI files byte-identical outside the approved footer URL replacement and one cover-loading adjustment. All original image URLs, source wording, CTA wording, slugs and canonicals remain intact.
- Translation hash locks were refreshed only after the approved raw changes were independently checked. Hub preservation checks allow exactly the retired footer-link transformation; they do not broadly ignore body changes.
- All 37 current translation manifest gates pass, including 247 source text/alt segments, 3,890 English words and seven FAQs in the new pair. Historical batch05b is not double-counted.
- Node/jsdom shop regression checks cover color-bound photos, sold-out sizes, exact variant addition, quantities, removal payload/totals, ecommerce amounts, transient failure and expired-cart behavior. No real order or payment is used by these checks.
- New static release gate checks sitemap, metadata, fragments, local HTML/CSS/JS, JSON-LD, language pairs, production/preview headers and immutable existing SEO fields. Raw image-file existence is not interpreted as a live 404 because media is hosted outside Git.

## External verification and remaining constraints

Repository changes do not alter Cloudflare account rules, the deployed Fourthwall proxy secret, Fourthwall product listings, Firebase rules or private analytics accounts.

After deployment, inspect actual headers on `apocalypsecloset.com`, a VI article and an EN article; confirm no production X-Robots noindex while Pages aliases stay noindex. Check GSC URL Inspection and GA4 DebugView. Existing account-level Cloudflare/Zaraz tags may require separate inspection for duplicate tracking.

Fourthwall currently provides signed 1920px image URLs. The storefront does not rewrite their signature or claim thumbnail-byte optimization without a supported smaller image URL. CDN resizing and whole-site mobile CWV measurement remain external performance work. Large HTML hubs are preserved until actual performance data supports structural changes.

Confirm purchase reporting on Fourthwall, shipping/returns configuration and end-to-end real checkout separately; no payment is submitted. The English policy is a translation/context update, not a legal compliance certification. Image/CDN/R2 backup, full external-image HTTP crawl, GSC indexing/overlap and Firebase account/security verification require their respective services.

PR #9 and its unmerged branch are not merged or rewritten by this repair.

## Release checkpoint

PR #65 merged normally as `17fd97ab3fef4df7ea38f4a4ec15c053a2866eae`; reviewed head `81c9953667c00e250dc3125d2078d2ef6cc2d1bb`; reviewed/uploaded tree `f067f50a9fe2f58b0d02ae7dce752a826e0b1753`. Branch Cloudflare Pages and Website quality passed. The optional branch Workers build failed with no diagnostic annotations; its production-master counterpart subsequently passed. No check was disabled or overridden.

Production-master Website quality, Cloudflare Pages, Workers Builds, GitHub Pages build and report-build-status passed. GitHub Pages publishing itself timed out after remaining at `updating_pages` for ten minutes; its failed-job-only retry returned `Deployment cancelled`. Workflow run: https://github.com/apocalypsecloset/doquochau.github.io/actions/runs/42048899407 .

The custom-domain home was still the previous version during verification. The reviewed immutable Cloudflare preview renders the new Solarpunk, White on White and privacy pages without desktop overflow; this is not proof of custom-domain publication. New extension rows now accurately say COMPLETE_QA_PASSED and are not labeled production-verified. This documentation/data-only checkpoint supplies a fresh deployment commit; publication still requires live verification. No website code is changed in this checkpoint.
