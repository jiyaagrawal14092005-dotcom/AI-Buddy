import { useEffect, useState } from "react";
import {
    Play,
    Pause,
    RotateCcw,
    Activity,
    Zap,
} from "lucide-react";

function Timer() {
    const [seconds, setSeconds] = useState(25 * 60);
    const [running, setRunning] = useState(false);

    const totalSeconds = 25 * 60;

    useEffect(() => {
        if (!running || seconds <= 0) return;

        const interval = setInterval(() => {
            setSeconds((prev) => prev - 1);
        }, 1000);

        return () => clearInterval(interval);
    }, [running, seconds]);

    useEffect(() => {
        if (seconds === 0) {
            setRunning(false);
        }
    }, [seconds]);

    const minutes = Math.floor(seconds / 60)
        .toString()
        .padStart(2, "0");

    const remainingSeconds = (seconds % 60)
        .toString()
        .padStart(2, "0");

    const progress =
        ((totalSeconds - seconds) / totalSeconds) * 100;

    const resetTimer = () => {
        setRunning(false);
        setSeconds(totalSeconds);
    };

    return (
        <section className="technical-timer">

            {/* TOP BAR */}
            <div className="technical-timer-top">
                <div className="technical-title">

                    <div className="technical-icon">
                        <Activity size={16} />
                    </div>

                    <div>
                        <span>SYSTEM MODULE // 04</span>
                        <h3>FOCUS MODE</h3>
                    </div>

                </div>

                <div className="technical-live">
                    <span className="live-dot"></span>
                    {running ? "ACTIVE" : "STANDBY"}
                </div>
            </div>

            {/* DIVIDER */}
            <div className="technical-divider">
                <span></span>
            </div>

            {/* TIMER */}
            <div className="technical-timer-main">

                <div className="timer-session-label">
                    SESSION_01
                </div>

                <div className="technical-time">
                    <span>{minutes}</span>
                    <b>:</b>
                    <span>{remainingSeconds}</span>
                </div>

                <div className="technical-progress">
                    <div
                        className="technical-progress-fill"
                        style={{ width: `${progress}%` }}
                    ></div>
                </div>

                <div className="technical-progress-info">
                    <span>FOCUS PROGRESS</span>
                    <strong>{Math.round(progress)}%</strong>
                </div>

            </div>

            {/* TELEMETRY */}
            <div className="technical-telemetry">

                <div className="telemetry-item">
                    <span>CORE LOAD</span>

                    <strong>
                        {running ? "64%" : "32%"}
                    </strong>
                </div>

                <div className="telemetry-item">
                    <span>SESSION</span>

                    <strong>01</strong>
                </div>

                <div className="telemetry-item">
                    <span>EFFICIENCY</span>

                    <strong className="efficiency">
                        <Zap size={12} />
                        HIGH
                    </strong>
                </div>

            </div>

            {/* CONTROLS */}
            <div className="technical-controls">

                <button
                    type="button"
                    className="technical-start"
                    onClick={() => setRunning(!running)}
                >
                    {running ? (
                        <Pause size={15} />
                    ) : (
                        <Play size={15} />
                    )}

                    {running
                        ? "PAUSE FOCUS"
                        : "START FOCUS"}
                </button>

                <button
                    type="button"
                    className="technical-reset"
                    onClick={resetTimer}
                >
                    <RotateCcw size={15} />
                    RESET
                </button>

            </div>

            {/* FOOTER */}
            <div className="technical-footer">
                <span>LOCAL PROCESS</span>
                <span>● ZARVIS CORE</span>
                <span>READY</span>
            </div>

        </section>
    );
}

export default Timer;