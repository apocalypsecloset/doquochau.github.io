# Article CSS

Article bundles have been split into three content-addressed shared blocks and
smaller detail files. HTML loads these in the same cascade order as the original
bundle; some detail rules intentionally precede a shared block.

Keep the order of the stylesheet links. CSS URLs remain in the same directory so
relative resource URLs retain their meaning. Filenames contain a content hash;
after changing an asset, use a new hash and update every reference to it.

`split_article_css.py` uses Python and tinycss2. It is a dry run by default;
`--write` migrates legacy `article-<16 hex>.css` files once. Re-running it after
migration reports that no legacy bundles remain. The manifest records the old
bundle to ordered asset mapping and verifies identical emitted CSS rules.

The two short editorial foundation bundles keep their independent styles. Their
rules are different from the larger article templates and are not forced into
the shared blocks.
