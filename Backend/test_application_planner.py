from app.agent.planner import Planner


planner = Planner()


intent = {
    "intent": "OPEN_APPLICATION",
    "confidence": 0.95,
    "parameters": {
        "application": "calculator",
        "action": "open_application"
    }
}


print("=== APPLICATION PLANNER TEST ===")

print("\nIntent:")
print(intent)

print("\nPlan:")

result = planner.create_plan(intent)

print(result)

print("\n=== GET TOOL ===")

print(
    planner.get_tool("OPEN_APPLICATION")
)

print("\n=== HAS TOOL ===")

print(
    planner.has_tool("OPEN_APPLICATION")
)