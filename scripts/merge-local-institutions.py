#!/usr/bin/env python3
"""
Put the institutions we hold curricula for into the universities directory.

The Resources page listed "Middle East — 0 universities" while the Programmes
page carried seven full curricula from five Saudi institutions. The directory
and the syllabus data had simply never been joined, so the schools whose
curricula the site is built on were the ones it did not list.

This reads data/syllabi-local.json and writes those institutions into
js/universities-regional.js, one entry per institution with its programmes
named and a link through to the Programmes page. Entries are marked
source: "curricula-on-file" so they stay distinguishable from the scraped and
hand-curated ones.

Re-running replaces what it wrote before rather than duplicating.

    .venv/bin/python scripts/merge-local-institutions.py
"""

import json
import os
import re
import sys
from collections import defaultdict

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYLLABI = os.path.join(PROJECT_DIR, "data", "syllabi-local.json")
REGIONAL = os.path.join(PROJECT_DIR, "js", "universities-regional.js")

SOURCE_TAG = "curricula-on-file"

# Which region each country belongs to in the directory's structure.
COUNTRY_REGION = {
    "Saudi Arabia": "Middle East",
    "United Arab Emirates": "Middle East",
    "Iran": "Middle East",
}

# City per institution, for the directory entry.
CITIES = {
    "King Saud University": "Riyadh",
    "University of Jeddah": "Jeddah",
    "Qassim University": "Buraydah",
    "Umm Al-Qura University": "Makkah",
    "University of Bisha": "Bisha",
}

DEGREE_LABEL = {
    "od": "O.D.",
    "masters": "MSc",
    "bachelor": "B.Optom",
    "diploma": "Diploma",
}


def load_regional():
    source = open(REGIONAL, encoding="utf-8").read()
    match = re.search(r"const universitiesByRegion\s*=\s*(\{.*?\n\});", source, re.S)
    if not match:
        print("Could not parse universitiesByRegion", file=sys.stderr)
        raise SystemExit(1)
    return source, match, json.loads(match.group(1))


def main():
    if not os.path.exists(SYLLABI):
        print(f"Missing {SYLLABI}", file=sys.stderr)
        return 1

    syllabi = json.load(open(SYLLABI, encoding="utf-8"))
    source, match, regions = load_regional()

    # Group programmes by institution.
    by_institution = defaultdict(list)
    for programme in syllabi.get("programmes", []):
        by_institution[programme["institution"]].append(programme)

    added = 0
    for institution, programmes in sorted(by_institution.items()):
        country = programmes[0].get("country", "")
        region = COUNTRY_REGION.get(country)

        if region is None or region not in regions:
            print(f"  no region mapped for {country!r} — skipping {institution}")
            continue

        countries = regions[region]["countries"]
        countries.setdefault(country, [])

        # Drop any previous entry we wrote for this institution.
        countries[country] = [
            u for u in countries[country]
            if not (u.get("source") == SOURCE_TAG and u.get("name") == institution)
        ]

        names = ", ".join(sorted({p["programme"] for p in programmes}))
        degrees = sorted({DEGREE_LABEL.get(p["programme_type"], p["programme_type"])
                          for p in programmes})
        years = max(p.get("duration_years") or 0 for p in programmes)
        topics = sum(p.get("course_count", 0) for p in programmes)

        countries[country].append({
            "name": institution,
            "city": CITIES.get(institution, ""),
            "country": country,
            "program": names,
            "degree": " / ".join(degrees),
            "duration": f"{years} years" if years else "",
            "accreditation": "NCAAA",
            "programmeCount": len(programmes),
            "courseCount": topics,
            "curriculumUrl": "programmes.html",
            "source": SOURCE_TAG,
        })
        added += 1
        print(f"  {institution}: {len(programmes)} programme(s), {topics} courses")

    # Recount and rewrite.
    updated = json.dumps(regions, indent=4, ensure_ascii=False)
    new_source = source[:match.start(1)] + updated + source[match.end(1):]

    total = sum(len(u) for r in regions.values() for u in r["countries"].values())
    new_source = re.sub(r"// Total: \d+", f"// Total: {total}", new_source)

    open(REGIONAL, "w", encoding="utf-8").write(new_source)

    print(f"\ninstitutions merged: {added}")
    print(f"directory total now: {total}")
    for region, entry in regions.items():
        count = sum(len(u) for u in entry["countries"].values())
        print(f"  {region:16} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
