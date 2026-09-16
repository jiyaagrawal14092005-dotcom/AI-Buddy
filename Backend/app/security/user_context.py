from copy import deepcopy


class UserContext:
    """
    Maintains the currently authenticated user context.

    This context is used by AI Buddy to ensure that actions,
    tools, memory, workflows and security checks are associated
    with the correct user.
    """

    def __init__(self):
        self.current_user = None

    # =============================================================
    # SET USER
    # =============================================================

    def set_user(
        self,
        user_id: str,
        username: str
    ) -> dict:

        if user_id is None:
            return {
                "success": False,
                "message": "User ID is required."
            }

        if not isinstance(
            user_id,
            str
        ):
            return {
                "success": False,
                "message": "User ID must be text."
            }

        user_id = user_id.strip()

        if not user_id:
            return {
                "success": False,
                "message": "User ID cannot be empty."
            }

        if username is None:
            return {
                "success": False,
                "message": "Username is required."
            }

        if not isinstance(
            username,
            str
        ):
            return {
                "success": False,
                "message": "Username must be text."
            }

        username = username.strip()

        if not username:
            return {
                "success": False,
                "message": "Username cannot be empty."
            }

        self.current_user = {
            "user_id": user_id,
            "username": username,
            "authenticated": True
        }

        return {
            "success": True,
            "user_id": user_id,
            "username": username,
            "authenticated": True,
            "message": (
                "User context set successfully."
            )
        }

    # =============================================================
    # GET USER
    # =============================================================

    def get_user(
        self
    ) -> dict:

        if not self.current_user:

            return {
                "success": False,
                "message": (
                    "No active user context."
                )
            }

        return {
            "success": True,
            "user": deepcopy(
                self.current_user
            )
        }

    # =============================================================
    # GET USER ID
    # =============================================================

    def get_user_id(
        self
    ) -> str | None:

        if not self.current_user:
            return None

        return self.current_user[
            "user_id"
        ]

    # =============================================================
    # GET USERNAME
    # =============================================================

    def get_username(
        self
    ) -> str | None:

        if not self.current_user:
            return None

        return self.current_user[
            "username"
        ]

    # =============================================================
    # AUTHENTICATION STATUS
    # =============================================================

    def is_authenticated(
        self
    ) -> bool:

        if not self.current_user:
            return False

        return bool(
            self.current_user.get(
                "authenticated",
                False
            )
        )

    # =============================================================
    # MATCH USER
    # =============================================================

    def matches_user(
        self,
        user_id: str
    ) -> bool:
        """
        Check whether the supplied user ID matches
        the active user context.
        """

        if not self.current_user:
            return False

        if not isinstance(
            user_id,
            str
        ):
            return False

        return (
            self.current_user["user_id"]
            == user_id.strip()
        )

    # =============================================================
    # UPDATE USERNAME
    # =============================================================

    def update_username(
        self,
        username: str
    ) -> dict:

        if not self.current_user:
            return {
                "success": False,
                "message": (
                    "No active user context."
                )
            }

        if not isinstance(
            username,
            str
        ):
            return {
                "success": False,
                "message": (
                    "Username must be text."
                )
            }

        username = username.strip()

        if not username:
            return {
                "success": False,
                "message": (
                    "Username cannot be empty."
                )
            }

        self.current_user[
            "username"
        ] = username

        return {
            "success": True,
            "user_id": self.current_user[
                "user_id"
            ],
            "username": username,
            "message": (
                "Username updated successfully."
            )
        }

    # =============================================================
    # CLEAR CONTEXT
    # =============================================================

    def clear(
        self
    ) -> dict:

        self.current_user = None

        return {
            "success": True,
            "message": (
                "User context cleared successfully."
            )
        }

    # =============================================================
    # STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:

        active = (
            self.current_user is not None
        )

        return {
            "name": "user_context",
            "available": True,
            "enabled": True,
            "active": active,
            "authenticated": (
                self.is_authenticated()
            ),
            "user_id": self.get_user_id(),
            "username": self.get_username(),
            "message": (
                "User context is operational."
            )
        }