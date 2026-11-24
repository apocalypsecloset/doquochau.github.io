# Fourthwall Storefront via Cloudflare Worker

This public repo never stores the Storefront token. GitHub push protection rejects committing it as a secret.

1. Cloudflare dashboard → **Workers & Pages** → Create Worker (free tier is sufficient for a small store).
2. Copy the contents of `cloudflare/fourthwall-proxy.js` into the Worker's code editor, then deploy.
3. Worker → Settings → Variables and Secrets → Add → choose **Secret**. Name: `FOURTHWALL_STOREFRONT_TOKEN`. Paste the token privately in Cloudflare, deploy. Do **not** paste the token into GitHub.
4. Copy the deployed URL, e.g. `https://your-worker.your-subdomain.workers.dev`, to `assets/js/fourthwall-storefront-config.js` as `apiBase`. This URL is public and safe to commit. The Storefront token stays in Cloudflare.
5. Verify the home product loads real sizes/images. Choose Black / L, add to bag, check that Fourthwall Checkout receives one line item. Don't complete a real purchase while QA testing.
6. Review draft PR before merging. Production site (master) remains unchanged until merge.

**Do not use** Open API username/password, Stripe secret keys, or payment details in client-side JavaScript.

CORS allows only apocalypsecloset.com, www and localhost:8000. If the final domain differs, revise ALLOWED_ORIGINS.

## Site redirects and response headers

`site-delivery.js` is a separate, optional Worker for a GitHub Pages origin. It
returns a real 301 response for `/index.html`, preserves query strings,
and adds HTML security headers and versioned
asset cache policies. It leaves document bodies and private/no-store responses
unchanged. HSTS applies to the requested hostname without opting subdomains into
preload. The CSP enforces framing, object and base restrictions while preserving
the site's existing inline consent bootstrap and third-party integrations.

Apply these rules through Cloudflare Redirect Rules and response-header/cache
rules, or deploy the separate Worker after checking existing routes. Preserve the
existing Fourthwall API Worker and the more specific R2 image routes. This file
does not deploy itself: the production domain currently reads GitHub Pages, so
GitHub merging `_headers` and `_redirects` alone does not activate those policies.
After activation, verify `/index.html` returns HTTP 301 and check the root HTML
response for the configured headers. Test shop, authentication and consent.

The nine malformed Alt Fashion blog aliases have been removed without redirects
at the owner's request. All site links and the sitemap use only
`/blog/alt-fashion-la-gi-va-tai-sao-no-quan-trong.html` for that article.
The redundant `en/index.html` has also been removed; navigation uses `/`.
