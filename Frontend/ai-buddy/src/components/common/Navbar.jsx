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
} from "lucide-react";

import { useAuth } from "../../context/AuthContext";


function Navbar() {
    const navigate = useNavigate();

    const { user, logout } = useAuth();

    const [showNotifications, setShowNotifications] = useState(false);
    const [showAccount, setShowAccount] = useState(false);
    const [isLoggingOut, setIsLoggingOut] = useState(false);

    const notificationRef = useRef(null);
    const accountRef = useRef(null);


    useEffect(() => {
        function handleOutsideClick(event) {

            if (
                notificationRef.current &&
                !notificationRef.current.contains(event.target)
            ) {
                setShowNotifications(false);
            }

            if (
                accountRef.current &&
                !accountRef.current.contains(event.target)
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


    function toggleNotifications() {

        setShowNotifications(
            (value) => !value
        );

        setShowAccount(false);
    }


    function toggleAccount() {

        setShowAccount(
            (value) => !value
        );

        setShowNotifications(false);
    }


    function goToPage(path) {

        setShowNotifications(false);
        setShowAccount(false);

        navigate(path);
    }


    async function handleLogout() {

        if (isLoggingOut) {
            return;
        }

        setIsLoggingOut(true);

        try {

            await logout();

            setShowAccount(false);
            setShowNotifications(false);

            navigate("/login", {
                replace: true,
            });

        } catch (error) {

            console.error(
                "Logout failed:",
                error
            );

        } finally {

            setIsLoggingOut(false);
        }
    }


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
                        onClick={toggleNotifications}
                    >
                        <Bell size={18} />

                        <span className="zarvis-notification-dot"></span>
                    </button>


                    {showNotifications && (

                        <div className="zarvis-notification-panel">

                            <div className="notification-panel-header">

                                <div>
                                    <strong>
                                        Notifications
                                    </strong>

                                    <span>
                                        Recent updates
                                    </span>
                                </div>

                                <button
                                    type="button"
                                >
                                    Mark all read
                                </button>

                            </div>


                            <div className="notification-item">

                                <div className="notification-icon">
                                    <CheckCircle2 size={17} />
                                </div>

                                <div className="notification-content">

                                    <strong>
                                        Task completed
                                    </strong>

                                    <span>
                                        Your study task was completed.
                                    </span>

                                </div>

                                <small>
                                    8 min ago
                                </small>

                            </div>


                            <div className="notification-item">

                                <div className="notification-icon">
                                    <CalendarClock size={17} />
                                </div>

                                <div className="notification-content">

                                    <strong>
                                        Reminder
                                    </strong>

                                    <span>
                                        Your upcoming schedule is ready.
                                    </span>

                                </div>

                                <small>
                                    20 min ago
                                </small>

                            </div>


                            <div className="notification-item">

                                <div className="notification-icon">
                                    <Workflow size={17} />
                                </div>

                                <div className="notification-content">

                                    <strong>
                                        Workflow update
                                    </strong>

                                    <span>
                                        Your workflow has been updated.
                                    </span>

                                </div>

                                <small>
                                    1 hr ago
                                </small>

                            </div>


                            <button
                                type="button"
                                className="notification-view-all"
                                onClick={() =>
                                    goToPage("/activity")
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
                        onClick={toggleAccount}
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


                            <button
                                type="button"
                                onClick={() =>
                                    goToPage("/settings")
                                }
                            >
                                <User size={17} />

                                <span>
                                    Profile
                                </span>

                            </button>


                            <button
                                type="button"
                                onClick={() =>
                                    goToPage("/settings")
                                }
                            >
                                <Settings size={17} />

                                <span>
                                    Settings
                                </span>

                            </button>


                            <button
                                type="button"
                                onClick={() =>
                                    goToPage("/integrations")
                                }
                            >
                                <Plug size={17} />

                                <span>
                                    Integrations
                                </span>

                            </button>


                            <button
                                type="button"
                                onClick={() =>
                                    goToPage("/activity")
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
                                onClick={handleLogout}
                                disabled={isLoggingOut}
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