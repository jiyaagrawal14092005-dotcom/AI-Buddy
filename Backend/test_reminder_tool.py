from app.tools.reminder import ReminderTool


reminder_tool = ReminderTool()


print("=== VALID REMINDER ===")

print(
    reminder_tool.create_reminder(
        "Practice Python",
        "2026-09-15T18:30:00"
    )
)


print("\n=== ANOTHER VALID REMINDER ===")

print(
    reminder_tool.create_reminder(
        "AI Buddy meeting",
        "2026-09-16T10:00:00"
    )
)


print("\n=== EMPTY REMINDER ===")

print(
    reminder_tool.create_reminder(
        "",
        "2026-09-15T18:30:00"
    )
)


print("\n=== INVALID TIME FORMAT ===")

print(
    reminder_tool.create_reminder(
        "Test reminder",
        "15-09-2026 18:30"
    )
)


print("\n=== EMPTY TIME ===")

print(
    reminder_tool.create_reminder(
        "Test reminder",
        ""
    )
)
