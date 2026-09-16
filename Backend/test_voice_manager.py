from app.voice.voice_manager import VoiceManager


manager = VoiceManager(
    wake_word="ai buddy"
)


test_cases = [
    "ai buddy open chrome",
    "AI Buddy set a timer for 10 minutes",
    "hello ai buddy read this page",
    "open chrome",
    "ai buddy",
]


for text in test_cases:

    result = manager.process_text(
        text
    )

    print()
    print("INPUT:", text)
    print("RESULT:", result)


print()
print("STATUS:")
print(manager.get_status())