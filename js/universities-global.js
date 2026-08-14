// Global University Database - Optometry Programs Worldwide
// Includes links to actual university syllabuses and program information

const universitiesDatabase = {
    // INDIA - Optometry Universities
    "india": [
        {
            name: "Manipal Academy of Higher Education",
            country: "India",
            city: "Manipal",
            state: "Karnataka",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            affiliation: "AIOS, COO",
            syllabusURL: "https://manipal.edu/colleges/college-of-allied-health-sciences",
            contact: "+91-820-292-0292",
            established: 2001
        },
        {
            name: "Bangalore Institute of Optometry",
            country: "India",
            city: "Bangalore",
            state: "Karnataka",
            program: "Diploma in Optometry",
            degree: "Dip.Optom",
            duration: "2 years",
            affiliation: "AIOS, COO",
            syllabusURL: "https://www.biomedicalocularsciences.in/",
            contact: "optometry@biomedical.edu",
            established: 1995
        },
        {
            name: "Delhi Institute of Technology",
            country: "India",
            city: "Delhi",
            state: "Delhi",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            affiliation: "AIOS, COO",
            syllabusURL: "https://dit.ac.in/academics/optometry",
            contact: "+91-11-2783-0666",
            established: 1999
        },
        {
            name: "VIT Vellore",
            country: "India",
            city: "Vellore",
            state: "Tamil Nadu",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            affiliation: "AIOS, COO",
            syllabusURL: "https://vit.ac.in/academics/school-of-advanced-sciences/optometry",
            contact: "+91-0416-220-2222",
            established: 2005
        },
        {
            name: "Aravind Eye Care System - Academy",
            country: "India",
            city: "Madurai",
            state: "Tamil Nadu",
            program: "Certified Optometry Specialist",
            degree: "COS",
            duration: "3 years",
            affiliation: "AIOS, COO",
            syllabusURL: "https://www.aravind.org/academy",
            contact: "+91-452-243-4000",
            established: 1976
        },
        {
            name: "Ramakrishna Mission Vivekananda University",
            country: "India",
            city: "Kolkata",
            state: "West Bengal",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            affiliation: "AIOS, COO",
            syllabusURL: "https://rkmvu.ac.in/school-of-biosciences",
            contact: "+91-33-2479-0844",
            established: 1998
        }
    ],

    // USA - Optometry Schools
    "usa": [
        {
            name: "University of Alabama at Birmingham - School of Optometry",
            country: "USA",
            city: "Birmingham",
            state: "Alabama",
            program: "Doctor of Optometry",
            degree: "O.D.",
            duration: "4 years",
            accreditation: "ACOE",
            syllabusURL: "https://www.uab.edu/optometry",
            contact: "+1-205-934-6779",
            established: 1967
        },
        {
            name: "Indiana University School of Optometry",
            country: "USA",
            city: "Bloomington",
            state: "Indiana",
            program: "Doctor of Optometry",
            degree: "O.D.",
            duration: "4 years",
            accreditation: "ACOE",
            syllabusURL: "https://optometry.iu.edu/",
            contact: "+1-812-855-2104",
            established: 1921
        },
        {
            name: "University of California, Berkeley - School of Optometry",
            country: "USA",
            city: "Berkeley",
            state: "California",
            program: "Doctor of Optometry",
            degree: "O.D.",
            duration: "4 years",
            accreditation: "ACOE",
            syllabusURL: "https://optometry.berkeley.edu/",
            contact: "+1-510-642-1971",
            established: 1891
        },
        {
            name: "Pacific University College of Optometry",
            country: "USA",
            city: "Forest Grove",
            state: "Oregon",
            program: "Doctor of Optometry",
            degree: "O.D.",
            duration: "4 years",
            accreditation: "ACOE",
            syllabusURL: "https://www.pacificu.edu/as/optometry",
            contact: "+1-503-352-1200",
            established: 1910
        },
        {
            name: "Ohio State University College of Optometry",
            country: "USA",
            city: "Columbus",
            state: "Ohio",
            program: "Doctor of Optometry",
            degree: "O.D.",
            duration: "4 years",
            accreditation: "ACOE",
            syllabusURL: "https://optometry.osu.edu/",
            contact: "+1-614-292-1900",
            established: 1971
        }
    ],

    // UK - Optometry Programs
    "uk": [
        {
            name: "University of Manchester School of Optometry",
            country: "United Kingdom",
            city: "Manchester",
            country_code: "GB",
            program: "BSc Optometry / MCOptom",
            degree: "BSc/MCOptom",
            duration: "3 years",
            accreditation: "GOC",
            syllabusURL: "https://www.manchester.ac.uk/study/masters/courses/list/02/healthcare/",
            contact: "+44-161-306-3000",
            established: 1975
        },
        {
            name: "City University of London - School of Optometry",
            country: "United Kingdom",
            city: "London",
            country_code: "GB",
            program: "BSc Optometry",
            degree: "BSc",
            duration: "3 years",
            accreditation: "GOC",
            syllabusURL: "https://www.city.ac.uk/",
            contact: "+44-20-7040-8000",
            established: 1976
        },
        {
            name: "University of Plymouth - School of Optometry",
            country: "United Kingdom",
            city: "Plymouth",
            country_code: "GB",
            program: "BSc Optometry",
            degree: "BSc",
            duration: "3 years",
            accreditation: "GOC",
            syllabusURL: "https://www.plymouth.ac.uk/courses/optometry",
            contact: "+44-1752-600600",
            established: 1994
        }
    ],

    // CANADA - Optometry Schools
    "canada": [
        {
            name: "University of Waterloo School of Optometry",
            country: "Canada",
            city: "Waterloo",
            province: "Ontario",
            program: "Doctor of Optometry",
            degree: "O.D.",
            duration: "4 years",
            accreditation: "CAO",
            syllabusURL: "https://www.uwaterloo.ca/optometry/",
            contact: "+1-519-888-4567",
            established: 1963
        },
        {
            name: "University of Montreal School of Optometry",
            country: "Canada",
            city: "Montreal",
            province: "Quebec",
            program: "Doctor of Optometry",
            degree: "O.D.",
            duration: "4 years",
            accreditation: "CAO",
            syllabusURL: "https://optometrie.umontreal.ca/",
            contact: "+1-514-343-6111",
            established: 1966
        }
    ],

    // AUSTRALIA - Optometry Programs
    "australia": [
        {
            name: "University of Melbourne School of Optometry",
            country: "Australia",
            city: "Melbourne",
            state: "Victoria",
            program: "Master of Science in Clinical Optometry",
            degree: "MClinOptom",
            duration: "2 years",
            accreditation: "ASBOS",
            syllabusURL: "https://www.unimelb.edu.au/study/degrees/master-of-optometry-and-vision-science",
            contact: "+61-3-9035-5555",
            established: 1964
        },
        {
            name: "University of New South Wales - School of Optometry",
            country: "Australia",
            city: "Sydney",
            state: "New South Wales",
            program: "Bachelor of Science (Optometry)",
            degree: "B.Sc",
            duration: "4 years",
            accreditation: "ASBOS",
            syllabusURL: "https://www.unsw.edu.au/study/programs/optometry",
            contact: "+61-2-9385-1000",
            established: 1971
        },
        {
            name: "Queensland University of Technology",
            country: "Australia",
            city: "Brisbane",
            state: "Queensland",
            program: "Bachelor of Vision Science (Optometry)",
            degree: "B.VisionSci",
            duration: "4 years",
            accreditation: "ASBOS",
            syllabusURL: "https://www.qut.edu.au/courses/course.html?courseCode=BP062",
            contact: "+61-7-3138-2000",
            established: 1968
        }
    ],

    // MIDDLE EAST - Optometry Programs
    "middle-east": [
        {
            name: "King Saud University - College of Applied Medical Sciences",
            country: "Saudi Arabia",
            city: "Riyadh",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            accreditation: "MOH",
            syllabusURL: "https://cams.ksu.edu.sa/en",
            contact: "+966-11-4670000",
            established: 2005
        },
        {
            name: "American University of the Emirates - Health Sciences",
            country: "United Arab Emirates",
            city: "Dubai",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            accreditation: "MOH UAE",
            syllabusURL: "https://www.aue.ae/academics",
            contact: "+971-4-399-9000",
            established: 2006
        }
    ],

    // ASIA-PACIFIC - Optometry Programs
    "asia-pacific": [
        {
            name: "University of Auckland School of Optometry",
            country: "New Zealand",
            city: "Auckland",
            program: "Bachelor of Health Science (Optometry)",
            degree: "BHSc(Optom)",
            duration: "3 years",
            accreditation: "NZOA",
            syllabusURL: "https://www.auckland.ac.nz/en/study/study-options/find-a-study-option/optometry.html",
            contact: "+64-9-373-7599",
            established: 1947
        },
        {
            name: "Universitas Indonesia - Faculty of Medicine",
            country: "Indonesia",
            city: "Jakarta",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            accreditation: "MOH Indonesia",
            syllabusURL: "https://fk.ui.ac.id/en/",
            contact: "+62-21-391-7898",
            established: 1987
        }
    ],

    // EUROPE - Optometry Programs
    "europe": [
        {
            name: "Université de Bordeaux - School of Optometry",
            country: "France",
            city: "Bordeaux",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            accreditation: "France MESR",
            syllabusURL: "https://www.u-bordeaux.fr/en",
            contact: "+33-5-5700-8000",
            established: 1995
        },
        {
            name: "University of Valencia - School of Optometry",
            country: "Spain",
            city: "Valencia",
            program: "Bachelor of Optometry",
            degree: "B.Optom",
            duration: "4 years",
            accreditation: "Spain MEC",
            syllabusURL: "https://www.uv.es/",
            contact: "+34-96-398-2000",
            established: 1989
        }
    ]
};

// Get universities by country
function getUniversitiesByCountry(country) {
    const countryMap = {
        "india": "india",
        "usa": "usa",
        "uk": "uk",
        "canada": "canada",
        "australia": "australia",
        "saudi-arabia": "middle-east",
        "sa": "middle-east",
        "uae": "middle-east",
        "new-zealand": "asia-pacific",
        "nz": "asia-pacific",
        "france": "europe",
        "spain": "europe"
    };

    const region = countryMap[country.toLowerCase()];
    return region ? universitiesDatabase[region] : [];
}

// Get all universities
function getAllUniversities() {
    const all = [];
    Object.values(universitiesDatabase).forEach(region => {
        all.push(...region);
    });
    return all;
}

// Search universities
function searchUniversities(query) {
    const all = getAllUniversities();
    const searchTerm = query.toLowerCase();
    return all.filter(uni =>
        uni.name.toLowerCase().includes(searchTerm) ||
        uni.city.toLowerCase().includes(searchTerm) ||
        uni.program.toLowerCase().includes(searchTerm)
    );
}

// Generate university card HTML
function generateUniversityCard(university) {
    return `
        <div class="university-card">
            <div class="university-header">
                <h3>${university.name}</h3>
                <span class="university-badge">${university.country}</span>
            </div>
            <div class="university-details">
                <p><strong>Program:</strong> ${university.program}</p>
                <p><strong>Degree:</strong> ${university.degree}</p>
                <p><strong>Duration:</strong> ${university.duration}</p>
                <p><strong>Location:</strong> ${university.city}</p>
                <p><strong>Accreditation:</strong> ${university.accreditation}</p>
                ${university.established ? `<p><strong>Established:</strong> ${university.established}</p>` : ''}
            </div>
            <div class="university-actions">
                <a href="${university.syllabusURL}" target="_blank" class="btn-link">
                    <i class="fas fa-external-link-alt"></i> View Program
                </a>
                <a href="tel:${university.contact}" class="btn-link">
                    <i class="fas fa-phone"></i> Contact
                </a>
            </div>
        </div>
    `;
}
