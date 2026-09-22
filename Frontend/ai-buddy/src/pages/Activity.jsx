import { useMemo, useState } from "react";
import {
    Activity as ActivityIcon,
    CheckCircle2,
    Clock3,
    Trash2,
    Bot,
    Zap,
    CalendarDays,
    Brain,
    Download,
    Bell,
    Info,
    XCircle,
} from "lucide-react";

import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";
import { useBuddy } from "../context/BuddyContext";


const initialActivities = [
    {
        id: 1,
        time: "09:42 AM",
        date: "Today",
        title: "Task completed",
        description: "Complete Python assignment",
        type: "COMPLETED",
        icon: CheckCircle2,
    },
    {
        id: 2,
        time: "08:15 AM",
        date: "Today",
        title: "Workflow executed",
        description: "Morning productivity workflow",
        type: "WORKFLOW",
        icon: Zap,
    },
    {
        id: 3,
        time: "07:30 PM",
        date: "Yesterday",
        title: "Schedule created",
        description: "Study session reminder added",
        type: "SCHEDULE",
        icon: CalendarDays,
    },
    {
        id: 4,
        time: "05:20 PM",
        date: "Yesterday",
        title: "Assistant action",
        description: "Zarvis processed your command",
        type: "ASSISTANT",
        icon: Bot,
    },
    {
        id: 5,
        time: "03:10 PM",
        date: "Yesterday",
        title: "Memory updated",
        description: "New preference saved to memory",
        type: "MEMORY",
        icon: Brain,
    },
    {
        id: 6,
        time: "11:45 AM",
        date: "Yesterday",
        title: "Task completed",
        description: "Review machine learning notes",
        type: "COMPLETED",
        icon: CheckCircle2,
    },
];


function Activity() {

    // ==========================================
    // GLOBAL NOTIFICATIONS
    // ==========================================

    const {
        notifications,
    } = useBuddy();


    // ==========================================
    // LOCAL ACTIVITY STATE
    // ==========================================

    const [activities, setActivities] =
        useState(initialActivities);

    const [search, setSearch] = useState("");

    const [filter, setFilter] = useState("ALL");


    // ==========================================
    // NOTIFICATION ICON
    // ==========================================

    const getNotificationIcon = (
        notification
    ) => {

        const iconType =
            notification?.icon ||
            notification?.type ||
            "info";


        if (
            iconType === "download"
        ) {
            return Download;
        }


        if (
            iconType === "success" ||
            notification?.type === "success"
        ) {
            return CheckCircle2;
        }


        if (
            iconType === "error" ||
            notification?.type === "error" ||
            notification?.type === "failed"
        ) {
            return XCircle;
        }


        if (
            iconType === "workflow" ||
            notification?.type === "workflow"
        ) {
            return Zap;
        }


        if (
            iconType === "reminder" ||
            notification?.type === "reminder"
        ) {
            return CalendarDays;
        }


        return Info;
    };


    // ==========================================
    // NOTIFICATION TYPE
    // ==========================================

    const getNotificationType = (
        notification
    ) => {

        const type =
            notification?.type ||
            notification?.icon ||
            "info";


        if (
            type === "download" ||
            type === "success"
        ) {
            return "COMPLETED";
        }


        if (
            type === "workflow"
        ) {
            return "WORKFLOW";
        }


        if (
            type === "reminder"
        ) {
            return "SCHEDULE";
        }


        if (
            type === "error" ||
            type === "failed"
        ) {
            return "ASSISTANT";
        }


        return "ASSISTANT";
    };


    // ==========================================
    // FORMAT NOTIFICATION TIME
    // ==========================================

    const formatNotificationTime = (
        createdAt
    ) => {

        if (!createdAt) {
            return {
                time: "NOW",
                date: "Today",
            };
        }


        const date =
            new Date(createdAt);


        if (
            Number.isNaN(
                date.getTime()
            )
        ) {
            return {
                time: "NOW",
                date: "Today",
            };
        }


        const now =
            new Date();


        const isToday =
            date.toDateString() ===
            now.toDateString();


        const yesterday =
            new Date();

        yesterday.setDate(
            yesterday.getDate() - 1
        );


        const isYesterday =
            date.toDateString() ===
            yesterday.toDateString();


        const time =
            date.toLocaleTimeString(
                [],
                {
                    hour: "2-digit",
                    minute: "2-digit",
                }
            );


        let dateLabel = "Earlier";


        if (isToday) {
            dateLabel = "Today";
        } else if (isYesterday) {
            dateLabel = "Yesterday";
        } else {
            dateLabel =
                date.toLocaleDateString(
                    [],
                    {
                        day: "2-digit",
                        month: "short",
                        year: "numeric",
                    }
                );
        }


        return {
            time,
            date: dateLabel,
        };
    };


    // ==========================================
    // CONVERT GLOBAL NOTIFICATIONS
    // TO ACTIVITY RECORDS
    // ==========================================

    const notificationActivities =
        useMemo(() => {

            return notifications.map(
                (notification) => {

                    const {
                        time,
                        date,
                    } =
                        formatNotificationTime(
                            notification.createdAt
                        );


                    return {
                        id:
                            `notification-${notification.id}`,

                        time,

                        date,

                        title:
                            notification.title ||
                            "Zarvis Update",

                        description:
                            notification.message ||
                            "",

                        type:
                            getNotificationType(
                                notification
                            ),

                        icon:
                            getNotificationIcon(
                                notification
                            ),

                        isNotification: true,

                        notificationId:
                            notification.id,

                        read:
                            notification.read,
                    };
                }
            );

        }, [notifications]);


    // ==========================================
    // COMBINE ACTIVITY + NOTIFICATIONS
    // ==========================================

    const allActivities = useMemo(
        () => {

            return [
                ...notificationActivities,
                ...activities,
            ];

        },
        [
            notificationActivities,
            activities,
        ]
    );


    // ==========================================
    // FILTER ACTIVITIES
    // ==========================================

    const filteredActivities =
        allActivities.filter(
            (activity) => {

                const searchText =
                    `${activity.title} ${activity.description} ${activity.type}`
                        .toLowerCase();


                const matchesSearch =
                    searchText.includes(
                        search.toLowerCase()
                    );


                const matchesFilter =
                    filter === "ALL" ||
                    activity.type === filter;


                return (
                    matchesSearch &&
                    matchesFilter
                );
            }
        );


    // ==========================================
    // STATS
    // ==========================================

    const completedCount =
        allActivities.filter(
            (item) =>
                item.type === "COMPLETED"
        ).length;


    const workflowCount =
        allActivities.filter(
            (item) =>
                item.type === "WORKFLOW"
        ).length;


    const assistantCount =
        allActivities.filter(
            (item) =>
                item.type === "ASSISTANT"
        ).length;


    // ==========================================
    // DELETE LOCAL ACTIVITY
    // ==========================================

    const clearActivity = (id) => {

        setActivities((current) =>
            current.filter(
                (activity) =>
                    activity.id !== id
            )
        );
    };


    // ==========================================
    // CLEAR LOCAL ACTIVITY
    //
    // Global notifications are intentionally
    // NOT deleted here.
    // ==========================================

    const clearAllActivities = () => {
        setActivities([]);
    };


    return (

        <div className="app">

            <Sidebar />

            <main className="main-content">

                <Navbar />


                <div className="activity-page-final">


                    {/* ================= HEADER ================= */}

                    <div className="activity-header-final">

                        <div className="activity-header-info-final">

                            <div className="activity-eyebrow-final">

                                <ActivityIcon
                                    size={14}
                                />

                                <span>
                                    ZARVIS ACTIVITY SYSTEM
                                </span>

                            </div>


                            <h1>
                                Activity
                            </h1>


                            <p>
                                Track everything Zarvis has
                                done across your workspace.
                            </p>

                        </div>


                        <button
                            type="button"
                            className="activity-clear-final"
                            onClick={
                                clearAllActivities
                            }
                            disabled={
                                activities.length === 0
                            }
                        >

                            <Trash2 size={15} />

                            Clear Activity

                        </button>

                    </div>


                    {/* ================= STATS ================= */}

                    <div className="activity-stats-final">

                        <div className="activity-stat-final">

                            <span>
                                TOTAL ACTIVITY
                            </span>

                            <strong>
                                {allActivities.length}
                            </strong>

                        </div>


                        <div className="activity-stat-final">

                            <span>
                                COMPLETED
                            </span>

                            <strong>
                                {completedCount}
                            </strong>

                        </div>


                        <div className="activity-stat-final">

                            <span>
                                WORKFLOWS
                            </span>

                            <strong>
                                {workflowCount}
                            </strong>

                        </div>


                        <div className="activity-stat-final">

                            <span>
                                ASSISTANT ACTIONS
                            </span>

                            <strong>
                                {assistantCount}
                            </strong>

                        </div>

                    </div>


                    {/* ================= TOOLBAR ================= */}

                    <div className="activity-toolbar-final">

                        <div className="activity-search-final">

                            <ActivityIcon
                                size={17}
                            />

                            <input
                                type="text"
                                placeholder="Search activity..."
                                value={search}
                                onChange={(e) =>
                                    setSearch(
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="activity-filters-final">

                            <button
                                type="button"
                                className={
                                    filter === "ALL"
                                        ? "active"
                                        : ""
                                }
                                onClick={() =>
                                    setFilter("ALL")
                                }
                            >
                                ALL
                            </button>


                            <button
                                type="button"
                                className={
                                    filter === "COMPLETED"
                                        ? "active"
                                        : ""
                                }
                                onClick={() =>
                                    setFilter(
                                        "COMPLETED"
                                    )
                                }
                            >
                                COMPLETED
                            </button>


                            <button
                                type="button"
                                className={
                                    filter === "WORKFLOW"
                                        ? "active"
                                        : ""
                                }
                                onClick={() =>
                                    setFilter(
                                        "WORKFLOW"
                                    )
                                }
                            >
                                WORKFLOW
                            </button>


                            <button
                                type="button"
                                className={
                                    filter === "SCHEDULE"
                                        ? "active"
                                        : ""
                                }
                                onClick={() =>
                                    setFilter(
                                        "SCHEDULE"
                                    )
                                }
                            >
                                SCHEDULE
                            </button>


                            <button
                                type="button"
                                className={
                                    filter === "ASSISTANT"
                                        ? "active"
                                        : ""
                                }
                                onClick={() =>
                                    setFilter(
                                        "ASSISTANT"
                                    )
                                }
                            >
                                ASSISTANT
                            </button>


                            <button
                                type="button"
                                className={
                                    filter === "MEMORY"
                                        ? "active"
                                        : ""
                                }
                                onClick={() =>
                                    setFilter(
                                        "MEMORY"
                                    )
                                }
                            >
                                MEMORY
                            </button>

                        </div>

                    </div>


                    {/* ================= ACTIVITY PANEL ================= */}

                    <section className="activity-panel-final">

                        <div className="activity-panel-header-final">

                            <div>

                                <span>
                                    SYSTEM LOG //{" "}
                                    {String(
                                        filteredActivities.length
                                    ).padStart(
                                        2,
                                        "0"
                                    )}
                                </span>


                                <h2>
                                    Recent Activity
                                </h2>

                            </div>


                            <div className="activity-live-final">

                                <span></span>

                                LIVE MONITORING

                            </div>

                        </div>


                        {/* ================= LIST ================= */}

                        <div className="activity-list-final">

                            {filteredActivities.length === 0 ? (

                                <div className="activity-empty-final">

                                    <ActivityIcon
                                        size={34}
                                    />

                                    <h3>
                                        No activity found
                                    </h3>

                                    <p>
                                        Try another search or
                                        clear the current filter.
                                    </p>

                                </div>

                            ) : (

                                filteredActivities.map(
                                    (activity) => {

                                        const Icon =
                                            activity.icon;


                                        const typeClass =
                                            activity.type ===
                                                "COMPLETED"
                                                ? "activity-type-completed"
                                                : activity.type ===
                                                    "WORKFLOW"
                                                    ? "activity-type-workflow"
                                                    : activity.type ===
                                                        "SCHEDULE"
                                                        ? "activity-type-schedule"
                                                        : activity.type ===
                                                            "ASSISTANT"
                                                            ? "activity-type-assistant"
                                                            : "activity-type-memory";


                                        return (

                                            <div
                                                className={`activity-row-final ${
                                                    activity.isNotification &&
                                                    !activity.read
                                                        ? "activity-notification-unread"
                                                        : ""
                                                }`}
                                                key={
                                                    activity.id
                                                }
                                            >


                                                {/* TIME */}

                                                <div className="activity-time-final">

                                                    <strong>
                                                        {
                                                            activity.time
                                                        }
                                                    </strong>

                                                    <span>
                                                        {
                                                            activity.date
                                                        }
                                                    </span>

                                                </div>


                                                {/* TIMELINE */}

                                                <div className="activity-line-final">

                                                    <div className="activity-dot-final">

                                                        <Icon
                                                            size={15}
                                                        />

                                                    </div>

                                                    <span></span>

                                                </div>


                                                {/* CONTENT */}

                                                <div className="activity-content-final">

                                                    <div className="activity-title-final">

                                                        <h3>
                                                            {
                                                                activity.title
                                                            }
                                                        </h3>


                                                        <span
                                                            className={
                                                                typeClass
                                                            }
                                                        >
                                                            {
                                                                activity.type
                                                            }
                                                        </span>

                                                    </div>


                                                    <p>
                                                        {
                                                            activity.description
                                                        }
                                                    </p>


                                                    <div className="activity-meta-final">

                                                        <span>

                                                            <Clock3
                                                                size={12}
                                                            />

                                                            {
                                                                activity.time
                                                            }

                                                        </span>


                                                        <span>

                                                            <Bot
                                                                size={12}
                                                            />

                                                            Zarvis Core

                                                        </span>


                                                        {activity.isNotification && (

                                                            <span>

                                                                <Bell
                                                                    size={12}
                                                                />

                                                                Notification

                                                            </span>

                                                        )}

                                                    </div>

                                                </div>


                                                {/* DELETE */}

                                                {!activity.isNotification && (

                                                    <button
                                                        type="button"
                                                        className="activity-delete-final"
                                                        title="Remove activity"
                                                        onClick={() =>
                                                            clearActivity(
                                                                activity.id
                                                            )
                                                        }
                                                    >

                                                        <Trash2
                                                            size={15}
                                                        />

                                                    </button>

                                                )}

                                            </div>
                                        );
                                    }
                                )

                            )}

                        </div>

                    </section>


                    {/* ================= STATUS BAR ================= */}

                    <div className="activity-status-bar-final">

                        <div>

                            <span className="activity-status-dot-final"></span>

                            <strong>
                                ACTIVITY MONITOR
                            </strong>

                            <span>
                                Tracking workspace events
                            </span>

                        </div>


                        <span>

                            <Bot size={12} />

                            ZARVIS CORE ONLINE

                        </span>

                    </div>

                </div>

            </main>

        </div>
    );
}


export default Activity;