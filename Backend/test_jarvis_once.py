import asyncio
import wave

from app.voice.jarvis_mode import JarvisMode


async def main():
    jarvis = JarvisMode(
        wake_word="Zarvis",
        user_id=1,
        chunk_seconds=4
    )

    print("Recording for 4 seconds...")
    print("Say: Zarvis, open Visual Studio Code")

    audio_data = await asyncio.to_thread(
        jarvis._record_chunk
    )

    if not audio_data:
        print("ERROR: No audio recorded.")
        return

    output_file = "jarvis_test.wav"

    with open(output_file, "wb") as file:
        file.write(audio_data)

    print(f"\nAudio saved successfully: {output_file}")
    print(f"Audio size: {len(audio_data)} bytes")

    with wave.open(output_file, "rb") as wav:
        print("Channels:", wav.getnchannels())
        print("Sample width:", wav.getsampwidth())
        print("Sample rate:", wav.getframerate())
        print("Frames:", wav.getnframes())

    stt_result = jarvis.voice_manager.speech_to_text.transcribe(
        audio_data
    )

    print("\nSTT RESULT:")
    print(stt_result)


if __name__ == "__main__":
    asyncio.run(main())