#!/usr/bin/env python3
"""
Extract published curricula from optometry school websites.

Starts from the ASCO member directory, follows each school's curriculum or
academics page, and pulls out course tables — course code, title, credit hours
and the term heading the table sits under.

What this can and cannot do, measured rather than assumed:

  * Schools that publish curricula as HTML tables parse cleanly. Southern
    College of Optometry, for example, yields 70+ courses across 11 term
    tables.
  * Schools that render their curriculum with JavaScript, publish it only as a
    PDF, or bury it in prose yield nothing. Requests sees no course codes on
    those pages at all.

The report at the end says which schools produced data and which did not, so
the gaps are visible instead of being quietly filled in. Nothing is invented:
a school that yields no courses is reported as zero.

Usage:
    .venv/bin/python scripts/extract-syllabi.py            # all ASCO schools
    .venv/bin/python scripts/extract-syllabi.py --limit 5  # first five
    .venv/bin/python scripts/extract-syllabi.py --out data/syllabi.json
"""

import argparse
import json
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUT = os.path.join(PROJECT_DIR, "data", "syllabi.json")

sys.path.insert(0, SCRIPT_DIR)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
)

# "OPT 110", "CLN203", "VS 421"
COURSE_CODE = re.compile(r"^([A-Z]{2,5})\s?[- ]?(\d{3,4})$")

# Words that mark a link as leading to curriculum content.
CURRICULUM_HINTS = ("curricul", "course of study", "program of study",
                    "academic program", "courses")

# Many schools do not link the curriculum from the home page; it sits one level
# in, behind an "Academics" or "Doctor of Optometry" page.
SECTION_HINTS = ("academic", "doctor of optometry", "od program",
                 "program", "degree")

# Column headers we care about, normalised.
HEADER_ALIASES = {
    "course #": "code",
    "course number": "code",
    "course": "code",
    "number": "code",
    "course title": "title",
    "title": "title",
    "credit hours": "credits",
    "credits": "credits",
    "credit": "credits",
    "hours": "credits",
}


class Extractor:
    def __init__(self, delay=1.0):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.delay = delay

    def get(self, url, timeout=15):
        response = self.session.get(url, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        time.sleep(self.delay)  # be polite to the hosts
        return response

    def matching_links(self, url, hints):
        """Same-host links whose text or href contains one of the hints."""
        try:
            response = self.get(url)
        except requests.RequestException:
            return {}

        soup = BeautifulSoup(response.content, "html.parser")
        host = urlparse(response.url).netloc
        found = {}

        for anchor in soup.find_all("a", href=True):
            text = (anchor.get_text(strip=True) or "").lower()
            haystack = f"{text} {anchor['href'].lower()}"

            if not any(hint in haystack for hint in hints):
                continue

            absolute = urljoin(response.url, anchor["href"])
            if urlparse(absolute).netloc != host:
                continue

            found[absolute] = anchor.get_text(strip=True)

        return found

    def find_curriculum_pages(self, seed_url):
        """
        Curriculum pages, searching two levels deep.

        Most schools do not link their curriculum from the home page — it sits
        behind "Academics" or "Doctor of Optometry". Searching only the home
        page found nothing for 13 of 24 schools.
        """
        direct = self.matching_links(seed_url, CURRICULUM_HINTS)

        # A page that literally says "curriculum" is the best bet.
        ranked = sorted(direct, key=lambda u: 0 if "curricul" in u.lower() else 1)
        if any("curricul" in u.lower() for u in ranked):
            return ranked[:4]

        # Otherwise step through the section pages looking for one.
        deeper = {}
        sections = self.matching_links(seed_url, SECTION_HINTS)

        for section in list(sections)[:6]:
            deeper.update(self.matching_links(section, CURRICULUM_HINTS))
            if any("curricul" in u.lower() for u in deeper):
                break

        combined = list(dict.fromkeys(list(deeper) + ranked))
        return sorted(combined, key=lambda u: 0 if "curricul" in u.lower() else 1)[:4]

    def parse_course_tables(self, url):
        """Pull course rows out of every table on a page."""
        try:
            response = self.get(url)
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        courses = []

        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            if len(rows) < 2:
                continue

            # Map the header row onto known column names.
            header_cells = [
                c.get_text(" ", strip=True).lower()
                for c in rows[0].find_all(["th", "td"])
            ]
            columns = {}
            for index, cell in enumerate(header_cells):
                if cell in HEADER_ALIASES:
                    columns[HEADER_ALIASES[cell]] = index

            if "code" not in columns or "title" not in columns:
                continue

            heading = table.find_previous(["h2", "h3", "h4"])
            term = heading.get_text(strip=True) if heading else None

            for row in rows[1:]:
                cells = [c.get_text(" ", strip=True) for c in row.find_all(["td", "th"])]
                if len(cells) <= max(columns.values()):
                    continue

                code = cells[columns["code"]].strip()
                title = cells[columns["title"]].strip()

                if not COURSE_CODE.match(code) or not title:
                    continue

                course = {"code": code, "title": title, "term": term}

                if "credits" in columns:
                    credits = cells[columns["credits"]].strip()
                    if credits and credits not in {"-", "–"}:
                        course["credits"] = credits

                courses.append(course)

        return courses

    def extract_school(self, school):
        """Everything published by one school, plus how it went."""
        record = {
            "school": school["name"],
            "state": school.get("state"),
            "url": school["url"],
            "curriculum_pages": [],
            "courses": [],
            "status": "no_courses_found",
        }

        try:
            pages = self.find_curriculum_pages(school["url"])
        except Exception as exc:
            record["status"] = f"error: {type(exc).__name__}"
            return record

        if not pages:
            record["status"] = "no_curriculum_page_found"
            return record

        seen = set()
        for page in pages:
            for course in self.parse_course_tables(page):
                key = (course["code"], course["title"])
                if key in seen:
                    continue
                seen.add(key)
                course["source_url"] = page
                record["courses"].append(course)

            record["curriculum_pages"].append(page)

        if record["courses"]:
            record["status"] = "ok"

        return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="only process the first N schools")
    parser.add_argument("--out", default=DEFAULT_OUT, help="where to write the JSON")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="seconds to pause between requests")
    args = parser.parse_args()

    import scrape_asco

    try:
        schools = scrape_asco.parse(scrape_asco.fetch())
    except Exception as exc:
        print(f"Could not load the ASCO directory: {exc}", file=sys.stderr)
        return 1

    if args.limit:
        schools = schools[:args.limit]

    extractor = Extractor(delay=args.delay)
    records = []

    print(f"Extracting curricula from {len(schools)} schools\n")

    for index, school in enumerate(schools, 1):
        print(f"[{index}/{len(schools)}] {school['name'][:50]}", flush=True)
        record = extractor.extract_school(school)
        records.append(record)
        print(f"    {record['status']}  courses: {len(record['courses'])}", flush=True)

    total_courses = sum(len(r["courses"]) for r in records)
    with_data = [r for r in records if r["courses"]]

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "extracted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "ASCO member directory -> each school's own curriculum page",
                "schools_attempted": len(records),
                "schools_with_courses": len(with_data),
                "total_courses": total_courses,
                "schools": records,
            },
            handle,
            indent=2,
        )

    print("\n" + "=" * 60)
    print(f"schools attempted:    {len(records)}")
    print(f"schools with courses: {len(with_data)}")
    print(f"courses extracted:    {total_courses}")
    print(f"written to:           {args.out}")

    if len(with_data) < len(records):
        print("\nNo courses from these (JS-rendered, PDF-only, or prose):")
        for record in records:
            if not record["courses"]:
                print(f"  - {record['school']}  [{record['status']}]")

    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
