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

        return await response.json();
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
    },

    // Users
    users: {
        getMe: () => apiRequest('/users/me'),
        updateProfile: (data) => apiRequest('/users/me', {
            method: 'PUT',
            body: JSON.stringify(data),
        }),
        getUser: (userId) => apiRequest(`/users/${userId}`),
        search: (params) => apiRequest(`/users/search?${new URLSearchParams(params)}`),
        getBirthdayMatches: () => apiRequest('/users/birthday-matches'),
    },

    // Posts
    posts: {
        getFeed: (filter = 'all') => apiRequest(`/posts/feed?filter=${filter}`),
        create: (data) => apiRequest('/posts', {
            method: 'POST',
            body: JSON.stringify(data),
        }),
        like: (postId) => apiRequest(`/posts/${postId}/like`, {
            method: 'POST',
        }),
        getComments: (postId) => apiRequest(`/posts/${postId}/comments`),
        addComment: (postId, content) => apiRequest(`/posts/${postId}/comments`, {
            method: 'POST',
            body: JSON.stringify({ content }),
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
    },

    // Friends
    friends: {
        getAll: () => apiRequest('/friends'),
        getMutual: () => apiRequest('/friends/mutual'),
        add: (userId) => apiRequest(`/friends/${userId}`, {
            method: 'POST',
        }),
        remove: (userId) => apiRequest(`/friends/${userId}`, {
            method: 'DELETE',
        }),
        check: (userId) => apiRequest(`/friends/check/${userId}`),
    },

    // Groups
    groups: {
        getAll: () => apiRequest('/groups'),
        getGroup: (groupId) => apiRequest(`/groups/${groupId}`),
        getMembers: (groupId) => apiRequest(`/groups/${groupId}/members`),
        getPosts: (groupId) => apiRequest(`/groups/${groupId}/posts`),
        join: (groupId) => apiRequest(`/groups/${groupId}/join`, {
            method: 'POST',
        }),
        leave: (groupId) => apiRequest(`/groups/${groupId}/leave`, {
            method: 'POST',
        }),
    },
};
