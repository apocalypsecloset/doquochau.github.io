# English internal-link refresh — 2026-11-04

Status: local QA complete; preview and deployed-file verification pending. Translation count remains **109/216 published, 107 pending**.

Older English articles and collections still linked to Vietnamese references whose complete English counterparts were published in subsequent batches. This change promotes **354 content links in 82 English pages** to their existing English counterparts. It removes only the redundant `(Vietnamese)` suffix and VI reference attributes for promoted links. It is a language-navigation repair, not a cannibalization diagnosis.

- Every link to a page's own Vietnamese original remains unchanged, including the different wording in the two handcrafted initial translations. Corporate Goth and Soft Goth remain byte-for-byte unchanged by this maintenance.
- No VI page, title, meta, canonical, hreflang pair, image URL/alt, heading, paragraph, table or content node changes. Homepage, POD, Fourthwall, shop, routing and PR #9 untouched.
- Changes are confined to exact anchor spans and JSON-LD bodies that actually need updating. Surrounding HTML source bytes and formatting are retained. FAQ/ItemList JSON-LD stays synchronized with visible link labels and card URLs.
- Target pages must exist; fragment targets must exist or the original VI reference is retained and reported. No missing fragments were found in this run.
- All 26 manifest gates pass. The 216 tracker VI URLs exactly match the VI sitemap inventory. Guard checks preserve SEO tags, all image attributes, content-node counts and body text except redundant reference-language suffixes.
- An immediate second run reports zero eligible changes, demonstrating the operation is idempotent.
- Sixteen browser views across four collections and four articles at 1440px/390px have no page horizontal overflow. Original-language switches still point to VI. Opening the Mary Jane card from the mobile footwear directory loads the English page with `lang=en` and its self-canonical.

Evidence: `docs/qa/en-internal-links-refresh.json` (all before/after URLs), `en-internal-links-regressions.json`, `en-internal-links-responsive.json`.

## Future batches

After completing and generating all translations in a batch, sync reciprocal alternates/sitemap/Journal, then run:

```text
python scripts/refresh_en_internal_links.py --apply --report docs/qa/<batch>-internal-links.json
```

Run all release gates and browser checks for the affected scope before PR/merge. Default invocation is read-only; `--apply` changes only eligible references to existing EN files. Never replace original-language switches with self-links.
