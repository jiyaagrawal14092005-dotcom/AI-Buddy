import {
    Activity,
    CheckCircle2,
    Zap,
    Clock3,
} from "lucide-react";

const activities = [
    {
        icon: CheckCircle2,
        title: "Task completed",
        text: "React module completed",
        time: "09:42",
        type: "SUCCESS",
    },
    {
        icon: Zap,
        title: "Workflow executed",
        text: "Daily planning workflow",
        time: "09:15",
        type: "AI",
    },
    {
        icon: Clock3,
        title: "Focus session",
        text: "25 minute session started",
        time: "08:50",
        type: "FOCUS",
    },
];

function ActivityCard() {
    return (
        <section className="activity-system">

            {/* HEADER */}
            <div className="activity-header">

                <div className="activity-heading">
                    <div className="activity-icon">
                        <Activity size={17} />
                    </div>

                    <div>
                        <span>MONITOR // 06</span>
                        <h3>ACTIVITY</h3>
                    </div>
                </div>

                <div className="activity-live">
                    <span></span>
                    LIVE
                </div>

            </div>

            {/* STATUS */}
            <div className="activity-status">
                <span>SYSTEM ACTIVITY</span>
                <strong>REAL-TIME</strong>
            </div>

            {/* ACTIVITY LIST */}
            <div className="activity-list">

                {activities.map((item, index) => {
                    const Icon = item.icon;

                    return (
                        <div className="activity-item" key={index}>

                            <div className="activity-marker">
                                <Icon size={14} />
                            </div>

                            <div className="activity-content">
                                <div className="activity-title-row">
                                    <h4>{item.title}</h4>

                                    <span className={`activity-type type-${item.type.toLowerCase()}`}>
                                        {item.type}
                                    </span>
                                </div>

                                <p>{item.text}</p>
                            </div>

                            <span className="activity-time">
                                {item.time}
                            </span>

                        </div>
                    );
                })}

            </div>

            {/* FOOTER */}
            <div className="activity-footer">
                <span>
                    <i></i>
                    ZARVIS MONITOR
                </span>

                <span>03 EVENTS</span>
            </div>

        </section>
    );
}

export default ActivityCard;