const coursesData = [
    {
        id: 1,
        title: "Refraction & Optics Fundamentals",
        category: "refraction",
        level: "undergraduate",
        country: "usa",
        description: "Master the principles of light refraction, lens optics, and spectacle prescription",
        icon: "fa-glasses",
        lectures: 12,
        materials: 24,
        resources: [
            { name: "Refraction Basics", type: "pdf", url: "#" },
            { name: "Lens Properties", type: "pdf", url: "#" },
            { name: "Spherical Aberration", type: "pdf", url: "#" }
        ]
    },
    {
        id: 2,
        title: "Anatomy & Physiology of the Eye",
        category: "anatomy",
        level: "undergraduate",
        country: "usa",
        description: "Comprehensive study of ocular anatomy and visual system physiology",
        icon: "fa-eye",
        lectures: 14,
        materials: 28,
        resources: [
            { name: "Eye Anatomy Overview", type: "pdf", url: "#" },
            { name: "Retinal Structure", type: "pdf", url: "#" },
            { name: "Visual Pathways", type: "pdf", url: "#" }
        ]
    },
    {
        id: 3,
        title: "Clinical Skills & Examinations",
        category: "clinical",
        level: "graduate",
        country: "uk",
        description: "Advanced clinical examination techniques including slit lamp and tonometry",
        icon: "fa-stethoscope",
        lectures: 10,
        materials: 20,
        resources: [
            { name: "Slit Lamp Technique", type: "pdf", url: "#" },
            { name: "Tonometry Guide", type: "pdf", url: "#" },
            { name: "Visual Field Testing", type: "pdf", url: "#" }
        ]
    },
    {
        id: 4,
        title: "Ocular Diseases & Pathology",
        category: "ocular-diseases",
        level: "graduate",
        country: "australia",
        description: "Study of common ocular diseases, management strategies, and treatment options",
        icon: "fa-virus",
        lectures: 16,
        materials: 32,
        resources: [
            { name: "Cataract Pathology", type: "pdf", url: "#" },
            { name: "Glaucoma Management", type: "pdf", url: "#" },
            { name: "Retinal Diseases", type: "pdf", url: "#" }
        ]
    },
    {
        id: 5,
        title: "Refractive Errors",
        category: "refraction",
        level: "undergraduate",
        country: "canada",
        description: "Deep dive into myopia, hyperopia, astigmatism, and presbyopia",
        icon: "fa-eye-slash",
        lectures: 8,
        materials: 16,
        resources: [
            { name: "Myopia Overview", type: "pdf", url: "#" },
            { name: "Hyperopia Correction", type: "pdf", url: "#" },
            { name: "Astigmatism Analysis", type: "pdf", url: "#" }
        ]
    },
    {
        id: 6,
        title: "Contact Lens Practice",
        category: "clinical",
        level: "clinical-practice",
        country: "usa",
        description: "Clinical applications of contact lens fitting and patient management",
        icon: "fa-circle",
        lectures: 10,
        materials: 18,
        resources: [
            { name: "Lens Fitting Basics", type: "pdf", url: "#" },
            { name: "RGP Lenses", type: "pdf", url: "#" },
            { name: "Soft Lens Complications", type: "pdf", url: "#" }
        ]
    },
    {
        id: 7,
        title: "Binocular Vision & Eye Movement",
        category: "anatomy",
        level: "graduate",
        country: "uk",
        description: "Understanding vergence, accommodation, and oculomotor control",
        icon: "fa-arrows-alt",
        lectures: 11,
        materials: 22,
        resources: [
            { name: "Binocular Basics", type: "pdf", url: "#" },
            { name: "Accommodation Physics", type: "pdf", url: "#" },
            { name: "Strabismus Review", type: "pdf", url: "#" }
        ]
    },
    {
        id: 8,
        title: "Low Vision & Rehabilitation",
        category: "clinical",
        level: "graduate",
        country: "india",
        description: "Managing patients with visual impairment and rehabilitation strategies",
        icon: "fa-handshake",
        lectures: 9,
        materials: 17,
        resources: [
            { name: "Low Vision Assessment", type: "pdf", url: "#" },
            { name: "Optical Aids", type: "pdf", url: "#" },
            { name: "Patient Counseling", type: "pdf", url: "#" }
        ]
    }
];

const resourcesData = [
    {
        id: 1,
        title: "Bachelor of Science in Optometry",
        university: "University of Alabama",
        country: "USA",
        region: "North America",
        description: "Four-year comprehensive optometry program with emphasis on clinical practice and patient care",
        icon: "fa-university",
        link: "#"
    },
    {
        id: 2,
        title: "BSc Optometry Programme",
        university: "University of Manchester",
        country: "United Kingdom",
        region: "Europe",
        description: "Three-year honors degree program covering optics, physiology, and clinical optometry",
        icon: "fa-university",
        link: "#"
    },
    {
        id: 3,
        title: "Master of Science in Clinical Optometry",
        university: "University of Melbourne",
        country: "Australia",
        region: "Oceania",
        description: "Advanced clinical training with research opportunities in visual science",
        icon: "fa-university",
        link: "#"
    },
    {
        id: 4,
        title: "Doctor of Optometry (OD)",
        university: "University of Waterloo",
        country: "Canada",
        region: "North America",
        description: "Professional doctorate program combining classroom and clinic-based education",
        icon: "fa-university",
        link: "#"
    },
    {
        id: 5,
        title: "Bachelor of Optometry",
        university: "Delhi Institute of Technology",
        country: "India",
        region: "Asia",
        description: "Four-year degree program focusing on vision care and eye disease management in developing countries",
        icon: "fa-university",
        link: "#"
    },
    {
        id: 6,
        title: "Optometrie Degree",
        university: "Université Paris Diderot",
        country: "France",
        region: "Europe",
        description: "Comprehensive training in refractive error management and ocular disease",
        icon: "fa-university",
        link: "#"
    },
    {
        id: 7,
        title: "Bachelor of Optometry Science",
        university: "University of Auckland",
        country: "New Zealand",
        region: "Oceania",
        description: "Three-year program emphasizing clinical competence and community eye health",
        icon: "fa-university",
        link: "#"
    },
    {
        id: 8,
        title: "Postgraduate Diploma in Optometry",
        university: "Durban University of Technology",
        country: "South Africa",
        region: "Africa",
        description: "Advanced specialization in pediatric optometry and low-vision rehabilitation",
        icon: "fa-university",
        link: "#"
    }
];

const categories = [
    { id: "refraction", name: "Refraction & Optics", icon: "fa-glasses" },
    { id: "anatomy", name: "Anatomy & Physiology", icon: "fa-dna" },
    { id: "clinical", name: "Clinical Skills", icon: "fa-stethoscope" },
    { id: "ocular-diseases", name: "Ocular Diseases", icon: "fa-virus" }
];

const levels = [
    { id: "undergraduate", name: "Undergraduate" },
    { id: "graduate", name: "Graduate" },
    { id: "clinical-practice", name: "Clinical Practice" }
];

const countries = [
    { code: "usa", name: "USA" },
    { code: "uk", name: "United Kingdom" },
    { code: "canada", name: "Canada" },
    { code: "australia", name: "Australia" },
    { code: "india", name: "India" },
    { code: "france", name: "France" },
    { code: "others", name: "Other Countries" }
];
