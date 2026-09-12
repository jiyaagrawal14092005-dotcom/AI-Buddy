import { useState } from "react";
import {
  Plus,
  Workflow as WorkflowIcon,
  Play,
  Pause,
  Trash2,
  Clock3,
  CheckCircle2,
  Zap,
  ArrowRight,
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const initialWorkflows = [
  {
    id: 1,
    name: "Morning Routine",
    description: "Start the day with a productive routine.",
    status: "ACTIVE",
    steps: [
      "Wake up reminder",
      "Review today's schedule",
      "Start focus session",
    ],
    lastRun: "Today, 06:00 AM",
  },
  {
    id: 2,
    name: "Study Session",
    description: "Prepare and start a focused study block.",
    status: "READY",
    steps: [
      "Open study task",
      "Start 25 min timer",
      "Review progress",
    ],
    lastRun: "Yesterday, 04:00 PM",
  },
  {
    id: 3,
    name: "Evening Planning",
    description: "Prepare tomorrow's tasks and schedule.",
    status: "READY",
    steps: [
      "Review completed tasks",
      "Plan tomorrow",
      "Create reminders",
    ],
    lastRun: "Yesterday, 08:30 PM",
  },
];

function Workflows() {
  const [workflows, setWorkflows] =
    useState(initialWorkflows);

  const [showForm, setShowForm] =
    useState(false);

  const [newWorkflow, setNewWorkflow] =
    useState({
      name: "",
      description: "",
      steps: "",
    });

  const toggleWorkflow = (id) => {
    setWorkflows((prev) =>
      prev.map((workflow) =>
        workflow.id === id
          ? {
            ...workflow,
            status:
              workflow.status === "ACTIVE"
                ? "READY"
                : "ACTIVE",
          }
          : workflow
      )
    );
  };

  const deleteWorkflow = (id) => {
    setWorkflows((prev) =>
      prev.filter(
        (workflow) => workflow.id !== id
      )
    );
  };

  const runWorkflow = (id) => {
    setWorkflows((prev) =>
      prev.map((workflow) =>
        workflow.id === id
          ? {
            ...workflow,
            status: "ACTIVE",
            lastRun: "Just now",
          }
          : workflow
      )
    );
  };

  const createWorkflow = (event) => {
    event.preventDefault();

    if (!newWorkflow.name.trim()) {
      return;
    }

    const steps = newWorkflow.steps
      .split(",")
      .map((step) => step.trim())
      .filter(Boolean);

    const workflow = {
      id: Date.now(),
      name: newWorkflow.name,
      description:
        newWorkflow.description ||
        "Custom workflow created with Zarvis.",
      status: "READY",
      steps:
        steps.length > 0
          ? steps
          : ["New workflow step"],
      lastRun: "Never",
    };

    setWorkflows((prev) => [
      workflow,
      ...prev,
    ]);

    setNewWorkflow({
      name: "",
      description: "",
      steps: "",
    });

    setShowForm(false);
  };

  const activeCount = workflows.filter(
    (workflow) =>
      workflow.status === "ACTIVE"
  ).length;

  const readyCount = workflows.filter(
    (workflow) =>
      workflow.status === "READY"
  ).length;

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
              onClick={() =>
                setShowForm(!showForm)
              }
            >
              <Plus size={18} />
              Create Workflow
            </button>

          </section>


          {/* STATS */}
          <section className="workflow-stats">

            <div className="workflow-stat-card">

              <span>
                TOTAL WORKFLOWS
              </span>

              <strong>
                {workflows.length}
              </strong>

            </div>


            <div className="workflow-stat-card">

              <span>
                ACTIVE
              </span>

              <strong>
                {activeCount}
              </strong>

            </div>


            <div className="workflow-stat-card">

              <span>
                READY
              </span>

              <strong>
                {readyCount}
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
              onSubmit={createWorkflow}
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
                >
                  ×
                </button>

              </div>


              <div className="workflow-form-grid">

                <div className="workflow-field">

                  <label>
                    Workflow Name
                  </label>

                  <input
                    type="text"
                    placeholder="e.g. Morning Routine"
                    value={newWorkflow.name}
                    onChange={(e) =>
                      setNewWorkflow({
                        ...newWorkflow,
                        name: e.target.value,
                      })
                    }
                  />

                </div>


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
                    onChange={(e) =>
                      setNewWorkflow({
                        ...newWorkflow,
                        description:
                          e.target.value,
                      })
                    }
                  />

                </div>


                <div className="workflow-field workflow-field-wide">

                  <label>
                    Steps
                  </label>

                  <input
                    type="text"
                    placeholder="Step 1, Step 2, Step 3"
                    value={newWorkflow.steps}
                    onChange={(e) =>
                      setNewWorkflow({
                        ...newWorkflow,
                        steps: e.target.value,
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
              >
                <Plus size={16} />
                CREATE WORKFLOW
              </button>

            </form>
          )}


          {/* WORKFLOW LIST */}
          <section className="workflow-list-panel">

            <div className="workflow-list-header">

              <div>

                <span>
                  AUTOMATION QUEUE // 03
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

              {workflows.length === 0 ? (

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

                workflows.map((workflow) => (

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
                        className={`workflow-status ${workflow.status ===
                            "ACTIVE"
                            ? "workflow-active"
                            : "workflow-ready"
                          }`}
                      >

                        <span></span>

                        {workflow.status}

                      </div>

                    </div>


                    {/* STEPS */}
                    <div className="workflow-steps">

                      <div className="workflow-steps-label">
                        WORKFLOW STEPS
                      </div>

                      <div className="workflow-step-list">

                        {workflow.steps.map(
                          (step, index) => (

                            <div
                              className="workflow-step"
                              key={index}
                            >

                              <div className="workflow-step-number">
                                {String(
                                  index + 1
                                ).padStart(2, "0")}
                              </div>

                              <span>
                                {step}
                              </span>

                              {index <
                                workflow.steps.length -
                                1 && (
                                  <ArrowRight
                                    size={13}
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
                          onClick={() =>
                            runWorkflow(
                              workflow.id
                            )
                          }
                        >
                          <Play size={14} />
                          RUN
                        </button>


                        <button
                          type="button"
                          className="workflow-toggle-button"
                          onClick={() =>
                            toggleWorkflow(
                              workflow.id
                            )
                          }
                        >
                          {workflow.status ===
                            "ACTIVE" ? (
                            <>
                              <Pause
                                size={14}
                              />
                              PAUSE
                            </>
                          ) : (
                            <>
                              <CheckCircle2
                                size={14}
                              />
                              ENABLE
                            </>
                          )}
                        </button>


                        <button
                          type="button"
                          className="workflow-delete-button"
                          onClick={() =>
                            deleteWorkflow(
                              workflow.id
                            )
                          }
                          title="Delete workflow"
                        >
                          <Trash2 size={15} />
                        </button>

                      </div>

                    </div>

                  </article>

                ))

              )}

            </div>

          </section>

        </div>

      </main>

    </div>
  );
}

export default Workflows;