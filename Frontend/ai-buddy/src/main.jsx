import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

import "./styles/variables.css";
import "./styles/global.css";
import "./styles/layout.css";
import "./styles/components.css";
import "./styles/dashboard.css";
import "./styles/robot.css";
import "./styles/assistant.css";
import "./styles/memory.css";
import "./styles/activity.css";
import "./styles/integrations.css";
import "./styles/security.css";
import "./styles/settings.css";
import "./styles/workflows.css";
import "./styles/schedule.css";
import "./styles/navbar.css";
import "./styles/auth.css";
ReactDOM.createRoot(
  document.getElementById("root")
).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);