import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
    CheckCircle2,
    Clock3,
    Plus,
    Circle,
    MoreHorizontal,
} from "lucide-react";

function Tasks() {
    const [searchParams, setSearchParams] = useSearchParams();

    const [tasks, setTasks] = useState([
        {
            id: 1,
            title: "Complete project documentation",
            time: "Today · 5:00 PM",
            priority: "High",
            completed: false,
        },
        {
            id: 2,
            title: "Prepare presentation",
            time: "Tomorrow",
            priority: "Medium",
            completed: false,
        },
        {
            id: 3,
            title: "Review study notes",
            time: "Friday",
            priority: "Low",
            completed: false,
        },
    ]);

    const [showForm, setShowForm] = useState(
        searchParams.get("create") === "true"
    );

    const [newTask, setNewTask] = useState("");

    // Open create form when Dashboard sends ?create=true
    useEffect(() => {
        if (searchParams.get("create") === "true") {
            setShowForm(true);

            // Remove ?create=true from URL
            setSearchParams({}, { replace: true });
        }
    }, [searchParams, setSearchParams]);

    const toggleTask = (id) => {
        setTasks((currentTasks) =>
            currentTasks.map((task) =>
                task.id === id
                    ? {
                        ...task,
                        completed: !task.completed,
                    }
                    : task
            )
        );
    };

    const addTask = () => {
        const text = newTask.trim();

        if (!text) return;

        const newTaskItem = {
            id: Date.now(),
            title: text,
            time: "No deadline",
            priority: "Medium",
            completed: false,
        };

        setTasks((currentTasks) => [
            ...currentTasks,
            newTaskItem,
        ]);

        setNewTask("");
        setShowForm(false);
    };

    const closeForm = () => {
        setShowForm(false);
        setNewTask("");
    };

    const completedCount = tasks.filter(
        (task) => task.completed
    ).length;

    return (
        <div className="page-container">

            {/* HEADER */}
            <div className="page-header">

                <div>
                    <span className="page-eyebrow">
                        ZARVIS TASK MANAGER
                    </span>

                    <h1>Tasks</h1>

                    <p>
                        Manage everything you need to get done.
                    </p>
                </div>

                <button
                    type="button"
                    className="primary-action"
                    onClick={() => setShowForm(true)}
                >
                    <Plus size={18} />
                    Create Task
                </button>

            </div>

            {/* STATS */}
            <div className="task-stats">

                <div className="glass-card page-stat">
                    <span>Total Tasks</span>
                    <strong>{tasks.length}</strong>
                </div>

                <div className="glass-card page-stat">
                    <span>Completed</span>
                    <strong>{completedCount}</strong>
                </div>

                <div className="glass-card page-stat">
                    <span>Remaining</span>
                    <strong>
                        {tasks.length - completedCount}
                    </strong>
                </div>

            </div>

            {/* CREATE TASK FORM */}
            {showForm && (
                <div className="task-form glass-card">

                    <div className="task-form-header">

                        <div>
                            <h2>Create New Task</h2>

                            <p>
                                Add a task to your Zarvis task list.
                            </p>
                        </div>

                        <button
                            type="button"
                            className="task-form-close"
                            onClick={closeForm}
                        >
                            ×
                        </button>

                    </div>

                    <div className="task-form-row">

                        <input
                            type="text"
                            placeholder="What do you need to do?"
                            value={newTask}
                            onChange={(event) =>
                                setNewTask(event.target.value)
                            }
                            onKeyDown={(event) => {
                                if (event.key === "Enter") {
                                    addTask();
                                }
                            }}
                            autoFocus
                        />

                        <button
                            type="button"
                            className="primary-action"
                            onClick={addTask}
                        >
                            <Plus size={17} />
                            Add
                        </button>

                    </div>

                </div>
            )}

            {/* TASK LIST */}
            <section className="glass-card tasks-page-card">

                <div className="card-header">

                    <div>
                        <h2>My Tasks</h2>

                        <p>
                            Your current tasks and priorities
                        </p>
                    </div>

                    <button
                        type="button"
                        className="small-action"
                        onClick={() => setShowForm(true)}
                    >
                        <Plus size={15} />
                        Add Task
                    </button>

                </div>

                <div className="tasks-page-list">

                    {tasks.map((task) => (
                        <div
                            className={`tasks-page-item ${task.completed ? "completed" : ""
                                }`}
                            key={task.id}
                        >

                            {/* COMPLETE */}
                            <button
                                type="button"
                                className="task-toggle"
                                onClick={() => toggleTask(task.id)}
                            >
                                {task.completed ? (
                                    <CheckCircle2 size={22} />
                                ) : (
                                    <Circle size={22} />
                                )}
                            </button>

                            {/* INFO */}
                            <div className="task-page-info">

                                <strong>
                                    {task.title}
                                </strong>

                                <span>
                                    <Clock3 size={13} />
                                    {task.time}
                                </span>

                            </div>

                            {/* PRIORITY */}
                            <span
                                className={`priority priority-${task.priority.toLowerCase()}`}
                            >
                                {task.priority}
                            </span>

                            {/* MORE */}
                            <button
                                type="button"
                                className="task-more"
                                title="More options"
                            >
                                <MoreHorizontal size={19} />
                            </button>

                        </div>
                    ))}

                </div>

            </section>

        </div>
    );
}

export default Tasks;