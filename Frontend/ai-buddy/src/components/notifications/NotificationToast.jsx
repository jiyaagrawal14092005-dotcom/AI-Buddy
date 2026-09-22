import { useEffect, useRef, useState } from "react";

import {
    Bell,
    CheckCircle2,
    Download,
    XCircle,
    CalendarClock,
    Workflow,
    Info,
    LoaderCircle,
    X,
} from "lucide-react";

import { useBuddy } from "../../context/BuddyContext";


function NotificationToast() {

    const {
        notifications,
        markNotificationRead,
    } = useBuddy();


    const [visibleNotification, setVisibleNotification] =
        useState(null);


    const lastShownNotificationId =
        useRef(null);


    const hideTimerRef =
        useRef(null);


    // ==========================================
    // GET NOTIFICATION ICON
    // ==========================================

    function getNotificationIcon(notification) {

        const iconType =
            notification?.icon ||
            notification?.type ||
            "info";


        if (iconType === "download") {

            return (
                <Download size={20} />
            );
        }


        if (
            iconType === "success" ||
            notification?.type === "success"
        ) {

            return (
                <CheckCircle2 size={20} />
            );
        }


        if (
            iconType === "error" ||
            notification?.type === "error" ||
            notification?.type === "failed"
        ) {

            return (
                <XCircle size={20} />
            );
        }


        if (
            iconType === "reminder" ||
            notification?.type === "reminder"
        ) {

            return (
                <CalendarClock size={20} />
            );
        }


        if (
            iconType === "workflow" ||
            notification?.type === "workflow"
        ) {

            return (
                <Workflow size={20} />
            );
        }


        if (
            iconType === "loading" ||
            notification?.type === "loading"
        ) {

            return (
                <LoaderCircle size={20} />
            );
        }


        return (
            <Info size={20} />
        );
    }


    // ==========================================
    // SHOW NEW NOTIFICATION
    // ==========================================

    useEffect(() => {

        if (
            !notifications ||
            notifications.length === 0
        ) {
            return;
        }


        const latestNotification =
            notifications[0];


        if (
            !latestNotification?.id
        ) {
            return;
        }


        // Do not show the same notification repeatedly.
        if (
            lastShownNotificationId.current ===
            latestNotification.id
        ) {
            return;
        }


        lastShownNotificationId.current =
            latestNotification.id;


        setVisibleNotification(
            latestNotification
        );


        // Clear an existing timer.
        if (hideTimerRef.current) {

            clearTimeout(
                hideTimerRef.current
            );
        }


        // Automatically hide popup after 5 seconds.
        hideTimerRef.current =
            setTimeout(() => {

                setVisibleNotification(
                    null
                );

            }, 5000);


        return () => {

            if (hideTimerRef.current) {

                clearTimeout(
                    hideTimerRef.current
                );
            }

        };

    }, [notifications]);


    // ==========================================
    // CLEANUP
    // ==========================================

    useEffect(() => {

        return () => {

            if (hideTimerRef.current) {

                clearTimeout(
                    hideTimerRef.current
                );
            }

        };

    }, []);


    // ==========================================
    // CLOSE POPUP
    // ==========================================

    function closeNotification() {

        if (
            hideTimerRef.current
        ) {

            clearTimeout(
                hideTimerRef.current
            );
        }


        if (
            visibleNotification?.id
        ) {

            markNotificationRead(
                visibleNotification.id
            );
        }


        setVisibleNotification(
            null
        );
    }


    // ==========================================
    // NO ACTIVE POPUP
    // ==========================================

    if (!visibleNotification) {
        return null;
    }


    // ==========================================
    // POPUP
    // ==========================================

    return (

        <div
            style={{
                position: "fixed",
                top: "80px",
                right: "24px",
                width: "360px",
                maxWidth: "calc(100vw - 32px)",
                zIndex: 99999,
                background: "rgba(15, 23, 42, 0.97)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                borderRadius: "16px",
                boxShadow:
                    "0 20px 50px rgba(0, 0, 0, 0.35)",
                backdropFilter: "blur(16px)",
                overflow: "hidden",
                animation:
                    "zarvisNotificationSlideIn 0.3s ease-out",
            }}
        >

            {/* ==========================================
                TOP ACCENT
            ========================================== */}

            <div
                style={{
                    height: "3px",
                    width: "100%",
                    background:
                        visibleNotification.type === "error" ||
                        visibleNotification.type === "failed"
                            ? "#ef4444"
                            : "#22c55e",
                }}
            />


            <div
                style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: "13px",
                    padding: "16px",
                }}
            >

                {/* ==========================================
                    ICON
                ========================================== */}

                <div
                    style={{
                        width: "42px",
                        height: "42px",
                        minWidth: "42px",
                        borderRadius: "12px",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        background:
                            visibleNotification.type === "error" ||
                            visibleNotification.type === "failed"
                                ? "rgba(239, 68, 68, 0.14)"
                                : "rgba(34, 197, 94, 0.14)",
                        color:
                            visibleNotification.type === "error" ||
                            visibleNotification.type === "failed"
                                ? "#f87171"
                                : "#4ade80",
                    }}
                >

                    {getNotificationIcon(
                        visibleNotification
                    )}

                </div>


                {/* ==========================================
                    CONTENT
                ========================================== */}

                <div
                    style={{
                        flex: 1,
                        minWidth: 0,
                    }}
                >

                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            gap: "8px",
                        }}
                    >

                        <strong
                            style={{
                                color: "#ffffff",
                                fontSize: "14px",
                                fontWeight: 600,
                                lineHeight: 1.4,
                            }}
                        >
                            {visibleNotification.title ||
                                "Zarvis Notification"}
                        </strong>


                        <button
                            type="button"
                            onClick={
                                closeNotification
                            }
                            aria-label="Close notification"
                            style={{
                                border: "none",
                                background: "transparent",
                                color: "#94a3b8",
                                cursor: "pointer",
                                padding: "2px",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                            }}
                        >

                            <X size={16} />

                        </button>

                    </div>


                    <p
                        style={{
                            margin: "5px 0 0",
                            color: "#cbd5e1",
                            fontSize: "13px",
                            lineHeight: 1.5,
                            wordBreak: "break-word",
                        }}
                    >
                        {visibleNotification.message ||
                            visibleNotification.description ||
                            "Zarvis has a new update for you."}
                    </p>


                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "6px",
                            marginTop: "9px",
                            color: "#64748b",
                            fontSize: "11px",
                        }}
                    >

                        <Bell size={12} />

                        <span>
                            Zarvis
                        </span>

                    </div>

                </div>

            </div>

        </div>
    );
}


export default NotificationToast;