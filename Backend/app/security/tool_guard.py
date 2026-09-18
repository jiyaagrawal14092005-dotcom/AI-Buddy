class ToolGuard:
    """
    Controls which tools AI Buddy can execute and determines
    whether a tool/action requires additional approval.
    """

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
            "browser",
            "shopping",
            "application_launcher",
            "time_tool",
        }

        # Tools that normally require explicit user approval.
        self._restricted_tools = {
            "email",
            "calendar",
            "file",
        }

        # Shopping actions that require explicit user approval.
        # Search, comparison, cart operations do not require approval.
        # Purchase preparation is approval-sensitive.
        self._restricted_shopping_actions = {
            "purchase",
            "buy",
        }

        # Browser actions that can change external state.
        self._restricted_browser_actions = {
            "click",
            "fill",
        }

        # Additional browser actions that should be treated
        # as sensitive when AI Buddy performs them.
        self._sensitive_browser_actions = {
            "navigate",
            "open",
            "click",
            "fill",
        }

    # =============================================================
    # NORMALIZATION
    # =============================================================

    def _normalize_tool_name(
        self,
        tool_name: str
    ) -> str:

        if not isinstance(tool_name, str):
            return ""

        return tool_name.strip().lower()

    def _normalize_action(
        self,
        action: str | None
    ) -> str:

        if not isinstance(action, str):
            return ""

        return action.strip().lower()

    # =============================================================
    # TOOL ALLOWED
    # =============================================================

    def is_tool_allowed(
        self,
        tool_name: str
    ) -> bool:

        tool_name = self._normalize_tool_name(
            tool_name
        )

        if not tool_name:
            return False

        return tool_name in self._allowed_tools

    # =============================================================
    # TOOL RESTRICTED
    # =============================================================

    def is_tool_restricted(
        self,
        tool_name: str
    ) -> bool:

        tool_name = self._normalize_tool_name(
            tool_name
        )

        if not tool_name:
            return False

        return tool_name in self._restricted_tools

    # =============================================================
    # SHOPPING ACTION RESTRICTED
    # =============================================================

    def is_shopping_action_restricted(
        self,
        action: str | None
    ) -> bool:

        action = self._normalize_action(
            action
        )

        if not action:
            return False

        return action in self._restricted_shopping_actions

    # =============================================================
    # BROWSER ACTION RESTRICTED
    # =============================================================

    def is_browser_action_restricted(
        self,
        action: str | None
    ) -> bool:

        action = self._normalize_action(
            action
        )

        if not action:
            return False

        return action in self._restricted_browser_actions

    # =============================================================
    # BROWSER ACTION SENSITIVE
    # =============================================================

    def is_browser_action_sensitive(
        self,
        action: str | None
    ) -> bool:

        action = self._normalize_action(
            action
        )

        if not action:
            return False

        return action in self._sensitive_browser_actions

    # =============================================================
    # TOOL APPROVAL
    # =============================================================

    def requires_approval(
        self,
        tool_name: str,
        action: str | None = None
    ) -> bool:

        tool_name = self._normalize_tool_name(
            tool_name
        )

        action = self._normalize_action(
            action
        )

        if not tool_name:
            return False

        # ---------------------------------------------------------
        # BROWSER USES ACTION-LEVEL SECURITY
        # ---------------------------------------------------------

        if tool_name == "browser":

            if not action:
                return True

            return (
                action
                in self._restricted_browser_actions
            )

        # ---------------------------------------------------------
        # SHOPPING USES ACTION-LEVEL SECURITY
        # ---------------------------------------------------------

        if tool_name == "shopping":

            if not action:
                # Unknown shopping action should not execute
                # without explicit approval.
                return True

            return (
                action
                in self._restricted_shopping_actions
            )

        # ---------------------------------------------------------
        # NORMAL TOOL-LEVEL SECURITY
        # ---------------------------------------------------------

        return (
            tool_name
            in self._restricted_tools
        )

    # =============================================================
    # CHECK USER ID
    # =============================================================

    def _validate_user_id(
        self,
        user_id: str
    ) -> dict:

        if user_id is None:
            return {
                "valid": False,
                "message": "User authentication is required."
            }

        if not isinstance(user_id, str):
            return {
                "valid": False,
                "message": "User ID must be text."
            }

        user_id = user_id.strip()

        if not user_id:
            return {
                "valid": False,
                "message": "User authentication is required."
            }

        return {
            "valid": True,
            "sanitized": user_id
        }

    # =============================================================
    # CHECK TOOL
    # =============================================================

    def check_tool(
        self,
        tool_name: str,
        user_id: str,
        permission_granted: bool = False,
        approval_granted: bool = False,
        action: str | None = None
    ) -> dict:
        """
        Perform the complete tool security check.

        Order:
        1. Validate user
        2. Validate tool
        3. Check registration
        4. Check permission
        5. Check approval
        6. Allow execution
        """

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["valid"]:
            return {
                "allowed": False,
                "message": user_result["message"]
            }

        if tool_name is None:
            return {
                "allowed": False,
                "message": "Tool name is required."
            }

        tool_name = self._normalize_tool_name(
            tool_name
        )

        if not tool_name:
            return {
                "allowed": False,
                "message": "Tool name cannot be empty."
            }

        action = self._normalize_action(
            action
        )

        if not self.is_tool_allowed(
            tool_name
        ):
            return {
                "allowed": False,
                "tool": tool_name,
                "message": "Tool is not registered."
            }

        # Permission check.
        if not isinstance(
            permission_granted,
            bool
        ):
            return {
                "allowed": False,
                "tool": tool_name,
                "message": "Invalid permission status."
            }

        if not permission_granted:
            return {
                "allowed": False,
                "tool": tool_name,
                "requires_permission": True,
                "message": (
                    "Required permission is not granted."
                )
            }

        # Approval check.
        if not isinstance(
            approval_granted,
            bool
        ):
            return {
                "allowed": False,
                "tool": tool_name,
                "message": "Invalid approval status."
            }

        approval_required = self.requires_approval(
            tool_name,
            action
        )

        if approval_required and not approval_granted:
            return {
                "allowed": False,
                "tool": tool_name,
                "requires_approval": True,
                "message": (
                    "User approval is required."
                )
            }

        result = {
            "allowed": True,
            "tool": tool_name,
            "user_id": user_result["sanitized"],
            "requires_approval": approval_required,
            "message": "Tool execution allowed."
        }

        if action:
            result["action"] = action

        return result

    # =============================================================
    # REGISTER TOOL
    # =============================================================

    def register_tool(
        self,
        tool_name: str,
        restricted: bool = False
    ) -> dict:

        if not isinstance(
            tool_name,
            str
        ):
            return {
                "success": False,
                "message": "Tool name must be text."
            }

        tool_name = self._normalize_tool_name(
            tool_name
        )

        if not tool_name:
            return {
                "success": False,
                "message": "Tool name is required."
            }

        if not isinstance(
            restricted,
            bool
        ):
            return {
                "success": False,
                "message": "Restricted must be boolean."
            }

        self._allowed_tools.add(
            tool_name
        )

        if restricted:
            self._restricted_tools.add(
                tool_name
            )
        else:
            self._restricted_tools.discard(
                tool_name
            )

        return {
            "success": True,
            "tool": tool_name,
            "restricted": restricted,
            "message": "Tool registered successfully."
        }

    # =============================================================
    # REMOVE TOOL
    # =============================================================

    def remove_tool(
        self,
        tool_name: str
    ) -> dict:

        if not isinstance(
            tool_name,
            str
        ):
            return {
                "success": False,
                "message": "Tool name must be text."
            }

        tool_name = self._normalize_tool_name(
            tool_name
        )

        if not tool_name:
            return {
                "success": False,
                "message": "Tool name is required."
            }

        existed = (
            tool_name
            in self._allowed_tools
        )

        self._allowed_tools.discard(
            tool_name
        )

        self._restricted_tools.discard(
            tool_name
        )

        return {
            "success": True,
            "tool": tool_name,
            "removed": existed,
            "message": "Tool removed successfully."
        }

    # =============================================================
    # GET ALLOWED TOOLS
    # =============================================================

    def get_allowed_tools(
        self
    ) -> list:

        return sorted(
            self._allowed_tools
        )

    # =============================================================
    # GET RESTRICTED TOOLS
    # =============================================================

    def get_restricted_tools(
        self
    ) -> list:

        return sorted(
            self._restricted_tools
        )

    # =============================================================
    # GET RESTRICTED SHOPPING ACTIONS
    # =============================================================

    def get_restricted_shopping_actions(
        self
    ) -> list:

        return sorted(
            self._restricted_shopping_actions
        )

    # =============================================================
    # GET RESTRICTED BROWSER ACTIONS
    # =============================================================

    def get_restricted_browser_actions(
        self
    ) -> list:

        return sorted(
            self._restricted_browser_actions
        )

    # =============================================================
    # GET STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:

        return {
            "name": "tool_guard",
            "available": True,
            "enabled": True,
            "allowed_tools": self.get_allowed_tools(),
            "restricted_tools": self.get_restricted_tools(),
            "restricted_shopping_actions": (
                self.get_restricted_shopping_actions()
            ),
            "restricted_browser_actions": (
                self.get_restricted_browser_actions()
            ),
            "message": "Tool guard is operational."
        }