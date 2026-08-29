"""Redirect stubs for old GoDaddy-site URLs still living in search indexes.

GitHub Pages cannot emit HTTP 301s, so each old path gets a stub page with an
instant meta refresh plus a canonical tag pointing at the replacement; search
engines treat that pair as a permanent redirect. Old paths that happen to match
a new filename (/contact -> contact.html) need no stub: Pages resolves
extensionless URLs to .html on its own. Each stub is written as dir/index.html
so both /old-path and /old-path/ resolve. Rerun after adding rows to REDIRECTS.
"""
import pathlib

REDIRECTS = {
    "about-tripp": "about.html",
    "contact-me": "contact.html",
    "victim-services": "victims.html",
    "open-records": "contact.html",
    "blog": "index.html",
    "photo-gallery": "index.html",
    "home": "index.html",
}

STUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved &mdash; Tripp Fitzner, District Attorney</title>
<link rel="canonical" href="https://middleda.org/{target}">
<meta http-equiv="refresh" content="0; url=https://middleda.org/{target}">
</head>
<body>
<p>This page has moved to <a href="https://middleda.org/{target}">middleda.org/{target}</a>.</p>
</body>
</html>
"""

for old, target in REDIRECTS.items():
    d = pathlib.Path(old)
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(STUB.format(target=target), encoding="utf-8")
    print(f"stub: /{old}/ -> /{target}")
