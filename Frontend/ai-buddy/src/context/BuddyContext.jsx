// ==========================================
// ZARVIS BUDDY CONTEXT
// Global assistant state, execution state,
// execution workflow, dashboard refresh,
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
    // BASIC EXECUTION WORKFLOW
    //
    // Stores the actual execution stages
    // received from Zarvis backend.
    // ==========================================

    const [executionWorkflow, setExecutionWorkflow] =
        useState([]);

    // ==========================================
    // DASHBOARD REFRESH
    //
    // Used when any feature performs a task.
    //
    // Example:
    //
    // Email sent
    //      ↓
    // refreshDashboard()
    //      ↓
    // Dashboard reloads latest data
    //
    // The value changes every time
    // refreshDashboard() is called.
    // ==========================================

    const [dashboardRefreshKey, setDashboardRefreshKey] =
        useState(0);

    const refreshDashboard = () => {

        setDashboardRefreshKey(
            (previous) => previous + 1
        );

    };

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

    const startExecution = (
        message = "Processing your request..."
    ) => {

        setExecutionActive(true);

        setExecutionStatus("RUNNING");

        setExecutionMessage(message);

        // Start a fresh workflow for every
        // new execution.
        setExecutionWorkflow([]);
    };

    // ==========================================
    // UPDATE GLOBAL EXECUTION
    // ==========================================

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

    // ==========================================
    // SET EXECUTION WORKFLOW
    //
    // Backend can send the complete workflow
    // array after task execution.
    // ==========================================

    const setExecutionWorkflowData = (
        workflow = []
    ) => {

        if (!Array.isArray(workflow)) {

            setExecutionWorkflow([]);

            return;

        }

        setExecutionWorkflow(workflow);
    };

    // ==========================================
    // UPDATE ONE WORKFLOW STEP
    //
    // Useful when execution is happening
    // step-by-step.
    // ==========================================

    const updateExecutionWorkflow = (
        workflow = []
    ) => {

        if (!Array.isArray(workflow)) {

            return;

        }

        setExecutionWorkflow(workflow);
    };

    // ==========================================
    // CLEAR EXECUTION WORKFLOW
    // ==========================================

    const clearExecutionWorkflow = () => {

        setExecutionWorkflow([]);

    };

    // ==========================================
    // FINISH EXECUTION
    // ==========================================

    const finishExecution = (
        message = "Task completed successfully."
    ) => {

        setExecutionStatus("COMPLETED");

        setExecutionMessage(message);

        setExecutionActive(false);
    };

    // ==========================================
    // FAIL EXECUTION
    // ==========================================

    const failExecution = (
        message = "Task failed."
    ) => {

        setExecutionStatus("FAILED");

        setExecutionMessage(message);

        setExecutionActive(false);
    };

    // ==========================================
    // CLEAR EXECUTION
    // ==========================================

    const clearExecution = () => {

        setExecutionActive(false);

        setExecutionStatus("IDLE");

        setExecutionMessage("");

        setExecutionWorkflow([]);
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

            createdAt:
                new Date().toISOString(),
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

    const removeNotification = (
        notificationId
    ) => {

        setNotifications((previous) =>

            previous.filter(
                (notification) =>
                    notification.id !==
                    notificationId
            )

        );
    };

    // ==========================================
    // MARK ONE NOTIFICATION AS READ
    // ==========================================

    const markNotificationRead = (
        notificationId
    ) => {

        setNotifications((previous) =>

            previous.map(
                (notification) =>

                    notification.id ===
                    notificationId

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

            previous.map(
                (notification) => ({
                    ...notification,
                    read: true,
                })
            )

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

        setExecutionWorkflow([]);

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
        // EXECUTION WORKFLOW
        // --------------------------------------

        executionWorkflow,

        setExecutionWorkflowData,

        updateExecutionWorkflow,

        clearExecutionWorkflow,

        // --------------------------------------
        // DASHBOARD REFRESH
        // --------------------------------------

        dashboardRefreshKey,

        refreshDashboard,

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