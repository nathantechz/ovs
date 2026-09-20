#!/usr/bin/env python3
"""
Find and quote textbook passages for a topic, with citable page numbers.

This is the grounding tool: every concept written into a note should be
traceable to a book, a section and a printed page, and this is what produces
that evidence.

Given a topic it searches the indexed section titles, opens the matching pages,
and prints the text with the page a reader would actually turn to. The printed
page is derived from the offset measured in data/library-index.json, and when
that offset could not be established the output says "PDF page" instead of
inventing a printed number.

Usage:
    .venv/bin/python scripts/cite.py "dry eye"
    .venv/bin/python scripts/cite.py "entropion" --category "Ocular Diseases"
    .venv/bin/python scripts/cite.py "prentice" --pages 3 --chars 1800
    .venv/bin/python scripts/cite.py --book "Kanski" --section "Blepharitis"
"""

import argparse
import json
import os
import re
import sys
import warnings

warnings.filterwarnings("ignore")

try:
    import pdfplumber
except ImportError:
    print("Needs pdfplumber", file=sys.stderr)
    raise SystemExit(1)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(PROJECT_DIR, "data", "library-index.json")


def load_index():
    if not os.path.exists(INDEX):
        print(f"Missing {INDEX}. Run scripts/index-library.py first.",
              file=sys.stderr)
        raise SystemExit(1)
    return json.load(open(INDEX, encoding="utf-8"))


def score(section_title, terms):
    """How well a section title matches the search terms."""
    title = section_title.lower()
    hits = sum(1 for t in terms if t in title)

    if not hits:
        return 0

    # Whole-phrase and title-initial matches rank higher.
    phrase = " ".join(terms)
    if phrase in title:
        return 100 + hits
    if title.startswith(terms[0]):
        return 50 + hits

    return hits


def find_sections(index, query, category=None, book=None, limit=12):
    terms = [t for t in re.split(r"\s+", query.lower().strip()) if t]
    results = []

    for entry in index["books"]:
        if category and entry["category"].lower() != category.lower():
            continue
        if book and book.lower() not in entry["title"].lower():
            continue

        for section in entry["sections"]:
            value = score(section["title"], terms)
            if value:
                results.append((value, entry, section))

    results.sort(key=lambda r: -r[0])
    return results[:limit]


def page_label(book, section):
    """Say which page this is, and be honest about which kind."""
    printed = section.get("printed_page")
    pdf_page = section.get("pdf_page")

    if printed is not None and printed > 0:
        return f"p. {printed}", pdf_page
    if pdf_page is not None:
        return f"PDF p. {pdf_page + 1} (printed page unresolved)", pdf_page

    # Contents-page entries know the printed page but not the PDF index.
    if printed is not None:
        offset = book.get("page_offset")
        if offset is not None:
            return f"p. {printed}", printed - offset
        return f"p. {printed} (text not retrieved)", None

    return "page unknown", None


def quote(book, start_index, pages=2, chars=1200):
    """Pull text from the PDF starting at a page index."""
    if start_index is None:
        return None

    try:
        with pdfplumber.open(book["path"]) as pdf:
            chunks = []
            for offset in range(pages):
                index = start_index + offset
                if index >= len(pdf.pages):
                    break
                text = pdf.pages[index].extract_text() or ""
                if text.strip():
                    chunks.append(text)
    except Exception as exc:
        return f"[could not read: {type(exc).__name__}]"

    joined = re.sub(r"\n{2,}", "\n", "\n".join(chunks)).strip()
    return joined[:chars]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--category")
    parser.add_argument("--book")
    parser.add_argument("--section")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--pages", type=int, default=2)
    parser.add_argument("--chars", type=int, default=1200)
    parser.add_argument("--titles-only", action="store_true",
                        help="list matching sections without opening the PDFs")
    args = parser.parse_args()

    index = load_index()
    query = args.section or args.query

    if not query:
        parser.error("give a topic, or --section with --book")

    matches = find_sections(index, query, args.category, args.book, args.limit)

    if not matches:
        print(f"No section titles match {query!r}.")
        print("Try a shorter term, or --category to widen the net.")
        return 1

    print(f"{len(matches)} matching sections for {query!r}\n" + "=" * 62)

    for value, book, section in matches:
        label, start = page_label(book, section)

        print(f"\n{book['title'][:64]}")
        print(f"  [{book['category']}]  §{section['title'][:56]}  {label}")

        if args.titles_only:
            continue

        text = quote(book, start, args.pages, args.chars)
        if text:
            indented = "\n".join("    " + l for l in text.split("\n"))
            print(indented)
        else:
            print("    [no page index available for this entry]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
