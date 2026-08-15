// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    setupPageNavigation();
    setupEventListeners();
    setupContactForm();
    renderFeaturedCourses();
    renderCategoriesFilter();
    renderResources();
    renderCourses();
    renderMaterials();
    renderTextbookCategories();
    renderAllTextbooks();
    setupSearchSuggestions();
    setupCardLinks();
});

// Make the static home/contact cards act as real links. Only .course-card had a
// handler, so everything else on the page looked clickable but did nothing.
function setupCardLinks() {
    // Feature cards -> the section of the site each one describes
    const featureTargets = ['courses', 'resources', 'materials', 'courses'];
    document.querySelectorAll('.features .feature-card').forEach((card, i) => {
        makeCardNavigate(card, featureTargets[i] || 'courses');
    });

    // Stat cards -> the page the number refers to
    const statTargets = ['materials', 'resources', 'resources', 'courses'];
    document.querySelectorAll('.stats .stat-card').forEach((card, i) => {
        makeCardNavigate(card, statTargets[i] || 'courses');
    });
}

function makeCardNavigate(card, pageName) {
    card.classList.add('is-clickable');
    card.setAttribute('role', 'link');
    card.setAttribute('tabindex', '0');

    const go = () => showPage(pageName);
    card.addEventListener('click', go);
    card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            go();
        }
    });
}

// Single place that switches pages, so nav links, cards and search all agree.
function showPage(pageName) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    const page = document.getElementById(pageName);
    if (page) page.classList.add('active');

    const link = document.querySelector(`.nav-link[data-page="${pageName}"]`);
    if (link) link.classList.add('active');

    closeNavMenu();
    window.scrollTo(0, 0);
    trackPageView(pageName);
}

// Setup navigation between pages. Covers any [data-page] element, not just the
// navbar, so in-page links like the one on the About page work too.
function setupPageNavigation() {
    document.querySelectorAll('[data-page]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            showPage(link.getAttribute('data-page'));
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

// Setup contact form
function setupContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', handleContactFormSubmit);
}

// Handle contact form submission
function handleContactFormSubmit(e) {
    e.preventDefault();

    const form = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');
    const submitBtn = form.querySelector('.btn-submit');

    // Get form data
    const formData = new FormData(form);

    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    // Send via Formspree (free service for static sites)
    fetch('https://formspree.io/f/mnakdvwl', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Success
            formMessage.className = 'form-message success';
            formMessage.textContent = '✓ Thank you! Your message has been sent successfully. We\'ll get back to you soon.';
            formMessage.style.display = 'block';
            form.reset();
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';

            // Track submission
            trackUserBehavior('contact_form_submit', {
                subject: formData.get('subject'),
                category: formData.get('category')
            });
        } else {
            throw new Error('Form submission failed');
        }
    })
    .catch(error => {
        formMessage.className = 'form-message error';
        formMessage.textContent = '✗ Something went wrong. Please try again in a moment.';
        formMessage.style.display = 'block';
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    });
}

function closeNavMenu() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.remove('active');
}

// Levenshtein similarity ratio between two words, 0..1
function levenshteinRatio(a, b) {
    if (!a.length || !b.length) return 0;

    const m = a.length;
    const n = b.length;
    const dp = Array(n + 1).fill(null).map(() => Array(m + 1).fill(0));

    for (let i = 0; i <= m; i++) dp[0][i] = i;
    for (let i = 0; i <= n; i++) dp[i][0] = i;

    for (let i = 1; i <= n; i++) {
        for (let j = 1; j <= m; j++) {
            const cost = a[j - 1] === b[i - 1] ? 0 : 1;
            dp[i][j] = Math.min(
                dp[i - 1][j] + 1,      // deletion
                dp[i][j - 1] + 1,      // insertion
                dp[i - 1][j - 1] + cost // substitution
            );
        }
    }

    const maxLen = Math.max(m, n);
    return Math.max(0, (maxLen - dp[n][m]) / maxLen);
}

// How well a single field matches the query, 0..1.
// Exact and prefix matches win outright; otherwise every query word is matched
// against its best word in the field so typos and partial phrases still land.
function fieldScore(text, query) {
    if (!text) return 0;

    const t = text.toLowerCase().trim();
    const q = query.toLowerCase().trim();

    if (t === q) return 1;
    if (t.startsWith(q)) return 0.95;
    if (t.includes(q)) return 0.9;

    const queryWords = q.split(/\s+/).filter(Boolean);
    const textWords = t.split(/[^a-z0-9]+/).filter(Boolean);
    if (!queryWords.length || !textWords.length) return 0;

    let total = 0;
    for (const qw of queryWords) {
        let best = 0;
        for (const tw of textWords) {
            const s = tw === qw ? 1
                : tw.startsWith(qw) ? 0.9
                : tw.includes(qw) ? 0.8
                : levenshteinRatio(tw, qw);
            if (s > best) best = s;
        }
        total += best;
    }

    // Word-level matches cap below a true substring hit so those still rank first.
    return (total / queryWords.length) * 0.85;
}

// Relative importance of each field. A hit in any one field is enough, so the
// per-field scores are combined with max() rather than summed — summing them
// meant even a perfect title match could not clear the threshold.
const SEARCH_WEIGHTS = { title: 1, category: 0.8, description: 0.7, degree: 0.6 };
const SEARCH_THRESHOLD = 0.55;

// Search courses with fuzzy matching
function searchCourses(searchTerm) {
    if (!searchTerm || searchTerm.trim().length === 0) {
        return coursesData;
    }

    const term = searchTerm.toLowerCase().trim();

    return coursesData
        .map(course => {
            const score = Math.max(
                fieldScore(course.title, term) * SEARCH_WEIGHTS.title,
                fieldScore(course.category, term) * SEARCH_WEIGHTS.category,
                fieldScore(course.description, term) * SEARCH_WEIGHTS.description,
                course.degree ? fieldScore(course.degree, term) * SEARCH_WEIGHTS.degree : 0
            );

            return { course, score };
        })
        .filter(item => item.score >= SEARCH_THRESHOLD)
        .sort((a, b) => b.score - a.score) // Sort by relevance
        .map(item => item.course);
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
        // Use fuzzy search for better matching
        filtered = searchCourses(filter.search);
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
    if (!searchTerm) return;

    hideSearchSuggestions();
    trackSearch(searchTerm);

    showPage('courses');
    renderCourses({ search: searchTerm });
}

// Live suggestion dropdown under the home search box.
function setupSearchSuggestions() {
    const input = document.getElementById('searchInput');
    const list = document.getElementById('searchSuggestions');
    if (!input || !list) return;

    let activeIndex = -1;

    const render = () => {
        const term = input.value.trim();
        if (term.length < 2) return hideSearchSuggestions();

        const matches = searchCourses(term).slice(0, 6);
        if (!matches.length) {
            list.innerHTML = `<div class="suggestion-empty">No matches for “${escapeHtml(term)}”</div>`;
            list.classList.add('is-open');
            input.setAttribute('aria-expanded', 'true');
            activeIndex = -1;
            return;
        }

        activeIndex = -1;
        list.innerHTML = matches.map((course, i) => {
            const hasMaterials = typeof resolveMaterialsKey === 'function'
                && resolveMaterialsKey(course.title);
            return `
                <div class="suggestion" role="option" data-index="${i}" data-course-id="${course.id}">
                    <i class="fas ${course.icon}"></i>
                    <div class="suggestion-text">
                        <div class="suggestion-title">${escapeHtml(course.title)}</div>
                        <div class="suggestion-meta">
                            ${escapeHtml(getLevelName(course.level))}
                            &middot; ${course.lectures} lectures
                            ${hasMaterials ? '<span class="suggestion-tag">Materials ready</span>' : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        list.classList.add('is-open');
        input.setAttribute('aria-expanded', 'true');
    };

    const setActive = (next) => {
        const items = list.querySelectorAll('.suggestion');
        if (!items.length) return;

        activeIndex = (next + items.length) % items.length;
        items.forEach((el, i) => el.classList.toggle('is-active', i === activeIndex));
        items[activeIndex].scrollIntoView({ block: 'nearest' });
    };

    input.addEventListener('input', render);
    input.addEventListener('focus', render);

    input.addEventListener('keydown', (e) => {
        const items = list.querySelectorAll('.suggestion');

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setActive(activeIndex + 1);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setActive(activeIndex - 1);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (activeIndex >= 0 && items[activeIndex]) {
                navigateToCourse(Number(items[activeIndex].dataset.courseId));
                hideSearchSuggestions();
            } else {
                performSearch();
            }
        } else if (e.key === 'Escape') {
            hideSearchSuggestions();
        }
    });

    list.addEventListener('mousedown', (e) => {
        const item = e.target.closest('.suggestion');
        if (!item) return;
        e.preventDefault();
        navigateToCourse(Number(item.dataset.courseId));
        hideSearchSuggestions();
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-bar')) hideSearchSuggestions();
    });
}

function hideSearchSuggestions() {
    const list = document.getElementById('searchSuggestions');
    const input = document.getElementById('searchInput');
    if (list) {
        list.classList.remove('is-open');
        list.innerHTML = '';
    }
    if (input) input.setAttribute('aria-expanded', 'false');
}

function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, c => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
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
    const materialsKey = typeof resolveMaterialsKey === 'function'
        ? resolveMaterialsKey(course.title)
        : null;

    if (materialsKey) {
        html += renderMaterialsForDownload(materialsKey);
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
