// Course Organization by Topic
// Groups similar courses together for better learning paths

const courseTopics = {
    "Optics & Refraction": {
        description: "Light, optics, refraction, lens design, and vision correction",
        icon: "fa-glasses",
        courses: [1, 2, 3, 4, 5, 6, 237] // Course IDs
    },
    "Ocular Anatomy & Physiology": {
        description: "Eye structure, visual system, and biological functions",
        icon: "fa-eye",
        courses: [7, 8, 9, 10, 11, 12]
    },
    "Clinical Skills & Examination": {
        description: "Patient examination, diagnostic techniques, and clinical procedures",
        icon: "fa-stethoscope",
        courses: [13, 14, 15, 16, 17]
    },
    "Contact Lens Practice": {
        description: "Contact lens fitting, design, and specialized applications",
        icon: "fa-circle",
        courses: [18, 19]
    },
    "Ocular Diseases & Pathology": {
        description: "Eye disease diagnosis, pathology, and management",
        icon: "fa-hospital",
        courses: [20, 21, 22, 23, 24, 25, 26, 27, 28]
    },
    "Pediatric Vision & Development": {
        description: "Children's eye care, refractive errors, and vision development",
        icon: "fa-child",
        courses: [29, 30]
    },
    "Systemic & Occupational Vision": {
        description: "Systemic diseases affecting vision, occupational eye health",
        icon: "fa-heart",
        courses: [31, 32, 33, 34, 35]
    },
    "Advanced Clinical Topics": {
        description: "Specialized areas: low vision, sports vision, professional care",
        icon: "fa-graduation-cap",
        courses: [36, 37, 38, 39, 40, 41, 42]
    }
};

// Get courses for a specific topic
function getCoursesForTopic(topicName) {
    const topic = courseTopics[topicName];
    if (!topic) return [];

    return topic.courses
        .map(courseId => coursesData.find(c => c.id === courseId))
        .filter(c => c !== undefined);
}

// Get all topics
function getAllTopics() {
    return Object.keys(courseTopics).map(name => ({
        name: name,
        ...courseTopics[name]
    }));
}

// Organize all courses by topic
function getOrganizedCourses() {
    const organized = {};

    for (const [topic, data] of Object.entries(courseTopics)) {
        organized[topic] = getCoursesForTopic(topic);
    }

    return organized;
}
