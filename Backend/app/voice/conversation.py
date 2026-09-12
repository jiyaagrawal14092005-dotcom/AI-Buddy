from app.voice.voice_manager import VoiceManager
from app.voice.voice_command import VoiceCommand


class VoiceConversation:

    def __init__(
        self,
        wake_word: str = "ai buddy"
    ):

        self.voice_manager = VoiceManager(
            wake_word
        )

        self.active = False
        self.history = []

    def start(self) -> dict:

        if self.active:
            return {
                "success": False,
                "active": True,
                "message": (
                    "Voice conversation is already active."
                )
            }

        self.active = True

        return {
            "success": True,
            "active": True,
            "message": (
                "Voice conversation started."
            )
        }

    def stop(self) -> dict:

        if not self.active:
            return {
                "success": False,
                "active": False,
                "message": (
                    "Voice conversation is not active."
                )
            }

        self.active = False

        if self.voice_manager.command_listener.is_listening():
            self.voice_manager.stop_listening()

        return {
            "success": True,
            "active": False,
            "message": (
                "Voice conversation stopped."
            )
        }

    def process_input(
        self,
        text: str
    ) -> dict:

        if not self.active:
            return {
                "success": False,
                "active": False,
                "message": (
                    "Voice conversation is not active."
                )
            }

        result = self.voice_manager.process_text(
            text
        )

        if not result.get(
            "success",
            False
        ):
            return {
                **result,
                "active": True
            }

        command_data = result.get(
            "command"
        )

        command = None

        if isinstance(
            command_data,
            dict
        ):

            command = VoiceCommand()

            command.set_text(
                command_data.get(
                    "text",
                    ""
                )
            )

            command.set_command(
                command_data.get(
                    "command",
                    ""
                )
            )

            command.set_parameters(
                command_data.get(
                    "parameters",
                    {}
                )
            )

        history_item = {
            "user": text,
            "wake_word_detected": result.get(
                "wake_word_detected",
                False
            ),
            "command": (
                command.to_dict()
                if command is not None
                else None
            )
        }

        self.history.append(
            history_item
        )

        return {
            **result,
            "active": True
        }

    def process_audio(
        self,
        audio_data
    ) -> dict:

        if not self.active:
            return {
                "success": False,
                "active": False,
                "message": (
                    "Voice conversation is not active."
                )
            }

        result = self.voice_manager.listen(
            audio_data
        )

        return {
            **result,
            "active": True
        }

    def add_response(
        self,
        response: str
    ) -> dict:

        if not isinstance(
            response,
            str
        ):
            return {
                "success": False,
                "message": (
                    "Response must be a string."
                )
            }

        response = response.strip()

        if not response:
            return {
                "success": False,
                "message": (
                    "Response cannot be empty."
                )
            }

        if not self.active:
            return {
                "success": False,
                "message": (
                    "Voice conversation is not active."
                )
            }

        if self.history:

            self.history[-1][
                "assistant"
            ] = response

        else:

            self.history.append({
                "user": "",
                "assistant": response
            })

        return {
            "success": True,
            "response": response,
            "message": (
                "Assistant response added."
            )
        }

    def speak_response(
        self,
        response: str
    ) -> dict:

        if not self.active:
            return {
                "success": False,
                "message": (
                    "Voice conversation is not active."
                )
            }

        result = self.voice_manager.speak(
            response
        )

        if result.get(
            "success",
            False
        ):
            self.add_response(
                response
            )

        return result

    def start_listening(self) -> dict:

        if not self.active:
            return {
                "success": False,
                "message": (
                    "Voice conversation is not active."
                )
            }

        return self.voice_manager.start_listening()

    def stop_listening(self) -> dict:

        return self.voice_manager.stop_listening()

    def start_recording(self) -> dict:

        if not self.active:
            return {
                "success": False,
                "recording": False,
                "message": (
                    "Voice conversation is not active."
                )
            }

        return self.voice_manager.start_recording()

    def stop_recording(self) -> dict:

        return self.voice_manager.stop_recording()

    def clear_history(self) -> None:

        self.history.clear()

    def get_history(self) -> list:

        return list(
            self.history
        )

    def is_active(self) -> bool:

        return self.active

    def get_status(self) -> dict:

        return {
            "active": self.active,
            "history_count": len(
                self.history
            ),
            "voice_manager": (
                self.voice_manager.get_status()
            )
        }