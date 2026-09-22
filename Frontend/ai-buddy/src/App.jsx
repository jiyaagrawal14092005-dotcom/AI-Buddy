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



/* ==========================================
   PROTECTED ROUTE
========================================== */

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



/* ==========================================
   PUBLIC ROUTE
========================================== */

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



/* ==========================================
   APP
========================================== */

function App() {

    return (

        <AuthProvider>

            <BuddyProvider>

                <BrowserRouter>

                    <GlobalVoiceAssistant />


                    <Routes>


                        {/* ==========================================
                            PUBLIC ROUTES
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
                            PROTECTED ROUTES
                        ========================================== */}

                        <Route
                            path="/"
                            element={
                                <ProtectedRoute>
                                    <Dashboard />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/assistant"
                            element={
                                <ProtectedRoute>
                                    <Assistant />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/tasks"
                            element={
                                <ProtectedRoute>
                                    <Tasks />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/schedule"
                            element={
                                <ProtectedRoute>
                                    <Schedule />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/workflows"
                            element={
                                <ProtectedRoute>
                                    <Workflows />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/activity"
                            element={
                                <ProtectedRoute>
                                    <Activity />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/integrations"
                            element={
                                <ProtectedRoute>
                                    <Integrations />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/memory"
                            element={
                                <ProtectedRoute>
                                    <Memory />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/security"
                            element={
                                <ProtectedRoute>
                                    <Security />
                                </ProtectedRoute>
                            }
                        />


                        <Route
                            path="/settings"
                            element={
                                <ProtectedRoute>
                                    <Settings />
                                </ProtectedRoute>
                            }
                        />


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