import { useEffect } from "react";
import useVoice from "../../hooks/useVoice";
import { useBuddy } from "../../context/BuddyContext";

function GlobalVoiceAssistant() {
    const {
        transcript,
        startWakeWordMode,
        stopWakeWordMode,
    } = useVoice();

    const {
        setCommand,
        startThinking,
    } = useBuddy();

    useEffect(() => {
        // Global voice system available
        startWakeWordMode();

        return () => {
            stopWakeWordMode();
        };
    }, []);

    useEffect(() => {
        if (!transcript) return;

        console.log("Zarvis heard:", transcript);

        setCommand(transcript);

        // Temporary frontend thinking state
        startThinking();
    }, [transcript]);

    return null;
}

export default GlobalVoiceAssistant;