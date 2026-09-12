import { NavLink } from "react-router-dom";

import {
    Home,
    CheckSquare,
    CalendarDays,
    Workflow,
    Brain,
    Settings,
    Sparkles,
    ShieldCheck,
} from "lucide-react";

const menuItems = [
    { label: "Dashboard", icon: Home, path: "/" },
    { label: "Tasks", icon: CheckSquare, path: "/tasks" },
    { label: "Schedule", icon: CalendarDays, path: "/schedule" },
    { label: "Workflows", icon: Workflow, path: "/workflows" },
    { label: "Memory", icon: Brain, path: "/memory" },
    { label: "Security", icon: ShieldCheck, path: "/security" },
    { label: "Settings", icon: Settings, path: "/settings" },
];

function Sidebar() {
    return (
        <aside className="sidebar">

            {/* LOGO */}
            <div className="sidebar-logo">
                <div className="logo-icon">
                    <Sparkles size={21} />
                </div>

                <div>
                    <h2>Zarvis</h2>
                    <span>Your AI Companion</span>
                </div>
            </div>

            {/* NAVIGATION */}
            <nav className="sidebar-nav">
                <p className="nav-title">MENU</p>

                {menuItems.map((item) => {
                    const Icon = item.icon;

                    return (
                        <NavLink
                            key={item.label}
                            to={item.path}
                            className={({ isActive }) =>
                                `nav-item ${isActive ? "active" : ""}`
                            }
                        >
                            <Icon size={18} />
                            <span>{item.label}</span>
                        </NavLink>
                    );
                })}
            </nav>

            {/* STATUS */}
            <div className="sidebar-bottom">
                <div className="buddy-status">
                    <span className="status-dot"></span>

                    <div>
                        <strong>Zarvis</strong>
                        <small>Online & Ready</small>
                    </div>
                </div>
            </div>

        </aside>
    );
}

export default Sidebar;