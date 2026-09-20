// ==========================================
// AI BUDDY TASK SERVICE
// ==========================================

import api from "./api";


// ==========================================
// GET ALL TASKS
// ==========================================

export async function getTasks(userId) {

    if (!userId) {
        throw new Error("User ID is required.");
    }

    return api.get(
        `/api/tasks/?user_id=${userId}`
    );
}


// ==========================================
// GET SINGLE TASK
// ==========================================

export async function getTask(taskId, userId) {

    if (!taskId) {
        throw new Error("Task ID is required.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    return api.get(
        `/api/tasks/${taskId}?user_id=${userId}`
    );
}


// ==========================================
// CREATE TASK
// ==========================================

export async function createTask(task, userId) {

    if (!task || !task.title?.trim()) {
        throw new Error("Task title is required.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    const taskName = encodeURIComponent(
        task.title.trim()
    );

    return api.post(
        `/api/tasks/create?task_name=${taskName}&user_id=${userId}`
    );
}


// ==========================================
// DELETE TASK
// ==========================================

export async function deleteTask(taskId, userId) {

    if (!taskId) {
        throw new Error("Task ID is required.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    return api.delete(
        `/api/tasks/${taskId}?user_id=${userId}`
    );
}


// ==========================================
// UPDATE TASK STATUS
// ==========================================

export async function updateTaskStatus(
    taskId,
    userId,
    status
) {

    if (!taskId) {
        throw new Error("Task ID is required.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    if (!status) {
        throw new Error("Task status is required.");
    }

    return api.put(
        `/api/tasks/${taskId}/status?user_id=${userId}&status=${encodeURIComponent(status)}`
    );
}


// ==========================================
// UPDATE TASK
// ==========================================

export async function updateTask() {

    throw new Error(
        "General task update is not currently supported by the backend."
    );
}


// ==========================================
// COMPLETE TASK
// ==========================================

export async function completeTask(
    taskId,
    userId
) {

    return updateTaskStatus(
        taskId,
        userId,
        "completed"
    );
}


// ==========================================
// GET TODAY'S TASKS
// ==========================================

export async function getTodayTasks(userId) {

    return getTasks(userId);
}


// ==========================================
// EXPORT SERVICE
// ==========================================

const taskService = {

    getTasks,
    getTask,
    createTask,
    updateTask,
    updateTaskStatus,
    completeTask,
    deleteTask,
    getTodayTasks,

};

export default taskService;