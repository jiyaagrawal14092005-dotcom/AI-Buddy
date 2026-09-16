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

        self.user_permissions[username].add(permission)

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

        self.user_permissions[username].remove(permission)

        return {
            "success": True,
            "username": username,
            "permission": permission,
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
            "username": username,
            "message": "All permissions cleared."
        }

    def grant_calendar_permissions(
        self,
        username: str
    ) -> dict:

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        calendar_permissions = {
            "calendar.read",
            "calendar.create",
            "calendar.update",
            "calendar.delete"
        }

        if username not in self.user_permissions:
            self.user_permissions[username] = set()

        self.user_permissions[username].update(
            calendar_permissions
        )

        return {
            "success": True,
            "username": username,
            "permissions": sorted(calendar_permissions),
            "message": "Calendar permissions granted successfully."
        }

    def has_calendar_permission(
        self,
        username: str,
        action: str
    ) -> bool:

        if not username or not action:
            return False

        permission_map = {
            "create": "calendar.create",
            "list": "calendar.read",
            "get": "calendar.read",
            "delete": "calendar.delete",
            "update": "calendar.update",
            "calendars": "calendar.read"
        }

        permission = permission_map.get(action)

        if permission is None:
            return False

        return self.has_permission(
            username,
            permission
        )