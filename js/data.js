const coursesData = [
    // Refraction & Optics Courses
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
        degree: "Bachelor of Optometry"
    },
    {
        id: 2,
        title: "Advanced Optics & Lens Design",
        category: "refraction",
        level: "graduate",
        country: "uk",
        description: "Deep dive into optical physics, aberrations, and advanced lens technologies",
        icon: "fa-glasses",
        lectures: 14,
        materials: 28,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 3,
        title: "Geometric Optics",
        category: "refraction",
        level: "undergraduate",
        country: "canada",
        description: "Foundation course on geometric optics, lens theory, and ray tracing",
        icon: "fa-glasses",
        lectures: 10,
        materials: 20,
        degree: "Doctor of Optometry"
    },
    {
        id: 4,
        title: "Aspheric & High-Order Aberrations",
        category: "refraction",
        level: "graduate",
        country: "australia",
        description: "Study of complex optical aberrations and correction strategies",
        icon: "fa-glasses",
        lectures: 9,
        materials: 18,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 5,
        title: "Wavefront Analysis & Measurement",
        category: "refraction",
        level: "graduate",
        country: "usa",
        description: "Wavefront technology and its applications in refractive correction",
        icon: "fa-glasses",
        lectures: 11,
        materials: 22,
        degree: "Doctor of Optometry"
    },
    {
        id: 6,
        title: "Contact Lens Optics",
        category: "refraction",
        level: "undergraduate",
        country: "india",
        description: "Optical principles applied to contact lens design and fitting",
        icon: "fa-circle",
        lectures: 10,
        materials: 20,
        degree: "Bachelor of Optometry"
    },
    {
        id: 43,
        title: "Physical Optics",
        category: "refraction",
        level: "undergraduate",
        country: "usa",
        description: "Wave nature of light, interference, diffraction, and polarization phenomena",
        icon: "fa-lightbulb",
        lectures: 14,
        materials: 28,
        degree: "Bachelor of Optometry"
    },

    // Anatomy & Physiology Courses
    {
        id: 7,
        title: "Anatomy & Physiology of the Eye",
        category: "anatomy",
        level: "undergraduate",
        country: "usa",
        description: "Comprehensive study of ocular anatomy and visual system physiology",
        icon: "fa-eye",
        lectures: 14,
        materials: 28,
        degree: "Bachelor of Optometry"
    },
    {
        id: 8,
        title: "Retinal & Choroidal Structure",
        category: "anatomy",
        level: "graduate",
        country: "uk",
        description: "In-depth examination of posterior segment anatomy",
        icon: "fa-eye",
        lectures: 12,
        materials: 24,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 9,
        title: "Visual Neuroscience",
        category: "anatomy",
        level: "graduate",
        country: "australia",
        description: "Study of neural pathways and processing in vision",
        icon: "fa-brain",
        lectures: 13,
        materials: 26,
        degree: "Doctor of Optometry"
    },
    {
        id: 10,
        title: "Anterior Segment Anatomy",
        category: "anatomy",
        level: "undergraduate",
        country: "canada",
        description: "Detailed exploration of cornea, iris, lens, and anterior chamber",
        icon: "fa-eye",
        lectures: 11,
        materials: 22,
        degree: "Bachelor of Optometry"
    },
    {
        id: 11,
        title: "Binocular Vision Physiology",
        category: "anatomy",
        level: "undergraduate",
        country: "india",
        description: "Understanding vergence, accommodation, and eye movement coordination",
        icon: "fa-arrows-alt",
        lectures: 10,
        materials: 20,
        degree: "Bachelor of Optometry"
    },
    {
        id: 12,
        title: "Biochemistry of the Eye",
        category: "anatomy",
        level: "graduate",
        country: "usa",
        description: "Molecular mechanisms and metabolic processes in ocular tissues",
        icon: "fa-flask",
        lectures: 12,
        materials: 24,
        degree: "Master in Clinical Optometry"
    },

    // Clinical Skills Courses
    {
        id: 13,
        title: "Clinical Skills & Examinations",
        category: "clinical",
        level: "undergraduate",
        country: "usa",
        description: "Advanced clinical examination techniques including slit lamp and tonometry",
        icon: "fa-stethoscope",
        lectures: 10,
        materials: 20,
        degree: "Bachelor of Optometry"
    },
    {
        id: 14,
        title: "Slit Lamp Biomicroscopy",
        category: "clinical",
        level: "undergraduate",
        country: "uk",
        description: "Mastering anterior segment examination using slit lamp technology",
        icon: "fa-microscope",
        lectures: 8,
        materials: 16,
        degree: "Doctor of Optometry"
    },
    {
        id: 15,
        title: "Fundus Examination Techniques",
        category: "clinical",
        level: "graduate",
        country: "canada",
        description: "Advanced posterior segment examination and imaging interpretation",
        icon: "fa-stethoscope",
        lectures: 11,
        materials: 22,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 16,
        title: "Visual Field Testing & Interpretation",
        category: "clinical",
        level: "undergraduate",
        country: "australia",
        description: "Perimetry techniques and analysis of visual field defects",
        icon: "fa-chart-area",
        lectures: 9,
        materials: 18,
        degree: "Bachelor of Optometry"
    },
    {
        id: 17,
        title: "Tonometry & Intraocular Pressure Management",
        category: "clinical",
        level: "graduate",
        country: "usa",
        description: "Advanced IOP measurement techniques and clinical significance",
        icon: "fa-tachometer-alt",
        lectures: 10,
        materials: 20,
        degree: "Doctor of Optometry"
    },
    {
        id: 18,
        title: "Contact Lens Fitting & Management",
        category: "clinical",
        level: "undergraduate",
        country: "india",
        description: "Clinical practice in fitting various contact lens types",
        icon: "fa-circle",
        lectures: 12,
        materials: 24,
        degree: "Bachelor of Optometry"
    },
    {
        id: 19,
        title: "Specialized Contact Lens Applications",
        category: "clinical",
        level: "graduate",
        country: "uk",
        description: "Advanced fitting for keratoconus, post-surgical, and corneal ectasia",
        icon: "fa-circle",
        lectures: 10,
        materials: 20,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 20,
        title: "Refraction & Optical Correction",
        category: "clinical",
        level: "undergraduate",
        country: "canada",
        description: "Complete methodology for refractive examination and prescription writing",
        icon: "fa-glasses",
        lectures: 11,
        materials: 22,
        degree: "Doctor of Optometry"
    },

    // Ocular Diseases Courses
    {
        id: 21,
        title: "Ocular Diseases & Pathology",
        category: "ocular-diseases",
        level: "undergraduate",
        country: "usa",
        description: "Study of common ocular diseases, management strategies, and treatment options",
        icon: "fa-virus",
        lectures: 16,
        materials: 32,
        degree: "Bachelor of Optometry"
    },
    {
        id: 22,
        title: "Cataract Pathology & Management",
        category: "ocular-diseases",
        level: "graduate",
        country: "uk",
        description: "Classification, pathogenesis, and management of cataract",
        icon: "fa-virus",
        lectures: 10,
        materials: 20,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 23,
        title: "Glaucoma: Assessment & Treatment",
        category: "ocular-diseases",
        level: "graduate",
        country: "australia",
        description: "Comprehensive study of glaucoma diagnosis, classification, and therapy",
        icon: "fa-virus",
        lectures: 14,
        materials: 28,
        degree: "Doctor of Optometry"
    },
    {
        id: 24,
        title: "Retinal Diseases & Degeneration",
        category: "ocular-diseases",
        level: "graduate",
        country: "canada",
        description: "AMD, diabetic retinopathy, retinal detachment, and other posterior segment diseases",
        icon: "fa-virus",
        lectures: 15,
        materials: 30,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 25,
        title: "Corneal Pathology & Disease",
        category: "ocular-diseases",
        level: "undergraduate",
        country: "usa",
        description: "Infections, inflammations, and degenerations of the cornea",
        icon: "fa-virus",
        lectures: 11,
        materials: 22,
        degree: "Bachelor of Optometry"
    },
    {
        id: 26,
        title: "Neuro-Ophthalmology",
        category: "ocular-diseases",
        level: "graduate",
        country: "india",
        description: "Vision disorders related to nervous system pathology",
        icon: "fa-brain",
        lectures: 12,
        materials: 24,
        degree: "Doctor of Optometry"
    },
    {
        id: 27,
        title: "Uveitis & Inflammatory Conditions",
        category: "ocular-diseases",
        level: "graduate",
        country: "uk",
        description: "Diagnosis and management of intraocular inflammation",
        icon: "fa-virus",
        lectures: 11,
        materials: 22,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 28,
        title: "Pediatric Eye Disease",
        category: "ocular-diseases",
        level: "graduate",
        country: "australia",
        description: "Eye diseases specific to children and developmental disorders",
        icon: "fa-virus",
        lectures: 10,
        materials: 20,
        degree: "Doctor of Optometry"
    },
    {
        id: 29,
        title: "Refractive Errors in Children",
        category: "ocular-diseases",
        level: "undergraduate",
        country: "canada",
        description: "Myopia control, hyperopia, astigmatism, and presbyopia in young patients",
        icon: "fa-eye-slash",
        lectures: 9,
        materials: 18,
        degree: "Bachelor of Optometry"
    },
    {
        id: 30,
        title: "Systemic Diseases & Ocular Manifestations",
        category: "ocular-diseases",
        level: "graduate",
        country: "usa",
        description: "Ocular signs of systemic conditions including diabetes, hypertension, and autoimmune diseases",
        icon: "fa-virus",
        lectures: 12,
        materials: 24,
        degree: "Master in Clinical Optometry"
    },

    // Bachelor-specific advanced courses
    {
        id: 31,
        title: "Patient Communication & Counseling",
        category: "clinical",
        level: "undergraduate",
        country: "usa",
        description: "Effective communication strategies and patient education techniques",
        icon: "fa-handshake",
        lectures: 8,
        materials: 16,
        degree: "Bachelor of Optometry"
    },
    {
        id: 32,
        title: "Pharmacology for Optometry",
        category: "clinical",
        level: "undergraduate",
        country: "uk",
        description: "Drug actions, side effects, and therapeutic use in eye care",
        icon: "fa-pills",
        lectures: 10,
        materials: 20,
        degree: "Bachelor of Optometry"
    },
    {
        id: 33,
        title: "Public Health & Epidemiology",
        category: "anatomy",
        level: "undergraduate",
        country: "australia",
        description: "Eye health in populations and disease prevention strategies",
        icon: "fa-globe",
        lectures: 8,
        materials: 16,
        degree: "Bachelor of Optometry"
    },

    // Master-specific advanced courses
    {
        id: 34,
        title: "Advanced Diagnostic Imaging",
        category: "clinical",
        level: "graduate",
        country: "canada",
        description: "OCT, fundus photography, fluorescein angiography, and interpretation",
        icon: "fa-image",
        lectures: 12,
        materials: 24,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 35,
        title: "Surgical Considerations in Optometry",
        category: "clinical",
        level: "graduate",
        country: "usa",
        description: "Pre- and post-operative management of surgical patients",
        icon: "fa-user-doctor",
        lectures: 10,
        materials: 20,
        degree: "Master in Clinical Optometry"
    },
    {
        id: 36,
        title: "Research Methods & Statistics",
        category: "refraction",
        level: "graduate",
        country: "india",
        description: "Epidemiological methods and evidence-based practice",
        icon: "fa-chart-bar",
        lectures: 9,
        materials: 18,
        degree: "Master in Clinical Optometry"
    },

    // Doctor-specific advanced courses
    {
        id: 37,
        title: "Advanced Ocular Pharmacology",
        category: "clinical",
        level: "graduate",
        country: "uk",
        description: "Therapeutic drugs, treatment protocols, and adverse effects",
        icon: "fa-pills",
        lectures: 11,
        materials: 22,
        degree: "Doctor of Optometry"
    },
    {
        id: 38,
        title: "Therapeutic Optometry",
        category: "clinical",
        level: "graduate",
        country: "australia",
        description: "Pharmacological management of ocular diseases within optometric scope",
        icon: "fa-clinic-medical",
        lectures: 12,
        materials: 24,
        degree: "Doctor of Optometry"
    },
    {
        id: 39,
        title: "Practice Management & Entrepreneurship",
        category: "clinical",
        level: "graduate",
        country: "canada",
        description: "Business skills, marketing, and clinical practice leadership",
        icon: "fa-chart-line",
        lectures: 8,
        materials: 16,
        degree: "Doctor of Optometry"
    },
    {
        id: 40,
        title: "Clinical Research & Evidence Synthesis",
        category: "refraction",
        level: "graduate",
        country: "usa",
        description: "Conducting and evaluating clinical research in optometry",
        icon: "fa-flask-vial",
        lectures: 10,
        materials: 20,
        degree: "Doctor of Optometry"
    },
    {
        id: 41,
        title: "Specialty Clinics & Case Management",
        category: "clinical",
        level: "graduate",
        country: "india",
        description: "Management of complex cases in specialized clinical settings",
        icon: "fa-stethoscope",
        lectures: 11,
        materials: 22,
        degree: "Doctor of Optometry"
    },
    {
        id: 42,
        title: "Digital Vision & Ergonomics",
        category: "clinical",
        level: "graduate",
        country: "uk",
        description: "Computer vision syndrome, digital eye strain, and workplace optimization",
        icon: "fa-computer",
        lectures: 9,
        materials: 18,
        degree: "Doctor of Optometry"
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
    },
    {
        id: 9,
        title: "Doctor of Optometry (OD)",
        university: "Indiana University",
        country: "USA",
        region: "North America",
        description: "Four-year professional doctorate with extensive clinical externships",
        icon: "fa-university",
        link: "#"
    },
    {
        id: 10,
        title: "Master of Science in Vision Science",
        university: "University of California, Berkeley",
        country: "USA",
        region: "North America",
        description: "Research-focused program in vision science and optical technology",
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
