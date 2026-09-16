class ActionPolicy:
    """
    Defines security policies for AI Buddy actions.

    Each action has:
    - risk level
    - whether explicit approval is required

    Unknown actions are denied by default.
    """

    VALID_RISK_LEVELS = {
        "low",
        "medium",
        "high",
        "critical",
    }

    def __init__(self):

        self._policies = {

            # =====================================================
            # LOW-RISK ACTIONS
            # =====================================================

            "task": {
                "risk": "low",
                "approval_required": False,
            },

            "reminder": {
                "risk": "low",
                "approval_required": False,
            },

            "timer": {
                "risk": "low",
                "approval_required": False,
            },

            "weather": {
                "risk": "low",
                "approval_required": False,
            },

            "search": {
                "risk": "low",
                "approval_required": False,
            },

            # =====================================================
            # MEDIUM-RISK ACTIONS
            # =====================================================

            "calendar": {
                "risk": "medium",
                "approval_required": True,
            },

            "file": {
                "risk": "medium",
                "approval_required": True,
            },

            # =====================================================
            # HIGH-RISK ACTIONS
            # =====================================================

            "email": {
                "risk": "high",
                "approval_required": True,
            },

            # =====================================================
            # BROWSER BASE POLICY
            # =====================================================

            "browser": {
                "risk": "medium",
                "approval_required": True,
            },

            # =====================================================
            # BROWSER SAFE ACTIONS
            # =====================================================

            "browser.open": {
                "risk": "low",
                "approval_required": False,
            },

            "browser.navigate": {
                "risk": "low",
                "approval_required": False,
            },

            "browser.read": {
                "risk": "low",
                "approval_required": False,
            },

            "browser.close": {
                "risk": "low",
                "approval_required": False,
            },

            # =====================================================
            # BROWSER INTERACTIVE ACTIONS
            # =====================================================

            "browser.click": {
                "risk": "medium",
                "approval_required": True,
            },

            "browser.fill": {
                "risk": "medium",
                "approval_required": True,
            },
        }

    # =============================================================
    # NORMALIZE ACTION
    # =============================================================

    def _normalize_action(
        self,
        action: str
    ) -> str:

        if not isinstance(action, str):
            return ""

        return action.strip().lower()

    # =============================================================
    # VALIDATE RISK
    # =============================================================

    def _validate_risk(
        self,
        risk: str
    ) -> bool:

        if not isinstance(risk, str):
            return False

        return (
            risk.strip().lower()
            in self.VALID_RISK_LEVELS
        )

    # =============================================================
    # GET POLICY
    # =============================================================

    def get_policy(
        self,
        action: str
    ) -> dict:

        action = self._normalize_action(
            action
        )

        if not action:

            return {
                "success": False,
                "message": "Action is required.",
            }

        policy = self._policies.get(
            action
        )

        if policy is None:

            return {
                "success": False,
                "action": action,
                "message": (
                    "No policy found for this action."
                ),
            }

        return {
            "success": True,
            "action": action,
            "policy": policy.copy(),
        }

    # =============================================================
    # CHECK ACTION
    # =============================================================

    def is_allowed(
        self,
        action: str,
        permission_granted: bool = False,
        approval_granted: bool = False
    ) -> dict:
        """
        Check whether an action can be executed.

        Security order:
        1. Action must have a registered policy.
        2. Permission must be granted.
        3. Approval must be granted when required.
        """

        action = self._normalize_action(
            action
        )

        if not action:

            return {
                "allowed": False,
                "message": "Action is required.",
            }

        policy_result = self.get_policy(
            action
        )

        if not policy_result["success"]:

            return {
                "allowed": False,
                "action": action,
                "message": (
                    policy_result["message"]
                ),
            }

        policy = policy_result["policy"]

        if not isinstance(
            permission_granted,
            bool
        ):

            return {
                "allowed": False,
                "action": action,
                "message": (
                    "Invalid permission status."
                ),
            }

        if not permission_granted:

            return {
                "allowed": False,
                "action": action,
                "requires_permission": True,
                "risk": policy["risk"],
                "message": (
                    "Required permission is not granted."
                ),
            }

        if not isinstance(
            approval_granted,
            bool
        ):

            return {
                "allowed": False,
                "action": action,
                "message": (
                    "Invalid approval status."
                ),
            }

        approval_required = (
            policy["approval_required"]
        )

        if (
            approval_required
            and not approval_granted
        ):

            return {
                "allowed": False,
                "action": action,
                "requires_approval": True,
                "risk": policy["risk"],
                "message": (
                    "User approval is required."
                ),
            }

        return {
            "allowed": True,
            "action": action,
            "risk": policy["risk"],
            "requires_approval": approval_required,
            "message": (
                "Action allowed by policy."
            ),
        }

    # =============================================================
    # ADD POLICY
    # =============================================================

    def add_policy(
        self,
        action: str,
        risk: str = "medium",
        approval_required: bool = True
    ) -> dict:
        """
        Add or update an action policy.
        """

        action = self._normalize_action(
            action
        )

        if not action:

            return {
                "success": False,
                "message": "Action is required.",
            }

        if not self._validate_risk(
            risk
        ):

            return {
                "success": False,
                "message": (
                    "Invalid risk level."
                ),
                "allowed_risk_levels": sorted(
                    self.VALID_RISK_LEVELS
                ),
            }

        if not isinstance(
            approval_required,
            bool
        ):

            return {
                "success": False,
                "message": (
                    "approval_required must be boolean."
                ),
            }

        self._policies[action] = {
            "risk": risk.strip().lower(),
            "approval_required": approval_required,
        }

        return {
            "success": True,
            "action": action,
            "policy": self._policies[action].copy(),
            "message": (
                "Action policy added successfully."
            ),
        }

    # =============================================================
    # REMOVE POLICY
    # =============================================================

    def remove_policy(
        self,
        action: str
    ) -> dict:

        action = self._normalize_action(
            action
        )

        if not action:

            return {
                "success": False,
                "message": "Action is required.",
            }

        if action not in self._policies:

            return {
                "success": False,
                "action": action,
                "message": (
                    "Action policy not found."
                ),
            }

        del self._policies[action]

        return {
            "success": True,
            "action": action,
            "message": (
                "Action policy removed successfully."
            ),
        }

    # =============================================================
    # CHECK POLICY EXISTS
    # =============================================================

    def has_policy(
        self,
        action: str
    ) -> bool:

        action = self._normalize_action(
            action
        )

        if not action:
            return False

        return action in self._policies

    # =============================================================
    # GET ALL POLICIES
    # =============================================================

    def get_all_policies(
        self
    ) -> dict:

        policies = {
            action: policy.copy()
            for action, policy
            in self._policies.items()
        }

        return {
            "success": True,
            "policies": policies,
            "count": len(policies),
        }

    # =============================================================
    # GET ACTIONS BY RISK
    # =============================================================

    def get_actions_by_risk(
        self,
        risk: str
    ) -> dict:

        if not self._validate_risk(
            risk
        ):

            return {
                "success": False,
                "message": (
                    "Invalid risk level."
                ),
            }

        risk = risk.strip().lower()

        actions = sorted(
            action
            for action, policy
            in self._policies.items()
            if policy["risk"] == risk
        )

        return {
            "success": True,
            "risk": risk,
            "actions": actions,
            "count": len(actions),
        }

    # =============================================================
    # GET APPROVAL-REQUIRED ACTIONS
    # =============================================================

    def get_approval_required_actions(
        self
    ) -> list:

        return sorted(
            action
            for action, policy
            in self._policies.items()
            if policy["approval_required"]
        )

    # =============================================================
    # GET STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:

        return {
            "name": "action_policy",
            "available": True,
            "enabled": True,
            "policy_count": len(
                self._policies
            ),
            "approval_required_count": len(
                self.get_approval_required_actions()
            ),
            "risk_levels": sorted(
                self.VALID_RISK_LEVELS
            ),
            "message": (
                "Action policy is operational."
            ),
        }