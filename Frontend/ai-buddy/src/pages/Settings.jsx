import { useState } from "react";
import {
    User,
    Bell,
    Palette,
    ShieldCheck,
    Mic,
    Volume2,
    Moon,
    Save,
    RotateCcw,
} from "lucide-react";

import Sidebar from "../components/common/Sidebar";
import { useAuth } from "../context/AuthContext";


function Settings() {

    const {
        user,
        updateProfile,
    } = useAuth();


    const [notifications, setNotifications] = useState(true);
    const [voiceAssistant, setVoiceAssistant] = useState(true);
    const [soundEffects, setSoundEffects] = useState(true);
    const [darkMode, setDarkMode] = useState(true);

    const [name, setName] = useState(
        user?.username || ""
    );

    const [saved, setSaved] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");


    // --------------------------------------
    // SAVE SETTINGS
    // --------------------------------------

    const handleSave = async () => {

        setError("");

        const trimmedName = name.trim();

        if (!trimmedName) {

            setError(
                "Please enter your name."
            );

            return;
        }

        try {

            setSaving(true);

            await updateProfile(
                trimmedName
            );

            setSaved(true);

            setTimeout(() => {
                setSaved(false);
            }, 2000);

        } catch (error) {

            console.error(
                "Profile update failed:",
                error
            );

            setError(
                error?.message ||
                "Failed to update profile."
            );

        } finally {

            setSaving(false);
        }
    };


    // --------------------------------------
    // RESET SETTINGS
    // --------------------------------------

    const handleReset = () => {

        setNotifications(true);
        setVoiceAssistant(true);
        setSoundEffects(true);
        setDarkMode(true);

        setName(
            user?.username || ""
        );

        setSaved(false);
        setError("");
    };


    return (
        <div className="app">

            {/* SIDEBAR */}
            <Sidebar />


            {/* MAIN CONTENT */}
            <main className="main-content">

                <div className="settings-page">


                    {/* HEADER */}
                    <div className="settings-header">

                        <div>

                            <span className="settings-eyebrow">
                                SYSTEM CONFIGURATION // 08
                            </span>

                            <h1>Settings</h1>

                            <p>
                                Customize how Zarvis works for you.
                            </p>

                        </div>


                        <div className="settings-status">

                            <span></span>

                            CONFIGURATION READY

                        </div>

                    </div>


                    {/* PROFILE */}
                    <section className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon">
                                <User size={17} />
                            </div>

                            <div>

                                <span>PROFILE</span>

                                <h2>
                                    Personal Information
                                </h2>

                            </div>

                        </div>


                        <div className="settings-divider"></div>


                        <div className="settings-form-grid">


                            {/* NAME */}
                            <div className="settings-field">

                                <label>NAME</label>

                                <input
                                    type="text"
                                    value={name}
                                    onChange={(event) =>
                                        setName(
                                            event.target.value
                                        )
                                    }
                                    placeholder="Enter your name"
                                />

                            </div>


                            {/* WORKSPACE */}
                            <div className="settings-field">

                                <label>
                                    WORKSPACE
                                </label>

                                <input
                                    type="text"
                                    defaultValue="Personal Workspace"
                                    placeholder="Workspace name"
                                />

                            </div>


                            {/* ABOUT YOU */}
                            <div className="settings-field full-field">

                                <label>
                                    ABOUT YOU
                                </label>

                                <textarea
                                    defaultValue="BCA student working on AI and Machine Learning projects."
                                    rows="3"
                                />

                            </div>

                        </div>

                    </section>


                    {/* ASSISTANT SETTINGS */}
                    <section className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon cyan">
                                <Mic size={17} />
                            </div>

                            <div>

                                <span>ASSISTANT</span>

                                <h2>
                                    Zarvis Behavior
                                </h2>

                            </div>

                        </div>


                        <div className="settings-divider"></div>


                        <div className="settings-option-list">


                            {/* VOICE ASSISTANT */}
                            <div className="settings-option">

                                <div className="settings-option-icon">
                                    <Mic size={16} />
                                </div>


                                <div className="settings-option-content">

                                    <strong>
                                        Voice Assistant
                                    </strong>

                                    <span>
                                        Allow Zarvis to listen and respond
                                        using voice.
                                    </span>

                                </div>


                                <button
                                    type="button"
                                    className={`settings-toggle ${
                                        voiceAssistant
                                            ? "active"
                                            : ""
                                    }`}
                                    onClick={() =>
                                        setVoiceAssistant(
                                            !voiceAssistant
                                        )
                                    }
                                    aria-label="Toggle Voice Assistant"
                                >
                                    <span></span>
                                </button>

                            </div>


                            {/* SOUND EFFECTS */}
                            <div className="settings-option">

                                <div className="settings-option-icon">
                                    <Volume2 size={16} />
                                </div>


                                <div className="settings-option-content">

                                    <strong>
                                        Sound Effects
                                    </strong>

                                    <span>
                                        Play subtle sounds for important
                                        Zarvis actions.
                                    </span>

                                </div>


                                <button
                                    type="button"
                                    className={`settings-toggle ${
                                        soundEffects
                                            ? "active"
                                            : ""
                                    }`}
                                    onClick={() =>
                                        setSoundEffects(
                                            !soundEffects
                                        )
                                    }
                                    aria-label="Toggle Sound Effects"
                                >
                                    <span></span>
                                </button>

                            </div>

                        </div>

                    </section>


                    {/* NOTIFICATIONS */}
                    <section className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon purple">
                                <Bell size={17} />
                            </div>

                            <div>

                                <span>
                                    NOTIFICATIONS
                                </span>

                                <h2>
                                    Alerts & Reminders
                                </h2>

                            </div>

                        </div>


                        <div className="settings-divider"></div>


                        <div className="settings-option-list">

                            <div className="settings-option">

                                <div className="settings-option-icon">
                                    <Bell size={16} />
                                </div>


                                <div className="settings-option-content">

                                    <strong>
                                        Notifications
                                    </strong>

                                    <span>
                                        Receive reminders, task updates
                                        and alerts.
                                    </span>

                                </div>


                                <button
                                    type="button"
                                    className={`settings-toggle ${
                                        notifications
                                            ? "active"
                                            : ""
                                    }`}
                                    onClick={() =>
                                        setNotifications(
                                            !notifications
                                        )
                                    }
                                    aria-label="Toggle Notifications"
                                >
                                    <span></span>
                                </button>

                            </div>

                        </div>

                    </section>


                    {/* APPEARANCE */}
                    <section className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon pink">
                                <Palette size={17} />
                            </div>

                            <div>

                                <span>
                                    APPEARANCE
                                </span>

                                <h2>
                                    Interface Preferences
                                </h2>

                            </div>

                        </div>


                        <div className="settings-divider"></div>


                        <div className="settings-option-list">

                            <div className="settings-option">

                                <div className="settings-option-icon">
                                    <Moon size={16} />
                                </div>


                                <div className="settings-option-content">

                                    <strong>
                                        Dark Interface
                                    </strong>

                                    <span>
                                        Keep the futuristic dark Zarvis
                                        interface enabled.
                                    </span>

                                </div>


                                <button
                                    type="button"
                                    className={`settings-toggle ${
                                        darkMode
                                            ? "active"
                                            : ""
                                    }`}
                                    onClick={() =>
                                        setDarkMode(
                                            !darkMode
                                        )
                                    }
                                    aria-label="Toggle Dark Interface"
                                >
                                    <span></span>
                                </button>

                            </div>

                        </div>

                    </section>


                    {/* SECURITY */}
                    <section className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon green">
                                <ShieldCheck size={17} />
                            </div>

                            <div>

                                <span>
                                    SECURITY
                                </span>

                                <h2>
                                    Privacy & Protection
                                </h2>

                            </div>

                        </div>


                        <div className="settings-divider"></div>


                        <div className="security-setting-status">

                            <div className="security-setting-icon">
                                <ShieldCheck size={18} />
                            </div>


                            <div>

                                <strong>
                                    SECURITY SYSTEM ACTIVE
                                </strong>

                                <span>
                                    Your Zarvis workspace is protected.
                                </span>

                            </div>


                            <div className="security-active">

                                <span></span>

                                ACTIVE

                            </div>

                        </div>

                    </section>


                    {/* ERROR MESSAGE */}
                    {error && (
                        <div
                            style={{
                                marginTop: "12px",
                                color: "#ff6b6b",
                                fontSize: "13px",
                            }}
                        >
                            {error}
                        </div>
                    )}


                    {/* BOTTOM ACTIONS */}
                    <div className="settings-actions">


                        <button
                            type="button"
                            className="settings-reset"
                            onClick={handleReset}
                            disabled={saving}
                        >

                            <RotateCcw size={15} />

                            RESET

                        </button>


                        <button
                            type="button"
                            className="settings-save"
                            onClick={handleSave}
                            disabled={saving}
                        >

                            <Save size={15} />

                            {saving
                                ? "SAVING..."
                                : saved
                                    ? "SAVED"
                                    : "SAVE CHANGES"
                            }

                        </button>

                    </div>


                </div>

            </main>

        </div>
    );
}


export default Settings;