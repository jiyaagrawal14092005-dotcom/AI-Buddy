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

const securityItems = [
    {
        icon: Lock,
        title: "Data Encryption",
        description: "Your Zarvis data is protected with secure encryption.",
        status: "SECURE",
    },
    {
        icon: KeyRound,
        title: "API Security",
        description: "Connected services use protected authentication.",
        status: "SECURE",
    },
    {
        icon: Smartphone,
        title: "Device Access",
        description: "Only authorized devices can access your workspace.",
        status: "VERIFIED",
    },
    {
        icon: Eye,
        title: "Privacy Controls",
        description: "You control what Zarvis can remember and access.",
        status: "ACTIVE",
    },
];

function Security() {
    return (
        <div className="app">

            {/* SIDEBAR */}

            <aside className="sidebar">

                <div className="sidebar-brand">
                    <div className="sidebar-logo-mark">✦</div>

                    <div className="sidebar-brand-text">
                        <h2>ZARVIS</h2>
                        <span>AI COMPANION</span>
                    </div>
                </div>

                <div className="sidebar-system">
                    <div className="system-indicator">
                        <span className="system-dot"></span>

                        <div>
                            <strong>SYSTEM ONLINE</strong>
                            <small>Zarvis Core Active</small>
                        </div>
                    </div>

                    <div className="system-line">
                        <span></span>
                    </div>
                </div>

                <nav className="sidebar-nav">

                    <a href="/" className="sidebar-nav-item">
                        <span className="sidebar-nav-icon">◈</span>
                        <span className="sidebar-nav-label">Dashboard</span>
                    </a>

                    <a href="/tasks" className="sidebar-nav-item">
                        <span className="sidebar-nav-icon">✓</span>
                        <span className="sidebar-nav-label">Tasks</span>
                    </a>

                    <a href="/schedule" className="sidebar-nav-item">
                        <span className="sidebar-nav-icon">▣</span>
                        <span className="sidebar-nav-label">Schedule</span>
                    </a>

                    <a href="/workflows" className="sidebar-nav-item">
                        <span className="sidebar-nav-icon">◇</span>
                        <span className="sidebar-nav-label">Workflows</span>
                    </a>

                    <a href="/memory" className="sidebar-nav-item">
                        <span className="sidebar-nav-icon">♧</span>
                        <span className="sidebar-nav-label">Memory</span>
                    </a>

                    <div className="sidebar-section-label sidebar-section-security">
                        <span>SYSTEM</span>
                        <span className="sidebar-section-line"></span>
                    </div>

                    <a
                        href="/security"
                        className="sidebar-nav-item active"
                    >
                        <span className="sidebar-nav-icon">◉</span>
                        <span className="sidebar-nav-label">Security</span>
                    </a>

                    <a href="/settings" className="sidebar-nav-item">
                        <span className="sidebar-nav-icon">⚙</span>
                        <span className="sidebar-nav-label">Settings</span>
                    </a>

                </nav>

                <div className="sidebar-bottom">

                    <div className="sidebar-core-card">
                        <div className="core-status-icon">
                            <span></span>
                        </div>

                        <div className="core-status-text">
                            <strong>ZARVIS CORE</strong>
                            <span>Ready to assist</span>
                        </div>

                        <div className="core-status-bars">
                            <i></i>
                            <i></i>
                            <i></i>
                        </div>
                    </div>

                    <div className="sidebar-version">
                        <span>V1.0</span>
                        <span>AI BUDDY SYSTEM</span>
                    </div>

                </div>

            </aside>


            {/* MAIN */}

            <main className="main-content">

                <div className="security-page">

                    {/* HEADER */}

                    <div className="security-page-header">

                        <div>
                            <span className="security-page-label">
                                SECURITY CENTER // 06
                            </span>

                            <h1>
                                Security & Privacy
                            </h1>

                            <p>
                                Manage your Zarvis security, access and privacy controls.
                            </p>
                        </div>

                        <div className="security-header-status">
                            <span></span>
                            ALL SYSTEMS SECURE
                        </div>

                    </div>


                    {/* SECURITY OVERVIEW */}

                    <section className="security-overview">

                        <div className="security-shield">

                            <div className="security-shield-ring">
                                <ShieldCheck size={32} />
                            </div>

                        </div>

                        <div className="security-overview-info">

                            <span>
                                ZARVIS SECURITY CORE
                            </span>

                            <h2>
                                Your workspace is protected
                            </h2>

                            <p>
                                Security systems are active and monitoring your workspace.
                            </p>

                        </div>

                        <div className="security-score">

                            <strong>
                                100%
                            </strong>

                            <span>
                                SECURITY STATUS
                            </span>

                        </div>

                    </section>


                    {/* SECURITY STATS */}

                    <div className="security-stats">

                        <div className="security-stat-card">
                            <ShieldCheck size={18} />

                            <div>
                                <span>SECURITY LEVEL</span>
                                <strong>HIGH</strong>
                            </div>
                        </div>

                        <div className="security-stat-card">
                            <Lock size={18} />

                            <div>
                                <span>ENCRYPTION</span>
                                <strong>ACTIVE</strong>
                            </div>
                        </div>

                        <div className="security-stat-card">
                            <Database size={18} />

                            <div>
                                <span>PROTECTED DATA</span>
                                <strong>08 ITEMS</strong>
                            </div>
                        </div>

                        <div className="security-stat-card">
                            <Activity size={18} />

                            <div>
                                <span>MONITORING</span>
                                <strong>LIVE</strong>
                            </div>
                        </div>

                    </div>


                    {/* CONTROLS */}

                    <div className="security-section-title">

                        <div>
                            <span>
                                PROTECTION SYSTEMS
                            </span>

                            <h2>
                                Security Controls
                            </h2>
                        </div>

                        <span className="security-live">
                            <i></i>
                            MONITORING
                        </span>

                    </div>


                    <section className="security-controls">

                        {securityItems.map((item, index) => {

                            const Icon = item.icon;

                            return (
                                <article
                                    className="security-control-card"
                                    key={index}
                                >

                                    <div className="security-control-icon">
                                        <Icon size={18} />
                                    </div>

                                    <div className="security-control-content">

                                        <div className="security-control-top">

                                            <span>
                                                CONTROL-{String(index + 1).padStart(2, "0")}
                                            </span>

                                            <strong>
                                                <CheckCircle2 size={12} />
                                                {item.status}
                                            </strong>

                                        </div>

                                        <h3>
                                            {item.title}
                                        </h3>

                                        <p>
                                            {item.description}
                                        </p>

                                    </div>

                                </article>
                            );
                        })}

                    </section>


                    {/* ACTIVITY */}

                    <section className="security-activity">

                        <div className="security-activity-header">

                            <div>
                                <span>
                                    SECURITY ACTIVITY
                                </span>

                                <h2>
                                    Recent Security Events
                                </h2>
                            </div>

                            <RefreshCw size={15} />

                        </div>


                        <div className="security-event">

                            <div className="security-event-icon">
                                <CheckCircle2 size={14} />
                            </div>

                            <div>
                                <strong>
                                    Security check completed
                                </strong>

                                <span>
                                    Zarvis security systems verified successfully.
                                </span>
                            </div>

                            <time>
                                8 min ago
                            </time>

                        </div>


                        <div className="security-event">

                            <div className="security-event-icon">
                                <Lock size={14} />
                            </div>

                            <div>
                                <strong>
                                    Protected session started
                                </strong>

                                <span>
                                    New secure workspace session initialized.
                                </span>
                            </div>

                            <time>
                                1 hr ago
                            </time>

                        </div>


                        <div className="security-event">

                            <div className="security-event-icon">
                                <ShieldCheck size={14} />
                            </div>

                            <div>
                                <strong>
                                    Privacy controls verified
                                </strong>

                                <span>
                                    Memory and access permissions are operating normally.
                                </span>
                            </div>

                            <time>
                                3 hrs ago
                            </time>

                        </div>

                    </section>


                    {/* WARNING / INFO */}

                    <div className="security-info">

                        <AlertTriangle size={14} />

                        <span>
                            Security settings should be reviewed whenever a new integration or device is connected.
                        </span>

                    </div>

                </div>

            </main>

        </div>
    );
}

export default Security;