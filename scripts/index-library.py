#!/usr/bin/env python3
"""
Index the optometry textbook library so a topic can be traced to a book, a
section and a page.

Two things make citation possible later:

  * PDF bookmarks give a section tree with the PDF page each section starts on.
    Most books in the library carry them (Kanski has 2385).
  * The printed page number usually appears in the running head or foot, and it
    does not match the PDF index — front matter shifts it. Sampling a few pages
    and comparing the printed number to the PDF index recovers that offset, so a
    citation can quote the page a reader would actually turn to.

Books without bookmarks fall back to scanning early pages for a contents list.
A book that yields neither is still catalogued, marked so, and reported.

Output: data/library-index.json
    { books: [ { title, category, path, pages, page_offset,
                 sections: [ {title, pdf_page, printed_page, depth} ] } ] }

Usage:
    .venv/bin/python scripts/index-library.py
    .venv/bin/python scripts/index-library.py --category "Contact Lens"
    .venv/bin/python scripts/index-library.py --limit 5
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
    from pypdf import PdfReader
except ImportError:
    print("Needs pdfplumber and pypdf:  .venv/bin/pip install pdfplumber pypdf",
          file=sys.stderr)
    raise SystemExit(1)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(PROJECT_DIR, "data", "library-index.json")

DEFAULT_LIBRARY = os.path.expanduser(
    "~/Library/CloudStorage/Dropbox/Books/Optometry"
)

# A printed page number sitting alone at the start or end of a line.
PAGE_NUMBER = re.compile(r"(?:^|\n)\s*(\d{1,4})\s*(?:\n|$)")


def clean_title(name):
    """Turn a filename into something readable."""
    title = os.path.splitext(name)[0]
    title = re.sub(r"\s*\(z-lib\.org\)", "", title)
    title = re.sub(r"\s*\(\d+\)$", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def walk_outline(outline, reader, depth=0, out=None):
    """Flatten the bookmark tree into (title, pdf_page, depth)."""
    if out is None:
        out = []

    for item in outline:
        if isinstance(item, list):
            walk_outline(item, reader, depth + 1, out)
            continue

        try:
            page = reader.get_destination_page_number(item)
            title = str(item.title).strip()
        except Exception:
            continue

        if title:
            out.append({"title": title, "pdf_page": page, "depth": depth})

    return out


def detect_page_offset(pdf, sample_pages):
    """
    Work out printed_page - pdf_index by reading the number printed on a few
    pages. The most common difference wins; None if nothing agrees.
    """
    offsets = {}

    for index in sample_pages:
        if index >= len(pdf.pages):
            continue

        try:
            text = pdf.pages[index].extract_text() or ""
        except Exception:
            continue

        if not text:
            continue

        # Look only at the first and last couple of lines — running heads/feet.
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        candidates = lines[:2] + lines[-2:]

        for line in candidates:
            for match in re.finditer(r"\b(\d{1,4})\b", line):
                number = int(match.group(1))
                if 1 <= number <= len(pdf.pages) + 60:
                    offsets[number - index] = offsets.get(number - index, 0) + 1

    if not offsets:
        return None

    best, votes = max(offsets.items(), key=lambda kv: kv[1])

    # Guard against junk. A real offset is small and negative or near zero
    # (front matter pushes printed numbers behind the PDF index), and it must
    # never imply a printed page of zero or less.
    if votes < 2:
        return None
    if best > 0 or best < -120:
        return None
    if min(sample_pages) + best < 1:
        return None

    return best


def bookmarks_are_usable(sections):
    """
    Some PDFs carry a bookmark per printed page with a meaningless title —
    netLibrary exports label every entry "Document". Those cannot be cited.
    """
    if not sections:
        return False

    titles = [s["title"].strip().lower() for s in sections]
    distinct = len(set(titles))

    # Almost every title identical means the tree carries no information.
    if distinct <= max(2, len(titles) // 20):
        return False

    junk = sum(1 for t in titles if t in {"document", "untitled", "page"}
               or t.startswith("nlreader"))
    return junk < len(titles) / 2


def parse_contents_pages(pdf, max_pages=25):
    """
    Fallback for books with no bookmarks: find a contents page and read
    'Chapter title .... 123' lines off it.
    """
    entries = []
    line_pattern = re.compile(r"^(.{4,90}?)[\s.]{2,}(\d{1,4})\s*$")

    for index in range(min(max_pages, len(pdf.pages))):
        try:
            text = pdf.pages[index].extract_text() or ""
        except Exception:
            continue

        if not re.search(r"\bcontents\b", text[:400], re.I):
            continue

        for line in text.split("\n"):
            match = line_pattern.match(line.strip())
            if not match:
                continue

            title = match.group(1).strip(" .")
            printed = int(match.group(2))

            if len(title) > 3 and not title.isdigit():
                entries.append({
                    "title": title,
                    "printed_page": printed,
                    "pdf_page": None,
                    "depth": 0,
                })

    return entries


def index_book(path, category):
    record = {
        "title": clean_title(os.path.basename(path)),
        "file": os.path.basename(path),
        "category": category,
        "path": path,
        "pages": None,
        "page_offset": None,
        "section_source": "none",
        "sections": [],
    }

    # Bookmarks first — cheap and structured.
    try:
        reader = PdfReader(path)
        record["pages"] = len(reader.pages)

        outline = reader.outline
        if outline:
            sections = walk_outline(outline, reader)
            if sections and bookmarks_are_usable(sections):
                record["sections"] = sections
                record["section_source"] = "bookmarks"
            elif sections:
                record["section_source"] = "bookmarks_unusable"
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}"
        return record

    # Page offset, and a contents fallback when there were no bookmarks.
    try:
        with pdfplumber.open(path) as pdf:
            total = len(pdf.pages)
            sample = [int(total * f) for f in (0.3, 0.4, 0.5, 0.6, 0.7)]
            record["page_offset"] = detect_page_offset(pdf, sample)

            if not record["sections"]:
                fallback = parse_contents_pages(pdf)
                if fallback:
                    record["sections"] = fallback
                    record["section_source"] = "contents_page"
    except Exception:
        pass

    # Translate PDF pages into printed pages where the offset is known.
    offset = record["page_offset"]
    if offset is not None:
        for section in record["sections"]:
            if section.get("pdf_page") is not None:
                section["printed_page"] = section["pdf_page"] + offset

    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", default=DEFAULT_LIBRARY)
    parser.add_argument("--category", help="index only this category")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    if not os.path.isdir(args.library):
        print(f"Not a directory: {args.library}", file=sys.stderr)
        return 1

    pdfs = []
    for root, _dirs, files in os.walk(args.library):
        for name in sorted(files):
            if not name.lower().endswith(".pdf"):
                continue

            relative = os.path.relpath(root, args.library)
            category = relative.split(os.sep)[0] if relative != "." else "Uncategorised"

            if args.category and category.lower() != args.category.lower():
                continue

            pdfs.append((os.path.join(root, name), category))

    if args.limit:
        pdfs = pdfs[:args.limit]

    print(f"Indexing {len(pdfs)} PDFs from {args.library}\n")

    books = []
    for number, (path, category) in enumerate(pdfs, 1):
        name = os.path.basename(path)[:52]
        print(f"[{number}/{len(pdfs)}] {name}", flush=True)

        record = index_book(path, category)
        books.append(record)

        offset = record["page_offset"]
        print(f"      {record['section_source']:14} sections={len(record['sections']):4} "
              f"pages={record['pages']} offset={offset}", flush=True)

    with_sections = [b for b in books if b["sections"]]
    total_sections = sum(len(b["sections"]) for b in books)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    json.dump(
        {
            "library": args.library,
            "book_count": len(books),
            "books_with_sections": len(with_sections),
            "total_sections": total_sections,
            "books": books,
        },
        open(OUTPUT, "w", encoding="utf-8"),
        indent=2,
        ensure_ascii=False,
    )

    print("\n" + "=" * 58)
    print(f"books indexed:        {len(books)}")
    print(f"books with sections:  {len(with_sections)}")
    print(f"sections total:       {total_sections}")
    print(f"page offset resolved: {sum(1 for b in books if b['page_offset'] is not None)}")
    print(f"written:              {OUTPUT}")

    empty = [b for b in books if not b["sections"]]
    if empty:
        print(f"\nNo sections recovered from {len(empty)} books:")
        for book in empty[:10]:
            print(f"  - [{book['category']}] {book['title'][:54]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
