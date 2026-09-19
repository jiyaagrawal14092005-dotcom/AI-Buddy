import {
    ShieldCheck,
    Lock,
    KeyRound,
    Smartphone,
    CheckCircle2,
    AlertTriangle,
    Activity,
    Eye,
    Database,
    RefreshCw,
} from "lucide-react";

import Sidebar from "../components/common/Sidebar";

const securityItems = [
    {
        title: "Data Encryption",
        description: "Your stored data is protected with secure encryption.",
        status: "SECURE",
        icon: Lock,
    },
    {
        title: "API Security",
        description: "API requests are monitored and protected.",
        status: "SECURE",
        icon: KeyRound,
    },
    {
        title: "Device Access",
        description: "Only verified devices can access your Zarvis workspace.",
        status: "VERIFIED",
        icon: Smartphone,
    },
    {
        title: "Privacy Controls",
        description: "Your personal data and preferences remain under your control.",
        status: "ACTIVE",
        icon: Eye,
    },
];

const securityEvents = [
    {
        title: "Workspace security check completed",
        description: "All security systems are operating normally.",
        time: "09:42 AM",
        icon: ShieldCheck,
    },
    {
        title: "Device verification successful",
        description: "Your current device has been verified.",
        time: "08:15 AM",
        icon: Smartphone,
    },
    {
        title: "Privacy settings reviewed",
        description: "Security and privacy controls are active.",
        time: "07:30 AM",
        icon: Eye,
    },
];

function Security() {
    return (
        <div className="app">
            <Sidebar />

            <main className="main-content">
                <div className="security-page">

                    {/* HEADER */}
                    <header className="security-page-header">
                        <div>
                            <span className="security-page-label">
                                SECURITY CENTER // 06
                            </span>

                            <h1>Security & Privacy</h1>

                            <p>
                                Monitor your Zarvis workspace security,
                                privacy and access controls.
                            </p>
                        </div>

                        <div className="security-header-status">
                            <span></span>
                            ALL SYSTEMS SECURE
                        </div>
                    </header>

                    {/* SECURITY CORE */}
                    <section className="security-overview">

                        <div className="security-shield">
                            <div className="security-shield-ring">
                                <ShieldCheck size={38} />
                            </div>
                        </div>

                        <div className="security-overview-info">
                            <span>ZARVIS SECURITY CORE</span>

                            <h2>Your workspace is protected</h2>

                            <p>
                                Security monitoring is active and your
                                workspace is currently protected.
                            </p>
                        </div>

                        <div className="security-score">
                            <strong>100%</strong>
                            <span>SECURITY STATUS</span>
                        </div>

                    </section>

                    {/* SECURITY STATS */}
                    <section className="security-stats">

                        <div className="security-stat-card">
                            <ShieldCheck size={22} />

                            <div>
                                <span>SECURITY LEVEL</span>
                                <strong>HIGH</strong>
                            </div>
                        </div>

                        <div className="security-stat-card">
                            <Lock size={22} />

                            <div>
                                <span>ENCRYPTION</span>
                                <strong>ACTIVE</strong>
                            </div>
                        </div>

                        <div className="security-stat-card">
                            <Database size={22} />

                            <div>
                                <span>PROTECTED DATA</span>
                                <strong>08 ITEMS</strong>
                            </div>
                        </div>

                        <div className="security-stat-card">
                            <Activity size={22} />

                            <div>
                                <span>MONITORING</span>
                                <strong>LIVE</strong>
                            </div>
                        </div>

                    </section>

                    {/* PROTECTION SYSTEMS */}
                    <div className="security-section-title">
                        <div>
                            <span>PROTECTION SYSTEMS</span>
                            <h2>Security Controls</h2>
                        </div>

                        <div className="security-live">
                            <i></i>
                            MONITORING LIVE
                        </div>
                    </div>

                    {/* SECURITY CONTROL CARDS */}
                    <section className="security-controls">

                        {securityItems.map((item) => {
                            const Icon = item.icon;

                            return (
                                <div
                                    className="security-control-card"
                                    key={item.title}
                                >
                                    <div className="security-control-icon">
                                        <Icon size={21} />
                                    </div>

                                    <div className="security-control-content">

                                        <div className="security-control-top">
                                            <span>CONTROL ACTIVE</span>

                                            <strong>
                                                <CheckCircle2 size={12} />
                                                {item.status}
                                            </strong>
                                        </div>

                                        <h3>{item.title}</h3>

                                        <p>{item.description}</p>

                                    </div>
                                </div>
                            );
                        })}

                    </section>

                    {/* SECURITY ACTIVITY */}
                    <section className="security-activity">

                        <div className="security-activity-header">
                            <div>
                                <span>SECURITY LOG</span>
                                <h2>Recent Security Events</h2>
                            </div>

                            <RefreshCw size={18} />
                        </div>

                        {securityEvents.map((event) => {
                            const Icon = event.icon;

                            return (
                                <div
                                    className="security-event"
                                    key={event.title}
                                >
                                    <div className="security-event-icon">
                                        <Icon size={16} />
                                    </div>

                                    <div>
                                        <strong>{event.title}</strong>
                                        <span>{event.description}</span>
                                    </div>

                                    <time>{event.time}</time>
                                </div>
                            );
                        })}

                    </section>

                    {/* SECURITY INFO */}
                    <div className="security-info">
                        <AlertTriangle size={16} />

                        <span>
                            Zarvis security monitoring is active.
                            Review your security controls regularly
                            to keep your workspace protected.
                        </span>
                    </div>

                </div>
            </main>
        </div>
    );
}

export default Security;