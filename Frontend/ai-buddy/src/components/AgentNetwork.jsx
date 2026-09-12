import {
    Brain,
    ListTodo,
    Search,
    CalendarDays,
    Zap,
    ShieldCheck,
} from "lucide-react";

const agents = [
    { name: "Planner", icon: Brain, position: "agent-1", status: "ACTIVE" },
    { name: "Tasks", icon: ListTodo, position: "agent-2", status: "READY" },
    { name: "Research", icon: Search, position: "agent-3", status: "READY" },
    { name: "Schedule", icon: CalendarDays, position: "agent-4", status: "READY" },
    { name: "Automation", icon: Zap, position: "agent-5", status: "READY" },
    { name: "Security", icon: ShieldCheck, position: "agent-6", status: "READY" },
];

function AgentNetwork() {
    return (
        <section className="zarvis-agent-panel">

            <div className="zarvis-agent-header">
                <div>
                    <span className="zarvis-agent-label">ZARVIS INTELLIGENCE</span>
                    <h2>Agent Network</h2>
                    <p>One core. Multiple specialized agents.</p>
                </div>

                <div className="zarvis-online">
                    <span />
                    ALL SYSTEMS ONLINE
                </div>
            </div>

            <div className="zarvis-agent-stage">

                {/* subtle connection structure */}
                <div className="agent-line line-1" />
                <div className="agent-line line-2" />
                <div className="agent-line line-3" />
                <div className="agent-line line-4" />
                <div className="agent-line line-5" />
                <div className="agent-line line-6" />

                {/* central core */}
                <div className="zarvis-main-core">

                    <div className="core-aura" />

                    <div className="core-ring" />

                    <div className="core-content">
                        <Brain size={25} />
                        <strong>ZARVIS</strong>
                        <small>AI CORE</small>
                    </div>

                </div>

                {/* agents */}
                {agents.map((agent) => {
                    const Icon = agent.icon;

                    return (
                        <div
                            className={`zarvis-agent-card ${agent.position}`}
                            key={agent.name}
                        >
                            <div className="agent-icon">
                                <Icon size={17} />
                            </div>

                            <div className="agent-details">
                                <strong>{agent.name}</strong>

                                <span>
                                    <i />
                                    {agent.status}
                                </span>
                            </div>
                        </div>
                    );
                })}

            </div>

            <div className="zarvis-agent-footer">
                <span>
                    <i />
                    06 AGENTS CONNECTED
                </span>

                <span>REAL-TIME COORDINATION</span>

                <span>LATENCY 12ms</span>
            </div>

        </section>
    );
}

export default AgentNetwork;