#!/usr/bin/env python3
"""
Point each note page's back-link at the course it belongs to.

The generated pages all link to "../index.html", which lands the reader on the
home page having lost their place. With hash routing in place they can return
to the exact course instead: ../index.html#/course/<id>.

Course ids are read from js/data.js so this stays correct if the catalogue is
renumbered. Idempotent — safe to re-run after regenerating the notes.
"""

import json
import os
import re
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_DIR = os.path.join(PROJECT_DIR, "notes")
DATA_JS = os.path.join(PROJECT_DIR, "js", "data.js")

# Which course each note filename prefix belongs to. The note sets are named
# after their folder, which does not always match the course title in data.js.
PREFIX_TO_COURSE = {
    "physical-optics": "Physical Optics",
    "ocular-anatomy": "Anatomy & Physiology of the Eye",
    "strabismus": "Binocular Vision Physiology",
}


def course_ids():
    """Map course title -> id by reading the id/title pairs out of data.js."""
    source = open(DATA_JS, encoding="utf-8").read()
    pairs = re.findall(r"id:\s*(\d+),\s*\n\s*title:\s*\"([^\"]+)\"", source)
    return {title: int(cid) for cid, title in pairs}


def main():
    ids = course_ids()
    if not ids:
        print("Could not read any courses from data.js", file=sys.stderr)
        return 1

    targets = {}
    for prefix, title in PREFIX_TO_COURSE.items():
        if title not in ids:
            print(f"No course titled {title!r} in data.js — skipping {prefix}",
                  file=sys.stderr)
            continue
        targets[prefix] = (ids[title], title)

    updated = 0
    for filename in sorted(os.listdir(NOTES_DIR)):
        if not filename.endswith(".html"):
            continue

        match = next((p for p in targets if filename.startswith(p)), None)
        if not match:
            continue

        course_id, course_title = targets[match]
        path = os.path.join(NOTES_DIR, filename)
        source = open(path, encoding="utf-8").read()

        new_link = (
            f'<a class="note-return" href="../index.html#/course/{course_id}">'
            f'&larr; Back to {course_title}</a>'
        )

        # Replace whatever the current back-link is with the course-specific one.
        updated_source, count = re.subn(
            r'<a[^>]*href="\.\./index\.html(?:#[^"]*)?"[^>]*>.*?</a>',
            new_link,
            source,
            count=1,
            flags=re.DOTALL,
        )

        if count and updated_source != source:
            open(path, "w", encoding="utf-8").write(updated_source)
            updated += 1

    print(f"back-links pointed at their course: {updated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
