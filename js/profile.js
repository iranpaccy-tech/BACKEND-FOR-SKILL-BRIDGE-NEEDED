const PROFILE_STORAGE_KEY = 'skillbridge_user';
const PROFILE_RETRY_COUNT = 10;
const PROFILE_RETRY_DELAY = 250;

function getStoredUser() {
    try {
        const stored = localStorage.getItem(PROFILE_STORAGE_KEY);
        return stored ? JSON.parse(stored) : null;
    } catch (error) {
        return null;
    }
}

function saveStoredUser(user) {
    if (!user) return;
    const name = user.name || [user.firstName, user.lastName].filter(Boolean).join(' ');
    if (!name) return;

    const stored = {
        name,
        firstName: user.firstName || null,
        lastName: user.lastName || null,
        email: user.email || null
    };

    localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(stored));
}

function setProfileLoading() {
    document.querySelectorAll('.profile-avatar').forEach(el => {
        if (!el.textContent.trim()) el.textContent = '…';
        el.classList.add('loading');
    });
    document.querySelectorAll('.profile-name').forEach(el => {
        if (!el.textContent.trim()) el.textContent = 'Loading...';
        el.classList.add('loading');
    });
}

function clearProfileLoading() {
    document.querySelectorAll('.profile-avatar.loading, .profile-name.loading').forEach(el => {
        el.classList.remove('loading');
    });
}

function applyProfile(user) {
    if (!user) return false;
    const name = user.name || [user.firstName, user.lastName].filter(Boolean).join(' ');
    if (!name) return false;

    document.querySelectorAll('.profile-avatar').forEach(el => {
        el.textContent = name.charAt(0).toUpperCase();
        el.classList.remove('loading');
    });

    document.querySelectorAll('.profile-name').forEach(el => {
        el.textContent = name;
        el.classList.remove('loading');
    });

    return true;
}

function initProfileHeader() {
    const storedUser = getStoredUser();
    if (storedUser && storedUser.name) {
        applyProfile(storedUser);
    } else {
        setProfileLoading();
    }

    if (window.Auth) {
        if (Auth.currentUser) {
            applyProfile(Auth.currentUser);
            saveStoredUser(Auth.currentUser);
            return;
        }

        let attempts = 0;
        const checkAuthUser = setInterval(() => {
            attempts += 1;
            if (Auth.currentUser) {
                applyProfile(Auth.currentUser);
                saveStoredUser(Auth.currentUser);
                clearInterval(checkAuthUser);
            } else if (attempts >= PROFILE_RETRY_COUNT) {
                clearInterval(checkAuthUser);
                if (!storedUser) clearProfileLoading();
            }
        }, PROFILE_RETRY_DELAY);
    } else if (!storedUser) {
        setProfileLoading();
        setTimeout(() => {
            if (!getStoredUser()) clearProfileLoading();
        }, PROFILE_RETRY_COUNT * PROFILE_RETRY_DELAY);
    }
}

const Profile = {
    init() {
        this.loadProfile();
    },
    loadProfile() {
        const user = Auth.currentUser;
        if (!user) {
            window.location.href = 'index.html';
            return;
        }
        document.getElementById('profileName').textContent = user.name || [user.firstName, user.lastName].filter(Boolean).join(' ');
        document.getElementById('profileEmail').textContent = user.email || '';
        document.getElementById('profileAvatar').textContent = user.avatar || '';
        document.getElementById('profileRole').textContent = user.role || 'Student';
    },
    edit() {
        UI.showModal('editProfileModal');
    },
    save() {
        const name = document.getElementById('editName').value;
        if (name) {
            const user = Auth.currentUser;
            if (user) {
                user.name = name;
                if (Auth.setUser) {
                    Auth.setUser(user);
                }
                this.loadProfile();
                UI.closeAllModals();
                UI.showToast('Profile updated!', 'success');
            }
        }
    }
};

document.addEventListener('DOMContentLoaded', initProfileHeader);
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('profile.html')) {
        Profile.init();
    }
});