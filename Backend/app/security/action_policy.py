class ActionPolicy:

    def __init__(self):

        self._policies = {
            "task": {
                "risk": "low",
                "approval_required": False
            },
            "reminder": {
                "risk": "low",
                "approval_required": False
            },
            "timer": {
                "risk": "low",
                "approval_required": False
            },
            "weather": {
                "risk": "low",
                "approval_required": False
            },
            "search": {
                "risk": "low",
                "approval_required": False
            },
            "calendar": {
                "risk": "medium",
                "approval_required": True
            },
            "email": {
                "risk": "high",
                "approval_required": True
            },
            "file": {
                "risk": "medium",
                "approval_required": True
            },
            "browser": {
                "risk": "medium",
                "approval_required": True
            }
        }

    def get_policy(
        self,
        action: str
    ) -> dict:

        if not action:
            return {
                "success": False,
                "message": "Action is required."
            }

        action = action.lower()

        policy = self._policies.get(action)

        if not policy:
            return {
                "success": False,
                "message": "No policy found for this action."
            }

        return {
            "success": True,
            "action": action,
            "policy": policy
        }

    def is_allowed(
        self,
        action: str,
        permission_granted: bool = False,
        approval_granted: bool = False
    ) -> dict:

        policy_result = self.get_policy(action)

        if not policy_result["success"]:
            return {
                "allowed": False,
                "message": policy_result["message"]
            }

        policy = policy_result["policy"]

        if not permission_granted:
            return {
                "allowed": False,
                "message": "Required permission is not granted."
            }

        if (
            policy["approval_required"]
            and not approval_granted
        ):
            return {
                "allowed": False,
                "requires_approval": True,
                "risk": policy["risk"],
                "message": "User approval is required."
            }

        return {
            "allowed": True,
            "risk": policy["risk"],
            "message": "Action allowed by policy."
        }

    def add_policy(
        self,
        action: str,
        risk: str = "medium",
        approval_required: bool = True
    ) -> dict:

        if not action:
            return {
                "success": False,
                "message": "Action is required."
            }

        action = action.lower()

        self._policies[action] = {
            "risk": risk,
            "approval_required": approval_required
        }

        return {
            "success": True,
            "message": "Action policy added successfully."
        }

    def remove_policy(
        self,
        action: str
    ) -> dict:

        if not action:
            return {
                "success": False,
                "message": "Action is required."
            }

        action = action.lower()

        if action not in self._policies:
            return {
                "success": False,
                "message": "Action policy not found."
            }

        del self._policies[action]

        return {
            "success": True,
            "message": "Action policy removed successfully."
        }

    def get_all_policies(
        self
    ) -> dict:

        return {
            "success": True,
            "policies": self._policies.copy()
        }