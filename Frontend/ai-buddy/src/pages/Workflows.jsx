import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import {
    Plus,
    Workflow as WorkflowIcon,
    Trash2,
    Clock3,
    CheckCircle2,
    Zap,
    ArrowRight,
} from "lucide-react";

import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";

import { useAuth } from "../context/AuthContext";

import {
    getWorkflows,
    createWorkflow as createWorkflowApi,
    deleteWorkflow as deleteWorkflowApi,
} from "../services/workflowService";


function Workflows() {

    const location = useLocation();

    const {
        user,
        authenticated,
    } = useAuth();


    const [workflows, setWorkflows] = useState([]);

    const [loading, setLoading] = useState(true);

    const [saving, setSaving] = useState(false);

    const [error, setError] = useState("");

    const [success, setSuccess] = useState("");


    const [showForm, setShowForm] = useState(
        location.state?.openForm === true
    );


    const [newWorkflow, setNewWorkflow] = useState({
        name: "",
        description: "",
        tool: "task",
        steps: "",
    });


    // ------------------------------------------
    // LOAD WORKFLOWS
    // ------------------------------------------

    const loadWorkflows = async () => {

        if (!authenticated || !user?.id) {
            setWorkflows([]);
            setLoading(false);
            return;
        }

        try {

            setLoading(true);
            setError("");

            const result = await getWorkflows(user.id);

            const backendWorkflows =
                Array.isArray(result?.workflows)
                    ? result.workflows
                    : [];


            const formattedWorkflows =
                backendWorkflows.map((workflow) => {

                    const parameters =
                        workflow.parameters ||
                        workflow.plan?.parameters ||
                        {};


                    const rawSteps =
                        parameters.steps || [];


                    const steps =
                        Array.isArray(rawSteps)
                            ? rawSteps
                            : [];


                    const displaySteps =
                        steps.length > 0
                            ? steps.map((step) => {

                                if (
                                    typeof step === "object" &&
                                    step !== null
                                ) {
                                    return (
                                        step.description ||
                                        step.name ||
                                        step.parameters?.task_name ||
                                        step.parameters?.reminder ||
                                        step.parameters?.city ||
                                        `${step.tool || "Action"} step`
                                    );
                                }

                                return String(step);
                            })
                            : [
                                "Workflow configured"
                            ];


                    return {

                        id: workflow.id,

                        name:
                            workflow.name ||
                            workflow.plan?.name ||
                            "Unnamed Workflow",

                        description:
                            workflow.description ||
                            parameters.description ||
                            "Workflow created with AI Buddy.",

                        tool:
                            workflow.tool ||
                            workflow.plan?.tool ||
                            "task",

                        status:
                            String(
                                workflow.status ||
                                "READY"
                            ).toUpperCase(),

                        steps: displaySteps,

                        lastRun:
                            workflow.last_run ||
                            workflow.updated_at ||
                            "Never",

                    };

                });


            setWorkflows(formattedWorkflows);

        } catch (requestError) {

            console.error(
                "Failed to load workflows:",
                requestError
            );

            setError(
                "Unable to load workflows from the backend."
            );

            setWorkflows([]);

        } finally {

            setLoading(false);

        }

    };


    // ------------------------------------------
    // INITIAL LOAD
    // ------------------------------------------

    useEffect(() => {

        loadWorkflows();

    }, [
        authenticated,
        user?.id
    ]);


    // ------------------------------------------
    // CREATE WORKFLOW
    // ------------------------------------------

    const handleCreateWorkflow =
        async (event) => {

            event.preventDefault();

            const name =
                newWorkflow.name.trim();


            const description =
                newWorkflow.description.trim();


            const tool =
                newWorkflow.tool.trim().toLowerCase();


            if (!name) {

                setError(
                    "Workflow name is required."
                );

                return;

            }


            if (!authenticated || !user?.id) {

                setError(
                    "Please login before creating a workflow."
                );

                return;

            }


            const rawSteps =
                newWorkflow.steps
                    .split(",")
                    .map((step) => step.trim())
                    .filter(Boolean);


            if (rawSteps.length === 0) {

                setError(
                    "Please enter at least one workflow step."
                );

                return;

            }


            const supportedTools = [
                "task",
                "reminder",
                "timer",
                "weather",
                "browser",
            ];


            if (!supportedTools.includes(tool)) {

                setError(
                    "Please select a supported workflow tool."
                );

                return;

            }


            // ------------------------------------------
            // CONVERT TEXT STEPS INTO BACKEND STEPS
            // ------------------------------------------

            const steps =
                rawSteps.map((stepText, index) => {

                    let parameters = {};


                    if (tool === "task") {

                        parameters = {
                            task_name: stepText,
                        };

                    }


                    else if (tool === "reminder") {

                        parameters = {
                            reminder: stepText,
                            time: "",
                        };

                    }


                    else if (tool === "timer") {

                        const duration =
                            Number(stepText);


                        parameters = {
                            duration_seconds:
                                Number.isFinite(duration) &&
                                duration > 0
                                    ? duration
                                    : 60,
                        };

                    }


                    else if (tool === "weather") {

                        parameters = {
                            city: stepText,
                        };

                    }


                    else if (tool === "browser") {

                        parameters = {
                            action: stepText,
                        };

                    }


                    return {

                        step_id: index + 1,

                        tool,

                        parameters,

                        description: stepText,

                    };

                });


            try {

                setSaving(true);

                setError("");

                setSuccess("");


                await createWorkflowApi(

                    {

                        name,

                        description,

                        tool,

                        parameters: {

                            description,

                            steps,

                        },

                    },

                    user.id

                );


                setSuccess(
                    "Workflow created successfully."
                );


                setNewWorkflow({

                    name: "",

                    description: "",

                    tool: "task",

                    steps: "",

                });


                setShowForm(false);


                await loadWorkflows();


            } catch (requestError) {

                console.error(
                    "Workflow creation failed:",
                    requestError
                );

                setError(
                    requestError?.message ||
                    "Unable to create workflow."
                );

            } finally {

                setSaving(false);

            }

        };


    // ------------------------------------------
    // DELETE WORKFLOW
    // ------------------------------------------

    const handleDeleteWorkflow =
        async (workflowId) => {

            if (!authenticated || !user?.id) {

                setError(
                    "Please login before deleting a workflow."
                );

                return;

            }


            try {

                setError("");

                setSuccess("");


                await deleteWorkflowApi(
                    workflowId,
                    user.id
                );


                setSuccess(
                    "Workflow deleted successfully."
                );


                await loadWorkflows();

            } catch (requestError) {

                console.error(
                    "Workflow deletion failed:",
                    requestError
                );

                setError(
                    requestError?.message ||
                    "Unable to delete workflow."
                );

            }

        };


    // ------------------------------------------
    // WORKFLOW COUNTS
    // ------------------------------------------

    const activeCount =
        workflows.filter(
            (workflow) =>
                workflow.status === "ACTIVE"
        ).length;


    const readyCount =
        workflows.filter(
            (workflow) =>
                workflow.status !== "ACTIVE"
        ).length;


    // ------------------------------------------
    // UI
    // ------------------------------------------

    return (

        <div className="app">

            <Sidebar />


            <main className="main-content">

                <Navbar />


                <div className="workflows-page">


                    {/* HEADER */}

                    <section className="workflows-header">

                        <div>

                            <span className="workflows-eyebrow">

                                <WorkflowIcon size={14} />

                                ZARVIS AUTOMATION SYSTEM

                            </span>


                            <h1>
                                Workflows
                            </h1>


                            <p>
                                Build routines that Zarvis can
                                organize and execute for you.
                            </p>

                        </div>


                        <button
                            type="button"
                            className="workflow-add-button"
                            onClick={() => {

                                setError("");

                                setSuccess("");

                                setShowForm(
                                    !showForm
                                );

                            }}
                        >

                            <Plus size={18} />

                            Create Workflow

                        </button>

                    </section>


                    {/* MESSAGES */}

                    {error && (

                        <div className="schedule-message schedule-error">

                            {error}

                        </div>

                    )}


                    {success && (

                        <div className="schedule-message schedule-success">

                            {success}

                        </div>

                    )}


                    {/* STATS */}

                    <section className="workflow-stats">


                        <div className="workflow-stat-card">

                            <span>
                                TOTAL WORKFLOWS
                            </span>

                            <strong>
                                {loading
                                    ? "..."
                                    : workflows.length}
                            </strong>

                        </div>


                        <div className="workflow-stat-card">

                            <span>
                                ACTIVE
                            </span>

                            <strong>
                                {loading
                                    ? "..."
                                    : activeCount}
                            </strong>

                        </div>


                        <div className="workflow-stat-card">

                            <span>
                                READY
                            </span>

                            <strong>
                                {loading
                                    ? "..."
                                    : readyCount}
                            </strong>

                        </div>


                        <div className="workflow-stat-card">

                            <span>
                                EXECUTION
                            </span>

                            <strong>
                                READY
                            </strong>

                        </div>

                    </section>


                    {/* CREATE WORKFLOW */}

                    {showForm && (

                        <form
                            className="workflow-create-panel"
                            onSubmit={
                                handleCreateWorkflow
                            }
                        >


                            <div className="workflow-create-header">

                                <div>

                                    <span>
                                        WORKFLOW BUILDER
                                    </span>

                                    <h2>
                                        Create New Workflow
                                    </h2>

                                </div>


                                <button
                                    type="button"
                                    onClick={() =>
                                        setShowForm(false)
                                    }
                                    aria-label="Close workflow form"
                                >
                                    ×
                                </button>

                            </div>


                            <div className="workflow-form-grid">


                                {/* WORKFLOW NAME */}

                                <div className="workflow-field">

                                    <label>
                                        Workflow Name
                                    </label>

                                    <input
                                        type="text"
                                        placeholder="e.g. Morning Tasks"
                                        value={
                                            newWorkflow.name
                                        }
                                        onChange={(event) =>
                                            setNewWorkflow({
                                                ...newWorkflow,
                                                name:
                                                    event.target.value,
                                            })
                                        }
                                    />

                                </div>


                                {/* DESCRIPTION */}

                                <div className="workflow-field">

                                    <label>
                                        Description
                                    </label>

                                    <input
                                        type="text"
                                        placeholder="What should this workflow do?"
                                        value={
                                            newWorkflow.description
                                        }
                                        onChange={(event) =>
                                            setNewWorkflow({
                                                ...newWorkflow,
                                                description:
                                                    event.target.value,
                                            })
                                        }
                                    />

                                </div>


                                {/* TOOL */}

                                <div className="workflow-field">

                                    <label>
                                        Action Tool
                                    </label>

                                    <select
                                        value={
                                            newWorkflow.tool
                                        }
                                        onChange={(event) =>
                                            setNewWorkflow({
                                                ...newWorkflow,
                                                tool:
                                                    event.target.value,
                                            })
                                        }
                                    >

                                        <option value="task">
                                            Task
                                        </option>

                                        <option value="reminder">
                                            Reminder
                                        </option>

                                        <option value="timer">
                                            Timer
                                        </option>

                                        <option value="weather">
                                            Weather
                                        </option>

                                        <option value="browser">
                                            Browser
                                        </option>

                                    </select>

                                </div>


                                {/* STEPS */}

                                <div className="workflow-field workflow-field-wide">

                                    <label>
                                        Steps
                                    </label>

                                    <input
                                        type="text"
                                        placeholder={
                                            newWorkflow.tool === "task"
                                                ? "Study Python, Complete assignment"
                                                : newWorkflow.tool === "reminder"
                                                    ? "Submit assignment, Attend meeting"
                                                    : newWorkflow.tool === "timer"
                                                        ? "60, 300, 600"
                                                        : newWorkflow.tool === "weather"
                                                            ? "Jaipur, Delhi, Mumbai"
                                                            : "Open website, Search information"
                                        }
                                        value={
                                            newWorkflow.steps
                                        }
                                        onChange={(event) =>
                                            setNewWorkflow({
                                                ...newWorkflow,
                                                steps:
                                                    event.target.value,
                                            })
                                        }
                                    />

                                    <small>
                                        Separate each step with a comma.
                                    </small>

                                </div>

                            </div>


                            <button
                                type="submit"
                                className="workflow-create-submit"
                                disabled={saving}
                            >

                                <Plus size={16} />

                                {saving
                                    ? "CREATING..."
                                    : "CREATE WORKFLOW"}

                            </button>

                        </form>

                    )}


                    {/* WORKFLOW LIST */}

                    <section className="workflow-list-panel">


                        <div className="workflow-list-header">

                            <div>

                                <span>
                                    AUTOMATION QUEUE // {String(
                                        workflows.length
                                    ).padStart(2, "0")}
                                </span>

                                <h2>
                                    Your Workflows
                                </h2>

                            </div>


                            <div className="workflow-network-status">

                                <span></span>

                                SYSTEM READY

                            </div>

                        </div>


                        <div className="workflow-list">


                            {loading ? (

                                <div className="workflow-empty">

                                    <WorkflowIcon size={34} />

                                    <h3>
                                        Loading workflows...
                                    </h3>

                                    <p>
                                        Fetching workflows from AI Buddy.
                                    </p>

                                </div>

                            ) : workflows.length === 0 ? (

                                <div className="workflow-empty">

                                    <WorkflowIcon size={34} />

                                    <h3>
                                        No workflows yet
                                    </h3>

                                    <p>
                                        Create your first automated
                                        routine with Zarvis.
                                    </p>

                                </div>

                            ) : (

                                workflows.map(
                                    (workflow) => (

                                        <article
                                            className="workflow-card"
                                            key={workflow.id}
                                        >


                                            {/* CARD TOP */}

                                            <div className="workflow-card-top">


                                                <div className="workflow-card-title">


                                                    <div className="workflow-card-icon">

                                                        <Zap size={17} />

                                                    </div>


                                                    <div>

                                                        <h3>
                                                            {workflow.name}
                                                        </h3>

                                                        <p>
                                                            {workflow.description}
                                                        </p>

                                                    </div>

                                                </div>


                                                <div
                                                    className={`workflow-status ${
                                                        workflow.status ===
                                                            "ACTIVE"
                                                            ? "workflow-active"
                                                            : "workflow-ready"
                                                    }`}
                                                >

                                                    <span></span>

                                                    {workflow.status}

                                                </div>

                                            </div>


                                            {/* TOOL */}

                                            <div className="workflow-steps">

                                                <div className="workflow-steps-label">

                                                    ACTION TOOL

                                                </div>


                                                <div className="workflow-step-list">

                                                    <div className="workflow-step">

                                                        <div className="workflow-step-number">
                                                            AI
                                                        </div>

                                                        <span>
                                                            {String(
                                                                workflow.tool ||
                                                                "task"
                                                            ).toUpperCase()}
                                                        </span>

                                                    </div>

                                                </div>

                                            </div>


                                            {/* STEPS */}

                                            <div className="workflow-steps">

                                                <div className="workflow-steps-label">

                                                    WORKFLOW STEPS

                                                </div>


                                                <div className="workflow-step-list">


                                                    {workflow.steps.map(
                                                        (
                                                            step,
                                                            index
                                                        ) => (

                                                            <div
                                                                className="workflow-step"
                                                                key={
                                                                    index
                                                                }
                                                            >

                                                                <div className="workflow-step-number">

                                                                    {String(
                                                                        index +
                                                                        1
                                                                    ).padStart(
                                                                        2,
                                                                        "0"
                                                                    )}

                                                                </div>


                                                                <span>
                                                                    {step}
                                                                </span>


                                                                {index <
                                                                    workflow
                                                                        .steps
                                                                        .length -
                                                                    1 && (

                                                                        <ArrowRight
                                                                            size={
                                                                                13
                                                                            }
                                                                        />

                                                                    )}

                                                            </div>

                                                        )
                                                    )}

                                                </div>

                                            </div>


                                            {/* FOOTER */}

                                            <div className="workflow-card-footer">


                                                <div className="workflow-last-run">

                                                    <Clock3 size={13} />

                                                    <span>
                                                        Last run:
                                                    </span>

                                                    <strong>
                                                        {workflow.lastRun}
                                                    </strong>

                                                </div>


                                                <div className="workflow-actions">


                                                    <button
                                                        type="button"
                                                        className="workflow-run-button"
                                                        disabled
                                                        title="Workflow execution endpoint is not implemented yet"
                                                    >

                                                        <CheckCircle2
                                                            size={14}
                                                        />

                                                        READY

                                                    </button>


                                                    <button
                                                        type="button"
                                                        className="workflow-delete-button"
                                                        onClick={() =>
                                                            handleDeleteWorkflow(
                                                                workflow.id
                                                            )
                                                        }
                                                        title="Delete workflow"
                                                        aria-label="Delete workflow"
                                                    >

                                                        <Trash2 size={15} />

                                                    </button>

                                                </div>

                                            </div>


                                        </article>

                                    )
                                )

                            )}

                        </div>

                    </section>

                </div>

            </main>

        </div>

    );

}


export default Workflows;