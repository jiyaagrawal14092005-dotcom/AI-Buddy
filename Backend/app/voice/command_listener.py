from app.voice.speech_to_text import SpeechToText


class CommandListener:

    def __init__(self):

        self.speech_to_text = SpeechToText()
        self.listening = False

    def start_listening(self) -> dict:

        if self.listening:
            return {
                "success": False,
                "listening": True,
                "message": "Command listener is already active."
            }

        self.listening = True

        return {
            "success": True,
            "listening": True,
            "message": "Command listener started."
        }

    def stop_listening(self) -> dict:

        if not self.listening:
            return {
                "success": False,
                "listening": False,
                "message": "Command listener is not active."
            }

        self.listening = False

        return {
            "success": True,
            "listening": False,
            "message": "Command listener stopped."
        }

    def listen(
        self,
        audio_data
    ) -> dict:

        if not self.listening:
            return {
                "success": False,
                "text": "",
                "message": (
                    "Command listener is not active."
                )
            }

        result = self.speech_to_text.transcribe(
            audio_data
        )

        return {
            "success": result.get(
                "success",
                False
            ),
            "text": result.get(
                "text",
                ""
            ),
            "message": result.get(
                "message",
                "Unable to process audio."
            )
        }

    def is_listening(self) -> bool:

        return self.listening

    def get_status(self) -> dict:

        return {
            "listening": self.listening,
            "speech_to_text": (
                self.speech_to_text.get_status()
            )
        }