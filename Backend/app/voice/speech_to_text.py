class SpeechToText:

    def __init__(self):

        self.name = "speech_to_text"
        self.available = False

    def transcribe(
        self,
        audio_data
    ) -> dict:

        if audio_data is None:

            return {
                "success": False,
                "text": "",
                "message": (
                    "Audio data is required."
                )
            }

        return {
            "success": False,
            "text": "",
            "message": (
                "Speech-to-text engine is not "
                "configured yet."
            )
        }

    def is_available(self) -> bool:

        return self.available

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "available": self.available
        }