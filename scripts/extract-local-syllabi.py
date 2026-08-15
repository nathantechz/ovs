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
    QU             Qassim University — Doctor of Optometry (from course specs)
    UmQ            Umm Al-Qura University — Opticianry Diploma

Levels come from the course code where the numbering encodes it — ASOD211 and
OPTO 221 are level 2, ASOD311 level 3 — which is how both institutions
structure their own handbooks.

The source tree is outside the repository, so pass --base if it has moved.

Usage:
    python3 scripts/extract-local-syllabi.py
    python3 scripts/extract-local-syllabi.py --base "/path/to/Opto Benchmark"
"""

import argparse
import json
import os
import re
import sys

try:
    import pdfplumber
except ImportError:
    print("pdfplumber is required:  pip install pdfplumber", file=sys.stderr)
    raise SystemExit(1)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(PROJECT_DIR, "data", "syllabi-local.json")

DEFAULT_BASE = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive-MSRamaiahUniversityofAppliedSciences/"
    "Saad/Optometry Study/Opto Benchmark"
)

# "OPTO 221", "ASOD211", "MATH 140"
COURSE_CODE = re.compile(r"\b([A-Z]{2,4})\s?(\d{3,4})\b")

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

# ─── KSU OD: Known truncated titles and their corrected versions ──────────
# PDF line-breaks truncate these titles at a column boundary. We provide the
# complete title from the handbook's descriptive paragraphs.
KSU_OD_TITLE_FIXES = {
    "OPTO 224": "Clinical Examination of the Visual System I",
    "OPTO 314": "Clinical Examination of Visual System II",
    "OPTO 316": "Anatomy and Physiology of the Eye",
    "OPTO 323": "Clinical Examination of the Visual System III",
    "OPTO 413": "Ocular Neuroanatomy and Neurophysiology",
    "OPTO 414": "Oculomotor Functions and Binocular Vision",
    "OPTO 419": "Clinical Examination of the Visual System IV",
    "OPTO 431": "Clinical Examination of the Visual System V",
    "OPTO 439": "Principles and Psychology of Learning",
    "OPTO 450": "Current Topics in Optometry and Vision Science",
}

# ─── University of Jeddah: Newline and truncation fixes ─────────────────────
JED_TITLE_FIXES = {
    "ASOD214": "Human Anatomy & Physiology",
    "ASOD216": "Ophthalmic Optics & Dispensing I",
    "ASOD224": "Ophthalmic Optics & Dispensing II",
    "ASOD312": "Clinical Examination of the Visual System I",
    "ASOD313": "Anatomy and Physiology of the Head and Neck",
    "ASOD412": "Clinical Examination of the Visual System II",
    "ASOD424": "Clinical Examination of the Visual System III",
    "ASOD512": "Optometry Professionalism and Ethics",
}

# ─── Qassim University: Course code → title mapping from spec PDFs ────────
QU_COURSE_MAP = {
    "OPTM 231": "Ocular Anatomy and Physiology",
    "OPTM 232": "Introduction to Optometry",
    "OPTM 241": "Geometrical Optics",
    "OPTM 242": "Physical Optics",
    "OPTM 251": "Neuroscience",
    "OPTM 332": "Ocular Biochemistry",
    "OPTM 342": "Visual Optics",
    "OPTM 344": "Ophthalmic Optics and Dispensing",
    "OPTM 352": "Vision Science 1",
    "OPTM 353": "Vision Science 2",
    "OPTM 361": "Optometry I",
    "OPTM 362": "Optometry II",
    "OPTM 371": "Ocular Disease 1 (Anterior Segment)",
    "OPTM 381": "Clinical Procedures I",
    "OPTM 454": "Binocular Vision",
    "OPTM 463": "Optometry III",
    "OPTM 464": "Pediatric Optometry",
    "OPTM 465": "Integrated Optometry",
    "OPTM 466": "Occupational Optometry",
    "OPTM 472": "Ocular Pharmacology I",
    "OPTM 473": "Clinical Procedures II",
    "OPTM 474": "Ocular Pharmacology II",
    "OPTM 475": "Eye and Systemic Disease",
    "OPTM 477": "Ocular Diseases 3",
    "OPTM 478": "Ocular Disease 2 (Posterior Segment)",
    "OPTM 482": "Clinical Procedures III",
    "OPTM 491": "Contact Lens 1",
    "OPTM 492": "Contact Lens 2",
    "OPTM 493": "Low Vision",
    "OPTM 494": "Specialty Contact Lens",
    "OPTM 545": "Community Optometry",
    "OPTM 567": "Optometry Practice and Management",
    "OPTM 569": "Graduation Project",
    "OPTM 583": "Clinical Externship I",
    "OPTM 585": "Clinical Externship II",
    "OPTM 586": "Pediatric Clinic",
    "OPTM 588": "Contact Lens Clinic",
    "OPTM 589": "Clinical Externship III",
    "OPTM 594": "Optometry Clinic I",
    "OPTM 595": "Optometry Clinic II",
    "OPTM 597": "Internship",
    "OPTO 565": "Optometric Research Methods",
    "OPTM 566": "Neuro-Optometry Clinic",
    "HLTH 421": "Biostatistics",
    "HLTH 424": "Epidemiology",
    "HLTH 426": "Health Management",
    "PHG 333": "General Pharmacology",
    # Non-optometry prerequisite codes from the mapping matrix
    "HLTH 222": "Medical Ethics",
    "HLTH 225": "Health Informatics",
    "HLTH 233": "Introduction to Health Sciences",
    "ANAT 212": "Human Anatomy",
    "PHSL 215": "Human Physiology",
    "MDL 111": "General Biology",
    "MDL 242": "Microbiology",
    "MDL 352": "General Pathology",
    "PHS 115": "Medical Physics",
    "MEDU 111": "Medical Education",
}

# ─── Umm Al-Qura: Code → English title (from Arabic study plan) ───────────
UMQ_COURSE_MAP = {
    "APOP1101T": "Principles of Mathematics",
    "APOP1102T": "Ocular Anatomy and Physiology",
    "APOP1103T": "Primary Eye Care and Professional Ethics",
    "APOP1104T": "Communication and Marketing Skills in Optometry",
    "APOP1105T": "Ophthalmic Lenses",
    "APOP1106T": "Physical Optics",
    "APOP2107T": "Geometric Optics",
    "APOP2108T": "Ophthalmic Lens Manufacturing",
    "APOP2109T": "Ophthalmic Lens Fitting I",
    "APOP2110T": "Contact Lenses I",
    "APOP3111T": "Optometric Examination I",
    "APOP3112T": "Computer Skills",
    "APOP3113T": "Ophthalmic Lens Fitting II",
    "APOP3114T": "Contact Lenses II",
    "APOP4115T": "Medical Reports",
    "APOP4116T": "Biostatistics",
    "APOP4117T": "Optometric Examination II",
    "APOP4118T": "Optical Center Management",
    "APOP4119T": "Ophthalmic Lens Fitting III",
    "APOP4901T": "Cooperative Training in Optometry",
    "AP1301T": "English Language I",
    "AP1302T": "English Language II",
    "AP1310T": "Values and Ethics",
    "AP1510T": "Professional Skills",
    "AP1201T": "AI Applications",
}


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
CLINICAL_MARKERS = ("clinic", "clinical", "practice", "internship", "rotation",
                    "externship")


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


def clean_title(title):
    """Normalize whitespace, remove newlines, and strip artifacts."""
    title = title.replace("\n", " ").replace("\r", " ")
    title = re.sub(r"\s+", " ", title).strip(" .")
    # Remove trailing page-number artifacts
    title = re.sub(r"\s+\d+$", "", title)
    return title


def parse_tabular(pdf):
    """Lines of 'CODE Title lec lab credit'."""
    courses = []
    all_lines = []

    for page in pdf.pages:
        for line in (page.extract_text() or "").split("\n"):
            all_lines.append(line.strip())

    # Multi-pass: first collect raw matches, then attempt to recover truncated
    # titles by peeking at continuation lines
    i = 0
    while i < len(all_lines):
        line = all_lines[i]
        match = CODE_TITLE_HOURS.match(line)
        if not match:
            i += 1
            continue

        prefix, number, title, lecture, lab, credits = match.groups()
        code = f"{prefix} {number}"
        title = clean_title(title)

        if len(title) < 3:
            i += 1
            continue

        # Apply known fixes for truncated titles
        if code in KSU_OD_TITLE_FIXES:
            title = KSU_OD_TITLE_FIXES[code]

        courses.append({
            "code": code,
            "title": title,
            "level": level_from_code(code),
            "lecture_hours": int(lecture),
            "lab_hours": int(lab),
            "credits": int(credits),
        })
        i += 1

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
                    "title": clean_title(title),
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
                    "title": clean_title(title),
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

                english = clean_title(english)
                if len(english) < 4 or english.isdigit():
                    continue

                # Apply known fixes for truncated/newline titles
                if code in JED_TITLE_FIXES:
                    english = JED_TITLE_FIXES[code]

                # Clean Arabic: remove excessive internal spaces from garbled OCR
                if arabic:
                    arabic = clean_title(arabic)

                credits = None
                for cell in cells:
                    if re.fullmatch(r"[1-8]", cell):
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
            # Remove artifacts like "16 Development and Quality Committee 2024"
            text = re.sub(r"\d+\s+Development and Quality Committee\s*\d*", "", text).strip()
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
                        "title": clean_title(title),
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


def parse_qu_course_specs(base_dir):
    """
    Qassim University: extract from 30 individual course specification PDFs and
    supplement with the course code → title mapping from the programme spec matrix.
    """
    spec_dir = os.path.join(
        base_dir,
        "QU/الاعتماد/4 - إعداد توصيفات المقررات + وتقاريرها/"
        "Course Specifications - Doctor of Optometry Program"
    )

    courses = {}

    # First, populate from the known mapping (covers all codes from the matrix)
    for code, title in QU_COURSE_MAP.items():
        level = level_from_code(code)
        courses[code] = {
            "code": code,
            "title": title,
            "level": level,
        }

    # Then enrich from the individual spec PDFs (descriptions, credit hours)
    if os.path.isdir(spec_dir):
        for fname in sorted(os.listdir(spec_dir)):
            if not fname.endswith(".pdf"):
                continue
            fpath = os.path.join(spec_dir, fname)
            try:
                with pdfplumber.open(fpath) as pdf:
                    text = ""
                    for page in pdf.pages[:3]:
                        text += (page.extract_text() or "") + "\n"

                    # Find course code
                    code_match = re.search(r"(OPTM|HLTH|PHG|ANAT|PHSL|MDL)\s*(\d{3})", text)
                    if not code_match:
                        continue
                    code = f"{code_match.group(1)} {code_match.group(2)}"

                    # Extract credit hours
                    credit_match = re.search(
                        r"Credit\s*(?:hours?|units?)\s*[:=]?\s*(\d+)",
                        text, re.IGNORECASE
                    )
                    if credit_match and code in courses:
                        courses[code]["credits"] = int(credit_match.group(1))

                    # Extract lecture/lab hours if available
                    lec_match = re.search(
                        r"Lecture\s*[:=]?\s*(\d+)\s*.*?(?:Lab|Practical|Tutorial)\s*[:=]?\s*(\d+)",
                        text, re.IGNORECASE | re.DOTALL
                    )
                    if lec_match and code in courses:
                        courses[code]["lecture_hours"] = int(lec_match.group(1))
                        courses[code]["lab_hours"] = int(lec_match.group(2))

                    # Extract course description
                    desc_match = re.search(
                        r"(?:Course\s*Description|Description)\s*[:.]?\s*\n(.+?)(?:\n\s*\n|\n\d+\.\s)",
                        text, re.IGNORECASE | re.DOTALL
                    )
                    if desc_match and code in courses:
                        desc = clean_title(desc_match.group(1))
                        if len(desc) > 40:
                            courses[code]["description"] = desc

            except Exception as e:
                print(f"  warning: {fname}: {e}")

    # Sort by code for stable output
    return sorted(courses.values(), key=lambda c: c["code"])


def parse_umq(base_dir):
    """
    Umm Al-Qura University: extract from study plan PDF (Arabic) and map to
    English titles.
    """
    pdf_path = os.path.join(base_dir, "UmQ/9aad98cd-c8e4-45ab-9bf6-89ac58092085-2.pdf")
    if not os.path.exists(pdf_path):
        return []

    courses = []
    seen_codes = set()

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables() or []:
                    for row in table:
                        cells = [(c or "").strip() for c in row]
                        joined = " ".join(cells)

                        # Find APOP/AP codes
                        for m in re.finditer(r"(APOP?\d{3,4}T?|AP\d{4}T?)", joined):
                            code = m.group(1)
                            if code in seen_codes:
                                continue
                            seen_codes.add(code)

                            title = UMQ_COURSE_MAP.get(code, "")
                            if not title:
                                continue

                            # Find Arabic title near the code
                            arabic = ""
                            for cell in cells:
                                if re.search(r"[؀-ۿﺀ-﻿ﭐ-﮿]", cell) and len(cell) > 3:
                                    candidate = clean_title(cell)
                                    if len(candidate) > len(arabic):
                                        arabic = candidate

                            # Credit hours from adjacent numeric cells
                            credits = None
                            for cell in cells:
                                if re.fullmatch(r"[2-6]", cell.strip()):
                                    credits = int(cell.strip())
                                    break

                            # Level from code: APOP1xxx = level 1, APOP2xxx = level 2...
                            level_match = re.search(r"(\d)\d{2,3}T?$", code)
                            level = int(level_match.group(1)) if level_match else None

                            courses.append({
                                "code": code,
                                "title": title,
                                "title_ar": arabic or None,
                                "level": level,
                                "credits": credits,
                            })
    except Exception as e:
        print(f"  warning: UmQ extraction error: {e}")

    return courses


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
        # Contents pages pad titles with dot leaders, sometimes followed by a
        # page number, so cut at the leader rather than trimming the end.
        course["title"] = re.split(r"\.{3,}", course["title"])[0].strip(" .")
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

    # ─── Standard PDF sources ───────────────────────────────────────────
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

    # ─── Qassim University (from course specification PDFs) ─────────────
    qu_courses = parse_qu_course_specs(args.base)
    if qu_courses:
        qu_levels = sorted({c["level"] for c in qu_courses if c.get("level")})
        programmes.append({
            "institution": "Qassim University",
            "country": "Saudi Arabia",
            "programme": "Doctor of Optometry",
            "programme_type": "od",
            "duration_years": 6,
            "source_file": "QU/Course Specifications + Programme Specification",
            "levels": qu_levels,
            "course_count": len(qu_courses),
            "courses": qu_courses,
        })
        print(f"  Qassim University — Doctor of Optometry: "
              f"{len(qu_courses)} courses, levels {qu_levels}")

    # ─── Umm Al-Qura University (Opticianry Diploma) ───────────────────
    umq_courses = parse_umq(args.base)
    if umq_courses:
        umq_levels = sorted({c["level"] for c in umq_courses if c.get("level")})
        programmes.append({
            "institution": "Umm Al-Qura University",
            "country": "Saudi Arabia",
            "programme": "Opticianry Diploma",
            "programme_type": "diploma",
            "duration_years": 2,
            "source_file": "UmQ/9aad98cd-c8e4-45ab-9bf6-89ac58092085-2.pdf",
            "levels": umq_levels,
            "course_count": len(umq_courses),
            "courses": umq_courses,
        })
        print(f"  Umm Al-Qura University — Opticianry Diploma: "
              f"{len(umq_courses)} courses, levels {umq_levels}")

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
