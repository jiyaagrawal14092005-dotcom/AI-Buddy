import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    Sparkles,
    Mic,
    Bot,
    User,
    Volume2,
    Target,
    Clock3,
    Zap,
    MessageCircle,
    CalendarDays,
    BookOpen,
    Bell,
    CircleHelp,
    CheckCircle2,
    Activity,
} from "lucide-react";

import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";

import { useAuth } from "../context/AuthContext";
import { useBuddy } from "../context/BuddyContext";

import { sendMessage } from "../services/chatService";

import {
    approveAction,
    rejectAction,
} from "../services/approvalService";


function Assistant() {

    const navigate = useNavigate();

    const {
        user,
        authenticated,
    } = useAuth();


    // ==========================================
    // GLOBAL BUDDY / NOTIFICATION STATE
    // ==========================================

    const {
        addNotification,
    } = useBuddy();


    const [isListening, setIsListening] =
        useState(false);

    const [isSpeaking, setIsSpeaking] =
        useState(false);

    const [isThinking, setIsThinking] =
        useState(false);

    const [inputText, setInputText] =
        useState("");

    const [pendingApproval, setPendingApproval] =
        useState(null);

    const [isApprovalProcessing, setIsApprovalProcessing] =
        useState(false);


    const [messages, setMessages] = useState([
        {
            type: "zarvis",
            text: "Hey! I'm Zarvis. Say my name when you need me.",
            time: "NOW",
        },
    ]);


    // ==========================================
    // VOICE REFERENCES
    // ==========================================

    const recognitionRef =
        useRef(null);

    const stopRecognitionRef =
        useRef(null);

    const stopRequestedRef =
        useRef(false);

    const shouldListenRef =
        useRef(true);

    const speakingRef =
        useRef(false);

    const thinkingRef =
        useRef(false);


    // ==========================================
    // WAKE WORD
    // ==========================================

    const WAKE_WORDS = [
        "zarvis",
        "jarvis",
    ];


    const wakeWordActiveRef =
        useRef(false);


    // ==========================================
    // KEEP LATEST AUTH STATE AVAILABLE TO VOICE
    // ==========================================

    const userRef =
        useRef(user);

    const authenticatedRef =
        useRef(authenticated);


    useEffect(() => {

        userRef.current = user;

        authenticatedRef.current =
            authenticated;


        console.log(
            "Zarvis auth state updated:",
            {
                authenticated,
                user,
                userId: user?.id,
            }
        );

    }, [
        user,
        authenticated,
    ]);


    // ==========================================
    // CHECK WAKE WORD
    // ==========================================

    const extractWakeWordCommand = (text) => {

        if (!text) {

            return {
                wakeDetected: false,
                command: "",
            };
        }


        const normalizedText =
            text
                .trim()
                .replace(
                    /[,.!?;:]+$/g,
                    ""
                )
                .trim();


        const lowerText =
            normalizedText.toLowerCase();


        for (
            const wakeWord
            of WAKE_WORDS
        ) {

            const wakePattern =
                new RegExp(
                    `^(?:hey|okay|ok)?\\s*${wakeWord}\\b`,
                    "i"
                );


            if (
                wakePattern.test(
                    lowerText
                )
            ) {

                const command =
                    normalizedText
                        .replace(
                            wakePattern,
                            ""
                        )
                        .trim()
                        .replace(
                            /^[,.:;!?]+\s*/,
                            ""
                        )
                        .trim();


                return {
                    wakeDetected: true,
                    command,
                };
            }
        }


        return {
            wakeDetected: false,
            command: "",
        };
    };


    // ==========================================
    // STOP-ONLY LISTENER
    // ==========================================

    const startStopListening = () => {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;


        if (!SpeechRecognition) {

            console.log(
                "Speech Recognition is not supported by this browser."
            );

            return;
        }


        if (stopRecognitionRef.current) {

            try {

                stopRecognitionRef.current.stop();

            } catch {
                // Already stopped
            }
        }


        const stopRecognition =
            new SpeechRecognition();


        stopRecognition.lang =
            "en-IN";

        stopRecognition.continuous =
            true;

        stopRecognition.interimResults =
            false;


        stopRecognition.onstart = () => {

            stopRecognitionRef.current =
                stopRecognition;


            console.log(
                "Zarvis STOP listener active."
            );
        };


        stopRecognition.onresult = (
            event
        ) => {

            for (
                let i =
                    event.resultIndex;

                i <
                event.results.length;

                i++
            ) {

                const transcript =
                    event.results[i][0]
                        .transcript
                        .trim()
                        .toLowerCase();


                if (!transcript) {
                    continue;
                }


                console.log(
                    "Zarvis STOP listener heard:",
                    transcript
                );


                const stopDetected =
                    transcript.includes(
                        "zarvis stop"
                    ) ||
                    transcript.includes(
                        "jarvis stop"
                    ) ||
                    transcript === "stop" ||
                    transcript.includes(
                        "stop listening"
                    ) ||
                    transcript.includes(
                        "stop jarvis"
                    ) ||
                    transcript.includes(
                        "stop zarvis"
                    );


                if (!stopDetected) {
                    continue;
                }


                console.log(
                    "Zarvis STOP command detected."
                );


                stopRequestedRef.current =
                    true;

                speakingRef.current =
                    false;


                if (
                    window.speechSynthesis
                ) {

                    window.speechSynthesis.cancel();

                }


                setIsSpeaking(false);

                setIsThinking(false);

                thinkingRef.current =
                    false;


                try {

                    stopRecognition.stop();

                } catch {
                    // Already stopped
                }


                return;
            }
        };


        stopRecognition.onerror = (
            event
        ) => {

            console.log(
                "Zarvis STOP listener error:",
                event.error
            );
        };


        stopRecognition.onend = () => {

            if (
                stopRecognitionRef.current ===
                stopRecognition
            ) {

                stopRecognitionRef.current =
                    null;
            }


            console.log(
                "Zarvis STOP listener stopped."
            );


            if (
                shouldListenRef.current
            ) {

                setTimeout(() => {

                    if (
                        shouldListenRef.current &&
                        !speakingRef.current &&
                        !thinkingRef.current &&
                        !stopRecognitionRef.current
                    ) {

                        console.log(
                            "Zarvis restarting normal wake-word listener after STOP."
                        );


                        stopRequestedRef.current =
                            false;


                        startListening();
                    }

                }, 500);

            } else {

                stopRequestedRef.current =
                    false;
            }
        };


        try {

            stopRecognition.start();

            stopRecognitionRef.current =
                stopRecognition;

        } catch (error) {

            console.log(
                "STOP recognition start error:",
                error
            );
        }
    };


    // ==========================================
    // SPEAK RESPONSE
    // ==========================================

    const speak = (text) => {

        if (
            !window.speechSynthesis
        ) {

            startListening();

            return;
        }


        window.speechSynthesis.cancel();


        stopRequestedRef.current =
            false;


        speakingRef.current =
            true;


        startStopListening();


        setIsSpeaking(true);

        setIsListening(false);

        setIsThinking(false);

        thinkingRef.current =
            false;


        const speech =
            new SpeechSynthesisUtterance(
                text
            );


        speech.lang =
            "en-IN";

        speech.rate =
            0.95;

        speech.pitch =
            1;


        speech.onend = () => {

            speakingRef.current =
                false;


            setIsSpeaking(false);


            if (
                stopRequestedRef.current
            ) {

                return;
            }


            if (
                stopRecognitionRef.current
            ) {

                try {

                    stopRecognitionRef.current.stop();

                } catch {
                    // Already stopped
                }
            }


            if (
                shouldListenRef.current
            ) {

                setTimeout(() => {

                    if (
                        shouldListenRef.current &&
                        !speakingRef.current &&
                        !thinkingRef.current &&
                        !stopRecognitionRef.current &&
                        !stopRequestedRef.current
                    ) {

                        startListening();

                    }

                }, 600);
            }
        };


        speech.onerror = () => {

            speakingRef.current =
                false;


            setIsSpeaking(false);


            if (
                stopRequestedRef.current
            ) {

                return;
            }


            if (
                stopRecognitionRef.current
            ) {

                try {

                    stopRecognitionRef.current.stop();

                } catch {
                    // Already stopped
                }
            }


            if (
                shouldListenRef.current
            ) {

                setTimeout(() => {

                    if (
                        shouldListenRef.current &&
                        !speakingRef.current &&
                        !thinkingRef.current &&
                        !stopRecognitionRef.current &&
                        !stopRequestedRef.current
                    ) {

                        startListening();

                    }

                }, 300);
            }
        };


        window.speechSynthesis.speak(
            speech
        );
    };


    // ==========================================
    // ADD GLOBAL NOTIFICATION
    // ==========================================

    const createActionNotification = (
        result,
        cleanText
    ) => {

        console.log(
            "=========================================="
        );

        console.log(
            "ZARVIS NOTIFICATION CHECK"
        );

        console.log(
            "Backend result:",
            result
        );


        // ==========================================
        // BASIC RESULT EXTRACTION
        // ==========================================

        const actionResult =
            result?.action_result ||
            result?.actionResult ||
            null;


        const workflow =
            result?.workflow ||
            null;


        const workflowStatus =
            workflow?.status ||
            result?.workflow_status ||
            result?.status ||
            "";


        const normalizedStatus =
            String(
                workflowStatus
            ).toUpperCase();


        // ==========================================
        // BROWSER RESULT
        // ==========================================

        const browserResult =
            actionResult?.browser ||
            result?.browser ||
            null;


        // ==========================================
        // ACTION TYPE
        // ==========================================

        const actionType =
            actionResult?.action ||
            browserResult?.action ||
            result?.action ||
            "";


        const normalizedAction =
            String(
                actionType
            ).toLowerCase();


        // ==========================================
        // DOWNLOAD INFORMATION
        // ==========================================

        let downloadedFile =
            actionResult?.download ||
            browserResult?.download ||
            result?.download ||
            actionResult?.file ||
            result?.file ||
            null;


        // ==========================================
        // DIRECT FILE INFORMATION
        // ==========================================

        if (
            !downloadedFile &&
            (
                actionResult?.filename ||
                actionResult?.name ||
                actionResult?.path ||
                actionResult?.download_path
            )
        ) {

            downloadedFile =
                actionResult;
        }


        // ==========================================
        // COMMAND TEXT
        // ==========================================

        const commandText =
            String(
                cleanText || ""
            ).toLowerCase();


        // ==========================================
        // DOWNLOAD COMMAND DETECTION
        // ==========================================

        const isDownloadCommand =
            commandText.includes(
                "download"
            ) ||
            commandText.includes(
                "download button"
            ) ||
            commandText.includes(
                "save the file"
            ) ||
            commandText.includes(
                "file save"
            );


        // ==========================================
        // SUCCESS CONDITIONS
        // ==========================================

        const actionSuccess =
            actionResult?.success === true ||
            actionResult?.status === "completed" ||
            browserResult?.success === true;


        const workflowCompleted =
            normalizedStatus ===
            "COMPLETED";


        const downloadDetected =
            normalizedAction ===
                "download" ||
            !!downloadedFile ||
            isDownloadCommand;


        console.log(
            "Notification detection:",
            {
                workflowStatus,
                normalizedStatus,
                actionType,
                normalizedAction,
                actionSuccess,
                workflowCompleted,
                isDownloadCommand,
                downloadDetected,
                downloadedFile,
            }
        );


        // ==========================================
        // DOWNLOAD SUCCESS
        // ==========================================

        if (
            downloadDetected &&
            (
                actionSuccess ||
                workflowCompleted
            )
        ) {

            const filename =
                downloadedFile?.filename ||
                downloadedFile?.name ||
                downloadedFile?.file_name ||
                "Downloaded file";


            const downloadPath =
                downloadedFile?.path ||
                downloadedFile?.download_path ||
                downloadedFile?.file_path ||
                "Windows Downloads folder";


            console.log(
                "Creating DOWNLOAD SUCCESS notification:",
                {
                    filename,
                    downloadPath,
                }
            );


            addNotification({

                title:
                    "Download completed",

                message:
                    `${filename} has been downloaded successfully.`,

                type:
                    "success",

                icon:
                    "download",

                path:
                    downloadPath,

                persistent:
                    true,

            });


            return;
        }


        // ==========================================
        // DOWNLOAD FAILURE
        // ==========================================

        if (
            isDownloadCommand &&
            (
                actionResult?.success === false ||
                normalizedStatus === "FAILED" ||
                normalizedStatus === "ERROR"
            )
        ) {

            const failureMessage =
                actionResult?.message ||
                browserResult?.message ||
                result?.message ||
                "The requested file could not be downloaded.";


            console.log(
                "Creating DOWNLOAD FAILURE notification:",
                failureMessage
            );


            addNotification({

                title:
                    "Download failed",

                message:
                    failureMessage,

                type:
                    "error",

                icon:
                    "error",

                persistent:
                    true,

            });


            return;
        }


        // ==========================================
        // GENERAL BROWSER WORKFLOW SUCCESS
        // ==========================================

        if (
            workflowCompleted &&
            (
                normalizedAction === "open" ||
                normalizedAction === "click" ||
                normalizedAction === "navigate"
            )
        ) {

            console.log(
                "Creating BROWSER WORKFLOW notification."
            );


            addNotification({

                title:
                    "Browser task completed",

                message:
                    result?.message ||
                    "Your browser task was completed successfully.",

                type:
                    "success",

                icon:
                    "workflow",

                persistent:
                    true,

            });


            return;
        }


        console.log(
            "No notification condition matched."
        );
    };


    // ==========================================
    // PROCESS COMMAND
    // ==========================================

    const processCommand =
        async (text) => {

            const cleanText =
                text?.trim();


            if (!cleanText) {
                return;
            }


            if (
                recognitionRef.current
            ) {

                try {

                    recognitionRef.current.stop();

                } catch {
                    // Already stopped
                }
            }


            setIsListening(false);

            setIsThinking(true);

            thinkingRef.current =
                true;


            setMessages(
                (prev) => [
                    ...prev,
                    {
                        type: "user",
                        text: cleanText,
                        time: "NOW",
                    },
                ]
            );


            try {

                // ==========================================
                // GET LATEST AUTH STATE
                // ==========================================

                const currentUser =
                    userRef.current;


                const currentAuthenticated =
                    authenticatedRef.current;


                console.log(
                    "Zarvis command auth check:",
                    {
                        authenticated:
                            currentAuthenticated,

                        user:
                            currentUser,

                        userId:
                            currentUser?.id,
                    }
                );


                if (
                    !currentAuthenticated ||
                    !currentUser?.id
                ) {

                    throw new Error(
                        "You are not logged in. Please login again."
                    );
                }


                // ==========================================
                // REAL BACKEND REQUEST
                // ==========================================

                const result =
                    await sendMessage(
                        cleanText,
                        currentUser.id
                    );


                console.log(
                    "Zarvis backend response:",
                    result
                );


                // ==========================================
                // CREATE GLOBAL NOTIFICATION
                // ==========================================

                createActionNotification(
                    result,
                    cleanText
                );


                // ==========================================
                // CHECK FOR ACTION APPROVAL
                // ==========================================

                if (
                    result?.approval_required &&
                    result?.approval_id
                ) {

                    setIsThinking(false);

                    thinkingRef.current =
                        false;


                    const approvalParameters =
                        result?.parameters ||
                        result?.plan?.parameters ||
                        result?.plan?.details ||
                        {};


                    setPendingApproval({

                        approvalId:
                            result.approval_id,

                        command:
                            cleanText,

                        intent:
                            result.intent,

                        parameters:
                            approvalParameters,

                        message:
                            result.message ||
                            "This action requires your approval before execution.",

                    });


                    const approvalMessage =
                        result.message ||
                        "This booking requires your approval before I can confirm it.";


                    setMessages(
                        (prev) => [
                            ...prev,
                            {
                                type: "zarvis",
                                text:
                                    approvalMessage,
                                time: "NOW",
                            },
                        ]
                    );


                    speak(
                        approvalMessage
                    );


                    return;
                }


                const response =
                    result?.message ||
                    result?.response ||
                    result?.reply ||
                    "I received your request, but I could not generate a response.";


                setIsThinking(false);

                thinkingRef.current =
                    false;


                setMessages(
                    (prev) => [
                        ...prev,
                        {
                            type: "zarvis",
                            text:
                                response,
                            time: "NOW",
                        },
                    ]
                );


                speak(response);


            } catch (error) {

                console.error(
                    "Zarvis backend request failed:",
                    error
                );


                setIsThinking(false);

                thinkingRef.current =
                    false;


                const errorMessage =
                    error?.message ||
                    "Sorry, I could not connect to AI Buddy.";


                setMessages(
                    (prev) => [
                        ...prev,
                        {
                            type: "zarvis",
                            text:
                                errorMessage,
                            time: "NOW",
                        },
                    ]
                );


                speak(
                    errorMessage
                );
            }
        };


    // ==========================================
    // APPROVE PENDING ACTION
    // ==========================================

    const handleApprove =
        async () => {

            if (
                !pendingApproval?.approvalId
            ) {
                return;
            }


            const approvalId =
                pendingApproval.approvalId;


            const originalCommand =
                pendingApproval.command;


            const currentUser =
                userRef.current;


            if (
                !currentUser?.id
            ) {

                const message =
                    "You are not logged in. Please login again.";


                setMessages(
                    (prev) => [
                        ...prev,
                        {
                            type: "zarvis",
                            text: message,
                            time: "NOW",
                        },
                    ]
                );


                speak(message);

                return;
            }


            try {

                setIsApprovalProcessing(
                    true
                );


                const approvalResult =
                    await approveAction(
                        approvalId
                    );


                console.log(
                    "Zarvis approval result:",
                    approvalResult
                );


                if (
                    !approvalResult?.success &&
                    approvalResult?.status !==
                        "APPROVED"
                ) {

                    throw new Error(
                        approvalResult?.message ||
                        "Approval could not be completed."
                    );
                }


                const result =
                    await sendMessage(
                        originalCommand,
                        currentUser.id,
                        approvalId
                    );


                console.log(
                    "Approved action execution result:",
                    result
                );


                // ==========================================
                // GLOBAL NOTIFICATION FOR APPROVED ACTION
                // ==========================================

                createActionNotification(
                    result,
                    originalCommand
                );


                setPendingApproval(
                    null
                );


                const response =
                    result?.message ||
                    result?.response ||
                    result?.reply ||
                    "The action was completed successfully.";


                setMessages(
                    (prev) => [
                        ...prev,
                        {
                            type: "zarvis",
                            text:
                                response,
                            time: "NOW",
                        },
                    ]
                );


                speak(response);


            } catch (error) {

                console.error(
                    "Zarvis approval execution failed:",
                    error
                );


                setPendingApproval(
                    null
                );


                const errorMessage =
                    error?.message ||
                    "I could not complete the approved action.";


                setMessages(
                    (prev) => [
                        ...prev,
                        {
                            type: "zarvis",
                            text:
                                errorMessage,
                            time: "NOW",
                        },
                    ]
                );


                speak(
                    errorMessage
                );


            } finally {

                setIsApprovalProcessing(
                    false
                );
            }
        };


    // ==========================================
    // REJECT PENDING ACTION
    // ==========================================

    const handleReject =
        async () => {

            if (
                !pendingApproval?.approvalId
            ) {
                return;
            }


            try {

                setIsApprovalProcessing(
                    true
                );


                const result =
                    await rejectAction(
                        pendingApproval.approvalId
                    );


                console.log(
                    "Zarvis rejection result:",
                    result
                );


                setPendingApproval(
                    null
                );


                const message =
                    result?.message ||
                    "Okay. I cancelled the booking request.";


                setMessages(
                    (prev) => [
                        ...prev,
                        {
                            type: "zarvis",
                            text: message,
                            time: "NOW",
                        },
                    ]
                );


                speak(message);


            } catch (error) {

                console.error(
                    "Zarvis rejection failed:",
                    error
                );


                const errorMessage =
                    error?.message ||
                    "I could not reject the booking request.";


                setMessages(
                    (prev) => [
                        ...prev,
                        {
                            type: "zarvis",
                            text:
                                errorMessage,
                            time: "NOW",
                        },
                    ]
                );


                speak(
                    errorMessage
                );


            } finally {

                setIsApprovalProcessing(
                    false
                );
            }
        };


    // ==========================================
    // START VOICE LISTENING
    // ==========================================

    const startListening =
        () => {

            if (
                speakingRef.current
            ) {
                return;
            }


            if (
                thinkingRef.current
            ) {
                return;
            }


            if (
                !shouldListenRef.current
            ) {
                return;
            }


            if (
                stopRecognitionRef.current
            ) {
                return;
            }


            if (
                stopRequestedRef.current
            ) {
                return;
            }


            const SpeechRecognition =
                window.SpeechRecognition ||
                window.webkitSpeechRecognition;


            if (!SpeechRecognition) {

                console.log(
                    "Speech Recognition is not supported by this browser."
                );

                return;
            }


            if (
                recognitionRef.current
            ) {

                try {

                    recognitionRef.current.stop();

                } catch {
                    // Already stopped
                }
            }


            const recognition =
                new SpeechRecognition();


            recognition.lang =
                "en-IN";

            recognition.continuous =
                false;

            recognition.interimResults =
                false;


            recognition.onstart = () => {

                setIsListening(true);

                setIsThinking(false);

                thinkingRef.current =
                    false;


                console.log(
                    "Zarvis microphone listening. Waiting for wake word..."
                );
            };


            recognition.onresult =
                (event) => {

                    const transcript =
                        event.results[0][0]
                            .transcript
                            .trim();


                    setIsListening(false);


                    if (!transcript) {
                        return;
                    }


                    console.log(
                        "Zarvis heard:",
                        transcript
                    );


                    const {
                        wakeDetected,
                        command,
                    } =
                        extractWakeWordCommand(
                            transcript
                        );


                    if (!wakeDetected) {

                        console.log(
                            "Wake word not detected. Ignoring:",
                            transcript
                        );


                        wakeWordActiveRef.current =
                            false;


                        return;
                    }


                    wakeWordActiveRef.current =
                        true;


                    console.log(
                        "Zarvis wake word detected."
                    );


                    if (!command) {

                        console.log(
                            "Wake word detected. Waiting for command..."
                        );


                        setTimeout(() => {

                            if (
                                shouldListenRef.current &&
                                !speakingRef.current &&
                                !thinkingRef.current &&
                                !stopRecognitionRef.current &&
                                !stopRequestedRef.current
                            ) {

                                startListening();

                            }

                        }, 300);


                        return;
                    }


                    console.log(
                        "Zarvis command accepted:",
                        command
                    );


                    processCommand(
                        command
                    );
                };


            recognition.onerror =
                (event) => {

                    setIsListening(false);


                    console.log(
                        "Voice recognition error:",
                        event.error
                    );


                    if (
                        event.error ===
                            "not-allowed" ||
                        event.error ===
                            "service-not-allowed"
                    ) {

                        shouldListenRef.current =
                            false;
                    }
                };


            recognition.onend =
                () => {

                    setIsListening(false);


                    if (
                        stopRequestedRef.current ||
                        stopRecognitionRef.current
                    ) {
                        return;
                    }


                    if (
                        shouldListenRef.current &&
                        !speakingRef.current &&
                        !thinkingRef.current
                    ) {

                        setTimeout(() => {

                            if (
                                shouldListenRef.current &&
                                !speakingRef.current &&
                                !thinkingRef.current &&
                                !stopRecognitionRef.current &&
                                !stopRequestedRef.current
                            ) {

                                startListening();

                            }

                        }, 500);
                    }
                };


            recognitionRef.current =
                recognition;


            try {

                recognition.start();

            } catch (error) {

                console.log(
                    "Recognition start error:",
                    error
                );
            }
        };


    // ==========================================
    // QUICK COMMAND
    // ==========================================

    const handleQuickCommand =
        (command) => {

            processCommand(
                command
            );
        };


    // ==========================================
    // TEXT INPUT
    // ==========================================

    const handleTextSubmit =
        (e) => {

            e.preventDefault();


            if (
                !inputText.trim()
            ) {
                return;
            }


            processCommand(
                inputText
            );


            setInputText("");
        };


    // ==========================================
    // INITIALIZE VOICE ASSISTANT
    // ==========================================

    useEffect(() => {

        shouldListenRef.current =
            true;

        wakeWordActiveRef.current =
            false;

        stopRequestedRef.current =
            false;


        const timer =
            setTimeout(() => {

                startListening();

            }, 1000);


        return () => {

            shouldListenRef.current =
                false;

            wakeWordActiveRef.current =
                false;

            stopRequestedRef.current =
                false;


            clearTimeout(
                timer
            );


            if (
                recognitionRef.current
            ) {

                try {

                    recognitionRef.current.stop();

                } catch {
                    // Already stopped
                }
            }


            if (
                stopRecognitionRef.current
            ) {

                try {

                    stopRecognitionRef.current.stop();

                } catch {
                    // Already stopped
                }
            }


            window.speechSynthesis?.cancel();

        };

    }, []);


    // ==========================================
    // UI
    // ==========================================

    return (

        <div className="app">

            <Sidebar />


            <main className="main-content">

                <Navbar />


                <div className="assistant-page">


                    {/* ==========================================
                        HEADER
                    ========================================== */}

                    <section className="assistant-header">

                        <div className="assistant-header-content">

                            <span className="assistant-eyebrow">

                                <Sparkles size={13} />

                                ZARVIS AI ASSISTANT

                            </span>


                            <h1>
                                What can I help you with?
                            </h1>


                            <p>
                                Say "Zarvis" before your voice command.
                                Zarvis listens, thinks and responds automatically.
                            </p>

                        </div>


                        <div className="assistant-online">

                            <span></span>

                            ZARVIS ONLINE

                        </div>

                    </section>


                    {/* ==========================================
                        QUICK COMMANDS
                    ========================================== */}

                    <div className="assistant-quick-commands">

                        <button
                            type="button"
                            onClick={() =>
                                handleQuickCommand(
                                    "Plan my day"
                                )
                            }
                        >

                            <CalendarDays size={15} />

                            Plan my day

                        </button>


                        <button
                            type="button"
                            onClick={() =>
                                handleQuickCommand(
                                    "Help me with my studies"
                                )
                            }
                        >

                            <BookOpen size={15} />

                            Help with studies

                        </button>


                        <button
                            type="button"
                            onClick={() =>
                                handleQuickCommand(
                                    "Set a reminder"
                                )
                            }
                        >

                            <Bell size={15} />

                            Set a reminder

                        </button>


                        <button
                            type="button"
                            onClick={() =>
                                handleQuickCommand(
                                    "Answer my question"
                                )
                            }
                        >

                            <CircleHelp size={15} />

                            Any question

                        </button>

                    </div>


                    <div className="assistant-layout">


                        {/* ==========================================
                            MAIN ASSISTANT PANEL
                        ========================================== */}

                        <section className="assistant-main-panel">


                            <div className="assistant-panel-top">

                                <div className="assistant-panel-title">

                                    <div className="assistant-panel-icon">

                                        <MessageCircle size={17} />

                                    </div>


                                    <div>

                                        <span>
                                            ZARVIS CORE
                                        </span>

                                        <strong>
                                            Voice Assistant
                                        </strong>

                                    </div>

                                </div>


                                <div className="assistant-panel-status">

                                    <span></span>

                                    {isListening
                                        ? "LISTENING"
                                        : isSpeaking
                                            ? "SPEAKING"
                                            : isThinking
                                                ? "THINKING"
                                                : "READY"}

                                </div>

                            </div>


                            {/* ==========================================
                                VOICE CENTER
                            ========================================== */}

                            <div className="assistant-voice-center">

                                <div
                                    className={`assistant-voice-orb ${
                                        isListening
                                            ? "voice-orb-listening"
                                            : isSpeaking
                                                ? "voice-orb-speaking"
                                                : isThinking
                                                    ? "voice-orb-thinking"
                                                    : ""
                                    }`}
                                >

                                    <div className="assistant-orb-ring orb-ring-1"></div>

                                    <div className="assistant-orb-ring orb-ring-2"></div>

                                    <div className="assistant-orb-ring orb-ring-3"></div>


                                    <div className="assistant-orb-particles">

                                        <span></span>
                                        <span></span>
                                        <span></span>

                                    </div>


                                    <div className="assistant-orb-core">

                                        {isSpeaking ? (
                                            <Volume2 size={31} />
                                        ) : isListening ? (
                                            <Mic size={31} />
                                        ) : (
                                            <Sparkles size={31} />
                                        )}

                                    </div>

                                </div>


                                <h2>

                                    {isListening
                                        ? "I'm listening..."
                                        : isSpeaking
                                            ? "I'm speaking..."
                                            : isThinking
                                                ? "Thinking..."
                                                : "Ready for you"}

                                </h2>


                                <p>

                                    {isListening
                                        ? 'Say "Zarvis" before your command.'
                                        : isSpeaking
                                            ? "Zarvis is responding."
                                            : isThinking
                                                ? "Processing your command..."
                                                : "Just speak naturally."}

                                </p>


                                <div
                                    className={`assistant-waveform ${
                                        isListening ||
                                        isSpeaking
                                            ? "wave-active"
                                            : ""
                                    }`}
                                >

                                    {Array.from({
                                        length: 25,
                                    }).map(
                                        (_, index) => (

                                            <span
                                                key={index}
                                                style={{
                                                    animationDelay:
                                                        `${index * 0.045}s`,
                                                }}
                                            ></span>

                                        )
                                    )}

                                </div>

                            </div>


                            {/* ==========================================
                                CONVERSATION
                            ========================================== */}

                            <div className="assistant-conversation">

                                <div className="conversation-label">

                                    <Activity size={12} />

                                    LIVE CONVERSATION

                                </div>


                                {messages
                                    .slice(-4)
                                    .map(
                                        (
                                            message,
                                            index
                                        ) => (

                                            <div
                                                key={index}
                                                className={`conversation-message ${
                                                    message.type ===
                                                    "user"
                                                        ? "conversation-user"
                                                        : "conversation-zarvis"
                                                }`}
                                            >

                                                <div className="conversation-avatar">

                                                    {message.type ===
                                                    "user" ? (
                                                        <User size={14} />
                                                    ) : (
                                                        <Bot size={14} />
                                                    )}

                                                </div>


                                                <div className="conversation-content">

                                                    <div className="conversation-heading">

                                                        <strong>

                                                            {message.type ===
                                                            "user"
                                                                ? "YOU"
                                                                : "ZARVIS"}

                                                        </strong>


                                                        <span>
                                                            {message.time}
                                                        </span>

                                                    </div>


                                                    <p>
                                                        {message.text}
                                                    </p>

                                                </div>

                                            </div>

                                        )
                                    )}


                                {/* ==========================================
                                    APPROVAL CARD
                                ========================================== */}

                                {pendingApproval && (

                                    <div
                                        style={{
                                            marginTop:
                                                "16px",

                                            padding:
                                                "18px",

                                            borderRadius:
                                                "16px",

                                            border:
                                                "1px solid rgba(124, 92, 255, 0.35)",

                                            background:
                                                "rgba(124, 92, 255, 0.08)",

                                            boxShadow:
                                                "0 10px 30px rgba(0, 0, 0, 0.15)",
                                        }}
                                    >

                                        <div
                                            style={{
                                                display:
                                                    "flex",

                                                alignItems:
                                                    "center",

                                                gap:
                                                    "12px",

                                                marginBottom:
                                                    "14px",
                                            }}
                                        >

                                            <div
                                                style={{
                                                    width:
                                                        "38px",

                                                    height:
                                                        "38px",

                                                    borderRadius:
                                                        "12px",

                                                    display:
                                                        "flex",

                                                    alignItems:
                                                        "center",

                                                    justifyContent:
                                                        "center",

                                                    background:
                                                        "rgba(124, 92, 255, 0.16)",

                                                    fontSize:
                                                        "18px",
                                                }}
                                            >
                                                🔐
                                            </div>


                                            <div>

                                                <strong
                                                    style={{
                                                        display:
                                                            "block",

                                                        fontSize:
                                                            "14px",

                                                        letterSpacing:
                                                            "0.04em",
                                                    }}
                                                >
                                                    BOOKING APPROVAL
                                                </strong>


                                                <span
                                                    style={{
                                                        display:
                                                            "block",

                                                        marginTop:
                                                            "3px",

                                                        fontSize:
                                                            "12px",

                                                        opacity:
                                                            0.7,
                                                    }}
                                                >
                                                    Your permission is required
                                                </span>

                                            </div>

                                        </div>


                                        <p
                                            style={{
                                                margin:
                                                    "0 0 14px",

                                                fontSize:
                                                    "13px",

                                                lineHeight:
                                                    1.6,

                                                opacity:
                                                    0.85,
                                            }}
                                        >
                                            Zarvis is ready to confirm this booking, but needs your permission first.
                                        </p>


                                        <div
                                            style={{
                                                display:
                                                    "grid",

                                                gap:
                                                    "8px",

                                                marginBottom:
                                                    "16px",
                                            }}
                                        >

                                            {pendingApproval.parameters?.service && (

                                                <div
                                                    style={{
                                                        display:
                                                            "flex",

                                                        justifyContent:
                                                            "space-between",

                                                        gap:
                                                            "12px",

                                                        padding:
                                                            "9px 11px",

                                                        borderRadius:
                                                            "10px",

                                                        background:
                                                            "rgba(255, 255, 255, 0.04)",
                                                    }}
                                                >

                                                    <span
                                                        style={{
                                                            fontSize:
                                                                "12px",

                                                            opacity:
                                                                0.65,
                                                        }}
                                                    >
                                                        Service
                                                    </span>


                                                    <strong
                                                        style={{
                                                            fontSize:
                                                                "12px",

                                                            textAlign:
                                                                "right",
                                                        }}
                                                    >
                                                        {
                                                            pendingApproval
                                                                .parameters
                                                                .service
                                                        }
                                                    </strong>

                                                </div>

                                            )}


                                            {pendingApproval.parameters?.date && (

                                                <div
                                                    style={{
                                                        display:
                                                            "flex",

                                                        justifyContent:
                                                            "space-between",

                                                        gap:
                                                            "12px",

                                                        padding:
                                                            "9px 11px",

                                                        borderRadius:
                                                            "10px",

                                                        background:
                                                            "rgba(255, 255, 255, 0.04)",
                                                    }}
                                                >

                                                    <span
                                                        style={{
                                                            fontSize:
                                                                "12px",

                                                            opacity:
                                                                0.65,
                                                        }}
                                                    >
                                                        Date
                                                    </span>


                                                    <strong
                                                        style={{
                                                            fontSize:
                                                                "12px",
                                                        }}
                                                    >
                                                        {
                                                            pendingApproval
                                                                .parameters
                                                                .date
                                                        }
                                                    </strong>

                                                </div>

                                            )}


                                            {pendingApproval.parameters?.time && (

                                                <div
                                                    style={{
                                                        display:
                                                            "flex",

                                                        justifyContent:
                                                            "space-between",

                                                        gap:
                                                            "12px",

                                                        padding:
                                                            "9px 11px",

                                                        borderRadius:
                                                            "10px",

                                                        background:
                                                            "rgba(255, 255, 255, 0.04)",
                                                    }}
                                                >

                                                    <span
                                                        style={{
                                                            fontSize:
                                                                "12px",

                                                            opacity:
                                                                0.65,
                                                        }}
                                                    >
                                                        Time
                                                    </span>


                                                    <strong
                                                        style={{
                                                            fontSize:
                                                                "12px",
                                                        }}
                                                    >
                                                        {
                                                            pendingApproval
                                                                .parameters
                                                                .time
                                                        }
                                                    </strong>

                                                </div>

                                            )}

                                        </div>


                                        <div
                                            style={{
                                                display:
                                                    "flex",

                                                gap:
                                                    "10px",

                                                justifyContent:
                                                    "flex-end",

                                                flexWrap:
                                                    "wrap",
                                            }}
                                        >

                                            <button
                                                type="button"
                                                onClick={
                                                    handleReject
                                                }
                                                disabled={
                                                    isApprovalProcessing
                                                }
                                                style={{
                                                    minHeight:
                                                        "42px",

                                                    padding:
                                                        "0 16px",

                                                    borderRadius:
                                                        "10px",

                                                    border:
                                                        "1px solid rgba(255, 255, 255, 0.16)",

                                                    background:
                                                        "transparent",

                                                    color:
                                                        "inherit",

                                                    cursor:
                                                        isApprovalProcessing
                                                            ? "not-allowed"
                                                            : "pointer",

                                                    opacity:
                                                        isApprovalProcessing
                                                            ? 0.5
                                                            : 1,
                                                }}
                                            >
                                                Reject
                                            </button>


                                            <button
                                                type="button"
                                                onClick={
                                                    handleApprove
                                                }
                                                disabled={
                                                    isApprovalProcessing
                                                }
                                                style={{
                                                    minHeight:
                                                        "42px",

                                                    padding:
                                                        "0 18px",

                                                    borderRadius:
                                                        "10px",

                                                    border:
                                                        "1px solid rgba(124, 92, 255, 0.5)",

                                                    background:
                                                        "rgba(124, 92, 255, 0.9)",

                                                    color:
                                                        "#ffffff",

                                                    fontWeight:
                                                        600,

                                                    cursor:
                                                        isApprovalProcessing
                                                            ? "not-allowed"
                                                            : "pointer",

                                                    opacity:
                                                        isApprovalProcessing
                                                            ? 0.6
                                                            : 1,
                                                }}
                                            >

                                                {isApprovalProcessing
                                                    ? "Processing..."
                                                    : "Approve Booking"}

                                            </button>

                                        </div>

                                    </div>

                                )}

                            </div>


                            {/* ==========================================
                                TEXT INPUT
                            ========================================== */}

                            <form
                                className="zarvis-chat-input"
                                onSubmit={
                                    handleTextSubmit
                                }
                            >

                                <input
                                    type="text"
                                    value={
                                        inputText
                                    }
                                    onChange={(e) =>
                                        setInputText(
                                            e.target.value
                                        )
                                    }
                                    placeholder="Ask Zarvis anything..."
                                    disabled={
                                        isThinking
                                    }
                                />


                                <button
                                    type="submit"
                                    disabled={
                                        isThinking ||
                                        !inputText.trim()
                                    }
                                >

                                    {isThinking
                                        ? "Thinking..."
                                        : "Send"}

                                </button>

                            </form>


                            {/* ==========================================
                                BOTTOM STATUS
                            ========================================== */}

                            <div className="assistant-bottom-bar">

                                <div>

                                    <span className="bottom-status-dot"></span>


                                    {isListening
                                        ? "MICROPHONE ACTIVE"
                                        : isSpeaking
                                            ? "VOICE OUTPUT ACTIVE"
                                            : "VOICE SYSTEM READY"}

                                </div>


                                <span>
                                    VOICE ENABLED
                                </span>


                                <span>
                                    ZARVIS CORE
                                </span>

                            </div>

                        </section>


                        {/* ==========================================
                            SIDE PANEL
                        ========================================== */}

                        <aside className="assistant-side-panel">


                            {/* ==========================================
                                TODAY'S FOCUS
                            ========================================== */}

                            <section className="assistant-side-card">

                                <div className="side-card-header">

                                    <div>

                                        <div className="side-card-icon">

                                            <Target size={15} />

                                        </div>


                                        <div>

                                            <span>
                                                TODAY
                                            </span>


                                            <h3>
                                                Today's Focus
                                            </h3>

                                        </div>

                                    </div>


                                    <button
                                        type="button"
                                        onClick={() =>
                                            navigate(
                                                "/tasks"
                                            )
                                        }
                                    >
                                        View all
                                    </button>

                                </div>


                                <div className="focus-list">

                                    <div className="focus-item completed">

                                        <CheckCircle2 size={16} />

                                        <span>
                                            Complete AI assignment
                                        </span>

                                    </div>


                                    <div className="focus-item">

                                        <div className="empty-check"></div>

                                        <span>
                                            Study Machine Learning
                                        </span>

                                    </div>


                                    <div className="focus-item">

                                        <div className="empty-check"></div>

                                        <span>
                                            Work on Zarvis frontend
                                        </span>

                                    </div>


                                    <div className="focus-item">

                                        <div className="empty-check"></div>

                                        <span>
                                            Review today's notes
                                        </span>

                                    </div>

                                </div>

                            </section>


                            {/* ==========================================
                                VOICE COMMANDS
                            ========================================== */}

                            <section className="assistant-side-card">

                                <div className="side-card-header">

                                    <div>

                                        <div className="side-card-icon side-icon-cyan">

                                            <Mic size={15} />

                                        </div>


                                        <div>

                                            <span>
                                                VOICE
                                            </span>


                                            <h3>
                                                Voice Commands
                                            </h3>

                                        </div>

                                    </div>

                                </div>


                                <div className="voice-command-list">

                                    <button
                                        type="button"
                                        onClick={() =>
                                            handleQuickCommand(
                                                "Plan my day"
                                            )
                                        }
                                    >

                                        <Sparkles size={13} />

                                        "Plan my day"

                                    </button>


                                    <button
                                        type="button"
                                        onClick={() =>
                                            handleQuickCommand(
                                                "Remind me at 6 PM"
                                            )
                                        }
                                    >

                                        <Clock3 size={13} />

                                        "Remind me at 6 PM"

                                    </button>


                                    <button
                                        type="button"
                                        onClick={() =>
                                            handleQuickCommand(
                                                "What's next?"
                                            )
                                        }
                                    >

                                        <Zap size={13} />

                                        "What's next?"

                                    </button>


                                    <button
                                        type="button"
                                        onClick={() =>
                                            handleQuickCommand(
                                                "Explain this topic"
                                            )
                                        }
                                    >

                                        <BookOpen size={13} />

                                        "Explain this topic"

                                    </button>

                                </div>

                            </section>


                            {/* ==========================================
                                SYSTEM STATUS
                            ========================================== */}

                            <section className="assistant-side-card assistant-system-card">

                                <div className="system-card-title">

                                    <div className="side-card-icon side-icon-purple">

                                        <Activity size={15} />

                                    </div>


                                    <div>

                                        <span>
                                            SYSTEM
                                        </span>


                                        <h3>
                                            Zarvis Status
                                        </h3>

                                    </div>

                                </div>


                                <div className="system-status-row">

                                    <span>
                                        Voice recognition
                                    </span>


                                    <strong>
                                        ACTIVE
                                    </strong>

                                </div>


                                <div className="system-status-row">

                                    <span>
                                        Voice response
                                    </span>


                                    <strong>
                                        ACTIVE
                                    </strong>

                                </div>


                                <div className="system-status-row">

                                    <span>
                                        Zarvis Core
                                    </span>


                                    <strong>
                                        ONLINE
                                    </strong>

                                </div>

                            </section>

                        </aside>

                    </div>

                </div>

            </main>

        </div>
    );
}


export default Assistant;