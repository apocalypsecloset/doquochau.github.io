# English translation batch32 — 2026-11-04

Baseline: master `294db2de4ca40d907b5579eec3e2b895c806228d`, 149/216 published translation pairs plus two EN-only originals. Ten complete translations are implemented. Published through PR #51 after preview, normal merge and production verification; see release confirmation below.

## Intent ownership

| Vietnamese source | English counterpart | Primary intent boundary |
| --- | --- | --- |
| `/blog/business-casual-la-gi.html` | `/en/blog/business-casual-women-guide.html` | Workplace formality and practical garment choices; Corporate Goth and Office Siren retain their aesthetic-specific intents |
| `/blog/smart-casual-la-gi.html` | `/en/blog/smart-casual-women-guide.html` | Mixed-formality dress guidance by setting; separate from Business Casual work context and Casual Chic visual finish |
| `/blog/power-dressing.html` | `/en/blog/power-dressing-style-guide.html` | Clothing and perceived authority through silhouette/context; Office Siren internet persona remains narrower |
| `/blog/preppy-style-la-gi.html` | `/en/blog/preppy-style-guide.html` | Uniform and collegiate style vocabulary; Ivy historical reference and Academia specialists remain separate |
| `/blog/ivy-style.html` | `/en/blog/ivy-style-guide.html` | Ivy League style context and wardrobe references; broader Preppy overview retains its own primary target |
| `/blog/classic-style-la-gi.html` | `/en/blog/classic-style-women-guide.html` | Classic-style wardrobe lines and repeated garment relationships; separate from vintage-period dressing and quiet-luxury material claims |
| `/blog/casual-chic-la-gi.html` | `/en/blog/casual-chic-style-guide.html` | Relaxed-polished visual styling; distinguish dress-code guidance and minimalist wardrobe philosophy |
| `/blog/quiet-luxury-la-gi.html` | `/en/blog/quiet-luxury-style-guide.html` | Understated quality and assessing garments; separate from Old Money social imagery and general Classic Style |
| `/blog/old-money-la-gi.html` | `/en/blog/old-money-style-guide.html` | Old Money visual references and historical/social limitations; avoid presenting price or class as identity proof |
| `/blog/balletcore-la-gi.html` | `/en/blog/balletcore-style-guide.html` | Ballet-rehearsal clothing references; separate from ballet-flat garment guide, Angelcore and Coquette |

## Completeness and editorial review

- All 1,662 indexed text/alt segments are translated with source SHA256 locks. Full body, H1/H2/H3, tables, captions, FAQs, metadata and internal anchor text are covered. The rendered articles contain 19,663 English words, 181 headings, 51 original image placements, 13 tables and 46 FAQs. No empty or partial EN pages.
- Intent screening distinguishes Business Casual workplace requirements, Smart Casual occasion-dependent formality and Casual Chic everyday composition. Power Dressing addresses perceived presence rather than the Office Siren internet persona. Preppy remains broader than Ivy's garment-history specialist. Classic, Quiet Luxury and Old Money have separate wardrobe, construction-assessment and social-imagery purposes. Balletcore retains the aesthetic overview; ballet flats and leg warmers retain individual garment intent. Existing Goth/Grunge comparison and gothic graphic-tee originals remain distinct.
- All original images, source attributes/order and external reference URLs remain. The Look #29 camisole/jeans, Look #30 corset/cargo and Look #13 E-Girl examples are related proportion/palette references, not complete officewear, collegiate, Quiet Luxury or rehearsal uniforms. Image context does not establish dress-code permission or construction quality.
- Employer or host requirements take priority over generic labels. Traffic-light and five-level scales are editorial frameworks, not universal permission lists or an exact hierarchy. Appearance does not establish competence, authority, ancestry, wealth, education or personal worth. Body type and gender are not style eligibility requirements.
- Fiber names, price, restrained branding or an aesthetic label do not prove ventilation, comfort, grip, quality or durability. Actual weight, weave/knit, finish, lining, ease, care and conditions are distinguished. Brief movement checks and the five-year thought exercise do not prove performance or lifespan.
- Cost per wear is clearly hypothetical arithmetic: (purchase plus care cost) divided by actual or estimated wears. The VND examples are not current product prices or financial-return claims. No seller's stock, prices, terms or individual workplace policy is asserted.

## Verification sources and limits

- Four preserved Indeed career guides were read for general dress-code terminology. They are not primary evidence of a particular employer's policy. Outfit matrices and applications remain the site's own editorial interpretation.
- [FIT's 1980s timeline](https://fashionhistory.fitnyc.edu/1980-1989/), [Trend-ology](https://exhibitions.fitnyc.edu/trend-ology/) and [Power Mode](https://www.fitnyc.edu/museum/exhibitions/power-mode.php) support the limited historical tailoring discussion, interchangeable wardrobe context and the suit's relationship to authority and conformity. The preserved New-York Historical Society source returned 403 in retrieval; its full contents were not independently re-read, and it is not reported as a confirmed broken URL.
- [FIT Ivy Style](https://exhibitions.fitnyc.edu/exhibitions-timeline/ivy-style/) and [Exhibitionism](https://exhibitions.fitnyc.edu/exhibitionism/) support campus origins, mid-century codification, garment examples and circulation beyond universities. The two Vogue Preppy links provide fashion commentary and a personal essay; the Plum Sykes link is identified as an essay rather than misrepresented as a definitive historical chronology.
- The preserved Vogue Quiet Luxury reports are dated 2023; the GQ Old Money commentary is dated March 2025. They provide label context, not current trend popularity. UNIQLO's January 2026 page is a retailer interpretation; promotional quality or exact historical claims are not automatically adopted. Classic and Casual Chic are practical editorial frameworks, not claims to one formal historical taxonomy.
- Vogue's historical Balletcore discussion and dancer interviews were read alongside [FIT Ballerina exhibition material](https://www.fitnyc.edu/museum/exhibitions/ballerina.php). Ballet's fashion influence predates the internet label. The Who What Wear source is retained as commentary; no publication date is inferred solely from its URL. Fashion ballet flats or bodysuits are not represented as specialist training equipment.

## QA

- Ten VI sources match baseline bytes outside marked reciprocal hreflang and visible EN-link additions. All original VI URL/slug/title/meta/canonical/body/images remain; all 216 original VI sitemap URLs remain. Homepage/POD/Fourthwall/shop/routing/PR #9 untouched.
- All 31 manifest gates pass. HTML IDs, local targets/fragments, complete source/tag/image/reference parity, FAQ/schema, title/meta, self-canonical, reciprocal vi/en, sitemap and sequential unique Journal cards pass. All 161 EN pages have one H1, self-canonical and unique title/description/canonical values.
- All 56 distinct HTTP image endpoints returned 200/image MIME in the completed image checks. Twenty live desktop1440/mobile390 browser views have no body overflow; images fit their article widths and all 13 tables scroll in wrappers. The mobile Business Casual jeans FAQ opens with its full answer; the Old Money H1 and intro wrap within the viewport.
- Guarded maintenance promotes 47 links in 21 older EN pages, preserving each page's own VI links and guarding unrelated bodies, metadata and assets. These maintenance touches are not additional translations.
- No GSC query × page access: editorial intent screening only, no confirmed cannibalization diagnosis, deletion, consolidation, redirect or noindex changes.

Evidence: `docs/qa/en-batch32-*.json`. Complete source-locked translations: `data/en-translations/batch32.json` and ten TSV files. The release comparisons and checks below confirm publication.

## Release confirmation

PR #51 merged normally as `df422586825d1eaf9a7e0b7c3d86e3faf713332e` from reviewed head `f2576587c88c292fc4d5c088d2e705820ae70a30`; no check override. All 43 preview files and all 43 production files match byte-for-byte: ten new EN pages, ten VI pages, twenty-one maintained older EN pages, Journal and sitemap. All five production-master checks succeeded; actual branch checks are recorded separately in `docs/qa/en-batch32-release-checks.json`. Final guarded link scan finds zero eligible links and zero skipped pages. Tracker: 159 MERGED and 57 PENDING, plus two additional EN-only originals (161 Journal cards).

The initial production comparison observed HTTP 503 on the existing `en/blog/how-to-style-ballet-flats.html` page. One targeted retry matched the repository bytes. The production JSON retains the initial failure and retry result; the cause is not inferred.
