import { useEffect, useState } from "react";
import {
    Mic,
    ArrowUp,
    Sparkles,
} from "lucide-react";

import chatService from "../services/chatService";
import useVoice from "../hooks/useVoice";

function ChatBox() {
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    const {
        isListening,
        transcript,
        error: voiceError,
        startListening,
        stopListening,
    } = useVoice();

    useEffect(() => {
        if (transcript) {
            setMessage(transcript);
        }
    }, [transcript]);

    useEffect(() => {
        if (voiceError) {
            setResponse(voiceError);
        }
    }, [voiceError]);

    const handleSend = async () => {
        const text = message.trim();

        if (!text || loading) return;

        setLoading(true);

        try {
            const result = await chatService.sendMessage(text);

            setResponse(result.message);
            setMessage("");
        } catch (error) {
            console.error(error);

            setResponse(
                "Sorry, something went wrong."
            );
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (event) => {
        if (event.key === "Enter") {
            handleSend();
        }
    };

    const handleSuggestion = (text) => {
        setMessage(text);
    };

    return (
        <section className="buddy-hero glass-card">

            {/* ==================================================
          LEFT SIDE — EXISTING ZARVIS COMMAND AREA
         ================================================== */}

            <div className="buddy-content">

                <div className="buddy-label">
                    <Sparkles size={14} />
                    ZARVIS AI COMPANION
                </div>

                <h1>
                    Good Morning!
                    <br />
                    What should I help you with{" "}
                    <span>today?</span>
                </h1>

                <p>
                    Speak or type your goal and Zarvis will
                    help you plan, organize and get things done.
                </p>


                {/* RESPONSE */}

                {response && (
                    <div className="zarvis-response">

                        <Sparkles size={15} />

                        <span>
                            {response}
                        </span>

                    </div>
                )}


                {/* COMMAND BOX */}

                <div
                    className={`command-box ${isListening
                            ? "command-box-listening"
                            : ""
                        }`}
                >

                    <input
                        type="text"
                        value={message}
                        onChange={(event) =>
                            setMessage(event.target.value)
                        }
                        onKeyDown={handleKeyDown}
                        placeholder={
                            isListening
                                ? "Listening..."
                                : "Tell Zarvis what you want to do..."
                        }
                        disabled={loading}
                    />


                    {/* VOICE */}

                    <button
                        type="button"
                        className={`voice-button ${isListening
                                ? "voice-button-active"
                                : ""
                            }`}
                        title={
                            isListening
                                ? "Stop listening"
                                : "Voice input"
                        }
                        onClick={
                            isListening
                                ? stopListening
                                : startListening
                        }
                    >
                        <Mic size={20} />
                    </button>


                    {/* SEND */}

                    <button
                        type="button"
                        className="send-button"
                        title="Send"
                        onClick={handleSend}
                        disabled={loading}
                    >
                        <ArrowUp size={19} />
                    </button>

                </div>


                {/* SUGGESTIONS */}

                <div className="suggestions">

                    <span>
                        Try saying:
                    </span>

                    <button
                        type="button"
                        onClick={() =>
                            handleSuggestion(
                                "Plan my day"
                            )
                        }
                    >
                        Plan my day
                    </button>

                    <button
                        type="button"
                        onClick={() =>
                            handleSuggestion(
                                "Create a schedule"
                            )
                        }
                    >
                        Create a schedule
                    </button>

                    <button
                        type="button"
                        onClick={() =>
                            handleSuggestion(
                                "Organize my tasks"
                            )
                        }
                    >
                        Organize my tasks
                    </button>

                </div>

            </div>


            {/* ==================================================
          RIGHT SIDE — CUTE ZARVIS ROBOT
         ================================================== */}

            <div className="buddy-visual">

                {/* BACKGROUND GLOW */}

                <div className="robot-glow"></div>


                {/* ==================================================
            ROTATING ORBIT 1
           ================================================== */}

                <div className="robot-orbit robot-orbit-1">

                    <span className="orbit-particle"></span>

                </div>


                {/* ==================================================
            ROTATING ORBIT 2
           ================================================== */}

                <div className="robot-orbit robot-orbit-2">

                    <span className="orbit-particle"></span>

                </div>


                {/* ==================================================
            ROTATING ORBIT 3
           ================================================== */}

                <div className="robot-orbit robot-orbit-3">

                    <span className="orbit-particle"></span>

                </div>


                {/* ==================================================
            CUTE ZARVIS
           ================================================== */}

                <div className="cute-zarvis">


                    {/* LEFT HEADPHONE */}

                    <div className="zarvis-ear zarvis-ear-left">

                        <div className="ear-inner"></div>

                    </div>


                    {/* RIGHT HEADPHONE */}

                    <div className="zarvis-ear zarvis-ear-right">

                        <div className="ear-inner"></div>

                    </div>


                    {/* ==================================================
              ROBOT HEAD
             ================================================== */}

                    <div className="zarvis-head">

                        {/* FACE */}

                        <div className="zarvis-face">


                            {/* LEFT EYE */}

                            <div className="zarvis-eye">

                                <span></span>

                            </div>


                            {/* RIGHT EYE */}

                            <div className="zarvis-eye">

                                <span></span>

                            </div>


                            {/* SMILE */}

                            <div className="zarvis-smile"></div>

                        </div>


                        {/* HEAD HIGHLIGHT */}

                        <div className="zarvis-head-shine"></div>

                    </div>


                    {/* ==================================================
              NECK
             ================================================== */}

                    <div className="zarvis-neck"></div>


                    {/* ==================================================
              BODY
             ================================================== */}

                    <div className="zarvis-body">


                        {/* CHEST Z */}

                        <div className="zarvis-chest">

                            <span>
                                Z
                            </span>

                        </div>


                        {/* BODY HIGHLIGHT */}

                        <div className="zarvis-body-shine"></div>

                    </div>


                    {/* ==================================================
              LEFT ARM
             ================================================== */}

                    <div className="zarvis-arm zarvis-arm-left">

                        <div className="zarvis-hand"></div>

                    </div>


                    {/* ==================================================
              RIGHT ARM
             ================================================== */}

                    <div className="zarvis-arm zarvis-arm-right">

                        <div className="zarvis-hand"></div>

                    </div>

                </div>


                {/* ==================================================
            GLOWING PLATFORM
           ================================================== */}

                <div className="zarvis-platform">

                    <div className="platform-light"></div>

                    <div className="platform-ring"></div>

                </div>

            </div>

        </section>
    );
}

export default ChatBox;