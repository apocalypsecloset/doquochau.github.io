# Batch40 — Four complete English collections (E2)

E1 checkpoint: `61515ae9`. E0b/VI release manifests remain unchanged. This batch creates four sources and four English pages; it does not refresh any of the 210 changed historical translation sources.

| VI source | EN page | Authored English words excluding cards | Child cards |
|---|---|---:|---:|
| `phoi-mau-quan-ao-nu` | `womens-color-coordination-guides` | 1,540 | 41 |
| `chon-trang-phuc-nu-theo-dia-diem-va-dip` | `occasion-destination-outfit-guides` | 1,486 | 23 |
| `cach-cham-soc-do-nu` | `womens-clothing-care-guides` | 1,654 | 11 |
| `chon-toc-va-makeup-theo-trang-phuc` | `alternative-hair-makeup-guides` | 1,583 | 9 |

## Content and intent

Color coordination teaches shade, contrast, surface and proportion before routing to individual color and garment questions. Occasion/destination guidance starts with activity, weather, travel and venue requirements. Care guidance separates washing, storage, fit and construction while deferring to the actual product label. Hair/makeup guidance coordinates neckline, volume, color and daily activities without treating an inspiration photograph as a guaranteed result.

The four sources contain 347 unique translatable segments. The English TSVs cover every segment. Narrative sentences were adapted individually; existing English child metadata and reviewed image descriptions were reused where appropriate. Proper names such as Da Lat, Ba Na, Tet and ao dai use English-friendly spellings in these new pages, leaving all existing English metadata untouched. No health, weather, venue-policy or product-performance fact was invented.

Source order, original image attributes, headings, TOC, tables and source links are retained. The four VI bodies are byte-identical to E1. With explicit user approval, only a marked pair of self-VI/EN alternates was inserted in each VI head; no visible language button or other body markup was added.

## Exact full-directory successor

The VI sources have 37/18/6/1 cards, with several other children already linked in prose. E2 requires a card for every translated child. These new English pages therefore add exactly 4/5/5/8 text cards, yielding 41/23/11/9. Original source images are retained; no extra image is fabricated for these cards.

`docs/link-fix-2026-11-17/batch40-release.json` adds a separate E2 manifest. It pins the full current pages, four head-only VI successors, Journal, sitemap, new TSVs and batch40 configuration. It neither replaces the E0b manifest nor adds a historical translation-source successor.

The existing hub gate receives an exact, fully translated source-parity snapshot only for these four pinned full-directory successors. This keeps every original parity assertion enabled. **`qa_batch40.py` checks the actual pages independently**: complete child coverage, current ItemList count/names/order/URLs, English text, authored word counts, full TSV coverage and exact correspondence to the source-parity DOM except for the declared card sections and ItemList. Unknown bytes, changed metadata or undeclared additions do not receive normalization. The unsuccessful first candidate and its original data remain as draft evidence; it was never accepted as a release.

No such normalization is inserted into `en_translate.source` or `en_translate_hubs.source`. All old manifests, TSVs, English articles and source hashes remain unchanged. The old 215 entries must still show 210 unreleased source mismatches. Batch40 has four brand-new, fully translated source locks of its own.

## Publication and strict Journal contract

The English Journal retains all 438 original card fields except their shifted ordinals and adds exactly four cards dated 17 November 2026, for exactly 442. The Node test verifies the exact successor file hash and still uses equality for counts, uniqueness, ordering, pagination and search. Publication/date helpers recognize the four explicit new pairs without changing the original 216-row tracker, 218-pair inventory or 220-publication inventory.

Four EN URLs are registered in the sitemap with the actual release date and reciprocal language tags. `search-index.js` remains unchanged: its 371 entries are VI-only; English discovery/search is driven by the English Journal cards, which now include these four collections.

## Validation and remaining work

- `qa_batch40.py`, `qa_en_hubs.py batch40`, `qa_en_translations.py batch40` and the 19 Node tests pass in the initial E2 checks.
- VI audit remains all PASS. EN audit still has nine failed gates; E7/E8 remain PASS. EN has 425 articles + 17 collections and 440 paired VI sources.
- Old EN article text is deliberately unchanged before E3. E3 incoming-link failures fall from 211 to 199. E6 measures 172 failures rather than 126 because four newly translated parent targets now enter its parity denominator. E4 reports 23 diagnostic entries; missing child-to-parent links and the EN audit's 15 pre-existing cluster differences remain visible. None of these counts was hidden by weakening a gate.
- The full existing QA suite and all 38 translation batches are run again. The intended state before E3 is 36 historical batches still failing, with batch19 and new batch40 passing. Exact command outputs are retained in `data/en-batch40-2026-11-17/`.

**Stop after E2. Do not start E3 or merge the review branch without the user's next instruction.**
