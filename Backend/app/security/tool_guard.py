class ToolGuard:

    def __init__(self):

        self._allowed_tools = {
            "task",
            "reminder",
            "timer",
            "weather",
            "email",
            "calendar",
            "file",
            "search",
            "browser"
        }

        self._restricted_tools = {
            "email",
            "calendar",
            "file",
            "browser"
        }

    def is_tool_allowed(
        self,
        tool_name: str
    ) -> bool:

        if not tool_name:
            return False

        return tool_name.lower() in self._allowed_tools

    def requires_approval(
        self,
        tool_name: str
    ) -> bool:

        if not tool_name:
            return False

        return (
            tool_name.lower()
            in self._restricted_tools
        )

    def check_tool(
        self,
        tool_name: str,
        user_id: str,
        permission_granted: bool = False,
        approval_granted: bool = False
    ) -> dict:

        if not user_id:
            return {
                "allowed": False,
                "message": "User authentication is required."
            }

        if not tool_name:
            return {
                "allowed": False,
                "message": "Tool name is required."
            }

        tool_name = tool_name.lower()

        if not self.is_tool_allowed(tool_name):
            return {
                "allowed": False,
                "message": "Tool is not registered."
            }

        if not permission_granted:
            return {
                "allowed": False,
                "message": "Required permission is not granted."
            }

        if self.requires_approval(tool_name):

            if not approval_granted:
                return {
                    "allowed": False,
                    "requires_approval": True,
                    "message": "User approval is required."
                }

        return {
            "allowed": True,
            "tool": tool_name,
            "user_id": user_id,
            "message": "Tool execution allowed."
        }

    def register_tool(
        self,
        tool_name: str,
        restricted: bool = False
    ) -> dict:

        if not tool_name:
            return {
                "success": False,
                "message": "Tool name is required."
            }

        tool_name = tool_name.lower()

        self._allowed_tools.add(tool_name)

        if restricted:
            self._restricted_tools.add(tool_name)

        return {
            "success": True,
            "tool": tool_name,
            "restricted": restricted,
            "message": "Tool registered successfully."
        }

    def remove_tool(
        self,
        tool_name: str
    ) -> dict:

        if not tool_name:
            return {
                "success": False,
                "message": "Tool name is required."
            }

        tool_name = tool_name.lower()

        self._allowed_tools.discard(tool_name)
        self._restricted_tools.discard(tool_name)

        return {
            "success": True,
            "message": "Tool removed successfully."
        }

    def get_allowed_tools(self) -> list:

        return sorted(
            self._allowed_tools
        )
    