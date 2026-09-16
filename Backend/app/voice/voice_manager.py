from app.voice.speech_to_text import SpeechToText
from app.voice.text_to_speech import TextToSpeech
from app.voice.wake_word import WakeWordDetector
from app.voice.command_listener import CommandListener
from app.voice.voice_command import VoiceCommand
from app.voice.voice_response import VoiceResponse
from app.voice.audio_manager import AudioManager


class VoiceManager:

    def __init__(
        self,
        wake_word: str = "ai buddy"
    ):

        self.speech_to_text = SpeechToText()

        self.text_to_speech = TextToSpeech()

        self.wake_word_detector = WakeWordDetector(
            wake_word
        )

        self.command_listener = CommandListener()

        self.voice_response = VoiceResponse(
            self.text_to_speech
        )

        self.audio_manager = AudioManager()

        self.enabled = True

    def process_text(
        self,
        text: str
    ) -> dict:

        if not isinstance(
            text,
            str
        ):

            return {
                "success": False,
                "wake_word_detected": False,
                "text": "",
                "command": None,
                "message": (
                    "Voice input must be a string."
                )
            }

        text = text.strip()

        if not text:

            return {
                "success": False,
                "wake_word_detected": False,
                "text": "",
                "command": None,
                "message": (
                    "Voice input cannot be empty."
                )
            }

        if not self.enabled:

            return {
                "success": False,
                "wake_word_detected": False,
                "text": text,
                "command": None,
                "message": (
                    "Voice manager is disabled."
                )
            }

        # ---------------------------------
        # WAKE WORD PROCESSING
        # ---------------------------------

        wake_word_result = (
            self.wake_word_detector.process(
                text
            )
        )

        if not wake_word_result.get(
            "success",
            False
        ):

            return {
                "success": False,
                "wake_word_detected": False,
                "text": text,
                "command": None,
                "message": (
                    wake_word_result.get(
                        "message",
                        "Unable to process wake word."
                    )
                )
            }

        wake_word_detected = (
            wake_word_result.get(
                "wake_word_detected",
                False
            )
        )

        command_text = (
            wake_word_result.get(
                "command",
                ""
            )
        )

        # ---------------------------------
        # CREATE VOICE COMMAND
        # ---------------------------------

        if not command_text:

            return {
                "success": True,
                "wake_word_detected": (
                    wake_word_detected
                ),
                "text": text,
                "command": None,
                "message": (
                    "Wake word detected but no command was provided."
                    if wake_word_detected
                    else "No command was provided."
                )
            }

        command = VoiceCommand()

        command.set_text(
            command_text
        )

        command.set_command(
            command_text
        )

        # ---------------------------------
        # RETURN PROCESSED COMMAND
        # ---------------------------------

        return {
            "success": True,
            "wake_word_detected": (
                wake_word_detected
            ),
            "text": text,
            "command": command.to_dict(),
            "message": (
                "Wake word detected and command extracted."
                if wake_word_detected
                else "Voice command processed."
            )
        }

    def listen(
        self,
        audio_data
    ) -> dict:

        if not self.enabled:

            return {
                "success": False,
                "text": "",
                "message": (
                    "Voice manager is disabled."
                )
            }

        if not self.command_listener.is_listening():

            self.command_listener.start_listening()

        return self.command_listener.listen(
            audio_data
        )

    def start_listening(self) -> dict:

        if not self.enabled:

            return {
                "success": False,
                "listening": False,
                "message": (
                    "Voice manager is disabled."
                )
            }

        return self.command_listener.start_listening()

    def stop_listening(self) -> dict:

        return self.command_listener.stop_listening()

    def speak(
        self,
        text: str
    ) -> dict:

        if not self.enabled:

            return {
                "success": False,
                "message": (
                    "Voice manager is disabled."
                )
            }

        return self.voice_response.speak(
            text
        )

    def prepare_response(
        self,
        text: str
    ) -> dict:

        if not self.enabled:

            return {
                "success": False,
                "response": "",
                "message": (
                    "Voice manager is disabled."
                )
            }

        return self.voice_response.prepare_response(
            text
        )

    def start_recording(self) -> dict:

        if not self.enabled:

            return {
                "success": False,
                "recording": False,
                "message": (
                    "Voice manager is disabled."
                )
            }

        return self.audio_manager.start_recording()

    def stop_recording(self) -> dict:

        return self.audio_manager.stop_recording()

    def start_playback(self) -> dict:

        if not self.enabled:

            return {
                "success": False,
                "playing": False,
                "message": (
                    "Voice manager is disabled."
                )
            }

        return self.audio_manager.start_playback()

    def stop_playback(self) -> dict:

        return self.audio_manager.stop_playback()

    def enable(self) -> None:

        self.enabled = True

    def disable(self) -> None:

        self.enabled = False

        if self.command_listener.is_listening():

            self.command_listener.stop_listening()

        if self.audio_manager.is_recording():

            self.audio_manager.stop_recording()

        if self.audio_manager.is_playing():

            self.audio_manager.stop_playback()

    def is_enabled(self) -> bool:

        return self.enabled

    def get_status(self) -> dict:

        return {
            "name": "voice_manager",
            "enabled": self.enabled,
            "speech_to_text": (
                self.speech_to_text.get_status()
            ),
            "text_to_speech": (
                self.text_to_speech.get_status()
            ),
            "wake_word": (
                self.wake_word_detector.get_status()
            ),
            "command_listener": (
                self.command_listener.get_status()
            ),
            "voice_response": (
                self.voice_response.get_status()
            ),
            "audio_manager": (
                self.audio_manager.get_status()
            )
        }