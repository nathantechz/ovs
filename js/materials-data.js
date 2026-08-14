// Materials and Textbook References
// This file contains all course materials with textbook citations

const materialsData = {
    "ocular-anatomy": {
        title: "Ocular Anatomy & Physiology",
        category: "anatomy",
        level: "undergraduate",
        country: "sa", // Saudi Arabia
        lectures: 8,
        materials: 8,
        textbookReferences: [
            {
                title: "Ocular Anatomy and Physiology",
                author: "Sheila Coyne Nemeth, Al Lens",
                edition: "2nd Edition",
                year: 2014,
                pages: "Complete reference",
                relevantSections: ["Chapter 1-12: Complete eye anatomy"],
                link: "materials/Ocular Anatomy & Physiology/Ocular Anatomy and Physiology, Second Edition (Al Lens Sheila Coyne Nemeth).pdf"
            }
        ],
        materials: [
            {
                id: 1,
                title: "Lecture 1: Introduction to Ocular Anatomy",
                type: "presentation",
                format: "pptx",
                pages: "40",
                download: "materials/Ocular Anatomy & Physiology/Lecture PPT/Lecture 1.pptx"
            },
            {
                id: 2,
                title: "Lecture 2: Anterior Segment",
                type: "presentation",
                format: "pptx",
                pages: "45",
                download: "materials/Ocular Anatomy & Physiology/Lecture PPT/Lecture 2.pptx"
            },
            {
                id: 3,
                title: "Lecture 3: Cornea & Conjunctiva",
                type: "presentation",
                format: "pptx",
                pages: "38",
                download: "materials/Ocular Anatomy & Physiology/Lecture PPT/Lecture 3.pptx"
            },
            {
                id: 4,
                title: "Lecture 4: Iris & Pupil",
                type: "presentation",
                format: "pptx",
                pages: "35",
                download: "materials/Ocular Anatomy & Physiology/Lecture PPT/Lecture 4.pptx"
            },
            {
                id: 5,
                title: "Lecture 5: Lens",
                type: "presentation",
                format: "pptx",
                pages: "42",
                download: "materials/Ocular Anatomy & Physiology/Lecture PPT/Lecture 5.pptx"
            },
            {
                id: 6,
                title: "Lecture 6: Vitreous",
                type: "presentation",
                format: "pptx",
                pages: "30",
                download: "materials/Ocular Anatomy & Physiology/Lecture PPT/Lecture 6.pptx"
            },
            {
                id: 7,
                title: "Lecture 7: Retina",
                type: "presentation",
                format: "pptx",
                pages: "48",
                download: "materials/Ocular Anatomy & Physiology/Lecture PPT/Lecture 7.pptx"
            },
            {
                id: 8,
                title: "Lecture 8: Optic Nerve & Visual Pathways",
                type: "presentation",
                format: "pptx",
                pages: "40",
                download: "materials/Ocular Anatomy & Physiology/Lecture PPT/Lecture 8.pptx"
            }
        ],
        readingNotes: [
            {
                title: "Reading Notes 1: Ocular Anatomy Basics",
                download: "materials/Ocular Anatomy & Physiology/Reading Notes/Notes 1.pdf"
            },
            {
                title: "Reading Notes 2: Anterior Segment Deep Dive",
                download: "materials/Ocular Anatomy & Physiology/Reading Notes/Notes 2.pdf"
            }
        ]
    },

    "physical-optics": {
        title: "Physical Optics",
        category: "refraction",
        level: "undergraduate",
        country: "sa",
        lectures: 14,
        materials: 14,
        textbookReferences: [
            {
                title: "Principles of Physical Optics",
                author: "Charles A. Bennett",
                edition: "2nd Edition",
                year: 2008,
                pages: "Complete optical physics reference",
                relevantSections: ["Chapter 1-15: Wave optics, interference, diffraction"],
                link: "materials/Physical Optics/Principles of Physical Optics, 2e (Charles A. Bennett).pdf"
            }
        ],
        materials: [
            {
                title: "Lecture 1-14: Physical Optics Complete Course",
                type: "presentations",
                download: "materials/Physical Optics/Lecture PPT/",
                notes: "14 comprehensive lectures on optical physics"
            }
        ]
    },

    "strabismus": {
        title: "Strabismus",
        category: "clinical",
        level: "graduate",
        country: "sa",
        lectures: 12,
        textbookReferences: [
            {
                title: "Comprehensive Overview of Strabismus",
                author: "Clinical Education Materials",
                edition: "Latest",
                pages: "Professional clinical reference",
                relevantSections: ["Assessment, diagnosis, and management of strabismus"]
            }
        ],
        materials: [
            {
                title: "Lecture 1-12: Strabismus Management",
                type: "presentations",
                download: "materials/Strabismus/Lecture PPT/",
                notes: "12 lectures on strabismus diagnosis and treatment"
            }
        ]
    },

    "biostatistics": {
        title: "Biostatistics",
        category: "anatomy",
        level: "undergraduate",
        country: "sa",
        lectures: 7,
        textbookReferences: [
            {
                title: "Biostatistics",
                author: "Professional Reference",
                edition: "Latest",
                pages: "Applied biostatistics for healthcare",
                relevantSections: ["Statistical methods, hypothesis testing, data analysis"]
            }
        ],
        materials: [
            {
                title: "Reading Notes 1-7: Biostatistics Fundamentals",
                type: "notes",
                download: "materials/Biostatistics/Reading Notes/",
                notes: "7 comprehensive reading notes on biostatistics"
            }
        ]
    },

    "pediatric-optometry": {
        title: "Pediatric Optometry",
        category: "clinical",
        level: "graduate",
        country: "sa",
        lectures: 6,
        textbookReferences: [
            {
                title: "Pediatric Eye Care",
                author: "Clinical Reference",
                edition: "Latest",
                pages: "Specialized pediatric optometry care",
                relevantSections: ["Child eye examination, refractive errors in children, amblyopia"]
            }
        ],
        materials: [
            {
                title: "Reading Notes 1-6: Pediatric Optometry",
                type: "notes",
                download: "materials/Pediatric Optometry/Reading Notes/",
                notes: "6 comprehensive reading notes on pediatric care"
            }
        ]
    },

    "environmental-safety": {
        title: "Environmental Health & Occupational Safety",
        category: "clinical",
        level: "undergraduate",
        country: "sa",
        lectures: 5,
        materials: 5,
        textbookReferences: [
            {
                title: "Occupational Safety in Optometry",
                author: "Professional Guide",
                edition: "Latest",
                pages: "Workplace eye health and safety",
                relevantSections: ["Hazard assessment, PPE, workplace ergonomics"]
            }
        ],
        materials: [
            {
                title: "Lecture 1-5: Occupational Eye Health",
                type: "presentations",
                download: "materials/Environmental Health & Occupational Safety/Lecture PPT/",
                notes: "5 lectures on workplace eye safety"
            }
        ]
    }
};

// Download handler function
function downloadMaterial(materialPath) {
    // Creates a download link for PDFs and presentations
    const link = document.createElement('a');
    link.href = materialPath;
    link.download = materialPath.split('/').pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Display textbook reference
function showTextbookReference(course) {
    if (course.textbookReferences && course.textbookReferences.length > 0) {
        return course.textbookReferences.map(ref =>
            `<div class="textbook-reference">
                <strong>${ref.title}</strong><br/>
                Author: ${ref.author}<br/>
                Edition: ${ref.edition} (${ref.year})<br/>
                Pages: ${ref.pages}<br/>
                Sections: ${ref.relevantSections.join(', ')}
            </div>`
        ).join('');
    }
    return '';
}
