// Faculty Dashboard - Customized Lecture Note Selector
// Allows faculty to select topics and generate custom teaching materials

class FacultyDashboard {
    constructor() {
        this.selectedTopics = [];
        this.selectedCourses = [];
        this.selectedMaterials = [];
    }

    // Initialize faculty dashboard
    init() {
        this.createDashboardUI();
        this.setupEventListeners();
    }

    // Create dashboard HTML
    createDashboardUI() {
        const dashboard = document.getElementById('faculty-dashboard');
        if (!dashboard) return;

        dashboard.innerHTML = `
            <div class="dashboard-container">
                <h2>Faculty Teaching Materials Builder</h2>
                <p class="subtitle">Select courses and topics to generate customized lecture note packages</p>

                <div class="dashboard-layout">
                    <!-- Left: Course Selection -->
                    <aside class="dashboard-sidebar">
                        <div class="selection-group">
                            <h3>Step 1: Select Courses</h3>
                            <div id="course-selector" class="course-selector">
                                <!-- Dynamically populated -->
                            </div>
                        </div>

                        <div class="selection-group">
                            <h3>Step 2: Select Topics</h3>
                            <div id="topic-selector" class="topic-selector">
                                <!-- Dynamically populated -->
                            </div>
                        </div>

                        <div class="selection-group">
                            <h3>Step 3: Select Materials</h3>
                            <div id="material-type-selector">
                                <label>
                                    <input type="checkbox" name="material-type" value="lectures" checked>
                                    Lecture Presentations
                                </label>
                                <label>
                                    <input type="checkbox" name="material-type" value="notes" checked>
                                    Reading Notes
                                </label>
                                <label>
                                    <input type="checkbox" name="material-type" value="practicals" checked>
                                    Practical Guides
                                </label>
                                <label>
                                    <input type="checkbox" name="material-type" value="syllabus" checked>
                                    Syllabus & References
                                </label>
                            </div>
                        </div>
                    </aside>

                    <!-- Right: Preview & Download -->
                    <main class="dashboard-main">
                        <div class="preview-section">
                            <h3>Selected Materials Preview</h3>
                            <div id="selection-preview" class="selection-preview">
                                <p class="placeholder">Select courses and topics to see materials</p>
                            </div>
                        </div>

                        <div class="actions-section">
                            <button class="btn-download" id="download-selected">
                                <i class="fas fa-download"></i> Download Selected Materials
                            </button>
                            <button class="btn-secondary" id="generate-syllabus">
                                <i class="fas fa-file-pdf"></i> Generate Custom Syllabus
                            </button>
                            <button class="btn-secondary" id="share-package">
                                <i class="fas fa-share-alt"></i> Share with Students
                            </button>
                        </div>

                        <div class="summary-section">
                            <h4>Summary</h4>
                            <ul id="selection-summary">
                                <li>Courses Selected: <strong id="course-count">0</strong></li>
                                <li>Topics Selected: <strong id="topic-count">0</strong></li>
                                <li>Materials Total: <strong id="material-count">0</strong></li>
                                <li>Estimated Size: <strong id="size-estimate">0 MB</strong></li>
                            </ul>
                        </div>
                    </main>
                </div>
            </div>
        `;
    }

    // Populate course selector
    populateCourseSelector() {
        const selector = document.getElementById('course-selector');
        if (!selector) return;

        const courses = [
            { id: 'anatomy', name: 'Ocular Anatomy & Physiology', icon: 'fa-eye' },
            { id: 'optics', name: 'Physical Optics', icon: 'fa-glasses' },
            { id: 'strabismus', name: 'Strabismus', icon: 'fa-arrows-alt' },
            { id: 'biostatistics', name: 'Biostatistics', icon: 'fa-chart-bar' },
            { id: 'pediatric', name: 'Pediatric Optometry', icon: 'fa-child' },
            { id: 'safety', name: 'Occupational Safety', icon: 'fa-hard-hat' }
        ];

        selector.innerHTML = courses.map(course => `
            <label class="course-option">
                <input type="checkbox" class="course-selector-input" value="${course.id}">
                <i class="fas ${course.icon}"></i>
                <span>${course.name}</span>
            </label>
        `).join('');
    }

    // Generate customized syllabus
    generateSyllabus() {
        const courseName = this.getSelectedCourseNames().join(', ');
        const topics = this.selectedTopics.join(', ');
        const date = new Date().toLocaleDateString();

        const syllabus = `
CUSTOM SYLLABUS
Generated from OLH - Optometry Learning Hub

Course(s): ${courseName}
Generated: ${date}
Selected Topics: ${topics}

This custom syllabus has been generated using the OLH Faculty Dashboard.
All materials included are sourced from world-class optometry programs
and include complete textbook references.

Source: https://nathantechz.github.io/ovs
GitHub Repository: https://github.com/nathantechz/ovs
        `;

        this.downloadAsFile(syllabus, 'OLH_Custom_Syllabus.txt');
    }

    // Share with students
    sharePackage() {
        const courseName = this.getSelectedCourseNames().join(', ');
        const shareLink = `
Course Package Created from OLH

Courses: ${courseName}
Topics Selected: ${this.selectedTopics.join(', ')}
Materials: ${this.selectedMaterials.length} items

Access Full Library: https://nathantechz.github.io/ovs
Download These Materials: [Download link will be generated]

All materials are accessible from OLH - Optometry Learning Hub
        `;

        // Copy to clipboard
        navigator.clipboard.writeText(shareLink).then(() => {
            alert('Share text copied to clipboard!\n\n' + shareLink);
        }).catch(() => {
            alert('Share text (copy manually):\n\n' + shareLink);
        });
    }

    // Get selected course names
    getSelectedCourseNames() {
        const courseMap = {
            'anatomy': 'Ocular Anatomy & Physiology',
            'optics': 'Physical Optics',
            'strabismus': 'Strabismus',
            'biostatistics': 'Biostatistics',
            'pediatric': 'Pediatric Optometry',
            'safety': 'Occupational Safety'
        };

        return this.selectedCourses.map(id => courseMap[id] || id);
    }

    // Download as file
    downloadAsFile(content, filename) {
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    // Setup event listeners
    setupEventListeners() {
        // Course selection
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('course-selector-input')) {
                if (e.target.checked) {
                    this.selectedCourses.push(e.target.value);
                } else {
                    this.selectedCourses = this.selectedCourses.filter(c => c !== e.target.value);
                }
                this.updatePreview();
            }
        });

        // Download button
        const downloadBtn = document.getElementById('download-selected');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                if (this.selectedCourses.length === 0) {
                    alert('Please select at least one course');
                    return;
                }
                alert('Download package prepared!\n\nCourses: ' + this.getSelectedCourseNames().join(', ') + '\n\nThe files will be organized in a folder structure for easy access.');
            });
        }

        // Generate syllabus
        const syllabusBtn = document.getElementById('generate-syllabus');
        if (syllabusBtn) {
            syllabusBtn.addEventListener('click', () => this.generateSyllabus());
        }

        // Share package
        const shareBtn = document.getElementById('share-package');
        if (shareBtn) {
            shareBtn.addEventListener('click', () => this.sharePackage());
        }
    }

    // Update preview
    updatePreview() {
        const preview = document.getElementById('selection-preview');
        if (!preview) return;

        if (this.selectedCourses.length === 0) {
            preview.innerHTML = '<p class="placeholder">Select courses and topics to see materials</p>';
            return;
        }

        const courseNames = this.getSelectedCourseNames();
        const html = `
            <div class="preview-items">
                <h4>Selected Courses:</h4>
                <ul>
                    ${courseNames.map(name => `<li><i class="fas fa-check"></i> ${name}</li>`).join('')}
                </ul>
                <p class="info-text">
                    Your custom teaching package includes:
                    <br>✓ Lecture presentations
                    <br>✓ Reading notes
                    <br>✓ Practical guides
                    <br>✓ Textbook references
                    <br>✓ All materials watermarked with OLH branding
                </p>
            </div>
        `;

        preview.innerHTML = html;
        this.updateSummary();
    }

    // Update summary counts
    updateSummary() {
        document.getElementById('course-count').textContent = this.selectedCourses.length;
        document.getElementById('topic-count').textContent = this.selectedTopics.length || 'All topics';
        document.getElementById('material-count').textContent = this.calculateMaterialCount();
        document.getElementById('size-estimate').textContent = this.estimateSize();
    }

    // Calculate materials count
    calculateMaterialCount() {
        // Rough estimate: 8 lectures + 8 notes + 5 practicals per course
        return (this.selectedCourses.length * 21).toString();
    }

    // Estimate download size
    estimateSize() {
        // Rough estimate: 50MB per course worth of materials
        const sizeMB = this.selectedCourses.length * 50;
        return sizeMB + ' MB';
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new FacultyDashboard();
    dashboard.init();
    dashboard.populateCourseSelector();
});
