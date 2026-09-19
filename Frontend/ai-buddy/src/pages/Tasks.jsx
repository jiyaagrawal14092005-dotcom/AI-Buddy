import { useEffect, useMemo, useState } from "react";
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

import { useAuth } from "../context/AuthContext";
import {
    getTasks,
    createTask,
    deleteTask,
    updateTaskStatus,
} from "../services/taskService";


function normalizeTask(task) {
    return {
        id: task.id,
        user_id: task.user_id,
        title: task.title || "Untitled Task",
        description:
            task.description ||
            "No description available",
        date: task.created_at
            ? new Date(task.created_at).toLocaleDateString()
            : "Today",
        time: task.created_at
            ? new Date(task.created_at).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            })
            : "Anytime",
        priority: "MEDIUM",
        completed: task.status === "completed",
        status: task.status || "pending",
        created_at: task.created_at,
    };
}


function Tasks() {

    const location = useLocation();

    const { user, authenticated } = useAuth();

    const userId = user?.id;


    // ==========================================
    // TASK STATE
    // ==========================================

    const [tasks, setTasks] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    const [actionLoading, setActionLoading] = useState(false);


    // ==========================================
    // SEARCH
    // ==========================================

    const [search, setSearch] = useState("");


    // ==========================================
    // ADD TASK FORM
    // ==========================================

    const [showForm, setShowForm] = useState(
        location.state?.openForm === true
    );


    const [newTask, setNewTask] = useState({
        title: "",
        description: "",
        time: "",
        priority: "MEDIUM",
    });


    // ==========================================
    // LOAD TASKS FROM BACKEND
    // ==========================================

    const loadTasks = async () => {

        if (!userId) {
            setTasks([]);
            setLoading(false);
            return;
        }

        try {

            setLoading(true);

            setError("");

            const result = await getTasks(userId);

            if (!result?.success) {

                throw new Error(
                    result?.message ||
                    "Unable to load tasks."
                );

            }

            const backendTasks = Array.isArray(result.tasks)
                ? result.tasks
                : [];

            setTasks(
                backendTasks.map(normalizeTask)
            );

        } catch (err) {

            console.error(
                "Failed to load tasks:",
                err
            );

            setError(
                err?.message ||
                "Failed to load tasks."
            );

            setTasks([]);

        } finally {

            setLoading(false);

        }
    };


    // ==========================================
    // INITIAL LOAD
    // ==========================================

    useEffect(() => {

        if (authenticated && userId) {
            loadTasks();
        } else {
            setTasks([]);
            setLoading(false);
        }

    }, [authenticated, userId]);


    // ==========================================
    // TOGGLE TASK STATUS
    // ==========================================

    const toggleTask = async (id) => {

        if (!userId) {

            setError(
                "Please login before updating a task."
            );

            return;
        }

        if (actionLoading) {
            return;
        }


        const selectedTask = tasks.find(
            (task) => task.id === id
        );


        if (!selectedTask) {
            return;
        }


        const nextStatus =
            selectedTask.completed
                ? "pending"
                : "completed";


        try {

            setActionLoading(true);

            setError("");


            const result = await updateTaskStatus(
                id,
                userId,
                nextStatus
            );


            if (!result?.success) {

                throw new Error(
                    result?.message ||
                    "Task status could not be updated."
                );

            }


            // Backend returns the updated task.

            if (result.task) {

                const updatedTask =
                    normalizeTask(result.task);


                setTasks((previousTasks) =>
                    previousTasks.map((task) =>
                        task.id === id
                            ? updatedTask
                            : task
                    )
                );

            } else {

                // Safe fallback:
                // reload from database.

                await loadTasks();

            }

        } catch (err) {

            console.error(
                "Failed to update task status:",
                err
            );

            setError(
                err?.message ||
                "Failed to update task status."
            );

        } finally {

            setActionLoading(false);

        }
    };


    // ==========================================
    // DELETE TASK
    // ==========================================

    const handleDeleteTask = async (id) => {

        if (!userId) {

            setError(
                "User ID is required."
            );

            return;
        }

        try {

            setActionLoading(true);

            setError("");

            const result = await deleteTask(
                id,
                userId
            );

            if (!result?.success) {

                throw new Error(
                    result?.message ||
                    "Task could not be deleted."
                );

            }

            setTasks((previousTasks) =>
                previousTasks.filter(
                    (task) => task.id !== id
                )
            );

        } catch (err) {

            console.error(
                "Failed to delete task:",
                err
            );

            setError(
                err?.message ||
                "Failed to delete task."
            );

        } finally {

            setActionLoading(false);

        }
    };


    // ==========================================
    // ADD TASK
    // ==========================================

    const addTask = async (event) => {

        event.preventDefault();

        if (!userId) {

            setError(
                "Please login before creating a task."
            );

            return;
        }

        if (!newTask.title.trim()) {

            setError(
                "Task title is required."
            );

            return;
        }


        try {

            setActionLoading(true);

            setError("");


            const result = await createTask(
                newTask,
                userId
            );


            if (!result?.success) {

                throw new Error(
                    result?.message ||
                    "Task could not be created."
                );

            }


            if (result.task) {

                const createdTask =
                    normalizeTask(result.task);

                setTasks((previousTasks) => [
                    createdTask,
                    ...previousTasks,
                ]);

            } else {

                // Safe fallback:
                // refresh database data.

                await loadTasks();

            }


            // Reset form

            setNewTask({
                title: "",
                description: "",
                time: "",
                priority: "MEDIUM",
            });


            setShowForm(false);

        } catch (err) {

            console.error(
                "Failed to create task:",
                err
            );

            setError(
                err?.message ||
                "Failed to create task."
            );

        } finally {

            setActionLoading(false);

        }
    };


    // ==========================================
    // SEARCH
    // ==========================================

    const filteredTasks = useMemo(() => {

        const searchText =
            search.trim().toLowerCase();

        if (!searchText) {
            return tasks;
        }

        return tasks.filter((task) =>
            `${task.title} ${task.description}`
                .toLowerCase()
                .includes(searchText)
        );

    }, [tasks, search]);


    // ==========================================
    // TASK STATS
    // ==========================================

    const completedTasks =
        tasks.filter(
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


    // ==========================================
    // RENDER
    // ==========================================

    return (

        <div className="app">

            {/* SIDEBAR */}

            <Sidebar />


            <main className="main-content">

                {/* NAVBAR */}

                <Navbar />


                <div className="tasks-page">


                    {/* ==========================================
                        HEADER
                    ========================================== */}

                    <section className="tasks-header">

                        <div>

                            <span className="tasks-eyebrow">

                                <ListTodo size={14} />

                                AI BUDDY TASK SYSTEM

                            </span>


                            <h1>
                                My Tasks
                            </h1>


                            <p>
                                Organize your work and let AI Buddy
                                keep you on track.
                            </p>

                        </div>


                        <button
                            type="button"
                            className="tasks-add-button"
                            onClick={() =>
                                setShowForm(!showForm)
                            }
                            disabled={actionLoading}
                        >

                            <Plus size={18} />

                            Add Task

                        </button>

                    </section>


                    {/* ==========================================
                        ERROR MESSAGE
                    ========================================== */}

                    {error && (

                        <div className="task-error">

                            {error}

                        </div>

                    )}


                    {/* ==========================================
                        STATS
                    ========================================== */}

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


                    {/* ==========================================
                        ADD TASK FORM
                    ========================================== */}

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
                                        onChange={(event) =>
                                            setNewTask({
                                                ...newTask,
                                                title:
                                                    event.target.value,
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
                                        onChange={(event) =>
                                            setNewTask({
                                                ...newTask,
                                                time:
                                                    event.target.value,
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
                                        value={
                                            newTask.description
                                        }
                                        onChange={(event) =>
                                            setNewTask({
                                                ...newTask,
                                                description:
                                                    event.target.value,
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
                                        value={
                                            newTask.priority
                                        }
                                        onChange={(event) =>
                                            setNewTask({
                                                ...newTask,
                                                priority:
                                                    event.target.value,
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
                                disabled={actionLoading}
                            >

                                <Plus size={16} />

                                {actionLoading
                                    ? "CREATING..."
                                    : "CREATE TASK"}

                            </button>

                        </form>

                    )}


                    {/* ==========================================
                        SEARCH
                    ========================================== */}

                    <section className="tasks-toolbar">


                        <div className="tasks-search">

                            <Search size={17} />


                            <input
                                type="text"
                                placeholder="Search your tasks..."
                                value={search}
                                onChange={(event) =>
                                    setSearch(
                                        event.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="tasks-toolbar-status">

                            <span></span>

                            {pendingTasks} TASKS ACTIVE

                        </div>

                    </section>


                    {/* ==========================================
                        TASK LIST
                    ========================================== */}

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


                            {/* ==================================
                                LOADING
                            ================================== */}

                            {loading ? (

                                <div className="tasks-empty">

                                    <ListTodo size={32} />

                                    <h3>
                                        Loading tasks...
                                    </h3>

                                    <p>
                                        AI Buddy is fetching your
                                        tasks from the database.
                                    </p>

                                </div>

                            ) : filteredTasks.length === 0 ? (

                                /* ==================================
                                   EMPTY STATE
                                ================================== */

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

                                /* ==================================
                                   TASKS
                                ================================== */

                                filteredTasks.map((task) => (

                                    <div
                                        className={
                                            `task-page-row ${
                                                task.completed
                                                    ? "task-page-completed"
                                                    : ""
                                            }`
                                        }
                                        key={task.id}
                                    >


                                        {/* CHECK */}

                                        <button
                                            type="button"
                                            className="task-page-check"
                                            onClick={() =>
                                                toggleTask(
                                                    task.id
                                                )
                                            }
                                            aria-label={
                                                task.completed
                                                    ? "Mark task incomplete"
                                                    : "Mark task complete"
                                            }
                                            disabled={actionLoading}
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


                                        {/* CONTENT */}

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


                                        {/* PRIORITY */}

                                        <span
                                            className={
                                                `task-page-priority priority-${task.priority.toLowerCase()}`
                                            }
                                        >
                                            {task.priority}
                                        </span>


                                        {/* DELETE */}

                                        <button
                                            type="button"
                                            className="task-page-delete"
                                            onClick={() =>
                                                handleDeleteTask(
                                                    task.id
                                                )
                                            }
                                            title="Delete task"
                                            aria-label="Delete task"
                                            disabled={actionLoading}
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