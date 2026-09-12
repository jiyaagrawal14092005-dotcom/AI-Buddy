from app.agent.reasoning import ReasoningEngine


reasoning = ReasoningEngine()


print("=== APPLICATION REASONING TEST ===")


plan = {
    "success": True,
    "intent": "OPEN_APPLICATION",
    "tool": "application_launcher",
    "parameters": {
        "application": "calculator",
        "action": "open_application"
    }
}


print("\n=== REASON ===")
print(
    reasoning.reason(
        "OPEN_APPLICATION",
        plan
    )
)


print("\n=== CAN EXECUTE ===")
print(
    reasoning.can_execute(
        "OPEN_APPLICATION"
    )
)


print("\n=== IS FUTURE INTENT ===")
print(
    reasoning.is_future_intent(
        "OPEN_APPLICATION"
    )
)


print("\n=== MISSING PARAMETER TEST ===")

invalid_plan = {
    "intent": "OPEN_APPLICATION",
    "tool": "application_launcher",
    "parameters": {}
}

print(
    reasoning.reason(
        "OPEN_APPLICATION",
        invalid_plan
    )
)