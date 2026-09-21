import io
import wave

import speech_recognition as sr


class SpeechToText:

    def __init__(self):

        self.name = "speech_to_text"
        self.recognizer = sr.Recognizer()

        # Google Speech Recognition network request
        # ko indefinitely wait karne se prevent karta hai.
        self.recognizer.operation_timeout = 10

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

            # =========================================
            # WAV BYTES
            # =========================================

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

                # SpeechRecognition expects mono audio.
                # If WAV contains multiple channels, we still
                # preserve the existing behavior and let the
                # recognizer process the supplied audio data.
                audio = sr.AudioData(
                    frames,
                    sample_rate,
                    sample_width
                )

            # =========================================
            # SPEECHRECOGNITION AUDIO DATA
            # =========================================

            elif isinstance(
                audio_data,
                sr.AudioData
            ):

                audio = audio_data

            # =========================================
            # INVALID AUDIO TYPE
            # =========================================

            else:

                return {
                    "success": False,
                    "text": "",
                    "message": (
                        "Audio data must be WAV bytes "
                        "or a SpeechRecognition AudioData object."
                    )
                }

            # =========================================
            # GOOGLE SPEECH RECOGNITION
            # =========================================

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

        # =========================================
        # SPEECH NOT UNDERSTOOD
        # =========================================

        except sr.UnknownValueError:

            return {
                "success": False,
                "text": "",
                "message": (
                    "Speech could not be understood."
                ),
                "error_type": "UNKNOWN_VALUE",
                "retryable": False
            }

        # =========================================
        # GOOGLE STT SERVICE / NETWORK ERROR
        # =========================================

        except sr.RequestError as error:

            return {
                "success": False,
                "text": "",
                "message": (
                    f"Speech recognition service error: {error}"
                ),
                "error_type": "REQUEST_ERROR",
                "retryable": True
            }

        # =========================================
        # OPERATION TIMEOUT
        # =========================================

        except sr.WaitTimeoutError:

            return {
                "success": False,
                "text": "",
                "message": (
                    "Speech recognition timed out."
                ),
                "error_type": "TIMEOUT",
                "retryable": True
            }

        # =========================================
        # INVALID WAV
        # =========================================

        except wave.Error as error:

            return {
                "success": False,
                "text": "",
                "message": (
                    f"Invalid WAV audio data: {error}"
                ),
                "error_type": "WAV_ERROR",
                "retryable": False
            }

        # =========================================
        # UNEXPECTED ERROR
        # =========================================

        except Exception as error:

            return {
                "success": False,
                "text": "",
                "message": (
                    f"Speech-to-text error: {error}"
                ),
                "error_type": "UNKNOWN_ERROR",
                "retryable": True
            }

    def is_available(self) -> bool:

        return self.available

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "available": self.available,
            "operation_timeout": (
                self.recognizer.operation_timeout
            )
        }