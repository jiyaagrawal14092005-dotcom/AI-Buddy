import { useEffect, useRef, useState } from "react";
import { Sparkles, Mic, Send } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useBuddy } from "../context/BuddyContext";

import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";
import ChatBox from "../components/chat/ChatBox";

import TaskCard from "../components/tasks/TaskCard";
import ScheduleCard from "../components/scheduler/ScheduleCard";
import ActivityCard from "../components/execution/ActivityCard";
import MemoryCard from "../components/dashboard/MemoryCard";
import AgentNetwork from "../components/dashboard/AgentNetwork";
import Timer from "../components/scheduler/Timer";
import UpcomingTasks from "../components/tasks/UpcomingTasks";


function Dashboard() {

    const navigate = useNavigate();

    const {
        buddyStatus,
        isThinking,
    } = useBuddy();


    const [activeAction, setActiveAction] =
        useState("");

    const [command, setCommand] =
        useState("");

    const [isListening, setIsListening] =
        useState(false);

    const [voiceMessage, setVoiceMessage] =
        useState("");


    const recognitionRef =
        useRef(null);


    /* =================================================
       VOICE RECOGNITION SETUP
    ================================================= */

    useEffect(() => {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;


        if (!SpeechRecognition) {
            return;
        }


        const recognition =
            new SpeechRecognition();


        recognition.continuous = false;

        recognition.interimResults = false;

        recognition.lang = "en-IN";


        recognition.onstart = () => {

            setIsListening(true);

            setVoiceMessage(
                "Listening..."
            );

        };


        recognition.onresult = (event) => {

            const spokenText =
                event.results[0][0].transcript;


            setCommand(spokenText);

            setVoiceMessage(
                `Heard: "${spokenText}"`
            );


            /*
             * Give React a moment to update
             * the command state before executing.
             */

            setTimeout(() => {

                executeCommand(
                    spokenText
                );

            }, 150);

        };


        recognition.onerror = (event) => {

            console.error(
                "Voice recognition error:",
                event.error
            );


            setIsListening(false);


            if (
                event.error ===
                "not-allowed"
            ) {

                setVoiceMessage(
                    "Microphone permission denied."
                );

            } else if (
                event.error ===
                "no-speech"
            ) {

                setVoiceMessage(
                    "I couldn't hear anything."
                );

            } else {

                setVoiceMessage(
                    "Voice recognition failed. Try again."
                );

            }

        };


        recognition.onend = () => {

            setIsListening(false);

        };


        recognitionRef.current =
            recognition;
           


        return () => {

            recognition.stop();

            recognitionRef.current =
                null;

        };

    }, []);


    /* =================================================
       QUICK ACTION
    ================================================= */

    const handleQuickAction = (
        action
    ) => {

        setActiveAction(action);

    };


    /* =================================================
       COMMAND EXECUTION
    ================================================= */

    const executeCommand = (
        inputCommand
    ) => {

        const userCommand =
            inputCommand
                .trim()
                .toLowerCase();


        if (!userCommand) {
            return;
        }


        /* ===============================
           CREATE TASK
        =============================== */

        if (
            userCommand.includes(
                "create task"
            ) ||
            userCommand.includes(
                "add task"
            ) ||
            userCommand.includes(
                "new task"
            ) ||
            userCommand === "task"
        ) {

            setCommand("");

            setActiveAction("task");


            navigate("/tasks", {
                state: {
                    openForm: true,
                },
            });

            return;
        }


        /* ===============================
           TRAVEL
        =============================== */

        if (
            userCommand.includes(
                "travel"
            ) ||
            userCommand.includes(
                "trip"
            ) ||
            userCommand.includes(
                "travel plan"
            )
        ) {

            setCommand("");

            setActiveAction(
                "travel"
            );


            navigate("/schedule", {
                state: {
                    eventType: "travel",
                },
            });

            return;
        }


        /* ===============================
           WORKFLOW
        =============================== */

        if (
            userCommand.includes(
                "workflow"
            ) ||
            userCommand.includes(
                "automation"
            ) ||
            userCommand.includes(
                "automate"
            )
        ) {

            setCommand("");

            setActiveAction(
                "workflow"
            );


            navigate("/workflows", {
                state: {
                    openForm: true,
                },
            });

            return;
        }


        /* ===============================
           MEMORY
        =============================== */

        if (
            userCommand.includes(
                "save memory"
            ) ||
            userCommand.includes(
                "add memory"
            ) ||
            userCommand.includes(
                "remember this"
            ) ||
            userCommand.includes(
                "remember"
            )
        ) {

            setCommand("");

            setActiveAction(
                "memory"
            );


            navigate("/memory", {
                state: {
                    openForm: true,
                },
            });

            return;
        }


        /* ===============================
           STUDY / ASSISTANT
        =============================== */

        if (
            userCommand.includes(
                "study"
            ) ||
            userCommand.includes(
                "study help"
            ) ||
            userCommand.includes(
                "explain"
            ) ||
            userCommand.includes(
                "learn"
            )
        ) {

            setCommand("");

            navigate("/assistant");

            return;
        }


        /* ===============================
           SCHEDULE
        =============================== */

        if (
            userCommand.includes(
                "schedule"
            ) ||
            userCommand.includes(
                "plan my day"
            ) ||
            userCommand.includes(
                "add event"
            ) ||
            userCommand.includes(
                "calendar"
            )
        ) {

            setCommand("");

            setActiveAction(
                "schedule"
            );


            navigate("/schedule");

            return;
        }


        /* ===============================
           FOCUS MODE
        =============================== */

        if (
            userCommand.includes(
                "focus"
            ) ||
            userCommand.includes(
                "start focus"
            ) ||
            userCommand.includes(
                "pomodoro"
            ) ||
            userCommand.includes(
                "timer"
            )
        ) {

            setCommand("");

            setActiveAction(
                "focus"
            );


            setTimeout(() => {

                document
                    .getElementById(
                        "zarvis-timer"
                    )
                    ?.scrollIntoView({
                        behavior:
                            "smooth",
                        block:
                            "center",
                    });

            }, 100);


            return;
        }


        /* ===============================
           OPEN ASSISTANT
        =============================== */

        if (
            userCommand.includes(
                "assistant"
            ) ||
            userCommand.includes(
                "chat with zarvis"
            ) ||
            userCommand.includes(
                "help me"
            )
        ) {

            setCommand("");

            navigate(
                "/assistant"
            );

            return;
        }


        /* ===============================
           UNKNOWN COMMAND
        =============================== */

        setActiveAction(
            `command:${inputCommand.trim()}`
        );

        setCommand("");

    };


    /* =================================================
       TEXT COMMAND
    ================================================= */

    const handleCommand = () => {

        executeCommand(
            command
        );

    };


    /* =================================================
       VOICE BUTTON
    ================================================= */

    const handleVoiceCommand = () => {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;


        if (!SpeechRecognition) {

            setVoiceMessage(
                "Voice recognition is not supported in this browser."
            );

            return;

        }


        if (isListening) {

            recognitionRef.current?.stop();

            setIsListening(false);

            setVoiceMessage(
                "Voice input stopped."
            );

            return;

        }


        setVoiceMessage(
            "Starting voice input..."
        );


        try {

            recognitionRef.current?.start();

        } catch (error) {

            console.error(
                "Could not start voice recognition:",
                error
            );

            setIsListening(false);

        }

    };


    /* =================================================
       TIMER
    ================================================= */

    const handleStartTimer = () => {

        setActiveAction(
            "focus"
        );


        document
            .getElementById(
                "zarvis-timer"
            )
            ?.scrollIntoView({
                behavior:
                    "smooth",
                block:
                    "center",
            });

    };


    return (

        <div className="app">


            {/* =================================================
                SIDEBAR
            ================================================= */}

            <Sidebar />


            <main className="main-content">


                <Navbar />


                <div className="dashboard">


                    {/* =================================================
                        HERO
                    ================================================= */}

                    <section className="dashboard-hero">


                        <div className="dashboard-welcome">


                            <div className="welcome-label">

                                <span className="welcome-spark">
                                    ✦
                                </span>

                                GOOD MORNING

                            </div>


                            <h1>

                                Hello,{" "}

                                <span>
                                    Shanu
                                </span>

                            </h1>


                            <p>

                                Your AI buddy is here to make your day

                                <br />

                                smarter, simpler and more productive.

                            </p>


                            {/* HERO QUICK ACTIONS */}

                            <div className="hero-quick-actions">


                                <button
                                    type="button"
                                    onClick={() =>
                                        navigate(
                                            "/schedule"
                                        )
                                    }
                                >

                                    <span>
                                        ◫
                                    </span>

                                    Plan My Day

                                </button>


                                <button
                                    type="button"
                                    onClick={() =>
                                        navigate(
                                            "/assistant"
                                        )
                                    }
                                >

                                    <span>
                                        ▣
                                    </span>

                                    Study Help

                                </button>


                                <button
                                    type="button"
                                    onClick={() =>
                                        navigate(
                                            "/schedule",
                                            {
                                                state: {
                                                    eventType:
                                                        "travel",
                                                },
                                            }
                                        )
                                    }
                                >

                                    <span>
                                        ✈
                                    </span>

                                    Travel Plans

                                </button>


                                <button
                                    type="button"
                                    onClick={() =>
                                        navigate(
                                            "/tasks",
                                            {
                                                state: {
                                                    openForm:
                                                        true,
                                                },
                                            }
                                        )
                                    }
                                >

                                    <span>
                                        ＋
                                    </span>

                                    Create Task

                                </button>


                            </div>


                            {/* HERO STATUS */}

                            <div className="hero-status-cards">


                                <div className="hero-status-card thinking-card">


                                    <div className="hero-status-icon zarvis-thinking-logo">

                                        <Sparkles
                                            size={27}
                                            strokeWidth={2.2}
                                        />

                                    </div>


                                    <div className="hero-status-content">

                                        <strong>
                                            Zarvis Thinking
                                        </strong>


                                        <span>

                                            {isThinking
                                                ? "Analyzing your request..."
                                                : "Ready to understand your request."}

                                        </span>


                                        <div className="thinking-wave">

                                            <i></i>
                                            <i></i>
                                            <i></i>
                                            <i></i>
                                            <i></i>
                                            <i></i>
                                            <i></i>
                                            <i></i>
                                            <i></i>

                                        </div>

                                    </div>

                                </div>


                                <div className="hero-status-card ready-card">


                                    <div className="hero-status-icon ready-help-icon">
                                        💬
                                    </div>


                                    <div className="hero-status-content">

                                        <strong>
                                            Ready to Help
                                        </strong>

                                        <span>
                                            Just tell me what you need!
                                        </span>


                                        <div className="ready-indicator">

                                            <span></span>

                                        </div>

                                    </div>

                                </div>


                            </div>


                        </div>


                        {/* =================================================
                            ROBOT
                        ================================================= */}

                        <ChatBox />


                        {/* =================================================
                            COMMAND SEARCH
                        ================================================= */}

                        <div className="hero-search-bar">


                            <div className="hero-search-logo">

                                <Sparkles
                                    size={18}
                                    strokeWidth={2}
                                />

                            </div>

<input
    type="text"
    value={command}
    onChange={(e) =>
        setCommand(e.target.value)
    }
    onFocus={() => {
        navigate("/chat", {
            state: {
                message: command,
            },
        });
    }}
    placeholder="Type your command or ask me anything..."
/>

                            <div className="hero-search-actions">


                                {/* VOICE */}

                                <button
                                    type="button"
                                    className={`hero-search-voice ${isListening
                                            ? "listening"
                                            : ""
                                        }`}
                                    aria-label={
                                        isListening
                                            ? "Stop voice command"
                                            : "Start voice command"
                                    }
                                    onClick={
                                        handleVoiceCommand
                                    }
                                >

                                    <Mic
                                        size={19}
                                        strokeWidth={2}
                                    />

                                </button>


                                {/* SEND */}

                                <button
                                    type="button"
                                    className="hero-search-send"
                                    aria-label="Send command"
                                    onClick={
                                        handleCommand
                                    }
                                >

                                    <Send
                                        size={18}
                                        strokeWidth={2}
                                    />

                                </button>


                            </div>

                        </div>


                        {/* VOICE STATUS */}

                        {voiceMessage && (

                            <div className="voice-command-status">

                                <span
                                    className={
                                        isListening
                                            ? "voice-status-active"
                                            : ""
                                    }
                                ></span>

                                {voiceMessage}

                            </div>

                        )}


                    </section>


                    {/* =================================================
                        STATS
                    ================================================= */}

                    <section className="stats-grid">


                        <div className="stat-card">

                            <div className="stat-card-top">

                                <span className="stat-label">
                                    TODAY'S TASKS
                                </span>

                                <span className="stat-icon">
                                    ✓
                                </span>

                            </div>

                            <strong className="stat-value">
                                08
                            </strong>

                            <span className="stat-description">
                                5 completed
                            </span>

                        </div>


                        <div className="stat-card">

                            <div className="stat-card-top">

                                <span className="stat-label">
                                    ACTIVE WORKFLOWS
                                </span>

                                <span className="stat-icon">
                                    ⚡
                                </span>

                            </div>

                            <strong className="stat-value">
                                03
                            </strong>

                            <span className="stat-description">
                                2 running now
                            </span>

                        </div>


                        <div className="stat-card">

                            <div className="stat-card-top">

                                <span className="stat-label">
                                    SCHEDULED
                                </span>

                                <span className="stat-icon">
                                    ◷
                                </span>

                            </div>

                            <strong className="stat-value">
                                06
                            </strong>

                            <span className="stat-description">
                                Next at 10:00 AM
                            </span>

                        </div>


                        <div className="stat-card">

                            <div className="stat-card-top">

                                <span className="stat-label">
                                    ZARVIS STATUS
                                </span>

                                <span className="stat-icon">
                                    ●
                                </span>

                            </div>

                            <strong className="stat-value">
                                {buddyStatus}
                            </strong>

                            <span className="stat-description">
                                Core operating normally
                            </span>

                        </div>


                    </section>


                    {/* =================================================
                        QUICK COMMANDS
                    ================================================= */}

                    <section className="quick-section">


                        <div className="section-title-row">


                            <div>

                                <span className="section-eyebrow">
                                    QUICK COMMANDS
                                </span>

                                <h2>
                                    What should Zarvis do?
                                </h2>

                            </div>


                            <button
                                type="button"
                                className="section-link"
                                onClick={() =>
                                    navigate(
                                        "/assistant"
                                    )
                                }
                            >
                                Open Assistant →
                            </button>


                        </div>


                        <div className="quick-actions-grid">


                            {/* CREATE TASK */}

                            <button
                                type="button"
                                className={`quick-action-card ${activeAction ===
                                        "task"
                                        ? "active"
                                        : ""
                                    }`}
                                onClick={() =>
                                    navigate(
                                        "/tasks",
                                        {
                                            state: {
                                                openForm:
                                                    true,
                                            },
                                        }
                                    )
                                }
                            >

                                <span className="quick-action-icon">
                                    ✓
                                </span>

                                <strong>
                                    Create Task
                                </strong>

                                <span>
                                    Add something to your day
                                </span>

                            </button>


                            {/* SCHEDULE */}

                            <button
                                type="button"
                                className={`quick-action-card ${activeAction ===
                                        "schedule"
                                        ? "active"
                                        : ""
                                    }`}
                                onClick={() =>
                                    navigate(
                                        "/schedule"
                                    )
                                }
                            >

                                <span className="quick-action-icon">
                                    ◷
                                </span>

                                <strong>
                                    Schedule
                                </strong>

                                <span>
                                    Plan an upcoming event
                                </span>

                            </button>


                            {/* WORKFLOW */}

                            <button
                                type="button"
                                className={`quick-action-card ${activeAction ===
                                        "workflow"
                                        ? "active"
                                        : ""
                                    }`}
                                onClick={() =>
                                    navigate(
                                        "/workflows",
                                        {
                                            state: {
                                                openForm:
                                                    true,
                                            },
                                        }
                                    )
                                }
                            >

                                <span className="quick-action-icon">
                                    ⚡
                                </span>

                                <strong>
                                    New Workflow
                                </strong>

                                <span>
                                    Automate a sequence
                                </span>

                            </button>


                            {/* MEMORY */}

                            <button
                                type="button"
                                className={`quick-action-card ${activeAction ===
                                        "memory"
                                        ? "active"
                                        : ""
                                    }`}
                                onClick={() =>
                                    navigate(
                                        "/memory",
                                        {
                                            state: {
                                                openForm:
                                                    true,
                                            },
                                        }
                                    )
                                }
                            >

                                <span className="quick-action-icon">
                                    ◈
                                </span>

                                <strong>
                                    Save Memory
                                </strong>

                                <span>
                                    Tell Zarvis something
                                </span>

                            </button>


                            {/* FOCUS MODE */}

                            <button
                                type="button"
                                className={`quick-action-card ${activeAction ===
                                        "focus"
                                        ? "active"
                                        : ""
                                    }`}
                                onClick={
                                    handleStartTimer
                                }
                            >

                                <span className="quick-action-icon">
                                    ⏱
                                </span>

                                <strong>
                                    Focus Mode
                                </strong>

                                <span>
                                    Start a focused session
                                </span>

                            </button>


                        </div>

                    </section>


                    {/* =================================================
                        COMMAND RESULT
                    ================================================= */}

                    {activeAction && (

                        <div className="dashboard-action-message">


                            <span>
                                COMMAND READY
                            </span>


                            <strong>

                                {activeAction.startsWith(
                                    "command:"
                                )

                                    ? activeAction.replace(
                                        "command:",
                                        ""
                                    )

                                    : activeAction ===
                                        "task"

                                        ? "Create Task selected"

                                        : activeAction ===
                                            "schedule"

                                            ? "Schedule selected"

                                            : activeAction ===
                                                "travel"

                                                ? "Travel Plan selected"

                                                : activeAction ===
                                                    "workflow"

                                                    ? "New Workflow selected"

                                                    : activeAction ===
                                                        "memory"

                                                        ? "Save Memory selected"

                                                        : activeAction ===
                                                            "focus"

                                                            ? "Focus Mode selected"

                                                            : ""}

                            </strong>


                            <button
                                type="button"
                                onClick={() =>
                                    setActiveAction("")
                                }
                            >
                                ×
                            </button>


                        </div>

                    )}


                    {/* =================================================
                        ZARVIS CORE
                    ================================================= */}

                    <section className="zarvis-core-card glass-card">


                        <div className="zarvis-core-header">


                            <div>

                                <span className="section-eyebrow">
                                    ZARVIS CORE
                                </span>

                                <h2>
                                    Your AI Command Center
                                </h2>

                                <p>
                                    Plan, organize and execute
                                    your day with Zarvis.
                                </p>

                            </div>


                            <div className="core-status">

                                <span></span>

                                {buddyStatus}

                            </div>


                        </div>


                        <div className="zarvis-core-metrics">


                            <div>

                                <span>
                                    CORE STATUS
                                </span>

                                <strong>
                                    {isThinking
                                        ? "THINKING"
                                        : "READY"}
                                </strong>

                            </div>


                            <div>

                                <span>
                                    MEMORY
                                </span>

                                <strong>
                                    ACTIVE
                                </strong>

                            </div>


                            <div>

                                <span>
                                    AUTOMATION
                                </span>

                                <strong>
                                    READY
                                </strong>

                            </div>


                            <div>

                                <span>
                                    VOICE
                                </span>

                                <strong>
                                    READY
                                </strong>

                            </div>


                        </div>

                    </section>


                    {/* =================================================
                        MAIN DASHBOARD
                    ================================================= */}

                    <div className="dashboard-main-grid">

                        <TaskCard />

                        <ScheduleCard />

                        <ActivityCard />

                    </div>


                    {/* =================================================
                        SECONDARY DASHBOARD
                    ================================================= */}

                    <div className="dashboard-secondary-grid">


                        <MemoryCard />


                        <div id="zarvis-timer">

                            <Timer />

                        </div>


                        <UpcomingTasks />


                    </div>


                    {/* =================================================
                        AGENT NETWORK
                    ================================================= */}

                    <AgentNetwork />


                </div>

            </main>

        </div>

    );

}


export default Dashboard;