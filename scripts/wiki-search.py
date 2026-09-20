#!/usr/bin/env python3
"""
Search the cached textbook wiki and return passages with their printed pages.

Reads wiki/**/*.md, which scripts/build-wiki.py wrote with a marker before each
page. Searching the cache avoids reopening the PDFs, so a lookup that used to
take a minute takes under a second.

Every hit reports the book, edition and the page carried by the nearest marker
above it. A book whose printed numbering could not be established is marked
"pdf p." so the distinction survives into whatever is written from it.

Usage:
    .venv/bin/python scripts/wiki-search.py "entropion"
    .venv/bin/python scripts/wiki-search.py "Schirmer" --book kanski
    .venv/bin/python scripts/wiki-search.py "keratoconus" --context 900 --limit 4
"""

import argparse
import glob
import os
import re
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(PROJECT_DIR, "wiki")

MARKER = re.compile(r"<!-- (page|pdf-page) (\d+) -->")


def read_front_matter(text):
    meta = {}
    if not text.startswith("---"):
        return meta, text

    end = text.find("\n---", 3)
    if end == -1:
        return meta, text

    for line in text[3:end].strip().split("\n"):
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')

    return meta, text[end + 4:]


def page_at(body, position):
    """The page marker immediately above this position."""
    last = None
    for match in MARKER.finditer(body, 0, position):
        last = match
    if not last:
        return None, None
    return last.group(1), int(last.group(2))


def citation(meta, kind, number):
    parts = [meta.get("title", "unknown")]
    if meta.get("edition"):
        parts.append(meta["edition"])
    if meta.get("year"):
        parts.append(meta["year"])

    head = ", ".join(parts)
    if number is None:
        return f"{head} (page unknown)"

    label = "p." if kind == "page" else "pdf p."
    return f"{head}, {label} {number}"


def search(query, book_filter=None, limit=8, context=600):
    terms = [t for t in query.lower().split() if t]
    if not terms:
        return []

    hits = []

    for path in sorted(glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True)):
        if os.path.basename(path) == "README.md":
            continue
        if book_filter and book_filter.lower() not in os.path.basename(path).lower():
            continue

        text = open(path, encoding="utf-8", errors="replace").read()
        meta, body = read_front_matter(text)
        lowered = body.lower()

        phrase = " ".join(terms)
        for match in re.finditer(re.escape(phrase), lowered):
            start = match.start()
            kind, number = page_at(body, start)

            begin = max(0, start - context // 3)
            passage = body[begin:start + context]
            passage = MARKER.sub("", passage)
            passage = re.sub(r"\n{2,}", "\n", passage).strip()

            hits.append({
                "cite": citation(meta, kind, number),
                "category": meta.get("category", ""),
                "page": number,
                "kind": kind,
                "text": passage,
            })

            if len(hits) >= limit * 3:
                break

    # Prefer earlier, denser hits but keep book variety.
    seen_books = {}
    ordered = []
    for hit in hits:
        book = hit["cite"].split(",")[0]
        seen_books[book] = seen_books.get(book, 0) + 1
        if seen_books[book] <= 3:
            ordered.append(hit)

    return ordered[:limit]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--book")
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--context", type=int, default=600)
    args = parser.parse_args()

    if not os.path.isdir(WIKI):
        print("No wiki/ yet. Run scripts/build-wiki.py --course-books",
              file=sys.stderr)
        return 1

    results = search(args.query, args.book, args.limit, args.context)

    if not results:
        print(f"No passages contain {args.query!r}.")
        return 1

    print(f"{len(results)} passages for {args.query!r}\n" + "=" * 66)
    for hit in results:
        print(f"\n### {hit['cite']}")
        print("\n".join("    " + l for l in hit["text"].split("\n")))

    return 0


if __name__ == "__main__":
    sys.exit(main())
