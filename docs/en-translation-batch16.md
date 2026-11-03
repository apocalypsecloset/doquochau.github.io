# Translation release 16 — What Is an Outfit (2026-11-03)

## Scope
- Original VI: `/blog/outfit-la-gi.html`.
- New English counterpart: `/en/blog/what-is-an-outfit.html`.
- After merge: **44/216** full VI→EN translations, **172 pending**, plus the two original English-only blog articles.
- Distinct English intent: What an Outfit is, how pieces form a complete look; separate from OOTD daily-look posts and fashion aesthetic explanations.

## Source and translation
- VI source SHA-256: `f5dcb6e2ac4ac247754775f21af35176d68d4c4b7181b9237bacb28f24ab1d89`.
- 116 unique text/image-alt segments completely translated, including full body, original mini-terminology table, outfit components and the additional style map updated July 17, 2026.
- Exact source parity: 13 H2, 1 three-column table with 5 rows, 5 figures/captions, 6 original content images in order, 20 list items, 1 blockquote and 4 FAQ answers.
- Original VI page/SEO fields byte-exact after removing only marked reciprocal EN hreflang and English switch.
- Four FAQPage schema questions and answers exactly match visible copy. Original Merriam-Webster and Vogue references preserved. EN link to published OOTD page.

## Static SEO QA
- Exactly one English H1, EN self canonical, reciprocal VI/EN alternate hreflang, BlogPosting/FAQPage/Breadcrumb structured data.
- English Journal links to the real translated HTML page.
- Sitemap retains **216 VI article URLs** and **46 EN blog URLs** (44 translations + 2 original EN-only guides), with no duplicates or linked HTML pages missing.
- No broken fragment anchors.
- Cloudflare Pages passed on prior branch head 48b839af2f2d3acf3fd1a5ef95793ce6ed97cdc8.

## Remaining QA limits
- Live production HTTP/images, mobile/desktop browser at 390/1440px, standalone Python QA and GSC query/page overlap not independently tested. Workers Builds preview failed as in prior translation branches; no Worker edits.
- No changes to homepage, shop, POD, Fourthwall, checkout or VI URL/title/canonical/meta.
