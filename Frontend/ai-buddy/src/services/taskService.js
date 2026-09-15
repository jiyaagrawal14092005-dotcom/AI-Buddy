// ==========================================
// ZARVIS TASK SERVICE
// ==========================================

import api from "./api";

// Get all tasks
export async function getTasks() {
    return api.get("/api/tasks");
}

// Get a single task
export async function getTask(taskId) {
    return api.get(`/api/tasks/${taskId}`);
}

// Create a new task
export async function createTask(task) {
    if (!task || !task.title?.trim()) {
        throw new Error("Task title is required.");
    }

    return api.post("/api/tasks", {
        ...task,
        title: task.title.trim(),
    });
}

// Update a task
export async function updateTask(taskId, task) {
    return api.put(`/api/tasks/${taskId}`, task);
}

// Mark task as completed
export async function completeTask(taskId) {
    return api.put(`/api/tasks/${taskId}`, {
        completed: true,
    });
}

// Delete a task
export async function deleteTask(taskId) {
    return api.delete(`/api/tasks/${taskId}`);
}

// Get today's tasks
export async function getTodayTasks() {
    return api.get("/api/tasks/today");
}

const taskService = {
    getTasks,
    getTask,
    createTask,
    updateTask,
    completeTask,
    deleteTask,
    getTodayTasks,
};

export default taskService;