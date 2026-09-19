// ==========================================
// ZARVIS AUTH SERVICE
// ==========================================

import api from "./api";

const USER_STORAGE_KEY = "ai_buddy_user";

// ==========================================
// Login user
// ==========================================
export async function login(credentials) {
    if (!credentials?.email || !credentials?.password) {
        throw new Error("Email and password are required.");
    }

    const result = await api.post("/api/auth/login", {
        email: credentials.email.trim(),
        password: credentials.password,
    });

    if (!result?.success || !result?.user) {
        throw new Error(
            result?.message || "Login failed."
        );
    }

    // Store logged-in user for frontend session
    localStorage.setItem(
        USER_STORAGE_KEY,
        JSON.stringify(result.user)
    );

    return result;
}

// ==========================================
// Register new user
// ==========================================
export async function register(userData) {
    if (!userData?.email || !userData?.password) {
        throw new Error("Email and password are required.");
    }

    return api.post("/api/auth/register", userData);
}

// ==========================================
// Logout user
// ==========================================
export async function logout() {
    try {
        await api.post("/api/auth/logout");
    } finally {
        localStorage.removeItem(USER_STORAGE_KEY);
    }

    return {
        success: true,
        message: "Logged out successfully.",
    };
}

// ==========================================
// Get current logged-in user
// ==========================================
export async function getCurrentUser() {
    const storedUser = localStorage.getItem(USER_STORAGE_KEY);

    if (!storedUser) {
        return null;
    }

    try {
        return JSON.parse(storedUser);
    } catch (error) {
        console.error(
            "Failed to read stored user:",
            error
        );

        localStorage.removeItem(USER_STORAGE_KEY);

        return null;
    }
}

// ==========================================
// Check authentication status
// ==========================================
export async function checkAuth() {
    try {
        const user = await getCurrentUser();

        if (!user || !user.id) {
            return {
                authenticated: false,
                user: null,
            };
        }

        return {
            authenticated: true,
            user,
        };
    } catch (error) {
        console.error(
            "Authentication check failed:",
            error
        );

        return {
            authenticated: false,
            user: null,
        };
    }
}

// ==========================================
// Export service
// ==========================================
const authService = {
    login,
    register,
    logout,
    getCurrentUser,
    checkAuth,
};

export default authService;