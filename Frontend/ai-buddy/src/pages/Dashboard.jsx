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

    return (
        <div className="app">

            {/* SIDEBAR */}
            <Sidebar />

            <main className="main-content">

                {/* NAVBAR */}
                <Navbar />

                <div className="dashboard">

                    {/* AI HERO / CHAT */}
                    <ChatBox />

                    {/* QUICK STATS */}
                    <section className="stats-grid">

                        <div className="stat-card glass-card">
                            <div className="stat-top">
                                <div className="stat-icon">✓</div>
                                <span>Today</span>
                            </div>

                            <div className="stat-value">12</div>

                            <div className="stat-label">
                                Tasks completed
                            </div>
                        </div>


                        <div className="stat-card glass-card">
                            <div className="stat-top">
                                <div className="stat-icon">◷</div>
                                <span>Focus</span>
                            </div>

                            <div className="stat-value">4.5h</div>

                            <div className="stat-label">
                                Focused time
                            </div>
                        </div>


                        <div className="stat-card glass-card">
                            <div className="stat-top">
                                <div className="stat-icon">⚡</div>
                                <span>Active</span>
                            </div>

                            <div className="stat-value">07</div>

                            <div className="stat-label">
                                Active tasks
                            </div>
                        </div>


                        <div className="stat-card glass-card">
                            <div className="stat-top">
                                <div className="stat-icon">✦</div>
                                <span>AI</span>
                            </div>

                            <div className="stat-value">24/7</div>

                            <div className="stat-label">
                                Zarvis availability
                            </div>
                        </div>

                    </section>


                    {/* QUICK ACTIONS */}
                    <section>

                        <div className="section-header">

                            <h2 className="section-title">
                                Quick Actions
                            </h2>

                            <span className="section-link">
                                View all
                            </span>

                        </div>


                        <div className="quick-actions">

                            {/* PLAN MY DAY */}
                            <button
                                type="button"
                                className="quick-action"
                                onClick={() =>
                                    handleQuickAction("Plan My Day")
                                }
                            >
                                <div className="quick-action-icon">
                                    ✦
                                </div>

                                <div className="quick-action-title">
                                    Plan My Day
                                </div>

                                <div className="quick-action-text">
                                    Build a smart daily plan
                                </div>
                            </button>


                            {/* CREATE TASK */}
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
                                    Create Task
                                </div>

                                <div className="quick-action-text">
                                    Add something to your list
                                </div>
                            </button>


                            {/* SCHEDULE */}
                            <button
                                type="button"
                                className="quick-action"
                                onClick={() =>
                                    navigate("/schedule?create=true")
                                }
                            >
                                <div className="quick-action-icon">
                                    ◷
                                </div>

                                <div className="quick-action-title">
                                    Schedule
                                </div>

                                <div className="quick-action-text">
                                    Organize your time
                                </div>
                            </button>


                            {/* START WORKFLOW */}
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
                                    Start Workflow
                                </div>

                                <div className="quick-action-text">
                                    Automate a routine
                                </div>
                            </button>

                        </div>


                        {/* QUICK ACTION RESPONSE */}
                        {activeAction && (
                            <div className="zarvis-response quick-action-response">

                                <span>✦</span>

                                <span>
                                    {activeAction} selected.
                                    Zarvis is ready.
                                </span>

                            </div>
                        )}

                    </section>


                    {/* DASHBOARD CARDS */}
                    <div className="dashboard-cards-grid">

                        <TaskCard />

                        <ScheduleCard />

                        <ActivityCard />

                        <MemoryCard />

                    </div>


                    {/* TIMER + UPCOMING TASKS */}
                    <div className="dashboard-cards-grid">

                        <Timer />

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