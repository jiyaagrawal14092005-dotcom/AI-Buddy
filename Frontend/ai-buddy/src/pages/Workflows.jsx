import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
    Workflow,
    Plus,
    Play,
    Clock3,
    CheckCircle2,
    MoreHorizontal,
    X,
} from "lucide-react";

function Workflows() {
    const [searchParams, setSearchParams] = useSearchParams();

    const [workflows, setWorkflows] = useState([
        {
            id: 1,
            title: "Morning Planning",
            description:
                "Review tasks and create your daily plan",
            steps: 4,
            lastRun: "Today, 9:00 AM",
            status: "Active",
        },
        {
            id: 2,
            title: "Study Routine",
            description:
                "Organize study sessions and track progress",
            steps: 5,
            lastRun: "Yesterday",
            status: "Active",
        },
        {
            id: 3,
            title: "Project Review",
            description:
                "Review project tasks and pending work",
            steps: 3,
            lastRun: "Monday",
            status: "Paused",
        },
    ]);

    const [runningWorkflow, setRunningWorkflow] =
        useState(null);

    const [showForm, setShowForm] = useState(
        searchParams.get("create") === "true"
    );

    const [workflowTitle, setWorkflowTitle] =
        useState("");

    const [workflowDescription, setWorkflowDescription] =
        useState("");

    const [workflowSteps, setWorkflowSteps] =
        useState("3");


    /* =========================
       OPEN FORM FROM DASHBOARD
    ========================= */

    useEffect(() => {
        if (searchParams.get("create") === "true") {
            setShowForm(true);

            setSearchParams({}, { replace: true });
        }
    }, [searchParams, setSearchParams]);


    /* =========================
       CREATE WORKFLOW
    ========================= */

    const addWorkflow = () => {
        if (!workflowTitle.trim()) {
            alert("Please enter a workflow name.");
            return;
        }

        const steps = Number(workflowSteps);

        if (!steps || steps < 1) {
            alert("Please enter a valid number of steps.");
            return;
        }

        const newWorkflow = {
            id: Date.now(),
            title: workflowTitle.trim(),
            description:
                workflowDescription.trim() ||
                "Custom Zarvis workflow",
            steps: steps,
            lastRun: "Not run yet",
            status: "Active",
        };

        setWorkflows((currentWorkflows) => [
            ...currentWorkflows,
            newWorkflow,
        ]);

        setWorkflowTitle("");
        setWorkflowDescription("");
        setWorkflowSteps("3");
        setShowForm(false);
    };


    /* =========================
       CLOSE FORM
    ========================= */

    const closeForm = () => {
        setShowForm(false);
        setWorkflowTitle("");
        setWorkflowDescription("");
        setWorkflowSteps("3");
    };


    /* =========================
       RUN WORKFLOW
    ========================= */

    const handleRun = (id) => {
        if (runningWorkflow !== null) return;

        setRunningWorkflow(id);

        setWorkflows((currentWorkflows) =>
            currentWorkflows.map((workflow) =>
                workflow.id === id
                    ? {
                        ...workflow,
                        status: "Running",
                        lastRun: "Running now",
                    }
                    : workflow
            )
        );

        setTimeout(() => {
            setRunningWorkflow(null);

            setWorkflows((currentWorkflows) =>
                currentWorkflows.map((workflow) =>
                    workflow.id === id
                        ? {
                            ...workflow,
                            status: "Active",
                            lastRun: "Just now",
                        }
                        : workflow
                )
            );
        }, 2000);
    };


    return (
        <div className="page-container">

            {/* =========================
          HEADER
      ========================= */}

            <div className="page-header">

                <div>

                    <span className="page-eyebrow">
                        ZARVIS AUTOMATION
                    </span>

                    <h1>
                        Workflows
                    </h1>

                    <p>
                        Automate routines and let Zarvis handle
                        repetitive work.
                    </p>

                </div>


                <button
                    type="button"
                    className="primary-action"
                    onClick={() => setShowForm(true)}
                >
                    <Plus size={18} />
                    Create Workflow
                </button>

            </div>


            {/* =========================
          STATS
      ========================= */}

            <div className="workflow-stats">

                <div className="glass-card page-stat">

                    <span>
                        Total Workflows
                    </span>

                    <strong>
                        {workflows.length}
                    </strong>

                </div>


                <div className="glass-card page-stat">

                    <span>
                        Active
                    </span>

                    <strong>
                        {
                            workflows.filter(
                                (workflow) =>
                                    workflow.status === "Active"
                            ).length
                        }
                    </strong>

                </div>


                <div className="glass-card page-stat">

                    <span>
                        Running
                    </span>

                    <strong>
                        {
                            workflows.filter(
                                (workflow) =>
                                    workflow.status === "Running"
                            ).length
                        }
                    </strong>

                </div>

            </div>


            {/* =========================
          CREATE WORKFLOW FORM
      ========================= */}

            {showForm && (
                <section className="glass-card workflow-form">

                    <div className="workflow-form-header">

                        <div>

                            <h2>
                                Create New Workflow
                            </h2>

                            <p>
                                Create a routine that Zarvis can
                                automate for you.
                            </p>

                        </div>


                        <button
                            type="button"
                            className="workflow-form-close"
                            onClick={closeForm}
                        >
                            <X size={17} />
                        </button>

                    </div>


                    <div className="workflow-form-grid">

                        {/* WORKFLOW NAME */}

                        <div className="workflow-field workflow-field-full">

                            <label>
                                Workflow Name
                            </label>

                            <input
                                type="text"
                                placeholder="e.g. Daily Study Routine"
                                value={workflowTitle}
                                onChange={(event) =>
                                    setWorkflowTitle(
                                        event.target.value
                                    )
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
                                value={workflowDescription}
                                onChange={(event) =>
                                    setWorkflowDescription(
                                        event.target.value
                                    )
                                }
                            />

                        </div>


                        {/* STEPS */}

                        <div className="workflow-field">

                            <label>
                                Number of Steps
                            </label>

                            <input
                                type="number"
                                min="1"
                                max="20"
                                value={workflowSteps}
                                onChange={(event) =>
                                    setWorkflowSteps(
                                        event.target.value
                                    )
                                }
                            />

                        </div>

                    </div>


                    {/* FORM ACTIONS */}

                    <div className="workflow-form-actions">

                        <button
                            type="button"
                            className="workflow-cancel"
                            onClick={closeForm}
                        >
                            Cancel
                        </button>


                        <button
                            type="button"
                            className="primary-action"
                            onClick={addWorkflow}
                        >
                            <Plus size={17} />
                            Create Workflow
                        </button>

                    </div>

                </section>
            )}


            {/* =========================
          WORKFLOW LIST
      ========================= */}

            <section className="glass-card workflows-page-card">

                <div className="card-header">

                    <div>

                        <h2>
                            My Workflows
                        </h2>

                        <p>
                            Your automated routines
                        </p>

                    </div>


                    <span className="card-count">
                        {workflows.length} Workflows
                    </span>

                </div>


                <div className="workflows-page-list">

                    {workflows.map((workflow) => (

                        <div
                            className="workflow-page-item"
                            key={workflow.id}
                        >

                            {/* ICON */}

                            <div className="workflow-page-icon">
                                <Workflow size={21} />
                            </div>


                            {/* INFO */}

                            <div className="workflow-page-info">

                                <div className="workflow-page-title">

                                    <strong>
                                        {workflow.title}
                                    </strong>

                                    <span
                                        className={`workflow-status ${workflow.status === "Running"
                                                ? "running"
                                                : workflow.status === "Paused"
                                                    ? "paused"
                                                    : ""
                                            }`}
                                    >
                                        {workflow.status}
                                    </span>

                                </div>


                                <p>
                                    {workflow.description}
                                </p>


                                <div className="workflow-page-meta">

                                    <span>
                                        <Workflow size={12} />
                                        {workflow.steps} Steps
                                    </span>

                                    <span>
                                        <Clock3 size={12} />
                                        {workflow.lastRun}
                                    </span>

                                </div>

                            </div>


                            {/* RUN */}

                            <button
                                type="button"
                                className={`workflow-run ${runningWorkflow === workflow.id
                                        ? "running"
                                        : ""
                                    }`}
                                onClick={() =>
                                    handleRun(workflow.id)
                                }
                                disabled={
                                    runningWorkflow !== null
                                }
                            >

                                {runningWorkflow === workflow.id ? (
                                    <>
                                        <Clock3 size={16} />
                                        Running
                                    </>
                                ) : (
                                    <>
                                        <Play size={16} />
                                        Run
                                    </>
                                )}

                            </button>


                            {/* MORE */}

                            <button
                                type="button"
                                className="workflow-more"
                                title="More options"
                            >
                                <MoreHorizontal size={19} />
                            </button>

                        </div>

                    ))}

                </div>

            </section>


            {/* =========================
          INFO
      ========================= */}

            <div className="workflow-info">

                <CheckCircle2 size={17} />

                <span>
                    Workflows are currently running with
                    frontend demo data. Real automation will
                    be connected when Zarvis gets its backend.
                </span>

            </div>

        </div>
    );
}

export default Workflows;