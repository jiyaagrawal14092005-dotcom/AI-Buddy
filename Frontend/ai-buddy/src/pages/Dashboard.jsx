import { useEffect, useState } from "react";
import { Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useBuddy } from "../context/BuddyContext";
import { useAuth } from "../context/AuthContext";

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

import { getTasks } from "../services/taskService";
import { getScheduledJobs } from "../services/schedulerService";


function Dashboard() {

    const navigate = useNavigate();

    const {
        buddyStatus,
        isThinking,
        dashboardRefreshKey,
    } = useBuddy();

    const {
        user,
        authenticated,
    } = useAuth();


    const [activeAction, setActiveAction] =
        useState("");


    /* =================================================
       DASHBOARD REAL DATA
    ================================================= */

    const [dashboardTasks, setDashboardTasks] =
        useState([]);

    const [dashboardSchedule, setDashboardSchedule] =
        useState([]);

    const [dashboardLoading, setDashboardLoading] =
        useState(true);


    /* =================================================
       LOAD DASHBOARD DATA
    ================================================= */

    useEffect(() => {

        const loadDashboardData = async () => {

            if (
                !authenticated ||
                !user?.id
            ) {

                setDashboardTasks([]);
                setDashboardSchedule([]);
                setDashboardLoading(false);

                return;
            }


            try {

                setDashboardLoading(true);


                const [
                    tasksResult,
                    scheduleResult,
                ] = await Promise.all([

                    getTasks(user.id),

                    getScheduledJobs(user.id),

                ]);


                const tasks =
                    Array.isArray(tasksResult)
                        ? tasksResult
                        : Array.isArray(tasksResult?.tasks)
                            ? tasksResult.tasks
                            : [];


                const jobs =
                    Array.isArray(scheduleResult?.jobs)
                        ? scheduleResult.jobs
                        : [];


                setDashboardTasks(tasks);


                const activeJobs =
                    jobs
                        .filter(
                            (job) =>
                                job.status === "scheduled" ||
                                job.status === "SCHEDULED"
                        )
                        .sort(
                            (a, b) =>
                                new Date(a.schedule) -
                                new Date(b.schedule)
                        );


                setDashboardSchedule(
                    activeJobs
                );


            } catch (error) {

                console.error(
                    "Failed to load dashboard data:",
                    error
                );

                setDashboardTasks([]);
                setDashboardSchedule([]);

            } finally {

                setDashboardLoading(false);

            }

        };


        loadDashboardData();

    }, [
        authenticated,
        user?.id,
        dashboardRefreshKey,
    ]);


    /* =================================================
       DASHBOARD STATISTICS
    ================================================= */

    const totalTasks =
        dashboardTasks.length;


    const completedTasks =
        dashboardTasks.filter(
            (task) =>
                String(task.status || "").toLowerCase() ===
                "completed"
        ).length;


    const scheduledCount =
        dashboardSchedule.length;


    const getNextScheduleTime = () => {

        if (
            dashboardSchedule.length === 0
        ) {

            return "No upcoming events";

        }


        const nextJob =
            dashboardSchedule[0];


        if (!nextJob?.schedule) {

            return "Time not specified";

        }


        const date =
            new Date(nextJob.schedule);


        if (
            Number.isNaN(
                date.getTime()
            )
        ) {

            return "Time not specified";

        }


        return date.toLocaleTimeString(
            "en-IN",
            {
                hour: "2-digit",
                minute: "2-digit",
            }
        );

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


    /* =================================================
       GREETING
    ================================================= */

    const getGreeting = () => {

        const hour =
            new Date().getHours();


        if (hour >= 5 && hour < 12) {
            return "GOOD MORNING";
        }


        if (hour >= 12 && hour < 17) {
            return "GOOD AFTERNOON";
        }


        if (hour >= 17 && hour < 21) {
            return "GOOD EVENING";
        }


        return "GOOD NIGHT";

    };


    return (

        <div className="app">

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

                                {getGreeting()}

                            </div>


                            <h1>

                                Hello,{" "}

                                <span>
                                    {user?.username || user?.name || "User"}
                                </span>

                            </h1>


                            <p>

                                Your AI buddy is here to make your day

                                <br />

                                smarter, simpler and more productive.

                            </p>


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


                        <ChatBox />

                    </section>


                    {/* =================================================
                        REAL STATS
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

                                {dashboardLoading
                                    ? "--"
                                    : String(totalTasks).padStart(
                                        2,
                                        "0"
                                    )}

                            </strong>

                            <span className="stat-description">

                                {dashboardLoading
                                    ? "Loading tasks..."
                                    : `${completedTasks} completed`}

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
                                Workflow engine ready
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

                                {dashboardLoading
                                    ? "--"
                                    : String(scheduledCount).padStart(
                                        2,
                                        "0"
                                    )}

                            </strong>

                            <span className="stat-description">

                                {dashboardLoading
                                    ? "Loading schedule..."
                                    : scheduledCount > 0
                                        ? `Next at ${getNextScheduleTime()}`
                                        : "No upcoming events"}

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


                            <button
                                type="button"
                                className={`quick-action-card ${
                                    activeAction === "task"
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


                            <button
                                type="button"
                                className={`quick-action-card ${
                                    activeAction === "schedule"
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


                            <button
                                type="button"
                                className={`quick-action-card ${
                                    activeAction === "workflow"
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


                            <button
                                type="button"
                                className={`quick-action-card ${
                                    activeAction === "memory"
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


                            <button
                                type="button"
                                className={`quick-action-card ${
                                    activeAction === "focus"
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