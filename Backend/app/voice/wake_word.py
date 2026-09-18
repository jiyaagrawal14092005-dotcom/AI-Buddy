import os
import re


class WakeWordDetector:
    """
    Local wake-word gate for AI Buddy.

    The wake word is configurable through:
    1. Constructor argument
    2. AI_BUDDY_WAKE_WORD environment variable
    3. Default value: "Zarvis"

    The detector only decides whether the wake word is present
    in already available text. It does not send audio anywhere.
    """

    DEFAULT_WAKE_WORD = "Zarvis"

    def __init__(
        self,
        wake_word: str | None = None
    ):
        if wake_word is None:
            wake_word = os.getenv(
                "AI_BUDDY_WAKE_WORD",
                self.DEFAULT_WAKE_WORD
            )

        if not isinstance(
            wake_word,
            str
        ):
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

    def _normalize_text(
        self,
        text: str
    ) -> str:

        if not isinstance(
            text,
            str
        ):
            return ""

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

    def _get_wake_word_variations(
        self
    ) -> list[str]:

        # Temporary Zarvis pronunciation variations.
        # These can be changed later without changing the
        # main Jarvis pipeline.
        if self.wake_word == "zarvis":

            return [
                "zarvis",
                "zarvis",
                "jarvis",
                "jarvis"
            ]

        return [
            self.wake_word
        ]

    def detect(
        self,
        text: str
    ) -> bool:

        if not self.enabled:
            return False

        if not isinstance(
            text,
            str
        ):
            return False

        normalized_text = self._normalize_text(
            text
        )

        if not normalized_text:
            return False

        variations = self._get_wake_word_variations()

        for variation in variations:

            normalized_variation = (
                self._normalize_text(
                    variation
                )
            )

            if not normalized_variation:
                continue

            # Word-boundary based matching prevents
            # accidental partial matches.
            pattern = (
                r"(?<!\w)"
                + re.escape(
                    normalized_variation
                )
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                normalized_text
            ):
                return True

        return False

    def extract_command(
        self,
        text: str
    ) -> str:

        if not isinstance(
            text,
            str
        ):
            return ""

        normalized_text = self._normalize_text(
            text
        )

        if not normalized_text:
            return ""

        variations = self._get_wake_word_variations()

        for variation in variations:

            normalized_variation = (
                self._normalize_text(
                    variation
                )
            )

            if not normalized_variation:
                continue

            pattern = (
                r"(?<!\w)"
                + re.escape(
                    normalized_variation
                )
                + r"(?!\w)"
            )

            match = re.search(
                pattern,
                normalized_text
            )

            if match:

                command = (
                    normalized_text[
                        match.end():
                    ]
                    .strip()
                )

                return command

        return ""

    def process(
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
                "wake_word": self.wake_word,
                "command": "",
                "message": (
                    "Text must be a string."
                )
            }

        if not self.enabled:

            return {
                "success": False,
                "wake_word_detected": False,
                "wake_word": self.wake_word,
                "command": "",
                "message": (
                    "Wake word detection is disabled."
                )
            }

        normalized_text = self._normalize_text(
            text
        )

        if not normalized_text:

            return {
                "success": True,
                "wake_word_detected": False,
                "wake_word": self.wake_word,
                "command": "",
                "message": (
                    "No speech text was provided."
                )
            }

        detected = self.detect(
            normalized_text
        )

        if not detected:

            # IMPORTANT PRIVACY GATE:
            # Do not return the original text as
            # an executable command.
            return {
                "success": True,
                "wake_word_detected": False,
                "wake_word": self.wake_word,
                "command": "",
                "message": (
                    "Wake word not detected. "
                    "Input blocked by local wake-word gate."
                )
            }

        command = self.extract_command(
            normalized_text
        )

        if not command:

            return {
                "success": True,
                "wake_word_detected": True,
                "wake_word": self.wake_word,
                "command": "",
                "message": (
                    "Wake word detected. "
                    "No command provided."
                )
            }

        return {
            "success": True,
            "wake_word_detected": True,
            "wake_word": self.wake_word,
            "command": command,
            "message": (
                "Wake word detected and "
                "command extracted."
            )
        }

    def set_wake_word(
        self,
        wake_word: str
    ) -> dict:

        if not isinstance(
            wake_word,
            str
        ):

            return {
                "success": False,
                "message": (
                    "Wake word must be a string."
                )
            }

        wake_word = wake_word.strip().lower()

        if not wake_word:

            return {
                "success": False,
                "message": (
                    "Wake word cannot be empty."
                )
            }

        self.wake_word = wake_word

        return {
            "success": True,
            "wake_word": self.wake_word,
            "message": (
                "Wake word updated successfully."
            )
        }

    def enable(self) -> dict:

        self.enabled = True

        return {
            "success": True,
            "enabled": True,
            "message": (
                "Wake word detection enabled."
            )
        }

    def disable(self) -> dict:

        self.enabled = False

        return {
            "success": True,
            "enabled": False,
            "message": (
                "Wake word detection disabled."
            )
        }

    def is_enabled(self) -> bool:

        return self.enabled

    def get_wake_word(self) -> str:

        return self.wake_word

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "wake_word": self.wake_word,
            "enabled": self.enabled,
            "variations": (
                self._get_wake_word_variations()
            )
        }