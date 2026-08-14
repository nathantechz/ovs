// Comprehensive Optometry Textbooks Index
// 123+ professional textbooks organized by subject
// Links textbooks to courses for recommended reading

const textbooksIndex = {
    "optics": {
        category: "Optics & Light",
        courses: ["Physical Optics", "Refraction & Optics Fundamentals", "Geometric Optics"],
        books: [
            {
                id: "optics-1",
                title: "Clinical Optics",
                authors: ["Professional Reference"],
                year: 2016,
                size: "21 MB",
                coverage: "Complete clinical optics reference",
                relevantChapters: ["1-15: Clinical optical principles"],
                difficulty: "Intermediate-Advanced"
            },
            {
                id: "optics-2",
                title: "Handbook of Optics Volume 1",
                authors: ["Professional Reference"],
                year: 2016,
                size: "17 MB",
                coverage: "Comprehensive optical physics",
                relevantChapters: ["All chapters on fundamentals"],
                difficulty: "Advanced"
            },
            {
                id: "optics-3",
                title: "Handbook of Visual Optics Volume One",
                authors: ["Artal, Pablo"],
                year: 2021,
                size: "24 MB",
                coverage: "Eye optics and fundamentals",
                relevantChapters: ["1-12: Fundamentals and eye optics"],
                difficulty: "Advanced"
            },
            {
                id: "optics-4",
                title: "Optics of the Human Eye",
                authors: ["David Atchison", "George Smith"],
                year: 2021,
                size: "5.7 MB",
                coverage: "Human eye optical principles",
                relevantChapters: ["Complete reference"],
                difficulty: "Intermediate"
            },
            {
                id: "optics-5",
                title: "Handbook of Optics Third Edition",
                authors: ["Professional Reference"],
                year: 2016,
                size: "9.5 MB",
                coverage: "Modern optical systems",
                relevantChapters: ["1-20: Advanced optics"],
                difficulty: "Advanced"
            }
        ]
    },

    "anatomy": {
        category: "Ocular Anatomy & Physiology",
        courses: ["Ocular Anatomy & Physiology", "Eye Anatomy", "Visual System"],
        books: [
            {
                id: "anatomy-1",
                title: "Ocular Anatomy and Physiology",
                authors: ["Sheila Coyne Nemeth", "Al Lens"],
                year: 2014,
                edition: "2nd Edition",
                size: "Reference",
                coverage: "Complete eye anatomy",
                relevantChapters: ["1-12: Complete anatomy"],
                difficulty: "Beginner-Intermediate"
            },
            {
                id: "anatomy-2",
                title: "General Anatomy Reference",
                authors: ["Professional Reference"],
                year: 2020,
                size: "12 KB",
                coverage: "Systemic anatomy with eye reference",
                relevantChapters: ["Relevant sections"],
                difficulty: "Beginner"
            }
        ]
    },

    "binocular-vision": {
        category: "Binocular Vision & Strabismus",
        courses: ["Binocular Vision & Eye Movement", "Strabismus", "Vergence & Accommodation"],
        bookCount: 29,
        size: "16 MB",
        description: "29 comprehensive books on binocular vision, strabismus management, and oculomotor control",
        highlights: [
            "Vergence and accommodation mechanisms",
            "Strabismus diagnosis and classification",
            "Clinical assessment methods",
            "Treatment strategies",
            "Pediatric strabismus",
            "Adult strabismus management"
        ]
    },

    "clinical-optometry": {
        category: "Clinical Optometry",
        courses: ["Clinical Skills & Examinations", "Refraction & Clinical Practice", "Contact Lens Fitting"],
        bookCount: 6,
        size: "170 MB",
        description: "6 major textbooks on comprehensive clinical practice",
        highlights: [
            "Complete patient examination procedures",
            "Refraction techniques",
            "Clinical decision making",
            "Prescription writing",
            "Patient management",
            "Advanced clinical protocols"
        ]
    },

    "ocular-diseases": {
        category: "Ocular Diseases & Pathology",
        courses: ["Ocular Diseases", "Common Eye Diseases", "Systemic Diseases & Ocular Manifestations"],
        bookCount: 8,
        size: "122 MB",
        description: "8 comprehensive textbooks on ocular pathology and disease management",
        highlights: [
            "Cataract pathology and management",
            "Glaucoma classification and treatment",
            "Retinal diseases",
            "Corneal pathology",
            "Uveitis",
            "Infectious diseases",
            "Systemic disease manifestations"
        ]
    },

    "contact-lens": {
        category: "Contact Lens Science & Practice",
        courses: ["Contact Lens Practice", "Specialized Contact Lens Applications"],
        bookCount: 6,
        description: "6 books covering all aspects of contact lens practice",
        highlights: [
            "Lens design and materials",
            "Fitting techniques",
            "RGP and soft lens practice",
            "Specialized applications",
            "Complications and management",
            "Patient education"
        ]
    },

    "refraction": {
        category: "Refraction & Refractive Errors",
        courses: ["Refraction & Optics", "Refractive Errors", "Optical Correction"],
        bookCount: 10,
        description: "10 books on refractive error assessment and correction",
        highlights: [
            "Myopia, hyperopia, astigmatism",
            "Presbyopia management",
            "Refractive surgery assessment",
            "Spectacle prescription",
            "Advanced refractive techniques"
        ]
    },

    "low-vision": {
        category: "Low Vision & Rehabilitation",
        courses: ["Low Vision & Rehabilitation", "Visual Rehabilitation"],
        bookCount: 12,
        description: "12 books on low vision assessment and rehabilitation",
        highlights: [
            "Low vision evaluation",
            "Optical and electronic aids",
            "Rehabilitation strategies",
            "Patient counseling",
            "Activities of daily living",
            "Accessibility solutions"
        ]
    },

    "pediatric": {
        category: "Pediatric Vision & Development",
        courses: ["Pediatric Optometry", "Refractive Errors in Children"],
        description: "Specialized resources for child eye care",
        highlights: [
            "Pediatric examination techniques",
            "Refractive error in children",
            "Amblyopia and strabismus",
            "Developmental milestones",
            "Behavioral optometry",
            "School vision screening"
        ]
    },

    "ophthalmic-diagnostics": {
        category: "Ophthalmic Diagnostic Imaging",
        courses: ["Advanced Diagnostic Imaging", "Clinical Instrumentation"],
        bookCount: 6,
        description: "Diagnostic imaging and instrumentation",
        highlights: [
            "OCT interpretation",
            "Fundus photography",
            "Fluorescein angiography",
            "Optical coherence tomography",
            "Digital imaging",
            "Image analysis"
        ]
    },

    "dispensing": {
        category: "Ophthalmic Dispensing",
        courses: ["Spectacle Dispensing", "Optical Laboratory Operations"],
        bookCount: 4,
        description: "Dispensing optics and optical shop management",
        highlights: [
            "Spectacle lens design",
            "Frame selection",
            "Lens materials",
            "Anti-reflective coatings",
            "Fitting height calculations"
        ]
    },

    "optometric-instruments": {
        category: "Optometric Instruments & Equipment",
        courses: ["Clinical Instrumentation", "Slit Lamp & Tonometry"],
        bookCount: 5,
        description: "Comprehensive coverage of optometric equipment",
        highlights: [
            "Slit lamp operation",
            "Tonometry equipment",
            "Refraction instruments",
            "Imaging devices",
            "Maintenance and calibration"
        ]
    },

    "neuro-ophthalmology": {
        category: "Neuro-Ophthalmology",
        courses: ["Neuro-Ophthalmology", "Visual Neurology"],
        bookCount: 2,
        description: "Neurological aspects of vision",
        highlights: [
            "Visual pathways",
            "Optic nerve diseases",
            "Visual field defects",
            "Pupillary disorders",
            "Oculomotor disorders"
        ]
    },

    "vision-therapy": {
        category: "Vision Therapy & Training",
        courses: ["Vision Therapy", "Visual Rehabilitation"],
        description: "Therapeutic techniques for vision rehabilitation",
        highlights: [
            "Vision therapy procedures",
            "Accommodation training",
            "Vergence therapy",
            "Prism adaptation",
            "Perceptual training"
        ]
    },

    "sports-vision": {
        category: "Sports Vision",
        courses: ["Sports Vision", "Performance Enhancement"],
        description: "Vision considerations for athletic performance",
        highlights: [
            "Sports vision testing",
            "Performance enhancement",
            "Eye protection",
            "Sport-specific vision needs"
        ]
    },

    "visual-perception": {
        category: "Visual Perception & Psychophysics",
        courses: ["Visual Perception", "Color Vision"],
        bookCount: 14,
        description: "14 books on visual perception and psychophysics",
        highlights: [
            "Color vision mechanisms",
            "Contrast sensitivity",
            "Visual acuity",
            "Perceptual organization",
            "Visual illusions",
            "Adaptation and habituation"
        ]
    },

    "pharmacology": {
        category: "Ocular Pharmacology",
        courses: ["Ocular Pharmacology", "Therapeutic Optometry"],
        description: "Drug actions and therapeutic use in eye care",
        highlights: [
            "Ophthalmic drugs",
            "Drug interactions",
            "Therapeutic agents",
            "Adverse effects",
            "Treatment protocols"
        ]
    },

    "public-health": {
        category: "Public Health & Community Optometry",
        courses: ["Public Health", "Community Eye Health"],
        description: "Population-based approaches to eye health",
        highlights: [
            "Epidemiology of eye disease",
            "Screening programs",
            "Public health initiatives",
            "Community outreach",
            "Preventive care"
        ]
    }
};

// Get textbooks for a specific course
function getTextbooksForCourse(courseName) {
    const results = [];
    Object.values(textbooksIndex).forEach(category => {
        if (category.courses && category.courses.includes(courseName)) {
            if (category.books) {
                results.push(...category.books);
            } else {
                results.push({
                    category: category.category,
                    bookCount: category.bookCount,
                    size: category.size,
                    highlights: category.highlights
                });
            }
        }
    });
    return results;
}

// Get all textbook categories
function getAllCategories() {
    return Object.keys(textbooksIndex).map(key => ({
        id: key,
        ...textbooksIndex[key]
    }));
}

// Get textbooks by category
function getTextbooksByCategory(categoryId) {
    return textbooksIndex[categoryId] || null;
}

// Generate textbook reading list HTML
function generateReadingList(courseName) {
    const textbooks = getTextbooksForCourse(courseName);

    if (textbooks.length === 0) {
        return `<p class="no-textbooks">No textbooks currently linked to this course. Check back soon!</p>`;
    }

    let html = `<div class="reading-list">`;

    textbooks.forEach(textbook => {
        if (textbook.books) {
            // Specific book
            html += `
                <div class="textbook-item">
                    <h4>${textbook.title}</h4>
                    <p><strong>Authors:</strong> ${textbook.authors.join(", ")}</p>
                    <p><strong>Year:</strong> ${textbook.year}</p>
                    ${textbook.edition ? `<p><strong>Edition:</strong> ${textbook.edition}</p>` : ''}
                    <p><strong>Coverage:</strong> ${textbook.coverage}</p>
                    <p><strong>Relevant Chapters:</strong> ${textbook.relevantChapters.join(", ")}</p>
                    <p><strong>Difficulty Level:</strong> ${textbook.difficulty}</p>
                    <button class="btn-access-textbook">Access Textbook</button>
                </div>
            `;
        } else if (textbook.bookCount) {
            // Category with multiple books
            html += `
                <div class="textbook-category">
                    <h4>${textbook.category}</h4>
                    <p><strong>${textbook.bookCount} Books Available</strong> | Size: ${textbook.size}</p>
                    <p>${textbook.description}</p>
                    <h5>Key Topics Covered:</h5>
                    <ul>
                        ${textbook.highlights.map(h => `<li>${h}</li>`).join('')}
                    </ul>
                    <button class="btn-browse-category">Browse ${textbook.bookCount} Books</button>
                </div>
            `;
        }
    });

    html += `</div>`;
    return html;
}

// Generate textbook summary for course page
function generateTextbookSummary(courseName) {
    const textbooks = getTextbooksForCourse(courseName);

    return `
        <div class="textbook-summary">
            <h3>Recommended Textbooks</h3>
            <p class="summary-count">${textbooks.length} recommended textbooks</p>
            ${generateReadingList(courseName)}
            <p class="textbook-note">
                <i class="fas fa-info-circle"></i>
                All textbook references are curated from our comprehensive library of 123+ professional optometry resources.
            </p>
        </div>
    `;
}

// Search textbooks across all categories
function searchTextbooks(query) {
    const results = [];
    const searchTerm = query.toLowerCase();

    Object.entries(textbooksIndex).forEach(([key, category]) => {
        if (category.category.toLowerCase().includes(searchTerm) ||
            (category.description && category.description.toLowerCase().includes(searchTerm))) {
            results.push({
                id: key,
                type: "category",
                ...category
            });
        }

        if (category.books) {
            category.books.forEach(book => {
                if (book.title.toLowerCase().includes(searchTerm) ||
                    book.authors.some(a => a.toLowerCase().includes(searchTerm))) {
                    results.push({
                        type: "book",
                        category: category.category,
                        ...book
                    });
                }
            });
        }
    });

    return results;
}

// Statistics about textbooks collection
function getTextbookStats() {
    let totalBooks = 0;
    let totalSize = 0;
    const categories = Object.keys(textbooksIndex).length;
    const courses = new Set();

    Object.values(textbooksIndex).forEach(category => {
        if (category.bookCount) {
            totalBooks += category.bookCount;
        }
        if (category.books) {
            totalBooks += category.books.length;
        }
        if (category.courses) {
            category.courses.forEach(c => courses.add(c));
        }
    });

    return {
        totalCategories: categories,
        totalBooks: totalBooks,
        linkedCourses: courses.size,
        coursesList: Array.from(courses)
    };
}
