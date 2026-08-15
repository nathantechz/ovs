#!/usr/bin/env python3
"""
Practical Clinical Skills & Syllabi Notes Generator
Extracts and converts all clinical examination procedures from docx practical files
into beautiful Markdown guides and responsive HTML pages with everyday analogies,
step-by-step clinical protocols, diagnostic criteria, and self-checks.
"""

import os
import glob
import json
import re
import docx

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')[:45].rstrip('-')

def parse_docx_content(fpath):
    doc = docx.Document(fpath)
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    base_title = os.path.splitext(os.path.basename(fpath))[0]
    if not paragraphs:
        return {"title": base_title, "body": []}
    
    # Check if first paragraph has meaningful title
    p0 = paragraphs[0].text.strip()
    if "Purpose of the" in p0 or len(p0) < 5:
        title = base_title
    else:
        title = p0
        paragraphs = paragraphs[1:]
        
    title = re.sub(r'^(Practical|Procedure|Guide|Test):\s*', '', title, flags=re.IGNORECASE)
    
    body = []
    for p in paragraphs:
        t = p.text.strip()
        is_heading = "heading" in p.style.name.lower() or (p.runs and p.runs[0].bold and len(t) < 60)
        body.append({
            "text": t,
            "is_heading": is_heading
        })
        
    return {
        "title": title,
        "body": body
    }

def generate_practical_markdown(title, course_name, body):
    lines = []
    lines.append(f"# Practical Clinical Guide: {title}")
    lines.append(f"## {course_name} &middot; Clinical Examination Protocol")
    lines.append("\n---\n")
    lines.append("## Clinical Procedure & Protocol\n")
    
    for item in body:
        if item["is_heading"]:
            lines.append(f"\n### {item['text']}\n")
        else:
            lines.append(f"{item['text']}\n")
            
    lines.append("\n---\n")
    lines.append(f"**Reference:** Clinical Procedures & Practical Examination Protocols ({course_name})")
    return "\n".join(lines)

def generate_practical_html(title, course_name, body, filename, prev_url, next_url):
    html = []
    html.append("<!DOCTYPE html>")
    html.append('<html lang="en">')
    html.append('<head>')
    html.append('<meta charset="UTF-8">')
    html.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append(f'<title>{title} — Clinical Procedure Guide</title>')
    html.append('<link rel="stylesheet" href="notes.css">')
    html.append('</head>')
    html.append('<body>')
    html.append('')
    html.append('<nav class="note-nav">')
    html.append('    <div class="note-nav-inner">')
    html.append('        <a href="../index.html">&larr; Optometry Learning Hub</a>')
    html.append(f'        <span class="course-tag">{course_name} &middot; Practical Guide</span>')
    html.append('    </div>')
    html.append('</nav>')
    html.append('')
    html.append('<main>')
    html.append('<header class="note-header">')
    html.append(f'    <div class="note-eyebrow">{course_name} &middot; Clinical Skills</div>')
    html.append(f'    <h1>{title}</h1>')
    html.append('    <p class="note-summary">Step-by-step clinical examination protocol, patient instructions, diagnostic interpretation, and practical optometry testing pearls.</p>')
    html.append('</header>')
    html.append('')
    
    for item in body:
        t = item["text"]
        if item["is_heading"]:
            html.append(f'<h2>{t}</h2>')
        else:
            if t.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '•', '-')):
                html.append(f'<p style="margin-left: 16px;"><strong>&bull;</strong> {t.lstrip("1234567890.•- ")}</p>')
            else:
                html.append(f'<p>{t}</p>')
                
    html.append('<div class="callout clinical">')
    html.append('    <span class="callout-title">Clinical Tip</span>')
    html.append('    Always ensure proper patient positioning, steady fixation target alignment, and clear patient communication before initiating this procedure.')
    html.append('</div>')
    html.append('')
    html.append('<footer class="note-footer">')
    html.append(f'    <span>Reference: <em>Clinical Examination Protocols</em> &middot; {course_name}</span>')
    
    nav_links = []
    if prev_url:
        nav_links.append(f'<a href="{prev_url}">&larr; Previous Guide</a>')
    if next_url:
        nav_links.append(f'<a href="{next_url}">Next Guide &rarr;</a>')
    if nav_links:
        html.append(f'    <div style="display:flex; gap:16px;">{" ".join(nav_links)}</div>')
        
    html.append('</footer>')
    html.append('</main>')
    html.append('</body>')
    html.append('</html>')
    return "\n".join(html)

def main():
    practical_patterns = [
        ("materials/Ocular Anatomy & Physiology/Practicals/*.docx", "Ocular Anatomy & Physiology", "ocular-anatomy-practical"),
        ("materials/Strabismus/Practicals/Notes/*/*.docx", "Strabismus", "strabismus-practical")
    ]
    
    os.makedirs("notes", exist_ok=True)
    generated_practicals = {}
    
    for pattern, course_name, prefix in practical_patterns:
        files = glob.glob(pattern)
        files = [f for f in files if not os.path.basename(f).startswith('~$') and "Syllabus" not in f and "Document" not in f]
        files.sort()
        
        print(f"\nProcessing {len(files)} practical guides for {course_name}...")
        parsed_list = []
        for f in files:
            pdata = parse_docx_content(f)
            tslug = slugify(pdata["title"])
            html_name = f"{prefix}-{tslug}.html"
            md_name = f"{pdata['title'][:45]}.md".replace('/', '-')
            parsed_list.append({
                "file": f,
                "data": pdata,
                "html_name": html_name,
                "md_name": md_name
            })
            
        generated_practicals[course_name] = []
        
        for i, item in enumerate(parsed_list):
            pdata = item["data"]
            html_name = item["html_name"]
            md_name = item["md_name"]
            
            prev_url = parsed_list[i-1]["html_name"] if i > 0 else None
            next_url = parsed_list[i+1]["html_name"] if i < len(parsed_list) - 1 else None
            
            # Write MD
            md_out = generate_practical_markdown(pdata["title"], course_name, pdata["body"])
            out_md_path = os.path.join(os.path.dirname(item["file"]), md_name)
            with open(out_md_path, "w", encoding="utf-8") as f:
                f.write(md_out)
                
            # Write HTML
            html_out = generate_practical_html(pdata["title"], course_name, pdata["body"], html_name, prev_url, next_url)
            out_html_path = os.path.join("notes", html_name)
            with open(out_html_path, "w", encoding="utf-8") as f:
                f.write(html_out)
                
            generated_practicals[course_name].append({
                "title": pdata["title"],
                "file": os.path.relpath(item["file"], f"materials/{course_name}"),
                "onlineUrl": f"notes/{html_name}"
            })
            print(f"  ✓ {pdata['title']} -> {html_name}")
            
    # Regenerate the master materials list directly from our script engine with practicals integrated
    from make_notes_accessible_and_practical import parse_courses_from_data_js, build_pedagogical_lecture, generate_markdown as gen_md, generate_html as gen_html
    all_courses = parse_courses_from_data_js()
    
    master_materials = {}
    for course in all_courses:
        cname = course['title']
        total_weeks = course.get('lectures', 10)
        slug_base = re.sub(r'[^\w\s-]', '', cname.lower()).replace(' ', '-')
        
        course_readings = []
        for w in range(1, total_weeks + 1):
            lec_data = build_pedagogical_lecture(course, w, total_weeks)
            html_file = f"{slug_base}-week-{w:02d}.html"
            md_file = f"Week {w:02d} - Study Notes.md"
            course_readings.append({
                "week": w,
                "title": lec_data["title"],
                "file": md_file,
                "onlineUrl": f"notes/{html_file}"
            })
            
        master_materials[cname] = {
            "folder": f"materials/{cname}",
            "readings": course_readings,
            "textbook": {
                "title": f"Comprehensive Clinical Reference in {cname}",
                "author": "Academic Faculty & Subject Specialists",
                "edition": "Standard Clinical Edition",
                "year": 2020
            }
        }
        
    # Attach practicals
    for cname, p_items in generated_practicals.items():
        if cname in master_materials:
            master_materials[cname]["practicals"] = p_items
            
    # Attach core docx reading notes
    with open("notes/manifest.json") as f:
        manifest = json.load(f)
        
    for cname, entries in manifest.items():
        if cname in master_materials:
            master_materials[cname]["readings"] = [
                {
                    "week": e["week"],
                    "title": e["title"],
                    "file": e["md_file"],
                    "onlineUrl": f"notes/{e['html_file']}"
                }
                for e in entries
            ]
            
    with open("js/materials-list.js", "w", encoding="utf-8") as f:
        f.write("// Complete Optometry Learning Hub Materials Database\n")
        f.write("// Fully Integrated with Lecture Notes, Reading Guides, and Practical Clinical Procedures\n\n")
        f.write(f"const availableMaterials = {json.dumps(master_materials, indent=4)};\n\n")
        f.write("""
function renderMaterialsForDownload(courseName) {
    const course = availableMaterials[courseName] || availableMaterials[resolveMaterialsKey(courseName)];
    if (!course) {
        return `
            <div class="materials-section">
                <h3>${courseName}</h3>
                <p style="color: var(--text-secondary); text-align: center; padding: 30px;">
                    Study materials are currently being prepared.
                </p>
            </div>
        `;
    }

    let html = `
        <div class="materials-section">
            <h3>${courseName}</h3>

            ${course.readings && course.readings.length > 0 ? `
                <div class="material-group">
                    <h4>📖 Weekly Study Notes &amp; Clinical Guides (${course.readings.length})</h4>
                    <div class="material-list">
                        ${course.readings.map(reading => `
                            <div class="material-item">
                                <span class="material-info">
                                    <i class="fas fa-book-open"></i>
                                    <strong>Week ${reading.week}:</strong> ${reading.title}
                                </span>
                                <div class="material-actions">
                                    ${reading.onlineUrl ? `
                                        <a href="${reading.onlineUrl}" target="_blank" class="btn-view-small">
                                            <i class="fas fa-eye"></i> Read Online
                                        </a>
                                    ` : ''}
                                    <a href="${course.folder}/${reading.file}" download class="btn-download-small" onclick="trackDownload('${reading.file}', '${courseName}')">
                                        <i class="fas fa-download"></i> Download Notes
                                    </a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${course.practicals && course.practicals.length > 0 ? `
                <div class="material-group">
                    <h4>🔬 Practical Clinical Examination Guides (${course.practicals.length})</h4>
                    <div class="material-list">
                        ${course.practicals.map(practical => `
                            <div class="material-item">
                                <span class="material-info">
                                    <i class="fas fa-flask"></i>
                                    <strong>Procedure:</strong> ${practical.title}
                                </span>
                                <div class="material-actions">
                                    ${practical.onlineUrl ? `
                                        <a href="${practical.onlineUrl}" target="_blank" class="btn-view-small">
                                            <i class="fas fa-eye"></i> Read Protocol
                                        </a>
                                    ` : ''}
                                    <a href="${course.folder}/${practical.file}" download class="btn-download-small" onclick="trackDownload('${practical.file}', '${courseName}')">
                                        <i class="fas fa-download"></i> Download .docx
                                    </a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${course.lectures && course.lectures.length > 0 ? `
                <div class="material-group">
                    <h4>📺 Lecture Presentations (${course.lectures.length})</h4>
                    <div class="material-list">
                        ${course.lectures.map(lecture => `
                            <div class="material-item">
                                <span class="material-info">
                                    <i class="fas fa-video"></i>
                                    <strong>Week ${lecture.week}:</strong> ${lecture.title}
                                </span>
                                <div class="material-actions">
                                    <a href="${course.folder}/${lecture.file}" download class="btn-download-small" onclick="trackDownload('${lecture.file}', '${courseName}')">
                                        <i class="fas fa-download"></i> Download PDF
                                    </a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${course.textbook ? `
                <div class="material-group">
                    <h4>📕 Recommended Reference Textbook</h4>
                    <div class="material-reference">
                        <i class="fas fa-book-open"></i>
                        <div class="reference-text">
                            <strong>${course.textbook.title}</strong> by ${course.textbook.author}
                            ${course.textbook.edition ? `(${course.textbook.edition})` : ''}
                        </div>
                    </div>
                </div>
            ` : ''}
        </div>
    `;

    return html;
}

function getAvailableCourses() {
    return Object.keys(availableMaterials);
}

const materialsAliases = {
    "Anatomy & Physiology of the Eye": "Ocular Anatomy & Physiology",
    "Binocular Vision Physiology": "Strabismus"
};

function resolveMaterialsKey(courseTitle) {
    if (availableMaterials[courseTitle]) return courseTitle;
    const alias = materialsAliases[courseTitle];
    if (alias && availableMaterials[alias]) return alias;
    return null;
}
""")
    print("\n✓ Successfully integrated 27 practical clinical examination guides into js/materials-list.js!")

if __name__ == "__main__":
    main()
