import { useState } from "react";
import { useLocation } from "react-router-dom";

import {
    Plus,
    Search,
    CheckCircle2,
    Circle,
    Trash2,
    Clock3,
    CalendarDays,
    ListTodo,
} from "lucide-react";

import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";

const initialTasks = [
    {
        id: 1,
        title: "Complete AI assignment",
        description: "Finish today's AI coursework",
        date: "Today",
        time: "10:30 AM",
        priority: "HIGH",
        completed: true,
    },
    {
        id: 2,
        title: "Study Machine Learning",
        description: "Revise supervised learning concepts",
        date: "Today",
        time: "12:00 PM",
        priority: "MEDIUM",
        completed: false,
    },
    {
        id: 3,
        title: "Work on Zarvis frontend",
        description: "Continue dashboard development",
        date: "Today",
        time: "03:30 PM",
        priority: "HIGH",
        completed: false,
    },
    {
        id: 4,
        title: "Review today's notes",
        description: "Quick revision before evening",
        date: "Today",
        time: "06:00 PM",
        priority: "LOW",
        completed: false,
    },
];


function Tasks() {

    const location = useLocation();

    const [tasks, setTasks] = useState(initialTasks);

    const [search, setSearch] = useState("");

    // Opens automatically when coming from Dashboard → Create Task
    const [showForm, setShowForm] = useState(
        location.state?.openForm === true
    );


    const [newTask, setNewTask] = useState({
        title: "",
        description: "",
        time: "",
        priority: "MEDIUM",
    });


    /* =================================================
       TOGGLE TASK
    ================================================= */

    const toggleTask = (id) => {

        setTasks((prev) =>
            prev.map((task) =>
                task.id === id
                    ? {
                        ...task,
                        completed: !task.completed,
                    }
                    : task
            )
        );

    };


    /* =================================================
       DELETE TASK
    ================================================= */

    const deleteTask = (id) => {

        setTasks((prev) =>
            prev.filter((task) => task.id !== id)
        );

    };


    /* =================================================
       ADD TASK
    ================================================= */

    const addTask = (event) => {

        event.preventDefault();

        if (!newTask.title.trim()) return;


        const task = {

            id: Date.now(),

            title: newTask.title.trim(),

            description:
                newTask.description.trim() ||
                "Created with Zarvis",

            date: "Today",

            time: newTask.time || "Anytime",

            priority: newTask.priority,

            completed: false,

        };


        setTasks((prev) => [
            task,
            ...prev,
        ]);


        // Reset form
        setNewTask({
            title: "",
            description: "",
            time: "",
            priority: "MEDIUM",
        });


        setShowForm(false);

    };


    /* =================================================
       SEARCH
    ================================================= */

    const filteredTasks = tasks.filter((task) =>

        `${task.title} ${task.description}`
            .toLowerCase()
            .includes(search.toLowerCase())

    );


    /* =================================================
       TASK STATS
    ================================================= */

    const completedTasks = tasks.filter(
        (task) => task.completed
    ).length;


    const pendingTasks =
        tasks.length - completedTasks;


    const completionPercentage =
        tasks.length
            ? Math.round(
                (completedTasks / tasks.length) * 100
            )
            : 0;


    return (

        <div className="app">

            {/* =================================================
                SIDEBAR
            ================================================= */}

            <Sidebar />


            <main className="main-content">

                {/* =================================================
                    NAVBAR
                ================================================= */}

                <Navbar />


                <div className="tasks-page">


                    {/* =================================================
                        HEADER
                    ================================================= */}

                    <section className="tasks-header">

                        <div>

                            <span className="tasks-eyebrow">

                                <ListTodo size={14} />

                                ZARVIS TASK SYSTEM

                            </span>


                            <h1>
                                My Tasks
                            </h1>


                            <p>
                                Organize your work and let Zarvis
                                keep you on track.
                            </p>

                        </div>


                        <button
                            type="button"
                            className="tasks-add-button"
                            onClick={() =>
                                setShowForm(!showForm)
                            }
                        >

                            <Plus size={18} />

                            Add Task

                        </button>

                    </section>


                    {/* =================================================
                        STATS
                    ================================================= */}

                    <section className="tasks-stats">


                        <div className="tasks-stat-card">

                            <span>
                                Total Tasks
                            </span>

                            <strong>
                                {tasks.length}
                            </strong>

                        </div>


                        <div className="tasks-stat-card">

                            <span>
                                Completed
                            </span>

                            <strong>
                                {completedTasks}
                            </strong>

                        </div>


                        <div className="tasks-stat-card">

                            <span>
                                Pending
                            </span>

                            <strong>
                                {pendingTasks}
                            </strong>

                        </div>


                        <div className="tasks-stat-card">

                            <span>
                                Completion
                            </span>

                            <strong>
                                {completionPercentage}%
                            </strong>

                        </div>


                    </section>


                    {/* =================================================
                        ADD TASK FORM
                    ================================================= */}

                    {showForm && (

                        <form
                            className="task-create-panel"
                            onSubmit={addTask}
                        >


                            <div className="task-create-header">

                                <div>

                                    <span>
                                        TASK CREATOR
                                    </span>

                                    <h2>
                                        Create New Task
                                    </h2>

                                </div>


                                <button
                                    type="button"
                                    onClick={() =>
                                        setShowForm(false)
                                    }
                                    aria-label="Close task form"
                                >
                                    ×
                                </button>

                            </div>


                            <div className="task-form-grid">


                                {/* TASK NAME */}

                                <div className="task-form-field">

                                    <label>
                                        Task Name
                                    </label>


                                    <input
                                        type="text"
                                        placeholder="e.g. Complete project"
                                        value={newTask.title}
                                        onChange={(e) =>
                                            setNewTask({
                                                ...newTask,
                                                title: e.target.value,
                                            })
                                        }
                                    />

                                </div>


                                {/* TIME */}

                                <div className="task-form-field">

                                    <label>
                                        Time
                                    </label>


                                    <input
                                        type="time"
                                        value={newTask.time}
                                        onChange={(e) =>
                                            setNewTask({
                                                ...newTask,
                                                time: e.target.value,
                                            })
                                        }
                                    />

                                </div>


                                {/* DESCRIPTION */}

                                <div className="task-form-field task-form-wide">

                                    <label>
                                        Description
                                    </label>


                                    <input
                                        type="text"
                                        placeholder="Add a short description"
                                        value={newTask.description}
                                        onChange={(e) =>
                                            setNewTask({
                                                ...newTask,
                                                description:
                                                    e.target.value,
                                            })
                                        }
                                    />

                                </div>


                                {/* PRIORITY */}

                                <div className="task-form-field">

                                    <label>
                                        Priority
                                    </label>


                                    <select
                                        value={newTask.priority}
                                        onChange={(e) =>
                                            setNewTask({
                                                ...newTask,
                                                priority:
                                                    e.target.value,
                                            })
                                        }
                                    >

                                        <option value="HIGH">
                                            HIGH
                                        </option>

                                        <option value="MEDIUM">
                                            MEDIUM
                                        </option>

                                        <option value="LOW">
                                            LOW
                                        </option>

                                    </select>

                                </div>

                            </div>


                            {/* CREATE */}

                            <button
                                type="submit"
                                className="task-create-submit"
                            >

                                <Plus size={16} />

                                CREATE TASK

                            </button>

                        </form>

                    )}


                    {/* =================================================
                        SEARCH
                    ================================================= */}

                    <section className="tasks-toolbar">


                        <div className="tasks-search">

                            <Search size={17} />


                            <input
                                type="text"
                                placeholder="Search your tasks..."
                                value={search}
                                onChange={(e) =>
                                    setSearch(e.target.value)
                                }
                            />

                        </div>


                        <div className="tasks-toolbar-status">

                            <span></span>

                            {pendingTasks} TASKS ACTIVE

                        </div>

                    </section>


                    {/* =================================================
                        TASK LIST
                    ================================================= */}

                    <section className="tasks-list-panel">


                        <div className="tasks-list-header">

                            <div>

                                <span>
                                    TASK QUEUE // 01
                                </span>

                                <h2>
                                    Today's Tasks
                                </h2>

                            </div>


                            <div className="tasks-list-count">
                                {filteredTasks.length}
                            </div>

                        </div>


                        <div className="tasks-list">


                            {/* EMPTY STATE */}

                            {filteredTasks.length === 0 ? (

                                <div className="tasks-empty">

                                    <ListTodo size={32} />

                                    <h3>
                                        No tasks found
                                    </h3>

                                    <p>
                                        Try another search or create
                                        a new task.
                                    </p>

                                </div>

                            ) : (

                                filteredTasks.map((task) => (

                                    <div
                                        className={`task-page-row ${task.completed
                                                ? "task-page-completed"
                                                : ""
                                            }`}
                                        key={task.id}
                                    >


                                        {/* =================================================
                                            CHECK
                                        ================================================= */}

                                        <button
                                            type="button"
                                            className="task-page-check"
                                            onClick={() =>
                                                toggleTask(task.id)
                                            }
                                            aria-label={
                                                task.completed
                                                    ? "Mark task incomplete"
                                                    : "Mark task complete"
                                            }
                                        >

                                            {task.completed ? (

                                                <CheckCircle2
                                                    size={21}
                                                />

                                            ) : (

                                                <Circle
                                                    size={21}
                                                />

                                            )}

                                        </button>


                                        {/* =================================================
                                            CONTENT
                                        ================================================= */}

                                        <div className="task-page-content">


                                            <strong>
                                                {task.title}
                                            </strong>


                                            <span>
                                                {task.description}
                                            </span>


                                            <div className="task-page-meta">


                                                <span>

                                                    <CalendarDays
                                                        size={12}
                                                    />

                                                    {task.date}

                                                </span>


                                                <span>

                                                    <Clock3
                                                        size={12}
                                                    />

                                                    {task.time}

                                                </span>


                                            </div>

                                        </div>


                                        {/* =================================================
                                            PRIORITY
                                        ================================================= */}

                                        <span
                                            className={`task-page-priority priority-${task.priority.toLowerCase()}`}
                                        >
                                            {task.priority}
                                        </span>


                                        {/* =================================================
                                            DELETE
                                        ================================================= */}

                                        <button
                                            type="button"
                                            className="task-page-delete"
                                            onClick={() =>
                                                deleteTask(task.id)
                                            }
                                            title="Delete task"
                                            aria-label="Delete task"
                                        >

                                            <Trash2 size={16} />

                                        </button>

                                    </div>

                                ))

                            )}

                        </div>

                    </section>

                </div>

            </main>

        </div>

    );
}


export default Tasks;