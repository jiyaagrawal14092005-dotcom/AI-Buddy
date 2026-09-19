// ==========================================
// ZARVIS CHAT SERVICE
// ==========================================

import api from "./api";

// ==========================================
// Send a message to Zarvis
// ==========================================
export async function sendMessage(message, userId) {
    if (!message || !message.trim()) {
        throw new Error("Message cannot be empty.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    return api.post("/api/chat", {
        message: message.trim(),
        user_id: userId,
    });
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
export async function sendCommand(command, userId) {
    if (!command || !command.trim()) {
        throw new Error("Command cannot be empty.");
    }

    if (!userId) {
        throw new Error("User ID is required.");
    }

    return api.post("/api/chat", {
        message: command.trim(),
        user_id: userId,
    });
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