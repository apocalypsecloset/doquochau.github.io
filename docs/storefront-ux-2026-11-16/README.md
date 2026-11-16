# Storefront UX maintenance — 2026-11-16

Authorized scope: apply the Wicked Clothes comparison recommendations to the existing Apocalypse Closet storefront, retaining its dark/red identity and existing SEO fields, article bodies, URLs, genuine product photographs and Fourthwall checkout.

Implemented in the main website: readable purchase typography and CTA states, neutral photo frames without editing merchandise, compact display names, native keyboard-accessible size radios backed by current API variants/prices, verified size guide next to purchase controls, mobile menu Escape behavior, cart thumbnails and continue-shopping links, product artwork context, order FAQs, three relevant editorial guides, Journal topic/search/reset combinations. No fabricated products, reviews, inventory, sales, discounts or production claims. Layout-only demo products removed on every host.

The public Fourthwall size guide was independently opened for Silent Chaos and Thorn Heart on 2026-11-16. Both charts show the same supplier garment dimensions:

| Size | Length cm | Width cm | Sleeve cm | Length in | Width in | Sleeve in |
| --- | --- | --- | --- | --- | --- | --- |
| S | 68 | 46 | 41 | 26.6 | 18.3 | 16.3 |
| M | 71 | 51 | 45 | 28 | 20.3 | 17.8 |
| L | 75 | 56 | 48 | 29.4 | 22 | 19 |
| XL | 78 | 61 | 52 | 30.8 | 24 | 20.5 |
| 2XL | 80 | 66 | 55 | 31.6 | 26 | 21.8 |
| 3XL | 83 | 70 | 59 | 32.5 | 27.8 | 23.3 |
| 4XL | 85 | 76 | 63 | 33.5 | 29.8 | 24.6 |

Source product URLs (open Size guide):
- https://shop.apocalypsecloset.com/products/silent-chaos-gothic-angel-graphic-tee-apocalypse-closet
- https://shop.apocalypsecloset.com/products/thorn-heart-gothic-graphic-tee-apocalypse-closet

These are supplier-published values, not mathematical conversions of rounded values. Supplier tolerance: up to 2 in / 5 cm. The on-site guide is explicitly allowlisted to these two products; future products use their own Fourthwall page. Reverify if garments change.

Prepared but not applied inside Fourthwall: `fourthwall-custom.css` reduces product heading size, moves options and CTA before the full description, and matches the main store's purchase button. Requires authenticated Fourthwall administration. No Fourthwall admin connector was found.

Newsletter capture requires a verified email platform/list or a working Fourthwall signup endpoint. No fake subscription form or mailto-as-signup was added. Customer photos need authentic assets and permission; existing product media were retained.

Historical preservation checks use exact SHA-256 matches for only the two approved UI successors. The current pages still undergo semantic/SEO and behavior tests; other pages retain their previous byte locks. No article body, slug, canonical, H1, SEO title or description was changed.
