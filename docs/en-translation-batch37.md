# English translation batch37 — 2026-11-05

Status: COMPLETE_LOCAL_QA; production verification pending. Baseline master: `9c24d990b5e6183b69bd8ed908557897bc6b5ed9`.

Ten complete translations: three collection hubs plus Gyaru, Harajuku, Ganguro, Kogal, Amekaji, Heisei Retro and Hime Gyaru. The remaining seven historical/global guides form the next final batch. This split keeps this release within the requested 10–20-page batch size and its linked Japanese-fashion context together.

All 1,735 indexed source text/alt/attribute segments translated; 17,901 English words, 294 H2/H3 headings and 157 original image placements. Three hubs retain all 110 cards, complete explanatory sections and galleries. Five tables total (four article comparisons plus shopping-hub table); 28 article FAQ pairs, with matching visible/schema answers. Hub galleries are not FAQ schema. Original images and external references retained.

## Intent and editorial decisions

The CSV and guardrails were read on master before translation. No GSC query × page tool is available. Intent review is editorial; no confirmed cannibalization diagnosis, URL deletion, merge, redirect or noindex. Existing four original/initial EN guides remain distinct. Full source-locked scope decisions: `data/en-intent-plans/batch37.json`.

Shopping hub routes size, material, budget, seller and care questions to their specialists. Aesthetic Dictionary is a lookup/navigation directory, distinct from the aesthetic-definition article. Accessories hub is a selection framework and directory, distinct from individual accessories. Gyaru is the overview; Ganguro covers historical high-contrast styling, Kogal uniform customization, Amekaji casual Americana and Hime Gyaru princess finishing. Harajuku is a place-based ecosystem, separate from the pending Japanese Streetwear specialist. Heisei Retro is a nostalgia umbrella, separate from Y2K futurism and specific subcultures. Local illustrative VND budgets are not current prices or product availability guarantees; optional material/comfort checks avoid quality guarantees.

Kogal uses adult outfit interpretations and preserves historical context without sexualizing minors. Amekaji and Hime Gyaru proportions remain optional styling choices rather than body requirements. UV tanning is not prescribed; Ganguro safety context follows WHO. Historical garment terms and source lettering remain intact in retained images, with English alt/captions.

## Reference checks

Checked original primary/institutional URLs through public retrieval on 2026-11-05:

- GO TOKYO SHIBUYA109: https://www.gotokyo.org/en/spot/66/index.html — Gyaru/Shibuya setting.
- GO TOKYO Harajuku: https://www.gotokyo.org/en/destinations/western-tokyo/harajuku/ and JNTO: https://www.japan.travel/en/spot/2174/ — place-based diversity.
- V&A: https://www.vam.ac.uk/articles/lolita-fashion-japanese-street-style and FIT: https://www.fitnyc.edu/museum/exhibitions/japan-fashion-now.php — independent subculture context.
- Web Japan's April–June 1997 archive: https://web-japan.org/kidsweb/archives/cool/97-4-6/fashion.html — contemporary documentation of loose socks and uniform customization.
- WHO: https://www.who.int/news-room/fact-sheets/detail/ultraviolet-radiation — avoiding artificial tanning and UV-related skin/eye harm; verified with primary search.
- KCI article ART002823024: https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002823024 — broader Amekaji/workwear meaning, not proof of every Gyaru styling convention.
- NDL/Hiroshima record: https://ndlsearch.ndl.go.jp/en/books/R000000025-I013720006675071 — academic bibliographic context; no claim of full dissertation review.
- Nippon Information: https://www.n-info.co.jp/report/report-0093/ — April 24, 2026 release, 90.1% awareness and 47.3% purchase/interest in its survey; figures remain dated and sample-specific, not a current or universal trend claim.

Original secondary/community references remain attributed, including Fa-So-La's egg retrospective and Gyaru Online's Hime overview, both retrieved. Their conventions are not presented as universal authoritative dress rules. All original links remain; no invented historical eyewitness, clinician or survey author attribution.

## QA and scope

Mixed manifest dispatcher runs BOTH complete article and hub gates and verifies exact source coverage; no gate weakened or source kind skipped. Hub byte-preservation regex now handles every marked batch, rather than only batch24. Hub schema date uses configured publication date with prior default retained.

All 35 manifest release gates pass, including the new mixed gate and 34 historical manifests. All 216 VI sitemap URLs retained; ten VI sources byte-identical outside marked language links. All 211 EN pages have one H1, unique title/description/canonical and self-canonical. Reciprocal vi/en, sitemap and 211 ordered English Journal cards pass. All 171 distinct image/srcset/logo endpoints return HTTP200/image MIME. All 20 desktop1440/mobile390 browser views have no document overflow; covers load and tables scroll inside wrappers. Responsive evidence: `docs/qa/en-batch37-responsive.json`.

Guarded maintenance promotes 224 existing links in 104 older EN pages to the newly available equivalents. These are maintenance touches, not extra translations. Final scan: zero eligible links and zero skipped pages. No homepage/POD/Fourthwall/shop/routing/PR9 changes. No EN stubs for seven remaining sources.

## English URLs in this batch

- https://apocalypsecloset.com/en/blog/alternative-fashion-shopping-guides.html
- https://apocalypsecloset.com/en/blog/fashion-aesthetic-directory.html
- https://apocalypsecloset.com/en/blog/alternative-accessories-guide-directory.html
- https://apocalypsecloset.com/en/blog/gyaru-style-guide.html
- https://apocalypsecloset.com/en/blog/harajuku-fashion-style-guide.html
- https://apocalypsecloset.com/en/blog/ganguro-gyaru-fashion-makeup.html
- https://apocalypsecloset.com/en/blog/kogal-gyaru-style-history.html
- https://apocalypsecloset.com/en/blog/amekaji-gyaru-american-casual.html
- https://apocalypsecloset.com/en/blog/heisei-retro-fashion-nostalgia.html
- https://apocalypsecloset.com/en/blog/hime-gyaru-princess-style.html

## Release confirmation

Pending normal PR merge and exact preview/production byte verification. CSV remains TRANSLATED_QA_PENDING until production proof.
