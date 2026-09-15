import {
    Search,
    Bell,
    Sun,
    ChevronDown,
} from "lucide-react";

function Navbar() {
    return (
        <header className="navbar reference-navbar">

            <div className="reference-navbar-search">
                <Search size={22} />

                <input
                    type="text"
                    placeholder="Search anything..."
                />
            </div>

            <div className="reference-navbar-actions">

                <button
                    type="button"
                    className="reference-navbar-icon"
                    title="Notifications"
                >
                    <Bell size={24} />
                    <span className="reference-notification-dot"></span>
                </button>

                <button
                    type="button"
                    className="reference-navbar-icon"
                    title="Theme"
                >
                    <Sun size={23} />
                </button>

                <button
                    type="button"
                    className="reference-navbar-profile"
                >
                    <div className="reference-profile-avatar">
                        S
                    </div>

                    <span>Shanu</span>

                    <ChevronDown size={16} />
                </button>

            </div>

        </header>
    );
}

export default Navbar;