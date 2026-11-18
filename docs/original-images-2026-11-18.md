# Restore original blog image URLs — 18 November 2026

At the owner's request, remove the generated assets/images/blog-responsive variants and use the original image URLs again across both languages. All 2,283 original URLs are mapped from the pinned audited image manifest; no filename guessing is used. All 6,623 affected image occurrences and 10 picture sources point to the same original image identities. Existing thumbnails, alt text, dimensions, loading priorities and other image improvements remain. The original full-size image can cost more bandwidth than the removed small versions.

Remove obsolete srcset/sizes on affected img elements. Picture sources use the matching single original URL. The 4,942 retired files are verified by SHA-256 and pinned Git blob before removal. Their removal reduces the current working/deployment tree by roughly 306 MiB; it does not rewrite Git history, so old commits still retain their blobs.

All titles, descriptions, social text, schema, article text, headings, links, canonical/hreflang and sitemap are preserved byte for byte. Social image URLs that used generated variants are restored to originals with matching original dimensions. Current QA verifies real original URLs, thumbnail identity and exact non-image preservation. Historical metadata, image, editorial and cleanup contracts only normalize exact known successors; they reject unreviewed bytes. Old manifests remain immutable historical records, not deployment dependencies.

Baseline: 8c3e9f88b9efa24e4bc5f1b4e9b445a1e5b20a86. The new release manifest records every edited text file, added audit file and retired image. The earlier title/description work remains active.
