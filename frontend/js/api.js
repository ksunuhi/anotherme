/**
 * API Helper - Centralized API calls to backend
 */

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Make an authenticated API request
 */
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }

        // Handle 204 No Content responses
        if (response.status === 204) {
            return null;
        }

        // Handle empty responses
        const text = await response.text();
        return text ? JSON.parse(text) : null;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * API methods
 */
const api = {
    // Authentication
    auth: {
        checkEmail: (email) => apiRequest(`/auth/check-email?email=${encodeURIComponent(email)}`),
        register: (data) => apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify(data),
        }),
        login: (data) => apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify(data),
        }),
        logout: () => {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/pages/login.html';
        },
        verifyEmail: (token) => apiRequest('/auth/verify-email', {
            method: 'POST',
            body: JSON.stringify({ token }),
        }),
        resendVerification: (email) => apiRequest('/auth/resend-verification', {
            method: 'POST',
            body: JSON.stringify({ email }),
        }),
    },

    // Users
    users: {
        getMe: () => apiRequest('/users/me'),
        getStats: () => apiRequest('/users/me/stats'),
        getBirthdayTwins: () => apiRequest('/users/birthday-twins'),
        getUser: (userId) => apiRequest(`/users/${userId}`),
        searchByBirthday: (year, month, day) => apiRequest(`/users/search/by-birthday?year=${year}&month=${month}&day=${day}`),
        updateProfile: (data) => apiRequest('/users/me', {
            method: 'PUT',
            body: JSON.stringify(data),
        }),
        uploadProfilePicture: async (file) => {
            const token = localStorage.getItem('token');
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE_URL}/users/me/profile-picture`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Upload failed');
            }

            return await response.json();
        },
        deleteProfilePicture: () => apiRequest('/users/me/profile-picture', {
            method: 'DELETE',
        }),
    },

    // Posts
    posts: {
        getFeed: (filter = 'friends') => apiRequest(`/posts/feed?filter_type=${filter}`),
        getMyPosts: () => apiRequest('/posts/feed?filter_type=my'),
        create: (content, visibility = 'public') => apiRequest('/posts', {
            method: 'POST',
            body: JSON.stringify({ content, visibility }),
        }),
        update: (postId, content) => apiRequest(`/posts/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({ content }),
        }),
        delete: (postId) => apiRequest(`/posts/${postId}`, {
            method: 'DELETE',
        }),
        like: (postId) => apiRequest(`/posts/${postId}/like`, {
            method: 'POST',
        }),
        getComments: (postId) => apiRequest(`/posts/${postId}/comments`),
        createComment: (postId, content) => apiRequest(`/posts/${postId}/comments`, {
            method: 'POST',
            body: JSON.stringify({ content }),
        }),
        deleteComment: (postId, commentId) => apiRequest(`/posts/${postId}/comments/${commentId}`, {
            method: 'DELETE',
        }),
    },

    // Messages
    messages: {
        getConversations: () => apiRequest('/messages/conversations'),
        getConversation: (userId) => apiRequest(`/messages/conversation/${userId}`),
        send: (recipientId, content) => apiRequest('/messages', {
            method: 'POST',
            body: JSON.stringify({ recipient_id: recipientId, content }),
        }),
        getUnreadCount: () => apiRequest('/messages/unread-count'),
        markAsRead: (messageId) => apiRequest(`/messages/${messageId}/read`, {
            method: 'PUT',
        }),
    },

    // Friends
    friends: {
        getAll: () => apiRequest('/friends'),
        getMutual: (userId) => apiRequest(`/friends/mutual/${userId}`),
        add: (userId) => apiRequest(`/friends/${userId}`, {
            method: 'POST',
        }),
        remove: (userId) => apiRequest(`/friends/${userId}`, {
            method: 'DELETE',
        }),
        check: (userId) => apiRequest(`/friends/check/${userId}`),
    },

    // Public APIs (No authentication required)
    public: {
        // Get recent signups
        getRecentUsers: (limit = 3) => apiRequest(`/users/recent?limit=${limit}`),

        // Search by birthday (public, limited results)
        searchByBirthday: (dateStr) => apiRequest(`/users/public/search-by-birthday?date_str=${dateStr}`),

        // Get count of users with specific birthday
        getBirthdayCount: (dateStr) => apiRequest(`/users/public/search-by-birthday/count?date_str=${dateStr}`),

        // Get public profile
        getPublicProfile: (userId) => apiRequest(`/users/public/${userId}`),

        // Get platform statistics
        getStatistics: () => apiRequest('/statistics/birthday-stats'),
    },
};
