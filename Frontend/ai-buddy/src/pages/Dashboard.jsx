import { useState } from "react";
import { Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useBuddy } from "../context/BuddyContext";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import ChatBox from "../components/ChatBox";

import TaskCard from "../components/TaskCard";
import ScheduleCard from "../components/ScheduleCard";
import ActivityCard from "../components/ActivityCard";
import MemoryCard from "../components/MemoryCard";
import AgentNetwork from "../components/AgentNetwork";
import Timer from "../components/Timer";
import UpcomingTasks from "../components/UpcomingTasks";

function Dashboard() {
    const navigate = useNavigate();

    const {
        buddyStatus,
        isThinking,
        lastCommand,
        lastResponse,
    } = useBuddy();

    const [activeAction, setActiveAction] = useState("");

    const handleQuickAction = (action) => {
        setActiveAction(action);
    };

    const handleStartTimer = () => {
        setActiveAction("");

        document
            .getElementById("zarvis-timer")
            ?.scrollIntoView({
                behavior: "smooth",
                block: "center",
            });
    };

    return (
        <div className="app">

            {/* =================================================
                SIDEBAR
            ================================================= */}

            <Sidebar />

            <main className="main-content">

                {/* =================================================
                    NAVBAR
                ================================================= */}

                <Navbar />

                <div className="dashboard">

                    {/* =================================================
                        HERO SECTION
                    ================================================= */}

                    <section className="dashboard-hero">

                        {/* LEFT SIDE — WELCOME TEXT */}

                        <div className="dashboard-welcome">

                            <div className="welcome-label">
                                <span className="welcome-spark">
                                    ✦
                                </span>

                                GOOD MORNING
                            </div>

                            <h1>
                                Hello,{" "}
                                <span>Shanu</span>
                            </h1>

                            <p>
                                Your AI buddy is here to make your day
                                <br />
                                smarter, simpler and more productive.
                            </p>

                            {/* QUICK HERO ACTIONS */}

                            <div className="hero-quick-actions">

                                <button
                                    type="button"
                                    onClick={() =>
                                        navigate("/schedule")
                                    }
                                >
                                    <span>◫</span>
                                    Plan My Day
                                </button>

                                <button
                                    type="button"
                                    onClick={() =>
                                        navigate("/assistant")
                                    }
                                >
                                    <span>▣</span>
                                    Study Help
                                </button>

                                <button
                                    type="button"
                                    onClick={() =>
                                        navigate("/schedule")
                                    }
                                >
                                    <span>✈</span>
                                    Travel Plans
                                </button>

                                <button
                                    type="button"
                                    onClick={() =>
                                        navigate("/tasks")
                                    }
                                >
                                    <span>＋</span>
                                    Create Task
                                </button>

                            </div>

                            {/* THINKING STATUS */}
<div className="hero-status-cards">

    <div className="hero-status-card thinking-card">

        <div className="hero-status-icon zarvis-thinking-logo">
    <Sparkles size={27} strokeWidth={2.2} />
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
                                    navigate("/assistant")
                                }
                            >
                                Open Assistant →
                            </button>

                        </div>


                        <div className="quick-actions-grid">

                            {/* CREATE TASK */}

                            <button
                                type="button"
                                className={`quick-action-card ${
                                    activeAction === "task"
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    handleQuickAction("task")
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
                                className={`quick-action-card ${
                                    activeAction === "schedule"
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    handleQuickAction("schedule")
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
                                className={`quick-action-card ${
                                    activeAction === "workflow"
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    handleQuickAction("workflow")
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
                                className={`quick-action-card ${
                                    activeAction === "memory"
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    handleQuickAction("memory")
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
                                className="quick-action-card"
                                onClick={handleStartTimer}
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
                        ACTION MESSAGE
                    ================================================= */}

                    {activeAction && (

                        <div className="dashboard-action-message">

                            <span>
                                COMMAND READY
                            </span>

                            <strong>

                                {activeAction === "task" &&
                                    "Create Task selected"}

                                {activeAction === "schedule" &&
                                    "Schedule selected"}

                                {activeAction === "workflow" &&
                                    "New Workflow selected"}

                                {activeAction === "memory" &&
                                    "Save Memory selected"}

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
                        MAIN MODULES
                    ================================================= */}

                    <div className="dashboard-main-grid">

                        <TaskCard />

                        <ScheduleCard />

                        <ActivityCard />

                    </div>


                    {/* =================================================
                        SECONDARY MODULES
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