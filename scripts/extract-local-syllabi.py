#!/usr/bin/env python3
"""
Extract curricula from the Saudi programme handbooks held locally.

The web scraper only reaches schools that publish curricula as HTML tables —
3 of 24. These handbooks are PDFs, so they need a different reader, and they
carry something the scraped pages mostly do not: an explicit programme type
and study level for every course.

Handled:
    KSU/OD         King Saud University — Doctor of Optometry
    KSU/MS         King Saud University — MSc (clinical and research tracks)
    KSU/OPTICIAN   King Saud University — Opticianry
    JED            University of Jeddah — Bachelor, bilingual tables

Levels come from the course code where the numbering encodes it — ASOD211 and
OPTO 221 are level 2, ASOD311 level 3 — which is how both institutions
structure their own handbooks.

The source tree is outside the repository, so pass --base if it has moved.

Usage:
    .venv/bin/python scripts/extract-local-syllabi.py
    .venv/bin/python scripts/extract-local-syllabi.py --base "/path/to/Opto Benchmark"
"""

import argparse
import json
import os
import re
import sys

try:
    import pdfplumber
except ImportError:
    print("pdfplumber is required:  .venv/bin/pip install pdfplumber", file=sys.stderr)
    raise SystemExit(1)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(PROJECT_DIR, "data", "syllabi-local.json")

DEFAULT_BASE = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive-MSRamaiahUniversityofAppliedSciences/"
    "Saad/Optometry Study/Opto Benchmark"
)

# "OPTO 221", "ASOD211", "MATH 140"
COURSE_CODE = re.compile(r"\b([A-Z]{2,4})\s?(\d{3})\b")

# A code, a title, then trailing numeric columns (lecture / lab / credit).
CODE_TITLE_HOURS = re.compile(
    r"^([A-Z]{2,4})\s?(\d{3})\s+(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s*$"
)

# MSc contents lines: "Visual Perception and Psychophysics OPTO 556 (2+1=3)"
MS_CONTENTS = re.compile(
    r"^(.+?)\s+([A-Z]{2,4})\s?(\d{3})\s*[:.]?\s*\((\d+)\+(\d+)=(\d+)\)"
)

# Opticianry lines: "OPTI 1201: Principles of Optics II - 3 credit(s)"
# The dash may be a hyphen or an en dash.
COLON_CREDITS = re.compile(
    r"^([A-Z]{2,4})\s?(\d{3,4})\s*:\s*(.+?)\s*[-–—]\s*(\d+)\s*credit",
    re.IGNORECASE,
)

SOURCES = [
    {
        "path": "KSU/OD/Optometry Doctor Program Handout KSU.pdf",
        "institution": "King Saud University",
        "country": "Saudi Arabia",
        "programme": "Doctor of Optometry",
        "programme_type": "od",
        "duration_years": 6,
        "parser": "tabular",
    },
    {
        "path": "KSU/MS/HandbookUpdated  2025 11.pdf",
        "institution": "King Saud University",
        "country": "Saudi Arabia",
        "programme": "MSc Optometry",
        "programme_type": "masters",
        "duration_years": 2,
        "parser": "ms_contents",
    },
    {
        "path": "KSU/OPTICIAN/OpticianryProgram Handbook.pdf",
        "institution": "King Saud University",
        "country": "Saudi Arabia",
        "programme": "Opticianry",
        "programme_type": "diploma",
        "duration_years": 2,
        "parser": "colon_credits",
    },
    {
        "path": "JED/البصريات.pdf",
        "institution": "University of Jeddah",
        "country": "Saudi Arabia",
        "programme": "Bachelor of Optometry",
        "programme_type": "bachelor",
        "duration_years": 5,
        "parser": "bilingual_tables",
    },
]

# Courses whose code or title marks them as research rather than clinical work.
RESEARCH_MARKERS = ("thesis", "research", "experimental design", "seminar",
                    "dissertation", "project")
CLINICAL_MARKERS = ("clinic", "clinical", "practice", "internship", "rotation")


def level_from_code(code):
    """OPTO 221 -> 2, ASOD311 -> 3. The hundreds digit is the study level."""
    match = re.search(r"(\d)(\d\d)$", code.replace(" ", ""))
    return int(match.group(1)) if match else None


def track_for(title, code):
    """Split masters courses into research and clinical tracks."""
    haystack = f"{title} {code}".lower()

    if any(word in haystack for word in RESEARCH_MARKERS):
        return "research"
    if any(word in haystack for word in CLINICAL_MARKERS):
        return "clinical"
    return "core"


def parse_tabular(pdf):
    """Lines of 'CODE Title lec lab credit'."""
    courses = []

    for page in pdf.pages:
        for line in (page.extract_text() or "").split("\n"):
            match = CODE_TITLE_HOURS.match(line.strip())
            if not match:
                continue

            prefix, number, title, lecture, lab, credits = match.groups()
            code = f"{prefix} {number}"
            title = title.strip(" .")

            if len(title) < 3:
                continue

            courses.append({
                "code": code,
                "title": title,
                "level": level_from_code(code),
                "lecture_hours": int(lecture),
                "lab_hours": int(lab),
                "credits": int(credits),
            })

    return courses


def parse_ms_contents(pdf):
    """MSc contents lines: 'Title OPTO 556 (2+1=3) ....'."""
    courses = []

    for page in pdf.pages:
        for raw in (page.extract_text() or "").split("\n"):
            line = raw.strip().rstrip(".")
            match = MS_CONTENTS.match(line)

            if match:
                title, prefix, number, lecture, lab, credits = match.groups()
                code = f"{prefix} {number}"
                courses.append({
                    "code": code,
                    "title": title.strip(" ."),
                    "level": level_from_code(code),
                    "lecture_hours": int(lecture),
                    "lab_hours": int(lab),
                    "credits": int(credits),
                })
                continue

            # "OPTO 600: Masters' thesis"
            thesis = re.match(r"^([A-Z]{2,4})\s?(\d{3})\s*:\s*(.+)$", line)
            if thesis:
                prefix, number, title = thesis.groups()
                code = f"{prefix} {number}"
                courses.append({
                    "code": code,
                    "title": title.strip(" ."),
                    "level": level_from_code(code),
                })

    return courses


def parse_bilingual_tables(pdf):
    """
    Jeddah's tables carry English and Arabic titles in separate columns, with
    the credit count and code scattered across padding cells.
    """
    courses = []

    for page in pdf.pages:
        for table in page.extract_tables() or []:
            for row in table:
                cells = [(c or "").strip() for c in row]
                joined = " ".join(cells)

                code_match = COURSE_CODE.search(joined)
                if not code_match:
                    continue

                code = f"{code_match.group(1)}{code_match.group(2)}"

                # The English title is the longest ASCII-only cell.
                english = ""
                arabic = ""
                for cell in cells:
                    if not cell or COURSE_CODE.fullmatch(cell.replace(" ", "")):
                        continue
                    if re.fullmatch(r"[\x00-\x7F\s\-&/,.'()IVX]+", cell):
                        if len(cell) > len(english):
                            english = cell
                    elif re.search(r"[؀-ۿ]", cell):
                        if len(cell) > len(arabic):
                            arabic = cell

                english = english.strip(" .")
                if len(english) < 4 or english.isdigit():
                    continue

                credits = None
                for cell in cells:
                    if re.fullmatch(r"[1-6]", cell):
                        credits = int(cell)
                        break

                courses.append({
                    "code": code,
                    "title": english,
                    "title_ar": arabic or None,
                    "level": level_from_code(code),
                    "credits": credits,
                })

    return courses


def parse_colon_credits(pdf):
    """
    Opticianry format: 'OPTI 1201: Title - 3 credit(s)', with the same codes
    reappearing later under 'Course Description' followed by a paragraph. The
    second occurrence is used to attach the description.
    """
    courses = {}
    order = []
    current_code = None
    description = []

    def flush():
        if current_code and description:
            text = " ".join(description).strip()
            if len(text) > 60 and current_code in courses:
                courses[current_code].setdefault("description", text)

    for page in pdf.pages:
        for raw in (page.extract_text() or "").split("\n"):
            line = raw.strip()
            match = COLON_CREDITS.match(line)

            if match:
                flush()
                description = []

                prefix, number, title, credits = match.groups()
                code = f"{prefix} {number}"
                current_code = code

                if code not in courses:
                    courses[code] = {
                        "code": code,
                        "title": title.strip(" ."),
                        # OPTI 1201 -> the second digit is the semester.
                        "level": int(number[1]) if len(number) == 4 else level_from_code(code),
                        "credits": int(credits),
                    }
                    order.append(code)
                continue

            # Skip running headers and stray page furniture.
            if current_code and line and not line.isupper():
                description.append(line)

    flush()
    return [courses[code] for code in order]


PARSERS = {
    "tabular": parse_tabular,
    "ms_contents": parse_ms_contents,
    "bilingual_tables": parse_bilingual_tables,
    "colon_credits": parse_colon_credits,
}


def dedupe(courses):
    seen = set()
    unique = []

    for course in courses:
        # Contents pages pad titles with dot leaders.
        course["title"] = re.sub(r"[.\s]{3,}$", "", course["title"]).strip(" .")
        key = (course["code"], course["title"].lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(course)

    return unique


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=DEFAULT_BASE,
                        help="folder holding the programme handbooks")
    args = parser.parse_args()

    if not os.path.isdir(args.base):
        print(f"Not a directory: {args.base}", file=sys.stderr)
        return 1

    programmes = []

    for source in SOURCES:
        path = os.path.join(args.base, source["path"])
        label = f"{source['institution']} — {source['programme']}"

        if not os.path.exists(path):
            print(f"  missing, skipped: {source['path']}")
            continue

        try:
            with pdfplumber.open(path) as pdf:
                courses = dedupe(PARSERS[source["parser"]](pdf))
        except Exception as exc:
            print(f"  failed: {label} ({type(exc).__name__}: {exc})")
            continue

        if source["programme_type"] == "masters":
            for course in courses:
                course["track"] = track_for(course["title"], course["code"])

        levels = sorted({c["level"] for c in courses if c["level"]})

        programmes.append({
            "institution": source["institution"],
            "country": source["country"],
            "programme": source["programme"],
            "programme_type": source["programme_type"],
            "duration_years": source["duration_years"],
            "source_file": source["path"],
            "levels": levels,
            "course_count": len(courses),
            "courses": courses,
        })

        print(f"  {label}: {len(courses)} courses, levels {levels or '-'}")

    total = sum(p["course_count"] for p in programmes)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    json.dump(
        {
            "source": "local programme handbooks (PDF)",
            "base": args.base,
            "programme_count": len(programmes),
            "total_courses": total,
            "programmes": programmes,
        },
        open(OUTPUT, "w", encoding="utf-8"),
        indent=2,
        ensure_ascii=False,
    )

    print(f"\nprogrammes: {len(programmes)}   courses: {total}")
    print(f"written:    {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
