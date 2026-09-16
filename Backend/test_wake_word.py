from app.voice.wake_word import WakeWordDetector


detector = WakeWordDetector(
    "ai buddy"
)


test_cases = [
    "ai buddy open chrome",
    "AI Buddy set a timer for 10 minutes",
    "hello ai buddy read this page",
    "open chrome",
]


for text in test_cases:

    result = detector.process(
        text
    )

    print()
    print("INPUT:", text)
    print("RESULT:", result)


print()
print("Wake word:", detector.get_wake_word())
print("Status:", detector.get_status())