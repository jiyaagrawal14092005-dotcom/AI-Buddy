import { BrowserRouter, Routes, Route } from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
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

function App() {
  return (
    <AuthProvider>
      <BuddyProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
<Route path="/signup" element={<Signup />} />
            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/assistant"
              element={<Assistant />}
            />

            <Route
              path="/tasks"
              element={<Tasks />}
            />

            <Route
              path="/schedule"
              element={<Schedule />}
            />

            <Route
              path="/workflows"
              element={<Workflows />}
            />

            <Route
              path="/activity"
              element={<Activity />}
            />

            <Route
              path="/integrations"
              element={<Integrations />}
            />

            <Route
              path="/memory"
              element={<Memory />}
            />

            <Route
              path="/security"
              element={<Security />}
            />

            <Route
              path="/settings"
              element={<Settings />}
            />
          </Routes>
        </BrowserRouter>
      </BuddyProvider>
    </AuthProvider>
  );
}

export default App;