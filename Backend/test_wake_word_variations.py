from app.voice.wake_word import WakeWordDetector


def main():

    detector = WakeWordDetector(
        wake_word="ai buddy"
    )

    test_phrases = [
        "ai buddy hello",
        "AI Buddy hello",
        "a buddy hello",
        "hey buddy hello",
        "hi buddy hello",
        "ai body hello",
        "a body hello",
        "i buddy hello",
        "eye buddy hello",
        "open chrome"
    ]

    print("=" * 60)
    print("AI BUDDY - WAKE WORD VARIATION TEST")
    print("=" * 60)

    for text in test_phrases:

        result = detector.process(text)

        print()
        print("INPUT:", text)
        print("RESULT:", result)

    print()
    print("=" * 60)
    print("STATUS")
    print("=" * 60)

    print(detector.get_status())


if __name__ == "__main__":
    main()