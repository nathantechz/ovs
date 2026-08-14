# OVS - Optometry Virtual Study Platform

A comprehensive, world-class optometry education platform providing lecture notes, syllabuses, and learning materials from top optometry programs worldwide.

## 🎯 Overview

OVS (Optometry Virtual Study Platform) is a free, open-source educational resource hub designed for:
- **Optometry Students** - Access quality lecture notes and study materials
- **Faculty & Educators** - Share curricula and teaching resources globally
- **Patients & Community** - Learn about eye health and optometry concepts

## ✨ Features

- 📚 **Comprehensive Course Library** - 150+ lecture notes across multiple topics
- 🌍 **Global Perspective** - Syllabuses and materials from 25+ universities across 10+ countries
- 📱 **Responsive Design** - Perfect viewing on desktop, tablet, and mobile devices
- 🔍 **Advanced Search** - Find courses and topics easily with our search functionality
- 📊 **Anonymous Analytics** - Track usage without collecting personal data
- 📥 **Easy Downloads** - Access PDFs and materials for offline study
- 🎓 **Quality Content** - World-class explanations of complex optometry concepts

## 📚 Course Topics

### 1. **Refraction & Optics**
   - Lens properties and principles
   - Spectacle prescription and fitting
   - Advanced optical concepts

### 2. **Anatomy & Physiology**
   - Ocular anatomy in detail
   - Visual system pathways
   - Retinal structure and function

### 3. **Clinical Skills & Examinations**
   - Slit lamp examination techniques
   - Tonometry and IOP measurement
   - Visual field testing
   - Contact lens fitting

### 4. **Ocular Diseases & Pathology**
   - Cataract pathology and management
   - Glaucoma: assessment and treatment
   - Retinal diseases and degeneration
   - Corneal conditions

## 🌐 Represented Countries

- 🇺🇸 United States
- 🇬🇧 United Kingdom
- 🇨🇦 Canada
- 🇦🇺 Australia
- 🇮🇳 India
- 🇫🇷 France
- 🇳🇿 New Zealand
- 🇿🇦 South Africa
- ...and more!

## 🚀 Getting Started

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/nathantechz/ovs.git
cd ovs
```

2. **View locally (option 1 - using Python):**
```bash
python -m http.server 8000
# or for Python 2
python -m SimpleHTTPServer 8000
```

Then open http://localhost:8000 in your browser.

3. **View locally (option 2 - using Node.js):**
```bash
npm install -g http-server
http-server
```

### GitHub Pages Deployment

The site is automatically deployed to GitHub Pages whenever you push to the main branch.

Access it at: https://nathantechz.github.io/ovs

## 📁 Project Structure

```
ovs/
├── index.html              # Main homepage
├── css/
│   └── styles.css          # All styling (responsive design)
├── js/
│   ├── app.js              # Main application logic
│   └── data.js             # Course and resource data
├── courses/                # Course content (to be populated)
│   ├── refraction/
│   ├── anatomy/
│   ├── clinical-skills/
│   └── ocular-diseases/
├── resources/              # University syllabuses
├── assets/                 # Images, icons, etc.
├── _config.yml             # Jekyll/GitHub Pages config
└── README.md              # This file
```

## 📝 Content Management

### Adding New Courses

1. Update `js/data.js` with course information:
```javascript
{
    id: 9,
    title: "Your Course Title",
    category: "refraction", // or anatomy, clinical, ocular-diseases
    level: "undergraduate", // or graduate, clinical-practice
    country: "usa",
    description: "Course description",
    icon: "fa-glasses",
    lectures: 12,
    materials: 24,
    resources: [...]
}
```

2. Create course folder in `courses/` directory
3. Add course materials (PDFs, notes, etc.)

### Adding University Resources

1. Update `js/data.js` with university information:
```javascript
{
    id: 9,
    title: "Program Name",
    university: "University Name",
    country: "Country",
    region: "Region",
    description: "Program description",
    icon: "fa-university",
    link: "https://..."
}
```

## 🔍 Search & Discovery

Users can:
- Search for courses by title or topic
- Filter by educational level (undergraduate/graduate/clinical)
- Filter by country/region
- Browse by category
- View featured content on homepage

## 📊 Analytics Setup

To enable Google Analytics:

1. Create a Google Analytics account
2. Get your Measurement ID (format: G-XXXXXXXXXX)
3. Update the GA ID in `index.html`:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR-ID"></script>
<script>
    gtag('config', 'G-YOUR-ID');
</script>
```

4. Uncomment the gtag config line in index.html

## 🎨 Customization

### Colors & Branding

Edit the CSS variables in `css/styles.css`:
```css
:root {
    --primary-color: #0066cc;
    --secondary-color: #00a854;
    /* ... other colors ... */
}
```

### Navigation & Structure

- Edit navigation links in `index.html` navbar
- Modify page sections in the main content area
- Adjust categories in `js/data.js`

## 🤝 Contributing

We welcome contributions from:
- Optometry educators and students
- Eye health professionals
- Content creators and writers
- Developers and designers

### How to Contribute

1. **Add Course Materials:**
   - Submit lecture notes, study guides, or teaching materials
   - Ensure proper attribution and copyright compliance

2. **Improve Content:**
   - Suggest edits or clarifications
   - Report errors or outdated information
   - Submit translations

3. **Enhance the Platform:**
   - Report bugs
   - Suggest features
   - Submit code improvements

### Contribution Guidelines

- All content must be original or properly attributed
- Follow academic integrity standards
- Include proper references and citations
- Test changes locally before submitting

## 📜 License

[Specify your license - MIT, Creative Commons, etc.]

## 📧 Contact & Support

- **Email:** info@ovs-education.org (when available)
- **GitHub Issues:** [Report bugs or request features](https://github.com/nathantechz/ovs/issues)
- **GitHub Discussions:** [Join our community](https://github.com/nathantechz/ovs/discussions)

## 🔮 Future Roadmap

- [ ] Interactive case studies and clinical scenarios
- [ ] Video lectures and tutorial videos
- [ ] Practice questions and self-assessment quizzes
- [ ] Community forums for peer learning
- [ ] AI-powered study recommendations
- [ ] Textbook content integration
- [ ] Interactive anatomy viewer
- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support
- [ ] Certification programs

## 📚 Sources & Attribution

Content is sourced from:
- Peer-reviewed academic publications
- Open Educational Resources (OER)
- University syllabuses (with permission)
- Published optometry textbooks (with proper attribution)
- Contributions from faculty and practitioners

## ⚠️ Disclaimer

This platform is designed for **educational purposes only**. The information provided should not be used for clinical diagnosis or treatment. Always consult with qualified eye care professionals for medical advice.

## 🙏 Acknowledgments

Special thanks to:
- All contributing educators and professionals
- The optometry education community
- Open source projects that make this possible
- Students and faculty providing feedback

## 📈 Statistics

- **Courses:** 150+
- **Materials:** 300+
- **Universities:** 25+
- **Countries:** 10+
- **Lecture Videos:** Coming soon
- **Interactive Tools:** In development

## 🔐 Privacy

- We collect **no personal data** through contact forms
- **Anonymous analytics only** to understand usage patterns
- No cookies or tracking pixels (except Google Analytics if enabled)
- No third-party data sharing

## 💡 Tips for Best Learning

1. **Start with fundamentals** - Begin with anatomy before pathology
2. **Read multiple sources** - Compare different teaching approaches
3. **Take notes** - Actively engage with the material
4. **Download PDFs** - Study offline at your pace
5. **Join communities** - Connect with other students (coming soon)
6. **Practice** - Apply knowledge to clinical scenarios (coming soon)

---

**Last Updated:** August 2026

**Version:** 1.0.0

**Built with ❤️ for optometry education worldwide**
