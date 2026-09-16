import re


class PromptGuard:
    """
    Protects AI Buddy from common prompt-injection attempts
    and requests to expose protected system information.
    """

    def __init__(self):

        self._blocked_patterns = [
            # Instruction override attempts
            r"ignore\s+(all\s+)?previous\s+instructions",
            r"ignore\s+(all\s+)?above\s+instructions",
            r"disregard\s+(all\s+)?previous\s+instructions",
            r"disregard\s+(all\s+)?above\s+instructions",
            r"forget\s+(all\s+)?previous\s+instructions",
            r"override\s+(all\s+)?previous\s+instructions",

            # System prompt extraction
            r"reveal\s+(your\s+)?system\s+prompt",
            r"show\s+(me\s+)?your\s+system\s+prompt",
            r"show\s+(me\s+)?your\s+system\s+instructions",
            r"reveal\s+(your\s+)?system\s+instructions",
            r"print\s+(your\s+)?hidden\s+instructions",
            r"show\s+(me\s+)?hidden\s+instructions",
            r"tell\s+me\s+(your\s+)?hidden\s+prompt",

            # Secret / credential extraction
            r"reveal\s+(your\s+)?secret\s+key",
            r"reveal\s+(your\s+)?api\s+key",
            r"show\s+(me\s+)?your\s+api\s+key",
            r"give\s+me\s+the\s+password",
            r"show\s+(me\s+)?the\s+password",
            r"reveal\s+(the\s+)?credentials",
            r"show\s+(me\s+)?the\s+credentials",
            r"reveal\s+(your\s+)?token",
            r"show\s+(me\s+)?your\s+token",

            # Security bypass attempts
            r"bypass\s+(your\s+)?security",
            r"disable\s+(your\s+)?security",
            r"turn\s+off\s+(your\s+)?security",
            r"bypass\s+(the\s+)?security\s+check",
            r"bypass\s+(the\s+)?authentication",
            r"bypass\s+(the\s+)?authorization",

            # Policy manipulation
            r"ignore\s+(your\s+)?safety\s+rules",
            r"ignore\s+(your\s+)?security\s+rules",
            r"disable\s+(your\s+)?safety\s+rules",
            r"act\s+as\s+(an?\s+)?unrestricted\s+ai",
            r"act\s+as\s+(an?\s+)?uncensored\s+ai",
            r"developer\s+mode",
            r"jailbreak",

            # Internal reasoning / protected data extraction
            r"reveal\s+(your\s+)?chain\s+of\s+thought",
            r"show\s+(your\s+)?chain\s+of\s+thought",
            r"print\s+(your\s+)?internal\s+reasoning",
            r"show\s+(me\s+)?your\s+internal\s+reasoning",
        ]

    # =============================================================
    # PROMPT NORMALIZATION
    # =============================================================

    def _normalize_prompt(
        self,
        prompt: str
    ) -> str:
        """
        Normalize prompt text for safer pattern matching.
        """

        if not isinstance(prompt, str):
            return ""

        prompt = prompt.lower()

        # Normalize whitespace.
        prompt = re.sub(
            r"\s+",
            " ",
            prompt
        )

        return prompt.strip()

    # =============================================================
    # PROMPT CHECK
    # =============================================================

    def check_prompt(
        self,
        prompt: str
    ) -> dict:
        """
        Check whether a prompt is allowed by the security policy.
        """

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

        sanitized_prompt = self.sanitize_prompt(prompt)

        if not sanitized_prompt:
            return {
                "allowed": False,
                "message": "Prompt cannot be empty."
            }

        normalized_prompt = self._normalize_prompt(
            sanitized_prompt
        )

        for pattern in self._blocked_patterns:

            try:
                matched = re.search(
                    pattern,
                    normalized_prompt,
                    re.IGNORECASE
                )
            except re.error:
                # Invalid custom pattern should never crash
                # the AI Buddy request pipeline.
                continue

            if matched:
                return {
                    "allowed": False,
                    "reason": "Suspicious prompt pattern detected.",
                    "matched_pattern": pattern,
                    "message": "Prompt blocked by security policy."
                }

        return {
            "allowed": True,
            "sanitized_prompt": sanitized_prompt,
            "message": "Prompt allowed."
        }

    # =============================================================
    # ADD BLOCKED PATTERN
    # =============================================================

    def add_blocked_pattern(
        self,
        pattern: str
    ) -> dict:
        """
        Add a custom security pattern.
        """

        if not isinstance(pattern, str):
            return {
                "success": False,
                "message": "Pattern must be text."
            }

        pattern = pattern.strip()

        if not pattern:
            return {
                "success": False,
                "message": "Pattern is required."
            }

        # Validate regex before storing it.
        try:
            re.compile(pattern)
        except re.error:
            return {
                "success": False,
                "message": "Invalid regular expression."
            }

        if pattern in self._blocked_patterns:
            return {
                "success": False,
                "message": "Pattern already exists."
            }

        self._blocked_patterns.append(pattern)

        return {
            "success": True,
            "message": "Blocked pattern added successfully.",
            "pattern_count": len(
                self._blocked_patterns
            )
        }

    # =============================================================
    # REMOVE BLOCKED PATTERN
    # =============================================================

    def remove_blocked_pattern(
        self,
        pattern: str
    ) -> dict:
        """
        Remove a previously added security pattern.
        """

        if not isinstance(pattern, str):
            return {
                "success": False,
                "message": "Pattern must be text."
            }

        pattern = pattern.strip()

        if pattern not in self._blocked_patterns:
            return {
                "success": False,
                "message": "Pattern not found."
            }

        self._blocked_patterns.remove(pattern)

        return {
            "success": True,
            "message": "Blocked pattern removed successfully.",
            "pattern_count": len(
                self._blocked_patterns
            )
        }

    # =============================================================
    # PATTERN COUNT
    # =============================================================

    def get_blocked_pattern_count(
        self
    ) -> int:
        """
        Return the number of active blocked patterns.
        """

        return len(
            self._blocked_patterns
        )

    # =============================================================
    # SANITIZE PROMPT
    # =============================================================

    def sanitize_prompt(
        self,
        prompt: str
    ) -> str:
        """
        Clean prompt text without changing its intended content.
        """

        if not isinstance(prompt, str):
            return ""

        # Remove null bytes and ASCII control characters.
        prompt = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]",
            "",
            prompt
        )

        prompt = prompt.strip()

        # Normalize repeated whitespace.
        prompt = re.sub(
            r"\s+",
            " ",
            prompt
        )

        return prompt

    # =============================================================
    # STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:
        """
        Return PromptGuard status and configuration.
        """

        return {
            "name": "prompt_guard",
            "available": True,
            "enabled": True,
            "blocked_pattern_count": len(
                self._blocked_patterns
            ),
            "message": "Prompt guard is operational."
        }