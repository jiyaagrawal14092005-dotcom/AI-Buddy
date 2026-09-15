// ==========================================
// ZARVIS AUTH SERVICE
// ==========================================

import api from "./api";

// Login user
export async function login(credentials) {
    if (!credentials?.email || !credentials?.password) {
        throw new Error("Email and password are required.");
    }

    return api.post("/api/auth/login", {
        email: credentials.email.trim(),
        password: credentials.password,
    });
}

// Register new user
export async function register(userData) {
    if (!userData?.email || !userData?.password) {
        throw new Error("Email and password are required.");
    }

    return api.post("/api/auth/register", userData);
}

// Logout user
export async function logout() {
    return api.post("/api/auth/logout");
}

// Get current logged-in user
export async function getCurrentUser() {
    return api.get("/api/auth/me");
}

// Check authentication status
export async function checkAuth() {
    try {
        const user = await getCurrentUser();

        return {
            authenticated: true,
            user,
        };
    } catch (error) {
        return {
            authenticated: false,
            user: null,
        };
    }
}

const authService = {
    login,
    register,
    logout,
    getCurrentUser,
    checkAuth,
};

export default authService;