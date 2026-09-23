// ==========================================
// ZARVIS AUTH SERVICE
// ==========================================

import api from "./api";

const USER_STORAGE_KEY = "ai_buddy_user";


// ------------------------------------------
// LOGIN USER
// ------------------------------------------

export async function login(credentials) {

    if (!credentials?.email || !credentials?.password) {
        throw new Error(
            "Email and password are required."
        );
    }

    const result = await api.post(
        "/api/auth/login",
        {
            email: credentials.email.trim(),
            password: credentials.password,
        }
    );

    if (!result?.success || !result?.user) {
        throw new Error(
            result?.message || "Login failed."
        );
    }

    localStorage.setItem(
        USER_STORAGE_KEY,
        JSON.stringify(result.user)
    );

    return result;
}


// ------------------------------------------
// REGISTER NEW USER
// ------------------------------------------

export async function register(userData) {

    if (!userData?.email || !userData?.password) {
        throw new Error(
            "Email and password are required."
        );
    }

    return api.post(
        "/api/auth/register",
        userData
    );
}


// ------------------------------------------
// UPDATE USER PROFILE
// ------------------------------------------

export async function updateProfile(
    userId,
    username
) {

    if (!userId) {
        throw new Error(
            "User ID is required."
        );
    }

    if (!username?.trim()) {
        throw new Error(
            "Name cannot be empty."
        );
    }

    const result = await api.put(
        "/api/auth/profile",
        {
            user_id: userId,
            username: username.trim(),
        }
    );

    if (!result?.success || !result?.user) {
        throw new Error(
            result?.message ||
            "Profile update failed."
        );
    }

    // --------------------------------------
    // UPDATE STORED USER
    // --------------------------------------

    localStorage.setItem(
        USER_STORAGE_KEY,
        JSON.stringify(result.user)
    );

    return result;
}


// ------------------------------------------
// LOGOUT USER
// ------------------------------------------

export async function logout() {

    try {

        await api.post(
            "/api/auth/logout"
        );

    } finally {

        localStorage.removeItem(
            USER_STORAGE_KEY
        );
    }

    return {
        success: true,
        message: "Logged out successfully.",
    };
}


// ------------------------------------------
// GET CURRENT LOGGED-IN USER
// ------------------------------------------

export async function getCurrentUser() {

    const storedUser =
        localStorage.getItem(
            USER_STORAGE_KEY
        );

    if (!storedUser) {
        return null;
    }

    try {

        return JSON.parse(
            storedUser
        );

    } catch (error) {

        console.error(
            "Failed to read stored user:",
            error
        );

        localStorage.removeItem(
            USER_STORAGE_KEY
        );

        return null;
    }
}


// ------------------------------------------
// CHECK AUTHENTICATION
// ------------------------------------------

export async function checkAuth() {

    try {

        const user =
            await getCurrentUser();

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


// ------------------------------------------
// EXPORT SERVICE
// ------------------------------------------

const authService = {

    login,
    register,
    updateProfile,
    logout,
    getCurrentUser,
    checkAuth,

};

export default authService;