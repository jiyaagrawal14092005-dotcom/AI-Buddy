// ==========================================
// ZARVIS AUTH CONTEXT
// ==========================================

import { createContext, useContext, useEffect, useState } from "react";
import authService from "../services/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [authenticated, setAuthenticated] = useState(false);

    // Check existing authentication
    useEffect(() => {
        const checkUser = async () => {
            try {
                const result = await authService.checkAuth();

                setAuthenticated(result.authenticated);
                setUser(result.user);
            } catch (error) {
                console.error("Authentication check failed:", error);
                setAuthenticated(false);
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        checkUser();
    }, []);

    // Login
    const login = async (credentials) => {
        setLoading(true);

        try {
            const result = await authService.login(credentials);

            const loggedInUser = result?.user || result;

            setUser(loggedInUser);
            setAuthenticated(true);

            return result;
        } finally {
            setLoading(false);
        }
    };

    // Register
    const register = async (userData) => {
        setLoading(true);

        try {
            const result = await authService.register(userData);

            return result;
        } finally {
            setLoading(false);
        }
    };

    // Logout
    const logout = async () => {
        setLoading(true);

        try {
            await authService.logout();
        } catch (error) {
            console.error("Logout error:", error);
        } finally {
            setUser(null);
            setAuthenticated(false);
            setLoading(false);
        }
    };

    const value = {
        user,
        loading,
        authenticated,
        login,
        register,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

// Custom hook
export function useAuth() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error(
            "useAuth must be used inside AuthProvider."
        );
    }

    return context;
}

export default AuthContext;