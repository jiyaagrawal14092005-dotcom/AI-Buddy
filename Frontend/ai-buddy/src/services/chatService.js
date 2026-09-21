// ==========================================
// ZARVIS CHAT SERVICE
// ==========================================

import api from "./api";

// ==========================================
// Send a message to Zarvis
// ==========================================
export async function sendMessage(
    message,
    userId,
    approvalId = null
) {
    if (!message || !message.trim()) {
        throw new Error("Message cannot be empty.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    const payload = {
        message: message.trim(),
        user_id: userId,
    };

    // Send approval_id only when the user has
    // explicitly approved the pending action.
    if (approvalId) {
        payload.approval_id = approvalId;
    }

    return api.post("/api/chat", payload);
}

// ==========================================
// Get chat history
// ==========================================
export async function getChatHistory() {
    return api.get("/api/chat/history");
}

// ==========================================
// Clear chat history
// ==========================================
export async function clearChatHistory() {
    return api.delete("/api/chat/history");
}

// ==========================================
// Send voice/text command
// ==========================================
export async function sendCommand(
    command,
    userId,
    approvalId = null
) {
    if (!command || !command.trim()) {
        throw new Error("Command cannot be empty.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    const payload = {
        message: command.trim(),
        user_id: userId,
    };

    if (approvalId) {
        payload.approval_id = approvalId;
    }

    return api.post("/api/chat", payload);
}

// ==========================================
// Export service
// ==========================================
const chatService = {
    sendMessage,
    getChatHistory,
    clearChatHistory,
    sendCommand,
};

export default chatService;