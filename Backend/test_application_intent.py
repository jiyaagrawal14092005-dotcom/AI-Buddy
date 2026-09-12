from app.agent.intent import IntentDetector


detector = IntentDetector()


test_messages = [
    "Open calculator",
    "Open notepad",
    "Launch Chrome",
    "Start Paint",
    "Open VS Code",
    "Open Google"
]


print("=== APPLICATION INTENT TEST ===")

for message in test_messages:

    print(f"\nUser: {message}")

    result = detector.detect(message)

    print("Result:")
    print(result)

    print("-" * 60)