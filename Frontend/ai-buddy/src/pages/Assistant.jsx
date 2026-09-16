import { useEffect, useRef, useState } from "react";

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

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

function Assistant() {
    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isThinking, setIsThinking] = useState(false);

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

    const getZarvisResponse = (text) => {
        const command = text.toLowerCase();

        if (command.includes("plan my day")) {
            return "Sure! I'll help you plan your day with a balanced schedule.";
        }

        if (
            command.includes("create a task") ||
            command.includes("add task") ||
            command.includes("new task")
        ) {
            return "Sure. Tell me what task you want me to create.";
        }

        if (
            command.includes("schedule") ||
            command.includes("event")
        ) {
            return "Sure. Tell me what you want to schedule and when.";
        }

        if (
            command.includes("remind") ||
            command.includes("reminder")
        ) {
            return "Of course. Tell me what you want me to remind you about.";
        }

        if (
            command.includes("focus") ||
            command.includes("timer")
        ) {
            return "Focus mode is ready. Let's start a productive session.";
        }

        if (
            command.includes("study") ||
            command.includes("learn") ||
            command.includes("explain")
        ) {
            return "Absolutely. Tell me the topic and I'll explain it simply.";
        }

        if (
            command.includes("hello") ||
            command.includes("hi") ||
            command.includes("hey")
        ) {
            return "Hey! I'm Zarvis. What can I help you with?";
        }

        if (
            command.includes("what's next") ||
            command.includes("what is next")
        ) {
            return "Your next priority is to continue your planned tasks. I can organize them for you.";
        }

        return `I heard you say "${text}". I'm ready to help you with that.`;
    };

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

    const processCommand = (text) => {
        if (!text.trim()) return;

        setIsListening(false);
        setIsThinking(true);

        setMessages((prev) => [
            ...prev,
            {
                type: "user",
                text,
                time: "NOW",
            },
        ]);

        const response = getZarvisResponse(text);

        setTimeout(() => {
            setIsThinking(false);

            setMessages((prev) => [
                ...prev,
                {
                    type: "zarvis",
                    text: response,
                    time: "NOW",
                },
            ]);

            speak(response);
        }, 700);
    };

    const startListening = () => {
        if (speakingRef.current) return;

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
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
                !isThinking
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

    const handleQuickCommand = (command) => {
        processCommand(command);
    };

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

                    {/* HEADER */}

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


                    {/* QUICK COMMANDS */}

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
                                handleQuickCommand(
                                    "Set a reminder"
                                )
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


                    {/* MAIN LAYOUT */}

                    <div className="assistant-layout">

                        {/* MAIN VOICE PANEL */}

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


                            {/* VOICE CENTER */}

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


                                {/* WAVEFORM */}

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


                            {/* CONVERSATION */}

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


                            {/* BOTTOM STATUS */}

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


                        {/* RIGHT PANEL */}

                        <aside className="assistant-side-panel">

                            {/* TODAY FOCUS */}

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

                                    <button type="button">
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


                            {/* VOICE COMMANDS */}

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


                            {/* SYSTEM STATUS */}

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