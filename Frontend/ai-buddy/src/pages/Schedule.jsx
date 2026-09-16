import { useRef, useState } from "react";
import { useLocation } from "react-router-dom";

import {
    Plus,
    CalendarDays,
    Clock3,
    MapPin,
    Trash2,
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";


function Schedule() {

    const location = useLocation();


    const [events, setEvents] = useState([
        {
            id: 1,
            title: "React Learning",
            date: "Today",
            time: "10:30 AM",
            location: "Study Desk",
        },
        {
            id: 2,
            title: "Work on Zarvis UI",
            date: "Today",
            time: "02:30 PM",
            location: "Home",
        },
        {
            id: 3,
            title: "Review Progress",
            date: "Today",
            time: "05:00 PM",
            location: "Study Desk",
        },
    ]);


    const [newEvent, setNewEvent] = useState(
        location.state?.eventType === "travel"
            ? "Travel Plan"
            : ""
    );


    const inputRef = useRef(null);


    /* =================================================
       OPEN ADD EVENT
    ================================================= */

    const openAddEvent = () => {

        inputRef.current?.focus();

    };


    /* =================================================
       ADD EVENT
    ================================================= */

    const addEvent = () => {

        const title = newEvent.trim();


        if (!title) {

            inputRef.current?.focus();

            return;

        }


        const event = {

            id: Date.now(),

            title: title,

            date: "Today",

            time: "Not scheduled",

            location:
                location.state?.eventType === "travel"
                    ? "Travel Plan"
                    : "Not specified",

        };


        setEvents((currentEvents) => [

            ...currentEvents,

            event,

        ]);


        setNewEvent("");


        // Keep cursor ready for another event
        setTimeout(() => {

            inputRef.current?.focus();

        }, 0);

    };


    /* =================================================
       DELETE EVENT
    ================================================= */

    const deleteEvent = (id) => {

        setEvents((currentEvents) =>
            currentEvents.filter(
                (event) => event.id !== id
            )
        );

    };


    /* =================================================
       SUMMARY DATA
    ================================================= */

    const upcomingCount =
        events.length > 1
            ? events.length - 1
            : 0;


    const onlineEvents = events.filter(
        (event) =>
            event.location === "Online" ||
            event.location === "Travel Plan"
    ).length;


    return (

        <div className="app">


            {/* =================================================
                SIDEBAR
            ================================================= */}

            <Sidebar />


            <main className="main-content">


                {/* =================================================
                    NAVBAR
                ================================================= */}

                <Navbar />


                <div className="schedule-page">


                    {/* =================================================
                        PAGE HEADER
                    ================================================= */}

                    <div className="page-header">

                        <div>

                            <span className="page-label">

                                ZARVIS PLANNER

                            </span>


                            <h1>
                                Schedule
                            </h1>


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


                    {/* =================================================
                        ADD EVENT INPUT
                    ================================================= */}

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

                                    addEvent();

                                }

                            }}
                            placeholder="What would you like to schedule?"
                        />


                        <button
                            type="button"
                            onClick={addEvent}
                            aria-label="Add event"
                        >

                            <Plus size={18} />

                        </button>

                    </div>


                    {/* =================================================
                        SCHEDULE SUMMARY
                    ================================================= */}

                    <div className="schedule-summary">


                        {/* TODAY'S EVENTS */}

                        <div className="schedule-stat">

                            <CalendarDays size={19} />

                            <div>

                                <strong>
                                    {events.length}
                                </strong>

                                <span>
                                    Today's Events
                                </span>

                            </div>

                        </div>


                        {/* UPCOMING */}

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


                        {/* ONLINE / TRAVEL */}

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


                    {/* =================================================
                        TODAY'S SCHEDULE
                    ================================================= */}

                    <section className="schedule-section">


                        {/* SECTION HEADER */}

                        <div className="section-heading">

                            <div>

                                <h2>
                                    Today's Schedule
                                </h2>

                                <p>
                                    Your planned events and activities.
                                </p>

                            </div>


                            <span>
                                {events.length} events
                            </span>

                        </div>


                        {/* =================================================
                            EVENT LIST
                        ================================================= */}

                        <div className="schedule-list">


                            {events.length === 0 ? (


                                /* EMPTY STATE */

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


                                /* EVENTS */

                                events.map((event) => (

                                    <div
                                        className="schedule-item"
                                        key={event.id}
                                    >


                                        {/* =================================================
                                            TIME
                                        ================================================= */}

                                        <div className="schedule-time">

                                            <Clock3 size={15} />

                                            <span>
                                                {event.time}
                                            </span>

                                        </div>


                                        {/* =================================================
                                            EVENT ICON
                                        ================================================= */}

                                        <div className="schedule-event-icon">

                                            <CalendarDays size={18} />

                                        </div>


                                        {/* =================================================
                                            EVENT DETAILS
                                        ================================================= */}

                                        <div className="schedule-event-info">


                                            <h3>
                                                {event.title}
                                            </h3>


                                            <div className="schedule-event-meta">


                                                <span>

                                                    <CalendarDays
                                                        size={12}
                                                    />

                                                    {event.date}

                                                </span>


                                                <span>

                                                    <MapPin
                                                        size={12}
                                                    />

                                                    {event.location}

                                                </span>


                                            </div>

                                        </div>


                                        {/* =================================================
                                            DELETE
                                        ================================================= */}

                                        <button
                                            type="button"
                                            className="schedule-delete"
                                            onClick={() =>
                                                deleteEvent(event.id)
                                            }
                                            title="Delete event"
                                            aria-label="Delete event"
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