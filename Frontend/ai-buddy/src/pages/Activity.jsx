import { useMemo, useState } from "react";
import {
    Activity as ActivityIcon,
    CheckCircle2,
    Clock3,
    Plus,
    Trash2,
    Zap,
    CalendarDays,
    MessageCircle,
    Brain,
    Search,
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const initialActivities = [
    {
        id: 1,
        type: "completed",
        title: "AI assignment completed",
        description: "Task marked as completed successfully.",
        time: "10:30 AM",
        date: "Today",
        icon: CheckCircle2,
    },
    {
        id: 2,
        type: "workflow",
        title: "Study workflow started",
        description: "Zarvis started your study routine.",
        time: "09:45 AM",
        date: "Today",
        icon: Zap,
    },
    {
        id: 3,
        type: "schedule",
        title: "Machine Learning Class added",
        description: "New event added to your schedule.",
        time: "09:10 AM",
        date: "Today",
        icon: CalendarDays,
    },
    {
        id: 4,
        type: "assistant",
        title: "Conversation with Zarvis",
        description: "Assistant session completed.",
        time: "08:40 AM",
        date: "Today",
        icon: MessageCircle,
    },
    {
        id: 5,
        type: "memory",
        title: "Memory updated",
        description: "A new preference was saved to memory.",
        time: "Yesterday",
        date: "Yesterday",
        icon: Brain,
    },
];

function Activity() {
    const [activities, setActivities] =
        useState(initialActivities);

    const [search, setSearch] = useState("");

    const [filter, setFilter] = useState("ALL");

    const filteredActivities = useMemo(() => {
        return activities.filter((activity) => {
            const matchesSearch =
                `${activity.title} ${activity.description}`
                    .toLowerCase()
                    .includes(search.toLowerCase());

            const matchesFilter =
                filter === "ALL" ||
                activity.type.toUpperCase() === filter;

            return matchesSearch && matchesFilter;
        });
    }, [activities, search, filter]);

    const clearActivity = () => {
        setActivities([]);
    };

    const deleteActivity = (id) => {
        setActivities((current) =>
            current.filter(
                (activity) => activity.id !== id
            )
        );
    };

    const completedCount = activities.filter(
        (activity) => activity.type === "completed"
    ).length;

    const workflowCount = activities.filter(
        (activity) => activity.type === "workflow"
    ).length;

    const todayCount = activities.filter(
        (activity) => activity.date === "Today"
    ).length;

    return (
        <div className="app">

            <Sidebar />

            <main className="main-content">

                <Navbar />

                <div className="activity-page-final">

                    {/* HEADER */}

                    <section className="activity-header-final">

                        <div className="activity-header-info-final">

                            <div className="activity-eyebrow-final">
                                <ActivityIcon size={14} />
                                <span>ZARVIS ACTIVITY SYSTEM</span>
                            </div>

                            <h1>Activity</h1>

                            <p>
                                See everything Zarvis has been
                                doing for you.
                            </p>

                        </div>

                        <button
                            type="button"
                            className="activity-clear-final"
                            onClick={clearActivity}
                            disabled={activities.length === 0}
                        >
                            <Trash2 size={16} />
                            Clear Activity
                        </button>

                    </section>


                    {/* STATS */}

                    <section className="activity-stats-final">

                        <div className="activity-stat-final">

                            <span>TOTAL ACTIVITY</span>

                            <strong>
                                {activities.length}
                            </strong>

                        </div>

                        <div className="activity-stat-final">

                            <span>TODAY</span>

                            <strong>
                                {todayCount}
                            </strong>

                        </div>

                        <div className="activity-stat-final">

                            <span>COMPLETED</span>

                            <strong>
                                {completedCount}
                            </strong>

                        </div>

                        <div className="activity-stat-final">

                            <span>WORKFLOWS</span>

                            <strong>
                                {workflowCount}
                            </strong>

                        </div>

                    </section>


                    {/* TOOLBAR */}

                    <section className="activity-toolbar-final">

                        <div className="activity-search-final">

                            <Search size={17} />

                            <input
                                type="text"
                                placeholder="Search activity..."
                                value={search}
                                onChange={(e) =>
                                    setSearch(e.target.value)
                                }
                            />

                        </div>


                        <div className="activity-filters-final">

                            {[
                                "ALL",
                                "COMPLETED",
                                "WORKFLOW",
                                "SCHEDULE",
                                "ASSISTANT",
                                "MEMORY",
                            ].map((item) => (

                                <button
                                    type="button"
                                    key={item}
                                    className={
                                        filter === item
                                            ? "active"
                                            : ""
                                    }
                                    onClick={() =>
                                        setFilter(item)
                                    }
                                >
                                    {item}
                                </button>

                            ))}

                        </div>

                    </section>


                    {/* ACTIVITY PANEL */}

                    <section className="activity-panel-final">

                        <div className="activity-panel-header-final">

                            <div>

                                <span>
                                    EXECUTION LOG // 05
                                </span>

                                <h2>
                                    Recent Activity
                                </h2>

                            </div>

                            <div className="activity-live-final">

                                <span></span>

                                LIVE

                            </div>

                        </div>


                        <div className="activity-list-final">

                            {filteredActivities.length === 0 ? (

                                <div className="activity-empty-final">

                                    <ActivityIcon size={34} />

                                    <h3>
                                        No activity found
                                    </h3>

                                    <p>
                                        Your Zarvis activity will
                                        appear here.
                                    </p>

                                </div>

                            ) : (

                                filteredActivities.map(
                                    (activity, index) => {

                                        const Icon = activity.icon;

                                        return (
                                            <div
                                                className="activity-row-final"
                                                key={activity.id}
                                            >

                                                <div className="activity-time-final">

                                                    <strong>
                                                        {activity.time}
                                                    </strong>

                                                    <span>
                                                        {activity.date}
                                                    </span>

                                                </div>


                                                <div className="activity-line-final">

                                                    <div className="activity-dot-final">
                                                        <Icon size={15} />
                                                    </div>

                                                    {index !==
                                                        filteredActivities.length - 1 && (
                                                            <span></span>
                                                        )}

                                                </div>


                                                <div className="activity-content-final">

                                                    <div className="activity-title-final">

                                                        <h3>
                                                            {activity.title}
                                                        </h3>

                                                        <span
                                                            className={`activity-type-${activity.type}`}
                                                        >
                                                            {activity.type.toUpperCase()}
                                                        </span>

                                                    </div>

                                                    <p>
                                                        {activity.description}
                                                    </p>

                                                    <div className="activity-meta-final">

                                                        <span>
                                                            <Clock3 size={12} />
                                                            {activity.time}
                                                        </span>

                                                        <span>
                                                            <ActivityIcon size={12} />
                                                            Zarvis Core
                                                        </span>

                                                    </div>

                                                </div>


                                                <button
                                                    type="button"
                                                    className="activity-delete-final"
                                                    onClick={() =>
                                                        deleteActivity(
                                                            activity.id
                                                        )
                                                    }
                                                    title="Delete activity"
                                                >
                                                    <Trash2 size={15} />
                                                </button>

                                            </div>
                                        );
                                    }
                                )

                            )}

                        </div>

                    </section>


                    {/* BOTTOM STATUS */}

                    <div className="activity-status-bar-final">

                        <div>

                            <span className="activity-status-dot-final"></span>

                            <strong>
                                ZARVIS CORE
                            </strong>

                            <span>
                                Activity monitoring active
                            </span>

                        </div>

                        <span>
                            <Plus size={13} />
                            REAL-TIME LOGGING
                        </span>

                    </div>

                </div>

            </main>

        </div>
    );
}

export default Activity;