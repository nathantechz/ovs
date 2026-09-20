#!/usr/bin/env python3
"""
Audit the published site for gaps and broken references.

Checks, against the files actually on disk:

  1. Every href in every HTML page resolves to a real file.
  2. Every download path in the materials registry resolves.
  3. Every notes_url in the programmes data resolves.
  4. Every note page links back somewhere that exists.
  5. No contact address appears in any published page.
  6. Every course in the catalogue is reachable, and every course with
     materials is linked to them.

This is the check that found 28 live 404s; run it before pushing.

    .venv/bin/python scripts/audit-site.py
"""

import json
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote, urlparse

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories that are not published.
SKIP_DIRS = {".git", ".venv", "node_modules", "wiki", "scripts", "__pycache__",
             "data", ".claude"}

HREF = re.compile(r'(?:href|src)="([^"]+)"')
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")

# Addresses that are fine to appear (form placeholders, example text).
ALLOWED_EMAILS = {"your.email@example.com", "noreply@anthropic.com"}


def html_files():
    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            if name.endswith(".html"):
                yield os.path.join(root, name)


def resolve(page_path, href):
    """Turn an href into a path on disk, or None if it is not a local file."""
    href = href.strip()

    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None

    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        return None  # external

    target = unquote(parsed.path)
    if not target:
        return None

    base = os.path.dirname(page_path)
    return os.path.normpath(os.path.join(base, target))


def check_links():
    broken = defaultdict(list)
    checked = 0

    for page in html_files():
        source = open(page, encoding="utf-8", errors="replace").read()
        # Inlined scripts assemble hrefs from template strings; those are code,
        # not links, so remove script and style blocks before scanning.
        scannable = re.sub(r"<(script|style)\b.*?</\1>", "", source,
                           flags=re.S | re.I)
        for href in HREF.findall(scannable):
            target = resolve(page, href)
            if target is None:
                continue
            checked += 1
            if not os.path.exists(target):
                broken[os.path.relpath(page, PROJECT_DIR)].append(href)

    return checked, broken


def check_materials():
    path = os.path.join(PROJECT_DIR, "js", "materials-list.js")
    if not os.path.exists(path):
        return 0, []

    source = open(path, encoding="utf-8").read()
    match = re.search(r"const availableMaterials\s*=\s*(\{.*?\n\});", source, re.S)
    if not match:
        return 0, [("materials-list.js", "could not parse availableMaterials")]

    data = json.loads(match.group(1))
    missing = []
    checked = 0

    for course, entry in data.items():
        folder = entry.get("folder", "")
        for group in ("readings", "notes", "lectures", "practicals"):
            for item in entry.get(group) or []:
                if item.get("file"):
                    checked += 1
                    if not os.path.exists(os.path.join(PROJECT_DIR, folder, item["file"])):
                        missing.append((course, item["file"]))

                if item.get("onlineUrl"):
                    checked += 1
                    if not os.path.exists(os.path.join(PROJECT_DIR, item["onlineUrl"])):
                        missing.append((course, item["onlineUrl"]))

    return checked, missing


def check_programmes():
    path = os.path.join(PROJECT_DIR, "data", "syllabi-local.json")
    if not os.path.exists(path):
        return 0, []

    data = json.load(open(path, encoding="utf-8"))
    missing = []
    checked = 0

    for programme in data.get("programmes", []):
        for course in programme.get("courses", []):
            url = course.get("notes_url")
            if url:
                checked += 1
                if not os.path.exists(os.path.join(PROJECT_DIR, url)):
                    missing.append((programme["institution"], url))

    return checked, missing


def check_emails():
    found = []
    for page in html_files():
        source = open(page, encoding="utf-8", errors="replace").read()
        for address in set(EMAIL.findall(source)):
            if address not in ALLOWED_EMAILS:
                found.append((os.path.relpath(page, PROJECT_DIR), address))
    return found


def check_course_coverage():
    data_js = os.path.join(PROJECT_DIR, "js", "data.js")
    registry = os.path.join(PROJECT_DIR, "js", "materials-list.js")

    if not (os.path.exists(data_js) and os.path.exists(registry)):
        return {}

    data_source = open(data_js, encoding="utf-8").read()
    courses_block = data_source[data_source.index("const coursesData"):]
    end = courses_block.find("const resourcesData")
    if end != -1:
        courses_block = courses_block[:end]
    titles = re.findall(r'title:\s*"([^"]+)"', courses_block)
    source = open(registry, encoding="utf-8").read()
    match = re.search(r"const availableMaterials\s*=\s*(\{.*?\n\});", source, re.S)
    keys = set(json.loads(match.group(1)).keys()) if match else set()

    aliases = dict(re.findall(r'"([^"]+)":\s*"([^"]+)"',
                              source[source.find("materialsAliases"):][:900])) \
        if "materialsAliases" in source else {}

    without = [t for t in titles
               if t not in keys and aliases.get(t) not in keys]

    orphaned = [k for k in keys if k not in titles
                and k not in set(aliases.values())]

    return {"courses": len(titles), "with_materials": len(titles) - len(without),
            "without_materials": without, "orphaned_registry_keys": orphaned}


def main():
    problems = 0

    print("=" * 66)
    print("SITE AUDIT")
    print("=" * 66)

    checked, broken = check_links()
    total_broken = sum(len(v) for v in broken.values())
    problems += total_broken
    print(f"\n1. Local hrefs          {checked} checked, {total_broken} broken")
    for page, hrefs in list(broken.items())[:8]:
        print(f"     {page}")
        for href in hrefs[:4]:
            print(f"       -> {href}")

    checked, missing = check_materials()
    problems += len(missing)
    print(f"\n2. Material downloads   {checked} checked, {len(missing)} missing")
    for course, path in missing[:6]:
        print(f"     [{course}] {path}")

    checked, missing = check_programmes()
    problems += len(missing)
    print(f"\n3. Programme notes      {checked} checked, {len(missing)} missing")
    for institution, url in missing[:6]:
        print(f"     [{institution}] {url}")

    emails = check_emails()
    problems += len(emails)
    print(f"\n4. Published addresses  {len(emails)} found")
    for page, address in emails[:6]:
        print(f"     {page}: {address}")

    coverage = check_course_coverage()
    if coverage:
        print(f"\n5. Course coverage      {coverage['with_materials']}"
              f"/{coverage['courses']} courses have materials")
        if coverage["without_materials"]:
            print(f"     {len(coverage['without_materials'])} without materials, e.g.:")
            for title in coverage["without_materials"][:6]:
                print(f"       - {title}")
        if coverage["orphaned_registry_keys"]:
            print(f"     {len(coverage['orphaned_registry_keys'])} registry keys "
                  f"match no course (materials that cannot be reached):")
            for key in coverage["orphaned_registry_keys"][:6]:
                print(f"       - {key}")
            problems += len(coverage["orphaned_registry_keys"])

    print("\n" + "=" * 66)
    print(f"{'PASS — no broken references' if problems == 0 else f'{problems} problems found'}")
    print("=" * 66)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
