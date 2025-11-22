/**
 * Authentication utilities
 */

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
}

/**
 * Redirect to login if not authenticated
 */
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/pages/login.html';
        return false;
    }
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
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/pages/login.html';
}

/**
 * Get authorization header
 */
function getAuthHeader() {
    const token = localStorage.getItem('token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}
