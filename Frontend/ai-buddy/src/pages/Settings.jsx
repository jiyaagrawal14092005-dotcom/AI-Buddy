import { useState } from "react";
import {
    Settings as SettingsIcon,
    User,
    Bell,
    Palette,
    MessageCircle,
    Volume2,
    Save,
} from "lucide-react";

function Settings() {
    const [notifications, setNotifications] = useState(true);
    const [sound, setSound] = useState(true);
    const [compactMode, setCompactMode] = useState(false);

    return (
        <div className="page-container">

            {/* HEADER */}
            <div className="page-header">
                <div>
                    <span className="page-eyebrow">
                        ZARVIS SETTINGS
                    </span>

                    <h1>Settings</h1>

                    <p>
                        Customize how Zarvis looks and works for you.
                    </p>
                </div>

                <button className="primary-action">
                    <Save size={18} />
                    Save Changes
                </button>
            </div>

            {/* SETTINGS GRID */}
            <div className="settings-grid">

                {/* PROFILE */}
                <section className="glass-card settings-card">

                    <div className="settings-card-header">
                        <div className="settings-icon">
                            <User size={19} />
                        </div>

                        <div>
                            <h2>Profile</h2>
                            <p>Your basic Zarvis profile.</p>
                        </div>
                    </div>

                    <div className="settings-field">
                        <label>Name</label>

                        <input
                            type="text"
                            placeholder="User"
                            defaultValue="User"
                        />
                    </div>

                    <div className="settings-field">
                        <label>Assistant Name</label>

                        <input
                            type="text"
                            defaultValue="Zarvis"
                        />
                    </div>

                </section>

                {/* APPEARANCE */}
                <section className="glass-card settings-card">

                    <div className="settings-card-header">
                        <div className="settings-icon">
                            <Palette size={19} />
                        </div>

                        <div>
                            <h2>Appearance</h2>
                            <p>Customize the Zarvis interface.</p>
                        </div>
                    </div>

                    <div className="settings-option">

                        <div>
                            <strong>Theme</strong>
                            <span>Dark futuristic theme</span>
                        </div>

                        <div className="theme-preview">
                            Dark
                        </div>

                    </div>

                    <div className="settings-option">

                        <div>
                            <strong>Compact Mode</strong>
                            <span>Use a more compact layout</span>
                        </div>

                        <button
                            className={`settings-toggle ${compactMode ? "enabled" : ""
                                }`}
                            onClick={() => setCompactMode(!compactMode)}
                        >
                            <span></span>
                        </button>

                    </div>

                </section>

                {/* NOTIFICATIONS */}
                <section className="glass-card settings-card">

                    <div className="settings-card-header">
                        <div className="settings-icon">
                            <Bell size={19} />
                        </div>

                        <div>
                            <h2>Notifications</h2>
                            <p>Control Zarvis notifications.</p>
                        </div>
                    </div>

                    <div className="settings-option">

                        <div>
                            <strong>Notifications</strong>
                            <span>Receive important reminders</span>
                        </div>

                        <button
                            className={`settings-toggle ${notifications ? "enabled" : ""
                                }`}
                            onClick={() =>
                                setNotifications(!notifications)
                            }
                        >
                            <span></span>
                        </button>

                    </div>

                    <div className="settings-option">

                        <div>
                            <strong>Sound Effects</strong>
                            <span>Play sounds for interactions</span>
                        </div>

                        <button
                            className={`settings-toggle ${sound ? "enabled" : ""
                                }`}
                            onClick={() => setSound(!sound)}
                        >
                            <span></span>
                        </button>

                    </div>

                </section>

                {/* ASSISTANT */}
                <section className="glass-card settings-card">

                    <div className="settings-card-header">
                        <div className="settings-icon">
                            <MessageCircle size={19} />
                        </div>

                        <div>
                            <h2>Assistant</h2>
                            <p>Configure how Zarvis interacts with you.</p>
                        </div>
                    </div>

                    <div className="settings-option">

                        <div>
                            <strong>Response Style</strong>
                            <span>Friendly and helpful</span>
                        </div>

                        <span className="settings-value">
                            Friendly
                        </span>

                    </div>

                    <div className="settings-option">

                        <div>
                            <strong>Voice</strong>
                            <span>Voice assistant preference</span>
                        </div>

                        <span className="settings-value">
                            Default
                        </span>

                    </div>

                </section>

            </div>

            {/* INFO */}
            <div className="settings-info">

                <Volume2 size={17} />

                <span>
                    More advanced settings will be available when
                    Zarvis is connected to the backend.
                </span>

            </div>

        </div>
    );
}

export default Settings;