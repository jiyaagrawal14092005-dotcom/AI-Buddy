import re


class WakeWordDetector:

    def __init__(self, wake_word: str = "ai buddy"):

        if not isinstance(wake_word, str):
            raise ValueError(
                "Wake word must be a string."
            )

        wake_word = wake_word.strip().lower()

        if not wake_word:
            raise ValueError(
                "Wake word cannot be empty."
            )

        self.name = "wake_word"
        self.wake_word = wake_word
        self.enabled = True

    def _normalize_text(self, text: str) -> str:

        text = text.lower().strip()

        text = re.sub(
            r"[^\w\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def _get_wake_word_variations(self) -> list[str]:

        if self.wake_word == "ai buddy":

            return [
                "ai buddy",
                "a buddy",
                "hey buddy",
                "hi buddy",
                "hey ai buddy",
                "hi ai buddy",
                "ai body",
                "a body",
                "i buddy",
                "eye buddy",
                "ay buddy",
                "ai buddies",
                "aibuddy"
            ]

        return [
            self.wake_word
        ]

    def detect(self, text: str) -> bool:

        if not self.enabled:
            return False

        if not isinstance(text, str):
            return False

        normalized_text = self._normalize_text(
            text
        )

        if not normalized_text:
            return False

        variations = self._get_wake_word_variations()

        for variation in variations:

            normalized_variation = (
                self._normalize_text(variation)
            )

            if (
                normalized_variation in normalized_text
            ):
                return True

        return False

    def extract_command(
        self,
        text: str
    ) -> str:

        if not isinstance(text, str):
            return ""

        normalized_text = self._normalize_text(
            text
        )

        if not normalized_text:
            return ""

        variations = self._get_wake_word_variations()

        for variation in variations:

            normalized_variation = (
                self._normalize_text(variation)
            )

            if normalized_variation in normalized_text:

                command = normalized_text.replace(
                    normalized_variation,
                    "",
                    1
                ).strip()

                return command

        return normalized_text

    def process(
        self,
        text: str
    ) -> dict:

        if not isinstance(text, str):

            return {
                "success": False,
                "wake_word_detected": False,
                "wake_word": self.wake_word,
                "command": "",
                "message": "Text must be a string."
            }

        if not self.enabled:

            return {
                "success": False,
                "wake_word_detected": False,
                "wake_word": self.wake_word,
                "command": text.strip(),
                "message": "Wake word detection is disabled."
            }

        detected = self.detect(text)

        if not detected:

            return {
                "success": True,
                "wake_word_detected": False,
                "wake_word": self.wake_word,
                "command": text.strip(),
                "message": "Wake word not detected."
            }

        command = self.extract_command(text)

        if not command:

            return {
                "success": True,
                "wake_word_detected": True,
                "wake_word": self.wake_word,
                "command": "",
                "message": "Wake word detected. No command provided."
            }

        return {
            "success": True,
            "wake_word_detected": True,
            "wake_word": self.wake_word,
            "command": command,
            "message": "Wake word detected and command extracted."
        }

    def set_wake_word(
        self,
        wake_word: str
    ) -> dict:

        if not isinstance(wake_word, str):

            return {
                "success": False,
                "message": "Wake word must be a string."
            }

        wake_word = wake_word.strip().lower()

        if not wake_word:

            return {
                "success": False,
                "message": "Wake word cannot be empty."
            }

        self.wake_word = wake_word

        return {
            "success": True,
            "wake_word": self.wake_word,
            "message": "Wake word updated successfully."
        }

    def enable(self) -> dict:

        self.enabled = True

        return {
            "success": True,
            "enabled": True,
            "message": "Wake word detection enabled."
        }

    def disable(self) -> dict:

        self.enabled = False

        return {
            "success": True,
            "enabled": False,
            "message": "Wake word detection disabled."
        }

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "wake_word": self.wake_word,
            "enabled": self.enabled,
            "variations": self._get_wake_word_variations()
        }