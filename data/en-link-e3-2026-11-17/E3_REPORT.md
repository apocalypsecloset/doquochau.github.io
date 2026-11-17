# E3: English links mirrored from the reviewed Vietnamese site

The user explicitly approved E3 after E1/E2 and the separate RULES/HUBS alignment. E3 changes 414 existing English pages. No VI HTML, old translation manifest/TSV, old release hash, title, meta, canonical, hreflang, image, original heading, TOC or FAQ changes in this phase.

## Current content and exact translation data

- 644 individually reviewed contextual links: 640 corresponding VI-to-EN relationships plus four routes for the two existing English-only originals. No article gains more than four contextual destinations. Each sentence was written literally against the existing EN paragraph and VI context; the replay script only inserts markup and exact spans.
- Unique contextual EN edges across the 425 articles increase from 1,933 to 2,577.
- 203 image-free navigation cards on nine parent pages, including the fabric and glasses guides. Every translated child in the reviewed parent classification has a card. Original navigation nodes and images remain intact. New card titles and descriptions reuse the existing target EN H1/meta; only the required CollectionPage ItemLists change in JSON-LD.
- 27 additional paragraph updates synchronize already-present links with the VI sentence/context without adding destinations. These include the five existing style collections and sources whose old locks would otherwise lack a corresponding EN text update.
- 416 supplemental TSV files under `data/en-translations/internal-links/` hold the actual VI context, English before/after spans and destination bindings. Historical root TSVs and all old `source_sha256` values remain unchanged. Current HTML can be reproduced exactly from the E2 baseline and these supplemental TSVs.
- Every contextual batch has at most 25 files and a before/after audit log. No batch increases any gate's diagnostic count.

## Successor recognition

`docs/link-fix-2026-11-17/en-e3-release.json` is additive. It pins the 414 EN predecessors/successors, all 416 updated TSV hashes, and exactly 210 VI source successors with their actual after-edit SHA-256 and unchanged historical source lock. A source successor is unavailable unless the paired changed EN HTML, corresponding updated TSVs and current VI source all have the pinned hashes. Unknown bytes retain their actual value and fail the historical contract.

`qa_en_link_fix.py` independently checks the actual current HTML before historical views are used. It proves exact TSV replay, 100% contextual target parity, live child-card coverage, real EN targets, metadata/image/original-heading/TOC/FAQ preservation and synchronized visible ItemLists. It runs before legacy gates in both CI jobs. Existing QA assertions are retained; the changes to existing helpers and qa_link_fix only recognize these exact successors.

## Validation

- Independent E3 QA: PASS, including 423 paired articles, 644 contextual additions, 203 cards, 27 existing-link sentence updates and all 210 conditional source successors.
- VI audit: PASS, all eleven gates.
- Node: 19/19 PASS, zero skipped.
- EN audit: E1–E8, E10 and E14 PASS. E3 requirements have 100% contextual parity, incoming links, sibling links and full parent/child navigation coverage.
- Remaining E4 diagnostics: E9 31 entries; E11 90 duplicate pairs; E12 51 repeated-anchor groups; E13 one pre-existing dense article. No assertion or threshold was changed to hide them. The existing dense article gains no new contextual destination in E3.
- Browser evidence: nine changed navigation pages at 1280px and 390px, 18 rendered views with no horizontal overflow and the expected added-card counts. Screenshots and metrics are in `browser/`. New cards contain no images; no claim about re-auditing all original remote image availability is made.
- Full clean GitHub CI verification is recorded separately after this content commit. Do not interpret the interrupted local aggregate run as final CI: its consent scan encountered HTML from an isolated Chrome test profile. That profile was moved outside the repository; QA rules were not changed. Standalone E3, VI and Node results above are complete.

`twenty_vi_en_examples.json` supplies twenty reproducible randomly selected VI-to-EN examples. The literal prose files, batch ledgers and supplemental TSVs retain the complete editorial/replay trail. Navigation-card counts are separate from the four-link contextual budget; the parent guides' new cards are navigation, matching E3's full child coverage requirement.

## Clean CI result after the content commit

Content commit `59bf0e34903667bb233882195ffe007210886501` passes both Website quality jobs in [run 44110748229](https://github.com/apocalypsecloset/doquochau.github.io/actions/runs/44110748229): static-and-shop and english-translations. All 38 translation batches execute successfully; the log reports `FAILED EN BATCHES: 0`. The independent current-HTML/TSV proof succeeds before historical checks in both jobs. VI exact replay, all seven general QA scripts, batch40 and the nineteen Node tests also pass. See `CI_REPORT.json` for the job and step results.

Cloudflare Pages reports a successful preview build. Workers Builds reports failure, also present at the E2 content commit; that external deployment configuration is outside E3. Automated HTTP byte verification of twelve preview pages was denied with HTTP 403, so this report makes no deployed-byte equality claim. The eighteen local Chrome views and their metrics are complete.

E3 is complete. E4/E5 and merge remain outside this approval.
