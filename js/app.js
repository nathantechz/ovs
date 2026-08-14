// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    renderHomePage();
});

// Initialize app
function initializeApp() {
    setupPageNavigation();
    renderFeaturedCourses();
    renderCategories();
    renderResources();
}

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
function renderCategories() {
    const container = document.getElementById('categoryFilters');
    if (!container) return;

    container.innerHTML = categories.map(cat => `
        <label>
            <input type="checkbox" value="${cat.id}" class="category-filter">
            <i class="fas ${cat.icon}"></i> ${cat.name}
        </label>
    `).join('');
}

// Render resources
function renderResources() {
    const container = document.getElementById('resourcesGrid');
    if (!container) return;

    container.innerHTML = resourcesData.map(resource => `
        <div class="resource-card">
            <div class="resource-card-header">
                <div>
                    <i class="fas ${resource.icon}"></i>
                </div>
                <div>
                    <div class="resource-card-title">${resource.title}</div>
                </div>
            </div>
            <div class="resource-card-body">
                <div class="resource-university">${resource.university}</div>
                <div class="resource-country">
                    <i class="fas fa-map-marker-alt"></i>
                    ${resource.country} • ${resource.region}
                </div>
                <p class="resource-desc">${resource.description}</p>
                <a href="${resource.link}" class="resource-link">View Syllabus →</a>
            </div>
        </div>
    `).join('');
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
    const levelFilters = document.querySelectorAll('input[type="checkbox"][value="undergraduate"], input[type="checkbox"][value="graduate"], input[type="checkbox"][value="clinical"]');
    levelFilters.forEach(filter => {
        filter.addEventListener('change', applyFilters);
    });
}

// Apply filters to courses
function applyFilters() {
    const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked')).map(c => c.value);
    const selectedCountry = document.getElementById('countryFilter')?.value || '';
    const selectedLevels = Array.from(document.querySelectorAll('input[type="checkbox"][value="undergraduate"]:checked, input[type="checkbox"][value="graduate"]:checked, input[type="checkbox"][value="clinical"]:checked')).map(c => c.value);

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

// Navigate to course detail (placeholder for future implementation)
function navigateToCourse(courseId) {
    const course = coursesData.find(c => c.id === courseId);
    if (course) {
        alert(`Course: ${course.title}\n\nFull course content will be available here.\n\nLectures: ${course.lectures}\nMaterials: ${course.materials}`);
        // In future: navigate to detailed course page
    }
}

// Render home page
function renderHomePage() {
    // This is called on initial load
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

// Re-setup filters when courses page is visited
const observer = new MutationObserver(() => {
    const coursesPage = document.getElementById('courses');
    if (coursesPage && coursesPage.classList.contains('active')) {
        setupFilterListeners();
    }
});

observer.observe(document.body, { subtree: true, attributes: true, attributeFilter: ['class'] });
