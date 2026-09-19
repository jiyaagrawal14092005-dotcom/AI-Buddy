import threading
import time
from typing import Callable

import speech_recognition as sr

from app.voice.speech_to_text import SpeechToText


class CommandListener:
    """
    Continuous microphone command listener for AI Buddy.

    The listener:
    1. Captures microphone audio locally.
    2. Converts speech to text.
    3. Stores the latest recognized text.
    4. Optionally sends recognized text to a callback.
    5. Provides a single microphone owner for voice features.
    """

    def __init__(
        self,
        command_callback: Callable[[str], None] | None = None
    ):

        self.speech_to_text = SpeechToText()

        self.listening = False

        self._listener_thread = None
        self._stop_event = threading.Event()

        self.last_text = ""
        self.last_error = ""

        self.command_callback = command_callback

        # Indicates that the microphone is currently
        # being used by this listener.
        self.microphone_active = False

        # Used when another component needs to request
        # immediate microphone/listener shutdown.
        self._microphone_lock = threading.Lock()

    # ---------------------------------------------------------
    # CALLBACK
    # ---------------------------------------------------------

    def set_command_callback(
        self,
        command_callback: Callable[[str], None] | None
    ) -> dict:

        if (
            command_callback is not None
            and not callable(command_callback)
        ):

            return {
                "success": False,
                "message": (
                    "Command callback must be callable "
                    "or None."
                )
            }

        self.command_callback = command_callback

        return {
            "success": True,
            "message": (
                "Command callback updated successfully."
            )
        }

    def _send_command_callback(
        self,
        text: str
    ) -> None:

        if not self.command_callback:
            return

        if not isinstance(text, str):
            return

        text = text.strip()

        if not text:
            return

        try:

            self.command_callback(
                text
            )

        except Exception as error:

            self.last_error = (
                f"Command callback error: {error}"
            )

    # ---------------------------------------------------------
    # START LISTENING
    # ---------------------------------------------------------

    def start_listening(self) -> dict:

        if self.listening:

            return {
                "success": True,
                "listening": True,
                "microphone_active": (
                    self.microphone_active
                ),
                "message": (
                    "Command listener is already listening."
                )
            }

        self.last_error = ""

        self._stop_event.clear()

        self.listening = True

        self._listener_thread = threading.Thread(
            target=self._continuous_listen_loop,
            daemon=True
        )

        self._listener_thread.start()

        return {
            "success": True,
            "listening": True,
            "microphone_active": False,
            "message": (
                "Command listener started."
            )
        }

    # ---------------------------------------------------------
    # STOP LISTENING
    # ---------------------------------------------------------

    def stop_listening(self) -> dict:

        if not self.listening:

            return {
                "success": True,
                "listening": False,
                "microphone_active": False,
                "message": (
                    "Command listener is already stopped."
                )
            }

        self.listening = False

        self._stop_event.set()

        if self._listener_thread is not None:

            self._listener_thread.join(
                timeout=2
            )

        self._listener_thread = None

        self.microphone_active = False

        return {
            "success": True,
            "listening": False,
            "microphone_active": False,
            "message": (
                "Command listener stopped."
            )
        }

    # ---------------------------------------------------------
    # FORCE MICROPHONE STOP
    # ---------------------------------------------------------

    def stop_microphone(self) -> dict:
        """
        Request immediate microphone shutdown.

        This is useful for Jarvis stop handling.
        """

        self.listening = False

        self._stop_event.set()

        self.microphone_active = False

        return {
            "success": True,
            "listening": False,
            "microphone_active": False,
            "message": (
                "Microphone stop requested."
            )
        }

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def is_listening(self) -> bool:

        return self.listening

    def is_microphone_active(self) -> bool:

        return self.microphone_active

    # ---------------------------------------------------------
    # AUDIO → TEXT
    # ---------------------------------------------------------

    def listen(
        self,
        audio_data
    ) -> dict:

        if not self.listening:

            return {
                "success": False,
                "text": "",
                "message": (
                    "Command listener is not listening."
                )
            }

        result = self.speech_to_text.transcribe(
            audio_data
        )

        if result.get(
            "success",
            False
        ):

            text = result.get(
                "text",
                ""
            )

            self.last_text = text

            self._send_command_callback(
                text
            )

        return result

    # ---------------------------------------------------------
    # SINGLE MICROPHONE LISTEN
    # ---------------------------------------------------------

    def listen_from_microphone(
        self,
        timeout: float = 2,
        phrase_time_limit: float = 8
    ) -> dict:
        """
        Capture one speech segment from the microphone.

        This method is intended to be used by Jarvis so that
        only CommandListener owns the microphone.
        """

        if not self.listening:

            return {
                "success": False,
                "text": "",
                "message": (
                    "Command listener is not listening."
                )
            }

        try:

            recognizer = (
                self.speech_to_text.recognizer
            )

            with self._microphone_lock:

                if (
                    not self.listening
                    or self._stop_event.is_set()
                ):

                    return {
                        "success": True,
                        "text": "",
                        "stopped": True,
                        "message": (
                            "Microphone listening stopped."
                        )
                    }

                self.microphone_active = True

                try:

                    with sr.Microphone() as source:

                        # Only calibrate when necessary.
                        # Keeping this short prevents unnecessary
                        # delay before every command.
                        if not getattr(
                            self,
                            "_ambient_calibrated",
                            False
                        ):

                            recognizer.adjust_for_ambient_noise(
                                source,
                                duration=0.3
                            )

                            self._ambient_calibrated = True

                        if (
                            not self.listening
                            or self._stop_event.is_set()
                        ):

                            return {
                                "success": True,
                                "text": "",
                                "stopped": True,
                                "message": (
                                    "Microphone listening stopped."
                                )
                            }

                        audio_data = recognizer.listen(
                            source,
                            timeout=timeout,
                            phrase_time_limit=phrase_time_limit
                        )

                    if (
                        not self.listening
                        or self._stop_event.is_set()
                    ):

                        return {
                            "success": True,
                            "text": "",
                            "stopped": True,
                            "message": (
                                "Microphone listening stopped."
                            )
                        }

                    return self.listen(
                        audio_data
                    )

                finally:

                    self.microphone_active = False

        except sr.WaitTimeoutError:

            self.microphone_active = False

            return {
                "success": True,
                "text": "",
                "timeout": True,
                "message": (
                    "No speech detected within the listening timeout."
                )
            }

        except sr.UnknownValueError:

            self.microphone_active = False

            self.last_error = (
                "Speech could not be understood."
            )

            return {
                "success": False,
                "text": "",
                "message": (
                    "Speech could not be understood."
                )
            }

        except sr.RequestError as error:

            self.microphone_active = False

            self.last_error = (
                f"Speech recognition service error: {error}"
            )

            return {
                "success": False,
                "text": "",
                "message": self.last_error
            }

        except Exception as error:

            self.microphone_active = False

            self.last_error = str(
                error
            )

            return {
                "success": False,
                "text": "",
                "message": (
                    f"Microphone listening error: {error}"
                )
            }

    # ---------------------------------------------------------
    # CONTINUOUS LISTEN LOOP
    # ---------------------------------------------------------

    def _continuous_listen_loop(
        self
    ):

        try:

            while (
                self.listening
                and not self._stop_event.is_set()
            ):

                result = (
                    self.listen_from_microphone(
                        timeout=2,
                        phrase_time_limit=8
                    )
                )

                if (
                    not self.listening
                    or self._stop_event.is_set()
                ):
                    break

                if result.get(
                    "timeout",
                    False
                ):
                    continue

                if not result.get(
                    "success",
                    False
                ):

                    if result.get(
                        "message"
                    ):

                        self.last_error = (
                            result["message"]
                        )

                    time.sleep(
                        0.2
                    )

        except Exception as error:

            self.last_error = str(
                error
            )

        finally:

            self.microphone_active = False

            self.listening = False

            self._stop_event.set()

    # ---------------------------------------------------------
    # RESET STATE
    # ---------------------------------------------------------

    def reset(self) -> dict:

        self.last_text = ""

        self.last_error = ""

        self._ambient_calibrated = False

        return {
            "success": True,
            "message": (
                "Command listener state reset."
            )
        }

    # ---------------------------------------------------------
    # COMPLETE STATUS
    # ---------------------------------------------------------

    def get_status(self) -> dict:

        return {
            "listening": self.listening,
            "microphone_active": (
                self.microphone_active
            ),
            "last_text": self.last_text,
            "last_error": self.last_error,
            "callback_configured": (
                self.command_callback is not None
            ),
            "speech_to_text": (
                self.speech_to_text.get_status()
                if hasattr(
                    self.speech_to_text,
                    "get_status"
                )
                else {
                    "name": "speech_to_text",
                    "available": True
                }
            )
        }