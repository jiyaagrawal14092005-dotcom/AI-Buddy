import asyncio
import types

from app.voice.jarvis_mode import JarvisMode
from app.database.connection import SessionLocal


LONG_RESPONSE = (
    "Hello, I am AI Buddy. "
    "This is a controlled Jarvis integration test. "
    "The Gemini API is intentionally bypassed for this test. "
    "The purpose of this test is to verify that JarvisMode, "
    "CommandListener, and TextToSpeech work together correctly. "
    "AI Buddy should continue speaking this long response until "
    "the user says the stop command. "
    "When the user says stop, Jarvis should immediately stop "
    "the current speech and deactivate Jarvis mode. "
    "This sentence is intentionally long so that there is "
    "enough time to test the stop command while speaking."
)


async def controlled_process(
    self,
    command_text: str,
    db=None
):
    print(
        f"\nControlled command received: "
        f"{command_text}"
    )

    if self._stop_event.is_set():
        return

    response_text = LONG_RESPONSE

    print(
        "\nStarting controlled TTS response..."
    )
    print(
        "Now say: Zarvis stop"
    )

    result = self.voice_manager.speak(
        response_text
    )

    print(
        "\nControlled TTS result:"
    )
    print(result)


async def main():

    db = SessionLocal()

    jarvis = JarvisMode(
        wake_word="Zarvis"
    )

    # Replace the normal Gemini-based command
    # processor only for this test.
    jarvis._process_command = types.MethodType(
        controlled_process,
        jarvis
    )

    print("\nStarting Jarvis...")

    start_result = await jarvis.start(
        user_id=1,
        db=db
    )

    print(start_result)

    if not start_result.get("success", False):
        print("\nCould not start Jarvis.")
        db.close()
        return

    print("\n========================================")
    print("CONTROLLED JARVIS INTEGRATION TEST")
    print("========================================")
    print("\nSay:")
    print("Zarvis hello")
    print("\nWhen AI Buddy starts speaking, say:")
    print("Zarvis stop")
    print("\nDo NOT press Ctrl+C unless the test")
    print("gets stuck.")
    print("========================================\n")

    try:

        while jarvis.active:

            await asyncio.sleep(0.2)

    except KeyboardInterrupt:

        print(
            "\nTest interrupted manually."
        )

    finally:

        print("\nStopping Jarvis...")

        stop_result = await jarvis.stop()

        print(stop_result)

        db.close()

        print("\nFinal Jarvis status:")
        print(jarvis.get_status())

        print("\nTest finished.")


if __name__ == "__main__":
    asyncio.run(main())