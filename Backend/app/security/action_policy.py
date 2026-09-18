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

            # =========================================
            # BASIC TASK ACTIONS
            # =========================================

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

            "time_tool": {
                "risk": "low",
                "approval_required": False
            },
            
            "search": {
                "risk": "low",
                "approval_required": False
            },

            # =========================================
            # APPLICATION LAUNCHER
            # =========================================

            "application_launcher": {
                "risk": "low",
                "approval_required": False
            },

            "application_launcher.open_application": {
                "risk": "low",
                "approval_required": False
            },

            "application_launcher.open_website": {
                "risk": "low",
                "approval_required": False
            },

            # =========================================
            # CALENDAR
            # =========================================

            "calendar": {
                "risk": "medium",
                "approval_required": True
            },

            # =========================================
            # FILE
            # =========================================

            "file": {
                "risk": "medium",
                "approval_required": True
            },

            # =========================================
            # EMAIL
            # =========================================

            "email": {
                "risk": "high",
                "approval_required": True
            },

            # =========================================
            # BROWSER
            # =========================================

            "browser": {
                "risk": "medium",
                "approval_required": True
            },

            "browser.open": {
                "risk": "low",
                "approval_required": False
            },

            "browser.navigate": {
                "risk": "low",
                "approval_required": False
            },

            "browser.read": {
                "risk": "low",
                "approval_required": False
            },

            "browser.close": {
                "risk": "low",
                "approval_required": False
            },

            "browser.click": {
                "risk": "medium",
                "approval_required": True
            },

            "browser.fill": {
                "risk": "medium",
                "approval_required": True
            },

            # =========================================
            # SHOPPING
            # =========================================

            "shopping": {
                "risk": "low",
                "approval_required": False
            },

            "shopping.search": {
                "risk": "low",
                "approval_required": False
            },

            "shopping.compare": {
                "risk": "low",
                "approval_required": False
            },

            "shopping.cart_add": {
                "risk": "medium",
                "approval_required": False
            },

            "shopping.cart_list": {
                "risk": "low",
                "approval_required": False
            },

            "shopping.cart_remove": {
                "risk": "medium",
                "approval_required": False
            },

            "shopping.purchase": {
                "risk": "high",
                "approval_required": True
            },

            "shopping.buy": {
                "risk": "high",
                "approval_required": True
            },
        }

    # =========================================
    # ACTION NORMALIZATION
    # =========================================

    def _normalize_action(
        self,
        action: str
    ) -> str:

        if not isinstance(action, str):
            return ""

        return action.strip().lower()

    # =========================================
    # GET POLICY
    # =========================================

    def get_policy(
        self,
        action: str
    ) -> dict | None:

        normalized_action = self._normalize_action(
            action
        )

        return self._policies.get(
            normalized_action
        )

    # =========================================
    # CHECK WHETHER ACTION IS ALLOWED
    # =========================================

    def is_allowed(
        self,
        action: str,
        permission_granted: bool = True,
        approval_granted: bool = False
    ) -> dict:

        normalized_action = self._normalize_action(
            action
        )

        # -----------------------------------------
        # UNKNOWN ACTION
        # -----------------------------------------

        if normalized_action not in self._policies:

            return {
                "allowed": False,
                "action": normalized_action,
                "message": (
                    f"Unknown action '{normalized_action}'. "
                    "Action denied by default."
                )
            }

        policy = self._policies[
            normalized_action
        ]

        # -----------------------------------------
        # PERMISSION CHECK
        # -----------------------------------------

        if not permission_granted:

            return {
                "allowed": False,
                "action": normalized_action,
                "risk": policy.get("risk"),
                "approval_required": policy.get(
                    "approval_required",
                    False
                ),
                "message": (
                    f"Permission not granted for "
                    f"action '{normalized_action}'."
                )
            }

        # -----------------------------------------
        # APPROVAL CHECK
        # -----------------------------------------

        approval_required = policy.get(
            "approval_required",
            False
        )

        if approval_required and not approval_granted:

            return {
                "allowed": False,
                "action": normalized_action,
                "risk": policy.get("risk"),
                "approval_required": True,
                "message": (
                    f"Explicit approval is required "
                    f"for action '{normalized_action}'."
                )
            }

        # -----------------------------------------
        # ACTION ALLOWED
        # -----------------------------------------

        return {
            "allowed": True,
            "action": normalized_action,
            "risk": policy.get("risk"),
            "approval_required": approval_required,
            "message": (
                f"Action '{normalized_action}' is allowed."
            )
        }

    # =========================================
    # ADD POLICY
    # =========================================

    def add_policy(
        self,
        action: str,
        risk: str,
        approval_required: bool
    ) -> dict:

        normalized_action = self._normalize_action(
            action
        )

        normalized_risk = (
            risk.strip().lower()
            if isinstance(risk, str)
            else ""
        )

        if not normalized_action:

            return {
                "success": False,
                "message": "Action cannot be empty."
            }

        if normalized_risk not in self.VALID_RISK_LEVELS:

            return {
                "success": False,
                "message": "Invalid risk level."
            }

        self._policies[normalized_action] = {
            "risk": normalized_risk,
            "approval_required": bool(
                approval_required
            )
        }

        return {
            "success": True,
            "action": normalized_action,
            "policy": self._policies[
                normalized_action
            ],
            "message": (
                "Action policy added successfully."
            )
        }

    # =========================================
    # REMOVE POLICY
    # =========================================

    def remove_policy(
        self,
        action: str
    ) -> dict:

        normalized_action = self._normalize_action(
            action
        )

        if normalized_action not in self._policies:

            return {
                "success": False,
                "message": "Action policy not found."
            }

        removed_policy = self._policies.pop(
            normalized_action
        )

        return {
            "success": True,
            "action": normalized_action,
            "policy": removed_policy,
            "message": (
                "Action policy removed successfully."
            )
        }

    # =========================================
    # CHECK POLICY EXISTENCE
    # =========================================

    def has_policy(
        self,
        action: str
    ) -> bool:

        normalized_action = self._normalize_action(
            action
        )

        return normalized_action in self._policies

    # =========================================
    # GET ALL POLICIES
    # =========================================

    def get_all(
        self
    ) -> dict:

        return dict(
            self._policies
        )

    # =========================================
    # GET POLICIES BY RISK
    # =========================================

    def get_by_risk(
        self,
        risk: str
    ) -> dict:

        normalized_risk = (
            risk.strip().lower()
            if isinstance(risk, str)
            else ""
        )

        return {
            action: policy
            for action, policy
            in self._policies.items()
            if policy.get("risk") == normalized_risk
        }

    # =========================================
    # GET APPROVAL-REQUIRED POLICIES
    # =========================================

    def get_approval_required(
        self
    ) -> dict:

        return {
            action: policy
            for action, policy
            in self._policies.items()
            if policy.get(
                "approval_required"
            ) is True
        }

    # =========================================
    # STATUS
    # =========================================

    def get_status(
        self
    ) -> dict:

        policies = self._policies

        approval_required_count = sum(
            1
            for policy in policies.values()
            if policy.get(
                "approval_required"
            ) is True
        )

        risk_counts = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0
        }

        for policy in policies.values():

            risk = policy.get("risk")

            if risk in risk_counts:
                risk_counts[risk] += 1

        return {
            "success": True,
            "service": "action_policy",
            "status": "ready",
            "policy_count": len(policies),
            "approval_required_count": (
                approval_required_count
            ),
            "risk_counts": risk_counts,
            "message": (
                "Action policy system is ready."
            )
        }