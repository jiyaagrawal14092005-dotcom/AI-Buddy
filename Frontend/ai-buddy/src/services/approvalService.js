// ==========================================
// ZARVIS APPROVAL SERVICE
// ==========================================

import api from "./api";

// ==========================================
// Approve a pending action
// ==========================================
export async function approveAction(approvalId) {
    if (!approvalId) {
        throw new Error("Approval ID is required.");
    }

    return api.post(
        `/api/approval/${approvalId}/approve`
    );
}

// ==========================================
// Reject a pending action
// ==========================================
export async function rejectAction(approvalId) {
    if (!approvalId) {
        throw new Error("Approval ID is required.");
    }

    return api.post(
        `/api/approval/${approvalId}/reject`
    );
}

// ==========================================
// Get approval request
// ==========================================
export async function getApprovalRequest(approvalId) {
    if (!approvalId) {
        throw new Error("Approval ID is required.");
    }

    return api.get(
        `/api/approval/${approvalId}`
    );
}

// ==========================================
// Export service
// ==========================================
const approvalService = {
    approveAction,
    rejectAction,
    getApprovalRequest,
};

export default approvalService;