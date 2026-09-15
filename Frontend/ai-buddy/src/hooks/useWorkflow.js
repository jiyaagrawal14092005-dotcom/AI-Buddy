// ==========================================
// ZARVIS WORKFLOW HOOK
// ==========================================

import { useCallback, useEffect, useState } from "react";
import workflowService from "../services/workflowService";

function useWorkflow() {
    const [workflows, setWorkflows] = useState([]);
    const [loading, setLoading] = useState(false);
    const [running, setRunning] = useState(false);
    const [error, setError] = useState("");

    // Load all workflows
    const loadWorkflows = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const data = await workflowService.getWorkflows();

            setWorkflows(
                Array.isArray(data)
                    ? data
                    : data?.workflows || []
            );
        } catch (err) {
            console.error(
                "Failed to load workflows:",
                err
            );

            setError("Unable to load workflows.");
        } finally {
            setLoading(false);
        }
    }, []);

    // Create workflow
    const addWorkflow = useCallback(async (workflow) => {
        setError("");

        try {
            const newWorkflow =
                await workflowService.createWorkflow(
                    workflow
                );

            setWorkflows((currentWorkflows) => [
                ...currentWorkflows,
                newWorkflow,
            ]);

            return newWorkflow;
        } catch (err) {
            console.error(
                "Failed to create workflow:",
                err
            );

            setError("Unable to create workflow.");
            return null;
        }
    }, []);

    // Update workflow
    const editWorkflow = useCallback(
        async (workflowId, workflow) => {
            setError("");

            try {
                const updatedWorkflow =
                    await workflowService.updateWorkflow(
                        workflowId,
                        workflow
                    );

                setWorkflows((currentWorkflows) =>
                    currentWorkflows.map((item) =>
                        item.id === workflowId
                            ? updatedWorkflow
                            : item
                    )
                );

                return updatedWorkflow;
            } catch (err) {
                console.error(
                    "Failed to update workflow:",
                    err
                );

                setError("Unable to update workflow.");
                return null;
            }
        },
        []
    );

    // Run workflow
    const runWorkflow = useCallback(async (workflowId) => {
        setRunning(true);
        setError("");

        try {
            const result =
                await workflowService.runWorkflow(
                    workflowId
                );

            setWorkflows((currentWorkflows) =>
                currentWorkflows.map((item) =>
                    item.id === workflowId
                        ? {
                            ...item,
                            status: "running",
                            active: true,
                        }
                        : item
                )
            );

            return result;
        } catch (err) {
            console.error(
                "Failed to run workflow:",
                err
            );

            setError("Unable to run workflow.");
            return null;
        } finally {
            setRunning(false);
        }
    }, []);

    // Stop workflow
    const stopWorkflow = useCallback(async (workflowId) => {
        setError("");

        try {
            const result =
                await workflowService.stopWorkflow(
                    workflowId
                );

            setWorkflows((currentWorkflows) =>
                currentWorkflows.map((item) =>
                    item.id === workflowId
                        ? {
                            ...item,
                            status: "stopped",
                            active: false,
                        }
                        : item
                )
            );

            return result;
        } catch (err) {
            console.error(
                "Failed to stop workflow:",
                err
            );

            setError("Unable to stop workflow.");
            return null;
        }
    }, []);

    // Delete workflow
    const removeWorkflow = useCallback(
        async (workflowId) => {
            setError("");

            try {
                await workflowService.deleteWorkflow(
                    workflowId
                );

                setWorkflows((currentWorkflows) =>
                    currentWorkflows.filter(
                        (item) => item.id !== workflowId
                    )
                );

                return true;
            } catch (err) {
                console.error(
                    "Failed to delete workflow:",
                    err
                );

                setError("Unable to delete workflow.");
                return false;
            }
        },
        []
    );

    // Load workflows when hook starts
    useEffect(() => {
        loadWorkflows();
    }, [loadWorkflows]);

    return {
        workflows,
        loading,
        running,
        error,
        loadWorkflows,
        addWorkflow,
        editWorkflow,
        runWorkflow,
        stopWorkflow,
        removeWorkflow,
    };
}

export default useWorkflow;