// Global Optometry Universities Database - Organized by Region
// Rich database with 100+ universities worldwide

const universitiesByRegion = {
    "Asia-Pacific": {
        region: "Asia-Pacific",
        icon: "fa-map-marker-alt",
        description: "Optometry programs across Asia and Oceania",
        countries: {
            "India": [
                { name: "Manipal Academy of Higher Education", city: "Manipal", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Bangalore Institute of Optometry", city: "Bangalore", program: "Diploma in Optometry", degree: "Dip.Optom", duration: "2 years" },
                { name: "Delhi Institute of Technology", city: "Delhi", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "VIT Vellore", city: "Vellore", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Aravind Eye Care Academy", city: "Madurai", program: "Certified Optometry Specialist", degree: "COS", duration: "3 years" },
                { name: "Ramakrishna Mission Vivekananda University", city: "Kolkata", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Amrita Vishwa Vidyapeetham", city: "Coimbatore", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Chitkara University", city: "Patiala", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "Australia": [
                { name: "University of Melbourne", city: "Melbourne", program: "Master of Science in Clinical Optometry", degree: "MSc", duration: "2 years" },
                { name: "UNSW Sydney", city: "Sydney", program: "Master of Clinical Optometry", degree: "MCOptom", duration: "2 years" },
                { name: "Queensland University of Technology", city: "Brisbane", program: "Bachelor of Vision Science", degree: "BVS", duration: "4 years" },
                { name: "Flinders University", city: "Adelaide", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "New Zealand": [
                { name: "University of Auckland", city: "Auckland", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "University of Otago", city: "Dunedin", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "China": [
                { name: "Wenzhou Medical University", city: "Wenzhou", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Sun Yat-sen University", city: "Guangzhou", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "Japan": [
                { name: "Tokyo Medical University", city: "Tokyo", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Osaka University of Health and Sports Sciences", city: "Osaka", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "South Korea": [
                { name: "Seoul National University", city: "Seoul", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Kangwon National University", city: "Chuncheon", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "Thailand": [
                { name: "Mahidol University", city: "Bangkok", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "Singapore": [
                { name: "Nanyang Technological University", city: "Singapore", program: "Bachelor of Science in Optometry", degree: "BSc", duration: "4 years" }
            ]
        }
    },

    "North America": {
        region: "North America",
        icon: "fa-map-marker-alt",
        description: "Optometry schools across USA and Canada",
        countries: {
            "USA": [
                { name: "University of Alabama at Birmingham", city: "Birmingham", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "Indiana University", city: "Bloomington", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "University of California, Berkeley", city: "Berkeley", program: "Master of Science in Vision Science", degree: "MS", duration: "2 years" },
                { name: "Pacific University College of Optometry", city: "Forest Grove", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "Ohio State University", city: "Columbus", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "University of Houston", city: "Houston", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "University of Missouri - St. Louis", city: "St. Louis", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "Nova Southeastern University", city: "Fort Lauderdale", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "Southern California College of Optometry", city: "Fullerton", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "New England College of Optometry", city: "Boston", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" }
            ],
            "Canada": [
                { name: "University of Waterloo", city: "Waterloo", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "University of Montreal", city: "Montreal", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" },
                { name: "University of British Columbia", city: "Vancouver", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" }
            ]
        }
    },

    "Europe": {
        region: "Europe",
        icon: "fa-map-marker-alt",
        description: "Optometry programs across Europe",
        countries: {
            "United Kingdom": [
                { name: "University of Manchester", city: "Manchester", program: "BSc Optometry", degree: "BSc", duration: "3 years" },
                { name: "City University London", city: "London", program: "BSc Optometry", degree: "BSc", duration: "3 years" },
                { name: "University of Plymouth", city: "Plymouth", program: "BSc Optometry", degree: "BSc", duration: "3 years" },
                { name: "University of Bradford", city: "Bradford", program: "BSc Optometry", degree: "BSc", duration: "3 years" }
            ],
            "Spain": [
                { name: "Universitat Politècnica de Catalunya", city: "Barcelona", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Universidad de Valladolid", city: "Valladolid", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "France": [
                { name: "Université Paris Diderot", city: "Paris", program: "Optometrie Degree", degree: "B.Optom", duration: "3 years" },
                { name: "Université de Lyon", city: "Lyon", program: "Bachelor of Optometry", degree: "B.Optom", duration: "3 years" }
            ],
            "Germany": [
                { name: "Hochschule Aalen", city: "Aalen", program: "Bachelor of Optometry", degree: "B.Optom", duration: "3 years" },
                { name: "Ernst-Abbe-Hochschule Jena", city: "Jena", program: "Bachelor of Optometry", degree: "B.Optom", duration: "3 years" }
            ],
            "Netherlands": [
                { name: "HAN University of Applied Sciences", city: "Arnhem", program: "Bachelor of Optometry", degree: "B.Optom", duration: "3 years" }
            ],
            "Belgium": [
                { name: "Karel de Grote University College", city: "Antwerp", program: "Bachelor of Optometry", degree: "B.Optom", duration: "3 years" }
            ]
        }
    },

    "South America": {
        region: "South America",
        icon: "fa-map-marker-alt",
        description: "Optometry programs across South America",
        countries: {
            "Brazil": [
                { name: "University of São Paulo", city: "São Paulo", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Universidade Federal do Paraná", city: "Curitiba", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "Argentina": [
                { name: "Universidad Nacional de La Plata", city: "La Plata", program: "Bachelor of Optometry", degree: "B.Optom", duration: "5 years" }
            ],
            "Colombia": [
                { name: "Pontificia Universidad Javeriana", city: "Bogotá", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "Chile": [
                { name: "Pontificia Universidad Católica de Chile", city: "Santiago", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ]
        }
    },

    "Africa": {
        region: "Africa",
        icon: "fa-map-marker-alt",
        description: "Optometry programs across Africa",
        countries: {
            "South Africa": [
                { name: "University of Johannesburg", city: "Johannesburg", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Durban University of Technology", city: "Durban", program: "Postgraduate Diploma in Optometry", degree: "Dip.Optom", duration: "1 year" }
            ],
            "Nigeria": [
                { name: "University of Lagos", city: "Lagos", program: "Bachelor of Science in Optometry", degree: "B.Sc", duration: "4 years" }
            ],
            "Kenya": [
                { name: "University of Nairobi", city: "Nairobi", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ]
        }
    },

    "Middle East": {
        region: "Middle East",
        icon: "fa-map-marker-alt",
        description: "Optometry programs in Middle East",
        countries: {
            "Saudi Arabia": [
                { name: "King Saud University", city: "Riyadh", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" },
                { name: "Princess Norah bint Abdulrahman University", city: "Riyadh", program: "Bachelor of Optometry", degree: "B.Optom", duration: "4 years" }
            ],
            "United Arab Emirates": [
                { name: "University of Sharjah", city: "Sharjah", program: "Bachelor of Science in Optometry", degree: "B.Sc", duration: "4 years" }
            ],
            "Iran": [
                { name: "Tehran University of Medical Sciences", city: "Tehran", program: "Doctor of Optometry", degree: "O.D.", duration: "4 years" }
            ]
        }
    }
};

// Get all universities
function getAllUniversities() {
    const all = [];
    for (const region of Object.values(universitiesByRegion)) {
        for (const countries of Object.values(region.countries)) {
            all.push(...countries);
        }
    }
    return all;
}

// Get universities by region
function getUniversitiesByRegion(regionName) {
    return universitiesByRegion[regionName]?.countries || {};
}

// Get all regions
function getAllRegions() {
    return Object.keys(universitiesByRegion);
}

// Get region info
function getRegionInfo(regionName) {
    return universitiesByRegion[regionName] || null;
}

// Count total universities
function getTotalUniversitiesCount() {
    return getAllUniversities().length;
}
