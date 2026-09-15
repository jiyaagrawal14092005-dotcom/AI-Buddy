from app.tools.application_launcher import ApplicationLauncher


launcher = ApplicationLauncher()


print("=== LAUNCHER INFO ===")

print(
    launcher.name
)


print("\n=== OPEN CALCULATOR ===")

print(
    launcher.execute({
        "action": "open_application",
        "application": "calculator"
    })
)


print("\n=== OPEN NOTEPAD ===")

print(
    launcher.execute({
        "action": "open_application",
        "application": "notepad"
    })
)


print("\n=== OPEN WEBSITE ===")

print(
    launcher.execute({
        "action": "open_website",
        "url": "https://www.google.com"
    })
)


print("\n=== UNSUPPORTED APPLICATION ===")

print(
    launcher.execute({
        "action": "open_application",
        "application": "unknown_app"
    })
)


print("\n=== INVALID URL ===")

print(
    launcher.execute({
        "action": "open_website",
        "url": "google.com"
    })
)


print("\n=== INVALID ACTION ===")

print(
    launcher.execute({
        "action": "invalid_action"
    })
)


print("\n=== AVAILABILITY ===")

print(
    launcher.is_available()
)