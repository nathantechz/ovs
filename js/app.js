// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    setupPageNavigation();
    setupEventListeners();
    renderFeaturedCourses();
    renderCategoriesFilter();
    renderResources();
    renderCourses();
    renderMaterials();
});

// Setup navigation between pages
function setupPageNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = link.getAttribute('data-page');

            // Hide all pages
            pages.forEach(page => page.classList.remove('active'));

            // Remove active from all nav links
            navLinks.forEach(l => l.classList.remove('active'));

            // Show selected page
            const selectedPage = document.getElementById(pageName);
            if (selectedPage) {
                selectedPage.classList.add('active');
                link.classList.add('active');
            }

            // Close mobile menu
            closeNavMenu();

            // Scroll to top
            window.scrollTo(0, 0);
        });
    });
}

// Setup event listeners
function setupEventListeners() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');

    // Mobile menu toggle
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Search functionality
    if (searchBtn) {
        searchBtn.addEventListener('click', performSearch);
    }

    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    // Filter listeners
    setupFilterListeners();
}

function closeNavMenu() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.remove('active');
}

// Render featured courses on homepage
function renderFeaturedCourses() {
    const container = document.getElementById('featuredCourses');
    if (!container) return;

    // Get top 4 featured courses
    const featured = coursesData.slice(0, 4);

    container.innerHTML = featured.map(course => `
        <div class="course-card" onclick="navigateToCourse(${course.id})">
            <div class="course-card-header">
                <div>
                    <i class="fas ${course.icon}"></i>
                    <div class="course-card-title">${course.title}</div>
                </div>
            </div>
            <div class="course-card-body">
                <p class="course-card-desc">${course.description}</p>
                <div class="course-card-footer">
                    <span><i class="fas fa-book"></i> ${course.lectures} Lectures</span>
                    <span><i class="fas fa-file"></i> ${course.materials} Materials</span>
                </div>
            </div>
        </div>
    `).join('');
}

// Render all courses
function renderCourses(filter = {}) {
    const container = document.getElementById('coursesGrid');
    if (!container) return;

    let filtered = coursesData;

    // Apply filters
    if (filter.category) {
        filtered = filtered.filter(c => c.category === filter.category);
    }
    if (filter.level) {
        filtered = filtered.filter(c => c.level === filter.level);
    }
    if (filter.country) {
        filtered = filtered.filter(c => c.country === filter.country);
    }
    if (filter.search) {
        const searchTerm = filter.search.toLowerCase();
        filtered = filtered.filter(c =>
            c.title.toLowerCase().includes(searchTerm) ||
            c.description.toLowerCase().includes(searchTerm)
        );
    }

    if (filtered.length === 0) {
        container.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 40px;">
                <i class="fas fa-search" style="font-size: 48px; color: #ccc; margin-bottom: 20px; display: block;"></i>
                <p style="color: var(--text-secondary);">No courses found matching your criteria.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = filtered.map(course => `
        <div class="course-card" onclick="navigateToCourse(${course.id})">
            <div class="course-card-header">
                <div style="width: 100%;">
                    <i class="fas ${course.icon}"></i>
                    <div class="course-card-title">${course.title}</div>
                </div>
            </div>
            <div class="course-card-body">
                <p class="course-card-desc">${course.description}</p>
                <div style="margin-bottom: 16px;">
                    <span class="course-badge">${getLevelName(course.level)}</span>
                    <span class="course-badge" style="background-color: #f0f9ff; color: #0066cc; margin-left: 8px;">${getCountryName(course.country)}</span>
                </div>
                <div class="course-card-footer">
                    <span><i class="fas fa-book"></i> ${course.lectures} Lectures</span>
                    <span><i class="fas fa-file"></i> ${course.materials} Materials</span>
                </div>
            </div>
        </div>
    `).join('');
}

// Render category filters
function renderCategoriesFilter() {
    const container = document.getElementById('categoryFilters');
    if (!container) return;

    container.innerHTML = categories.map(cat => `
        <label>
            <input type="checkbox" value="${cat.id}" class="category-filter">
            <i class="fas ${cat.icon}"></i> ${cat.name}
        </label>
    `).join('');
}

// Render materials for download
function renderMaterials() {
    const container = document.getElementById('materialsContainer');
    if (!container || typeof availableMaterials === 'undefined') return;

    const courses = getAvailableCourses();
    let html = '';

    courses.forEach(courseName => {
        html += renderMaterialsForDownload(courseName);
    });

    container.innerHTML = html;
}

// Render resources with regional organization
function renderResources() {
    const container = document.getElementById('resourcesGrid');
    if (!container) return;

    if (typeof universitiesByRegion === 'undefined') {
        container.innerHTML = '<p>Loading universities...</p>';
        return;
    }

    let html = `
        <div class="resources-header">
            <h2>Global Optometry Universities Directory</h2>
            <p>Browse ${getTotalUniversitiesCount()}+ optometry programs across ${getAllRegions().length} major world regions</p>
        </div>
    `;

    // Render regions
    const regions = getAllRegions();
    regions.forEach(regionName => {
        const regionInfo = getRegionInfo(regionName);
        const countries = regionInfo.countries;
        const universityCount = Object.values(countries).reduce((sum, unis) => sum + unis.length, 0);

        html += `
            <div class="region-card">
                <div class="region-header" onclick="toggleRegion('${regionName}')">
                    <div class="region-info">
                        <i class="fas ${regionInfo.icon}"></i>
                        <div>
                            <h3>${regionName}</h3>
                            <p>${universityCount} universities</p>
                        </div>
                    </div>
                    <i class="fas fa-chevron-down region-toggle" id="toggle-${regionName}"></i>
                </div>
                <div class="region-content" id="region-${regionName}" style="display: none;">
        `;

        // Render countries within region
        Object.entries(countries).forEach(([country, universities]) => {
            html += `
                <div class="country-section">
                    <h4>${country} (${universities.length})</h4>
                    <div class="universities-list">
            `;

            universities.forEach(uni => {
                html += `
                    <div class="university-item">
                        <div class="uni-name">${uni.name}</div>
                        <div class="uni-details">
                            <span class="uni-program">${uni.program}</span>
                            <span class="uni-duration">${uni.duration}</span>
                        </div>
                        <div class="uni-city"><i class="fas fa-map-pin"></i> ${uni.city}</div>
                    </div>
                `;
            });

            html += `
                    </div>
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

// Toggle region expansion
function toggleRegion(regionName) {
    const content = document.getElementById(`region-${regionName}`);
    const toggle = document.getElementById(`toggle-${regionName}`);

    if (content.style.display === 'none') {
        content.style.display = 'block';
        toggle.style.transform = 'rotate(180deg)';
    } else {
        content.style.display = 'none';
        toggle.style.transform = 'rotate(0deg)';
    }
}

// Setup filter listeners
function setupFilterListeners() {
    // Category filters
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('change', applyFilters);
    });

    // Country filter
    const countryFilter = document.getElementById('countryFilter');
    if (countryFilter) {
        countryFilter.addEventListener('change', applyFilters);
    }

    // Level filters
    const levelCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    levelCheckboxes.forEach(checkbox => {
        if (checkbox.value === 'undergraduate' || checkbox.value === 'graduate' || checkbox.value === 'clinical') {
            checkbox.addEventListener('change', applyFilters);
        }
    });
}

// Apply filters to courses
function applyFilters() {
    const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked')).map(c => c.value);
    const selectedCountry = document.getElementById('countryFilter')?.value || '';
    const selectedLevels = Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(c =>
        c.value === 'undergraduate' || c.value === 'graduate' || c.value === 'clinical'
    ).map(c => c.value);

    let filter = {};

    if (selectedCountry) filter.country = selectedCountry;

    // If multiple categories selected, filter by first one for simplicity
    if (selectedCategories.length > 0) {
        filter.category = selectedCategories[0];
    }

    if (selectedLevels.length > 0) {
        filter.level = selectedLevels[0];
    }

    renderCourses(filter);
}

// Perform search
function performSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    const searchTerm = searchInput.value.trim();

    if (!searchTerm) {
        alert('Please enter a search term');
        return;
    }

    // Navigate to courses page
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    const coursesPage = document.getElementById('courses');
    const coursesLink = document.querySelector('[data-page="courses"]');

    if (coursesPage) {
        coursesPage.classList.add('active');
    }
    if (coursesLink) {
        coursesLink.classList.add('active');
    }

    // Render filtered courses
    renderCourses({ search: searchTerm });

    closeNavMenu();
    window.scrollTo(0, 0);
}

// Navigate to course detail page
function navigateToCourse(courseId) {
    const course = coursesData.find(c => c.id === courseId);
    if (!course) return;

    // Track course view
    trackMaterialView(course.title, 'course');

    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    // Show course detail page
    const courseDetailPage = document.getElementById('courseDetail');
    if (courseDetailPage) {
        courseDetailPage.classList.add('active');
    }

    // Update title and description
    document.getElementById('courseTitle').textContent = course.title;
    document.getElementById('courseDescription').textContent = course.description;

    // Render course materials
    const content = document.getElementById('courseDetailContent');
    let html = `
        <div class="course-info">
            <div class="info-grid">
                <div class="info-item">
                    <i class="fas fa-book"></i>
                    <div>
                        <div class="info-label">Lectures</div>
                        <div class="info-value">${course.lectures}</div>
                    </div>
                </div>
                <div class="info-item">
                    <i class="fas fa-file"></i>
                    <div>
                        <div class="info-label">Materials</div>
                        <div class="info-value">${course.materials}</div>
                    </div>
                </div>
                <div class="info-item">
                    <i class="fas fa-layer-group"></i>
                    <div>
                        <div class="info-label">Level</div>
                        <div class="info-value">${getLevelName(course.level)}</div>
                    </div>
                </div>
                <div class="info-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <div>
                        <div class="info-label">Country</div>
                        <div class="info-value">${getCountryName(course.country)}</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Check if materials are available
    if (typeof availableMaterials !== 'undefined' && availableMaterials[course.title]) {
        html += renderMaterialsForDownload(course.title);
    } else {
        html += `
            <div class="materials-section">
                <h3>📥 Course Materials</h3>
                <p style="color: var(--text-secondary); text-align: center; padding: 40px 20px;">
                    Materials for this course will be available soon.
                </p>
            </div>
        `;
    }

    content.innerHTML = html;
    window.scrollTo(0, 0);
}

// Show courses page
function showCoursesPage() {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    const coursesPage = document.getElementById('courses');
    const coursesLink = document.querySelector('[data-page="courses"]');

    if (coursesPage) coursesPage.classList.add('active');
    if (coursesLink) coursesLink.classList.add('active');

    window.scrollTo(0, 0);
}

// Helper functions
function getLevelName(levelId) {
    const level = levels.find(l => l.id === levelId);
    return level ? level.name : levelId;
}

function getCountryName(countryCode) {
    const country = countries.find(c => c.code === countryCode);
    return country ? country.name : countryCode;
}

// Track page views with Google Analytics
function trackPageView(pageName) {
    if (window.gtag) {
        gtag('event', 'page_view', {
            page_title: pageName,
            page_path: `/${pageName}`
        });
    }
}

// Track search
function trackSearch(searchTerm) {
    if (window.gtag) {
        gtag('event', 'search', {
            search_term: searchTerm
        });
    }
}

// Render textbook categories
function renderTextbookCategories() {
    const container = document.getElementById('textbook-categories');
    if (!container || typeof textbooksIndex === 'undefined') return;

    const categories = getAllCategories();

    container.innerHTML = categories.map(cat => `
        <label class="textbook-category-filter">
            <input type="checkbox" value="${cat.id}" class="textbook-category-input">
            <span>${cat.category}</span>
            ${cat.bookCount ? `<small>(${cat.bookCount})</small>` : ''}
        </label>
    `).join('');

    // Setup listeners
    document.querySelectorAll('.textbook-category-input').forEach(input => {
        input.addEventListener('change', filterTextbooks);
    });
}

// Render all textbooks
function renderAllTextbooks(filter = null) {
    const container = document.getElementById('textbooks-grid');
    if (!container || typeof textbooksIndex === 'undefined') return;

    const categories = getAllCategories();
    let html = '';

    categories.forEach(category => {
        if (filter && !filter.includes(category.id)) return;

        html += `
            <div class="textbook-card">
                <div class="textbook-card-header">
                    <div class="textbook-card-title">${category.category}</div>
                </div>
                <div class="textbook-card-body">
                    <div class="textbook-card-category">📚 Reference Collection</div>
                    ${category.bookCount ? `
                        <div class="textbook-card-info">
                            <strong>${category.bookCount} Books Available</strong>
                            Size: ${category.size}
                        </div>
                    ` : ''}
                    <div class="textbook-card-info">
                        ${category.description || 'Comprehensive reference materials'}
                    </div>
                    ${category.highlights ? `
                        <div class="textbook-card-highlights">
                            <strong>Topics Covered:</strong>
                            <ul>
                                ${category.highlights.slice(0, 3).map(h => `<li>${h}</li>`).join('')}
                                ${category.highlights.length > 3 ? `<li>+ ${category.highlights.length - 3} more</li>` : ''}
                            </ul>
                        </div>
                    ` : ''}
                </div>
                <div class="textbook-card-footer">
                    <button class="btn-textbook-info" onclick="viewTextbookCategory('${category.id}')">
                        View All Books
                    </button>
                </div>
            </div>
        `;
    });

    container.innerHTML = html || '<p class="no-textbooks">No textbooks found matching your criteria.</p>';
}

// Filter textbooks
function filterTextbooks() {
    const selected = Array.from(document.querySelectorAll('.textbook-category-input:checked')).map(c => c.value);
    renderAllTextbooks(selected.length > 0 ? selected : null);
}

// View textbook category
function viewTextbookCategory(categoryId) {
    const category = getTextbooksByCategory(categoryId);
    if (category) {
        alert(`${category.category}\n\n${category.description || 'Comprehensive reference materials'}\n\nBooks: ${category.bookCount || 'Multiple'}`);
    }
}

// Search textbooks
function searchTextbooksFunction() {
    const input = document.getElementById('textbook-search-input');
    if (!input) return;

    const query = input.value.trim();
    if (!query) {
        renderAllTextbooks();
        return;
    }

    if (typeof searchTextbooks !== 'undefined') {
        const results = searchTextbooks(query);
        const container = document.getElementById('textbooks-grid');

        if (results.length === 0) {
            container.innerHTML = '<p class="no-textbooks">No textbooks found matching your search.</p>';
            return;
        }

        let html = '';
        const processedCategories = new Set();

        results.forEach(result => {
            if (result.type === 'category' && !processedCategories.has(result.id)) {
                processedCategories.add(result.id);
                html += `
                    <div class="textbook-card">
                        <div class="textbook-card-header">
                            <div class="textbook-card-title">${result.category}</div>
                        </div>
                        <div class="textbook-card-body">
                            <div class="textbook-card-category">Match: Category</div>
                            <div class="textbook-card-info">${result.description || ''}</div>
                        </div>
                    </div>
                `;
            }
        });

        container.innerHTML = html;
    }
}

// Setup textbook search
document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('textbook-search-btn');
    const searchInput = document.getElementById('textbook-search-input');

    if (searchBtn) {
        searchBtn.addEventListener('click', searchTextbooksFunction);
    }
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchTextbooksFunction();
            }
        });
    }
});
