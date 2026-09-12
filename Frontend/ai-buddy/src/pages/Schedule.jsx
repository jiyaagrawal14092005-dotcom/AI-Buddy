import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
    CalendarDays,
    Clock3,
    Plus,
    CheckCircle2,
    X,
} from "lucide-react";

function Schedule() {
    const [searchParams, setSearchParams] = useSearchParams();

    const [schedule, setSchedule] = useState([
        {
            id: 1,
            time: "09:00 AM",
            title: "Morning Planning",
            description: "Review goals and organize your day",
            type: "Planning",
        },
        {
            id: 2,
            time: "11:00 AM",
            title: "Project Development",
            description: "Work on your current project",
            type: "Work",
        },
        {
            id: 3,
            time: "02:00 PM",
            title: "Study Session",
            description: "Review notes and learn something new",
            type: "Study",
        },
        {
            id: 4,
            time: "05:00 PM",
            title: "Task Review",
            description: "Check completed and pending tasks",
            type: "Review",
        },
    ]);

    const [showForm, setShowForm] = useState(
        searchParams.get("create") === "true"
    );

    const [eventTitle, setEventTitle] = useState("");
    const [eventTime, setEventTime] = useState("");
    const [eventDescription, setEventDescription] = useState("");

    useEffect(() => {
        if (searchParams.get("create") === "true") {
            setShowForm(true);
            setSearchParams({}, { replace: true });
        }
    }, [searchParams, setSearchParams]);

    const formatTime = (time) => {
        if (!time) return "";

        const [hours, minutes] = time.split(":");

        let hour = Number(hours);

        const period = hour >= 12 ? "PM" : "AM";

        hour = hour % 12 || 12;

        return `${String(hour).padStart(2, "0")}:${minutes} ${period}`;
    };

    const addEvent = () => {
        if (!eventTitle.trim()) {
            alert("Please enter an event name.");
            return;
        }

        if (!eventTime) {
            alert("Please select a time.");
            return;
        }

        const newEvent = {
            id: Date.now(),
            time: formatTime(eventTime),
            title: eventTitle.trim(),
            description:
                eventDescription.trim() || "Scheduled activity",
            type: "Personal",
        };

        setSchedule((currentSchedule) => [
            ...currentSchedule,
            newEvent,
        ]);

        setEventTitle("");
        setEventTime("");
        setEventDescription("");
        setShowForm(false);
    };

    const closeForm = () => {
        setShowForm(false);
        setEventTitle("");
        setEventTime("");
        setEventDescription("");
    };

    return (
        <div className="page-container">

            {/* HEADER */}
            <div className="page-header">

                <div>
                    <span className="page-eyebrow">
                        ZARVIS SCHEDULE
                    </span>

                    <h1>Schedule</h1>

                    <p>
                        Organize your time and stay on track.
                    </p>
                </div>

                <button
                    type="button"
                    className="primary-action"
                    onClick={() => setShowForm(true)}
                >
                    <Plus size={18} />
                    Add Event
                </button>

            </div>

            {/* DATE CARD */}
            <div className="schedule-date glass-card">

                <div className="schedule-date-icon">
                    <CalendarDays size={21} />
                </div>

                <div>
                    <strong>Today</strong>

                    <span>
                        Thursday, September 11
                    </span>
                </div>

                <div className="schedule-date-status">
                    <CheckCircle2 size={16} />
                    Zarvis is keeping you on track
                </div>

            </div>

            {/* ADD EVENT FORM */}
            {showForm && (
                <section className="glass-card event-form">

                    <div className="event-form-header">

                        <div>
                            <h2>Add New Event</h2>

                            <p>
                                Add an event to your Zarvis schedule.
                            </p>
                        </div>

                        <button
                            type="button"
                            className="event-form-close"
                            onClick={closeForm}
                        >
                            <X size={17} />
                        </button>

                    </div>

                    <div className="event-form-grid">

                        {/* EVENT NAME */}
                        <div className="event-field event-field-full">

                            <label>
                                Event Name
                            </label>

                            <input
                                type="text"
                                placeholder="e.g. Team meeting"
                                value={eventTitle}
                                onChange={(event) =>
                                    setEventTitle(event.target.value)
                                }
                            />

                        </div>

                        {/* TIME */}
                        <div className="event-field">

                            <label>
                                Time
                            </label>

                            <input
                                type="time"
                                value={eventTime}
                                onChange={(event) =>
                                    setEventTime(event.target.value)
                                }
                            />

                        </div>

                        {/* DESCRIPTION */}
                        <div className="event-field">

                            <label>
                                Description
                            </label>

                            <input
                                type="text"
                                placeholder="Optional"
                                value={eventDescription}
                                onChange={(event) =>
                                    setEventDescription(event.target.value)
                                }
                            />

                        </div>

                    </div>

                    {/* ACTIONS */}
                    <div className="event-form-actions">

                        <button
                            type="button"
                            className="event-cancel"
                            onClick={closeForm}
                        >
                            Cancel
                        </button>

                        <button
                            type="button"
                            className="primary-action"
                            onClick={addEvent}
                        >
                            <Plus size={17} />
                            Add Event
                        </button>

                    </div>

                </section>
            )}

            {/* TIMELINE */}
            <section className="glass-card schedule-page-card">

                <div className="card-header">

                    <div>
                        <h2>
                            Today's Schedule
                        </h2>

                        <p>
                            Your planned activities
                        </p>
                    </div>

                    <span className="card-count">
                        {schedule.length} Events
                    </span>

                </div>

                <div className="schedule-timeline">

                    {schedule.map((item, index) => (

                        <div
                            className="schedule-page-item"
                            key={item.id}
                        >

                            {/* TIME */}
                            <div className="schedule-time">
                                {item.time}
                            </div>

                            {/* TIMELINE */}
                            <div className="schedule-line">

                                <span className="schedule-dot"></span>

                                {index !== schedule.length - 1 && (
                                    <span className="schedule-connector"></span>
                                )}

                            </div>

                            {/* EVENT */}
                            <div className="schedule-event">

                                <div className="schedule-event-top">

                                    <strong>
                                        {item.title}
                                    </strong>

                                    <span className="schedule-type">
                                        {item.type}
                                    </span>

                                </div>

                                <p>
                                    {item.description}
                                </p>

                                <span className="schedule-duration">

                                    <Clock3 size={12} />

                                    Planned activity

                                </span>

                            </div>

                        </div>

                    ))}

                </div>

            </section>

        </div>
    );
}

export default Schedule;