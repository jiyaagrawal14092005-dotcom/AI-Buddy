const chatService = {
    async sendMessage(message) {
        // Real AI API baad me yahan connect hogi
        console.log("Message sent to Zarvis:", message);

        return {
            success: true,
            message: `Zarvis received: "${message}"`,
        };
    },
};

export default chatService;