// ==========================================
// ZARVIS CHAT SERVICE
// ==========================================

import api from "./api";

// Send a message to Zarvis
export async function sendMessage(message) {
    if (!message || !message.trim()) {
        throw new Error("Message cannot be empty.");
    }

    return api.post("/api/chat", {
        message: message.trim(),
    });
}

// Get chat history
export async function getChatHistory() {
    return api.get("/api/chat/history");
}

// Clear chat history
export async function clearChatHistory() {
    return api.delete("/api/chat/history");
}

// Send voice/text command
export async function sendCommand(command) {
    if (!command || !command.trim()) {
        throw new Error("Command cannot be empty.");
    }

    return api.post("/api/chat/command", {
        command: command.trim(),
    });
}

const chatService = {
    sendMessage,
    getChatHistory,
    clearChatHistory,
    sendCommand,
};

export default chatService;