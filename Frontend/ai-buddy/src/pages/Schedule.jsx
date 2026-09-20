// ==========================================
// AI BUDDY SCHEDULE PAGE
// ==========================================

import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";

import {
    Plus,
    CalendarDays,
    Clock3,
    MapPin,
    Trash2,
} from "lucide-react";

import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";
import Timer from "../components/scheduler/Timer";

import { useAuth } from "../context/AuthContext";
import {
    scheduleJob,
    getScheduledJobs,
    cancelJob,
} from "../services/schedulerService";

function Schedule() {
    const location = useLocation();
    const { user, authenticated } = useAuth();

    const [events, setEvents] = useState([]);

    const [newEvent, setNewEvent] = useState(
        location.state?.eventType === "travel"
            ? "Travel Plan"
            : ""
    );

    const [eventDate, setEventDate] = useState("");
    const [eventTime, setEventTime] = useState("");
    const [eventLocation, setEventLocation] = useState("");

    const [loading, setLoading] = useState(false);
    const [loadingEvents, setLoadingEvents] = useState(true);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const inputRef = useRef(null);


    // ==========================================
    // LOAD SCHEDULED EVENTS
    // ==========================================

    const loadEvents = async () => {
        if (!authenticated || !user?.id) {
            setLoadingEvents(false);
            return;
        }

        try {
            setLoadingEvents(true);
            setError("");

            const result = await getScheduledJobs(user.id);

            const jobs = Array.isArray(result?.jobs)
                ? result.jobs
                : [];

            const formattedEvents = jobs.map((job) => {
                let date = "Scheduled";
                let time = "Not specified";

                if (job.schedule) {
                    const scheduledDate =
                        new Date(job.schedule);

                    if (!Number.isNaN(
                        scheduledDate.getTime()
                    )) {
                        date =
                            scheduledDate.toLocaleDateString(
                                "en-IN",
                                {
                                    day: "2-digit",
                                    month: "short",
                                    year: "numeric",
                                }
                            );

                        time =
                            scheduledDate.toLocaleTimeString(
                                "en-IN",
                                {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                }
                            );
                    }
                }

                return {
                    id: job.id,
                    databaseId: job.id,
                    jobId: job.id,
                    title: job.name,
                    date,
                    time,
                    location: "Scheduled Event",
                    status: job.status,
                    schedule: job.schedule,
                };
            });

            setEvents(formattedEvents);
        } catch (requestError) {
            console.error(
                "Failed to load scheduled events:",
                requestError
            );

            setError(
                "Unable to load scheduled events."
            );
        } finally {
            setLoadingEvents(false);
        }
    };


    // ==========================================
    // INITIAL LOAD
    // ==========================================

    useEffect(() => {
        loadEvents();
    }, [authenticated, user?.id]);


    // ==========================================
    // FOCUS ADD EVENT INPUT
    // ==========================================

    const openAddEvent = () => {
        inputRef.current?.focus();
    };


    // ==========================================
    // ADD SCHEDULED EVENT
    // ==========================================

    const addEvent = async () => {
        const title = newEvent.trim();

        if (!title) {
            setError("Please enter an event name.");
            inputRef.current?.focus();
            return;
        }

        if (!eventDate) {
            setError("Please select a date.");
            return;
        }

        if (!eventTime) {
            setError("Please select a time.");
            return;
        }

        if (!authenticated || !user?.id) {
            setError(
                "Please login before creating a schedule."
            );
            return;
        }

        const selectedDateTime = new Date(
            `${eventDate}T${eventTime}`
        );

        const currentTime = new Date();

        const delaySeconds =
            (
                selectedDateTime.getTime() -
                currentTime.getTime()
            ) / 1000;

        if (delaySeconds <= 0) {
            setError(
                "Please select a future date and time."
            );
            return;
        }

        try {
            setLoading(true);
            setError("");
            setSuccess("");

            const result = await scheduleJob(
                user.id,
                delaySeconds,
                title
            );

            if (!result?.success) {
                throw new Error(
                    result?.message ||
                    "Unable to schedule event."
                );
            }

            setSuccess(
                "Event scheduled successfully."
            );

            setNewEvent("");
            setEventDate("");
            setEventTime("");
            setEventLocation("");

            await loadEvents();

            setTimeout(() => {
                inputRef.current?.focus();
            }, 0);

        } catch (requestError) {
            console.error(
                "Schedule creation failed:",
                requestError
            );

            setError(
                requestError?.message ||
                "Unable to schedule event."
            );
        } finally {
            setLoading(false);
        }
    };


    // ==========================================
    // CANCEL EVENT
    // ==========================================

    const deleteEvent = async (event) => {
        if (!event?.jobId) {
            return;
        }

        try {
            setError("");
            setSuccess("");

            if (
                event.status === "scheduled" ||
                event.status === "SCHEDULED"
            ) {
                await cancelJob(event.jobId);
            }

            await loadEvents();

            setSuccess(
                "Scheduled event cancelled."
            );

        } catch (requestError) {
            console.error(
                "Failed to cancel scheduled event:",
                requestError
            );

            setError(
                requestError?.message ||
                "Unable to cancel scheduled event."
            );
        }
    };


    // ==========================================
    // SUMMARY COUNTS
    // ==========================================

    const upcomingCount =
        events.filter(
            (event) =>
                event.status === "scheduled" ||
                event.status === "SCHEDULED"
        ).length;

    const onlineEvents = events.filter(
        (event) =>
            event.location === "Online" ||
            event.location === "Travel Plan"
    ).length;


    // ==========================================
    // RENDER
    // ==========================================

    return (
        <div className="app">
            <Sidebar />

            <main className="main-content">
                <Navbar />

                <div className="schedule-page">

                    {/* ==========================================
                        PAGE HEADER
                    ========================================== */}

                    <div className="page-header">
                        <div>
                            <span className="page-label">
                                ZARVIS PLANNER
                            </span>

                            <h1>Schedule</h1>

                            <p>
                                Organize your day and keep track
                                of what is coming next.
                            </p>
                        </div>

                        <button
                            type="button"
                            className="primary-action"
                            onClick={openAddEvent}
                        >
                            <Plus size={17} />
                            Add Event
                        </button>
                    </div>


                    {/* ==========================================
                        STATUS MESSAGES
                    ========================================== */}

                    {error && (
                        <div className="schedule-message schedule-error">
                            {error}
                        </div>
                    )}

                    {success && (
                        <div className="schedule-message schedule-success">
                            {success}
                        </div>
                    )}


                    {/* ==========================================
                        EVENT INPUT
                    ========================================== */}

                    <div className="schedule-input-card">

                        <CalendarDays size={19} />

                        <input
                            ref={inputRef}
                            type="text"
                            value={newEvent}
                            onChange={(event) =>
                                setNewEvent(
                                    event.target.value
                                )
                            }
                            onKeyDown={(event) => {
                                if (event.key === "Enter") {
                                    event.preventDefault();
                                }
                            }}
                            placeholder="What would you like to schedule?"
                        />

                    </div>


                    {/* ==========================================
                        DATE / TIME / LOCATION
                    ========================================== */}

                    <div className="schedule-input-card">

                        <CalendarDays size={18} />

                        <input
                            type="date"
                            value={eventDate}
                            onChange={(event) =>
                                setEventDate(
                                    event.target.value
                                )
                            }
                        />

                        <Clock3 size={18} />

                        <input
                            type="time"
                            value={eventTime}
                            onChange={(event) =>
                                setEventTime(
                                    event.target.value
                                )
                            }
                        />

                        <MapPin size={18} />

                        <input
                            type="text"
                            value={eventLocation}
                            onChange={(event) =>
                                setEventLocation(
                                    event.target.value
                                )
                            }
                            placeholder="Location"
                        />

                        <button
                            type="button"
                            onClick={addEvent}
                            disabled={loading}
                            aria-label="Schedule event"
                        >
                            <Plus size={18} />
                        </button>

                    </div>


                    {/* ==========================================
                        SUMMARY
                    ========================================== */}

                    <div className="schedule-summary">

                        <div className="schedule-stat">
                            <CalendarDays size={19} />

                            <div>
                                <strong>
                                    {events.length}
                                </strong>

                                <span>
                                    Scheduled Events
                                </span>
                            </div>
                        </div>


                        <div className="schedule-stat">
                            <Clock3 size={19} />

                            <div>
                                <strong>
                                    {upcomingCount}
                                </strong>

                                <span>
                                    Upcoming
                                </span>
                            </div>
                        </div>


                        <div className="schedule-stat">
                            <MapPin size={19} />

                            <div>
                                <strong>
                                    {onlineEvents}
                                </strong>

                                <span>
                                    Online / Travel
                                </span>
                            </div>
                        </div>

                    </div>


                    {/* ==========================================
                        TIMER
                    ========================================== */}

                    <section className="schedule-timer-section">
                        <Timer />
                    </section>


                    {/* ==========================================
                        TODAY'S SCHEDULE
                    ========================================== */}

                    <section className="schedule-section">

                        <div className="section-heading">

                            <div>
                                <h2>
                                    Scheduled Events
                                </h2>

                                <p>
                                    Your planned events and activities.
                                </p>
                            </div>

                            <span>
                                {events.length} events
                            </span>

                        </div>


                        <div className="schedule-list">

                            {loadingEvents ? (

                                <div className="empty-schedule">
                                    <Clock3 size={30} />

                                    <h3>
                                        Loading schedule...
                                    </h3>

                                    <p>
                                        Fetching your scheduled events.
                                    </p>
                                </div>

                            ) : events.length === 0 ? (

                                <div className="empty-schedule">

                                    <CalendarDays size={30} />

                                    <h3>
                                        No events scheduled
                                    </h3>

                                    <p>
                                        Add an event to start
                                        planning your day.
                                    </p>

                                </div>

                            ) : (

                                events.map((event) => (

                                    <div
                                        className="schedule-item"
                                        key={event.id}
                                    >

                                        <div className="schedule-time">

                                            <Clock3 size={15} />

                                            <span>
                                                {event.time}
                                            </span>

                                        </div>


                                        <div className="schedule-event-icon">

                                            <CalendarDays size={18} />

                                        </div>


                                        <div className="schedule-event-info">

                                            <h3>
                                                {event.title}
                                            </h3>

                                            <div className="schedule-event-meta">

                                                <span>
                                                    <CalendarDays size={12} />
                                                    {event.date}
                                                </span>

                                                <span>
                                                    <MapPin size={12} />
                                                    {event.location}
                                                </span>

                                                <span>
                                                    {event.status}
                                                </span>

                                            </div>

                                        </div>


                                        <button
                                            type="button"
                                            className="schedule-delete"
                                            onClick={() =>
                                                deleteEvent(event)
                                            }
                                            title="Cancel event"
                                            aria-label="Cancel event"
                                        >
                                            <Trash2 size={16} />
                                        </button>

                                    </div>

                                ))

                            )}

                        </div>

                    </section>

                </div>

            </main>

        </div>
    );
}

export default Schedule;