import asyncio
import io
import wave

import sounddevice as sd

from app.voice.speech_to_text import SpeechToText
from app.voice.wake_word import WakeWordDetector


SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5


def record_audio():

    print()
    print("=" * 60)
    print("MICROPHONE TEST")
    print("=" * 60)

    print()
    print("🎙️ Get ready...")
    print("Speak clearly:")
    print("AI Buddy hello")
    print()

    input("Press ENTER, then speak immediately...")

    print()
    print("🔴 RECORDING...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )

    sd.wait()

    print("🟢 Recording finished.")

    audio_bytes = audio.tobytes()

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:

        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_bytes)

    return buffer.getvalue()


async def main():

    stt = SpeechToText()

    wake_word = WakeWordDetector(
        wake_word="ai buddy"
    )

    print()
    print("=" * 60)
    print("AI BUDDY - STT + WAKE WORD TEST")
    print("=" * 60)

    print()
    print("Speech-to-Text available:", stt.is_available())
    print("Wake word:", wake_word.wake_word)

    audio_bytes = record_audio()

    print()
    print("=" * 60)
    print("STEP 1 - SPEECH TO TEXT")
    print("=" * 60)

    result = stt.transcribe(audio_bytes)

    print()
    print("STT RESULT:")
    print(result)

    if not result.get("success"):

        print()
        print("❌ STT FAILED")
        print("Message:", result.get("message"))

        return

    recognized_text = result.get("text", "")

    print()
    print("Recognized text:")
    print(recognized_text)

    print()
    print("=" * 60)
    print("STEP 2 - WAKE WORD DETECTION")
    print("=" * 60)

    wake_result = wake_word.process(
        recognized_text
    )

    print()
    print("WAKE WORD RESULT:")
    print(wake_result)

    print()

    if wake_result.get("wake_word_detected"):

        print("✅ WAKE WORD DETECTED")

        command = wake_result.get(
            "command"
        )

        print()
        print("Extracted command:")
        print(command)

        if command:

            print()
            print("🎯 COMPLETE STT + WAKE WORD PIPELINE PASSED")

        else:

            print()
            print("⚠️ Wake word detected,")
            print("but no command was extracted.")

    else:

        print("❌ WAKE WORD NOT DETECTED")

        print()
        print(
            "Try speaking exactly: AI Buddy hello"
        )

    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":

    asyncio.run(main())