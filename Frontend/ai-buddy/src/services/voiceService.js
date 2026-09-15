// ==========================================
// ZARVIS VOICE SERVICE
// ==========================================

// Check whether browser supports speech recognition
export function isSpeechRecognitionSupported() {
    return Boolean(
        window.SpeechRecognition ||
        window.webkitSpeechRecognition
    );
}

// Start speech recognition
export function startListening({
    onResult,
    onStart,
    onEnd,
    onError,
} = {}) {
    if (!isSpeechRecognitionSupported()) {
        const error = new Error(
            "Speech recognition is not supported in this browser."
        );

        onError?.(error);
        return null;
    }

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        onStart?.();
    };

    recognition.onresult = (event) => {
        const transcript =
            event.results?.[0]?.[0]?.transcript || "";

        onResult?.(transcript);
    };

    recognition.onerror = (event) => {
        onError?.(
            new Error(
                event.error || "Speech recognition failed."
            )
        );
    };

    recognition.onend = () => {
        onEnd?.();
    };

    recognition.start();

    return recognition;
}

// Stop speech recognition
export function stopListening(recognition) {
    if (recognition) {
        recognition.stop();
    }
}

// Check whether browser supports text-to-speech
export function isSpeechSynthesisSupported() {
    return "speechSynthesis" in window;
}

// Make Zarvis speak
export function speak(text, options = {}) {
    if (!isSpeechSynthesisSupported()) {
        console.warn(
            "Text-to-speech is not supported in this browser."
        );
        return;
    }

    if (!text || !text.trim()) {
        return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(
        text.trim()
    );

    utterance.lang = options.lang || "en-IN";
    utterance.rate = options.rate || 1;
    utterance.pitch = options.pitch || 1;
    utterance.volume = options.volume ?? 1;

    window.speechSynthesis.speak(utterance);

    return utterance;
}

// Stop Zarvis speaking
export function stopSpeaking() {
    if (isSpeechSynthesisSupported()) {
        window.speechSynthesis.cancel();
    }
}

// Pause Zarvis speaking
export function pauseSpeaking() {
    if (isSpeechSynthesisSupported()) {
        window.speechSynthesis.pause();
    }
}

// Resume Zarvis speaking
export function resumeSpeaking() {
    if (isSpeechSynthesisSupported()) {
        window.speechSynthesis.resume();
    }
}

const voiceService = {
    isSpeechRecognitionSupported,
    startListening,
    stopListening,
    isSpeechSynthesisSupported,
    speak,
    stopSpeaking,
    pauseSpeaking,
    resumeSpeaking,
};

export default voiceService;