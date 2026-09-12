import { BrowserRouter, Routes, Route } from "react-router-dom";

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

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* MAIN */}
        <Route path="/" element={<Dashboard />} />

        {/* WORKSPACE */}
        <Route path="/assistant" element={<Assistant />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/schedule" element={<Schedule />} />
        <Route path="/workflows" element={<Workflows />} />
        <Route path="/activity" element={<Activity />} />
        <Route path="/memory" element={<Memory />} />

        {/* INTEGRATIONS */}
        <Route
          path="/integrations"
          element={<Integrations />}
        />

        {/* SYSTEM */}
        <Route path="/security" element={<Security />} />
        <Route path="/settings" element={<Settings />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;