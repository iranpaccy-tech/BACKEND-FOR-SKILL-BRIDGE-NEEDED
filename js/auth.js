/**
 * FRONTEND AUTHENTICATION
 * Uses Flask API instead of localStorage
 */

const Auth = {
    currentUser: null,

    init() {
        this.checkAuthStatus();
        this.setupEventListeners();
    },

    setupEventListeners() {
        document.getElementById('loginForm')?.addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('registerForm')?.addEventListener('submit', (e) => this.handleRegister(e));
    },

    showLogin() {
        window.location.href = '/login';
    },

    showRegister() {
        window.location.href = '/register';
    },

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        if (!email || !password) {
            UI.showToast('Please fill in all fields', 'error');
            return;
        }

        UI.showToast('Logging in...', 'info');

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();

            if (response.ok && data.success) {
                this.currentUser = data.user;
                saveAuthUser(data.user);
                UI.showToast(`Welcome back, ${data.user.firstName}!`, 'success');
                setTimeout(() => {
                    if (data.user.role === 'admin') {
                        window.location.href = '/admin';
                    } else if (data.user.role === 'teacher') {
                        window.location.href = '/teacher';
                    } else {
                        window.location.href = '/dashboard';
                    }
                }, 1000);
            } else {
                UI.showToast(data.message || 'Login failed', 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            UI.showToast('Connection error. Please try again.', 'error');
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const firstName = document.getElementById('registerFirstName')?.value || document.getElementById('registerName')?.value.split(' ')[0];
        const lastName = document.getElementById('registerLastName')?.value || document.getElementById('registerName')?.value.split(' ')[1] || '';
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('registerConfirmPassword').value;

        if (!firstName || !email || !password) {
            UI.showToast('Please fill in all required fields', 'error');
            return;
        }

        if (password !== confirmPassword) {
            UI.showToast('Passwords do not match', 'error');
            return;
        }

        if (password.length < 6) {
            UI.showToast('Password must be at least 6 characters', 'error');
            return;
        }

        UI.showToast('Creating account...', 'info');

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    firstName,
                    lastName,
                    email,
                    password,
                    confirmPassword
                })
            });
            const data = await response.json();

            if (response.ok && data.success) {
                this.currentUser = data.user;
                saveAuthUser(data.user);
                UI.showToast(`Welcome, ${data.user.firstName}!`, 'success');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                UI.showToast(data.message || 'Registration failed', 'error');
            }
        } catch (error) {
            console.error('Registration error:', error);
            UI.showToast('Connection error. Please try again.', 'error');
        }
    },

    async logout() {
        try {
            await fetch('/api/auth/logout', { method: 'POST' });
        } catch (error) {
            console.error('Logout error:', error);
        }
        this.currentUser = null;
        localStorage.removeItem('skillbridge_user');
        UI.showToast('Logged out', 'info');
        window.location.href = '/login';
    },

    updateUI() {
        // This will be called after checking auth status
        const navAuth = document.getElementById('navAuth');
        if (!navAuth) return;

        if (this.currentUser) {
            navAuth.innerHTML = `
                <span style="margin-right:1rem">👤 ${this.currentUser.firstName}</span>
                <a href="/dashboard" class="btn-outline" style="margin-right:0.5rem">Dashboard</a>
                <button class="btn-primary" onclick="Auth.logout()">Logout</button>
            `;
        } else {
            navAuth.innerHTML = `
                <button class="btn-outline" onclick="Auth.showLogin()">Log In</button>
                <button class="btn-primary" onclick="Auth.showRegister()">Sign Up</button>
            `;
        }
    },

    async checkAuthStatus() {
        try {
            const response = await fetch('/api/user');
            const data = await response.json();
            if (data.success) {
                this.currentUser = data.user;
                saveAuthUser(data.user);
            } else {
                this.currentUser = null;
                localStorage.removeItem('skillbridge_user');
            }
        } catch (error) {
            this.currentUser = null;
        }
        this.updateUI();
    }
};

function saveAuthUser(user) {
    if (!user) return;
    const name = user.name || [user.firstName, user.lastName].filter(Boolean).join(' ');
    if (!name) return;
    localStorage.setItem('skillbridge_user', JSON.stringify({
        name,
        firstName: user.firstName || null,
        lastName: user.lastName || null,
        email: user.email || null
    }));
}

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', () => Auth.init());