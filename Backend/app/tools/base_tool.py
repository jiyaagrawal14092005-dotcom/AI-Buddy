class BaseTool:

    def __init__(
        self,
        name: str,
        description: str
    ):

        if not isinstance(
            name,
            str
        ) or not name.strip():

            raise ValueError(
                "Tool name must be a non-empty string."
            )

        if not isinstance(
            description,
            str
        ) or not description.strip():

            raise ValueError(
                "Tool description must be a non-empty string."
            )

        self.name = name.strip()
        self.description = description.strip()

    # =================================
    # TOOL INFORMATION
    # =================================

    def get_info(self) -> dict:

        return {
            "name": self.name,
            "description": self.description
        }

    # =================================
    # CHECK TOOL NAME
    # =================================

    def matches(
        self,
        tool_name: str
    ) -> bool:

        if not isinstance(
            tool_name,
            str
        ):
            return False

        return (
            self.name.lower()
            == tool_name.strip().lower()
        )

    # =================================
    # EXECUTE TOOL
    # =================================

    def execute(
        self,
        parameters: dict | None = None
    ) -> dict:

        raise NotImplementedError(
            f"Tool '{self.name}' "
            "must implement the execute() method."
        )

    # =================================
    # TOOL STATUS
    # =================================

    def is_available(self) -> bool:

        return True