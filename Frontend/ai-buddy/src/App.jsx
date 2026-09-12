import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Tasks from "./pages/Tasks";
import Schedule from "./pages/Schedule";
import Workflows from "./pages/Workflows";
import Memory from "./pages/Memory";
import Security from "./pages/Security";
import Settings from "./pages/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/schedule" element={<Schedule />} />
        <Route path="/workflows" element={<Workflows />} />
        <Route path="/memory" element={<Memory />} />
        <Route path="/security" element={<Security />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;