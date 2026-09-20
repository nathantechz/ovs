#!/usr/bin/env python3
"""
Cache textbook text as Markdown so citations never need the PDFs again.

Opening a 900-page PDF to quote two paragraphs is slow and has to be repeated
every time. This extracts each book once into wiki/<category>/<book>.md with a
page marker before every page:

    <!-- page 189 -->

The number in the marker is the printed page — the one a student turns to —
already corrected by the offset measured for that book. Grepping the marker is
then enough to locate and cite a passage, and scripts/cite.py reads these files
in preference to the PDF.

Books whose page offset could not be established are still cached, but their
markers say `pdf-page` rather than `page`, so a citation drawn from them is
never presented as a printed page it might not be.

Front matter records the title, edition, year, page count and offset, so the
citation line can be assembled without reopening anything.

Usage:
    .venv/bin/python scripts/build-wiki.py --course-books   # the six UB courses
    .venv/bin/python scripts/build-wiki.py --all
    .venv/bin/python scripts/build-wiki.py --book "Kanski"
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
WIKI = os.path.join(PROJECT_DIR, "wiki")

# The books the University of Bisha diploma notes are grounded in. Matching is
# on a distinctive fragment of the filename.
COURSE_BOOKS = [
    "Kanski", "KURANA", "MODULE 2", "MODULE 3", "MODULE 5", "MODULE 6",
    "MODULE 9", "Visual Perception_A clinical", "Visual Optical Instruments",
    "System_for_Ophthalmic_Dispensing", "Clinical Refraction",
    "Optics of the Human Eye", "Evans_essentials",
    "introduction_to_ophthalmic_optics", "Perimetry", "Ultrasound",
    "Optical coherence tomography", "The lensometer",
]

# Known editions that the PDF text does not state cleanly.
EDITION_HINTS = {
    "Kanski": ("8th Edition", "2016", "Jack J. Kanski, Brad Bowling"),
    "System_for_Ophthalmic_Dispensing": ("3rd Edition", "2007", "Clifford Brooks, Irvin Borish"),
    "Clinical Refraction": ("2nd Edition", "2006", "William J. Benjamin (Borish's)"),
    "Visual Perception_A clinical": ("4th Edition", "2010", "Steven H. Schwartz"),
    "KURANA": ("", "", "A. K. Khurana"),
    "Optics of the Human Eye": ("", "2000", "David A. Atchison, George Smith"),
    "Evans_essentials": ("", "2005", "Bruce J. W. Evans"),
}


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)[:70]


def book_meta(book):
    for key, (edition, year, author) in EDITION_HINTS.items():
        if key.lower() in book["file"].lower():
            return edition, year, author
    return "", "", ""


def section_map(book):
    """pdf page index -> list of section titles starting on that page."""
    mapping = {}

    for section in book["sections"]:
        page = section.get("pdf_page")
        if page is None:
            continue
        mapping.setdefault(page, []).append(section)

    return mapping


def extract(book, out_path):
    offset = book.get("page_offset")
    uses_printed = offset is not None
    edition, year, author = book_meta(book)
    sections = section_map(book)

    front = [
        "---",
        f'title: "{book["title"]}"',
        f'category: "{book["category"]}"',
    ]
    if author:
        front.append(f'author: "{author}"')
    if edition:
        front.append(f'edition: "{edition}"')
    if year:
        front.append(f'year: "{year}"')
    front += [
        f"pages: {book['pages']}",
        f"page_offset: {offset if offset is not None else 'null'}",
        f"page_numbers: {'printed' if uses_printed else 'pdf-index-only'}",
        f'source_file: "{book["file"]}"',
        f"sections_indexed: {len(book['sections'])}",
        "---",
        "",
        f"# {book['title']}",
        "",
    ]

    if author or edition:
        front.append(f"*{author}{' — ' if author and edition else ''}{edition}"
                     f"{f' ({year})' if year else ''}*")
        front.append("")

    if not uses_printed:
        front.append("> Printed page numbers could not be established for this "
                     "book. Markers below give the PDF page index; cite them as "
                     "such rather than as printed pages.")
        front.append("")

    written_pages = 0
    body = []

    with pdfplumber.open(book["path"]) as pdf:
        total = len(pdf.pages)

        for index in range(total):
            try:
                text = pdf.pages[index].extract_text() or ""
            except Exception:
                continue

            if not text.strip():
                continue

            for section in sections.get(index, []):
                depth = min(section.get("depth", 0), 4)
                body.append("")
                body.append(f"{'#' * (depth + 2)} {section['title']}")
                body.append("")

            label = index + offset if uses_printed else index + 1
            kind = "page" if uses_printed else "pdf-page"

            # A negative or zero printed number means the offset does not hold
            # this far into the book; fall back to the honest PDF index.
            if uses_printed and label < 1:
                label, kind = index + 1, "pdf-page"

            body.append(f"<!-- {kind} {label} -->")
            body.append(text.rstrip())
            body.append("")
            written_pages += 1

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(front + body))

    return written_pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--course-books", action="store_true")
    parser.add_argument("--book", help="filename fragment")
    parser.add_argument("--force", action="store_true",
                        help="re-extract even if the .md already exists")
    args = parser.parse_args()

    if not os.path.exists(INDEX):
        print(f"Missing {INDEX}. Run scripts/index-library.py first.",
              file=sys.stderr)
        return 1

    index = json.load(open(INDEX, encoding="utf-8"))
    books = index["books"]

    if args.book:
        books = [b for b in books if args.book.lower() in b["file"].lower()]
    elif args.course_books:
        books = [b for b in books
                 if any(k.lower() in b["file"].lower() for k in COURSE_BOOKS)]
    elif not args.all:
        parser.error("choose --all, --course-books or --book")

    if not books:
        print("No books matched.")
        return 1

    print(f"Caching {len(books)} books into {WIKI}\n")

    manifest = []
    for number, book in enumerate(books, 1):
        out_path = os.path.join(WIKI, slugify(book["category"]),
                                slugify(book["title"]) + ".md")

        if os.path.exists(out_path) and not args.force:
            size = os.path.getsize(out_path) // 1024
            print(f"[{number}/{len(books)}] cached  {book['title'][:46]} ({size} KB)")
            manifest.append({"title": book["title"], "category": book["category"],
                             "path": os.path.relpath(out_path, PROJECT_DIR)})
            continue

        print(f"[{number}/{len(books)}] {book['title'][:52]}", flush=True)

        try:
            pages = extract(book, out_path)
        except Exception as exc:
            print(f"      failed: {type(exc).__name__}: {exc}")
            continue

        size = os.path.getsize(out_path) // 1024
        print(f"      {pages} pages -> {size} KB", flush=True)

        manifest.append({"title": book["title"], "category": book["category"],
                         "pages": pages,
                         "page_numbers": "printed" if book.get("page_offset") is not None
                                         else "pdf-index-only",
                         "path": os.path.relpath(out_path, PROJECT_DIR)})

    # A contents page for the wiki itself.
    by_category = {}
    for item in manifest:
        by_category.setdefault(item["category"], []).append(item)

    lines = ["# Textbook Wiki", "",
             "Cached full text of the library, one Markdown file per book.",
             "Every page carries a marker comment so a passage can be located "
             "and cited without reopening the PDF:", "",
             "```", "<!-- page 189 -->", "```", "",
             "`page` is the printed page number. `pdf-page` means the printed "
             "numbering could not be established for that book and the number "
             "is the PDF index instead.", ""]

    for category in sorted(by_category):
        lines.append(f"## {category}")
        lines.append("")
        for item in sorted(by_category[category], key=lambda i: i["title"]):
            note = "" if item.get("page_numbers") != "pdf-index-only" else "  *(pdf-index pages)*"
            lines.append(f"- [{item['title']}]({os.path.relpath(item['path'], 'wiki')})"
                         f"{note}")
        lines.append("")

    os.makedirs(WIKI, exist_ok=True)
    with open(os.path.join(WIKI, "README.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    print(f"\ncached books: {len(manifest)}")
    print(f"contents:     {os.path.join(WIKI, 'README.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
