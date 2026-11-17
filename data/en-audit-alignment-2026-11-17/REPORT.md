# Approved EN audit classification alignment

Baseline: `a0272175089f56498bfecc40961a21baeb46fcf2` (E2). The user explicitly approved synchronizing RULES/HUBS with VI while retaining all fourteen gates and thresholds.

The EN audit now imports the reviewed VI classification function and copies its RULES/HUBS, including the missing Outfit-core parent. Across all 440 VI/EN pairs, classification mismatches are zero. This changes fifteen article classifications and the classifications of the four new collection pages. `verification.json` records every changed classification.

All gate code and thresholds, starting at MODULES through the end of the script, are byte-identical to the E2 baseline. All functions except cluster have identical ASTs. No other QA script, HTML, translation TSV, manifest or historical hash was changed for this alignment.

| Gate | Before diagnostic count | After diagnostic count |
|---|---:|---:|
| E1 | 0 | 0 |
| E2 | 9 | 9 |
| E3 | 199 | 199 |
| E4 | 23 | 21 |
| E5 | 171 | 162 |
| E6 | 172 | 172 |
| E7 | 0 | 0 |
| E8 | 0 | 0 |
| E9 | 35 | 35 |
| E10 | 0 | 0 |
| E11 | 90 | 90 |
| E12 | 52 | 52 |
| E13 | 1 | 1 |
| E14 | 0 | 0 |

Both EN audits exit 1 with nine failing gates. The changed E4/E5 counts reflect corrected grouping and the newly declared parent, not repaired website links. The VI audit exits 0 with all eleven gates passing. The UTF-8 logs and the current EN page CSV are saved alongside this report.

E1/E2 remain complete. E3 website edits and source-successor release remain pending the user's explicit E3 approval, as requested. Uncommitted editorial planning in `data/en-link-e3-2026-11-17/` has not been applied to the website or translation data and is excluded from this alignment commit.
