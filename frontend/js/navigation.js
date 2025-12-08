/**
 * Shared Navigation Component
 * Renders header and footer for all pages
 */

/**
 * Render the header navigation
 */
function renderHeader() {
    const isLoggedIn = isAuthenticated();
    const currentUser = getCurrentUser();

    const header = `
    <header class="bg-white shadow-sm fixed w-full top-0 z-50">
        <nav class="container mx-auto px-6 py-4">
            <div class="flex items-center justify-between">
                <!-- Logo -->
                <div class="flex items-center space-x-3">
                    <a href="${isLoggedIn ? 'dashboard.html' : 'index.html'}" class="flex items-center space-x-3">
                        <div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                            <span class="text-white font-bold text-xl">AM</span>
                        </div>
                        <span class="text-2xl font-bold text-gray-900">AnotherMe</span>
                    </a>
                </div>

                <!-- Desktop Navigation -->
                <div class="hidden md:flex items-center space-x-8">
                    ${isLoggedIn ? `
                        <a href="dashboard.html" class="text-gray-700 hover:text-primary transition">Dashboard</a>
                        <a href="friends.html" class="text-gray-700 hover:text-primary transition">Friends</a>
                    ` : `
                        <a href="index.html#home" class="text-gray-700 hover:text-primary transition">Home</a>
                        <a href="index.html#about" class="text-gray-700 hover:text-primary transition">About</a>
                        <a href="index.html#features" class="text-gray-700 hover:text-primary transition">Features</a>
                        <a href="index.html#how-it-works" class="text-gray-700 hover:text-primary transition">How It Works</a>
                    `}
                </div>

                <!-- Auth Buttons / User Menu -->
                <div class="hidden md:flex items-center space-x-4">
                    ${isLoggedIn ? `
                        <!-- User Menu -->
                        <div class="relative" id="userMenuContainer">
                            <button onclick="toggleUserMenu()" class="flex items-center space-x-2 text-gray-700 hover:text-primary transition">
                                <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white font-semibold">
                                    ${currentUser ? getInitials(currentUser.full_name) : 'U'}
                                </div>
                                <span class="font-medium">${currentUser ? currentUser.full_name.split(' ')[0] : 'User'}</span>
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                </svg>
                            </button>

                            <!-- Dropdown Menu -->
                            <div id="userMenu" class="hidden absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 border border-gray-200">
                                <a href="profile.html" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">My Profile</a>
                                <hr class="my-2">
                                <a href="#" onclick="handleLogout(); return false;" class="block px-4 py-2 text-red-600 hover:bg-gray-100">Sign Out</a>
                            </div>
                        </div>
                    ` : `
                        <a href="login.html" class="text-primary hover:text-primary-dark transition font-medium">
                            Log In
                        </a>
                        <a href="register.html" class="bg-primary hover:bg-primary-dark text-white px-6 py-2 rounded-lg transition font-medium">
                            Sign Up
                        </a>
                    `}
                </div>

                <!-- Mobile Menu Button -->
                <button onclick="toggleMobileMenu()" class="md:hidden text-gray-700">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </div>

            <!-- Mobile Menu -->
            <div id="mobileMenu" class="hidden md:hidden mt-4 pb-4">
                ${isLoggedIn ? `
                    <a href="dashboard.html" class="block py-2 text-gray-700 hover:text-primary transition">Dashboard</a>
                    <a href="friends.html" class="block py-2 text-gray-700 hover:text-primary transition">Friends</a>
                    <hr class="my-2">
                    <a href="profile.html" class="block py-2 text-gray-700 hover:text-primary transition">My Profile</a>
                    <a href="#" onclick="handleLogout(); return false;" class="block py-2 text-red-600 hover:text-primary transition">Sign Out</a>
                ` : `
                    <a href="index.html#home" class="block py-2 text-gray-700 hover:text-primary transition">Home</a>
                    <a href="index.html#about" class="block py-2 text-gray-700 hover:text-primary transition">About</a>
                    <a href="index.html#features" class="block py-2 text-gray-700 hover:text-primary transition">Features</a>
                    <a href="index.html#how-it-works" class="block py-2 text-gray-700 hover:text-primary transition">How It Works</a>
                    <hr class="my-2">
                    <a href="login.html" class="block py-2 text-primary hover:text-primary-dark transition font-medium">Log In</a>
                    <a href="register.html" class="block py-2 bg-primary hover:bg-primary-dark text-white px-6 rounded-lg transition font-medium text-center">Sign Up</a>
                `}
            </div>
        </nav>
    </header>
    `;

    document.getElementById('app-header').innerHTML = header;
}

/**
 * Render the footer
 */
function renderFooter() {
    const footer = `
    <footer class="bg-gray-900 text-gray-400 py-12 px-6">
        <div class="container mx-auto max-w-6xl">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                <!-- Brand -->
                <div>
                    <div class="flex items-center space-x-2 mb-4">
                        <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                            <span class="text-white font-bold">AM</span>
                        </div>
                        <span class="text-xl font-bold text-white">AnotherMe</span>
                    </div>
                    <p class="text-sm">
                        Connect with your birthday twins and celebrate the unique bond of shared birthdays.
                    </p>
                </div>

                <!-- Product -->
                <div>
                    <h4 class="font-semibold text-white mb-4">Product</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="index.html#features" class="hover:text-white transition">Features</a></li>
                        <li><a href="index.html#how-it-works" class="hover:text-white transition">How It Works</a></li>
                    </ul>
                </div>

                <!-- Company -->
                <div>
                    <h4 class="font-semibold text-white mb-4">Company</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="index.html#about" class="hover:text-white transition">About Us</a></li>
                        <li><a href="contact.html" class="hover:text-white transition">Contact</a></li>
                    </ul>
                </div>

                <!-- Legal -->
                <div>
                    <h4 class="font-semibold text-white mb-4">Legal</h4>
                    <ul class="space-y-2 text-sm">
                        <li><a href="privacy-policy.html" class="hover:text-white transition">Privacy Policy</a></li>
                        <li><a href="terms-of-service.html" class="hover:text-white transition">Terms of Service</a></li>
                    </ul>
                </div>
            </div>

            <!-- Bottom Bar -->
            <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
                <p class="text-sm text-gray-400 mb-4 md:mb-0">
                    © 2025 AnotherMe. All rights reserved.
                </p>
                <div class="flex space-x-6">
                    <a href="#" class="text-gray-400 hover:text-white transition">
                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                        </svg>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white transition">
                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                        </svg>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white transition">
                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.295-.6.295-.002 0-.003 0-.005 0l.213-3.054 5.56-5.022c.24-.213-.054-.334-.373-.121L7.773 13.96l-2.885-.9c-.626-.196-.638-.626.13-.93l11.25-4.332c.52-.198.976.127.804.923z"/>
                        </svg>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white transition">
                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    </footer>
    `;

    document.getElementById('app-footer').innerHTML = footer;
}

/**
 * Toggle user menu dropdown
 */
function toggleUserMenu() {
    const menu = document.getElementById('userMenu');
    menu.classList.toggle('hidden');
}

/**
 * Toggle mobile menu
 */
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('hidden');
}

/**
 * Handle logout
 */
function handleLogout() {
    if (confirm('Are you sure you want to sign out?')) {
        logout();
    }
}

/**
 * Close dropdowns when clicking outside
 */
document.addEventListener('click', function(event) {
    const userMenuContainer = document.getElementById('userMenuContainer');
    const userMenu = document.getElementById('userMenu');

    if (userMenuContainer && userMenu && !userMenuContainer.contains(event.target)) {
        userMenu.classList.add('hidden');
    }
});

/**
 * Initialize navigation on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    renderHeader();
    renderFooter();
});
