// ==========================================
// AI BUDDY WORKFLOW SERVICE
// ==========================================

import api from "./api";

// ------------------------------------------
// GET ALL WORKFLOWS
// ------------------------------------------

export async function getWorkflows(userId) {
    if (!userId) {
        throw new Error("User ID is required.");
    }

    return api.get(
        `/api/workflows/?user_id=${userId}`
    );
}


// ------------------------------------------
// GET SINGLE WORKFLOW
// ------------------------------------------

export async function getWorkflow(workflowId, userId) {
    if (!workflowId) {
        throw new Error("Workflow ID is required.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    return api.get(
        `/api/workflows/${workflowId}?user_id=${userId}`
    );
}


// ------------------------------------------
// CREATE WORKFLOW
// ------------------------------------------

export async function createWorkflow(
    workflow,
    userId
) {
    if (!workflow || !workflow.name?.trim()) {
        throw new Error(
            "Workflow name is required."
        );
    }

    if (!workflow.tool?.trim()) {
        throw new Error(
            "Workflow tool is required."
        );
    }

    if (!userId) {
        throw new Error(
            "User ID is required."
        );
    }

    const name = encodeURIComponent(
        workflow.name.trim()
    );

    const tool = encodeURIComponent(
        workflow.tool.trim()
    );

    const parameters = encodeURIComponent(
        JSON.stringify(
            workflow.parameters || {}
        )
    );

    return api.post(
        `/api/workflows/create?name=${name}&tool=${tool}&user_id=${userId}&parameters=${parameters}`
    );
}


// ------------------------------------------
// CLEAR ALL WORKFLOWS
// ------------------------------------------

export async function clearWorkflows(userId) {
    if (!userId) {
        throw new Error(
            "User ID is required."
        );
    }

    return api.delete(
        `/api/workflows/clear?user_id=${userId}`
    );
}


// ------------------------------------------
// DELETE SINGLE WORKFLOW
// ------------------------------------------

export async function deleteWorkflow(
    workflowId,
    userId
) {
    if (!workflowId) {
        throw new Error(
            "Workflow ID is required."
        );
    }

    if (!userId) {
        throw new Error(
            "User ID is required."
        );
    }

    return api.delete(
        `/api/workflows/${workflowId}?user_id=${userId}`
    );
}


// ------------------------------------------
// WORKFLOW SERVICE STATUS
// ------------------------------------------

export async function getWorkflowServiceStatus() {
    return api.get(
        "/api/workflows/status"
    );
}


// ------------------------------------------
// EXPORT
// ------------------------------------------

const workflowService = {
    getWorkflows,
    getWorkflow,
    createWorkflow,
    clearWorkflows,
    deleteWorkflow,
    getWorkflowServiceStatus,
};

export default workflowService;