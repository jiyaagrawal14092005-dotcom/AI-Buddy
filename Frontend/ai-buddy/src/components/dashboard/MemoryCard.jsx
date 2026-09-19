import { useNavigate } from "react-router-dom";

import {
    Brain,
    UserRound,
    BookOpen,
    Sparkles,
    ArrowUpRight,
} from "lucide-react";

const memories = [
    {
        icon: UserRound,
        title: "User preference",
        text: "Prefers focused study sessions",
    },
    {
        icon: BookOpen,
        title: "Learning goal",
        text: "Currently learning Machine Learning",
    },
    {
        icon: Sparkles,
        title: "AI preference",
        text: "Likes simple explanations",
    },
];

function MemoryCard() {
    const navigate = useNavigate();

    return (
        <section className="dashboard-module memory-module">

            <div className="module-header">

                <div className="module-title">

                    <div className="module-icon module-icon-cyan">
                        <Brain size={16} />
                    </div>

                    <div>
                        <span className="module-label">
                            MEMORY SYSTEM // 05
                        </span>

                        <h3>AI Memory Core</h3>
                    </div>

                </div>

                <div className="memory-count">
                    08
                </div>

            </div>

            <div className="module-line">
                <span></span>
            </div>

            <div className="memory-core-status">

                <div className="memory-pulse">
                    <span></span>
                </div>

                <div>
                    <strong>MEMORY ACTIVE</strong>
                    <small>Zarvis learning from your interactions</small>
                </div>

            </div>

            <div className="memory-list">

                {memories.map((memory, index) => {

                    const Icon = memory.icon;

                    return (
                        <div
                            className="memory-row"
                            key={index}
                        >

                            <div className="memory-icon">
                                <Icon size={13} />
                            </div>

                            <div className="memory-content">

                                <strong>
                                    {memory.title}
                                </strong>

                                <span>
                                    {memory.text}
                                </span>

                            </div>

                            <span className="memory-dot"></span>

                        </div>
                    );
                })}

            </div>

            <button
                type="button"
                className="module-footer-button"
                onClick={() => navigate("/memory")}
            >
                <span>OPEN MEMORY</span>
                <ArrowUpRight size={14} />
            </button>

        </section>
    );
}

export default MemoryCard;