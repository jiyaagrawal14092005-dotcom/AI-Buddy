import {
    Clock3,
    CheckCircle2,
    Circle,
    ArrowUpRight,
} from "lucide-react";

const tasks = [
    {
        time: "10:30",
        period: "AM",
        title: "Complete React Module",
        category: "LEARNING",
        priority: "HIGH",
        done: true,
    },
    {
        time: "12:00",
        period: "PM",
        title: "Lunch Break",
        category: "PERSONAL",
        priority: "NORMAL",
        done: false,
    },
    {
        time: "02:30",
        period: "PM",
        title: "Work on Zarvis UI",
        category: "PROJECT",
        priority: "HIGH",
        done: false,
    },
    {
        time: "05:00",
        period: "PM",
        title: "Review Today's Progress",
        category: "PRODUCTIVITY",
        priority: "NORMAL",
        done: false,
    },
];

function UpcomingTasks() {
    return (
        <section className="upcoming-system">

            {/* HEADER */}
            <div className="upcoming-header">

                <div className="upcoming-heading">
                    <div className="upcoming-icon">
                        <Clock3 size={17} />
                    </div>

                    <div>
                        <span>SCHEDULE MODULE // 05</span>
                        <h3>UPCOMING TASKS</h3>
                    </div>
                </div>

                <button className="view-schedule">
                    VIEW ALL
                    <ArrowUpRight size={13} />
                </button>

            </div>

            {/* STATUS BAR */}
            <div className="upcoming-status">
                <span>
                    <i></i>
                    TODAY
                </span>

                <span>04 TASKS</span>

                <span>SYNCED</span>
            </div>

            {/* TASK LIST */}
            <div className="upcoming-list">

                {tasks.map((task, index) => (
                    <div
                        className={`upcoming-task ${task.done ? "task-completed" : ""
                            }`}
                        key={index}
                    >

                        {/* TIME */}
                        <div className="task-time">
                            <strong>{task.time}</strong>
                            <span>{task.period}</span>
                        </div>

                        {/* CONNECTOR */}
                        <div className="task-track">

                            <div className="task-dot">
                                {task.done ? (
                                    <CheckCircle2 size={15} />
                                ) : (
                                    <Circle size={14} />
                                )}
                            </div>

                            {index !== tasks.length - 1 && (
                                <div className="task-connector"></div>
                            )}

                        </div>

                        {/* DETAILS */}
                        <div className="task-details">

                            <div className="task-title-row">
                                <h4>{task.title}</h4>

                                <span
                                    className={`priority priority-${task.priority.toLowerCase()}`}
                                >
                                    {task.priority}
                                </span>
                            </div>

                            <span className="task-category">
                                {task.category}
                            </span>

                        </div>

                    </div>
                ))}

            </div>

            {/* FOOTER */}
            <div className="upcoming-footer">
                <span>
                    <span className="footer-pulse"></span>
                    ZARVIS MONITORING SCHEDULE
                </span>

                <span>REAL-TIME</span>
            </div>

        </section>
    );
}

export default UpcomingTasks;