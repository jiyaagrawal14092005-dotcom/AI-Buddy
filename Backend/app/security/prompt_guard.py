import re


class PromptGuard:

    def __init__(self):

        self._blocked_patterns = [
            r"ignore\s+(all\s+)?previous\s+instructions",
            r"ignore\s+(all\s+)?above\s+instructions",
            r"reveal\s+(your\s+)?system\s+prompt",
            r"show\s+(me\s+)?your\s+system\s+instructions",
            r"print\s+(your\s+)?hidden\s+instructions",
            r"bypass\s+(your\s+)?security",
            r"disable\s+(your\s+)?security",
            r"reveal\s+secret\s+key",
            r"reveal\s+api\s+key",
            r"give\s+me\s+the\s+password"
        ]

    def check_prompt(
        self,
        prompt: str
    ) -> dict:

        if prompt is None:
            return {
                "allowed": False,
                "message": "Prompt is required."
            }

        if not isinstance(prompt, str):
            return {
                "allowed": False,
                "message": "Prompt must be text."
            }

        prompt = prompt.strip()

        if not prompt:
            return {
                "allowed": False,
                "message": "Prompt cannot be empty."
            }

        for pattern in self._blocked_patterns:

            if re.search(
                pattern,
                prompt,
                re.IGNORECASE
            ):
                return {
                    "allowed": False,
                    "reason": "Suspicious prompt pattern detected.",
                    "message": "Prompt blocked by security policy."
                }

        return {
            "allowed": True,
            "sanitized_prompt": prompt,
            "message": "Prompt allowed."
        }

    def add_blocked_pattern(
        self,
        pattern: str
    ) -> dict:

        if not pattern:
            return {
                "success": False,
                "message": "Pattern is required."
            }

        self._blocked_patterns.append(pattern)

        return {
            "success": True,
            "message": "Blocked pattern added successfully."
        }

    def get_blocked_pattern_count(
        self
    ) -> int:

        return len(
            self._blocked_patterns
        )

    def sanitize_prompt(
        self,
        prompt: str
    ) -> str:

        if not isinstance(prompt, str):
            return ""

        prompt = prompt.strip()

        prompt = re.sub(
            r"\s+",
            " ",
            prompt
        )

        return prompt