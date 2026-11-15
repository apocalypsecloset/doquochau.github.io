# Newest-first journal order

Both journal grids previously appended the 218 newly published articles after the existing archive. Sort by the publication date already shown in Vietnamese cards, keeping same-date cards in their existing order. English counterparts follow the same recorded dates; English-only articles use their BlogPosting publication date. Undated collection hubs remain at the end without inventing dates.

The 218 articles dated 2026-11-15 now precede the older archive in both languages. Existing card content, images, filters, search, load more, URLs, metadata and article pages are preserved. English numbering follows the new order.

`scripts/journal_order.py --write` applies this order; its read-only check is included in the site gate. The journal interaction test asserts descending dates and the new first article. Validation also compares every card to its original content while allowing only order, publication data attributes and English sequence numbers to change.
