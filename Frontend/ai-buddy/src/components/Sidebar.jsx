import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";

import {
    LayoutDashboard,
    MessageCircle,
    CheckSquare,
    CalendarDays,
    Workflow,
    Activity,
    Brain,
    Plug,
    ShieldCheck,
    Settings,
    Sparkles,
    ChevronRight,
    Bell,
    User,
    CheckCircle2,
    Clock3,
    Zap,
    X,
} from "lucide-react";

const menuItems = [
    {
        label: "Dashboard",
        icon: LayoutDashboard,
        path: "/",
    },
    {
        label: "Assistant",
        icon: MessageCircle,
        path: "/assistant",
    },
    {
        label: "Tasks",
        icon: CheckSquare,
        path: "/tasks",
    },
    {
        label: "Schedule",
        icon: CalendarDays,
        path: "/schedule",
    },
    {
        label: "Workflows",
        icon: Workflow,
        path: "/workflows",
    },
    {
        label: "Activity",
        icon: Activity,
        path: "/activity",
    },
    {
        label: "Memory",
        icon: Brain,
        path: "/memory",
    },
    {
        label: "Integrations",
        icon: Plug,
        path: "/integrations",
    },
    {
        label: "Security",
        icon: ShieldCheck,
        path: "/security",
    },
    {
        label: "Settings",
        icon: Settings,
        path: "/settings",
    },
];

function Sidebar() {
    const navigate = useNavigate();

    const [showNotifications, setShowNotifications] =
        useState(false);

    return (
        <aside className="sidebar">

            {/* BRAND */}
            <div className="sidebar-brand">

                <div className="sidebar-logo-mark">
                    <Sparkles size={19} />
                </div>

                <div className="sidebar-brand-text">
                    <h2>ZARVIS</h2>
                    <span>AI COMPANION</span>
                </div>

            </div>


            {/* SYSTEM STATUS */}
            <div className="sidebar-system">

                <div className="system-indicator">

                    <span className="system-dot"></span>

                    <div>
                        <strong>SYSTEM ONLINE</strong>
                        <small>Zarvis Core Active</small>
                    </div>

                </div>

                <div className="system-line">
                    <span></span>
                </div>

            </div>


            {/* NAVIGATION */}
            <nav className="sidebar-nav">

                {/* WORKSPACE */}
                <div className="sidebar-section-label">

                    <span>WORKSPACE</span>

                    <span className="sidebar-section-line"></span>

                </div>


                {menuItems.slice(0, 8).map((item) => {

                    const Icon = item.icon;

                    return (
                        <NavLink
                            key={item.label}
                            to={item.path}
                            className={({ isActive }) =>
                                `sidebar-nav-item ${
                                    isActive ? "active" : ""
                                }`
                            }
                        >

                            <span className="sidebar-nav-icon">
                                <Icon size={17} />
                            </span>

                            <span className="sidebar-nav-label">
                                {item.label}
                            </span>

                            <ChevronRight
                                size={14}
                                className="sidebar-nav-arrow"
                            />

                        </NavLink>
                    );

                })}


                {/* SYSTEM */}
                <div className="sidebar-section-label sidebar-section-security">

                    <span>SYSTEM</span>

                    <span className="sidebar-section-line"></span>

                </div>


                {menuItems.slice(8).map((item) => {

                    const Icon = item.icon;

                    return (
                        <NavLink
                            key={item.label}
                            to={item.path}
                            className={({ isActive }) =>
                                `sidebar-nav-item ${
                                    isActive ? "active" : ""
                                }`
                            }
                        >

                            <span className="sidebar-nav-icon">
                                <Icon size={17} />
                            </span>

                            <span className="sidebar-nav-label">
                                {item.label}
                            </span>

                            <ChevronRight
                                size={14}
                                className="sidebar-nav-arrow"
                            />

                        </NavLink>
                    );

                })}

            </nav>


            {/* =================================================
                NOTIFICATION + USER ACCOUNT
            ================================================= */}

            <div className="sidebar-account-area">

                {/* NOTIFICATIONS */}

                <div className="sidebar-notification-wrapper">

                    <button
                        type="button"
                        className={`sidebar-bottom-action ${
                            showNotifications
                                ? "notification-open"
                                : ""
                        }`}
                        onClick={() =>
                            setShowNotifications(
                                !showNotifications
                            )
                        }
                        aria-label="Open notifications"
                        aria-expanded={showNotifications}
                    >

                        <span className="sidebar-bottom-action-icon">

                            <Bell size={17} />

                            <span className="notification-dot"></span>

                        </span>

                        <span className="sidebar-bottom-action-text">

                            <strong>
                                Notifications
                            </strong>

                            <small>
                                3 new alerts
                            </small>

                        </span>

                        <ChevronRight
                            size={14}
                            className={`sidebar-notification-arrow ${
                                showNotifications
                                    ? "open"
                                    : ""
                            }`}
                        />

                    </button>


                    {/* NOTIFICATION PANEL */}

                    {showNotifications && (

                        <div className="sidebar-notification-panel">

                            <div className="notification-panel-header">

                                <div>

                                    <span>
                                        ALERT CENTER
                                    </span>

                                    <strong>
                                        Notifications
                                    </strong>

                                </div>

                                <button
                                    type="button"
                                    className="notification-close"
                                    onClick={() =>
                                        setShowNotifications(false)
                                    }
                                    aria-label="Close notifications"
                                >
                                    <X size={14} />
                                </button>

                            </div>


                            {/* Notification 1 */}

                            <div className="sidebar-notification-item">

                                <div className="sidebar-notification-icon">

                                    <CheckCircle2 size={14} />

                                </div>

                                <div className="sidebar-notification-content">

                                    <strong>
                                        Task completed
                                    </strong>

                                    <span>
                                        Your morning task was completed.
                                    </span>

                                    <small>
                                        Just now
                                    </small>

                                </div>

                            </div>


                            {/* Notification 2 */}

                            <div className="sidebar-notification-item">

                                <div className="sidebar-notification-icon schedule">

                                    <Clock3 size={14} />

                                </div>

                                <div className="sidebar-notification-content">

                                    <strong>
                                        Upcoming schedule
                                    </strong>

                                    <span>
                                        You have an event at 10:00 AM.
                                    </span>

                                    <small>
                                        12 min ago
                                    </small>

                                </div>

                            </div>


                            {/* Notification 3 */}

                            <div className="sidebar-notification-item">

                                <div className="sidebar-notification-icon workflow">

                                    <Zap size={14} />

                                </div>

                                <div className="sidebar-notification-content">

                                    <strong>
                                        Workflow active
                                    </strong>

                                    <span>
                                        Your daily workflow is running.
                                    </span>

                                    <small>
                                        28 min ago
                                    </small>

                                </div>

                            </div>


                            {/* View all */}

                            <button
                                type="button"
                                className="notification-view-all"
                                onClick={() => {
                                    setShowNotifications(false);
                                    navigate("/activity");
                                }}
                            >

                                View all activity

                                <ChevronRight size={13} />

                            </button>

                        </div>

                    )}

                </div>


                {/* USER ACCOUNT */}

                <button
                    type="button"
                    className="sidebar-user-account"
                    onClick={() =>
                        navigate("/settings")
                    }
                    aria-label="Open user account settings"
                >

                    <div className="sidebar-user-avatar">

                        <User size={17} />

                    </div>


                    <div className="sidebar-user-info">

                        <strong>
                            Shanu
                        </strong>

                        <span>
                            Personal Account
                        </span>

                    </div>


                    <ChevronRight
                        size={15}
                        className="sidebar-user-arrow"
                    />

                </button>

            </div>


            {/* BOTTOM CORE */}

            <div className="sidebar-bottom">

                <div className="sidebar-core-card">

                    <div className="core-status-icon">
                        <span></span>
                    </div>

                    <div className="core-status-text">

                        <strong>
                            ZARVIS CORE
                        </strong>

                        <span>
                            Ready to assist
                        </span>

                    </div>

                    <div className="core-status-bars">

                        <i></i>
                        <i></i>
                        <i></i>

                    </div>

                </div>


                <div className="sidebar-version">

                    <span>
                        V1.0
                    </span>

                    <span>
                        AI BUDDY SYSTEM
                    </span>

                </div>

            </div>

        </aside>
    );
}

export default Sidebar;