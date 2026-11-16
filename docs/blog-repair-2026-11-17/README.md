# Bilingual blog repair — 17 November 2026

Base: `7465236e399e127d785f6579cc839c10d2f74ecc`.

- Promote 571 in-article VI links to existing EN counterparts across 93 EN articles. Preserve explicit original-language switches, anchor text, query strings and fragments.
- Consolidate both Capsule Wardrobe FAQs into one visible section, retaining all three answers, the illustration, existing section anchors and exact FAQ schema content.
- Remove 1,554 redundant plain caption instances across 438 articles, retaining the first occurrence and all unique/link captions. All image attributes, files and reviewed alt text remain unchanged. No new visual claims are invented.
- Move the app link below the title and apply a compact, responsive secondary CTA on 232 EN articles. Preserve destination, Vietnamese label and click tracking.
- Preserve every URL, canonical, title, H1, meta tag, hreflang and script.

456 HTML pages change (overlapping issue groups). The release manifest hashes both the baseline and approved result. Historical migration tests recognize only those exact approved successors; unknown bytes still fail. `qa_blog_repair.py` independently inspects actual current HTML for all 874 published URLs and verifies each edit against a deterministic repair of the Git baseline. Older translation gates retain their original source locks and inspect their historical content contract; this new gate verifies the authorized current successor.

Validation: new 874-page gate; existing static, schema/image, privacy, storefront, audit and R2 gates; all 37 translation batches; 19 Node behavior tests. Browser preview checks cover EN Oxford desktop/mobile (390 px) and Capsule FAQ. HTTP status and external asset crawling across every URL remain outside this repair's verified scope.
