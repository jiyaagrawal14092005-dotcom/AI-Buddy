class PermissionManager:

    def __init__(self):

        self.user_permissions = {}

    def grant_permission(
        self,
        username: str,
        permission: str
    ) -> dict:

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        if not permission:
            return {
                "success": False,
                "message": "Permission is required."
            }

        if username not in self.user_permissions:
            self.user_permissions[username] = set()

        self.user_permissions[username].add(
            permission
        )

        return {
            "success": True,
            "username": username,
            "permission": permission,
            "message": "Permission granted successfully."
        }

    def revoke_permission(
        self,
        username: str,
        permission: str
    ) -> dict:

        if username not in self.user_permissions:
            return {
                "success": False,
                "message": "User not found."
            }

        if permission not in self.user_permissions[username]:
            return {
                "success": False,
                "message": "Permission not found."
            }

        self.user_permissions[username].remove(
            permission
        )

        return {
            "success": True,
            "message": "Permission revoked successfully."
        }

    def has_permission(
        self,
        username: str,
        permission: str
    ) -> bool:

        return permission in self.user_permissions.get(
            username,
            set()
        )

    def get_permissions(
        self,
        username: str
    ) -> list:

        return list(
            self.user_permissions.get(
                username,
                set()
            )
        )

    def clear_permissions(
        self,
        username: str
    ) -> dict:

        if username not in self.user_permissions:
            return {
                "success": False,
                "message": "User not found."
            }

        self.user_permissions[username].clear()

        return {
            "success": True,
            "message": "All permissions cleared."
        }