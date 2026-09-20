import { useState, useEffect, useRef } from "react";
import { useBuddy } from "../context/BuddyContext";

function useVoice() {
    const {
        startListeningState,
        stopListeningState,
        enableWakeWord,
        disableWakeWord,
    } = useBuddy();

    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState("");
    const [error, setError] = useState("");

    const recognitionRef = useRef(null);

    useEffect(() => {
        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            setError(
                "Voice recognition is not supported in this browser."
            );
            return;
        }

        const recognition = new SpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-IN";

        recognition.onstart = () => {
            setIsListening(true);
            setError("");
            startListeningState();
        };

        recognition.onresult = (event) => {
            const text =
                event.results[0][0].transcript;

            setTranscript(text);
        };

        recognition.onerror = (event) => {
            console.error(
                "Voice recognition error:",
                event.error
            );

            setError(
                "Could not hear you. Please try again."
            );

            setIsListening(false);
            stopListeningState();
        };

        recognition.onend = () => {
            setIsListening(false);
            stopListeningState();
        };

        recognitionRef.current = recognition;

        return () => {
            try {
                recognition.stop();
            } catch (err) {
                console.log("Recognition already stopped.");
            }
        };
    }, [startListeningState, stopListeningState]);

    // Start normal voice listening
    const startListening = () => {
        if (!recognitionRef.current) {
            setError(
                "Voice recognition is not supported."
            );
            return;
        }

        setTranscript("");
        setError("");

        try {
            recognitionRef.current.start();
        } catch (err) {
            console.log("Voice already active.");
        }
    };

    // Stop voice listening
    const stopListening = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
    };

    // Enable wake-word mode
    const startWakeWordMode = () => {
        enableWakeWord();

        console.log(
            'Zarvis wake-word mode enabled. Say "Zarvis".'
        );
    };

    // Disable wake-word mode
    const stopWakeWordMode = () => {
        disableWakeWord();

        console.log("Zarvis wake-word mode disabled.");
    };

    return {
        isListening,
        transcript,
        error,

        startListening,
        stopListening,

        startWakeWordMode,
        stopWakeWordMode,
    };
}

export default useVoice;