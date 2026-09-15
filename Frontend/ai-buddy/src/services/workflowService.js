// ==========================================
// ZARVIS WORKFLOW SERVICE
// ==========================================

import api from "./api";

// Get all workflows
export async function getWorkflows() {
    return api.get("/api/workflows");
}

// Get a single workflow
export async function getWorkflow(workflowId) {
    return api.get(`/api/workflows/${workflowId}`);
}

// Create a new workflow
export async function createWorkflow(workflow) {
    if (!workflow || !workflow.name?.trim()) {
        throw new Error("Workflow name is required.");
    }

    return api.post("/api/workflows", {
        ...workflow,
        name: workflow.name.trim(),
    });
}

// Update a workflow
export async function updateWorkflow(workflowId, workflow) {
    return api.put(`/api/workflows/${workflowId}`, workflow);
}

// Run a workflow
export async function runWorkflow(workflowId) {
    return api.post(`/api/workflows/${workflowId}/run`);
}

// Stop a running workflow
export async function stopWorkflow(workflowId) {
    return api.post(`/api/workflows/${workflowId}/stop`);
}

// Delete a workflow
export async function deleteWorkflow(workflowId) {
    return api.delete(`/api/workflows/${workflowId}`);
}

// Get workflow execution status
export async function getWorkflowStatus(workflowId) {
    return api.get(`/api/workflows/${workflowId}/status`);
}

const workflowService = {
    getWorkflows,
    getWorkflow,
    createWorkflow,
    updateWorkflow,
    runWorkflow,
    stopWorkflow,
    deleteWorkflow,
    getWorkflowStatus,
};

export default workflowService;