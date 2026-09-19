import threading
import time

from app.voice.text_to_speech import TextToSpeech
from app.voice.command_listener import CommandListener


tts = TextToSpeech()
listener = CommandListener()

stop_event = threading.Event()


def on_text(text: str):
    print(f"\nMicrophone heard: {text}")

    normalized = " ".join(
        text.lower().strip().split()
    )

    if normalized in {
        "stop",
        "jarvis stop",
        "zarvis stop",
    }:

        print("STOP COMMAND DETECTED")

        stop_event.set()

        print("Stopping TTS...")

        tts.stop()

        print("TTS stop signal sent.")


listener.set_command_callback(on_text)


def speak():
    text = (
        "This is a long test sentence for AI Buddy. "
        "AI Buddy is testing the Jarvis voice assistant. "
        "The purpose of this test is to verify that "
        "the assistant can stop speaking immediately "
        "when the user says the stop command. "
        "This sentence is intentionally long so that "
        "you have enough time to say stop while the "
        "assistant is speaking."
    )

    print("\nTTS started...")
    result = tts.speak(text)

    print("\nTTS RESULT:")
    print(result)


print("\nStarting microphone listener...")

listener_result = listener.start_listening()

print(listener_result)

if not listener_result.get("success", False):
    print("Could not start microphone listener.")
    raise SystemExit


speech_thread = threading.Thread(
    target=speak,
    daemon=True
)

speech_thread.start()


try:

    while speech_thread.is_alive():

        time.sleep(0.1)

except KeyboardInterrupt:

    print("\nTest interrupted manually.")

finally:

    print("\nStopping microphone...")

    listener.stop_microphone()

    listener.set_command_callback(None)

    if speech_thread.is_alive():
        tts.stop()

    speech_thread.join(timeout=2)

    print("\nFinal TTS status:")
    print(tts.get_status())

    print("\nTest finished.")