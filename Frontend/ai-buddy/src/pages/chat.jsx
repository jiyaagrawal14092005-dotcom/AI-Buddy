import { useState } from "react";
import {
    ArrowLeft,
    Mic,
    Send,
    Sparkles,
} from "lucide-react";

import { useNavigate, useLocation } from "react-router-dom";

import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";

import { sendMessage } from "../services/chatService";

function Chat() {
    const navigate = useNavigate();
    const location = useLocation();

    const [message, setMessage] = useState(
        location.state?.message || ""
    );

    const [messages, setMessages] = useState([
        {
            type: "zarvis",
            text: "Hey! I'm Zarvis. How can I help you?",
            time: "NOW",
        },
    ]);

    const [isLoading, setIsLoading] = useState(false);

    // SEND MESSAGE
    const handleSend = async (e) => {
        e.preventDefault();

        const userMessage = message.trim();

        if (!userMessage || isLoading) return;

        // Show user's message immediately
        setMessages((prev) => [
            ...prev,
            {
                type: "user",
                text: userMessage,
                time: "NOW",
            },
        ]);

        setMessage("");
        setIsLoading(true);

        try {
            // Send message to Zarvis backend
            const response = await sendMessage(userMessage);

            // Get Zarvis response
            const zarvisReply =
                response?.response ||
                response?.message ||
                response?.reply ||
                "I'm processing your request.";

            setMessages((prev) => [
                ...prev,
                {
                    type: "zarvis",
                    text: zarvisReply,
                    time: "NOW",
                },
            ]);
        } catch (error) {
            console.error("Chat error:", error);

            setMessages((prev) => [
                ...prev,
                {
                    type: "zarvis",
                    text: "Sorry, I couldn't connect to Zarvis right now.",
                    time: "NOW",
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    // VOICE INPUT
    const handleVoiceInput = () => {
        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            alert(
                "Voice recognition is not supported in this browser."
            );
            return;
        }

        const recognition = new SpeechRecognition();

        recognition.lang = "en-IN";
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            console.log("Zarvis is listening...");
        };

        recognition.onresult = (event) => {
            const transcript =
                event.results[0][0].transcript;

            setMessage(transcript);
        };

        recognition.onerror = (event) => {
            console.log(
                "Voice recognition error:",
                event.error
            );
        };

        recognition.onend = () => {
            console.log("Voice recognition stopped.");
        };

        recognition.start();
    };

    return (
        <div className="app">

            {/* SIDEBAR */}
            <Sidebar />

            {/* MAIN CONTENT */}
            <main className="main-content">

                {/* NAVBAR */}
                <Navbar />

                {/* CHAT PAGE */}
                <div className="chat-page">

                    {/* HEADER */}
                    <div className="chat-header">

                        <button
                            type="button"
                            onClick={() => navigate("/")}
                            aria-label="Back to dashboard"
                        >
                            <ArrowLeft size={18} />
                        </button>

                        <div>

                            <span>
                                <Sparkles size={14} />
                                ZARVIS
                            </span>

                            <h1>
                                Chat with Zarvis
                            </h1>

                            <p>
                                Give commands, ask questions or talk with your AI buddy.
                            </p>

                        </div>

                    </div>

                    {/* CONVERSATION */}
                    <div className="chat-conversation">

                        {messages.map((msg, index) => (

                            <div
                                key={index}
                                className={`chat-message ${
                                    msg.type === "user"
                                        ? "user-message"
                                        : "zarvis-message"
                                }`}
                            >

                                <div className="chat-message-label">
                                    {msg.type === "user"
                                        ? "YOU"
                                        : "ZARVIS"}
                                </div>

                                <div className="chat-message-text">
                                    {msg.text}
                                </div>

                                <span className="chat-message-time">
                                    {msg.time}
                                </span>

                            </div>

                        ))}

                        {/* THINKING MESSAGE */}
                        {isLoading && (
                            <div className="chat-message zarvis-message">
                                <div className="chat-message-label">
                                    ZARVIS
                                </div>

                                <div className="chat-message-text">
                                    Zarvis is thinking...
                                </div>
                            </div>
                        )}

                    </div>

                    {/* CHAT INPUT */}
                    <form
                        className="chat-input"
                        onSubmit={handleSend}
                    >

                        {/* MIC */}
                        <button
                            type="button"
                            className="chat-mic"
                            aria-label="Voice input"
                            onClick={handleVoiceInput}
                            disabled={isLoading}
                        >
                            <Mic size={18} />
                        </button>

                        {/* INPUT */}
                        <input
                            type="text"
                            value={message}
                            onChange={(e) =>
                                setMessage(e.target.value)
                            }
                            placeholder="Ask Zarvis anything..."
                            disabled={isLoading}
                        />

                        {/* SEND */}
                        <button
                            type="submit"
                            className="chat-send"
                            aria-label="Send message"
                            disabled={
                                isLoading || !message.trim()
                            }
                        >
                            <Send size={17} />
                        </button>

                    </form>

                </div>

            </main>

        </div>
    );
}

export default Chat;