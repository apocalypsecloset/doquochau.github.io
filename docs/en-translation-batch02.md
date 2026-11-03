# English translation batch 02 — 2026-11-03

Baseline master: `14189d9d0eb4a75b53efa2f7586b3e0d6c2e51f3` (PR #10 merged).

## Progress
- 216 Vietnamese sitemap blog URLs remain present.
- 2 prior translations already merged: Corporate Goth and Soft Goth.
- This batch adds 10 complete translations; **12/216 complete, 204 still pending**.
- Existing 2 English originals are separate: 14 English articles after this batch reaches master.
- A complete translation is not a claim of Google indexing or confirmed search performance.

## Mappings and unique primary intent
| Vietnamese source | English counterpart | Role / intent |
|---|---|---|
| `/blog/grunge-la-gi-khac-gi-punk.html` | `/en/blog/what-is-grunge-style-vs-punk.html` | DEFINITION_COMPARISON: Grunge definition and distinction from punk; not Goth vs Grunge or an outfit formula guide |
| `/blog/soft-grunge-aesthetic-la-gi.html` | `/en/blog/soft-grunge-wardrobe-outfits.html` | SUBSTYLE_GUIDE: Tumblr soft grunge wardrobe and soft-rough outfit balance |
| `/blog/phoi-do-grunge-nu.html` | `/en/blog/grunge-outfits-women-layering.html` | OUTFIT_GUIDE: Practical women's grunge outfit construction; not grunge definition or Gothic graphic tee styling |
| `/blog/phoi-do-voi-ao-thun-nu.html` | `/en/blog/alternative-t-shirt-outfits-women.html` | ITEM_GUIDE: General women's T-shirt types across alternative styles; gothic graphic print styling remains the existing specialist URL |
| `/blog/witch-aesthetic-whimsigoth-la-gi.html` | `/en/blog/witch-aesthetic-vs-whimsigoth.html` | SUBSTYLE_COMPARISON: Witch umbrella vs 1990s mystical bohemian Whimsigoth distinction |
| `/blog/goth-aesthetic-huong-dan-day-du.html` | `/en/blog/what-is-goth-style.html` | PILLAR: Goth fashion definition and pillar; future goth hub is navigation only, existing goth vs grunge owns cross-aesthetic comparison |
| `/blog/fairy-grunge-la-gi.html` | `/en/blog/fairy-grunge-style-outfits.html` | HYBRID_STYLE_GUIDE: Fairycore-grunge hybrid with organic textures and earthy movement; distinct from soft grunge Tumblr |
| `/blog/romantic-goth-la-gi.html` | `/en/blog/romantic-goth-style-guide.html` | SUBSTYLE_GUIDE: Ornate dark romance and historical-looking texture, unlike low-intensity soft goth |
| `/blog/trad-goth-la-gi-traditional-goth-style.html` | `/en/blog/trad-goth-hair-makeup-outfits.html` | SUBSTYLE_GUIDE: First-wave post-punk/deathrock fashion lineage and hair/makeup; not general goth pillar |
| `/blog/nu-metal-aesthetic-la-gi.html` | `/en/blog/nu-metal-fashion-outfits.html` | SUBSTYLE_GUIDE: Nu metal late-1990s/2000s sports-skate-rock silhouette; distinct from worn-in grunge |

## QA evidence
- `qa/en-batch02-static.json`: source text hash, complete source section/table/FAQ/caption/image counts, English text, H1, title, meta, schema, internal targets and anchors.
- 19,818 English words, 71 editorial images including covers and original look references, 15 tables, 47 FAQ answers. All original external references retained.
- `qa/en-batch02-images.json`: 83 distinct original/responsive image URLs checked with curl HEAD: all HTTP 200 and image content types. Python urllib was rejected at the transport level; its failed checks are not represented as site image failures.
- `qa/en-batch02-responsive.json`: all ten articles rendered at desktop 1440 and mobile 390 iframe widths; no horizontal overflow after fixing two legacy inline-image widths in an English-only stylesheet. Mobile table stays within a 341px container with 650px content scrolling internally. TOC and FAQ interactions verified.
- Vietnamese source text, title, meta, canonical, images and markup remain byte-for-byte identical after removing the two explicitly marked additions (EN alternate link and visible language switch). No other VI article changes.
- All 216 VI sitemap URLs retained; only 10 completed EN URLs added. Journal contains only completed EN articles.
- Source Whimsigoth had reverse-ordered inserted formula paragraphs and misplaced section headings. The English order is repaired without dropping any heading or paragraph; VI is preserved.
- Broad stylistic absolutes and illustrative unmeasured percentages in source copy were edited into qualified styling guidance in EN.

## SEO review limits
No connected GSC query × page dataset was available. These are editorial intent distinctions, not a confirmed cannibalization diagnosis. Existing risk hints remain unconfirmed; no VI URL was deleted, merged, redirected or noindexed. All pairs self-canonicalize and have reciprocal vi/en alternates. Source internal links point to completed EN equivalents where available; untranslated targets retain working VI references labelled Vietnamese. References and original images are retained, not recreated.

## Reproduction
Install `scripts/requirements-en.txt`, then run:

```sh
python scripts/en_translate.py generate
python scripts/qa_en_translations.py
```

`data/en-translations/*.tsv` contains reviewed full text-segment translations; the manifest locks each source's SHA-256. Generation stops if the source changes or a Vietnamese segment is missing. No fallback English stubs are emitted. `scripts/sync_en_batch.py` wires the completed batch into alternates, sitemap and Journal; it is not a translator and must not be used to label untranslated articles complete.

## Remaining work
204 complete source translations and per-batch QA remain. Prioritize Nu Goth, Vampire Goth, subtype comparisons, Emo, Dark Academia, dark-feminine outfits, mesh/oversized tops and the Goth/Punk navigation hubs next. Hubs must remain navigation hubs rather than competing definition articles. Then proceed through the remaining inventory in batches of 10–20. Do not interpret this batch report as completion of all 216 articles.

## GitHub publication checks — PR #11
- Commit `abe2874dae684615eb45e8400ceda09546002448`: Cloudflare Pages **success**; deployed preview `https://458a889d.doquochau-github-io.pages.dev`.
- `qa/en-batch02-preview-deployment.json`: all 10 deployed preview HTML responses match the QA-validated local files byte-for-byte.
- Separate `Workers Builds: doquochau-github-io` check **failure**. The same named check also failed on the baseline master commit `14189d9`; this is not a newly introduced check failure from the article changes. Its GitHub output provides no diagnostic annotations; the Cloudflare build log requires separate dashboard access. No Worker, routing, shop or Fourthwall files were changed to address it.
- Do not describe the full check suite as all green. The actual Pages deployment and the source/content QA above are distinct from the existing Worker-build issue.
