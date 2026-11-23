# Consent assets

Edit assets/js/privacy-consent.js and assets/css/privacy-consent.css, then run:

```powershell
python -X utf8 tools/privacy/build_assets.py
```

The builder generates one fingerprinted JS/CSS pair and updates the script URL in
all HTML pages without reformatting their contents. Actual file paths change when
content changes so edge caches cannot keep an earlier version behind query strings.
The unversioned sources remain compatible with older cached HTML. When updating
again, retain earlier fingerprinted pairs until the HTML cache window has expired
before separately removing any pairs no longer referenced.
Compact layout rules are gated by ac-cookie-banner--compact so an older cached
script can still use the unversioned CSS without changing its original layout.

The banner offers equally styled analytics accept/decline buttons. Settings retains
the full storage explanation, optional analytics toggle and withdrawal controls.
The consent key/version, 180-day retention, production host gate, GPC treatment and
Google tag loading logic are unchanged by the compact-banner update.
