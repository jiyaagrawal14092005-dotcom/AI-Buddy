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
        self.voice_response = VoiceResponse()
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
                "message": "Text must be a string."
            }

        text = text.strip()

        if not text:
            return {
                "success": False,
                "wake_word_detected": False,
                "text": "",
                "command": None,
                "message": "Text cannot be empty."
            }

        if not self.enabled:
            return {
                "success": False,
                "wake_word_detected": False,
                "text": text,
                "command": None,
                "message": "Voice manager is disabled."
            }

        wake_word_detected = (
            self.wake_word_detector.detect(
                text
            )
        )

        command = VoiceCommand(
            text
        )

        return {
            "success": True,
            "wake_word_detected": wake_word_detected,
            "text": text,
            "command": command.to_dict(),
            "message": (
                "Wake word detected."
                if wake_word_detected
                else "Wake word not detected."
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
                "message": "Voice manager is disabled."
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
                "message": "Voice manager is disabled."
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
                "message": "Voice manager is disabled."
            }

        return self.voice_response.speak(
            text
        )

    def prepare_response(
        self,
        text: str
    ) -> dict:

        return self.voice_response.prepare_response(
            text
        )

    def start_recording(self) -> dict:

        if not self.enabled:
            return {
                "success": False,
                "recording": False,
                "message": "Voice manager is disabled."
            }

        return self.audio_manager.start_recording()

    def stop_recording(self) -> dict:

        return self.audio_manager.stop_recording()

    def set_audio_data(
        self,
        audio_data
    ) -> dict:

        return self.audio_manager.set_audio_data(
            audio_data
        )

    def start_playback(self) -> dict:

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