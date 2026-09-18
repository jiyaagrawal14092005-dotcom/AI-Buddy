import io
import wave

import numpy as np
import sounddevice as sd

from app.voice.speech_to_text import SpeechToText


SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5


print("========================================")
print("AI Buddy - Jarvis Audio Pipeline Test")
print("========================================")
print()
print("Speak clearly after recording starts.")
print()

print("Recording...")

recording = sd.rec(
    int(SAMPLE_RATE * RECORD_SECONDS),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16"
)

sd.wait()

print("Recording finished.")
print("Converting audio to WAV...")

audio_array = np.asarray(recording, dtype=np.int16)

wav_buffer = io.BytesIO()

with wave.open(wav_buffer, "wb") as wav_file:
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(2)
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.writeframes(audio_array.tobytes())

audio_bytes = wav_buffer.getvalue()

print("WAV created.")
print("Audio size:", len(audio_bytes), "bytes")
print()
print("Sending audio to AI Buddy SpeechToText...")
print()

speech_to_text = SpeechToText()

result = speech_to_text.transcribe(audio_bytes)

print("========================================")
print("RESULT")
print("========================================")
print(result)
print()

if result.get("success"):
    print("SUCCESS: sounddevice -> WAV -> SpeechToText is working.")
else:
    print("FAILED: sounddevice -> WAV -> SpeechToText has an issue.")