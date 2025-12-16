/**
 * Utility functions
 */

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;

    // Less than 1 minute
    if (diff < 60000) {
        return 'Just now';
    }

    // Less than 1 hour
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes}m ago`;
    }

    // Less than 24 hours
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours}h ago`;
    }

    // Less than 7 days
    if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days}d ago`;
    }

    // Format as date
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
}

/**
 * Format birthday (MM/DD/YYYY)
 */
function formatBirthday(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Get initials from name
 */
function getInitials(name) {
    if (!name) return '??';
    const parts = name.trim().split(' ');
    if (parts.length === 1) {
        return parts[0].substring(0, 2).toUpperCase();
    }
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

/**
 * Generate avatar color from user ID
 */
function getAvatarColor(userId) {
    const colors = [
        '#6366F1', // primary
        '#A855F7', // purple
        '#14B8A6', // teal
        '#F59E0B', // amber
        '#EF4444', // red
        '#10B981', // green
        '#3B82F6', // blue
    ];
    const hash = userId.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[hash % colors.length];
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white z-50 ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        'bg-blue-500'
    }`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Validate email
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate password strength
 */
function validatePassword(password) {
    const errors = [];

    if (password.length < 8) {
        errors.push('Password must be at least 8 characters');
    }
    if (!/[A-Z]/.test(password)) {
        errors.push('Password must contain at least one uppercase letter');
    }
    if (!/[a-z]/.test(password)) {
        errors.push('Password must contain at least one lowercase letter');
    }
    if (!/[0-9]/.test(password)) {
        errors.push('Password must contain at least one number');
    }

    return {
        isValid: errors.length === 0,
        errors
    };
}

/**
 * Render avatar HTML with profile picture or initials
 * @param {Object} user - User object with profile_picture_url, full_name, and id
 * @param {string} size - Size class (e.g., 'w-8 h-8', 'w-10 h-10', 'w-12 h-12')
 * @param {string} extraClasses - Additional CSS classes
 * @returns {string} HTML string for avatar
 */
function renderAvatar(user, size = 'w-10 h-10', extraClasses = '') {
    if (!user) {
        return `<div class="${size} rounded-full bg-gray-400 flex items-center justify-center text-white font-semibold ${extraClasses}">??</div>`;
    }

    if (user.profile_picture_url) {
        return `<img src="http://localhost:8000/uploads/${user.profile_picture_url}"
                     alt="${user.full_name || 'User'}"
                     class="${size} rounded-full object-cover ${extraClasses}" />`;
    }

    return `<div class="${size} rounded-full flex items-center justify-center text-white font-semibold ${extraClasses}"
                 style="background-color: ${getAvatarColor(user.id)}">
                ${getInitials(user.full_name)}
            </div>`;
}
