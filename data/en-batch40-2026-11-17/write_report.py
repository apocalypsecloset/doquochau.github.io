"""Produce the E2 checkpoint after the complete CI-equivalent local run."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
rows=json.loads((D/'qa_results.json').read_text(encoding='utf-8'))
assert len(rows)==51
general=[r for r in rows if not r['name'].startswith(('translations_','hubs_'))]
translations=[r for r in rows if r['name'].startswith('translations_')]
assert len(general)==10 and all(r['exit_code']==0 for r in general)
assert len(translations)==38
failed=[r['name'].removeprefix('translations_') for r in translations if r['exit_code']]
assert len(failed)==36
assert {r['name'] for r in translations if r['exit_code']==0}=={'translations_batch19','translations_batch40'}
batch=json.loads((D/'qa_batch40.json').read_text(encoding='utf-8'))
assert not batch['errors']
node=(D/'node_tests.txt').read_text(encoding='utf-8');assert 'pass 19' in node and 'fail 0' in node
report='''# E1–E2 checkpoint — stop before E3

E1 commit: `61515ae9`. E0b manifests and all old EN source locks remain unchanged.

## E1

- Active audits: `scripts/internal_link_audit.py` and `scripts/internal_link_audit_en.py`.
- VI and EN task documents are in `docs/`.
- Historical tools and `link_changes.csv` moved to `data/link-fix-2026-11-17/`; `tools/` removed. Frozen patch/log bytes are preserved. Local libraries moved to ignored `.venv/site-packages`.
- No `/tools/*` header rule was added. No HTML changed during E1. VI audit and exact successor QA passed before the E1 commit.

## E2: four complete English collections

| English slug | Authored words excluding cards | Child cards | TSV segments |
|---|---:|---:|---:|
'''
for r in batch['results']:report+=f"| `{r['en_slug']}` | {r['authored_words']} | {r['child_cards']} | {r['tsv_segments']} |\n"
report+='''
Each source is fully adapted in batch40 and its TSV. Every already-translated child has a card with a real EN URL and `hreflang=en`. Current CollectionPage/ItemList/BreadcrumbList metadata matches the visible page. The full-content successor is independently checked against the translated source-parity DOM, including exactly 22 added text cards. The original 62 source cards/images remain intact.

The only VI edits in E2 are the explicitly approved, marked self-VI/EN alternate tags in the heads of the four new hubs. Every other byte, including their bodies, remains unchanged. No existing EN article, historical hub, TSV or translation manifest was rewritten. No historical `source_sha256` is accepted early; 210 of the old 215 source locks still reject the changed VI sources.

The English Journal has exactly 442 cards: 438 originals with only their ordinals shifted, plus four dated collection cards. All original titles, descriptions, links, dates and search content remain. Sitemap registration and publication-date/catalog helpers include the four explicit new pairs. The VI-only `search-index.js` is unchanged; the EN Journal's actual search/pagination is tested with the real 442-card DOM.

## Completed validation

'''
for r in general:report+=f"- `{r['name']}`: PASS (exit 0).\n"
report+='''- `qa_en_hubs batch40` and `qa_en_translations batch40`: PASS.
- Node: 19/19 PASS, none skipped.
- All 38 translation batches executed: batch19 and batch40 PASS; the same 36 historical batches remain FAIL before E3. No continue-on-error or successful replacement of those failures.
- Existing `docs/qa/*`, reviewed manifests, old source hashes and the 216/218/220 inventory contracts remain unchanged.

## EN audit remains a baseline for E3

The site now has 425 English articles plus 17 collections, with 440 VI/EN pairings. There are still nine failed EN gates. E7/E8 stay PASS. Incoming-link failures fall from 211 to 199. E6 failures rise from 126 to 172 because the four newly translated parent targets now count toward parity; old article text has not been changed to link up to them. E4 reports 23 diagnostic entries. The 15 previously reported classification differences and missing Outfit-core declaration in the supplied EN audit remain disclosed rather than silently changed.

## Scope and evidence

`docs/en-translation-batch40.md` explains intent, rendering and exact successor recognition. `docs/link-fix-2026-11-17/batch40-release.json` is additive; it does not replace earlier hash records. `qa_batch40.json` inspects the current full directories, while the source-parity gate retains its original assertions. `qa_results.json` and each stdout/stderr file retain all 51 command results, including the unresolved historical batch failures.

Remote CI and browser preview results are reported separately in the PR/chat after the branch is pushed. This local report does not claim an unobserved production deployment or merge.

**E1 and E2 complete. E3 has not started and requires the user's next explicit approval.**
'''
(D/'E2_REPORT.md').write_text(report,encoding='utf-8')
print('E2 report: 10 general checks PASS, 19 Node PASS, 36/38 translation batches still FAIL.')
