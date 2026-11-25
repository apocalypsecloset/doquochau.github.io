# Product schema snapshot

`catalog.snapshot.json` contains public product data read from the existing public
proxy. It contains no Storefront credential. The shared `ACShopModel.productSchema`
builds a ProductGroup with one Product and Offer per priced color/size, preserving
sold-out states. Variant URLs use `?variant=<public-id>` and preselect those options.

Run from this checkout before publishing a catalog/price/availability change:

```powershell
node tools/shop/build-schema.cjs --refresh
node tools/shop/build-schema.cjs --check
```

The first command reads the public API and refreshes the two static schema blocks
and fallback prices. Runtime still refreshes offers from the live catalog; it uses
the same schema function. Rebuild HTML whenever the upstream catalog changes so
non-JavaScript crawlers do not retain old offers. A snapshot is not real-time inventory.
No GTIN, review, loyalty benefit, return promise or shipping fee is invented.
