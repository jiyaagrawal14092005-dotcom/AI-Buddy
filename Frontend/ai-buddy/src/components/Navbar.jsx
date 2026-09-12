import { useState } from "react";
import {
  Bell,
  Sun,
  Search,
  CheckCircle2,
  Clock3,
  Workflow,
  Check,
  Trash2,
  ListTodo,
  CalendarDays,
  Brain,
  Settings,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [showSearchResults, setShowSearchResults] =
    useState(false);

  const [showNotifications, setShowNotifications] =
    useState(false);

  const [notifications, setNotifications] = useState([
    {
      id: 1,
      title: "Task completed",
      text: "Project documentation was completed.",
      time: "10 min ago",
      type: "success",
      read: false,
    },
    {
      id: 2,
      title: "Upcoming task",
      text: "Prepare presentation is due tomorrow.",
      time: "32 min ago",
      type: "task",
      read: false,
    },
    {
      id: 3,
      title: "Workflow finished",
      text: "Morning Planning workflow completed.",
      time: "1 hour ago",
      type: "workflow",
      read: true,
    },
  ]);

  const searchItems = [
    {
      title: "Dashboard",
      description: "Zarvis overview and quick actions",
      icon: CheckCircle2,
      path: "/",
    },
    {
      title: "Tasks",
      description: "Manage your tasks",
      icon: ListTodo,
      path: "/tasks",
    },
    {
      title: "Schedule",
      description: "Organize your time",
      icon: CalendarDays,
      path: "/schedule",
    },
    {
      title: "Workflows",
      description: "Automate your routines",
      icon: Workflow,
      path: "/workflows",
    },
    {
      title: "Memory",
      description: "View saved memories",
      icon: Brain,
      path: "/memory",
    },
    {
      title: "Security",
      description: "Manage security settings",
      icon: CheckCircle2,
      path: "/security",
    },
    {
      title: "Settings",
      description: "Customize Zarvis",
      icon: Settings,
      path: "/settings",
    },
  ];

  const filteredResults = searchItems.filter((item) =>
    `${item.title} ${item.description}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  const handleSearchChange = (event) => {
    const value = event.target.value;

    setSearch(value);
    setShowSearchResults(value.trim().length > 0);
  };

  const handleSearchResult = (path) => {
    navigate(path);
    setSearch("");
    setShowSearchResults(false);
  };

  const unreadCount = notifications.filter(
    (notification) => !notification.read
  ).length;

  const markAsRead = (id) => {
    setNotifications((current) =>
      current.map((notification) =>
        notification.id === id
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications((current) =>
      current.map((notification) => ({
        ...notification,
        read: true,
      }))
    );
  };

  const clearAll = () => {
    setNotifications([]);
  };

  return (
    <header className="navbar">

      <div className="navbar-left">

        {/* Mobile Brand */}
        <div className="mobile-brand">
          <div className="logo-icon">
            <span>✦</span>
          </div>

          <strong>Zarvis</strong>
        </div>


        {/* GLOBAL SEARCH */}
        <div className="search-wrapper">

          <div className="search-box">
            <Search size={17} />

            <input
              type="text"
              placeholder="Search anything..."
              value={search}
              onChange={handleSearchChange}
              onFocus={() => {
                if (search.trim()) {
                  setShowSearchResults(true);
                }
              }}
            />

            <span className="search-shortcut">
              ⌘ K
            </span>
          </div>


          {/* SEARCH RESULTS */}
          {showSearchResults && (
            <div className="global-search-results">

              <div className="search-results-header">
                <span>ZARVIS SEARCH</span>

                <small>
                  {filteredResults.length} results
                </small>
              </div>

              {filteredResults.length > 0 ? (
                filteredResults.map((item) => {
                  const Icon = item.icon;

                  return (
                    <button
                      type="button"
                      className="search-result-item"
                      key={item.path}
                      onClick={() =>
                        handleSearchResult(item.path)
                      }
                    >
                      <div className="search-result-icon">
                        <Icon size={16} />
                      </div>

                      <div className="search-result-info">
                        <strong>{item.title}</strong>
                        <span>{item.description}</span>
                      </div>
                    </button>
                  );
                })
              ) : (
                <div className="search-no-results">
                  <Search size={22} />

                  <strong>
                    No results found
                  </strong>

                  <span>
                    Try another search.
                  </span>
                </div>
              )}

            </div>
          )}

        </div>

      </div>


      <div className="navbar-right">

        {/* Theme */}
        <button
          type="button"
          className="icon-button"
          title="Theme"
        >
          <Sun size={18} />
        </button>


        {/* Notifications */}
        <div className="notification-wrapper">

          <button
            type="button"
            className="icon-button notification-button"
            title="Notifications"
            onClick={() =>
              setShowNotifications(
                (current) => !current
              )
            }
          >
            <Bell size={18} />

            {unreadCount > 0 && (
              <span className="notification-dot"></span>
            )}

            {unreadCount > 0 && (
              <span className="notification-count">
                {unreadCount}
              </span>
            )}
          </button>


          {showNotifications && (
            <div className="notification-panel">

              <div className="notification-panel-header">

                <div>
                  <h3>Notifications</h3>

                  <span>
                    {unreadCount > 0
                      ? `${unreadCount} unread`
                      : "All caught up"}
                  </span>
                </div>

                {unreadCount > 0 && (
                  <button
                    type="button"
                    className="notification-mark-read"
                    onClick={markAllAsRead}
                  >
                    <Check size={13} />
                    Mark all read
                  </button>
                )}

              </div>


              <div className="notification-list">

                {notifications.length > 0 ? (
                  notifications.map((notification) => {

                    let Icon = Workflow;

                    if (
                      notification.type === "success"
                    ) {
                      Icon = CheckCircle2;
                    }

                    if (
                      notification.type === "task"
                    ) {
                      Icon = Clock3;
                    }

                    return (
                      <button
                        type="button"
                        className={`notification-item ${notification.read
                            ? ""
                            : "unread"
                          }`}
                        key={notification.id}
                        onClick={() =>
                          markAsRead(
                            notification.id
                          )
                        }
                      >

                        <div
                          className={`notification-icon notification-${notification.type}`}
                        >
                          <Icon size={16} />
                        </div>

                        <div className="notification-content">

                          <strong>
                            {notification.title}
                          </strong>

                          <p>
                            {notification.text}
                          </p>

                          <span>
                            {notification.time}
                          </span>

                        </div>

                        {!notification.read && (
                          <span className="notification-unread-dot"></span>
                        )}

                      </button>
                    );
                  })
                ) : (
                  <div className="notification-empty">

                    <CheckCircle2 size={28} />

                    <strong>
                      You're all caught up
                    </strong>

                    <span>
                      No new notifications.
                    </span>

                  </div>
                )}

              </div>


              {notifications.length > 0 && (
                <div className="notification-panel-footer">

                  <button
                    type="button"
                    className="notification-clear"
                    onClick={clearAll}
                  >
                    <Trash2 size={13} />
                    Clear all
                  </button>

                </div>
              )}

            </div>
          )}

        </div>


        {/* User Profile */}
        <div className="profile">

          <div className="profile-avatar">
            U
          </div>

          <div className="profile-info">
            <strong>User</strong>
            <span>Online</span>
          </div>

        </div>

      </div>

    </header>
  );
}

export default Navbar;