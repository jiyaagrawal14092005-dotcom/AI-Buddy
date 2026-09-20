import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    CalendarDays,
    Clock3,
    ArrowUpRight,
} from "lucide-react";

import { useAuth } from "../../context/AuthContext";
import { getScheduledJobs } from "../../services/schedulerService";

function ScheduleCard() {
    const navigate = useNavigate();
    const { user, authenticated } = useAuth();

    const [schedule, setSchedule] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadSchedule = async () => {
            if (!authenticated || !user?.id) {
                setSchedule([]);
                setLoading(false);
                return;
            }

            try {
                setLoading(true);

                const result = await getScheduledJobs(user.id);

                const jobs = Array.isArray(result?.jobs)
                    ? result.jobs
                    : [];

                const activeJobs = jobs
                    .filter(
                        (job) =>
                            job.status === "scheduled" ||
                            job.status === "SCHEDULED"
                    )
                    .sort(
                        (a, b) =>
                            new Date(a.schedule) -
                            new Date(b.schedule)
                    )
                    .slice(0, 3);

                setSchedule(activeJobs);
            } catch (error) {
                console.error(
                    "Failed to load dashboard schedule:",
                    error
                );

                setSchedule([]);
            } finally {
                setLoading(false);
            }
        };

        loadSchedule();
    }, [authenticated, user?.id]);

    const formatTime = (scheduleDate) => {
        if (!scheduleDate) {
            return "--:--";
        }

        const date = new Date(scheduleDate);

        if (Number.isNaN(date.getTime())) {
            return "--:--";
        }

        return date.toLocaleTimeString("en-IN", {
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    const getCategory = (name) => {
        const title = String(name || "").toLowerCase();

        if (
            title.includes("learn") ||
            title.includes("study") ||
            title.includes("class")
        ) {
            return "LEARNING";
        }

        if (
            title.includes("project") ||
            title.includes("ai buddy") ||
            title.includes("development")
        ) {
            return "PROJECT";
        }

        return "SCHEDULED";
    };

    return (
        <section className="schedule-system">
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

                <button
                    type="button"
                    className="schedule-view-all"
                    onClick={() => navigate("/schedule")}
                >
                    VIEW ALL
                    <ArrowUpRight size={13} />
                </button>
            </div>

            <div className="schedule-status">
                <span>
                    <i></i>
                    TODAY
                </span>

                <span>
                    {loading
                        ? "LOADING..."
                        : `${schedule.length
                        .toString()
                        .padStart(2, "0")} EVENTS`}
                </span>

                <strong>
                    {loading
                        ? "SYNCING"
                        : schedule.length > 0
                            ? "ON TRACK"
                            : "NO EVENTS"}
                </strong>
            </div>

            <div className="schedule-list">
                {loading ? (
                    <div className="schedule-item">
                        <div className="schedule-time">
                            <Clock3 size={13} />
                            <span>--:--</span>
                        </div>

                        <div className="schedule-details">
                            <h4>Loading schedule...</h4>
                            <span>SYNCING</span>
                        </div>

                        <div className="schedule-marker">
                            <i></i>
                        </div>
                    </div>
                ) : schedule.length === 0 ? (
                    <div className="schedule-item">
                        <div className="schedule-time">
                            <Clock3 size={13} />
                            <span>--:--</span>
                        </div>

                        <div className="schedule-details">
                            <h4>No upcoming events</h4>
                            <span>ADD FROM SCHEDULE</span>
                        </div>

                        <div className="schedule-marker">
                            <i></i>
                        </div>
                    </div>
                ) : (
                    schedule.map((item) => (
                        <div
                            className="schedule-item"
                            key={item.id}
                        >
                            <div className="schedule-time">
                                <Clock3 size={13} />
                                <span>
                                    {formatTime(item.schedule)}
                                </span>
                            </div>

                            <div className="schedule-details">
                                <h4>{item.name}</h4>

                                <span>
                                    {getCategory(item.name)}
                                </span>
                            </div>

                            <div className="schedule-marker">
                                <i></i>
                            </div>
                        </div>
                    ))
                )}
            </div>

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