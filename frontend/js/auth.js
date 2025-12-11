/**
 * Authentication utilities
 */

// Inactivity timeout configuration
const INACTIVITY_TIMEOUT = 30 * 60 * 1000; // 30 minutes in milliseconds
let inactivityTimer = null;
let lastActivityTime = Date.now();

/**
 * Check if user is logged in
 */
function isAuthenticated() {
    return !!localStorage.getItem('token');
}

/**
 * Get current user from localStorage
 */
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

/**
 * Save authentication token and user data
 */
function saveAuth(token, user) {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));

    // Initialize inactivity tracking after login
    initInactivityTracking();
}

/**
 * Redirect to login if not authenticated
 */
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/pages/login.html';
        return false;
    }

    // Initialize inactivity tracking for authenticated users
    initInactivityTracking();
    return true;
}

/**
 * Redirect to dashboard if already authenticated
 */
function redirectIfAuthenticated() {
    if (isAuthenticated()) {
        window.location.href = '/pages/dashboard.html';
    }
}

/**
 * Logout user
 */
function logout() {
    // Clear inactivity timer
    if (inactivityTimer) {
        clearTimeout(inactivityTimer);
        inactivityTimer = null;
    }

    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/pages/login.html';
}

/**
 * Logout user due to inactivity
 */
function logoutDueToInactivity() {
    alert('You have been logged out due to inactivity. Please login again.');
    logout();
}

/**
 * Reset the inactivity timer
 */
function resetInactivityTimer() {
    lastActivityTime = Date.now();

    // Clear existing timer
    if (inactivityTimer) {
        clearTimeout(inactivityTimer);
    }

    // Set new timer
    inactivityTimer = setTimeout(logoutDueToInactivity, INACTIVITY_TIMEOUT);
}

/**
 * Initialize inactivity tracking
 * Tracks mouse movement, keyboard input, clicks, and touch events
 */
function initInactivityTracking() {
    // Only initialize if user is authenticated
    if (!isAuthenticated()) {
        return;
    }

    // Clear any existing timer
    if (inactivityTimer) {
        clearTimeout(inactivityTimer);
    }

    // Start the inactivity timer
    resetInactivityTimer();

    // Track user activity events
    const activityEvents = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];

    // Remove existing listeners to prevent duplicates
    activityEvents.forEach(event => {
        document.removeEventListener(event, resetInactivityTimer);
    });

    // Add activity listeners
    activityEvents.forEach(event => {
        document.addEventListener(event, resetInactivityTimer, { passive: true });
    });
}

/**
 * Get authorization header
 */
function getAuthHeader() {
    const token = localStorage.getItem('token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}
