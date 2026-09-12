from app.voice.text_to_speech import TextToSpeech


tts = TextToSpeech()


print("=== TEXT TO SPEECH TEST ===")


print("\n=== STATUS ===")

print(
    tts.get_status()
)


print("\n=== AVAILABILITY ===")

print(
    tts.is_available()
)


print("\n=== SPEAK TEST ===")

result = tts.synthesize(
    "Hello, I am AI Buddy. Your voice assistant is working."
)

print(result)