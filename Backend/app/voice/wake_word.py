class WakeWordDetector:

    def __init__(
        self,
        wake_word: str = "ai buddy"
    ):

        if not isinstance(
            wake_word,
            str
        ):

            raise TypeError(
                "Wake word must be a string."
            )

        wake_word = wake_word.strip().lower()

        if not wake_word:

            raise ValueError(
                "Wake word cannot be empty."
            )

        self.wake_word = wake_word
        self.available = False

    def detect(
        self,
        text: str
    ) -> bool:

        if not isinstance(
            text,
            str
        ):

            return False

        text = text.strip().lower()

        if not text:

            return False

        return self.wake_word in text

    def get_wake_word(self) -> str:

        return self.wake_word

    def set_wake_word(
        self,
        wake_word: str
    ) -> None:

        if not isinstance(
            wake_word,
            str
        ):

            raise TypeError(
                "Wake word must be a string."
            )

        wake_word = wake_word.strip().lower()

        if not wake_word:

            raise ValueError(
                "Wake word cannot be empty."
            )

        self.wake_word = wake_word

    def is_available(self) -> bool:

        return self.available

    def get_status(self) -> dict:

        return {
            "wake_word": self.wake_word,
            "available": self.available
        }