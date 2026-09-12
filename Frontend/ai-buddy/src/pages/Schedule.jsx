import { useState } from "react";
import {
    Plus,
    CalendarDays,
    Clock3,
    MapPin,
    Trash2,
    CheckCircle2,
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const initialEvents = [
    {
        id: 1,
        title: "Machine Learning Class",
        date: "Today",
        time: "11:00 AM",
        location: "Online",
        type: "STUDY",
    },
    {
        id: 2,
        title: "Project Development",
        date: "Today",
        time: "02:00 PM",
        location: "Workspace",
        type: "WORK",
    },
    {
        id: 3,
        title: "Revision Session",
        date: "Today",
        time: "05:30 PM",
        location: "Personal",
        type: "FOCUS",
    },
];

function Schedule() {
    const [events, setEvents] = useState(initialEvents);
    const [showForm, setShowForm] = useState(false);

    const [newEvent, setNewEvent] = useState({
        title: "",
        date: "",
        time: "",
        location: "",
        type: "STUDY",
    });

    const addEvent = (e) => {
        e.preventDefault();

        if (!newEvent.title.trim()) return;

        const event = {
            id: Date.now(),
            title: newEvent.title,
            date: newEvent.date || "Today",
            time: newEvent.time || "Anytime",
            location: newEvent.location || "Personal",
            type: newEvent.type,
        };

        setEvents((prev) => [...prev, event]);

        setNewEvent({
            title: "",
            date: "",
            time: "",
            location: "",
            type: "STUDY",
        });

        setShowForm(false);
    };

    const deleteEvent = (id) => {
        setEvents((prev) =>
            prev.filter((event) => event.id !== id)
        );
    };

    return (
        <div className="app">

            <Sidebar />

            <main className="main-content">

                <Navbar />

                <div className="schedule-page">

                    {/* HEADER */}
                    <section className="schedule-page-header">

                        <div>
                            <span className="schedule-eyebrow">
                                <CalendarDays size={14} />
                                ZARVIS SCHEDULE SYSTEM
                            </span>

                            <h1>
                                My Schedule
                            </h1>

                            <p>
                                Keep your day organized with Zarvis.
                            </p>
                        </div>

                        <button
                            type="button"
                            className="schedule-add-button"
                            onClick={() =>
                                setShowForm(!showForm)
                            }
                        >
                            <Plus size={18} />
                            Add Event
                        </button>

                    </section>


                    {/* SUMMARY */}
                    <section className="schedule-summary">

                        <div className="schedule-summary-card">

                            <span>
                                TODAY'S EVENTS
                            </span>

                            <strong>
                                {events.length}
                            </strong>

                        </div>

                        <div className="schedule-summary-card">

                            <span>
                                NEXT EVENT
                            </span>

                            <strong>
                                {events.length
                                    ? events[0].time
                                    : "--"}
                            </strong>

                        </div>

                        <div className="schedule-summary-card">

                            <span>
                                STUDY
                            </span>

                            <strong>
                                {
                                    events.filter(
                                        (event) =>
                                            event.type === "STUDY"
                                    ).length
                                }
                            </strong>

                        </div>

                        <div className="schedule-summary-card">

                            <span>
                                WORK
                            </span>

                            <strong>
                                {
                                    events.filter(
                                        (event) =>
                                            event.type === "WORK"
                                    ).length
                                }
                            </strong>

                        </div>

                    </section>


                    {/* CREATE EVENT */}
                    {showForm && (
                        <form
                            className="schedule-create-panel"
                            onSubmit={addEvent}
                        >

                            <div className="schedule-create-header">

                                <div>
                                    <span>
                                        EVENT CREATOR
                                    </span>

                                    <h2>
                                        Create New Event
                                    </h2>
                                </div>

                                <button
                                    type="button"
                                    onClick={() =>
                                        setShowForm(false)
                                    }
                                >
                                    ×
                                </button>

                            </div>


                            <div className="schedule-form-grid">

                                <div className="schedule-field">

                                    <label>
                                        Event Name
                                    </label>

                                    <input
                                        type="text"
                                        placeholder="e.g. Team meeting"
                                        value={newEvent.title}
                                        onChange={(e) =>
                                            setNewEvent({
                                                ...newEvent,
                                                title: e.target.value,
                                            })
                                        }
                                    />

                                </div>


                                <div className="schedule-field">

                                    <label>
                                        Date
                                    </label>

                                    <input
                                        type="date"
                                        value={newEvent.date}
                                        onChange={(e) =>
                                            setNewEvent({
                                                ...newEvent,
                                                date: e.target.value,
                                            })
                                        }
                                    />

                                </div>


                                <div className="schedule-field">

                                    <label>
                                        Time
                                    </label>

                                    <input
                                        type="time"
                                        value={newEvent.time}
                                        onChange={(e) =>
                                            setNewEvent({
                                                ...newEvent,
                                                time: e.target.value,
                                            })
                                        }
                                    />

                                </div>


                                <div className="schedule-field">

                                    <label>
                                        Location
                                    </label>

                                    <input
                                        type="text"
                                        placeholder="Online / Workspace"
                                        value={newEvent.location}
                                        onChange={(e) =>
                                            setNewEvent({
                                                ...newEvent,
                                                location:
                                                    e.target.value,
                                            })
                                        }
                                    />

                                </div>


                                <div className="schedule-field">

                                    <label>
                                        Event Type
                                    </label>

                                    <select
                                        value={newEvent.type}
                                        onChange={(e) =>
                                            setNewEvent({
                                                ...newEvent,
                                                type: e.target.value,
                                            })
                                        }
                                    >

                                        <option value="STUDY">
                                            STUDY
                                        </option>

                                        <option value="WORK">
                                            WORK
                                        </option>

                                        <option value="FOCUS">
                                            FOCUS
                                        </option>

                                        <option value="PERSONAL">
                                            PERSONAL
                                        </option>

                                    </select>

                                </div>

                            </div>


                            <button
                                type="submit"
                                className="schedule-create-submit"
                            >
                                <Plus size={16} />
                                CREATE EVENT
                            </button>

                        </form>
                    )}


                    {/* EVENTS */}
                    <section className="schedule-events-panel">

                        <div className="schedule-events-header">

                            <div>
                                <span>
                                    SCHEDULE QUEUE // 02
                                </span>

                                <h2>
                                    Upcoming Events
                                </h2>
                            </div>

                            <div className="schedule-live">
                                <span></span>
                                LIVE
                            </div>

                        </div>


                        <div className="schedule-events-list">

                            {events.length === 0 ? (

                                <div className="schedule-empty">

                                    <CalendarDays size={32} />

                                    <h3>
                                        No events scheduled
                                    </h3>

                                    <p>
                                        Add an event to organize
                                        your day.
                                    </p>

                                </div>

                            ) : (

                                events.map((event) => (

                                    <div
                                        className="schedule-page-row"
                                        key={event.id}
                                    >

                                        <div className="schedule-page-time">

                                            <strong>
                                                {event.time}
                                            </strong>

                                            <span>
                                                {event.date}
                                            </span>

                                        </div>


                                        <div className="schedule-page-line">

                                            <span></span>

                                        </div>


                                        <div className="schedule-page-content">

                                            <div className="schedule-page-title">

                                                <CheckCircle2
                                                    size={17}
                                                />

                                                <strong>
                                                    {event.title}
                                                </strong>

                                            </div>


                                            <div className="schedule-page-meta">

                                                <span>
                                                    <MapPin size={12} />
                                                    {event.location}
                                                </span>

                                                <span>
                                                    <Clock3 size={12} />
                                                    {event.type}
                                                </span>

                                            </div>

                                        </div>


                                        <button
                                            type="button"
                                            className="schedule-delete"
                                            onClick={() =>
                                                deleteEvent(event.id)
                                            }
                                            title="Delete event"
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