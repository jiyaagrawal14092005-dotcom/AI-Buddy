import {
    BrowserRouter,
    Routes,
    Route,
    Navigate,
} from "react-router-dom";

import { AuthProvider, useAuth } from "./context/AuthContext";
import { BuddyProvider } from "./context/BuddyContext";

import Dashboard from "./pages/Dashboard";
import Assistant from "./pages/Assistant";
import Tasks from "./pages/Tasks";
import Schedule from "./pages/Schedule";
import Workflows from "./pages/Workflows";
import Activity from "./pages/Activity";
import Integrations from "./pages/Integrations";
import Memory from "./pages/Memory";
import Security from "./pages/Security";
import Settings from "./pages/Settings";

import Login from "./pages/auth/Login";
import Signup from "./pages/auth/Signup";

import Chat from "./pages/chat";

import GlobalVoiceAssistant from "./components/voice/GlobalVoiceAssistant";
import NotificationToast from "./components/notifications/NotificationToast";


// ==========================================
// PROTECTED ROUTE
// ==========================================

function ProtectedRoute({ children }) {

    const {
        authenticated,
        loading,
    } = useAuth();


    if (loading) {

        return (
            <div
                style={{
                    minHeight: "100vh",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                }}
            >
                Checking authentication...
            </div>
        );
    }


    if (!authenticated) {

        return (
            <Navigate
                to="/login"
                replace
            />
        );
    }


    return children;
}


// ==========================================
// PUBLIC ROUTE
// ==========================================

function PublicRoute({ children }) {

    const {
        authenticated,
        loading,
    } = useAuth();


    if (loading) {

        return (
            <div
                style={{
                    minHeight: "100vh",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                }}
            >
                Loading...
            </div>
        );
    }


    if (authenticated) {

        return (
            <Navigate
                to="/"
                replace
            />
        );
    }


    return children;
}


// ==========================================
// MAIN APP
// ==========================================

function App() {

    return (

        <AuthProvider>

            <BuddyProvider>

                {/* ==========================================
                    GLOBAL NOTIFICATION POPUP

                    This stays mounted globally so the
                    notification system does not belong
                    to only one page.
                ========================================== */}

                <NotificationToast />


                <BrowserRouter>

                    {/* ==========================================
                        GLOBAL VOICE ASSISTANT
                    ========================================== */}

                    <GlobalVoiceAssistant />


                    {/* ==========================================
                        APPLICATION ROUTES
                    ========================================== */}

                    <Routes>


                        {/* ==========================================
                            AUTHENTICATION
                        ========================================== */}

                        <Route
                            path="/login"
                            element={
                                <PublicRoute>
                                    <Login />
                                </PublicRoute>
                            }
                        />


                        <Route
                            path="/signup"
                            element={
                                <PublicRoute>
                                    <Signup />
                                </PublicRoute>
                            }
                        />


                        {/* ==========================================
                            DASHBOARD
                        ========================================== */}

                        <Route
                            path="/"
                            element={
                                <ProtectedRoute>
                                    <Dashboard />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            ASSISTANT
                        ========================================== */}

                        <Route
                            path="/assistant"
                            element={
                                <ProtectedRoute>
                                    <Assistant />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            TASKS
                        ========================================== */}

                        <Route
                            path="/tasks"
                            element={
                                <ProtectedRoute>
                                    <Tasks />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            SCHEDULE
                        ========================================== */}

                        <Route
                            path="/schedule"
                            element={
                                <ProtectedRoute>
                                    <Schedule />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            WORKFLOWS
                        ========================================== */}

                        <Route
                            path="/workflows"
                            element={
                                <ProtectedRoute>
                                    <Workflows />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            ACTIVITY
                        ========================================== */}

                        <Route
                            path="/activity"
                            element={
                                <ProtectedRoute>
                                    <Activity />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            INTEGRATIONS
                        ========================================== */}

                        <Route
                            path="/integrations"
                            element={
                                <ProtectedRoute>
                                    <Integrations />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            MEMORY
                        ========================================== */}

                        <Route
                            path="/memory"
                            element={
                                <ProtectedRoute>
                                    <Memory />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            SECURITY
                        ========================================== */}

                        <Route
                            path="/security"
                            element={
                                <ProtectedRoute>
                                    <Security />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            SETTINGS
                        ========================================== */}

                        <Route
                            path="/settings"
                            element={
                                <ProtectedRoute>
                                    <Settings />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            CHAT
                        ========================================== */}

                        <Route
                            path="/chat"
                            element={
                                <ProtectedRoute>
                                    <Chat />
                                </ProtectedRoute>
                            }
                        />


                        {/* ==========================================
                            UNKNOWN ROUTE
                        ========================================== */}

                        <Route
                            path="*"
                            element={
                                <Navigate
                                    to="/"
                                    replace
                                />
                            }
                        />

                    </Routes>

                </BrowserRouter>

            </BuddyProvider>

        </AuthProvider>
    );
}


export default App;