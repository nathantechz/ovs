#!/usr/bin/env python3
"""
Print a page range straight out of the cached wiki.

Once a topic's pages are known — from a book's contents list or from
scripts/wiki-search.py — this pulls exactly those pages so the note can be
written from the source text rather than from memory.

Usage:
    .venv/bin/python scripts/wiki-pages.py kanski 34 37
    .venv/bin/python scripts/wiki-pages.py module-3 20 24 --raw
"""

import argparse
import glob
import os
import re
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(PROJECT_DIR, "wiki")

MARKER = re.compile(r"<!-- (page|pdf-page) (\d+) -->")


def find_book(fragment):
    matches = [
        p for p in glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True)
        if fragment.lower() in os.path.basename(p).lower()
        and os.path.basename(p) != "README.md"
    ]
    if not matches:
        return None
    return sorted(matches, key=len)[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book", help="filename fragment, e.g. kanski")
    parser.add_argument("start", type=int)
    parser.add_argument("end", type=int, nargs="?")
    parser.add_argument("--raw", action="store_true",
                        help="omit the page banners")
    args = parser.parse_args()

    path = find_book(args.book)
    if not path:
        print(f"No cached book matches {args.book!r}. Files available:",
              file=sys.stderr)
        for p in sorted(glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True)):
            print(f"  {os.path.basename(p)}", file=sys.stderr)
        return 1

    end = args.end if args.end is not None else args.start
    text = open(path, encoding="utf-8", errors="replace").read()

    parts = MARKER.split(text)
    # parts: [pre, kind, number, body, kind, number, body, ...]
    printed = 0
    for i in range(1, len(parts), 3):
        kind, number, body = parts[i], int(parts[i + 1]), parts[i + 2]
        if args.start <= number <= end:
            if not args.raw:
                label = "p." if kind == "page" else "pdf p."
                print(f"\n=========== {label} {number} ===========")
            print(body.strip())
            printed += 1

    if not printed:
        print(f"No pages {args.start}-{end} in {os.path.basename(path)}.",
              file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
