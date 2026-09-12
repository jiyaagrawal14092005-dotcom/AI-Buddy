from app.agent.intent import IntentDetector


detector = IntentDetector()


test_messages = [
    "Set a timer for 10 minutes",
    "Remind me to study at 7 PM",
    "What is Python?",
    "Create a task to complete my assignment"
]


for message in test_messages:

    print("\nUser:", message)

    try:
        result = detector.detect(message)
        print("Intent:", result)

    except Exception as e:
        print("⚠️ Gemini temporarily unavailable.")
        print("Error:", e)