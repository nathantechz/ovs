#!/usr/bin/env python3
"""
Regenerate js/universities-regional.js.

Two kinds of data go into that file and they are labelled differently, because
they are not equally trustworthy:

  * SCRAPED  — fetched and parsed from a live directory on every run.
               Currently the ASCO member list, which covers US programmes.
  * CURATED  — maintained by hand in this file. Everything else.

Earlier versions of this script claimed to scrape every accreditor but actually
returned hardcoded lists for all of them. They do not any more: if the ASCO
fetch or parse fails, this exits non-zero and leaves the existing file alone
rather than silently writing curated data under a "scraped" banner.

Usage:
    .venv/bin/python scripts/update-universities.py
    .venv/bin/python scripts/update-universities.py --curated-only

Setup:
    python3 -m venv .venv
    .venv/bin/pip install requests beautifulsoup4 lxml

Weekly refresh (Sunday 02:00):
    0 2 * * 0 cd /path/to/ovs && .venv/bin/python scripts/update-universities.py
"""

import argparse
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_FILE = os.path.join(PROJECT_DIR, "js", "universities-regional.js")

sys.path.insert(0, SCRIPT_DIR)

# Region and country scaffolding. Countries with no entries yet are kept so the
# structure of the directory stays visible.
REGIONS = {
    "North America": {
        "icon": "fa-map-marker-alt",
        "description": "Optometry schools across USA and Canada",
        "countries": ["USA", "Canada"],
    },
    "Europe": {
        "icon": "fa-map-marker-alt",
        "description": "Optometry programs across Europe",
        "countries": ["United Kingdom", "Spain", "France", "Germany",
                      "Netherlands", "Belgium"],
    },
    "Asia-Pacific": {
        "icon": "fa-map-marker-alt",
        "description": "Optometry programs across Asia and Oceania",
        "countries": ["India", "Australia", "New Zealand", "China", "Japan",
                      "South Korea", "Thailand", "Singapore"],
    },
    "South America": {
        "icon": "fa-map-marker-alt",
        "description": "Optometry programs across South America",
        "countries": ["Brazil", "Argentina", "Colombia", "Chile"],
    },
    "Africa": {
        "icon": "fa-map-marker-alt",
        "description": "Optometry programs across Africa",
        "countries": ["South Africa", "Nigeria", "Kenya"],
    },
    "Middle East": {
        "icon": "fa-map-marker-alt",
        "description": "Optometry programs in Middle East",
        "countries": ["Saudi Arabia", "United Arab Emirates", "Iran"],
    },
}

# Hand-maintained. Every entry carries source: "curated" so the front end and
# any reader can tell it apart from scraped data.
CURATED = {
    "Canada": [
        ("University of Waterloo School of Optometry", "Waterloo", "O.D.", "Doctor of Optometry", "4 years", "ACOE"),
        ("Université de Montréal École d'optométrie", "Montreal", "O.D.", "Doctor of Optometry", "5 years", "ACOE"),
    ],
    "United Kingdom": [
        ("University of Manchester", "Manchester", "BSc", "BSc Optometry", "3 years", "GOC"),
        ("City, University of London", "London", "BSc", "BSc Optometry", "3 years", "GOC"),
        ("University of Plymouth", "Plymouth", "BSc", "BSc Optometry", "3 years", "GOC"),
        ("University of Bradford", "Bradford", "BSc", "BSc Optometry", "3 years", "GOC"),
        ("Aston University", "Birmingham", "MOptom", "Optometry", "4 years", "GOC"),
        ("Cardiff University", "Cardiff", "BSc", "BSc Optometry", "3 years", "GOC"),
        ("Glasgow Caledonian University", "Glasgow", "BSc", "BSc Optometry", "4 years", "GOC"),
        ("University of Hertfordshire", "Hatfield", "BSc", "BSc Optometry", "3 years", "GOC"),
        ("Ulster University", "Coleraine", "BSc", "BSc Optometry", "3 years", "GOC"),
    ],
    "India": [
        ("Manipal Academy of Higher Education", "Manipal", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("VIT Vellore", "Vellore", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("Aravind Eye Care Academy", "Madurai", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("Dr. M.G.R. Educational and Research Institute", "Chennai", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("Alagappa University", "Karaikudi", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("SRM Institute of Science and Technology", "Chennai", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("Amrita Vishwa Vidyapeetham", "Coimbatore", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("Chitkara University", "Patiala", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("Elite School of Optometry", "Chennai", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("LV Prasad Eye Institute (Bausch & Lomb School of Optometry)", "Hyderabad", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
        ("All India Institute of Medical Sciences (AIIMS)", "New Delhi", "B.Optom", "Bachelor of Optometry", "4 years", "State"),
    ],
    "Australia": [
        ("University of Melbourne", "Melbourne", "OD", "Doctor of Optometry", "4 years", "OCANZ"),
        ("UNSW Sydney", "Sydney", "BOptom/MClinOptom", "Optometry", "5 years", "OCANZ"),
        ("Queensland University of Technology", "Brisbane", "BVisSc/MOptom", "Optometry", "5 years", "OCANZ"),
        ("Flinders University", "Adelaide", "BMedSc/MOptom", "Optometry", "5 years", "OCANZ"),
        ("Deakin University", "Geelong", "BVisSc/MOptom", "Optometry", "3.5 years", "OCANZ"),
    ],
    "New Zealand": [
        ("University of Auckland", "Auckland", "BOptom", "Bachelor of Optometry", "5 years", "OCANZ"),
    ],
    "South Africa": [
        ("University of KwaZulu-Natal", "Durban", "BOptom", "Bachelor of Optometry", "4 years", "HPCSA"),
        ("University of Johannesburg", "Johannesburg", "BOptom", "Bachelor of Optometry", "4 years", "HPCSA"),
        ("University of the Free State", "Bloemfontein", "BOptom", "Bachelor of Optometry", "4 years", "HPCSA"),
        ("University of Limpopo", "Polokwane", "BOptom", "Bachelor of Optometry", "4 years", "HPCSA"),
    ],
}


def curated_records(country):
    """Expand the terse CURATED tuples into full records."""
    records = []

    for name, city, degree, program, duration, accreditation in CURATED.get(country, []):
        records.append({
            "name": name,
            "city": city,
            "country": country,
            "degree": degree,
            "program": program,
            "duration": duration,
            "accreditation": accreditation,
            "source": "curated",
        })

    return records


def scraped_usa():
    """Live ASCO parse. Raises if it cannot produce a full list."""
    import scrape_asco

    schools = scrape_asco.parse(scrape_asco.fetch())

    if len(schools) < 15:
        raise RuntimeError(
            f"ASCO parse produced only {len(schools)} schools; layout has likely changed"
        )

    records = []
    for school in schools:
        records.append({
            "name": school["name"],
            "city": school["city"] or "",
            "state": school["state"],
            "country": "USA",
            "degree": "O.D.",
            "program": "Doctor of Optometry",
            "duration": "4 years",
            "accreditation": "ACOE",
            "url": school["url"],
            "source": "scraped:ASCO",
        })

    return records


def build(curated_only=False):
    data = {}
    scraped_count = 0

    for region, meta in REGIONS.items():
        countries = {}

        for country in meta["countries"]:
            if country == "USA" and not curated_only:
                countries[country] = scraped_usa()
                scraped_count += len(countries[country])
            else:
                countries[country] = curated_records(country)

        data[region] = {
            "region": region,
            "icon": meta["icon"],
            "description": meta["description"],
            "countries": countries,
        }

    return data, scraped_count


def render_js(data, scraped_count, total):
    generated = datetime.now()

    header = (
        "// Global Optometry Universities Database - Organized by Region\n"
        f"// Generated: {generated.strftime('%Y-%m-%d %H:%M:%S')} "
        "by scripts/update-universities.py\n"
        "//\n"
        f"// {scraped_count} entries scraped live from the ASCO member directory\n"
        f"// {total - scraped_count} entries are hand-curated (source: \"curated\")\n"
        "// Every record carries a `source` field saying which it is.\n"
        f"// Total: {total}\n\n"
    )

    body = "const universitiesByRegion = " + json.dumps(data, indent=4) + ";\n"

    footer = """
// Get all universities
function getAllUniversities() {
    const all = [];
    for (const region of Object.values(universitiesByRegion)) {
        for (const countries of Object.values(region.countries)) {
            all.push(...countries);
        }
    }
    return all;
}

// Get universities by region
function getUniversitiesByRegion(regionName) {
    return universitiesByRegion[regionName]?.countries || {};
}

// Get all regions
function getAllRegions() {
    return Object.keys(universitiesByRegion);
}

// Get region info
function getRegionInfo(regionName) {
    return universitiesByRegion[regionName] || null;
}

// Count total universities
function getTotalUniversitiesCount() {
    return getAllUniversities().length;
}

// Last updated timestamp
const lastUpdated = "%s";
""" % generated.isoformat()

    return header + body + footer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--curated-only",
        action="store_true",
        help="skip the network fetch and emit only hand-maintained data",
    )
    args = parser.parse_args()

    try:
        data, scraped_count = build(curated_only=args.curated_only)
    except Exception as exc:
        print(f"Update aborted: {exc}", file=sys.stderr)
        print(f"{OUTPUT_FILE} left unchanged.", file=sys.stderr)
        return 1

    total = sum(
        len(unis)
        for region in data.values()
        for unis in region["countries"].values()
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as handle:
        handle.write(render_js(data, scraped_count, total))

    print(f"Wrote {OUTPUT_FILE}")
    print(f"  scraped (ASCO): {scraped_count}")
    print(f"  curated:        {total - scraped_count}")
    print(f"  total:          {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
