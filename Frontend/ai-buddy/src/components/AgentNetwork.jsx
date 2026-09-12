import {
    Network,
    Brain,
    Search,
    Zap,
    CheckCircle2,
} from "lucide-react";

const agents = [
    {
        name: "Planner",
        role: "TASK PLANNING",
        icon: Brain,
        status: "ACTIVE",
        load: "84%",
    },
    {
        name: "Research",
        role: "INFORMATION",
        icon: Search,
        status: "READY",
        load: "42%",
    },
    {
        name: "Executor",
        role: "TASK EXECUTION",
        icon: Zap,
        status: "READY",
        load: "28%",
    },
];

function AgentNetwork() {
    return (
        <section className="agent-network">

            <div className="agent-network-header">

                <div className="agent-network-title">

                    <div className="agent-network-icon">
                        <Network size={17} />
                    </div>

                    <div>
                        <span>AI SYSTEM // 06</span>
                        <h2>Agent Network</h2>
                    </div>

                </div>

                <div className="agent-network-status">
                    <span></span>
                    NETWORK STABLE
                </div>

            </div>

            <div className="agent-network-line">
                <span></span>
            </div>

            <div className="agent-network-body">

                <div className="network-core">

                    <div className="network-ring network-ring-one"></div>
                    <div className="network-ring network-ring-two"></div>

                    <div className="network-core-center">
                        <span>Z</span>
                    </div>

                    <div className="network-core-label">
                        ZARVIS CORE
                    </div>

                </div>

                <div className="agent-list">

                    {agents.map((agent, index) => {

                        const Icon = agent.icon;

                        return (
                            <div
                                className="agent-item"
                                key={agent.name}
                            >

                                <div className="agent-item-icon">
                                    <Icon size={15} />
                                </div>

                                <div className="agent-item-info">

                                    <div className="agent-item-name">
                                        <strong>{agent.name}</strong>

                                        <span
                                            className={
                                                agent.status === "ACTIVE"
                                                    ? "agent-active"
                                                    : "agent-ready"
                                            }
                                        >
                                            <i></i>
                                            {agent.status}
                                        </span>
                                    </div>

                                    <span className="agent-item-role">
                                        {agent.role}
                                    </span>

                                </div>

                                <div className="agent-load">

                                    <div className="agent-load-bar">
                                        <span
                                            style={{
                                                width: agent.load,
                                            }}
                                        ></span>
                                    </div>

                                    <small>{agent.load}</small>

                                </div>

                            </div>
                        );
                    })}

                </div>

            </div>

            <div className="agent-network-footer">

                <div>
                    <CheckCircle2 size={13} />
                    <span>3 AGENTS AVAILABLE</span>
                </div>

                <span>
                    REAL-TIME PROCESSING
                </span>

            </div>

        </section>
    );
}

export default AgentNetwork;