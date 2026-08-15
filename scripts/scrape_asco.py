#!/usr/bin/env python3
"""
Parser for the ASCO (Association of Schools and Colleges of Optometry)
member directory.

Unlike the older scripts in this folder, this one really does fetch and parse
the live page. If the fetch or the parse fails it raises, rather than quietly
falling back to a hardcoded list — a silent fallback is what previously made a
hand-maintained list look like scraped data.

The page is laid out as a flat run of lines:

    Alabama                                  <- state heading
    UNIVERSITY OF ALABAMA AT BIRMINGHAM      <- school name, all caps
    School of Optometry                      <- division (optional)
    1716 University Boulevard                <- street (optional, repeatable)
    Birmingham, Alabama 35294-0010           <- city, state ZIP
    https://www.uab.edu/optometry            <- URL

so we walk the lines and start a new record at each all-caps name.
"""

import re
import sys

import requests
from bs4 import BeautifulSoup

ASCO_URL = "https://optometriceducation.org/about-asco/asco-member-schools-and-colleges/"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
)

US_STATES = {
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming",
    "Puerto Rico", "District of Columbia",
}

# "Birmingham, Alabama 35294-0010" / "San Juan, Puerto Rico 00919"
CITY_STATE_ZIP = re.compile(r"^(.+?),\s*([A-Za-z .]+?)\s+([\d]{5}(?:-\d{4})?)$")

# Words that stay lowercase inside a title-cased name.
SMALL_WORDS = {"of", "at", "the", "and", "in", "for", "de", "at"}


def title_case(name):
    """Title-case an ALL CAPS school name without capitalising particles."""
    words = name.split()
    out = []

    for i, word in enumerate(words):
        lowered = word.lower()

        # Keep recognised acronyms as-is.
        if word.isupper() and len(word) <= 5 and word.strip("()").isalpha() and len(word) > 1:
            if lowered.strip("()") in {"suny", "mcphs", "uab", "uiw"}:
                out.append(word)
                continue

        if i > 0 and lowered in SMALL_WORDS:
            out.append(lowered)
        else:
            out.append(word.capitalize() if word.isupper() else word.title())

    return " ".join(out)


def fetch(url=ASCO_URL, timeout=20):
    """Fetch the directory page. Raises on any non-200."""
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    response.raise_for_status()
    return response.content


def is_school_name(line):
    """School names are set in capitals; addresses and divisions are not."""
    letters = [c for c in line if c.isalpha()]
    if len(letters) < 8:
        return False
    if not all(c.isupper() for c in letters):
        return False
    return "OPTOMETRY" in line or "UNIVERSITY" in line or "COLLEGE" in line


def parse(html):
    """Turn the directory page into a list of school dicts."""
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("main") or soup

    # Non-breaking spaces appear inside several names.
    lines = [
        line.replace("\xa0", " ").strip()
        for line in root.get_text("\n", strip=True).split("\n")
        if line.strip()
    ]

    schools = []
    current = None
    state = None

    for line in lines:
        if line in US_STATES:
            state = line
            continue

        if is_school_name(line):
            if current:
                schools.append(current)
            current = {
                "name": title_case(line),
                "state": state,
                "division": None,
                "city": None,
                "url": None,
                "country": "USA",
                "degree": "O.D.",
                "program": "Doctor of Optometry",
                "accreditation": "ACOE",
                "source": "ASCO member directory",
            }
            continue

        if not current:
            continue

        if line.startswith("http"):
            current["url"] = line
            continue

        match = CITY_STATE_ZIP.match(line)
        if match:
            current["city"] = match.group(1).strip()
            continue

        # First non-address line after the name is the school/division.
        if current["division"] is None and not re.match(r"^\d", line):
            current["division"] = line

    if current:
        schools.append(current)

    # A record without a URL means the layout drifted; drop it rather than
    # emit something half-parsed.
    return [s for s in schools if s["url"] and s["state"]]


def main():
    try:
        html = fetch()
    except requests.RequestException as exc:
        print(f"ASCO fetch failed: {exc}", file=sys.stderr)
        return 1

    schools = parse(html)

    if len(schools) < 15:
        print(
            f"Only parsed {len(schools)} schools — the page layout has probably "
            "changed. Refusing to emit a partial list.",
            file=sys.stderr,
        )
        return 1

    for school in schools:
        print(f"{school['name']} — {school['city']}, {school['state']}")
    print(f"\n{len(schools)} schools parsed from the live ASCO directory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
