import asyncio

from app.voice.jarvis_mode import JarvisMode


async def main():

    jarvis = JarvisMode(
        wake_word="ai buddy",
        user_id=1,
        chunk_seconds=2
    )

    print("=" * 60)
    print("AI BUDDY - JARVIS MICROPHONE TEST")
    print("=" * 60)

    print()
    print("STATUS BEFORE RECORDING:")
    print(
        jarvis.get_status()
    )

    print()
    print("🎙️ Recording for 2 seconds...")
    print("Please speak something now.")

    try:

        audio_data = await asyncio.to_thread(
            jarvis._record_chunk
        )

        if not audio_data:

            print()
            print("❌ No audio data captured.")
            return

        print()
        print("✅ Audio captured successfully.")

        print(
            "Audio bytes:",
            len(audio_data)
        )

        print()
        print("Converting speech to text...")

        result = (
            jarvis.voice_manager
            .speech_to_text
            .transcribe(
                audio_data
            )
        )

        print()
        print("SPEECH-TO-TEXT RESULT:")
        print(
            result
        )

        print()
        print("=" * 60)
        print("TEST COMPLETE")
        print("=" * 60)

    except KeyboardInterrupt:

        print()
        print("❌ Test interrupted by user.")

    except Exception as error:

        print()
        print(
            "❌ Microphone test error:",
            error
        )


if __name__ == "__main__":

    asyncio.run(
        main()
    )