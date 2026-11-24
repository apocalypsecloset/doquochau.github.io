# Shared English navigation style

English pages use `en-navigation.css` and `en-navigation.js` for their header and
footer. The component preserves each page's existing navigation destinations,
including labelled Vietnamese references, and retains the commerce cart button
and its ID on store/product pages. Article and product styles remain separate.

`apply_shell.py` applies the common markup to all `lang="en"` HTML documents.
It requires BeautifulSoup/lxml. Run after generating new English pages. It is
idempotent and verifies that navigation targets are preserved. Source HTML
contains the links and footer without requiring JavaScript; JavaScript controls
the mobile menu, dropdowns and active-page indicator.

When editing the CSS/JS, update the VERSION in the script and rerun it so pages
request the new assets. Keep the legacy site-shell assets for Vietnamese pages.
