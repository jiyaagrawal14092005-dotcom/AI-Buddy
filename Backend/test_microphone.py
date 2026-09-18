import speech_recognition as sr


recognizer = sr.Recognizer()

print("Speak now...")

with sr.Microphone() as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(
        source,
        duration=1
    )

    print("Listening...")
    audio = recognizer.listen(
        source,
        timeout=5,
        phrase_time_limit=8
    )

print("Processing...")

try:
    text = recognizer.recognize_google(audio)
    print("Recognized:", text)

except sr.UnknownValueError:
    print("Could not understand the speech.")

except sr.RequestError as error:
    print("Speech recognition service error:", error)

except Exception as error:
    print("Unexpected error:", error)