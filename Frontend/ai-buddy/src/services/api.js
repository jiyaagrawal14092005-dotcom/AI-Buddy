// ==========================================
// ZARVIS API SERVICE
// ==========================================

const API_BASE_URL = "http://localhost:8000";

// Common API request handler
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {}),
            },
            ...options,
        });

        if (!response.ok) {
            throw new Error(
                `API Error: ${response.status} ${response.statusText}`
            );
        }

        const contentType = response.headers.get("content-type");

        if (contentType && contentType.includes("application/json")) {
            return await response.json();
        }

        return await response.text();
    } catch (error) {
        console.error("Zarvis API Error:", error);
        throw error;
    }
}

// GET request
export async function get(endpoint) {
    return apiRequest(endpoint, {
        method: "GET",
    });
}

// POST request
export async function post(endpoint, data = {}) {
    return apiRequest(endpoint, {
        method: "POST",
        body: JSON.stringify(data),
    });
}

// PUT request
export async function put(endpoint, data = {}) {
    return apiRequest(endpoint, {
        method: "PUT",
        body: JSON.stringify(data),
    });
}

// DELETE request
export async function remove(endpoint) {
    return apiRequest(endpoint, {
        method: "DELETE",
    });
}

// Default API object
const api = {
    get,
    post,
    put,
    delete: remove,
};

export default api;