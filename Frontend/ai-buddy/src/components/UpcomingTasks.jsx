import {
    ListTodo,
    Clock3,
    ArrowUpRight,
} from "lucide-react";

const upcomingTasks = [
    {
        title: "Complete project documentation",
        date: "Today",
        time: "07:00 PM",
        priority: "HIGH",
    },
    {
        title: "Prepare tomorrow's schedule",
        date: "Today",
        time: "08:30 PM",
        priority: "MEDIUM",
    },
    {
        title: "Machine Learning revision",
        date: "Tomorrow",
        time: "10:00 AM",
        priority: "LOW",
    },
    {
        title: "Work on Zarvis backend",
        date: "Tomorrow",
        time: "04:00 PM",
        priority: "HIGH",
    },
];

function UpcomingTasks() {
    return (
        <section className="dashboard-module upcoming-module">

            <div className="module-header">

                <div className="module-title">

                    <div className="module-icon module-icon-cyan">
                        <ListTodo size={16} />
                    </div>

                    <div>
                        <span className="module-label">
                            TASK QUEUE // 07
                        </span>

                        <h3>Upcoming Tasks</h3>
                    </div>

                </div>

                <button
                    type="button"
                    className="module-action"
                >
                    <ArrowUpRight size={15} />
                </button>

            </div>

            <div className="module-line">
                <span></span>
            </div>

            <div className="upcoming-list">

                {upcomingTasks.map((task, index) => (
                    <div
                        className="upcoming-row"
                        key={index}
                    >

                        <div className="upcoming-index">
                            {String(index + 1).padStart(2, "0")}
                        </div>

                        <div className="upcoming-content">

                            <strong>
                                {task.title}
                            </strong>

                            <div className="upcoming-meta">

                                <span>
                                    <Clock3 size={10} />
                                    {task.date}
                                </span>

                                <span>
                                    {task.time}
                                </span>

                            </div>

                        </div>

                        <span
                            className={`upcoming-priority upcoming-${task.priority.toLowerCase()}`}
                        >
                            {task.priority}
                        </span>

                    </div>
                ))}

            </div>

            <button
                type="button"
                className="module-footer-button"
            >
                <span>OPEN TASK QUEUE</span>
                <ArrowUpRight size={14} />
            </button>

        </section>
    );
}

export default UpcomingTasks;