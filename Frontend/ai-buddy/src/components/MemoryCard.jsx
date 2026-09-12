import {
    Brain,
    User,
    Clock3,
    Database,
} from "lucide-react";

const memories = [
    {
        icon: User,
        label: "PREFERENCE",
        text: "Prefers focused study sessions",
    },
    {
        icon: Clock3,
        label: "ROUTINE",
        text: "Usually productive in the morning",
    },
    {
        icon: Database,
        label: "CONTEXT",
        text: "Working on Zarvis project",
    },
];

function MemoryCard() {
    return (
        <section className="memory-system">

            {/* HEADER */}
            <div className="memory-header">

                <div className="memory-heading">
                    <div className="memory-icon">
                        <Brain size={17} />
                    </div>

                    <div>
                        <span>MEMORY MODULE // 07</span>
                        <h3>MEMORY CORE</h3>
                    </div>
                </div>

                <div className="memory-status">
                    <span></span>
                    ACTIVE
                </div>

            </div>

            {/* STATUS BAR */}
            <div className="memory-status-bar">
                <span>PERSONAL CONTEXT</span>
                <strong>SYNCED</strong>
            </div>

            {/* MEMORY LIST */}
            <div className="memory-list">

                {memories.map((memory, index) => {
                    const Icon = memory.icon;

                    return (
                        <div className="memory-item" key={index}>

                            <div className="memory-item-icon">
                                <Icon size={14} />
                            </div>

                            <div className="memory-content">
                                <span>{memory.label}</span>
                                <p>{memory.text}</p>
                            </div>

                            <div className="memory-indicator">
                                ●
                            </div>

                        </div>
                    );
                })}

            </div>

            {/* FOOTER */}
            <div className="memory-footer">

                <span>
                    <i></i>
                    ZARVIS MEMORY ENGINE
                </span>

                <span>03 ENTRIES</span>

            </div>

        </section>
    );
}

export default MemoryCard;