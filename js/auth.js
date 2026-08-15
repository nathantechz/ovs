// Email Registration & Authentication System

// Check if user is registered
function isUserRegistered() {
    return localStorage.getItem('olh_user_email') !== null;
}

// Get registered email
function getUserEmail() {
    return localStorage.getItem('olh_user_email');
}

// Register user with email
function registerUser(email) {
    if (!validateEmail(email)) {
        alert('Please enter a valid email address');
        return false;
    }
    localStorage.setItem('olh_user_email', email);
    localStorage.setItem('olh_registration_date', new Date().toISOString());
    return true;
}

// Validate email format
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Logout user
function logoutUser() {
    localStorage.removeItem('olh_user_email');
    localStorage.removeItem('olh_registration_date');
    location.reload();
}

// Show registration modal
function showRegistrationModal() {
    if (isUserRegistered()) {
        return;
    }

    const modal = document.getElementById('registrationModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

// Hide registration modal
function hideRegistrationModal() {
    const modal = document.getElementById('registrationModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Handle registration form submission
function handleRegistrationSubmit(e) {
    e.preventDefault();
    const emailInput = document.getElementById('registrationEmail');
    const email = emailInput.value.trim();

    if (registerUser(email)) {
        hideRegistrationModal();
        location.reload();
    }
}

// Setup auth UI
function setupAuthUI() {
    if (isUserRegistered()) {
        const userEmail = getUserEmail();
        const authSection = document.getElementById('authSection');
        if (authSection) {
            authSection.innerHTML = `
                <div class="auth-info">
                    <span>👤 ${userEmail}</span>
                    <button onclick="logoutUser()" class="btn-logout">Logout</button>
                </div>
            `;
        }
    } else {
        showRegistrationModal();
    }

    // Setup registration form
    const regForm = document.getElementById('registrationForm');
    if (regForm) {
        regForm.addEventListener('submit', handleRegistrationSubmit);
    }

    // Close modal when clicking outside
    const modal = document.getElementById('registrationModal');
    if (modal) {
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                // Prevent closing by clicking outside if not registered
                if (!isUserRegistered()) {
                    return;
                }
                hideRegistrationModal();
            }
        });
    }
}

// Show forgot password modal
function showForgotPasswordModal() {
    const modal = document.getElementById('forgotPasswordModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

// Hide forgot password modal
function hideForgotPasswordModal() {
    const modal = document.getElementById('forgotPasswordModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Handle forgot password
function handleForgotPassword(e) {
    e.preventDefault();
    const emailInput = document.getElementById('forgotPasswordEmail');
    const email = emailInput.value.trim();

    if (validateEmail(email)) {
        const userEmail = getUserEmail();
        if (userEmail === email) {
            logoutUser();
        } else {
            alert('Email not found in our records.');
        }
    }
}

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', () => {
    setupAuthUI();

    // Setup forgot password form
    const forgotForm = document.getElementById('forgotPasswordForm');
    if (forgotForm) {
        forgotForm.addEventListener('submit', handleForgotPassword);
    }
});
