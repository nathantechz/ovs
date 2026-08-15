#!/usr/bin/env python3
import os
import re
import glob
import docx

COURSES_CONFIG = [
    {
        "course_name": "Ocular Anatomy & Physiology",
        "short_name": "Ocular Anatomy",
        "folder_key": "ocular-anatomy",
        "source_dir": "materials/Ocular Anatomy & Physiology/Reading Notes",
        "file_pattern": "Week *.docx",
        "out_md_dir": "materials/Ocular Anatomy & Physiology/Reading Notes",
        "out_html_prefix": "ocular-anatomy",
        "textbook_ref": "Ocular Anatomy and Physiology, Sheila Coyne Nemeth & Al Lens (2nd Edition)"
    },
    {
        "course_name": "Physical Optics",
        "short_name": "Physical Optics",
        "folder_key": "physical-optics",
        "source_dir": "materials/Physical Optics/Reading Notes",
        "file_pattern": "Week *.docx",
        "out_md_dir": "materials/Physical Optics/Reading Notes",
        "out_html_prefix": "physical-optics",
        "textbook_ref": "Principles of Physical Optics, Charles A. Bennett (2nd Edition)"
    },
    {
        "course_name": "Strabismus",
        "short_name": "Strabismus",
        "folder_key": "strabismus",
        "source_dir": "materials/Strabismus/Lecture Notes",
        "file_pattern": "Week *.docx",
        "out_md_dir": "materials/Strabismus/Lecture Notes",
        "out_html_prefix": "strabismus",
        "textbook_ref": "Clinical Management of Binocular Vision / Clinical Orthoptics"
    }
]

MATH_REPLACEMENTS = [
    (r'\$\\lambda\$', '&lambda;'),
    (r'\$A\$', 'A'),
    (r'\$f\$', 'f'),
    (r'\$\\phi\$', '&phi;'),
    (r'\$\\theta\$', '&theta;'),
    (r'\$\\Delta\$', '&Delta;'),
    (r'\$\\omega\$', '&omega;'),
    (r'\$\\pi\$', '&pi;'),
    (r'\$\\approx\$', '&asymp;'),
    (r'\$\\times\$', '&times;'),
    (r'\$\\cdot\$', '&middot;'),
    (r'\$\\propto\$', '&prop;'),
    (r'\$\\ge\$', '&ge;'),
    (r'\$\\le\$', '&le;'),
    (r'\$\\pm\$', '&plusmn;'),
    (r'\$\\mu m\$', '&mu;m'),
    (r'\$\\mu\$', '&mu;'),
    (r'\$\\Delta\$', '&Delta;'),
    (r'\$\\partial\$', '&part;'),
    (r'\$\^2\$', '²'),
    (r'\$\^3\$', '³'),
    (r'\$\^-1\$', '⁻¹'),
    (r'\$\^-8\$', '⁻⁸'),
    (r'\$(.*?)\$', r'<em>\1</em>')
]

def clean_math_html(text):
    for pattern, repl in MATH_REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    return text

def clean_math_md(text):
    text = re.sub(r'\$\\lambda\$', 'λ', text)
    text = re.sub(r'\$\\phi\$', 'φ', text)
    text = re.sub(r'\$\\theta\$', 'θ', text)
    text = re.sub(r'\$\\Delta\$', 'Δ', text)
    text = re.sub(r'\$\\omega\$', 'ω', text)
    text = re.sub(r'\$\\pi\$', 'π', text)
    text = re.sub(r'\$\\approx\$', '≈', text)
    text = re.sub(r'\$\\times\$', '×', text)
    text = re.sub(r'\$\\cdot\$', '·', text)
    text = re.sub(r'\$\\propto\$', '∝', text)
    text = re.sub(r'\$\\ge\$', '≥', text)
    text = re.sub(r'\$\\le\$', '≤', text)
    text = re.sub(r'\$\\pm\$', '±', text)
    text = re.sub(r'\$\\mu m\$', 'μm', text)
    text = re.sub(r'\$\\partial\$', '∂', text)
    text = re.sub(r'\$(.*?)\$', r'\1', text)
    return text

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def extract_week_num(filename):
    m = re.search(r'Week\s*(\d+)', filename, re.IGNORECASE)
    return int(m.group(1)) if m else 999

def parse_docx(file_path):
    doc = docx.Document(file_path)
    title = ""
    subtitle = ""
    sections = []
    current_section = {"heading": "", "level": 2, "elements": []}
    
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    if not paragraphs:
        return {"title": "Study Notes", "subtitle": "", "sections": []}
    
    # Check first paragraph for main title
    p0 = paragraphs[0]
    p0_text = p0.text.strip()
    
    # Try to extract clean title
    if "Reading Notes:" in p0_text:
        parts = p0_text.split("Reading Notes:", 1)
        title = parts[1].strip()
    elif "Topic:" in p0_text:
        parts = p0_text.split("Topic:", 1)
        title = parts[1].strip()
    elif len(paragraphs) > 1 and ("Topic:" in paragraphs[1].text or "Reading Notes:" in paragraphs[1].text):
        subtitle = p0_text
        p1_text = paragraphs[1].text.strip()
        if "Topic:" in p1_text:
            title = p1_text.split("Topic:", 1)[1].strip()
        elif "Reading Notes:" in p1_text:
            title = p1_text.split("Reading Notes:", 1)[1].strip()
        else:
            title = p1_text
        paragraphs = paragraphs[1:]
    else:
        title = p0_text
        
    paragraphs = paragraphs[1:]
    
    for p in paragraphs:
        text = p.text.strip()
        style_name = p.style.name.lower()
        runs = p.runs
        
        # Check if entire paragraph is a heading by style
        if "heading" in style_name:
            if current_section["heading"] or current_section["elements"]:
                sections.append(current_section)
            current_section = {"heading": text, "level": 2, "elements": []}
            continue
            
        # Check if starting run is bold and looks like a section header (e.g., "1. Introduction" or "I. Core Definitions")
        is_split_heading = False
        if runs:
            first_run_text = runs[0].text.strip()
            if (runs[0].bold and (re.match(r'^([0-9]+|[IVXLCDM]+)[\.\:]\s+', first_run_text) or 
                                 re.match(r'^(Section|Module|Chapter|Part)\s+', first_run_text, re.IGNORECASE))):
                if current_section["heading"] or current_section["elements"]:
                    sections.append(current_section)
                current_section = {"heading": first_run_text, "level": 2, "elements": []}
                is_split_heading = True
                
                # Check remaining runs in this paragraph as body
                remaining_runs = runs[1:]
                if remaining_runs:
                    rem_text = "".join(r.text for r in remaining_runs).strip()
                    if rem_text:
                        current_section["elements"].append({
                            "type": "paragraph",
                            "runs": [{"text": r.text, "bold": r.bold, "italic": r.italic} for r in remaining_runs]
                        })
                continue

        # Check for list paragraphs
        is_list = "list" in style_name or text.startswith(('•', '-', '*', '–'))
        clean_text = re.sub(r'^[•\-\*\–]\s*', '', text)
        
        element_runs = [{"text": r.text, "bold": r.bold, "italic": r.italic} for r in runs]
        if is_list:
            current_section["elements"].append({
                "type": "list_item",
                "runs": element_runs,
                "text": clean_text
            })
        else:
            current_section["elements"].append({
                "type": "paragraph",
                "runs": element_runs,
                "text": text
            })
            
    if current_section["heading"] or current_section["elements"]:
        sections.append(current_section)
        
    return {
        "title": title,
        "subtitle": subtitle,
        "sections": sections
    }

def runs_to_html(runs):
    html = ""
    for r in runs:
        t = r["text"]
        if not t:
            continue
        t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        t = clean_math_html(t)
        if r.get("bold"):
            t = f"<strong>{t}</strong>"
        if r.get("italic"):
            t = f"<em>{t}</em>"
        html += t
    return html

def runs_to_md(runs):
    md = ""
    for r in runs:
        t = r["text"]
        if not t:
            continue
        t = clean_math_md(t)
        if r.get("bold") and r.get("italic"):
            t = f"***{t.strip()}*** "
        elif r.get("bold"):
            t = f"**{t.strip()}** "
        elif r.get("italic"):
            t = f"*{t.strip()}* "
        md += t
    return md

def generate_markdown(course_info, week_num, parsed_data):
    md_lines = []
    md_lines.append(f"# {course_info['course_name']} - Week {week_num}: {parsed_data['title']}")
    if parsed_data.get('subtitle'):
        md_lines.append(f"## {parsed_data['subtitle']}")
    md_lines.append("\n---\n")
    
    for sec in parsed_data["sections"]:
        if sec["heading"]:
            md_lines.append(f"## {clean_math_md(sec['heading'])}\n")
        in_list = False
        for el in sec["elements"]:
            if el["type"] == "list_item":
                md_lines.append(f"- {runs_to_md(el['runs']).strip()}")
                in_list = True
            else:
                if in_list:
                    md_lines.append("")
                    in_list = False
                md_lines.append(f"{runs_to_md(el['runs']).strip()}\n")
        if in_list:
            md_lines.append("")
            
    md_lines.append("\n---\n")
    md_lines.append(f"**Reference:** {course_info['textbook_ref']}")
    return "\n".join(md_lines)

def generate_html(course_info, week_num, total_weeks, parsed_data, prev_link=None, next_link=None, prev_title=None, next_title=None):
    title = parsed_data["title"] or f"Week {week_num} Notes"
    
    html_lines = []
    html_lines.append("<!DOCTYPE html>")
    html_lines.append('<html lang="en">')
    html_lines.append('<head>')
    html_lines.append('<meta charset="UTF-8">')
    html_lines.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_lines.append(f'<title>{title} — {course_info["short_name"]} Notes</title>')
    html_lines.append('<link rel="stylesheet" href="notes.css">')
    html_lines.append('</head>')
    html_lines.append('<body>')
    html_lines.append('')
    html_lines.append('<nav class="note-nav">')
    html_lines.append('    <div class="note-nav-inner">')
    html_lines.append('        <a href="../index.html">&larr; Optometry Learning Hub</a>')
    html_lines.append(f'        <span class="course-tag">{course_info["short_name"]} &middot; Week {week_num}</span>')
    html_lines.append('    </div>')
    html_lines.append('</nav>')
    html_lines.append('')
    html_lines.append('<main>')
    html_lines.append('')
    html_lines.append('<header class="note-header">')
    html_lines.append(f'    <div class="note-eyebrow">{course_info["course_name"]} &middot; Week {week_num} of {total_weeks}</div>')
    html_lines.append(f'    <h1>{clean_math_html(title)}</h1>')
    if parsed_data.get("subtitle"):
        html_lines.append(f'    <p class="note-summary">{clean_math_html(parsed_data["subtitle"])}</p>')
    html_lines.append('</header>')
    html_lines.append('')
    
    for sec in parsed_data["sections"]:
        if sec["heading"]:
            h_text = clean_math_html(sec["heading"])
            html_lines.append(f'<h2>{h_text}</h2>\n')
            
        in_list = False
        for el in sec["elements"]:
            if el["type"] == "list_item":
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                html_lines.append(f'    <li>{runs_to_html(el["runs"])}</li>')
            else:
                if in_list:
                    html_lines.append('</ul>\n')
                    in_list = False
                p_content = runs_to_html(el["runs"])
                if p_content.strip():
                    html_lines.append(f'<p>{p_content}</p>')
        if in_list:
            html_lines.append('</ul>\n')
            
    html_lines.append('<footer class="note-footer">')
    html_lines.append(f'    <span>Reference: <em>{course_info["textbook_ref"]}</em></span>')
    
    nav_links = []
    if prev_link:
        nav_links.append(f'<a href="{prev_link}">&larr; Prev: Week {week_num-1}</a>')
    if next_link:
        nav_links.append(f'<a href="{next_link}">Next: Week {week_num+1} &rarr;</a>')
        
    if nav_links:
        html_lines.append(f'    <div style="display:flex; gap:16px;">{" ".join(nav_links)}</div>')
    html_lines.append('</footer>')
    html_lines.append('')
    html_lines.append('</main>')
    html_lines.append('</body>')
    html_lines.append('</html>')
    
    return "\n".join(html_lines)

def main():
    os.makedirs("notes", exist_ok=True)
    manifest = {}
    
    for course in COURSES_CONFIG:
        print(f"\nProcessing {course['course_name']}...")
        source_files = glob.glob(os.path.join(course['source_dir'], course['file_pattern']))
        source_files.sort(key=extract_week_num)
        
        total_weeks = len(source_files)
        course_notes = []
        
        # First pass: parse all
        for fpath in source_files:
            week_num = extract_week_num(fpath)
            parsed = parse_docx(fpath)
            slug = slugify(parsed["title"]) or f"week-{week_num}"
            if len(slug) > 40:
                slug = slug[:40].rstrip('-')
            html_filename = f"{course['out_html_prefix']}-{week_num:02d}-{slug}.html"
            
            course_notes.append({
                "week": week_num,
                "file_path": fpath,
                "parsed": parsed,
                "html_filename": html_filename,
                "title": parsed["title"]
            })
            
        manifest[course["course_name"]] = []
        
        # Second pass: generate Markdown & HTML with prev/next links
        for i, note in enumerate(course_notes):
            week_num = note["week"]
            parsed = note["parsed"]
            html_filename = note["html_filename"]
            
            # Markdown output
            md_content = generate_markdown(course, week_num, parsed)
            md_filename = f"Week {week_num} - {parsed['title'][:50]}.md".replace("/", "-")
            md_path = os.path.join(course["out_md_dir"], md_filename)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
                
            # HTML output
            prev_link = course_notes[i-1]["html_filename"] if i > 0 else None
            next_link = course_notes[i+1]["html_filename"] if i < len(course_notes) - 1 else None
            
            html_content = generate_html(
                course, week_num, total_weeks, parsed,
                prev_link=prev_link, next_link=next_link
            )
            html_path = os.path.join("notes", html_filename)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            manifest[course["course_name"]].append({
                "week": week_num,
                "title": note["title"],
                "html_file": html_filename,
                "md_file": md_filename
            })
            print(f"  ✓ Week {week_num}: {note['title']} -> {html_filename}")
            
    # Save manifest for JS usage
    import json
    with open("notes/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("\n✓ Notes generation complete. Manifest saved to notes/manifest.json")

if __name__ == "__main__":
    main()
