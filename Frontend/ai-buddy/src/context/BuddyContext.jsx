// ==========================================
// ZARVIS BUDDY CONTEXT
// ==========================================

import {
    createContext,
    useContext,
    useState,
} from "react";

const BuddyContext = createContext(null);

export function BuddyProvider({ children }) {
    const [buddyStatus, setBuddyStatus] = useState("ONLINE");
    const [isThinking, setIsThinking] = useState(false);

    const [lastCommand, setLastCommand] = useState("");
    const [lastResponse, setLastResponse] = useState("");

    // Voice states
    const [isListening, setIsListening] = useState(false);
    const [wakeWordActive, setWakeWordActive] = useState(false);

    // Set Zarvis status
    const updateStatus = (status) => {
        setBuddyStatus(status);
    };

    // Start thinking
    const startThinking = () => {
        setIsThinking(true);
        setBuddyStatus("THINKING");
    };

    // Stop thinking
    const stopThinking = () => {
        setIsThinking(false);
        setBuddyStatus("ONLINE");
    };

    // Save latest command
    const setCommand = (command) => {
        setLastCommand(command);
    };

    // Save latest response
    const setResponse = (response) => {
        setLastResponse(response);
    };

    // Voice listening state
    const startListeningState = () => {
        setIsListening(true);
        setBuddyStatus("LISTENING");
    };

    const stopListeningState = () => {
        setIsListening(false);

        if (!isThinking) {
            setBuddyStatus("ONLINE");
        }
    };

    // Wake word state
    const enableWakeWord = () => {
        setWakeWordActive(true);
    };

    const disableWakeWord = () => {
        setWakeWordActive(false);
        setIsListening(false);

        if (!isThinking) {
            setBuddyStatus("ONLINE");
        }
    };

    // Reset assistant state
    const resetBuddy = () => {
        setIsThinking(false);
        setIsListening(false);
        setWakeWordActive(false);

        setLastCommand("");
        setLastResponse("");

        setBuddyStatus("ONLINE");
    };

    const value = {
        buddyStatus,
        isThinking,
        lastCommand,
        lastResponse,

        isListening,
        wakeWordActive,

        updateStatus,

        startThinking,
        stopThinking,

        setCommand,
        setResponse,

        startListeningState,
        stopListeningState,

        enableWakeWord,
        disableWakeWord,

        resetBuddy,
    };

    return (
        <BuddyContext.Provider value={value}>
            {children}
        </BuddyContext.Provider>
    );
}

// Custom hook
export function useBuddy() {
    const context = useContext(BuddyContext);

    if (!context) {
        throw new Error(
            "useBuddy must be used inside BuddyProvider."
        );
    }

    return context;
}

export default BuddyContext;