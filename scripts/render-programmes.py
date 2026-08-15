#!/usr/bin/env python3
"""
Render data/syllabi-local.json as a programme browser.

A reader arrives knowing what they are enrolled on — a two-year diploma, a
five-year bachelor, an OD, a taught masters — not which individual course they
want. So the page is driven by that: pick a programme, then a level, and see
exactly the courses and credit load for that stage.

Credit hours are a filter in their own right, since "what can I fit into this
semester" is a real question and every course here carries its credit count.

Data is inlined, so the page works offline and needs no fetch.

Usage:
    .venv/bin/python scripts/render-programmes.py
"""

import html
import json
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(PROJECT_DIR, "data", "syllabi-local.json")
OUTPUT = os.path.join(PROJECT_DIR, "programmes.html")

TYPE_LABELS = {
    "diploma": "Diploma",
    "bachelor": "Bachelor",
    "od": "Doctor of Optometry",
    "masters": "Masters",
}


def build(data):
    programmes = [p for p in data["programmes"] if p["courses"]]
    payload = json.dumps(programmes, ensure_ascii=False)

    options = "".join(
        f'<option value="{i}">{html.escape(p["programme"])}'
        f' — {html.escape(p["institution"])}</option>'
        for i, p in enumerate(programmes)
    )

    total_courses = sum(p["course_count"] for p in programmes)
    total_credits = sum(
        c.get("credits") or 0 for p in programmes for c in p["courses"]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Programmes &amp; Levels — Optometry Learning Hub</title>
<link rel="stylesheet" href="notes/notes.css">
<style>
.wrap {{ max-width: 1000px; margin: 0 auto; padding: 36px 24px 80px; }}
.lede {{ color: var(--text-muted); font-size: 17px; max-width: 68ch; }}
.pickers {{ display: grid; gap: 14px; margin: 26px 0 10px;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }}
.picker label {{ display: block; font-size: 12px; font-weight: 700;
                 text-transform: uppercase; letter-spacing: .06em;
                 color: var(--text-muted); margin-bottom: 6px; }}
.picker select {{ width: 100%; padding: 11px 13px; font: inherit; border-radius: 8px;
                  border: 1px solid var(--border); background: var(--bg); color: var(--text); }}
.levels {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 6px; }}
.lvl {{ padding: 8px 15px; border-radius: 999px; border: 1px solid var(--border);
        background: var(--bg); color: var(--text); font: inherit; font-size: 14px;
        cursor: pointer; }}
.lvl.on {{ background: var(--primary); border-color: var(--primary); color: #fff; }}
.summary {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0 6px; }}
.chip {{ background: var(--surface); border: 1px solid var(--border);
         border-radius: 8px; padding: 10px 16px; }}
.chip b {{ display: block; font-size: 20px; color: var(--primary); }}
.chip span {{ font-size: 12.5px; color: var(--text-muted); }}
.term {{ margin-top: 28px; }}
.term h2 {{ font-size: 15px; text-transform: uppercase; letter-spacing: .07em;
            color: var(--text-muted); border: none; padding: 0; margin-bottom: 12px; }}
table.courses {{ width: 100%; border-collapse: collapse; min-width: 0; }}
table.courses th {{ font-size: 12px; text-transform: uppercase; letter-spacing: .05em;
                    color: var(--text-muted); }}
table.courses td.code {{ font-family: ui-monospace, Menlo, monospace; font-size: 13px;
                         color: var(--text-muted); white-space: nowrap; }}
table.courses td.cr {{ text-align: right; white-space: nowrap; }}
.track {{ font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 999px;
          background: var(--surface); border: 1px solid var(--border);
          color: var(--text-muted); margin-left: 8px; }}
.track.research {{ background: #eef2ff; border-color: #6366f1; color: #4338ca; }}
.track.clinical {{ background: #e8f8f0; border-color: #00a854; color: #00794a; }}
.desc {{ font-size: 13.5px; color: var(--text-muted); margin-top: 4px; }}
.none {{ padding: 40px; text-align: center; color: var(--text-muted);
         border: 1px solid var(--border); border-radius: 10px; background: var(--surface); }}
@media (prefers-color-scheme: dark) {{
  .track.research {{ background:#1e1b4b; color:#a5b4fc; }}
  .track.clinical {{ background:#10251c; color:#4ade80; }}
}}
</style>
</head>
<body>

<nav class="note-nav">
    <div class="note-nav-inner">
        <a class="note-return" href="index.html#/">&larr; Optometry Learning Hub</a>
        <span class="course-tag">Programmes &amp; Levels</span>
    </div>
</nav>

<div class="wrap">
    <div class="note-eyebrow">Curricula</div>
    <h1>Programmes &amp; Levels</h1>
    <p class="lede">
        Choose the programme you are on and the level you have reached. The courses,
        their credit hours and the load for that stage are shown below, taken from each
        institution's own published handbook.
    </p>

    <div class="pickers">
        <div class="picker">
            <label for="prog">Programme</label>
            <select id="prog">{options}</select>
        </div>
        <div class="picker">
            <label for="credits">Credit hours</label>
            <select id="credits">
                <option value="">Any</option>
                <option value="1-2">1–2 credits</option>
                <option value="3-3">3 credits</option>
                <option value="4-99">4 or more</option>
            </select>
        </div>
        <div class="picker">
            <label for="track">Track</label>
            <select id="track">
                <option value="">All tracks</option>
                <option value="core">Core</option>
                <option value="clinical">Clinical</option>
                <option value="research">Research</option>
            </select>
        </div>
    </div>

    <div class="levels" id="levels"></div>
    <div class="summary" id="summary"></div>
    <div id="out"></div>

    <p class="lede" style="margin-top:40px; font-size:14px;">
        {total_courses} courses and {total_credits} credit hours across
        {len(programmes)} programmes, parsed from the handbook PDFs.
        Levels are taken from each institution's own course numbering.
    </p>
</div>

<script>
const PROGRAMMES = {payload};

const progSel = document.getElementById('prog');
const creditSel = document.getElementById('credits');
const trackSel = document.getElementById('track');
const levelsBox = document.getElementById('levels');
const summaryBox = document.getElementById('summary');
const out = document.getElementById('out');

let activeLevel = null;

function esc(s) {{
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {{
        return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c];
    }});
}}

function currentProgramme() {{
    return PROGRAMMES[Number(progSel.value)];
}}

function creditRange() {{
    if (!creditSel.value) return null;
    const parts = creditSel.value.split('-');
    return [Number(parts[0]), Number(parts[1])];
}}

function visibleCourses() {{
    const programme = currentProgramme();
    const range = creditRange();
    const track = trackSel.value;

    return programme.courses.filter(function (course) {{
        if (activeLevel !== null && course.level !== activeLevel) return false;

        if (range) {{
            const credits = course.credits;
            if (credits == null || credits < range[0] || credits > range[1]) return false;
        }}

        if (track && (course.track || 'core') !== track) return false;

        return true;
    }});
}}

function renderLevels() {{
    const programme = currentProgramme();
    const buttons = ['<button class="lvl' + (activeLevel === null ? ' on' : '') +
                     '" data-level="">All levels</button>'];

    programme.levels.forEach(function (level) {{
        buttons.push('<button class="lvl' + (activeLevel === level ? ' on' : '') +
                     '" data-level="' + level + '">Level ' + level + '</button>');
    }});

    levelsBox.innerHTML = buttons.join('');

    levelsBox.querySelectorAll('.lvl').forEach(function (button) {{
        button.addEventListener('click', function () {{
            const raw = button.dataset.level;
            activeLevel = raw === '' ? null : Number(raw);
            render();
        }});
    }});
}}

function render() {{
    const programme = currentProgramme();
    const courses = visibleCourses();
    const credits = courses.reduce(function (sum, c) {{ return sum + (c.credits || 0); }}, 0);

    renderLevels();

    // Show the track picker only where tracks exist.
    const hasTracks = programme.courses.some(function (c) {{ return c.track; }});
    trackSel.parentElement.style.display = hasTracks ? '' : 'none';
    if (!hasTracks) trackSel.value = '';

    summaryBox.innerHTML =
        '<div class="chip"><b>' + courses.length + '</b><span>courses</span></div>' +
        '<div class="chip"><b>' + credits + '</b><span>credit hours</span></div>' +
        '<div class="chip"><b>' + programme.duration_years + '</b><span>years</span></div>' +
        '<div class="chip"><b>' + esc(programme.programme_type.toUpperCase()) +
        '</b><span>award</span></div>';

    if (!courses.length) {{
        out.innerHTML = '<div class="none">No courses match those filters.</div>';
        return;
    }}

    // Group by level so a stage reads as a block.
    const byLevel = {{}};
    courses.forEach(function (course) {{
        const key = course.level == null ? 'Other' : 'Level ' + course.level;
        (byLevel[key] = byLevel[key] || []).push(course);
    }});

    out.innerHTML = Object.keys(byLevel).sort().map(function (key) {{
        const rows = byLevel[key].map(function (course) {{
            const track = course.track && course.track !== 'core'
                ? '<span class="track ' + course.track + '">' + course.track + '</span>'
                : '';
            const desc = course.description
                ? '<div class="desc">' + esc(course.description.slice(0, 220)) + '…</div>'
                : '';
            const arabic = course.title_ar
                ? '<div class="desc" dir="rtl">' + esc(course.title_ar) + '</div>'
                : '';

            return '<tr>' +
                '<td class="code">' + esc(course.code) + '</td>' +
                '<td>' + esc(course.title) + track + arabic + desc + '</td>' +
                '<td class="cr">' + (course.credits == null ? '—' : course.credits) + '</td>' +
                '</tr>';
        }}).join('');

        const levelCredits = byLevel[key].reduce(function (s, c) {{ return s + (c.credits || 0); }}, 0);

        return '<section class="term">' +
            '<h2>' + esc(key) + ' — ' + byLevel[key].length + ' courses, ' +
            levelCredits + ' credits</h2>' +
            '<div class="table-wrap"><table class="courses">' +
            '<thead><tr><th>Code</th><th>Course</th><th style="text-align:right">Cr</th></tr></thead>' +
            '<tbody>' + rows + '</tbody></table></div></section>';
    }}).join('');
}}

progSel.addEventListener('change', function () {{ activeLevel = null; render(); }});
creditSel.addEventListener('change', render);
trackSel.addEventListener('change', render);
render();
</script>

</body>
</html>
"""


def main():
    if not os.path.exists(DATA):
        print(f"Missing {DATA}. Run scripts/extract-local-syllabi.py first.",
              file=sys.stderr)
        return 1

    data = json.load(open(DATA, encoding="utf-8"))
    open(OUTPUT, "w", encoding="utf-8").write(build(data))

    print(f"Wrote {OUTPUT}")
    print(f"  programmes: {len([p for p in data['programmes'] if p['courses']])}")
    print(f"  courses:    {data['total_courses']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
