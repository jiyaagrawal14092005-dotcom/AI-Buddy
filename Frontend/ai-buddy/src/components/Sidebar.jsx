import { NavLink } from "react-router-dom";

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
                                `sidebar-nav-item ${isActive ? "active" : ""
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
                                `sidebar-nav-item ${isActive ? "active" : ""
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