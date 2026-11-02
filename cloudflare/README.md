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
