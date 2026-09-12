import { useState } from "react";
import {
    ShieldCheck,
    Lock,
    KeyRound,
    Smartphone,
    Eye,
    CheckCircle2,
    AlertTriangle,
} from "lucide-react";

function Security() {
    const [twoFactor, setTwoFactor] = useState(false);
    const [activityAlerts, setActivityAlerts] = useState(true);

    return (
        <div className="page-container">

            {/* HEADER */}
            <div className="page-header">
                <div>
                    <span className="page-eyebrow">
                        ZARVIS SECURITY
                    </span>

                    <h1>Security</h1>

                    <p>
                        Manage your security and privacy preferences.
                    </p>
                </div>

                <div className="security-status">
                    <span className="security-status-dot"></span>
                    Protected
                </div>
            </div>

            {/* SECURITY OVERVIEW */}
            <div className="security-overview">

                <div className="glass-card security-overview-card">
                    <div className="security-big-icon">
                        <ShieldCheck size={23} />
                    </div>

                    <div>
                        <span>Security Status</span>
                        <strong>Protected</strong>
                    </div>
                </div>

                <div className="glass-card security-overview-card">
                    <div className="security-big-icon">
                        <Lock size={23} />
                    </div>

                    <div>
                        <span>Data Protection</span>
                        <strong>Enabled</strong>
                    </div>
                </div>

                <div className="glass-card security-overview-card">
                    <div className="security-big-icon">
                        <Eye size={23} />
                    </div>

                    <div>
                        <span>Privacy</span>
                        <strong>Private</strong>
                    </div>
                </div>

            </div>

            {/* SECURITY SETTINGS */}
            <section className="glass-card security-card">

                <div className="card-header">
                    <div>
                        <h2>Security Settings</h2>
                        <p>Control how your Zarvis account is protected.</p>
                    </div>

                    <ShieldCheck size={21} />
                </div>

                <div className="security-list">

                    {/* TWO FACTOR */}
                    <div className="security-item">

                        <div className="security-item-icon">
                            <KeyRound size={19} />
                        </div>

                        <div className="security-item-info">
                            <strong>Two-Factor Authentication</strong>
                            <p>
                                Add an extra layer of protection to your account.
                            </p>
                        </div>

                        <button
                            className={`security-toggle ${twoFactor ? "enabled" : ""
                                }`}
                            onClick={() => setTwoFactor(!twoFactor)}
                        >
                            <span></span>
                        </button>

                    </div>

                    {/* ACTIVITY ALERTS */}
                    <div className="security-item">

                        <div className="security-item-icon">
                            <Smartphone size={19} />
                        </div>

                        <div className="security-item-info">
                            <strong>Activity Alerts</strong>
                            <p>
                                Get notified about important account activity.
                            </p>
                        </div>

                        <button
                            className={`security-toggle ${activityAlerts ? "enabled" : ""
                                }`}
                            onClick={() =>
                                setActivityAlerts(!activityAlerts)
                            }
                        >
                            <span></span>
                        </button>

                    </div>

                    {/* DATA PRIVACY */}
                    <div className="security-item">

                        <div className="security-item-icon">
                            <Eye size={19} />
                        </div>

                        <div className="security-item-info">
                            <strong>Private Data</strong>
                            <p>
                                Your saved memories and personal data stay private.
                            </p>
                        </div>

                        <span className="security-enabled">
                            <CheckCircle2 size={15} />
                            Enabled
                        </span>

                    </div>

                </div>

            </section>

            {/* SECURITY NOTICE */}
            <div className="security-notice">

                <div className="security-notice-icon">
                    <AlertTriangle size={18} />
                </div>

                <div>
                    <strong>Security reminder</strong>

                    <p>
                        Never share your password or authentication codes
                        with anyone.
                    </p>
                </div>

            </div>

        </div>
    );
}

export default Security;