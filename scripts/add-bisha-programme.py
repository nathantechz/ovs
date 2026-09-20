#!/usr/bin/env python3
"""
Add the University of Bisha diploma to data/syllabi-local.json.

Bisha is the programme the study notes are being written against, but it was
missing from the Programmes page because its syllabus arrived as photographs of
the course-content tables rather than as a PDF the extractor could read. The
topics below are transcribed from those tables.

Unlike the extracted programmes, which list courses, this records the six
courses and their topics, with a link to the notes where they exist. Re-running
is safe: the existing Bisha entry is replaced.

Usage:
    .venv/bin/python scripts/add-bisha-programme.py
    .venv/bin/python scripts/render-programmes.py
"""

import json
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(PROJECT_DIR, "data", "syllabi-local.json")
NOTES_DIR = os.path.join(PROJECT_DIR, "notes", "ub-diploma")

INSTITUTION = "University of Bisha"

# Transcribed from the course-content tables. Each entry is
# (course, course_slug, [(topic title, contact hours), ...]).
COURSES = [
    ("Ocular Diseases", "ocular-diseases", [
        ("Introduction to ophthalmic diseases", 3),
        ("Eyelid disorders (ptosis, blepharospasm)", 3),
        ("Eyelid malpositions (entropion, ectropion, dermatitis)", 3),
        ("Eyelid infections and inflammation", 3),
        ("Conjunctival diseases and allergic conjunctivitis", 3),
        ("Dry eye disease", 3),
        ("Corneal diseases (part 1)", 3),
        ("Corneal diseases (part 2)", 3),
        ("Lens diseases", 3),
        ("Retinal diseases", 3),
    ]),
    ("Contact Lenses", "contact-lenses", [
        ("History of contact lenses", 1),
        ("Corneal topography and basic nomenclature of contact lenses", 2),
        ("Rigid gas permeable (GP) lenses: materials, manufacturing, care", 2),
        ("Optical properties of rigid lenses", 2),
        ("Complications of rigid lenses", 1),
        ("Soft contact lenses (SCL): materials, manufacturing, design, use", 2),
        ("Care of soft lenses", 1),
        ("Complications of soft lenses", 1),
        ("Complications of soft lenses (continued)", 1),
        ("Optical properties of soft lenses", 2),
    ]),
    ("Neurovisual Perception", "neurovisual-perception", [
        ("Retina and primary visual cortex", 2),
        ("Physiology of vision", 2),
        ("Light and dark adaptation", 2),
        ("Visual acuity", 2),
        ("Contrast sensitivity", 2),
        ("Color vision", 4),
        ("Color vision deficiencies", 2),
        ("Spatial vision", 2),
        ("Depth perception", 2),
    ]),
    ("Optical Instrumentation", "optical-instrumentation", [
        ("Visual acuity, contrast sensitivity, and color vision testing instruments", 2),
        ("Corneal topography and retinoscopy instruments", 3),
        ("Visual field testing", 2),
        ("A-scan, B-scan, and ultrasound imaging", 2),
        ("Electrophysiological tests (VEP, ERG, EOG)", 2),
        ("Contact lens curvature measurement device", 2),
        ("Lens power measurement device (lensmeter)", 2),
    ]),
    ("Ophthalmic Lenses and Spectacle Dispensing", "ophthalmic-lenses-dispensing", [
        ("Optics of ophthalmic lenses", None),
        ("Spherical lenses", None),
        ("Cylindrical lenses", None),
        ("Contact lenses", None),
        ("Lens notations and symbols", None),
        ("Prism, conical sections, and spherical equivalent", None),
        ("Vertex distance", None),
        ("Distance and near vision", None),
        ("Prentice's rule and decentration", None),
        ("Frames: types, parts, and measurements", None),
        ("Frame design and lens mounting", None),
    ]),
    ("Visual Optics and Binocular Vision", "visual-optics-binocular-vision", [
        ("Theoretical optics: the eye as an optical system", None),
        ("Optical principles of refractive errors and their correction", None),
        ("Fundamentals of corneal measurement and corneal topography", None),
        ("Principles of retinal imaging and their application to the eye", None),
        ("Accommodation of the eye", None),
        ("Binocular vision and eye movements", None),
        ("Eye movements and the use of prisms", None),
        ("Relationship between accommodation and eye movements", None),
        ("Strabismus and its types", None),
        ("Measurement of fixation disparity and eye stability", None),
    ]),
]


def notes_written(course_slug):
    """Which topic slugs already have a rendered note page."""
    folder = os.path.join(NOTES_DIR, course_slug)
    if not os.path.isdir(folder):
        return set()
    return {
        name[:-5] for name in os.listdir(folder)
        if name.endswith(".html") and name != "index.html"
    }


def build_entry():
    courses = []
    total_hours = 0

    for course_name, course_slug, topics in COURSES:
        written = notes_written(course_slug)

        for number, (title, hours) in enumerate(topics, 1):
            if hours:
                total_hours += hours

            # A note page is matched by its leading topic number.
            prefix = f"{number:02d}-"
            match = next((s for s in written if s.startswith(prefix)), None)

            entry = {
                "code": f"{course_slug[:4].upper()}-{number:02d}",
                "title": title,
                "course": course_name,
                "level": 1 if course_name in ("Ocular Diseases", "Contact Lenses") else 2,
            }
            if hours:
                entry["credits"] = hours
            if match:
                entry["notes_url"] = f"notes/ub-diploma/{course_slug}/{match}.html"

            courses.append(entry)

    return {
        "institution": INSTITUTION,
        "country": "Saudi Arabia",
        "programme": "Diploma in Optometry",
        "programme_type": "diploma",
        "duration_years": 2,
        "source_file": "course-content tables (transcribed from syllabus images)",
        "levels": sorted({c["level"] for c in courses}),
        "course_count": len(courses),
        "contact_hours": total_hours,
        "courses": courses,
    }


def main():
    if not os.path.exists(DATA):
        print(f"Missing {DATA}", file=sys.stderr)
        return 1

    data = json.load(open(DATA, encoding="utf-8"))

    data["programmes"] = [p for p in data["programmes"]
                          if p["institution"] != INSTITUTION]

    entry = build_entry()
    data["programmes"].append(entry)

    data["programme_count"] = len(data["programmes"])
    data["total_courses"] = sum(p["course_count"] for p in data["programmes"])

    json.dump(data, open(DATA, "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    linked = sum(1 for c in entry["courses"] if c.get("notes_url"))
    print(f"{INSTITUTION} — {entry['programme']}")
    print(f"  topics:        {entry['course_count']}")
    print(f"  contact hours: {entry['contact_hours']}")
    print(f"  notes linked:  {linked}")
    print(f"  programmes now: {data['programme_count']}, "
          f"topics/courses total: {data['total_courses']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
