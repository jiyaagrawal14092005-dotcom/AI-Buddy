import {
  Search,
  Bell,
  Sun,
} from "lucide-react";

function Navbar() {
  return (
    <header className="navbar">

      {/* LEFT GREETING */}
      <div className="navbar-greeting">

        <div className="navbar-sun">
          <Sun size={27} />
        </div>

        <div className="navbar-greeting-text">
          <h2>Good Morning, Shanu!</h2>
          <p>Your goals. My priority.</p>
        </div>

      </div>

      {/* RIGHT SIDE */}
      <div className="navbar-actions">

        {/* SEARCH */}
        <div className="navbar-search">

          <Search size={18} />

          <input
            type="text"
            placeholder="Search anything..."
          />

        </div>

        {/* NOTIFICATION */}
        <button
          type="button"
          className="navbar-notification"
          aria-label="Notifications"
        >
          <Bell size={25} />

          <span className="navbar-notification-dot"></span>
        </button>

        {/* PROFILE */}
        <button
          type="button"
          className="navbar-profile"
          aria-label="Profile"
        >
          S
        </button>

      </div>

    </header>
  );
}

export default Navbar;