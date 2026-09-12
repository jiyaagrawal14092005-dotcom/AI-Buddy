class TextToSpeech:

    def __init__(self):

        self.name = "text_to_speech"
        self.available = False

    def synthesize(
        self,
        text: str
    ) -> dict:

        if not isinstance(
            text,
            str
        ):

            return {
                "success": False,
                "audio": None,
                "message": (
                    "Text must be a string."
                )
            }

        text = text.strip()

        if not text:

            return {
                "success": False,
                "audio": None,
                "message": (
                    "Text cannot be empty."
                )
            }

        return {
            "success": False,
            "audio": None,
            "message": (
                "Text-to-speech engine is not "
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