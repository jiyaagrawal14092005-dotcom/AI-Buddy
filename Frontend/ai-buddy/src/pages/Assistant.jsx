import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    Sparkles,
    Mic,
    Bot,
    User,
    Volume2,
    Target,
    Clock3,
    Zap,
    MessageCircle,
    CalendarDays,
    BookOpen,
    Bell,
    CircleHelp,
    CheckCircle2,
    Activity,
} from "lucide-react";

import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";
import { useAuth } from "../context/AuthContext";
import { sendMessage } from "../services/chatService";

function Assistant() {
    const navigate = useNavigate();
    const { user, authenticated } = useAuth();

    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isThinking, setIsThinking] = useState(false);
    const [inputText, setInputText] = useState("");

    const [messages, setMessages] = useState([
        {
            type: "zarvis",
            text: "Hey! I'm Zarvis. I'm listening.",
            time: "NOW",
        },
    ]);

    const recognitionRef = useRef(null);
    const shouldListenRef = useRef(true);
    const speakingRef = useRef(false);
    const thinkingRef = useRef(false);

    // ==========================================
    // KEEP LATEST AUTH STATE AVAILABLE TO VOICE
    // ==========================================

    const userRef = useRef(user);
    const authenticatedRef = useRef(authenticated);

    useEffect(() => {
        userRef.current = user;
        authenticatedRef.current = authenticated;

        console.log("Zarvis auth state updated:", {
            authenticated,
            user,
            userId: user?.id,
        });
    }, [user, authenticated]);

    // ==========================================
    // SPEAK RESPONSE
    // ==========================================

    const speak = (text) => {
        if (!window.speechSynthesis) {
            startListening();
            return;
        }

        window.speechSynthesis.cancel();

        speakingRef.current = true;

        setIsSpeaking(true);
        setIsListening(false);
        setIsThinking(false);
        thinkingRef.current = false;

        const speech = new SpeechSynthesisUtterance(text);

        speech.lang = "en-IN";
        speech.rate = 0.95;
        speech.pitch = 1;

        speech.onend = () => {
            speakingRef.current = false;
            setIsSpeaking(false);

            if (shouldListenRef.current) {
                setTimeout(() => {
                    startListening();
                }, 600);
            }
        };

        speech.onerror = () => {
            speakingRef.current = false;
            setIsSpeaking(false);

            if (shouldListenRef.current) {
                startListening();
            }
        };

        window.speechSynthesis.speak(speech);
    };

    // ==========================================
    // PROCESS COMMAND
    // ==========================================

    const processCommand = async (text) => {
        const cleanText = text?.trim();

        if (!cleanText) return;

        if (recognitionRef.current) {
            try {
                recognitionRef.current.stop();
            } catch {
                // Already stopped
            }
        }

        setIsListening(false);
        setIsThinking(true);
        thinkingRef.current = true;

        setMessages((prev) => [
            ...prev,
            {
                type: "user",
                text: cleanText,
                time: "NOW",
            },
        ]);

        try {
            // ==========================================
            // GET LATEST AUTH STATE
            // ==========================================

            const currentUser = userRef.current;
            const currentAuthenticated = authenticatedRef.current;

            console.log("Zarvis command auth check:", {
                authenticated: currentAuthenticated,
                user: currentUser,
                userId: currentUser?.id,
            });

            if (!currentAuthenticated || !currentUser?.id) {
                throw new Error(
                    "You are not logged in. Please login again."
                );
            }

            // ==========================================
            // REAL BACKEND REQUEST
            // ==========================================

            const result = await sendMessage(
                cleanText,
                currentUser.id
            );

            console.log(
                "Zarvis backend response:",
                result
            );

            const response =
                result?.message ||
                result?.response ||
                result?.reply ||
                "I received your request, but I could not generate a response.";

            setIsThinking(false);
            thinkingRef.current = false;

            setMessages((prev) => [
                ...prev,
                {
                    type: "zarvis",
                    text: response,
                    time: "NOW",
                },
            ]);

            speak(response);

        } catch (error) {
            console.error(
                "Zarvis backend request failed:",
                error
            );

            setIsThinking(false);
            thinkingRef.current = false;

            const errorMessage =
                error?.message ||
                "Sorry, I could not connect to AI Buddy.";

            setMessages((prev) => [
                ...prev,
                {
                    type: "zarvis",
                    text: errorMessage,
                    time: "NOW",
                },
            ]);

            speak(errorMessage);
        }
    };

    // ==========================================
    // START VOICE LISTENING
    // ==========================================

    const startListening = () => {
        if (speakingRef.current) return;

        if (thinkingRef.current) return;

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            console.log(
                "Speech Recognition is not supported by this browser."
            );
            return;
        }

        if (recognitionRef.current) {
            try {
                recognitionRef.current.stop();
            } catch {
                // Already stopped
            }
        }

        const recognition = new SpeechRecognition();

        recognition.lang = "en-IN";
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            setIsListening(true);
            setIsThinking(false);
            thinkingRef.current = false;
        };

        recognition.onresult = (event) => {
            const transcript =
                event.results[0][0].transcript.trim();

            setIsListening(false);

            if (transcript) {
                processCommand(transcript);
            }
        };

        recognition.onerror = (event) => {
            setIsListening(false);

            console.log(
                "Voice recognition error:",
                event.error
            );

            if (
                event.error === "not-allowed" ||
                event.error === "service-not-allowed"
            ) {
                shouldListenRef.current = false;
            }
        };

        recognition.onend = () => {
            setIsListening(false);

            if (
                shouldListenRef.current &&
                !speakingRef.current &&
                !thinkingRef.current
            ) {
                setTimeout(() => {
                    startListening();
                }, 500);
            }
        };

        recognitionRef.current = recognition;

        try {
            recognition.start();
        } catch (error) {
            console.log(
                "Recognition start error:",
                error
            );
        }
    };

    // ==========================================
    // QUICK COMMAND
    // ==========================================

    const handleQuickCommand = (command) => {
        processCommand(command);
    };

    // ==========================================
    // TEXT INPUT
    // ==========================================

    const handleTextSubmit = (e) => {
        e.preventDefault();

        if (!inputText.trim()) return;

        processCommand(inputText);

        setInputText("");
    };

    // ==========================================
    // INITIALIZE VOICE ASSISTANT
    // ==========================================

    useEffect(() => {
        shouldListenRef.current = true;

        const timer = setTimeout(() => {
            startListening();
        }, 1000);

        return () => {
            shouldListenRef.current = false;

            clearTimeout(timer);

            if (recognitionRef.current) {
                try {
                    recognitionRef.current.stop();
                } catch {
                    // Already stopped
                }
            }

            window.speechSynthesis?.cancel();
        };
    }, []);

    return (
        <div className="app">
            <Sidebar />

            <main className="main-content">
                <Navbar />

                <div className="assistant-page">

                    <section className="assistant-header">
                        <div className="assistant-header-content">
                            <span className="assistant-eyebrow">
                                <Sparkles size={13} />
                                ZARVIS AI ASSISTANT
                            </span>

                            <h1>
                                What can I help you with?
                            </h1>

                            <p>
                                Speak naturally. Zarvis listens,
                                thinks and responds automatically.
                            </p>
                        </div>

                        <div className="assistant-online">
                            <span></span>
                            ZARVIS ONLINE
                        </div>
                    </section>

                    <div className="assistant-quick-commands">

                        <button
                            type="button"
                            onClick={() =>
                                handleQuickCommand("Plan my day")
                            }
                        >
                            <CalendarDays size={15} />
                            Plan my day
                        </button>

                        <button
                            type="button"
                            onClick={() =>
                                handleQuickCommand(
                                    "Help me with my studies"
                                )
                            }
                        >
                            <BookOpen size={15} />
                            Help with studies
                        </button>

                        <button
                            type="button"
                            onClick={() =>
                                handleQuickCommand("Set a reminder")
                            }
                        >
                            <Bell size={15} />
                            Set a reminder
                        </button>

                        <button
                            type="button"
                            onClick={() =>
                                handleQuickCommand(
                                    "Answer my question"
                                )
                            }
                        >
                            <CircleHelp size={15} />
                            Any question
                        </button>

                    </div>

                    <div className="assistant-layout">

                        <section className="assistant-main-panel">

                            <div className="assistant-panel-top">

                                <div className="assistant-panel-title">

                                    <div className="assistant-panel-icon">
                                        <MessageCircle size={17} />
                                    </div>

                                    <div>
                                        <span>
                                            ZARVIS CORE
                                        </span>

                                        <strong>
                                            Voice Assistant
                                        </strong>
                                    </div>

                                </div>

                                <div className="assistant-panel-status">

                                    <span></span>

                                    {isListening
                                        ? "LISTENING"
                                        : isSpeaking
                                            ? "SPEAKING"
                                            : isThinking
                                                ? "THINKING"
                                                : "READY"}

                                </div>

                            </div>

                            <div className="assistant-voice-center">

                                <div
                                    className={`assistant-voice-orb ${
                                        isListening
                                            ? "voice-orb-listening"
                                            : isSpeaking
                                                ? "voice-orb-speaking"
                                                : isThinking
                                                    ? "voice-orb-thinking"
                                                    : ""
                                    }`}
                                >

                                    <div className="assistant-orb-ring orb-ring-1"></div>
                                    <div className="assistant-orb-ring orb-ring-2"></div>
                                    <div className="assistant-orb-ring orb-ring-3"></div>

                                    <div className="assistant-orb-particles">
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>

                                    <div className="assistant-orb-core">

                                        {isSpeaking ? (
                                            <Volume2 size={31} />
                                        ) : isListening ? (
                                            <Mic size={31} />
                                        ) : (
                                            <Sparkles size={31} />
                                        )}

                                    </div>

                                </div>

                                <h2>
                                    {isListening
                                        ? "I'm listening..."
                                        : isSpeaking
                                            ? "I'm speaking..."
                                            : isThinking
                                                ? "Thinking..."
                                                : "Ready for you"}
                                </h2>

                                <p>
                                    {isListening
                                        ? "Tell me what you need."
                                        : isSpeaking
                                            ? "Zarvis is responding."
                                            : isThinking
                                                ? "Processing your command..."
                                                : "Just speak naturally."}
                                </p>

                                <div
                                    className={`assistant-waveform ${
                                        isListening || isSpeaking
                                            ? "wave-active"
                                            : ""
                                    }`}
                                >
                                    {Array.from({
                                        length: 25,
                                    }).map((_, index) => (
                                        <span
                                            key={index}
                                            style={{
                                                animationDelay:
                                                    `${index * 0.045}s`,
                                            }}
                                        ></span>
                                    ))}
                                </div>

                            </div>

                            <div className="assistant-conversation">

                                <div className="conversation-label">
                                    <Activity size={12} />
                                    LIVE CONVERSATION
                                </div>

                                {messages
                                    .slice(-4)
                                    .map((message, index) => (
                                        <div
                                            key={index}
                                            className={`conversation-message ${
                                                message.type === "user"
                                                    ? "conversation-user"
                                                    : "conversation-zarvis"
                                            }`}
                                        >

                                            <div className="conversation-avatar">

                                                {message.type === "user" ? (
                                                    <User size={14} />
                                                ) : (
                                                    <Bot size={14} />
                                                )}

                                            </div>

                                            <div className="conversation-content">

                                                <div className="conversation-heading">

                                                    <strong>
                                                        {message.type === "user"
                                                            ? "YOU"
                                                            : "ZARVIS"}
                                                    </strong>

                                                    <span>
                                                        {message.time}
                                                    </span>

                                                </div>

                                                <p>
                                                    {message.text}
                                                </p>

                                            </div>

                                        </div>
                                    ))}

                            </div>

                            <form
                                className="zarvis-chat-input"
                                onSubmit={handleTextSubmit}
                            >

                                <input
                                    type="text"
                                    value={inputText}
                                    onChange={(e) =>
                                        setInputText(e.target.value)
                                    }
                                    placeholder="Ask Zarvis anything..."
                                    disabled={isThinking}
                                />

                                <button
                                    type="submit"
                                    disabled={
                                        isThinking ||
                                        !inputText.trim()
                                    }
                                >
                                    {isThinking
                                        ? "Thinking..."
                                        : "Send"}
                                </button>

                            </form>

                            <div className="assistant-bottom-bar">

                                <div>

                                    <span className="bottom-status-dot"></span>

                                    {isListening
                                        ? "MICROPHONE ACTIVE"
                                        : isSpeaking
                                            ? "VOICE OUTPUT ACTIVE"
                                            : "VOICE SYSTEM READY"}

                                </div>

                                <span>
                                    VOICE ENABLED
                                </span>

                                <span>
                                    ZARVIS CORE
                                </span>

                            </div>

                        </section>

                        <aside className="assistant-side-panel">

                            <section className="assistant-side-card">

                                <div className="side-card-header">

                                    <div>

                                        <div className="side-card-icon">
                                            <Target size={15} />
                                        </div>

                                        <div>
                                            <span>
                                                TODAY
                                            </span>

                                            <h3>
                                                Today's Focus
                                            </h3>
                                        </div>

                                    </div>

                                    <button
                                        type="button"
                                        onClick={() =>
                                            navigate("/tasks")
                                        }
                                    >
                                        View all
                                    </button>

                                </div>

                                <div className="focus-list">

                                    <div className="focus-item completed">
                                        <CheckCircle2 size={16} />
                                        <span>
                                            Complete AI assignment
                                        </span>
                                    </div>

                                    <div className="focus-item">
                                        <div className="empty-check"></div>
                                        <span>
                                            Study Machine Learning
                                        </span>
                                    </div>

                                    <div className="focus-item">
                                        <div className="empty-check"></div>
                                        <span>
                                            Work on Zarvis frontend
                                        </span>
                                    </div>

                                    <div className="focus-item">
                                        <div className="empty-check"></div>
                                        <span>
                                            Review today's notes
                                        </span>
                                    </div>

                                </div>

                            </section>

                            <section className="assistant-side-card">

                                <div className="side-card-header">

                                    <div>

                                        <div className="side-card-icon side-icon-cyan">
                                            <Mic size={15} />
                                        </div>

                                        <div>
                                            <span>
                                                VOICE
                                            </span>

                                            <h3>
                                                Voice Commands
                                            </h3>
                                        </div>

                                    </div>

                                </div>

                                <div className="voice-command-list">

                                    <button
                                        type="button"
                                        onClick={() =>
                                            handleQuickCommand(
                                                "Plan my day"
                                            )
                                        }
                                    >
                                        <Sparkles size={13} />
                                        "Plan my day"
                                    </button>

                                    <button
                                        type="button"
                                        onClick={() =>
                                            handleQuickCommand(
                                                "Remind me at 6 PM"
                                            )
                                        }
                                    >
                                        <Clock3 size={13} />
                                        "Remind me at 6 PM"
                                    </button>

                                    <button
                                        type="button"
                                        onClick={() =>
                                            handleQuickCommand(
                                                "What's next?"
                                            )
                                        }
                                    >
                                        <Zap size={13} />
                                        "What's next?"
                                    </button>

                                    <button
                                        type="button"
                                        onClick={() =>
                                            handleQuickCommand(
                                                "Explain this topic"
                                            )
                                        }
                                    >
                                        <BookOpen size={13} />
                                        "Explain this topic"
                                    </button>

                                </div>

                            </section>

                            <section className="assistant-side-card assistant-system-card">

                                <div className="system-card-title">

                                    <div className="side-card-icon side-icon-purple">
                                        <Activity size={15} />
                                    </div>

                                    <div>
                                        <span>
                                            SYSTEM
                                        </span>

                                        <h3>
                                            Zarvis Status
                                        </h3>
                                    </div>

                                </div>

                                <div className="system-status-row">
                                    <span>
                                        Voice recognition
                                    </span>
                                    <strong>
                                        ACTIVE
                                    </strong>
                                </div>

                                <div className="system-status-row">
                                    <span>
                                        Voice response
                                    </span>
                                    <strong>
                                        ACTIVE
                                    </strong>
                                </div>

                                <div className="system-status-row">
                                    <span>
                                        Zarvis Core
                                    </span>
                                    <strong>
                                        ONLINE
                                    </strong>
                                </div>

                            </section>

                        </aside>

                    </div>

                </div>

            </main>

        </div>
    );
}

export default Assistant;