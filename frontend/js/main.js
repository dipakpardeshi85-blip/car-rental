// Car Rental Website - Main JavaScript Utilities

const API_BASE = 'http://localhost:5000/api';

// API Helper Functions
async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers,
        },
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Request failed');
    }

    return data;
}

// Authentication State
function getCurrentUser() {
    const userStr = localStorage.getItem('currentUser');
    return userStr ? JSON.parse(userStr) : null;
}

function setCurrentUser(user) {
    if (user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
    } else {
        localStorage.removeItem('currentUser');
    }
}

function isLoggedIn() {
    return getCurrentUser() !== null;
}

function isAdmin() {
    const user = getCurrentUser();
    return user && user.is_admin;
}

async function checkAuthStatus() {
    try {
        const user = await apiRequest('/user');
        setCurrentUser(user);
        return user;
    } catch (error) {
        setCurrentUser(null);
        return null;
    }
}

// Navigation Helper
function updateNavigation() {
    const user = getCurrentUser();
    const authLinks = document.getElementById('authLinks');

    if (!authLinks) return;

    if (user) {
        authLinks.innerHTML = `
            <li><a href="/browse.html">Browse Cars</a></li>
            <li><a href="/dashboard.html">Dashboard</a></li>
            ${user.is_admin ? '<li><a href="/admin.html">Admin</a></li>' : ''}
            <li><a href="#" id="logoutBtn" class="btn btn-outline">Logout</a></li>
        `;

        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                await logout();
            });
        }
    } else {
        authLinks.innerHTML = `
            <li><a href="/browse.html">Browse Cars</a></li>
            <li><a href="/login.html">Login</a></li>
            <li><a href="/register.html" class="btn btn-primary">Sign Up</a></li>
        `;
    }
}

async function logout() {
    try {
        await apiRequest('/logout', { method: 'POST' });
        setCurrentUser(null);
        window.location.href = '/';
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

// Date Formatting
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    }).format(amount);
}

// Calculate days between dates
function calculateDays(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

// Show Alert Messages
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Form Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return re.test(phone);
}

// Loading Spinner
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.id = 'loadingSpinner';
    element.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.remove();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus().then(() => {
        updateNavigation();
    });
});

// Export functions for use in other scripts
window.CarRental = {
    apiRequest,
    getCurrentUser,
    setCurrentUser,
    isLoggedIn,
    isAdmin,
    checkAuthStatus,
    updateNavigation,
    logout,
    formatDate,
    formatCurrency,
    calculateDays,
    showAlert,
    validateEmail,
    validatePhone,
    showLoading,
    hideLoading,
};
