# E15: EN navigation to existing English counterparts

Baseline: merged `1dd10834efa9aaef5cff197cd2ff298172bbc9a4`. The supplied `internal_link_audit_en (2).py` is archived as `supplied_audit_en.py`. Its exact E15 gate is added to the active audit, retaining the previously approved VI-aligned RULES/HUBS. The other fourteen gates and thresholds are unchanged.

## Results

- Scan: all 450 English HTML pages, including 442 English articles/collections, with anchors in every page region.
- Before: E15 has one violation. After: E15 PASS, zero violations; all 15 EN gates PASS. VI still passes all 11 gates. Complete outputs: `audit_en_after.txt` and `audit_vi_after.txt`.
- One URL promoted: `en/blog/vay-lien-than-chu-a.html`, `/blog/phoi-do-voi-chan-vay-chu-a.html` → `/en/blog/how-to-style-a-line-skirts.html`, with `hreflang="en"`.
- Keep the context-specific anchor “styling an A-line skirt”; it already accurately describes the destination in natural English.
- Eight existing exception links get the missing `(Vietnamese)` label: six Outfit Builder links and two links to the women's alternative outfit guide. Their VI URLs and surrounding sentences remain unchanged.
- Total changed anchor occurrences: **9** across **9 pages**: **1 destination changed**, **8 language labels added**. No untranslated prose links needed removal.
- Original-language switches and links to each page's own VI original remain intact. Existing labelled `/outfits/`, `/style/`, `phoi-do-nu-ca-tinh` and `app-phoi-do` exceptions retain their destinations.

## Preservation

Nine new paragraph-level TSVs record exact before/after HTML under `data/en-translations/internal-links/e15/`. None of these paragraphs or labels occurs in the affected pages' JSON-LD, FAQ or ItemList; no schema change is required. All JSON-LD stays byte-equivalent, valid and consistent with visible FAQ content.

`en-e15-release.json` is additive: every old hash, manifest and translation TSV remains untouched. It pins the nine HTML files, nine TSVs and their VI sources. The legacy E4/E3 checks recognize only those exact successors. E4 now also requires all 15 current audit gates, adding the requested E15 without removing an old check.

The independent `qa_en_link_e15.py` checks current HTML, exact full-file TSV replay, real paired targets, preserved metadata/images/headings/TOC/FAQ/JSON-LD, original-language links and the complete 450-page link inventory. It runs before historical QA in both CI jobs. Local E15 and E4 proofs pass; CI checks the full historical translation contracts as well.

The inventory and patch ledger provide every affected source and anchor. This branch has not been merged.
