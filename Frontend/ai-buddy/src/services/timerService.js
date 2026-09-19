import api from "./api";

/**
 * Create a new timer on the backend.
 *
 * @param {number} durationSeconds
 * @returns {Promise<object>}
 */
export async function createTimer(durationSeconds) {
    if (!durationSeconds || durationSeconds <= 0) {
        throw new Error("Timer duration must be greater than zero.");
    }

    return api.post(
        `/api/timer/create?duration_seconds=${durationSeconds}`
    );
}

/**
 * Start an existing backend timer.
 *
 * @param {number} timerId
 * @returns {Promise<object>}
 */
export async function startTimer(timerId) {
    if (!timerId) {
        throw new Error("Timer ID is required.");
    }

    return api.post(`/api/timer/${timerId}/start`);
}

/**
 * Get the current status of a backend timer.
 *
 * @param {number} timerId
 * @returns {Promise<object>}
 */
export async function getTimer(timerId) {
    if (!timerId) {
        throw new Error("Timer ID is required.");
    }

    return api.get(`/api/timer/${timerId}`);
}

/**
 * Get all backend timers.
 *
 * @returns {Promise<object>}
 */
export async function getAllTimers() {
    return api.get("/api/timer/");
}

/**
 * Cancel an existing backend timer.
 *
 * @param {number} timerId
 * @returns {Promise<object>}
 */
export async function cancelTimer(timerId) {
    if (!timerId) {
        throw new Error("Timer ID is required.");
    }

    return api.post(`/api/timer/${timerId}/cancel`);
}

/**
 * Remove an existing backend timer.
 *
 * @param {number} timerId
 * @returns {Promise<object>}
 */
export async function removeTimer(timerId) {
    if (!timerId) {
        throw new Error("Timer ID is required.");
    }

    return api.delete(`/api/timer/${timerId}`);
}

const timerService = {
    createTimer,
    startTimer,
    getTimer,
    getAllTimers,
    cancelTimer,
    removeTimer,
};

export default timerService;