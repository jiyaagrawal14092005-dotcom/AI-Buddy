import io
import wave

import speech_recognition as sr


class SpeechToText:

    def __init__(self):

        self.name = "speech_to_text"
        self.recognizer = sr.Recognizer()
        self.available = True

    def transcribe(
        self,
        audio_data
    ) -> dict:

        if audio_data is None:
            return {
                "success": False,
                "text": "",
                "message": "Audio data is required."
            }

        try:

            if isinstance(audio_data, bytes):

                audio_buffer = io.BytesIO(
                    audio_data
                )

                with wave.open(
                    audio_buffer,
                    "rb"
                ) as wav_file:

                    frames = wav_file.readframes(
                        wav_file.getnframes()
                    )

                    sample_rate = wav_file.getframerate()
                    sample_width = wav_file.getsampwidth()
                    channels = wav_file.getnchannels()

                audio = sr.AudioData(
                    frames,
                    sample_rate,
                    sample_width
                )

            elif isinstance(
                audio_data,
                sr.AudioData
            ):

                audio = audio_data

            else:

                return {
                    "success": False,
                    "text": "",
                    "message": (
                        "Audio data must be WAV bytes "
                        "or a SpeechRecognition AudioData object."
                    )
                }

            text = self.recognizer.recognize_google(
                audio
            )

            text = text.strip()

            if not text:

                return {
                    "success": False,
                    "text": "",
                    "message": "No speech was recognized."
                }

            return {
                "success": True,
                "text": text,
                "message": (
                    "Speech converted to text successfully."
                )
            }

        except sr.UnknownValueError:

            return {
                "success": False,
                "text": "",
                "message": (
                    "Speech could not be understood."
                )
            }

        except sr.RequestError as error:

            return {
                "success": False,
                "text": "",
                "message": (
                    f"Speech recognition service error: {error}"
                )
            }

        except wave.Error as error:

            return {
                "success": False,
                "text": "",
                "message": (
                    f"Invalid WAV audio data: {error}"
                )
            }

        except Exception as error:

            return {
                "success": False,
                "text": "",
                "message": (
                    f"Speech-to-text error: {error}"
                )
            }

    def is_available(self) -> bool:

        return self.available

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "available": self.available
        }