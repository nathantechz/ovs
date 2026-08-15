#!/usr/bin/env python3
"""
Build a subject graph linking courses that teach the same material.

Different schools name the same course differently. Southern College calls it
"Optics of the Eye", MCPHS calls it "Visual Optics", and this site calls it
"Physical Optics". A flat course list cannot express that; a graph can.

    subject node  ── covers ──  course node (school A)
                  ── covers ──  course node (school B)
                  ── covers ──  course node (this site)

Two courses joined through the same subject are teaching overlapping material,
whatever they are called. The graph is what makes "different name, same
content" answerable.

Subjects are matched by keyword patterns defined below. Each match records
which pattern fired, so a mapping can be checked rather than taken on trust,
and anything that matches nothing is reported as unmapped instead of being
forced into a bucket.

Inputs:
    data/syllabi.json   scraped school curricula (scripts/extract-syllabi.py)
    js/data.js          this site's own course catalogue

Output:
    data/topic-graph.json

Usage:
    .venv/bin/python scripts/build-topic-graph.py
"""

import json
import os
import re
import sys
from collections import defaultdict

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYLLABI = os.path.join(PROJECT_DIR, "data", "syllabi.json")
DATA_JS = os.path.join(PROJECT_DIR, "js", "data.js")
OUTPUT = os.path.join(PROJECT_DIR, "data", "topic-graph.json")

# Canonical subjects and the keywords that identify them. Ordered: the first
# matching subject wins for the primary assignment, though a course may map to
# several. Derived from the titles actually present in the scraped data.
SUBJECTS = [
    ("optics-physical", "Physical & Visual Optics", "optics", [
        r"\baberration", r"\bwavefront\b", r"\blens design\b", r"\baspheric\b",
        r"\bphysical optics\b", r"\bvisual optics\b", r"\boptics of the eye\b",
        r"\bgeometrical? (and|&) physical optics\b", r"\bgeometric(al)? optics\b",
    ]),
    ("optics-ophthalmic", "Ophthalmic Optics & Dispensing", "optics", [
        r"\bophthalmic optics\b", r"\bdispensing\b", r"\bspectacle\b",
        r"\bophthalmic lens", r"\boptical (materials|fabrication)\b",
    ]),
    ("refraction", "Refraction & Refractive Error", "optics", [
        r"\brefraction\b", r"\brefractive error\b", r"\bametropia\b",
    ]),
    ("anatomy", "Ocular Anatomy & Physiology", "foundations", [
        r"\banatomy\b", r"\bhistology\b", r"\bphysiology\b", r"\bgross anatomy\b",
    ]),
    ("neuro", "Neuroanatomy & Visual Neuroscience", "foundations", [
        r"\bneuro-?optometry\b", r"\bneurobiolog", r"\bneuro eye\b",
        r"\bneuroscience\b", r"\boculomotor\b",
        r"\bneuroanatomy\b", r"\bneuro anatomy\b", r"\bneurophysiolog",
        r"\bneuro-?ophthalm", r"\bvisual neuro",
    ]),
    ("biochem", "Ocular Biochemistry & Cell Biology", "foundations", [
        r"\bbiochemistry\b", r"\bcell biology\b", r"\bmolecular\b", r"\bimmunolog",
        r"\bmicrobiolog", r"\bgenetics\b",
    ]),
    ("perception", "Visual Perception & Psychophysics", "foundations", [
        r"\bvisual perception\b", r"\bperception\b", r"\bpsychophysic",
        r"\bcolo(u)?r vision\b",
    ]),
    ("binocular", "Binocular Vision & Ocular Motility", "clinical", [
        r"\bbinocular\b", r"\bocular motility\b", r"\bstrabismus\b",
        r"\bamblyopia\b", r"\bvergence\b", r"\baccommodation\b",
    ]),
    ("vision-therapy", "Vision Therapy & Rehabilitation", "clinical", [
        r"\bvision therapy\b", r"\bvision rehabilitation\b", r"\blow vision\b",
        r"\bvision rehab",
    ]),
    ("contact-lens", "Contact Lenses", "clinical", [
        r"\bcontact lens", r"\bcornea (and|&) contact lens\b",
    ]),
    ("clinical-methods", "Clinical Methods & Procedures", "clinical", [
        r"\bslit lamp\b", r"\btonometry\b", r"\bgonioscop", r"\bbiomicroscop",
        r"\bclinical evaluation\b", r"\bcevs\b", r"\bfundamentals\b",
        r"\btheory (and|&) methods\b", r"\bclinical (methods|procedures|skills)\b",
        r"\bexamination\b", r"\boptometric methods\b",
    ]),
    ("clinical-practice", "Clinical Rotations & Internships", "clinical", [
        r"\bfoundations of clinical care\b", r"\bspecialty clinic",
        r"\bcase management\b", r"\bclinical management\b",
        r"\bclinical rotation\b", r"\bexternship\b", r"\binternship\b",
        r"\bclinic\b", r"\bprimary (eye )?care\b", r"\bpreceptor",
    ]),
    ("anterior-segment", "Anterior Segment Disease", "disease", [
        r"\buveitis\b", r"\binflammat", r"\bocular surface\b", r"\bdry eye\b",
        r"\banterior segment\b", r"\bcornea\b", r"\bcorneal\b", r"\bexternal disease\b",
    ]),
    ("posterior-segment", "Posterior Segment & Retinal Disease", "disease", [
        r"\bposterior segment\b", r"\bretina\b", r"\bretinal\b", r"\bvitreo",
    ]),
    ("glaucoma", "Glaucoma", "disease", [r"\bglaucoma\b", r"\bintraocular pressure\b", r"\biop\b"]),
    ("systemic", "Systemic Disease & Ocular Manifestations", "disease", [
        r"\bsystemic disease", r"\bpathophysiolog", r"\bsystems [IVX]+\b",
        r"\bocular manifestation",
        r"\bsystemic disease\b", r"\bgeneral patholog", r"\bbasic patholog",
        r"\bsystems based physiolog", r"\bpatholog",
    ]),
    ("pharmacology", "Pharmacology", "disease", [
        r"\bpharmacolog", r"\bpharmaceutic", r"\btherapeutic",
    ]),
    ("surgery", "Surgical & Peri-operative Care", "disease", [
        r"\bsurgic", r"\bsurgery\b", r"\bperi-?operative\b", r"\blaser\b",
    ]),
    ("pediatrics", "Pediatric Optometry", "populations", [
        r"\bvisual development\b", r"\bspecial populations\b",
        r"\bpediatric\b", r"\bpaediatric\b", r"\binfant\b", r"\bchild",
    ]),
    ("geriatrics", "Geriatric & Aging Vision", "populations", [
        r"\bgeriatric\b", r"\baging\b", r"\bageing\b",
    ]),
    ("public-health", "Public Health & Community Eye Care", "populations", [
        r"\bergonomic", r"\bdigital vision\b", r"\benvironmental optometry\b",
        r"\bsports\b", r"\bperformance vision\b", r"\boccupational\b",
        r"\bpublic health\b", r"\bcommunity eye care\b", r"\bepidemiolog",
        r"\bcommunity\b", r"\bglobal health\b",
    ]),
    ("practice-management", "Practice Management & Business", "professional", [
        r"\bclinicolegal\b", r"\blegal\b",
        r"\bpractice management\b", r"\bbusiness\b", r"\bpractice strategies\b",
        r"\bproduct management\b", r"\boptometric practice\b", r"\bethic",
        r"\bjurisprudence\b", r"\bpractice (and|&) procedures\b",
    ]),
    ("research", "Research Methods & Evidence", "professional", [
        r"\bresearch\b", r"\bstatistic", r"\bevidence[- ]based\b", r"\bliterature\b",
        r"\bepidemiology\b", r"\bcritical (appraisal|thinking)\b",
    ]),
    ("imaging", "Diagnostic Imaging & Instrumentation", "clinical", [
        r"\bimaging\b", r"\binstrument", r"\bdiagnostic techn", r"\boct\b",
        r"\bperimetr", r"\bvisual field",
    ]),
    ("professional-skills", "Professional & Communication Skills", "professional", [
        r"\bcommunicat", r"\bacademic success\b", r"\bprofessional develop",
        r"\bintegrative clinical analysis\b", r"\bcase analysis\b", r"\bseminar\b",
    ]),
]


def load_syllabi():
    if not os.path.exists(SYLLABI):
        print(f"Missing {SYLLABI}. Run scripts/extract-syllabi.py first.",
              file=sys.stderr)
        return None
    return json.load(open(SYLLABI, encoding="utf-8"))


def load_site_courses():
    """Read id/title/category out of js/data.js."""
    source = open(DATA_JS, encoding="utf-8").read()
    block = source[source.index("const coursesData"):]

    courses = []
    for match in re.finditer(
        r"id:\s*(\d+),\s*\n\s*title:\s*\"([^\"]+)\",\s*\n\s*category:\s*\"([^\"]+)\"",
        block,
    ):
        courses.append({
            "id": int(match.group(1)),
            "title": match.group(2),
            "category": match.group(3),
        })

    return courses


def match_subjects(title):
    """Every subject whose pattern appears in the title, with the pattern."""
    lowered = title.lower()
    hits = []

    for slug, label, group, patterns in SUBJECTS:
        for pattern in patterns:
            if re.search(pattern, lowered):
                hits.append({"subject": slug, "matched": pattern})
                break

    return hits


def main():
    syllabi = load_syllabi()
    if syllabi is None:
        return 1

    site_courses = load_site_courses()

    subject_nodes = {
        slug: {
            "id": f"subject:{slug}",
            "type": "subject",
            "label": label,
            "group": group,
            "courseCount": 0,
            "sourceCount": 0,
        }
        for slug, label, group, _ in SUBJECTS
    }

    course_nodes = []
    edges = []
    unmapped = []
    subject_sources = defaultdict(set)

    def add_course(node_id, label, source, extra=None):
        node = {
            "id": node_id,
            "type": "course",
            "label": label,
            "source": source,
        }
        if extra:
            node.update(extra)

        hits = match_subjects(label)
        if not hits:
            unmapped.append({"course": label, "source": source})
            node["subjects"] = []
        else:
            node["subjects"] = [h["subject"] for h in hits]
            for hit in hits:
                edges.append({
                    "from": node_id,
                    "to": f"subject:{hit['subject']}",
                    "matched": hit["matched"],
                })
                subject_nodes[hit["subject"]]["courseCount"] += 1
                subject_sources[hit["subject"]].add(source)

        course_nodes.append(node)

    # Courses published by this site
    for course in site_courses:
        add_course(
            f"olh:{course['id']}",
            course["title"],
            "Optometry Learning Hub",
            {"courseId": course["id"], "category": course["category"],
             "href": f"#/course/{course['id']}"},
        )

    # Courses scraped from each school
    for school in syllabi["schools"]:
        for index, course in enumerate(school["courses"]):
            add_course(
                f"{school['school'][:18]}:{course['code']}:{index}",
                course["title"],
                school["school"],
                {"code": course["code"], "term": course.get("term"),
                 "credits": course.get("credits")},
            )

    for slug, sources in subject_sources.items():
        subject_nodes[slug]["sourceCount"] = len(sources)
        subject_nodes[slug]["sources"] = sorted(sources)

    # Subjects taught at more than one institution are the real overlaps.
    shared = [s for s in subject_nodes.values() if s["sourceCount"] > 1]

    graph = {
        "generated_from": {
            "syllabi": os.path.relpath(SYLLABI, PROJECT_DIR),
            "site_catalogue": os.path.relpath(DATA_JS, PROJECT_DIR),
            "extracted_at": syllabi.get("extracted_at"),
        },
        "counts": {
            "subjects": len(subject_nodes),
            "courses": len(course_nodes),
            "edges": len(edges),
            "unmapped": len(unmapped),
            "sharedSubjects": len(shared),
        },
        "nodes": list(subject_nodes.values()) + course_nodes,
        "edges": edges,
        "unmapped": unmapped,
    }

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    json.dump(graph, open(OUTPUT, "w", encoding="utf-8"), indent=2)

    print(f"subjects:  {len(subject_nodes)}")
    print(f"courses:   {len(course_nodes)}")
    print(f"edges:     {len(edges)}")
    print(f"unmapped:  {len(unmapped)}")
    print(f"written:   {OUTPUT}\n")

    print("Subjects taught under different names at more than one institution:")
    for subject in sorted(shared, key=lambda s: -s["courseCount"])[:12]:
        print(f"  {subject['label']:44} {subject['courseCount']:3} courses "
              f"across {subject['sourceCount']} sources")

    if unmapped:
        print(f"\n{len(unmapped)} courses matched no subject, e.g.:")
        for item in unmapped[:8]:
            print(f"  - {item['course'][:52]}  ({item['source'][:28]})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
