#!/usr/bin/env python3
"""Insert a download panel into each generated note page."""
import json, os, re, html

NOTES = "notes"
manifest = json.load(open(os.path.join(NOTES, "manifest.json")))

FOLDERS = {
    "Ocular Anatomy & Physiology": "materials/Ocular Anatomy & Physiology/Reading Notes",
    "Physical Optics": "materials/Physical Optics/Reading Notes",
    "Strabismus": "materials/Strabismus/Lecture Notes",
}

PANEL = """
<section class="note-downloads">
    <h2>Download this topic</h2>
    <p>Take these notes offline in whichever format suits you.</p>
    <div class="download-row">
{links}
    </div>
</section>
"""

LINK = ('        <a class="dl" href="{href}" download>'
        '<span class="dl-fmt">{fmt}</span>'
        '<span class="dl-meta">{meta}</span></a>')

changed = 0
missing = []

for course, entries in manifest.items():
    folder = FOLDERS.get(course)
    if not folder:
        continue

    for entry in entries:
        page = os.path.join(NOTES, entry["html_file"])
        if not os.path.exists(page):
            missing.append(entry["html_file"])
            continue

        src = open(page, encoding="utf-8").read()
        if "note-downloads" in src:
            continue

        links = []
        md = os.path.join(folder, entry["md_file"])
        if os.path.exists(md):
            kb = max(1, round(os.path.getsize(md) / 1024))
            links.append(LINK.format(href="../" + md.replace(" ", "%20"),
                                     fmt="Markdown", meta=f"{kb} KB &middot; .md"))

        docx = os.path.join(folder, f"Week {entry['week']}.docx")
        if os.path.exists(docx):
            kb = max(1, round(os.path.getsize(docx) / 1024))
            links.append(LINK.format(href="../" + docx.replace(" ", "%20"),
                                     fmt="Word document", meta=f"{kb} KB &middot; .docx"))

        links.append('        <button class="dl dl-print" onclick="window.print()">'
                     '<span class="dl-fmt">Print / Save as PDF</span>'
                     '<span class="dl-meta">uses your browser</span></button>')

        panel = PANEL.format(links="\n".join(links))
        src = src.replace("<footer class=\"note-footer\">", panel + "\n<footer class=\"note-footer\">", 1)
        open(page, "w", encoding="utf-8").write(src)
        changed += 1

print(f"panels inserted: {changed}")
if missing:
    print("missing pages:", missing)
