// Anonymous Behavior Tracking System

// Generate or get anonymous session ID
function getSessionId() {
    let sessionId = sessionStorage.getItem('olh_session_id');
    if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        sessionStorage.setItem('olh_session_id', sessionId);
    }
    return sessionId;
}

// Track user behavior (page views, downloads, etc.)
function trackUserBehavior(action, details = {}) {
    const event = {
        timestamp: new Date().toISOString(),
        sessionId: getSessionId(),
        action: action,
        page: window.location.pathname,
        ...details
    };

    // Send to Google Analytics if available
    if (window.gtag) {
        gtag('event', action, {
            session_id: event.sessionId,
            ...details
        });
    }

    // Also send to server if backend is available
    if (navigator.sendBeacon) {
        try {
            navigator.sendBeacon('/api/track', JSON.stringify(event));
        } catch (e) {
            // Fail silently
        }
    }

    return event;
}

// Track page view
function trackPageView(pageName) {
    trackUserBehavior('page_view', {
        page_name: pageName
    });
}

// Track download
function trackDownload(fileName, courseId) {
    trackUserBehavior('download', {
        file_name: fileName,
        course_id: courseId
    });
}

// Track material view
function trackMaterialView(materialName, type) {
    trackUserBehavior('material_view', {
        material_name: materialName,
        material_type: type
    });
}

// Initialize tracking on page load
document.addEventListener('DOMContentLoaded', () => {
    // Get current page
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        if (page.classList.contains('active')) {
            trackPageView(page.id);
        }
    });
});
