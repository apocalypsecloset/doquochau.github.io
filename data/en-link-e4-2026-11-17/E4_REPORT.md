# E4 — English link cleanup

Authorized by the user's “tiếp E4”. Baseline: `9880f3f07c1b8898590cdd2afa3f323c497e4def`. PR #80 remains a draft; no merge performed.

## Changes

- 187 English HTML files, with 215 new supplemental TSVs in `data/en-translations/internal-links/e4/`.
- Removed 99 redundant link wrappers and one excess contextual destination, preserving the corresponding text. The densest article now has 12 contextual destinations.
- Reworded 25 paragraphs to remove publishing terminology, renamed 176 anchors, and added three relevant contextual links. Every newly authored anchor has 2–6 words. Each article stays within four new contextual destinations cumulatively across E3 and E4.
- Every one of the 442 English destinations has at least three distinct incoming anchor labels across `en/blog/`, using the same whole-page counting scope as the VI phase-four verification. This includes existing navigation and related modules; it is not a claim that each destination has three different prose anchors.
- Kept all contextual VI-to-EN relationships: parity remains 100%. Original-language switches remain intact.
- Unique contextual outgoing destinations summed across the 425 English articles: 1,933 before E3, 2,577 after E3, and 2,578 after E4. Of the three E4 additions, two point to articles and one to an English directory; removing one excess article destination produces the net increase of one article edge.

## Integrity and validation

Both unchanged audits pass: EN 14/14 gates and VI 11/11 gates. `qa_en_link_e4.py` independently validates actual current HTML, exact TSV replay, real targets, cumulative budgets, metadata, images, headings, TOC, FAQ and the 442-page inventory. The E3 predecessor proof also passes.

The additive `en-e4-release.json` pins each changed HTML and TSV to its exact SHA256. All historical manifests, source hashes and TSVs remain unchanged. Existing QA changes only recognize these exact successors; thresholds and assertions remain intact. CI executes the actual E4 proof before checking historical predecessors.

Headless Chrome checked four representative articles at 1280px and 390px: eight rendered views passed language, anchor presence and horizontal-overflow checks. Screenshots and measurements are in `browser/`. Two screenshots were visually reviewed. Existing image assets were not changed; the local T-shirt screenshot includes an unavailable pre-existing image, so this is not an image-delivery certification.

The four new English collections and the 20 VI/EN sentence examples are recorded in the E2/E3 reports. No slug migration or additional phase was introduced.

## Remote CI

Content commit `cc6069c3a2da57afff244d4379c48f1c87a1b3a8`: [Website quality run 44119574777](https://github.com/apocalypsecloset/doquochau.github.io/actions/runs/44119574777) passes both `static-and-shop` and `english-translations`. All 38 translation batches pass (zero failures), as do all 19 Node tests and every general QA step. Exact step results are recorded in `CI_REPORT.json`. Cloudflare Pages succeeds; Workers Builds remains failed, as already observed at E2/E3. No merge performed.
