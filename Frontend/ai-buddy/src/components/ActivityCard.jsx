import {
    Activity,
    CheckCircle2,
    Zap,
    MessageCircle,
    Clock3,
} from "lucide-react";

const activities = [
    {
        icon: CheckCircle2,
        title: "Task completed",
        text: "AI assignment marked complete",
        time: "8 min ago",
        type: "success",
    },
    {
        icon: Zap,
        title: "Workflow executed",
        text: "Morning routine completed",
        time: "32 min ago",
        type: "purple",
    },
    {
        icon: MessageCircle,
        title: "Zarvis interaction",
        text: "Planning assistant activated",
        time: "1 hr ago",
        type: "cyan",
    },
    {
        icon: Clock3,
        title: "Focus session",
        text: "25 minute session started",
        time: "2 hrs ago",
        type: "pink",
    },
];

function ActivityCard() {
    return (
        <section className="dashboard-module activity-module">

            <div className="module-header">

                <div className="module-title">

                    <div className="module-icon module-icon-purple">
                        <Activity size={16} />
                    </div>

                    <div>
                        <span className="module-label">
                            ACTIVITY SYSTEM // 03
                        </span>

                        <h3>Recent Activity</h3>
                    </div>

                </div>

                <div className="activity-live">
                    <span></span>
                    LIVE
                </div>

            </div>

            <div className="module-line">
                <span></span>
            </div>

            <div className="activity-list">

                {activities.map((activity, index) => {

                    const Icon = activity.icon;

                    return (
                        <div
                            className="activity-row"
                            key={index}
                        >

                            <div
                                className={`activity-icon activity-${activity.type}`}
                            >
                                <Icon size={13} />
                            </div>

                            <div className="activity-content">

                                <strong>
                                    {activity.title}
                                </strong>

                                <span>
                                    {activity.text}
                                </span>

                            </div>

                            <time>
                                {activity.time}
                            </time>

                        </div>
                    );
                })}

            </div>

            <button
                type="button"
                className="module-footer-button"
            >
                <span>VIEW ACTIVITY LOG</span>
                <Activity size={13} />
            </button>

        </section>
    );
}

export default ActivityCard;