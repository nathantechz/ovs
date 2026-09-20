#!/usr/bin/env python3
"""
Repair download paths in js/materials-list.js that point at nothing.

Several registry entries name a file by its bare filename when it actually
sits one level down, in "Reading Notes/" or "Lecture Notes/". The page renders
the link happily and the student gets a 404 — 28 of them were live on the
published site.

For every entry whose path does not resolve, this searches the course folder
recursively for a file of that name and rewrites the path to the real
location. A file that genuinely is not there is reported and left alone, so a
missing file is never papered over with a wrong path.

    .venv/bin/python scripts/fix-material-paths.py --check   # report only
    .venv/bin/python scripts/fix-material-paths.py           # apply
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(PROJECT_DIR, "js", "materials-list.js")

GROUPS = ("readings", "notes", "lectures", "practicals")


def load_registry():
    source = open(REGISTRY, encoding="utf-8").read()
    match = re.search(r"const availableMaterials\s*=\s*(\{.*?\n\});", source, re.S)
    if not match:
        print("Could not find the availableMaterials object.", file=sys.stderr)
        raise SystemExit(1)
    return source, match, json.loads(match.group(1))


def index_folder(folder):
    """basename -> list of paths relative to the course folder."""
    found = {}
    if not os.path.isdir(folder):
        return found

    for root, _dirs, files in os.walk(folder):
        for name in files:
            relative = os.path.relpath(os.path.join(root, name), folder)
            found.setdefault(name, []).append(relative)

    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="report what would change without writing")
    args = parser.parse_args()

    source, match, data = load_registry()

    repairs = []
    unresolved = []

    for course, entry in data.items():
        folder = os.path.join(PROJECT_DIR, entry.get("folder", ""))
        by_name = index_folder(folder)

        for group in GROUPS:
            for item in entry.get(group) or []:
                path = item.get("file")
                if not path:
                    continue

                if os.path.exists(os.path.join(folder, path)):
                    continue

                candidates = by_name.get(os.path.basename(path), [])

                if len(candidates) == 1:
                    repairs.append((course, path, candidates[0]))
                elif len(candidates) > 1:
                    # Prefer the one whose folder matches the group name.
                    hint = {"readings": "Reading", "notes": "Lecture",
                            "lectures": "Lecture", "practicals": "Practical"}[group]
                    preferred = [c for c in candidates if hint.lower() in c.lower()]
                    chosen = preferred[0] if preferred else sorted(candidates)[0]
                    repairs.append((course, path, chosen))
                else:
                    unresolved.append((course, group, path))

    print(f"broken paths found:  {len(repairs) + len(unresolved)}")
    print(f"  repairable:        {len(repairs)}")
    print(f"  file truly absent: {len(unresolved)}")

    if repairs:
        print("\nBy course:")
        for course, count in Counter(c for c, _, _ in repairs).most_common():
            print(f"  {count:3}  {course}")
        print("\nExamples:")
        for course, old, new in repairs[:5]:
            print(f"  [{course}]\n    {old}\n    -> {new}")

    if unresolved:
        print(f"\nNo matching file anywhere in the course folder "
              f"({len(unresolved)}) — left unchanged:")
        for course, group, path in unresolved[:10]:
            print(f"  [{course}/{group}] {path}")

    if args.check or not repairs:
        return 0

    # Rewrite each broken path exactly once, matching the JSON string.
    updated = source
    applied = 0
    for _course, old, new in repairs:
        needle = json.dumps(old)
        replacement = json.dumps(new)
        if needle in updated:
            updated = updated.replace(needle, replacement, 1)
            applied += 1

    open(REGISTRY, "w", encoding="utf-8").write(updated)
    print(f"\nrewrote {applied} paths in {os.path.relpath(REGISTRY, PROJECT_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
