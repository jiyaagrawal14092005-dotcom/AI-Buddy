from app.voice.text_to_speech import TextToSpeech


class VoiceResponse:

    def __init__(
        self,
        text_to_speech: TextToSpeech | None = None
    ):

        if text_to_speech is not None:
            self.text_to_speech = text_to_speech
        else:
            self.text_to_speech = TextToSpeech()

        self.last_response = ""

    def prepare_response(
        self,
        text: str
    ) -> dict:

        if not isinstance(
            text,
            str
        ):
            return {
                "success": False,
                "response": "",
                "message": "Response text must be a string."
            }

        text = text.strip()

        if not text:
            return {
                "success": False,
                "response": "",
                "message": "Response text cannot be empty."
            }

        self.last_response = text

        return {
            "success": True,
            "response": text,
            "message": "Voice response prepared successfully."
        }

    def speak(
        self,
        text: str
    ) -> dict:

        result = self.text_to_speech.synthesize(
            text
        )

        if result.get("success", False):

            self.last_response = text.strip()

        return result

    def get_last_response(self) -> str:

        return self.last_response

    def clear(self) -> None:

        self.last_response = ""

    def is_available(self) -> bool:

        return self.text_to_speech.is_available()

    def get_status(self) -> dict:

        return {
            "name": "voice_response",
            "available": self.is_available(),
            "last_response": self.last_response,
            "text_to_speech": (
                self.text_to_speech.get_status()
            )
        }