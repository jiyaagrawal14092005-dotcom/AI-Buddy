import { useEffect, useState } from "react";

import {
    Play,
    Pause,
    RotateCcw,
    Activity,
    Zap,
    CheckCircle2,
} from "lucide-react";

import {
    getAllTimers,
    getTimer,
    cancelTimer,
} from "../../services/timerService";

import { useBuddy } from "../../context/BuddyContext";


const DEFAULT_MINUTES = 25;


function Timer() {

    const {
        addNotification,
    } = useBuddy();


    // =====================================================
    // LOCAL FOCUS TIMER
    // =====================================================

    const [seconds, setSeconds] =
        useState(DEFAULT_MINUTES * 60);

    const [running, setRunning] =
        useState(false);

    const [completed, setCompleted] =
        useState(false);


    // =====================================================
    // BACKEND AI TIMER
    // =====================================================

    const [backendTimer, setBackendTimer] =
        useState(null);

    const [backendLoading, setBackendLoading] =
        useState(false);


    // Track previous backend status
    const [previousBackendStatus, setPreviousBackendStatus] =
        useState(null);


    const totalSeconds =
        DEFAULT_MINUTES * 60;


    // =====================================================
    // LOCAL TIMER ENGINE
    // =====================================================

    useEffect(() => {

        if (!running || seconds <= 0) {
            return;
        }


        const interval = setInterval(() => {

            setSeconds((previous) => {

                if (previous <= 1) {

                    setRunning(false);
                    setCompleted(true);

                    return 0;
                }

                return previous - 1;

            });

        }, 1000);


        return () => {
            clearInterval(interval);
        };

    }, [running, seconds]);


    // =====================================================
    // LOAD BACKEND AI TIMER
    // =====================================================

    useEffect(() => {

        let mounted = true;


        const loadBackendTimer = async () => {

            try {

                setBackendLoading(true);


                const result =
                    await getAllTimers();


                if (!mounted) {
                    return;
                }


                if (
                    result?.success &&
                    Array.isArray(result?.timers)
                ) {

                    /*
                     * IMPORTANT:
                     * First check for an active timer.
                     *
                     * This keeps the existing AI timer
                     * behaviour intact.
                     */

                    const activeTimers =
                        result.timers.filter(
                            (timer) =>
                                timer.status === "running" ||
                                timer.status === "created"
                        );


                    if (activeTimers.length > 0) {

                        const latestTimer =
                            activeTimers[
                                activeTimers.length - 1
                            ];


                        setBackendTimer(
                            latestTimer
                        );

                        return;
                    }


                    /*
                     * If there is no active timer,
                     * check whether a Focus Mode timer
                     * has just completed.
                     *
                     * We only keep the latest completed
                     * Focus Mode timer for notification.
                     */

                    const completedFocusTimers =
                        result.timers.filter(
                            (timer) =>
                                timer.status === "completed" &&
                                timer.focus_mode === true
                        );


                    if (
                        completedFocusTimers.length > 0
                    ) {

                        const latestCompleted =
                            completedFocusTimers[
                                completedFocusTimers.length - 1
                            ];


                        setBackendTimer(
                            latestCompleted
                        );

                    }

                }

            } catch (error) {

                console.error(
                    "Failed to load backend timer:",
                    error
                );

            } finally {

                if (mounted) {
                    setBackendLoading(false);
                }

            }

        };


        loadBackendTimer();


        const interval =
            setInterval(
                loadBackendTimer,
                3000
            );


        return () => {

            mounted = false;

            clearInterval(interval);

        };

    }, []);


    // =====================================================
    // UPDATE BACKEND TIMER
    // =====================================================

    useEffect(() => {

        if (!backendTimer?.timer_id) {
            return;
        }


        let mounted = true;


        const updateBackendTimer = async () => {

            try {

                const result =
                    await getTimer(
                        backendTimer.timer_id
                    );


                if (
                    mounted &&
                    result?.success &&
                    result?.timer
                ) {

                    setBackendTimer(
                        result.timer
                    );

                }

            } catch (error) {

                console.error(
                    "Failed to update backend timer:",
                    error
                );

            }

        };


        updateBackendTimer();


        const interval =
            setInterval(
                updateBackendTimer,
                1000
            );


        return () => {

            mounted = false;

            clearInterval(interval);

        };

    }, [backendTimer?.timer_id]);


    // =====================================================
    // FOCUS MODE START / COMPLETE NOTIFICATIONS
    // =====================================================

    useEffect(() => {

        if (!backendTimer?.focus_mode) {
            return;
        }


        const currentStatus =
            backendTimer.status;


        /*
         * START notification
         *
         * Only show when the timer actually changes
         * into running state.
         */

        if (
            currentStatus === "running" &&
            previousBackendStatus !== "running"
        ) {

            const durationSeconds =
                Number(
                    backendTimer.duration_seconds || 0
                );


            const durationMinutes =
                Math.floor(
                    durationSeconds / 60
                );


            const displayDuration =
                durationSeconds < 60
                    ? `${durationSeconds} seconds`
                    : `${durationMinutes} minute${
                        durationMinutes === 1
                            ? ""
                            : "s"
                    }`;


            addNotification({
                type: "success",
                title: "Focus Mode Started",
                message:
                    `Focus Mode started for ${displayDuration}.`,
            });

        }


        /*
         * COMPLETION notification
         */

        if (
            currentStatus === "completed" &&
            previousBackendStatus === "running"
        ) {

            addNotification({
                type: "success",
                title: "Focus Mode Completed",
                message:
                    "Focus Mode completed.",
            });

        }


        setPreviousBackendStatus(
            currentStatus
        );

    }, [
        backendTimer?.status,
        backendTimer?.focus_mode,
        backendTimer?.timer_id,
        addNotification,
        previousBackendStatus,
    ]);


    // =====================================================
    // DETERMINE TIMER TYPE
    // =====================================================

    const isBackendTimer =
        Boolean(backendTimer);


    // =====================================================
    // BACKEND TIMER STATES
    // =====================================================

    const backendRunning =
        backendTimer?.status === "running";


    const backendCompleted =
        backendTimer?.status === "completed";


    const backendCreated =
        backendTimer?.status === "created";


    const isFocusMode =
        backendTimer?.focus_mode === true;


    // =====================================================
    // ACTIVE SECONDS
    // =====================================================

    const activeSeconds =
        isBackendTimer
            ? Math.max(
                0,
                Math.ceil(
                    Number(
                        backendTimer.remaining_seconds || 0
                    )
                )
            )
            : seconds;


    // =====================================================
    // TIME FORMAT
    // =====================================================

    const minutes =
        Math.floor(activeSeconds / 60)
            .toString()
            .padStart(2, "0");


    const remainingSeconds =
        (activeSeconds % 60)
            .toString()
            .padStart(2, "0");


    // =====================================================
    // PROGRESS
    // =====================================================

    const backendDuration =
        isBackendTimer
            ? Number(
                backendTimer.duration_seconds || 0
            )
            : totalSeconds;


    const progress =
        backendDuration > 0
            ? (
                (
                    backendDuration -
                    activeSeconds
                ) /
                backendDuration
            ) * 100
            : 0;


    const safeProgress =
        Math.min(
            100,
            Math.max(
                0,
                progress
            )
        );


    // =====================================================
    // DISPLAY STATES
    // =====================================================

    const displayCompleted =
        isBackendTimer
            ? backendCompleted
            : completed;


    const displayRunning =
        isBackendTimer
            ? backendRunning
            : running;


    // =====================================================
    // STATUS
    // =====================================================

    const statusText =
        displayCompleted
            ? "COMPLETE"
            : displayRunning
            ? "ACTIVE"
            : backendCreated
            ? "READY"
            : "STANDBY";


    // =====================================================
    // START / PAUSE LOCAL TIMER
    // =====================================================

    const toggleTimer = () => {

        // AI / Focus timer is controlled by backend
        if (isBackendTimer) {
            return;
        }


        if (completed) {
            return;
        }


        setRunning(
            (previous) => !previous
        );

    };


    // =====================================================
    // RESET / CANCEL TIMER
    // =====================================================

    const resetTimer = async () => {

        // Backend AI / Focus timer
        if (backendTimer?.timer_id) {

            try {

                await cancelTimer(
                    backendTimer.timer_id
                );

            } catch (error) {

                console.error(
                    "Failed to cancel backend timer:",
                    error
                );

            }


            setBackendTimer(null);
            setPreviousBackendStatus(null);

            return;
        }


        // Local Focus Timer
        setRunning(false);

        setSeconds(
            DEFAULT_MINUTES * 60
        );

        setCompleted(false);

    };


    // =====================================================
    // FOOTER STATUS
    // =====================================================

    const footerStatus =
        displayCompleted
            ? "SESSION COMPLETE"
            : displayRunning
            ? "RUNNING"
            : "READY";


    // =====================================================
    // SESSION NUMBER
    // =====================================================

    const sessionNumber =
        isBackendTimer
            ? `AI-${backendTimer.timer_id}`
            : "01";


    // =====================================================
    // UI
    // =====================================================

    return (

        <section className="technical-timer">


            {/* ================= TOP BAR ================= */}

            <div className="technical-timer-top">

                <div className="technical-title">

                    <div className="technical-icon">
                        <Activity size={16} />
                    </div>


                    <div>

                        <span>
                            SYSTEM MODULE // 04
                        </span>


                        <h3>
                            {isBackendTimer
                                ? isFocusMode
                                    ? "FOCUS MODE"
                                    : "AI TIMER"
                                : "FOCUS MODE"}
                        </h3>

                    </div>

                </div>


                <div className="technical-live">

                    <span
                        className={`live-dot ${
                            displayRunning
                                ? "timer-live"
                                : ""
                        }`}
                    ></span>


                    {statusText}

                </div>

            </div>


            {/* ================= DIVIDER ================= */}

            <div className="technical-divider">

                <span></span>

            </div>


            {/* ================= TIMER ================= */}

            <div className="technical-timer-main">


                <div className="timer-session-label">

                    {isBackendTimer
                        ? isFocusMode
                            ? `FOCUS_MODE_${backendTimer.timer_id}`
                            : `AI_TIMER_${backendTimer.timer_id}`
                        : "SESSION_01"}

                </div>


                <div
                    className={`technical-time ${
                        displayCompleted
                            ? "timer-completed"
                            : ""
                    }`}
                >

                    <span>
                        {minutes}
                    </span>


                    <b>
                        :
                    </b>


                    <span>
                        {remainingSeconds}
                    </span>

                </div>


                <div className="technical-progress">

                    <div
                        className="technical-progress-fill"
                        style={{
                            width:
                                `${safeProgress}%`,
                        }}
                    ></div>

                </div>


                <div className="technical-progress-info">

                    <span>

                        {isBackendTimer
                            ? isFocusMode
                                ? "FOCUS PROGRESS"
                                : "AI TIMER PROGRESS"
                            : "FOCUS PROGRESS"}

                    </span>


                    <strong>

                        {Math.round(
                            safeProgress
                        )}%

                    </strong>

                </div>

            </div>


            {/* ================= TELEMETRY ================= */}

            <div className="technical-telemetry">


                <div className="telemetry-item">

                    <span>
                        CORE LOAD
                    </span>


                    <strong>

                        {displayRunning
                            ? "64%"
                            : displayCompleted
                            ? "28%"
                            : "32%"}

                    </strong>

                </div>


                <div className="telemetry-item">

                    <span>
                        SESSION
                    </span>


                    <strong>
                        {sessionNumber}
                    </strong>

                </div>


                <div className="telemetry-item">

                    <span>
                        EFFICIENCY
                    </span>


                    <strong className="efficiency">

                        <Zap size={12} />


                        {displayCompleted
                            ? "DONE"
                            : "HIGH"}

                    </strong>

                </div>

            </div>


            {/* ================= CONTROLS ================= */}

            <div className="technical-controls">


                <button
                    type="button"
                    className="technical-start"
                    onClick={toggleTimer}
                    disabled={
                        displayCompleted ||
                        isBackendTimer
                    }
                >

                    {displayCompleted ? (

                        <CheckCircle2
                            size={15}
                        />

                    ) : displayRunning ? (

                        <Pause
                            size={15}
                        />

                    ) : (

                        <Play
                            size={15}
                        />

                    )}


                    {displayCompleted
                        ? "FOCUS COMPLETE"
                        : isBackendTimer
                        ? "AI CONTROLLED"
                        : displayRunning
                        ? "PAUSE FOCUS"
                        : "START FOCUS"}

                </button>


                <button
                    type="button"
                    className="technical-reset"
                    onClick={resetTimer}
                    disabled={backendLoading}
                >

                    <RotateCcw
                        size={15}
                    />

                    RESET

                </button>

            </div>


            {/* ================= FOOTER ================= */}

            <div className="technical-footer">

                <span>

                    {isBackendTimer
                        ? "BACKEND PROCESS"
                        : "LOCAL PROCESS"}

                </span>


                <span>
                    ● ZARVIS CORE
                </span>


                <span>
                    {footerStatus}
                </span>

            </div>


        </section>

    );

}


export default Timer;