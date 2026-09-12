import {
    CalendarDays,
    Clock3,
    ArrowUpRight,
} from "lucide-react";

const schedule = [
    {
        time: "10:30 AM",
        title: "React Learning",
        category: "LEARNING",
    },
    {
        time: "02:30 PM",
        title: "Work on Zarvis UI",
        category: "PROJECT",
    },
    {
        time: "05:00 PM",
        title: "Review Progress",
        category: "PRODUCTIVITY",
    },
];

function ScheduleCard() {
    return (
        <section className="schedule-system">

            {/* HEADER */}
            <div className="schedule-header">

                <div className="schedule-heading">
                    <div className="schedule-icon">
                        <CalendarDays size={17} />
                    </div>

                    <div>
                        <span>SCHEDULE MODULE // 03</span>
                        <h3>TODAY'S SCHEDULE</h3>
                    </div>
                </div>

                <button className="schedule-view-all">
                    VIEW ALL
                    <ArrowUpRight size={13} />
                </button>

            </div>

            {/* STATUS */}
            <div className="schedule-status">
                <span>
                    <i></i>
                    TODAY
                </span>

                <span>03 EVENTS</span>

                <strong>ON TRACK</strong>
            </div>

            {/* SCHEDULE LIST */}
            <div className="schedule-list">

                {schedule.map((item, index) => (
                    <div
                        className="schedule-item"
                        key={index}
                    >

                        {/* TIME */}
                        <div className="schedule-time">
                            <Clock3 size={13} />
                            <span>{item.time}</span>
                        </div>

                        {/* DETAILS */}
                        <div className="schedule-details">
                            <h4>{item.title}</h4>

                            <span>
                                {item.category}
                            </span>
                        </div>

                        {/* STATUS */}
                        <div className="schedule-marker">
                            <i></i>
                        </div>

                    </div>
                ))}

            </div>

            {/* FOOTER */}
            <div className="schedule-footer">

                <span>
                    <i></i>
                    ZARVIS SCHEDULE ENGINE
                </span>

                <span>SYNCED</span>

            </div>

        </section>
    );
}

export default ScheduleCard;