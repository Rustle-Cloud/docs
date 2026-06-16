#!/usr/bin/env python3
"""Inject SEO meta into the built mdBook (run after `mdbook build`, before deploy).

mdBook emits a per-page <title> and a single book-wide description, but no canonical,
no Open Graph / Twitter cards, and it duplicates the first chapter as both index.html
and introduction.html. This pass fixes all of that on the generated `book/`:

  * a self-referential canonical (introduction.html canonicalises to the root, killing
    the duplicate);
  * og:/twitter: title from the page <title>;
  * a real per-page description taken from the page's first paragraph (overriding the
    generic book description);
  * og:url / og:type / site_name / twitter:card.

Idempotent (skips a page that already has a canonical). stdlib only.
"""
import glob
import html
import os
import re

SITE = "https://docs.rustle.cloud/"
SKIP = {"404.html", "print.html", "toc.html"}
SKIP_REL = {"api/openapi.html"}  # standalone Redoc app, not a content page


def attr(s: str) -> str:
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def first_paragraph(doc: str) -> str | None:
    main = re.search(r"<main[^>]*>(.*?)</main>", doc, re.S)
    body = main.group(1) if main else doc
    for para in re.findall(r"<p>(.*?)</p>", body, re.S):
        text = html.unescape(re.sub(r"<[^>]+>", "", para))
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 40:
            if len(text) > 157:
                text = text[:157].rsplit(" ", 1)[0] + "…"
            return text
    return None


def main() -> None:
    changed = 0
    for path in glob.glob("book/**/*.html", recursive=True):
        rel = os.path.relpath(path, "book").replace(os.sep, "/")
        if os.path.basename(path) in SKIP or rel in SKIP_REL:
            continue
        doc = open(path, encoding="utf-8").read()
        if 'rel="canonical"' in doc:
            continue

        url = SITE if rel in ("index.html", "introduction.html") else SITE + rel
        tm = re.search(r"<title>(.*?)</title>", doc, re.S)
        title = html.unescape(tm.group(1).strip()) if tm else "Rustle Docs"
        desc = first_paragraph(doc)
        if not desc:
            dm = re.search(r'<meta name="description" content="(.*?)"', doc)
            desc = html.unescape(dm.group(1)) if dm else ""

        t, d = attr(title), attr(desc)
        tags = (
            f'<link rel="canonical" href="{url}">\n'
            f'<meta property="og:type" content="article">\n'
            f'<meta property="og:site_name" content="Rustle Docs">\n'
            f'<meta property="og:title" content="{t}">\n'
            f'<meta property="og:description" content="{d}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta name="twitter:card" content="summary">\n'
            f'<meta name="twitter:title" content="{t}">\n'
            f'<meta name="twitter:description" content="{d}">\n'
        )
        if desc:
            doc = re.sub(r'<meta name="description" content=".*?"\s*/?>',
                         f'<meta name="description" content="{d}">', doc, count=1)
        doc = doc.replace("</head>", tags + "</head>", 1)
        open(path, "w", encoding="utf-8").write(doc)
        changed += 1
    print(f"[seo] injected meta into {changed} pages")


if __name__ == "__main__":
    main()
