// ==========================================
// ZARVIS TASK HOOK
// ==========================================

import { useCallback, useEffect, useState } from "react";
import taskService from "../services/taskService";

function useTasks() {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    // Load all tasks
    const loadTasks = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const data = await taskService.getTasks();

            setTasks(
                Array.isArray(data)
                    ? data
                    : data?.tasks || []
            );
        } catch (err) {
            console.error("Failed to load tasks:", err);
            setError("Unable to load tasks.");
        } finally {
            setLoading(false);
        }
    }, []);

    // Create task
    const addTask = useCallback(async (task) => {
        setError("");

        try {
            const newTask = await taskService.createTask(task);

            setTasks((currentTasks) => [
                ...currentTasks,
                newTask,
            ]);

            return newTask;
        } catch (err) {
            console.error("Failed to create task:", err);
            setError("Unable to create task.");
            return null;
        }
    }, []);

    // Update task
    const editTask = useCallback(async (taskId, task) => {
        setError("");

        try {
            const updatedTask = await taskService.updateTask(
                taskId,
                task
            );

            setTasks((currentTasks) =>
                currentTasks.map((item) =>
                    item.id === taskId
                        ? updatedTask
                        : item
                )
            );

            return updatedTask;
        } catch (err) {
            console.error("Failed to update task:", err);
            setError("Unable to update task.");
            return null;
        }
    }, []);

    // Complete task
    const completeTask = useCallback(async (taskId) => {
        setError("");

        try {
            const updatedTask =
                await taskService.completeTask(taskId);

            setTasks((currentTasks) =>
                currentTasks.map((item) =>
                    item.id === taskId
                        ? {
                            ...item,
                            ...updatedTask,
                            completed: true,
                        }
                        : item
                )
            );

            return updatedTask;
        } catch (err) {
            console.error(
                "Failed to complete task:",
                err
            );
            setError("Unable to complete task.");
            return null;
        }
    }, []);

    // Delete task
    const removeTask = useCallback(async (taskId) => {
        setError("");

        try {
            await taskService.deleteTask(taskId);

            setTasks((currentTasks) =>
                currentTasks.filter(
                    (item) => item.id !== taskId
                )
            );

            return true;
        } catch (err) {
            console.error("Failed to delete task:", err);
            setError("Unable to delete task.");
            return false;
        }
    }, []);

    // Load tasks when hook starts
    useEffect(() => {
        loadTasks();
    }, [loadTasks]);

    return {
        tasks,
        loading,
        error,
        loadTasks,
        addTask,
        editTask,
        completeTask,
        removeTask,
    };
}

export default useTasks;