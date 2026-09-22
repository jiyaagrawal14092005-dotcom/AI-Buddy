import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    Bell,
    ChevronDown,
    User,
    Settings,
    Plug,
    CircleHelp,
    LogOut,
    CheckCircle2,
    CalendarClock,
    Workflow,
    Info,
    XCircle,
    Download,
    LoaderCircle,
} from "lucide-react";

import { useAuth } from "../../context/AuthContext";
import { useBuddy } from "../../context/BuddyContext";


function Navbar() {

    const navigate = useNavigate();

    const { user, logout } = useAuth();

    const {
        notifications,
        unreadNotificationCount,
        markNotificationRead,
        markAllNotificationsRead,
    } = useBuddy();


    const [showNotifications, setShowNotifications] =
        useState(false);

    const [showAccount, setShowAccount] =
        useState(false);

    const [isLoggingOut, setIsLoggingOut] =
        useState(false);


    const notificationRef = useRef(null);
    const accountRef = useRef(null);


    // ==========================================
    // CLOSE DROPDOWNS WHEN CLICKING OUTSIDE
    // ==========================================

    useEffect(() => {

        function handleOutsideClick(event) {

            if (
                notificationRef.current &&
                !notificationRef.current.contains(
                    event.target
                )
            ) {
                setShowNotifications(false);
            }


            if (
                accountRef.current &&
                !accountRef.current.contains(
                    event.target
                )
            ) {
                setShowAccount(false);
            }
        }


        document.addEventListener(
            "mousedown",
            handleOutsideClick
        );


        return () => {

            document.removeEventListener(
                "mousedown",
                handleOutsideClick
            );

        };

    }, []);


    // ==========================================
    // TOGGLE NOTIFICATIONS
    // ==========================================

    function toggleNotifications() {

        setShowNotifications(
            (value) => !value
        );

        setShowAccount(false);
    }


    // ==========================================
    // TOGGLE ACCOUNT
    // ==========================================

    function toggleAccount() {

        setShowAccount(
            (value) => !value
        );

        setShowNotifications(false);
    }


    // ==========================================
    // NAVIGATION
    // ==========================================

    function goToPage(path) {

        setShowNotifications(false);
        setShowAccount(false);

        navigate(path);
    }


    // ==========================================
    // LOGOUT
    // ==========================================

    async function handleLogout() {

        if (isLoggingOut) {
            return;
        }


        setIsLoggingOut(true);


        try {

            await logout();


            setShowAccount(false);
            setShowNotifications(false);


            navigate(
                "/login",
                {
                    replace: true,
                }
            );

        } catch (error) {

            console.error(
                "Logout failed:",
                error
            );

        } finally {

            setIsLoggingOut(false);
        }
    }


    // ==========================================
    // NOTIFICATION ICON
    // ==========================================

    function getNotificationIcon(notification) {

        const iconType =
            notification?.icon ||
            notification?.type ||
            "info";


        if (
            iconType === "download"
        ) {
            return (
                <Download size={17} />
            );
        }


        if (
            iconType === "success" ||
            notification?.type === "success"
        ) {
            return (
                <CheckCircle2 size={17} />
            );
        }


        if (
            iconType === "error" ||
            notification?.type === "error" ||
            notification?.type === "failed"
        ) {
            return (
                <XCircle size={17} />
            );
        }


        if (
            iconType === "workflow" ||
            notification?.type === "workflow"
        ) {
            return (
                <Workflow size={17} />
            );
        }


        if (
            iconType === "reminder" ||
            notification?.type === "reminder"
        ) {
            return (
                <CalendarClock size={17} />
            );
        }


        if (
            iconType === "loading" ||
            notification?.type === "loading"
        ) {
            return (
                <LoaderCircle size={17} />
            );
        }


        return (
            <Info size={17} />
        );
    }


    // ==========================================
    // NOTIFICATION TIME
    //
    // IMPORTANT:
    // Do not use Date.now() here because this
    // function is called while rendering.
    // ==========================================

    function formatNotificationTime(createdAt) {

        if (!createdAt) {
            return "";
        }


        const date =
            new Date(createdAt);


        if (
            Number.isNaN(
                date.getTime()
            )
        ) {
            return "";
        }


        return new Intl.DateTimeFormat(
            "en-IN",
            {
                day: "2-digit",
                month: "short",
                hour: "2-digit",
                minute: "2-digit",
            }
        ).format(date);
    }


    // ==========================================
    // LATEST / CURRENT NOTIFICATION
    //
    // Only ONE notification is shown
    // inside the bell dropdown.
    // ==========================================

    const latestNotification =
        notifications.length > 0
            ? notifications[0]
            : null;


    // ==========================================
    // NOTIFICATION CLICK
    // ==========================================

    function handleNotificationClick(
        notification
    ) {

        if (
            notification?.id
        ) {

            markNotificationRead(
                notification.id
            );

        }
    }


    // ==========================================
    // ACCOUNT DISPLAY
    // ==========================================

    const displayName =
        user?.username ||
        user?.email ||
        "User";


    const avatarLetter =
        displayName
            .charAt(0)
            .toUpperCase();


    return (

        <header className="zarvis-navbar">

            <div className="zarvis-navbar-actions">


                {/* ==========================================
                    NOTIFICATIONS
                ========================================== */}

                <div
                    className="zarvis-notification-wrapper"
                    ref={notificationRef}
                >

                    <button
                        type="button"
                        className="zarvis-notification-button"
                        aria-label="Notifications"
                        onClick={
                            toggleNotifications
                        }
                    >

                        <Bell size={18} />


                        {unreadNotificationCount > 0 && (

                            <span className="zarvis-notification-dot">

                                {unreadNotificationCount > 9
                                    ? "9+"
                                    : unreadNotificationCount}

                            </span>

                        )}

                    </button>


                    {showNotifications && (

                        <div className="zarvis-notification-panel">


                            {/* ==========================================
                                NOTIFICATION HEADER
                            ========================================== */}

                            <div className="notification-panel-header">

                                <div>

                                    <strong>
                                        Notifications
                                    </strong>

                                    <span>
                                        {unreadNotificationCount > 0
                                            ? `${unreadNotificationCount} unread`
                                            : "You're all caught up"}
                                    </span>

                                </div>


                                {notifications.length > 0 && (

                                    <button
                                        type="button"
                                        onClick={
                                            markAllNotificationsRead
                                        }
                                    >
                                        Mark all read
                                    </button>

                                )}

                            </div>


                            {/* ==========================================
                                ONLY CURRENT / LATEST NOTIFICATION
                            ========================================== */}

                            <div className="zarvis-notification-list">

                                {latestNotification ? (

                                    <button
                                        type="button"
                                        className={`notification-item ${
                                            latestNotification.read
                                                ? "notification-read"
                                                : "notification-unread"
                                        }`}
                                        onClick={() =>
                                            handleNotificationClick(
                                                latestNotification
                                            )
                                        }
                                    >

                                        <div className="notification-icon">

                                            {getNotificationIcon(
                                                latestNotification
                                            )}

                                        </div>


                                        <div className="notification-content">

                                            <strong>
                                                {
                                                    latestNotification.title
                                                }
                                            </strong>


                                            <span>
                                                {
                                                    latestNotification.message
                                                }
                                            </span>

                                        </div>


                                        <small>
                                            {
                                                formatNotificationTime(
                                                    latestNotification.createdAt
                                                )
                                            }
                                        </small>

                                    </button>

                                ) : (

                                    <div className="notification-empty">

                                        <div className="notification-empty-icon">

                                            <Bell
                                                size={20}
                                            />

                                        </div>


                                        <strong>
                                            No notifications
                                        </strong>


                                        <span>
                                            Zarvis updates will appear here.
                                        </span>

                                    </div>

                                )}

                            </div>


                            {/* ==========================================
                                VIEW ALL NOTIFICATIONS
                            ========================================== */}

                            <button
                                type="button"
                                className="notification-view-all"
                                onClick={() =>
                                    goToPage(
                                        "/activity"
                                    )
                                }
                            >
                                View all notifications →
                            </button>

                        </div>

                    )}

                </div>


                {/* ==========================================
                    ACCOUNT
                ========================================== */}

                <div
                    className="zarvis-account-wrapper"
                    ref={accountRef}
                >

                    <button
                        type="button"
                        className="zarvis-account-button"
                        onClick={
                            toggleAccount
                        }
                    >

                        <div className="zarvis-avatar">
                            {avatarLetter}
                        </div>


                        <div className="zarvis-account-info">

                            <strong>
                                {displayName}
                            </strong>


                            <span>
                                Personal Workspace
                            </span>

                        </div>


                        <ChevronDown
                            size={15}
                            className={
                                showAccount
                                    ? "account-chevron-open"
                                    : ""
                            }
                        />

                    </button>


                    {showAccount && (

                        <div className="zarvis-account-menu">


                            {/* ==========================================
                                ACCOUNT PROFILE
                            ========================================== */}

                            <div className="account-menu-profile">

                                <div className="account-menu-avatar">
                                    {avatarLetter}
                                </div>


                                <div>

                                    <strong>
                                        {displayName}
                                    </strong>


                                    <span>
                                        Personal Workspace
                                    </span>

                                </div>

                            </div>


                            {/* ==========================================
                                PROFILE
                            ========================================== */}

                            <button
                                type="button"
                                onClick={() =>
                                    goToPage(
                                        "/settings"
                                    )
                                }
                            >

                                <User size={17} />

                                <span>
                                    Profile
                                </span>

                            </button>


                            {/* ==========================================
                                SETTINGS
                            ========================================== */}

                            <button
                                type="button"
                                onClick={() =>
                                    goToPage(
                                        "/settings"
                                    )
                                }
                            >

                                <Settings size={17} />

                                <span>
                                    Settings
                                </span>

                            </button>


                            {/* ==========================================
                                INTEGRATIONS
                            ========================================== */}

                            <button
                                type="button"
                                onClick={() =>
                                    goToPage(
                                        "/integrations"
                                    )
                                }
                            >

                                <Plug size={17} />

                                <span>
                                    Integrations
                                </span>

                            </button>


                            {/* ==========================================
                                HELP & SUPPORT
                            ========================================== */}

                            <button
                                type="button"
                                onClick={() =>
                                    goToPage(
                                        "/activity"
                                    )
                                }
                            >

                                <CircleHelp size={17} />

                                <span>
                                    Help & Support
                                </span>

                            </button>


                            <div className="account-menu-divider"></div>


                            {/* ==========================================
                                REAL LOGOUT
                            ========================================== */}

                            <button
                                type="button"
                                className="account-logout"
                                onClick={
                                    handleLogout
                                }
                                disabled={
                                    isLoggingOut
                                }
                            >

                                <LogOut size={17} />

                                <span>
                                    {isLoggingOut
                                        ? "Logging out..."
                                        : "Logout"}
                                </span>

                            </button>

                        </div>

                    )}

                </div>

            </div>

        </header>
    );
}


export default Navbar;