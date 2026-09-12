import { useState, useEffect, useRef } from "react";

function useVoice() {
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
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        recognitionRef.current = recognition;

        return () => {
            recognition.stop();
        };
    }, []);

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

    const stopListening = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
    };

    return {
        isListening,
        transcript,
        error,
        startListening,
        stopListening,
    };
}

export default useVoice;