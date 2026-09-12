import { useState } from "react";
import {
    Plug,
    Mail,
    CalendarDays,
    Cloud,
    GraduationCap,
    ShoppingCart,
    Search,
    CheckCircle2,
    ShieldCheck,
    Settings2,
    ExternalLink,
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const initialIntegrations = [
    {
        id: 1,
        name: "Google Calendar",
        description: "Manage events, meetings and your daily schedule.",
        category: "PRODUCTIVITY",
        icon: CalendarDays,
        connected: true,
    },
    {
        id: 2,
        name: "Email",
        description: "Read, organize and manage your important emails.",
        category: "COMMUNICATION",
        icon: Mail,
        connected: true,
    },
    {
        id: 3,
        name: "Cloud Storage",
        description: "Access and organize your files and documents.",
        category: "STORAGE",
        icon: Cloud,
        connected: false,
    },
    {
        id: 4,
        name: "Education",
        description: "Connect learning platforms and study resources.",
        category: "EDUCATION",
        icon: GraduationCap,
        connected: false,
    },
    {
        id: 5,
        name: "Shopping",
        description: "Connect shopping services for automated purchases.",
        category: "SERVICES",
        icon: ShoppingCart,
        connected: false,
    },
];

function Integrations() {
    const [integrations, setIntegrations] = useState(
        initialIntegrations
    );

    const [search, setSearch] = useState("");

    const toggleConnection = (id) => {
        setIntegrations((current) =>
            current.map((item) =>
                item.id === id
                    ? {
                        ...item,
                        connected: !item.connected,
                    }
                    : item
            )
        );
    };

    const filteredIntegrations = integrations.filter((item) =>
        `${item.name} ${item.description} ${item.category}`
            .toLowerCase()
            .includes(search.toLowerCase())
    );

    const connectedCount = integrations.filter(
        (item) => item.connected
    ).length;

    return (
        <div className="app">

            <Sidebar />

            <main className="main-content">

                <Navbar />

                <div className="integrations-page-final">

                    {/* HEADER */}

                    <section className="integrations-header-final">

                        <div className="integrations-header-info-final">

                            <div className="integrations-eyebrow-final">
                                <Plug size={14} />
                                <span>ZARVIS CONNECTION SYSTEM</span>
                            </div>

                            <h1>Integrations</h1>

                            <p>
                                Connect Zarvis with the tools and services
                                you use every day.
                            </p>

                        </div>

                        <div className="integrations-status-final">

                            <span></span>

                            SYSTEM READY

                        </div>

                    </section>

                    {/* STATS */}

                    <section className="integrations-stats-final">

                        <div className="integration-stat-final">
                            <span>TOTAL SERVICES</span>
                            <strong>{integrations.length}</strong>
                        </div>

                        <div className="integration-stat-final">
                            <span>CONNECTED</span>
                            <strong>{connectedCount}</strong>
                        </div>

                        <div className="integration-stat-final">
                            <span>AVAILABLE</span>
                            <strong>
                                {integrations.length - connectedCount}
                            </strong>
                        </div>

                        <div className="integration-stat-final">
                            <span>SECURITY</span>
                            <strong className="security-ok">
                                SECURE
                            </strong>
                        </div>

                    </section>

                    {/* SEARCH */}

                    <section className="integrations-toolbar-final">

                        <div className="integrations-search-final">

                            <Search size={17} />

                            <input
                                type="text"
                                placeholder="Search integrations..."
                                value={search}
                                onChange={(e) =>
                                    setSearch(e.target.value)
                                }
                            />

                        </div>

                        <div className="integration-toolbar-info-final">

                            <ShieldCheck size={15} />

                            <span>
                                Connections are protected by Zarvis Security
                            </span>

                        </div>

                    </section>

                    {/* INTEGRATIONS */}

                    <section className="integrations-panel-final">

                        <div className="integrations-panel-header-final">

                            <div>
                                <span>CONNECTION HUB // 05</span>
                                <h2>Available Integrations</h2>
                            </div>

                            <div className="integration-count-final">
                                {connectedCount} CONNECTED
                            </div>

                        </div>

                        <div className="integration-grid-final">

                            {filteredIntegrations.map((item) => {

                                const Icon = item.icon;

                                return (
                                    <div
                                        className={`integration-card-final ${item.connected
                                                ? "connected"
                                                : ""
                                            }`}
                                        key={item.id}
                                    >

                                        <div className="integration-card-top-final">

                                            <div className="integration-icon-final">
                                                <Icon size={22} />
                                            </div>

                                            <div
                                                className={`integration-connection-final ${item.connected
                                                        ? "connected"
                                                        : ""
                                                    }`}
                                            >
                                                <span></span>

                                                {item.connected
                                                    ? "CONNECTED"
                                                    : "AVAILABLE"}
                                            </div>

                                        </div>

                                        <div className="integration-card-content-final">

                                            <span className="integration-category-final">
                                                {item.category}
                                            </span>

                                            <h3>{item.name}</h3>

                                            <p>
                                                {item.description}
                                            </p>

                                        </div>

                                        <div className="integration-card-footer-final">

                                            <button
                                                type="button"
                                                className={
                                                    item.connected
                                                        ? "integration-manage-final"
                                                        : "integration-connect-final"
                                                }
                                                onClick={() =>
                                                    toggleConnection(item.id)
                                                }
                                            >

                                                {item.connected ? (
                                                    <>
                                                        <Settings2 size={14} />
                                                        Manage
                                                    </>
                                                ) : (
                                                    <>
                                                        <Plug size={14} />
                                                        Connect
                                                    </>
                                                )}

                                            </button>

                                            <button
                                                type="button"
                                                className="integration-external-final"
                                                title="Open integration"
                                            >
                                                <ExternalLink size={14} />
                                            </button>

                                        </div>

                                    </div>
                                );
                            })}

                        </div>

                        {filteredIntegrations.length === 0 && (
                            <div className="integration-empty-final">

                                <Search size={30} />

                                <h3>No integration found</h3>

                                <p>
                                    Try searching for another service.
                                </p>

                            </div>
                        )}

                    </section>

                    {/* SECURITY BAR */}

                    <div className="integrations-security-bar-final">

                        <div>

                            <div className="integration-security-icon-final">
                                <ShieldCheck size={16} />
                            </div>

                            <div>
                                <strong>ZARVIS CONNECTION SECURITY</strong>

                                <span>
                                    Your connected services remain under
                                    your control.
                                </span>
                            </div>

                        </div>

                        <span>
                            <CheckCircle2 size={14} />
                            SECURE
                        </span>

                    </div>

                </div>

            </main>

        </div>
    );
}

export default Integrations;