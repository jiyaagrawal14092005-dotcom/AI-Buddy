// ==========================================
// AI BUDDY SCHEDULER SERVICE
// ==========================================

import api from "./api";

// ==========================================
// SCHEDULE ONE-TIME JOB
// ==========================================

export async function scheduleJob(
    userId,
    delaySeconds,
    name = "AI Buddy Job"
) {
    if (!userId) {
        throw new Error("User ID is required.");
    }

    if (!delaySeconds || delaySeconds <= 0) {
        throw new Error(
            "Delay must be greater than zero."
        );
    }

    const encodedName =
        encodeURIComponent(name.trim());

    return api.post(
        `/api/scheduler/schedule?user_id=${userId}&delay_seconds=${Math.ceil(
            delaySeconds
        )}&name=${encodedName}`
    );
}


// ==========================================
// GET DATABASE JOBS
// ==========================================

export async function getScheduledJobs(
    userId
) {
    if (!userId) {
        throw new Error("User ID is required.");
    }

    return api.get(
        `/api/scheduler/database-jobs?user_id=${userId}`
    );
}


// ==========================================
// GET RUNTIME JOBS
// ==========================================

export async function getRuntimeJobs() {
    return api.get(
        "/api/scheduler/jobs"
    );
}


// ==========================================
// GET SINGLE JOB
// ==========================================

export async function getJob(
    jobId
) {
    if (!jobId) {
        throw new Error("Job ID is required.");
    }

    return api.get(
        `/api/scheduler/jobs/${jobId}`
    );
}


// ==========================================
// CANCEL JOB
// ==========================================

export async function cancelJob(
    jobId
) {
    if (!jobId) {
        throw new Error("Job ID is required.");
    }

    return api.post(
        `/api/scheduler/jobs/${jobId}/cancel`
    );
}


// ==========================================
// REMOVE JOB
// ==========================================

export async function removeJob(
    jobId
) {
    if (!jobId) {
        throw new Error("Job ID is required.");
    }

    return api.delete(
        `/api/scheduler/jobs/${jobId}`
    );
}


// ==========================================
// DEFAULT SERVICE
// ==========================================

const schedulerService = {
    scheduleJob,
    getScheduledJobs,
    getRuntimeJobs,
    getJob,
    cancelJob,
    removeJob,
};

export default schedulerService;