class AuthorizationManager:

    def __init__(self):

        self.roles = {
            "admin": {
                "chat",
                "task",
                "reminder",
                "timer",
                "weather",
                "email",
                "calendar",
                "file",
                "notification",
                "browser",
                "settings"
            },
            "user": {
                "chat",
                "task",
                "reminder",
                "timer",
                "weather",
                "email",
                "calendar",
                "file",
                "notification",
                "browser"
            },
            "guest": {
                "chat",
                "weather"
            }
        }

        self.user_roles = {}

    def assign_role(
        self,
        username: str,
        role: str
    ) -> dict:

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        if role not in self.roles:
            return {
                "success": False,
                "message": "Invalid role."
            }

        self.user_roles[username] = role

        return {
            "success": True,
            "username": username,
            "role": role,
            "message": "Role assigned successfully."
        }

    def get_role(
        self,
        username: str
    ) -> str:

        return self.user_roles.get(
            username,
            "guest"
        )

    def is_allowed(
        self,
        username: str,
        action: str
    ) -> bool:

        role = self.get_role(username)

        allowed_actions = self.roles.get(
            role,
            set()
        )

        return action in allowed_actions

    def check_permission(
        self,
        username: str,
        action: str
    ) -> dict:

        role = self.get_role(username)

        allowed = self.is_allowed(
            username,
            action
        )

        return {
            "success": True,
            "username": username,
            "role": role,
            "action": action,
            "allowed": allowed,
            "message": (
                "Action is authorized."
                if allowed
                else "Action is not authorized."
            )
        }

    def remove_user(
        self,
        username: str
    ) -> dict:

        if username not in self.user_roles:
            return {
                "success": False,
                "message": "User role not found."
            }

        del self.user_roles[username]

        return {
            "success": True,
            "message": "User role removed successfully."
        }