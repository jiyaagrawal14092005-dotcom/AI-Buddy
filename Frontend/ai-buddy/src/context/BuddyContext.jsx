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

    // Set Zarvis status
    const updateStatus = (status) => {
        setBuddyStatus(status);
    };

    // Start thinking state
    const startThinking = () => {
        setIsThinking(true);
        setBuddyStatus("THINKING");
    };

    // Stop thinking state
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

    // Reset current assistant state
    const resetBuddy = () => {
        setIsThinking(false);
        setLastCommand("");
        setLastResponse("");
        setBuddyStatus("ONLINE");
    };

    const value = {
        buddyStatus,
        isThinking,
        lastCommand,
        lastResponse,

        updateStatus,
        startThinking,
        stopThinking,
        setCommand,
        setResponse,
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