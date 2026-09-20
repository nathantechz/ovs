#!/usr/bin/env python3
"""
Render the University of Bisha diploma notes from authored content.

Content lives in scripts/ub_notes_content.py as structured data — sections,
citations, tables, figures — and this turns it into the HTML pages under
notes/ub-diploma/, plus a course index.

Keeping the two apart means a citation can be corrected in one place, the
house style can change without touching 57 files, and the whole set can be
rebuilt after the textbook wiki is re-extracted.

Every page carries:
  * the WCO competency category the topic sits in
  * inline citations to book, edition and printed page
  * an illustration (drawn as SVG, never a lifted textbook photograph)
  * a current-practice section where the textbook is behind
  * a source list

Usage:
    .venv/bin/python scripts/build-ub-notes.py
    .venv/bin/python scripts/build-ub-notes.py --course "Ocular Diseases"
"""

import argparse
import html
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(PROJECT_DIR, "notes", "ub-diploma")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ub_notes_content import COURSES
except ImportError as exc:
    print(f"Cannot load ub_notes_content.py: {exc}", file=sys.stderr)
    raise SystemExit(1)


def esc(text):
    return html.escape(str(text), quote=False)


def render_block(block):
    """One content block -> HTML."""
    kind = block.get("type", "prose")

    if kind == "prose":
        cite = f' <span class="cite">{esc(block["cite"])}</span>' if block.get("cite") else ""
        return f"<p>{block['text']}{cite}</p>"

    if kind == "list":
        items = "".join(f"<li>{item}</li>" for item in block["items"])
        source = f'<p class="source">{esc(block["source"])}</p>' if block.get("source") else ""
        intro = f"<p>{block['intro']}</p>" if block.get("intro") else ""
        return f"{intro}<ul>{items}</ul>{source}"

    if kind == "steps":
        items = "".join(f"<li>{item}</li>" for item in block["items"])
        source = f'<p class="source">{esc(block["source"])}</p>' if block.get("source") else ""
        intro = f"<p>{block['intro']}</p>" if block.get("intro") else ""
        return f"{intro}<ol class='procedure'>{items}</ol>{source}"

    if kind == "table":
        head = "".join(f"<th>{h}</th>" for h in block["headers"])
        rows = "".join(
            "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
            for row in block["rows"]
        )
        source = f'<p class="source">{esc(block["source"])}</p>' if block.get("source") else ""
        return (f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead>'
                f"<tbody>{rows}</tbody></table>{source}</div>")

    if kind == "callout":
        variant = block.get("variant", "")
        title = f'<span class="callout-title">{esc(block["title"])}</span>' if block.get("title") else ""
        return f'<div class="callout {variant}">{title}{block["text"]}</div>'

    if kind == "figure":
        caption = f'<figcaption>{block["caption"]}</figcaption>' if block.get("caption") else ""
        return f'<figure>{block["svg"]}{caption}</figure>'

    if kind == "equation":
        where = f'<span class="where">{block["where"]}</span>' if block.get("where") else ""
        return f'<span class="eq">{block["text"]}{where}</span>'

    raise ValueError(f"unknown block type: {kind}")


def render_section(section):
    parts = [f"<h2>{esc(section['heading'])}</h2>"]

    for block in section["blocks"]:
        if block.get("type") == "subheading":
            parts.append(f"<h3>{esc(block['text'])}</h3>")
        else:
            parts.append(render_block(block))

    return "\n".join(parts)


def render_note(course, topic, index, total, prev_topic, next_topic):
    sections = "\n\n".join(render_section(s) for s in topic["sections"])

    checklist = ""
    if topic.get("check"):
        items = "".join(f"<li>{q}</li>" for q in topic["check"])
        checklist = (f'<div class="checklist"><h2>Check yourself</h2>'
                     f"<ul>{items}</ul></div>")

    sources = ""
    if topic.get("sources"):
        items = "".join(f"<li>{s}</li>" for s in topic["sources"])
        sources = (f'<section class="note-sources"><h2>Sources</h2>'
                   f"<ol>{items}</ol></section>")

    nav_next = (f'<a href="{next_topic["slug"]}.html">Next: '
                f'{esc(next_topic["title"])} &rarr;</a>') if next_topic else \
               '<a href="index.html">Back to course index</a>'

    hours = f' &middot; {topic["hours"]} contact hours' if topic.get("hours") else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(topic['title'])} — {esc(course['name'])}</title>
<link rel="stylesheet" href="../../notes.css">
</head>
<body>

<nav class="note-nav">
    <div class="note-nav-inner">
        <a class="note-return" href="index.html">&larr; {esc(course['name'])}</a>
        <span class="course-tag">Topic {index} of {total}{hours}</span>
    </div>
</nav>

<main>

<header class="note-header">
    <div class="note-eyebrow">University of Bisha &middot; Diploma in Optometry (2 years)</div>
    <h1>{esc(topic['title'])}</h1>
    <p class="note-summary">{topic['summary']}</p>
</header>

<div class="callout wco">
    <span class="callout-title">WCO competency mapping</span>
    {topic['wco']}
</div>

{sections}

{checklist}

{sources}

<footer class="note-footer">
    <span>{esc(course['name'])} &middot; Topic {index} of {total}</span>
    {nav_next}
</footer>

</main>
</body>
</html>
"""


def render_course_index(course, courses):
    rows = []
    for number, topic in enumerate(course["topics"], 1):
        hours = f"{topic['hours']} h" if topic.get("hours") else "—"
        # "external" topics were authored as their own file and are linked but
        # not regenerated, so hand-written pages are never overwritten.
        linkable = bool(topic.get("sections") or topic.get("external"))
        badge = "" if linkable else ' <span class="pending">outline only</span>'
        link = (f'<a href="{topic["slug"]}.html">{esc(topic["title"])}</a>'
                if linkable else esc(topic["title"]))
        rows.append(f"<tr><td>{number}</td><td>{link}{badge}</td><td>{hours}</td></tr>")

    others = "".join(
        f'<li><a href="../{c["slug"]}/index.html">{esc(c["name"])}</a></li>'
        for c in courses if c["slug"] != course["slug"]
    )

    ready = sum(1 for t in course["topics"]
                if t.get("sections") or t.get("external"))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(course['name'])} — University of Bisha Diploma</title>
<link rel="stylesheet" href="../../notes.css">
</head>
<body>

<nav class="note-nav">
    <div class="note-nav-inner">
        <a class="note-return" href="../../../index.html#/">&larr; Optometry Learning Hub</a>
        <span class="course-tag">University of Bisha &middot; Diploma</span>
    </div>
</nav>

<main>

<header class="note-header">
    <div class="note-eyebrow">Diploma in Optometry (2 years)</div>
    <h1>{esc(course['name'])}</h1>
    <p class="note-summary">{course['summary']}</p>
</header>

<div class="callout wco">
    <span class="callout-title">WCO competency scope</span>
    {course['wco']}
</div>

<h2>Topics ({ready} of {len(course['topics'])} written)</h2>

<div class="table-wrap">
<table>
    <thead><tr><th>#</th><th>Topic</th><th>Hours</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
</table>
</div>

<h2>Grounding</h2>
<p>{course['grounding']}</p>

<h2>Other courses on this programme</h2>
<ul>{others}</ul>

</main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--course", help="build only this course")
    args = parser.parse_args()

    built = 0
    for course in COURSES:
        if args.course and args.course.lower() not in course["name"].lower():
            continue

        course_dir = os.path.join(OUT_DIR, course["slug"])
        os.makedirs(course_dir, exist_ok=True)

        written = [t for t in course["topics"]
                   if t.get("sections") or t.get("external")]
        total = len(course["topics"])

        for number, topic in enumerate(course["topics"], 1):
            if not topic.get("sections"):
                continue

            following = next(
                (t for t in course["topics"][number:]
                 if t.get("sections") or t.get("external")), None)
            preceding = next(
                (t for t in reversed(course["topics"][:number - 1])
                 if t.get("sections") or t.get("external")), None)

            page = render_note(course, topic, number, total, preceding, following)
            path = os.path.join(course_dir, topic["slug"] + ".html")
            open(path, "w", encoding="utf-8").write(page)
            built += 1

        index_path = os.path.join(course_dir, "index.html")
        open(index_path, "w", encoding="utf-8").write(
            render_course_index(course, COURSES))

        print(f"{course['name']}: {len(written)}/{total} topics -> {course_dir}")

    print(f"\n{built} note pages written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
