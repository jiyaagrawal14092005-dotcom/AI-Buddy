import { useState } from "react";
import { useNavigate } from "react-router-dom";

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

            {/* SIDEBAR */}
            <Sidebar />

            {/* MAIN CONTENT */}
            <main className="main-content">

                {/* NAVBAR */}
                <Navbar />

                <div className="dashboard">

                    {/* HERO SECTION */}
                    <section className="dashboard-hero">

                        <div className="dashboard-welcome">

                            <div className="welcome-label">
                                <span className="welcome-spark">
                                    ✦
                                </span>

                                ZARVIS AI COMPANION
                            </div>

                            <h1>
                                Good Morning,
                                <br />
                                <span>Shanu!</span>
                            </h1>

                            <p>
                                Your goals. My priority.
                            </p>

                        </div>

                        <ChatBox />

                    </section>


                    {/* STATS */}
                    <section className="stats-grid">

                        <div className="stat-card glass-card">

                            <div className="stat-top">

                                <div className="stat-icon stat-blue">
                                    ✓
                                </div>

                                <span>
                                    Total Tasks
                                </span>

                            </div>

                            <div className="stat-value">
                                5
                            </div>

                            <div className="stat-label stat-success">
                                ↑ 2 completed today
                            </div>

                        </div>


                        <div className="stat-card glass-card">

                            <div className="stat-top">

                                <div className="stat-icon stat-cyan">
                                    ▣
                                </div>

                                <span>
                                    Today's Events
                                </span>

                            </div>

                            <div className="stat-value">
                                3
                            </div>

                            <div className="stat-label stat-success">
                                ↑ 1 upcoming
                            </div>

                        </div>


                        <div className="stat-card glass-card">

                            <div className="stat-top">

                                <div className="stat-icon stat-pink">
                                    ⚡
                                </div>

                                <span>
                                    Active Workflows
                                </span>

                            </div>

                            <div className="stat-value">
                                1
                            </div>

                            <div className="stat-label">
                                Running
                            </div>

                        </div>


                        <div className="stat-card glass-card">

                            <div className="stat-top">

                                <div className="stat-icon stat-purple">
                                    ♧
                                </div>

                                <span>
                                    Memory Entries
                                </span>

                            </div>

                            <div className="stat-value">
                                8
                            </div>

                            <div className="stat-label stat-success">
                                ↑ 1 new
                            </div>

                        </div>

                    </section>


                    {/* QUICK ACTIONS */}
                    <section className="quick-section">

                        <div className="section-header">

                            <h2 className="section-title">
                                <span>⚡</span>
                                Quick Actions
                            </h2>

                            <button
                                type="button"
                                className="section-link"
                            >
                                View all
                            </button>

                        </div>


                        <div className="quick-actions">

                            {/* ADD TASK */}
                            <button
                                type="button"
                                className="quick-action"
                                onClick={() =>
                                    navigate("/tasks?create=true")
                                }
                            >

                                <div className="quick-action-icon">
                                    ✓
                                </div>

                                <div className="quick-action-title">
                                    Add Task
                                </div>

                                <div className="quick-action-text">
                                    Create a new task
                                </div>

                            </button>


                            {/* ADD EVENT */}
                            <button
                                type="button"
                                className="quick-action"
                                onClick={() =>
                                    navigate("/schedule?create=true")
                                }
                            >

                                <div className="quick-action-icon">
                                    ▣
                                </div>

                                <div className="quick-action-title">
                                    Add Event
                                </div>

                                <div className="quick-action-text">
                                    Schedule something
                                </div>

                            </button>


                            {/* CREATE WORKFLOW */}
                            <button
                                type="button"
                                className="quick-action"
                                onClick={() =>
                                    navigate("/workflows?create=true")
                                }
                            >

                                <div className="quick-action-icon">
                                    ⚡
                                </div>

                                <div className="quick-action-title">
                                    Create Workflow
                                </div>

                                <div className="quick-action-text">
                                    Automate a routine
                                </div>

                            </button>


                            {/* START TIMER */}
                            <button
                                type="button"
                                className="quick-action"
                                onClick={handleStartTimer}
                            >

                                <div className="quick-action-icon">
                                    ◷
                                </div>

                                <div className="quick-action-title">
                                    Start Timer
                                </div>

                                <div className="quick-action-text">
                                    Focus on your work
                                </div>

                            </button>


                            {/* ASK ZARVIS */}
                            <button
                                type="button"
                                className="quick-action"
                                onClick={() =>
                                    navigate("/assistant")
                                }
                            >

                                <div className="quick-action-icon">
                                    💬
                                </div>

                                <div className="quick-action-title">
                                    Ask Zarvis
                                </div>

                                <div className="quick-action-text">
                                    Talk to your AI buddy
                                </div>

                            </button>

                        </div>


                        {/* ACTION RESPONSE */}
                        {activeAction && (
                            <div className="zarvis-response">

                                <span>
                                    ✦
                                </span>

                                <span>
                                    {activeAction} selected.
                                    Zarvis is ready.
                                </span>

                            </div>
                        )}

                    </section>


                    {/* ZARVIS CORE */}
                    <section className="zarvis-core-card glass-card">

                        <div className="core-orb">

                            <div className="core-orb-inner">
                                Z
                            </div>

                        </div>


                        <div className="core-info">

                            <span className="core-label">
                                ZARVIS INTELLIGENCE
                            </span>

                            <h2>
                                Zarvis Core
                            </h2>

                            <p>
                                Your AI brain, always working for you.
                            </p>

                            <div className="core-tags">

                                <span>
                                    ✦ Plan
                                </span>

                                <span>
                                    ✦ Think
                                </span>

                                <span>
                                    ◆ Execute
                                </span>

                                <span>
                                    ✦ Support
                                </span>

                            </div>

                        </div>


                        <button
                            type="button"
                            className="core-arrow"
                            onClick={() =>
                                navigate("/assistant")
                            }
                        >
                            →
                        </button>

                    </section>


                    {/* MAIN DASHBOARD GRID */}
                    <div className="dashboard-main-grid">

                        <TaskCard />

                        <ScheduleCard />

                        <ActivityCard />

                    </div>


                    {/* SECONDARY GRID */}
                    <div className="dashboard-secondary-grid">

                        <MemoryCard />

                        {/* TIMER */}
                        <div id="zarvis-timer">
                            <Timer />
                        </div>

                        <UpcomingTasks />

                    </div>


                    {/* AGENT NETWORK */}
                    <AgentNetwork />

                </div>

            </main>

        </div>
    );
}

export default Dashboard;