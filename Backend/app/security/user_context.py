class UserContext:

    def __init__(self):

        self.current_user = None

    def set_user(
        self,
        user_id: str,
        username: str
    ) -> dict:

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required."
            }

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        self.current_user = {
            "user_id": user_id,
            "username": username
        }

        return {
            "success": True,
            "user_id": user_id,
            "username": username,
            "message": "User context set successfully."
        }

    def get_user(self) -> dict:

        if not self.current_user:

            return {
                "success": False,
                "message": "No active user context."
            }

        return {
            "success": True,
            "user": self.current_user.copy()
        }

    def get_user_id(self):

        if not self.current_user:
            return None

        return self.current_user["user_id"]

    def get_username(self):

        if not self.current_user:
            return None

        return self.current_user["username"]

    def is_authenticated(self) -> bool:

        return self.current_user is not None

    def clear(self) -> dict:

        self.current_user = None

        return {
            "success": True,
            "message": "User context cleared successfully."
        }