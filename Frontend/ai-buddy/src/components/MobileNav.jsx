import { NavLink } from "react-router-dom";

import {
    LayoutDashboard,
    CheckSquare,
    CalendarDays,
    Workflow,
    Brain,
} from "lucide-react";

const mobileItems = [
    {
        label: "Home",
        icon: LayoutDashboard,
        path: "/",
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
        label: "Memory",
        icon: Brain,
        path: "/memory",
    },
];

function MobileNav() {
    return (
        <nav className="mobile-nav">

            {mobileItems.map((item) => {
                const Icon = item.icon;

                return (
                    <NavLink
                        key={item.label}
                        to={item.path}
                        className={({ isActive }) =>
                            `mobile-nav-item ${isActive ? "active" : ""
                            }`
                        }
                    >
                        <Icon size={19} />

                        <span>
                            {item.label}
                        </span>
                    </NavLink>
                );
            })}

        </nav>
    );
}

export default MobileNav;