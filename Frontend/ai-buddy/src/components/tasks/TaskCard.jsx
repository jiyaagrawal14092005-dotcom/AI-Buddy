import { useNavigate } from "react-router-dom";

import {
    CheckSquare,
    CheckCircle2,
    Circle,
    ArrowUpRight,
} from "lucide-react";

const tasks = [
    {
        title: "Complete React Module",
        category: "LEARNING",
        priority: "HIGH",
        done: true,
    },
    {
        title: "Review project documentation",
        category: "PROJECT",
        priority: "NORMAL",
        done: false,
    },
    {
        title: "Prepare tomorrow's schedule",
        category: "PRODUCTIVITY",
        priority: "NORMAL",
        done: false,
    },
];

function TaskCard() {
    const navigate = useNavigate();

    return (
        <section className="task-system">

            {/* HEADER */}
            <div className="task-header">

                <div className="task-heading">
                    <div className="task-icon">
                        <CheckSquare size={17} />
                    </div>

                    <div>
                        <span>TASK MODULE // 01</span>
                        <h3>TASKS</h3>
                    </div>
                </div>

                <button
                    type="button"
                    className="task-view-all"
                    onClick={() => navigate("/tasks")}
                >
                    VIEW ALL
                    <ArrowUpRight size={13} />
                </button>

            </div>

            {/* STATUS */}
            <div className="task-status">
                <span>
                    <i></i>
                    TODAY
                </span>

                <span>03 TASKS</span>

                <strong>33% COMPLETE</strong>
            </div>

            {/* TASK LIST */}
            <div className="task-list">

                {tasks.map((task, index) => (
                    <div
                        className={`task-row ${
                            task.done ? "task-row-done" : ""
                        }`}
                        key={index}
                    >

                        <div className="task-check">
                            {task.done ? (
                                <CheckCircle2 size={16} />
                            ) : (
                                <Circle size={16} />
                            )}
                        </div>

                        <div className="task-info">

                            <div className="task-name-row">
                                <h4>{task.title}</h4>

                                <span
                                    className={`task-priority task-priority-${task.priority.toLowerCase()}`}
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
            <div className="task-footer">

                <span>
                    <i></i>
                    ZARVIS TASK ENGINE
                </span>

                <span>01 ACTIVE</span>

            </div>

        </section>
    );
}

export default TaskCard;