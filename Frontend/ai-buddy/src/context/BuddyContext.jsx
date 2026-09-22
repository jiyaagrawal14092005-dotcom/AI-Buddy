
// ==========================================
// ZARVIS BUDDY CONTEXT
// Global assistant state, execution state,
// and notification management
// ==========================================

import {
    createContext,
    useContext,
    useState,
} from "react";

const BuddyContext = createContext(null);

export function BuddyProvider({ children }) {

    // ==========================================
    // ZARVIS STATUS
    // ==========================================

    const [buddyStatus, setBuddyStatus] = useState("ONLINE");
    const [isThinking, setIsThinking] = useState(false);

    const [lastCommand, setLastCommand] = useState("");
    const [lastResponse, setLastResponse] = useState("");

    // ==========================================
    // VOICE STATES
    // ==========================================

    const [isListening, setIsListening] = useState(false);
    const [wakeWordActive, setWakeWordActive] = useState(false);

    // ==========================================
    // GLOBAL EXECUTION STATE
    //
    // This state belongs to BuddyProvider,
    // not Assistant.jsx.
    //
    // Therefore it survives route changes.
    // ==========================================

    const [executionActive, setExecutionActive] = useState(false);

    const [executionStatus, setExecutionStatus] =
        useState("IDLE");

    const [executionMessage, setExecutionMessage] =
        useState("");

    // ==========================================
    // GLOBAL NOTIFICATIONS
    // ==========================================

    const [notifications, setNotifications] = useState([]);

    // ==========================================
    // SET ZARVIS STATUS
    // ==========================================

    const updateStatus = (status) => {
        setBuddyStatus(status);
    };

    // ==========================================
    // START THINKING
    // ==========================================

    const startThinking = () => {
        setIsThinking(true);
        setBuddyStatus("THINKING");
    };

    // ==========================================
    // STOP THINKING
    // ==========================================

    const stopThinking = () => {
        setIsThinking(false);
        setBuddyStatus("ONLINE");
    };

    // ==========================================
    // SAVE LATEST COMMAND
    // ==========================================

    const setCommand = (command) => {
        setLastCommand(command);
    };

    // ==========================================
    // SAVE LATEST RESPONSE
    // ==========================================

    const setResponse = (response) => {
        setLastResponse(response);
    };

    // ==========================================
    // VOICE LISTENING STATE
    // ==========================================

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

    // ==========================================
    // WAKE WORD STATE
    // ==========================================

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

    // ==========================================
    // GLOBAL EXECUTION
    // ==========================================

    const startExecution = (message = "Processing your request...") => {
        setExecutionActive(true);
        setExecutionStatus("RUNNING");
        setExecutionMessage(message);
    };

    const updateExecution = (
        status,
        message = ""
    ) => {
        setExecutionStatus(status);
        setExecutionMessage(message);

        if (
            status === "COMPLETED" ||
            status === "FAILED" ||
            status === "CANCELLED"
        ) {
            setExecutionActive(false);
        }
    };

    const finishExecution = (
        message = "Task completed successfully."
    ) => {
        setExecutionStatus("COMPLETED");
        setExecutionMessage(message);
        setExecutionActive(false);
    };

    const failExecution = (
        message = "Task failed."
    ) => {
        setExecutionStatus("FAILED");
        setExecutionMessage(message);
        setExecutionActive(false);
    };

    const clearExecution = () => {
        setExecutionActive(false);
        setExecutionStatus("IDLE");
        setExecutionMessage("");
    };

    // ==========================================
    // ADD GLOBAL NOTIFICATION
    // ==========================================

    const addNotification = ({
        title = "Zarvis Update",
        message = "",
        type = "info",
        icon = "info",
        persistent = true,
    } = {}) => {

        const notification = {
            id:
                `${Date.now()}-${Math.random()
                    .toString(36)
                    .slice(2, 9)}`,

            title,
            message,
            type,
            icon,
            persistent,

            read: false,

            createdAt: new Date().toISOString(),
        };

        setNotifications((previous) => [
            notification,
            ...previous,
        ]);

        return notification.id;
    };

    // ==========================================
    // REMOVE NOTIFICATION
    // ==========================================

    const removeNotification = (notificationId) => {
        setNotifications((previous) =>
            previous.filter(
                (notification) =>
                    notification.id !== notificationId
            )
        );
    };

    // ==========================================
    // MARK ONE NOTIFICATION AS READ
    // ==========================================

    const markNotificationRead = (notificationId) => {
        setNotifications((previous) =>
            previous.map((notification) =>
                notification.id === notificationId
                    ? {
                        ...notification,
                        read: true,
                    }
                    : notification
            )
        );
    };

    // ==========================================
    // MARK ALL NOTIFICATIONS AS READ
    // ==========================================

    const markAllNotificationsRead = () => {
        setNotifications((previous) =>
            previous.map((notification) => ({
                ...notification,
                read: true,
            }))
        );
    };

    // ==========================================
    // CLEAR ALL NOTIFICATIONS
    // ==========================================

    const clearNotifications = () => {
        setNotifications([]);
    };

    // ==========================================
    // UNREAD NOTIFICATION COUNT
    // ==========================================

    const unreadNotificationCount =
        notifications.filter(
            (notification) =>
                !notification.read
        ).length;

    // ==========================================
    // RESET ASSISTANT STATE
    // ==========================================

    const resetBuddy = () => {

        setIsThinking(false);
        setIsListening(false);
        setWakeWordActive(false);

        setLastCommand("");
        setLastResponse("");

        setExecutionActive(false);
        setExecutionStatus("IDLE");
        setExecutionMessage("");

        setBuddyStatus("ONLINE");
    };

    // ==========================================
    // CONTEXT VALUE
    // ==========================================

    const value = {

        // --------------------------------------
        // ZARVIS STATUS
        // --------------------------------------

        buddyStatus,
        isThinking,
        lastCommand,
        lastResponse,

        // --------------------------------------
        // VOICE
        // --------------------------------------

        isListening,
        wakeWordActive,

        // --------------------------------------
        // EXISTING FUNCTIONS
        // --------------------------------------

        updateStatus,

        startThinking,
        stopThinking,

        setCommand,
        setResponse,

        startListeningState,
        stopListeningState,

        enableWakeWord,
        disableWakeWord,

        // --------------------------------------
        // GLOBAL EXECUTION
        // --------------------------------------

        executionActive,
        executionStatus,
        executionMessage,

        startExecution,
        updateExecution,
        finishExecution,
        failExecution,
        clearExecution,

        // --------------------------------------
        // GLOBAL NOTIFICATIONS
        // --------------------------------------

        notifications,
        unreadNotificationCount,

        addNotification,
        removeNotification,

        markNotificationRead,
        markAllNotificationsRead,

        clearNotifications,

        // --------------------------------------
        // RESET
        // --------------------------------------

        resetBuddy,
    };

    return (
        <BuddyContext.Provider value={value}>
            {children}
        </BuddyContext.Provider>
    );
}

export function useBuddy() {

    const context = useContext(
        BuddyContext
    );

    if (!context) {
        throw new Error(
            "useBuddy must be used inside BuddyProvider."
        );
    }

    return context;
}

export default BuddyContext;

