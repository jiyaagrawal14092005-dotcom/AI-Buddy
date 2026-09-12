class VoiceCommand:

    def __init__(
        self,
        text: str = ""
    ):

        self.text = ""
        self.command = ""
        self.parameters = {}

        if text:
            self.set_text(text)

    def set_text(
        self,
        text: str
    ) -> None:

        if not isinstance(
            text,
            str
        ):
            raise TypeError(
                "Voice command text must be a string."
            )

        text = text.strip()

        if not text:
            raise ValueError(
                "Voice command text cannot be empty."
            )

        self.text = text
        self.command = text
        self.parameters = {}

    def set_command(
        self,
        command: str
    ) -> None:

        if not isinstance(
            command,
            str
        ):
            raise TypeError(
                "Command must be a string."
            )

        command = command.strip()

        if not command:
            raise ValueError(
                "Command cannot be empty."
            )

        self.command = command

    def set_parameters(
        self,
        parameters: dict
    ) -> None:

        if not isinstance(
            parameters,
            dict
        ):
            raise TypeError(
                "Command parameters must be a dictionary."
            )

        self.parameters = dict(
            parameters
        )

    def add_parameter(
        self,
        key: str,
        value
    ) -> None:

        if not isinstance(
            key,
            str
        ):
            raise TypeError(
                "Parameter key must be a string."
            )

        key = key.strip()

        if not key:
            raise ValueError(
                "Parameter key cannot be empty."
            )

        self.parameters[key] = value

    def get_text(self) -> str:

        return self.text

    def get_command(self) -> str:

        return self.command

    def get_parameters(self) -> dict:

        return dict(
            self.parameters
        )

    def is_valid(self) -> bool:

        return bool(
            self.command.strip()
        )

    def to_dict(self) -> dict:

        return {
            "text": self.text,
            "command": self.command,
            "parameters": dict(
                self.parameters
            )
        }