# Exclude internal files from the primary GitHub Pages publication

Baseline: `da423fe` (PR #73). The custom domain currently serves GitHub Pages through Cloudflare. `_headers` does not apply to GitHub Pages; internal QA reports, translation drafts and source tools therefore remained deployable despite the Cloudflare-only noindex rules.

Add Jekyll's `_config.yml` `exclude` entries for `docs/`, `data/`, `scripts/` and `cloudflare/`, retaining the default dependency exclusions. Source files remain in GitHub for editing and QA. Public HTML, sitemap, images, CSS, JavaScript, redirects, shop configuration and article content are unchanged.

Before this change, scan 1,279 runtime HTML/CSS/JS/JSON/XML/TXT/SVG files outside those four source directories. No literal reference to an excluded directory is present, including parent-relative paths. The excluded baseline holds 248 docs files, 270 data files, 24 source scripts and two Cloudflare proxy source/docs files (9,273,754 bytes). This is a deployed-output cleanup, not a secrecy claim about a public repository.

Validation: inspect the final GitHub Pages build/deploy, confirm the sampled formerly public source URL now renders 404, and check homepage/shop, blog and sitemap remain available. Record results in the pull request. The local runtime has no Ruby/Jekyll, so do not claim a local Jekyll build.

Cloudflare Pages uses separate build settings. Its noindex response headers remain; this configuration does not restrict its output. Applying primary-domain security headers still requires authenticated Cloudflare access. The dashboard is currently signed out; no DNS, routing or security settings were changed.

Reference: https://jekyllrb.com/docs/configuration/options/ (exclude directories/files).
