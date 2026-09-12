from app.tools.calendar_tool import CalendarTool


calendar_tool = CalendarTool()


print("=== CALENDAR TOOL INFO ===")

print(
    calendar_tool.get_info()
)


print("\n=== VALID EVENT ===")

print(
    calendar_tool.execute({
        "title": "Python Practice",
        "date": "2026-09-15",
        "time": "18:30",
        "details": "Practice Python for AI Buddy"
    })
)


print("\n=== EVENT USING 'event' FIELD ===")

print(
    calendar_tool.execute({
        "event": "AI Buddy Meeting",
        "date": "2026-09-16",
        "time": "10:00"
    })
)


print("\n=== INVALID DATE ===")

print(
    calendar_tool.execute({
        "title": "Test Event",
        "date": "15-09-2026",
        "time": "18:30"
    })
)


print("\n=== INVALID TIME ===")

print(
    calendar_tool.execute({
        "title": "Test Event",
        "date": "2026-09-15",
        "time": "6:30 PM"
    })
)


print("\n=== CALENDAR AVAILABILITY ===")

print(
    calendar_tool.is_available()
)