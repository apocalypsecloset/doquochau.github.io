# Apocalypse Closet — Blog VI → EN migration inventory

## Scope confirmed from the live-source sitemap in the repository
- Vietnamese /blog/*.html URLs: **216** (sitemap entries, not proof every article is indexable).
- Existing new /en/blog/*.html articles: **2**; these are new original editorials, not automatically paired translations.
- Maintain all existing Vietnamese URLs, slugs, canonicals, SEO titles, image URLs and content unless each page requires separately approved repair.
- Add an individual English page at /en/blog/<english-search-intent-slug>.html only after translation and QA. Do **not** simply relocate Vietnamese files.
- Both versions should have self-referencing canonical and reciprocal hreflang (en, vi), but **only** once the English translation is real and published.
- Internal links should prefer same-language destinations; the POD store / remains English.
- Do not translate the Vietnamese home, blog card snippets, or affiliate CTA mechanically into English without rewriting search intent and product relevance.

## Translation pipeline
1. Read and classify each existing article: original intent, current Google Search Console performance, commercial relevance to Gothic/Grunge POD, language quality and image availability.
2. Priority batch: 10–20 articles from the highest SEO relevance and existing clicks; collect actual GSC queries before choosing the batch. Prioritize Gothic/Grunge/graphic tee outfits over generic fashion topics.
3. Draft full English translations, preserve the original facts and any useful diagrams/images, localize examples, units and links for international shoppers.
4. QA full English body, heading hierarchy, image alt, schema and references (no leftover Vietnamese-only metadata or affiliate links).
5. Create English file and link from /en/blog.html, add reciprocal hreflang to corresponding Vietnamese article, add sitemap entry for EN URL.
6. Review performance and indexing after each batch; then continue until all eligible articles are translated. Some heavily local/affiliate pieces may need adaptation instead of literal translation.

## Scope and completion
This inventory contains 216 unstarted translation records. Nothing here creates public EN article pages until translated and reviewed. Use the CSV as a source-of-truth, replacing PENDING_GSC with actual performance metrics where available.

Existing EN originals:
- https://apocalypsecloset.com/en/blog/how-to-style-gothic-graphic-tees.html
- https://apocalypsecloset.com/en/blog/goth-vs-grunge-style.html
