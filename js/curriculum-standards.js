// Optometry Curriculum Standards by Country
// Ensures that courses match international educational requirements

const curriculumStandards = {
    "india": {
        name: "India - Diploma in Optometry",
        organization: "All India Ophthalmological Society (AIOS) & COO",
        standard: "Minimum Optometry Curriculum",
        year: 2024,
        requiredCourses: [
            {
                category: "anatomy",
                title: "Ocular Anatomy & Physiology",
                hours: 90,
                status: "✅ Available",
                materials: 8
            },
            {
                category: "refraction",
                title: "Physical Optics & Geometric Optics",
                hours: 60,
                status: "✅ Available",
                materials: 14
            },
            {
                category: "clinical",
                title: "Clinical Optometry & Refraction",
                hours: 120,
                status: "✅ Available",
                materials: 15
            },
            {
                category: "clinical",
                title: "Binocular Vision & Strabismus",
                hours: 45,
                status: "✅ Available",
                materials: 12
            },
            {
                category: "anatomy",
                title: "Biostatistics & Research Methods",
                hours: 30,
                status: "✅ Available",
                materials: 7
            },
            {
                category: "clinical",
                title: "Contact Lens Practice",
                hours: 60,
                status: "Planned",
                materials: 0
            },
            {
                category: "ocular-diseases",
                title: "Ocular Pathology & Disease",
                hours: 90,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Low Vision & Rehabilitation",
                hours: 30,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Pediatric Optometry",
                hours: 45,
                status: "✅ Available",
                materials: 6
            },
            {
                category: "clinical",
                title: "Occupational & Environmental Health",
                hours: 30,
                status: "✅ Available",
                materials: 5
            }
        ],
        totalHours: 600,
        completionPercentage: 65
    },

    "usa": {
        name: "USA - Doctor of Optometry (OD)",
        organization: "ACOE (Accreditation Council for Optometric Education)",
        standard: "Comprehensive OD Program",
        year: 2024,
        requiredCourses: [
            {
                category: "anatomy",
                title: "Ocular Anatomy & Physiology",
                hours: 120,
                status: "✅ Available",
                materials: 8
            },
            {
                category: "refraction",
                title: "Physical Optics & Principles of Refraction",
                hours: 120,
                status: "✅ Available",
                materials: 14
            },
            {
                category: "clinical",
                title: "Comprehensive Clinical Optometry",
                hours: 200,
                status: "✅ Available",
                materials: 15
            },
            {
                category: "ocular-diseases",
                title: "Ocular Disease & Pathology",
                hours: 120,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Pharmacology & Therapeutics",
                hours: 60,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Contact Lens Specialization",
                hours: 100,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Binocular Vision & Strabismus",
                hours: 80,
                status: "✅ Available",
                materials: 12
            },
            {
                category: "clinical",
                title: "Pediatric & Geriatric Optometry",
                hours: 80,
                status: "✅ Available",
                materials: 11
            }
        ],
        totalHours: 1200,
        completionPercentage: 55
    },

    "uk": {
        name: "United Kingdom - BSc Optometry / MCOptom",
        organization: "GOC (General Optical Council)",
        standard: "UK Optometry Degree",
        year: 2024,
        requiredCourses: [
            {
                category: "anatomy",
                title: "Ocular Anatomy & Physiology",
                hours: 100,
                status: "✅ Available",
                materials: 8
            },
            {
                category: "refraction",
                title: "Optics & Light",
                hours: 80,
                status: "✅ Available",
                materials: 14
            },
            {
                category: "clinical",
                title: "Clinical Practice & Examination",
                hours: 150,
                status: "✅ Available",
                materials: 15
            },
            {
                category: "ocular-diseases",
                title: "Ocular Disease Management",
                hours: 100,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Contact Lenses",
                hours: 60,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Binocular Vision",
                hours: 60,
                status: "✅ Available",
                materials: 12
            },
            {
                category: "anatomy",
                title: "Research & Evidence Practice",
                hours: 50,
                status: "✅ Available",
                materials: 7
            }
        ],
        totalHours: 600,
        completionPercentage: 60
    },

    "canada": {
        name: "Canada - Doctor of Optometry",
        organization: "CAO (Canadian Association of Optometrists)",
        standard: "Canadian OD Program",
        year: 2024,
        requiredCourses: [
            {
                category: "anatomy",
                title: "Ocular Anatomy & Physiology",
                hours: 120,
                status: "✅ Available",
                materials: 8
            },
            {
                category: "refraction",
                title: "Optics & Vision Science",
                hours: 100,
                status: "✅ Available",
                materials: 14
            },
            {
                category: "clinical",
                title: "Clinical Optometry",
                hours: 180,
                status: "✅ Available",
                materials: 15
            },
            {
                category: "ocular-diseases",
                title: "Eye Disease & Pathology",
                hours: 100,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Therapeutic Optometry",
                hours: 80,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Binocular Vision & Strabismus",
                hours: 80,
                status: "✅ Available",
                materials: 12
            }
        ],
        totalHours: 800,
        completionPercentage: 60
    },

    "australia": {
        name: "Australia - Bachelor/Master of Optometry",
        organization: "ASBOS (Australasian Society of Behavioural Optometry & Vision Science)",
        standard: "Australian Optometry Degree",
        year: 2024,
        requiredCourses: [
            {
                category: "anatomy",
                title: "Ocular Anatomy & Physiology",
                hours: 120,
                status: "✅ Available",
                materials: 8
            },
            {
                category: "refraction",
                title: "Optical Science & Principles",
                hours: 100,
                status: "✅ Available",
                materials: 14
            },
            {
                category: "clinical",
                title: "Clinical Optometry & Practice",
                hours: 150,
                status: "✅ Available",
                materials: 15
            },
            {
                category: "ocular-diseases",
                title: "Systemic & Ocular Disease",
                hours: 100,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Contact Lens Practice",
                hours: 80,
                status: "Planned",
                materials: 0
            },
            {
                category: "clinical",
                title: "Vision Development & Strabismus",
                hours: 80,
                status: "✅ Available",
                materials: 12
            },
            {
                category: "clinical",
                title: "Research Methods",
                hours: 50,
                status: "✅ Available",
                materials: 7
            }
        ],
        totalHours: 800,
        completionPercentage: 60
    },

    "saudi-arabia": {
        name: "Saudi Arabia - Diploma in Optometry",
        organization: "MOH & PHCC Standards",
        standard: "Saudi Optometry Curriculum",
        year: 2024,
        requiredCourses: [
            {
                category: "anatomy",
                title: "Ocular Anatomy & Physiology",
                hours: 90,
                status: "✅ Available",
                materials: 8
            },
            {
                category: "refraction",
                title: "Physical Optics",
                hours: 60,
                status: "✅ Available",
                materials: 14
            },
            {
                category: "clinical",
                title: "Refraction & Clinical Practice",
                hours: 120,
                status: "✅ Available",
                materials: 15
            },
            {
                category: "clinical",
                title: "Binocular Vision & Strabismus",
                hours: 45,
                status: "✅ Available",
                materials: 12
            },
            {
                category: "anatomy",
                title: "Biostatistics",
                hours: 30,
                status: "✅ Available",
                materials: 7
            },
            {
                category: "clinical",
                title: "Pediatric Optometry",
                hours: 45,
                status: "✅ Available",
                materials: 6
            },
            {
                category: "clinical",
                title: "Occupational Eye Health",
                hours: 30,
                status: "✅ Available",
                materials: 5
            },
            {
                category: "ocular-diseases",
                title: "Common Eye Diseases",
                hours: 60,
                status: "Planned",
                materials: 0
            }
        ],
        totalHours: 480,
        completionPercentage: 70
    }
};

// Get curriculum for specific country
function getCurriculumForCountry(countryCode) {
    const countryMap = {
        "india": "india",
        "usa": "usa",
        "uk": "uk",
        "canada": "canada",
        "australia": "australia",
        "sa": "saudi-arabia",
        "saudi-arabia": "saudi-arabia"
    };

    return curriculumStandards[countryMap[countryCode]] || null;
}

// Display curriculum requirements
function displayCurriculumRequirements(countryCode) {
    const curriculum = getCurriculumForCountry(countryCode);
    if (!curriculum) return;

    const html = `
        <div class="curriculum-card">
            <h3>${curriculum.name}</h3>
            <p class="curriculum-meta">
                <strong>Standard:</strong> ${curriculum.standard}<br>
                <strong>Organization:</strong> ${curriculum.organization}<br>
                <strong>Total Hours:</strong> ${curriculum.totalHours}
            </p>

            <div class="progress-bar">
                <div class="progress-fill" style="width: ${curriculum.completionPercentage}%"></div>
                <span class="progress-text">${curriculum.completionPercentage}% Complete</span>
            </div>

            <h4>Curriculum Requirements</h4>
            <table class="curriculum-table">
                <thead>
                    <tr>
                        <th>Course</th>
                        <th>Hours</th>
                        <th>Status</th>
                        <th>Materials</th>
                    </tr>
                </thead>
                <tbody>
                    ${curriculum.requiredCourses.map(course => `
                        <tr>
                            <td><strong>${course.title}</strong></td>
                            <td>${course.hours}</td>
                            <td>${course.status}</td>
                            <td>${course.materials} items</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;

    return html;
}

// Filter courses by country curriculum
function getCoursesForCountry(countryCode) {
    const curriculum = getCurriculumForCountry(countryCode);
    if (!curriculum) return [];

    // Return only courses that are marked as "Available"
    return curriculum.requiredCourses.filter(course => course.status === "✅ Available");
}
