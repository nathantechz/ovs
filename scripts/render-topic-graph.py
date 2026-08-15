#!/usr/bin/env python3
"""
Render data/topic-graph.json as a self-contained page.

The graph answers one question: which courses teach the same material under
different names? Each subject is drawn as a cluster with the courses that map
to it grouped by institution, so an overlap is visible at a glance.

The data is inlined rather than fetched, so the page works from the filesystem
as well as over HTTP.

Usage:
    .venv/bin/python scripts/render-topic-graph.py
"""

import html
import json
import os
import sys
from collections import defaultdict

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(PROJECT_DIR, "data", "topic-graph.json")
OUTPUT = os.path.join(PROJECT_DIR, "curriculum-map.html")

GROUP_LABELS = {
    "optics": "Optics",
    "foundations": "Basic & Vision Science",
    "clinical": "Clinical Practice",
    "disease": "Ocular & Systemic Disease",
    "populations": "Patient Populations",
    "professional": "Professional Practice",
}

SITE_SOURCE = "Optometry Learning Hub"


def build_page(graph):
    subjects = [n for n in graph["nodes"] if n["type"] == "subject"]
    courses = {n["id"]: n for n in graph["nodes"] if n["type"] == "course"}

    # subject -> source -> [course nodes]
    by_subject = defaultdict(lambda: defaultdict(list))
    for edge in graph["edges"]:
        slug = edge["to"].split(":", 1)[1]
        course = courses.get(edge["from"])
        if course:
            by_subject[slug][course["source"]].append(course)

    sources = sorted({c["source"] for c in courses.values()})
    counts = graph["counts"]

    cards = []
    for group in GROUP_LABELS:
        group_subjects = [
            s for s in subjects
            if s["group"] == group and by_subject.get(s["id"].split(":", 1)[1])
        ]
        if not group_subjects:
            continue

        group_subjects.sort(key=lambda s: -s["courseCount"])
        items = []

        for subject in group_subjects:
            slug = subject["id"].split(":", 1)[1]
            per_source = by_subject[slug]
            shared = len(per_source) > 1

            columns = []
            for source in sorted(per_source):
                entries = per_source[source]
                seen = set()
                lines = []
                for course in sorted(entries, key=lambda c: c["label"]):
                    if course["label"] in seen:
                        continue
                    seen.add(course["label"])

                    code = course.get("code")
                    label = html.escape(course["label"])
                    if course.get("href"):
                        lines.append(
                            f'<li><a href="index.html{course["href"]}">{label}</a></li>'
                        )
                    else:
                        prefix = f'<span class="code">{html.escape(code)}</span> ' if code else ""
                        lines.append(f"<li>{prefix}{label}</li>")

                is_site = source == SITE_SOURCE
                columns.append(f"""
                <div class="src{' src-site' if is_site else ''}">
                    <h4>{html.escape(source)}<span>{len(seen)}</span></h4>
                    <ul>{''.join(lines)}</ul>
                </div>""")

            items.append(f"""
            <article class="subject" data-sources="{len(per_source)}" data-label="{html.escape(subject['label'].lower())}">
                <header>
                    <h3>{html.escape(subject['label'])}</h3>
                    <div class="tags">
                        {'<span class="tag shared">Taught at ' + str(len(per_source)) + ' institutions</span>' if shared else '<span class="tag">Single source</span>'}
                        <span class="tag count">{subject['courseCount']} courses</span>
                    </div>
                </header>
                <div class="sources">{''.join(columns)}</div>
            </article>""")

        cards.append(f"""
        <section class="group">
            <h2>{GROUP_LABELS[group]}</h2>
            <div class="subjects">{''.join(items)}</div>
        </section>""")

    generated = graph.get("generated_from", {}).get("extracted_at", "unknown")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Curriculum Map — Optometry Learning Hub</title>
<link rel="stylesheet" href="notes/notes.css">
<style>
.map-head {{ max-width: 1100px; margin: 0 auto; padding: 36px 24px 8px; }}
.map-wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 24px 80px; }}
.lede {{ color: var(--text-muted); font-size: 17px; max-width: 70ch; }}
.stats {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 22px 0 8px; }}
.stat {{ background: var(--surface); border: 1px solid var(--border);
        border-radius: 8px; padding: 10px 16px; }}
.stat b {{ display: block; font-size: 21px; color: var(--primary); }}
.stat span {{ font-size: 12.5px; color: var(--text-muted); }}
.controls {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0 6px;
             position: sticky; top: 0; background: var(--bg); padding: 12px 0;
             z-index: 5; border-bottom: 1px solid var(--border); }}
.controls input {{ flex: 1; min-width: 200px; padding: 10px 14px; font-size: 15px;
                   border: 1px solid var(--border); border-radius: 8px;
                   background: var(--bg); color: var(--text); }}
.controls button {{ padding: 10px 16px; border-radius: 8px; cursor: pointer;
                    border: 1px solid var(--border); background: var(--bg);
                    color: var(--text); font: inherit; }}
.controls button.on {{ background: var(--primary); color: #fff; border-color: var(--primary); }}
.group {{ margin-top: 40px; }}
.group > h2 {{ font-size: 15px; text-transform: uppercase; letter-spacing: .07em;
               color: var(--text-muted); border: none; padding: 0; margin-bottom: 14px; }}
.subjects {{ display: grid; gap: 16px; }}
.subject {{ border: 1px solid var(--border); border-radius: 12px;
            padding: 18px 20px; background: var(--surface); }}
.subject > header {{ display: flex; flex-wrap: wrap; gap: 10px;
                     justify-content: space-between; align-items: baseline;
                     margin-bottom: 14px; }}
.subject h3 {{ margin: 0; font-size: 18px; }}
.tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.tag {{ font-size: 11.5px; font-weight: 600; padding: 3px 10px; border-radius: 999px;
        background: var(--bg); border: 1px solid var(--border); color: var(--text-muted); }}
.tag.shared {{ background: #e8f8f0; border-color: #00a854; color: #00794a; }}
.sources {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(215px, 1fr)); gap: 14px; }}
.src {{ background: var(--bg); border: 1px solid var(--border);
        border-radius: 8px; padding: 12px 14px; }}
.src-site {{ border-color: var(--primary); }}
.src h4 {{ margin: 0 0 8px; font-size: 12.5px; color: var(--text-muted);
           display: flex; justify-content: space-between; gap: 8px; font-weight: 600; }}
.src-site h4 {{ color: var(--primary); }}
.src ul {{ margin: 0; padding-left: 16px; }}
.src li {{ font-size: 14px; margin-bottom: 5px; }}
.src a {{ color: var(--primary); text-decoration: none; }}
.src a:hover {{ text-decoration: underline; }}
.code {{ font-family: ui-monospace, Menlo, monospace; font-size: 12px;
         color: var(--text-muted); }}
.subject.hidden {{ display: none; }}
.group.hidden {{ display: none; }}
@media (prefers-color-scheme: dark) {{
  .tag.shared {{ background: #10251c; color: #4ade80; }}
}}
</style>
</head>
<body>

<nav class="note-nav">
    <div class="note-nav-inner">
        <a class="note-return" href="index.html#/">&larr; Optometry Learning Hub</a>
        <span class="course-tag">Curriculum Map</span>
    </div>
</nav>

<div class="map-head">
    <div class="note-eyebrow">Cross-institution</div>
    <h1>Curriculum Map</h1>
    <p class="lede">
        Schools teach the same material under different names. Southern College calls it
        <em>Optics of the Eye</em>, MCPHS calls it <em>Visual Optics</em>, this site calls it
        <em>Physical Optics</em>. Each card below is one subject, with every course that
        teaches it grouped by institution — so equivalents line up side by side.
    </p>

    <div class="stats">
        <div class="stat"><b>{counts['subjects']}</b><span>subjects</span></div>
        <div class="stat"><b>{counts['courses']}</b><span>courses</span></div>
        <div class="stat"><b>{counts['sharedSubjects']}</b><span>taught at 2+ institutions</span></div>
        <div class="stat"><b>{len(sources)}</b><span>sources</span></div>
    </div>
</div>

<div class="map-wrap">
    <div class="controls">
        <input id="q" type="search" placeholder="Filter subjects and courses…" aria-label="Filter">
        <button id="sharedOnly" type="button">Only shared subjects</button>
    </div>

    {''.join(cards)}

    <p class="lede" style="margin-top:40px; font-size:14px;">
        Built from {counts['courses']} courses across {len(sources)} sources.
        {counts['unmapped']} courses matched no subject and are excluded rather than
        forced into a category. Curricula scraped {html.escape(str(generated))}.
    </p>
</div>

<script>
(function () {{
    const q = document.getElementById('q');
    const sharedBtn = document.getElementById('sharedOnly');
    const subjects = [...document.querySelectorAll('.subject')];
    let sharedOnly = false;

    function apply() {{
        const term = q.value.trim().toLowerCase();

        subjects.forEach(function (el) {{
            const matchesTerm = !term || el.textContent.toLowerCase().includes(term);
            const matchesShared = !sharedOnly || Number(el.dataset.sources) > 1;
            el.classList.toggle('hidden', !(matchesTerm && matchesShared));
        }});

        // Hide a group heading when everything under it is filtered out.
        document.querySelectorAll('.group').forEach(function (group) {{
            const anyVisible = group.querySelector('.subject:not(.hidden)');
            group.classList.toggle('hidden', !anyVisible);
        }});
    }}

    q.addEventListener('input', apply);
    sharedBtn.addEventListener('click', function () {{
        sharedOnly = !sharedOnly;
        sharedBtn.classList.toggle('on', sharedOnly);
        apply();
    }});
}})();
</script>

</body>
</html>
"""


def main():
    if not os.path.exists(GRAPH):
        print(f"Missing {GRAPH}. Run scripts/build-topic-graph.py first.",
              file=sys.stderr)
        return 1

    graph = json.load(open(GRAPH, encoding="utf-8"))
    open(OUTPUT, "w", encoding="utf-8").write(build_page(graph))

    print(f"Wrote {OUTPUT}")
    print(f"  subjects: {graph['counts']['subjects']}")
    print(f"  courses:  {graph['counts']['courses']}")
    print(f"  shared:   {graph['counts']['sharedSubjects']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
