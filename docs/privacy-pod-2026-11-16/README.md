# Privacy, basic analytics consent and POD policies

Authorized scope: synchronize Privacy VI/EN, gate analytics behind optional consent, publish separate bilingual Terms, Shipping and Returns/Refund pages, QA, merge and verify production. Baseline `0e12619` (PR #75).

## Implementation

- Shared early privacy bootstrap, before any legacy Google code. Remove 605 directly embedded Google tags and the old inline/delayed Google initializers. Every actual HTML document loads the bootstrap; the headless Google verification file is preserved. Version the existing shared analytics loader to avoid stale unconditional initialization.
- Basic consent mode: no Google script or analytics event queue before affirmative choice. Reject/accept/settings use equally styled controls, an unchecked optional analytics checkbox and an accessible native settings dialog. Necessary-only keeps account and cart storage. Advertising storage, advertising user data and ad personalization stay denied.
- Store a versioned choice for 180 days. Respect Global Privacy Control. Handle missing/expired/future/malformed choices, storage denial and cross-tab updates. Withdrawal disables GA, removes first-party GA cookies and reloads a document where Google is not loaded. Already transmitted data requires a separate data request. No attempt is made to control third-party storefront cookies from this domain.
- Analytics starts only on the production domain and www alias after consent. Existing shop/login callers use the same gated gtag wrapper. No replay of pre-consent events. New GA cookies have 180-day expiry without per-view renewal, Google signals/ad personalization disabled; custom blog search events carry query length instead of the raw query. Page location/referrer config excludes query strings/fragments. This is not a claim that provider data is wholly anonymous or that every account-side GA setting is verified.
- Privacy VI/EN use matching section IDs and describe actual Firebase/Firestore, Cloudflare, optional GA4, local storage, Fourthwall order/customer sharing and external Shopee attribution. Preserve existing privacy URLs, SEO titles, descriptions and H1; preserve the existing #terms-of-service anchor with a link to the separate terms page. No invented legal name, registered address, tax number, processor region or GA account-retention setting.
- Add terms.html, shipping.html, returns.html and three /en/ counterparts, with reciprocal hreflang, self canonicals, WebPage/breadcrumb/brand schema and six additional sitemap URLs. Static policy navigation on all policy pages and homepage; settings/policy access on other pages through the shared UI. Add a homepage note that standard POD returns do not limit mandatory consumer rights.
- Shipping uses destination/product checkout estimates, never an invented worldwide delivery promise. Returns distinguishes defects, normal sizing/change-of-mind requests and eligible EU/EEA/UK withdrawal rights; made-to-order alone does not remove those rights. Fourthwall remains the transaction merchant of record. Order support uses the actual shop domain/contact route; no return address or fixed bank posting time is fabricated.

## Sources checked 2026-11-16

- https://developers.google.com/tag-platform/security/guides/consent?consentmode=basic
- https://fourthwall.com/legal/privacy-policy
- https://fourthwall.com/legal/merchandise-privacy-policy
- https://fourthwall.com/legal/merchandise-terms-of-service (3.2–3.4)
- https://help.fourthwall.com/frequently-asked-questions/shipping-and-orders/returns-refunds-and-quality-issues
- https://help.fourthwall.com/frequently-asked-questions/shipping-and-orders/shipping-and-delivery-expectations
- https://policies.google.com/privacy
- https://www.cloudflare.com/privacypolicy/

## Preservation and QA

`reviewed-html.json` records exact before/after hashes for all 1,044 existing HTML files. The new independent gate regenerates the exact allowed script-only transformation from the baseline for every page except the two authorized Privacy bodies and the exact homepage policy additions; it separately checks original SEO/H1 and bilingual policy source text. It rejects arbitrary additional changes. `content.json` is the reviewed bilingual policy source.

Historical editorial/translation gates recognize only these exact reviewed successor hashes before comparing their former baseline. Translation source hashes continue identifying the same editorial content before this script-only maintenance; no article translation, alt, image, slug, canonical or SEO title is changed. Six new policy pages are checked independently rather than compared to nonexistent historical pages. All previous semantic gates remain enabled, with the new privacy gate and eight consent tests added to CI.

Local test and release results, browser preview, merge and actual production verification are recorded in the PR. Browser settings UI alone is not proof of authenticated Firebase operation, receipt of GA reports or universal legal compliance. Cloudflare security-header/Workers build issues from #75 remain outside this authorized change.
