import "../styles/navbar.css";
import {
Bell,
ChevronDown,
} from "lucide-react";

function Navbar() {
    return (
        <header className="zarvis-navbar">
            <div className="zarvis-navbar-actions">
                <button
                    type="button"
                    className="zarvis-notification-button"
                    aria-label="Notifications"
                >
                    <Bell size={18} />
                    <span className="zarvis-notification-dot"></span>
                </button>

                <button
                    type="button"
                    className="zarvis-account-button"
                >
                    <div className="zarvis-avatar">
                        S
                    </div>

                    <div className="zarvis-account-info">
                        <strong>Shanu</strong>
                        <span>Personal Workspace</span>
                    </div>

                    <ChevronDown size={15} />
                </button>
            </div>
        </header>
    );
}

export default Navbar;