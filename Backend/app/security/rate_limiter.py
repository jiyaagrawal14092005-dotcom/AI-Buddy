import time


class RateLimiter:

    def __init__(
        self,
        max_requests: int = 10,
        window_seconds: int = 60
    ):

        if not isinstance(
            max_requests,
            int
        ):
            raise TypeError(
                "Max requests must be an integer."
            )

        if max_requests <= 0:
            raise ValueError(
                "Max requests must be greater than zero."
            )

        if not isinstance(
            window_seconds,
            int
        ):
            raise TypeError(
                "Window seconds must be an integer."
            )

        if window_seconds <= 0:
            raise ValueError(
                "Window seconds must be greater than zero."
            )

        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self._requests = {}

        self.name = "rate_limiter"
        self.enabled = True

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def _validate_user_id(
        self,
        user_id: str
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

        if len(user_id) > 100:
            return {
                "success": False,
                "message": "User ID is too long."
            }

        return {
            "success": True,
            "user_id": user_id
        }

    # ---------------------------------------------------------
    # REMOVE EXPIRED REQUESTS
    # ---------------------------------------------------------

    def _cleanup_user_requests(
        self,
        user_id: str,
        current_time: float
    ) -> list:

        request_times = self._requests.get(
            user_id,
            []
        )

        valid_requests = [
            timestamp
            for timestamp in request_times
            if current_time - timestamp
            < self.window_seconds
        ]

        self._requests[user_id] = valid_requests

        return valid_requests

    # ---------------------------------------------------------
    # ALLOW REQUEST
    # ---------------------------------------------------------

    def allow_request(
        self,
        user_id: str
    ) -> dict:

        validation = self._validate_user_id(
            user_id
        )

        if not validation["success"]:
            return {
                "allowed": False,
                "remaining": 0,
                "message": validation["message"]
            }

        user_id = validation["user_id"]

        current_time = time.time()

        request_times = (
            self._cleanup_user_requests(
                user_id,
                current_time
            )
        )

        if len(request_times) >= self.max_requests:

            retry_after = (
                self.window_seconds
                - (
                    current_time
                    - request_times[0]
                )
            )

            return {
                "allowed": False,
                "remaining": 0,
                "retry_after_seconds": max(
                    0,
                    round(
                        retry_after,
                        2
                    )
                ),
                "message": "Rate limit exceeded."
            }

        request_times.append(
            current_time
        )

        remaining = (
            self.max_requests
            - len(request_times)
        )

        return {
            "allowed": True,
            "remaining": remaining,
            "limit": self.max_requests,
            "window_seconds": self.window_seconds,
            "message": "Request allowed."
        }

    # ---------------------------------------------------------
    # GET REMAINING REQUESTS
    # ---------------------------------------------------------

    def get_remaining_requests(
        self,
        user_id: str
    ) -> int:

        validation = self._validate_user_id(
            user_id
        )

        if not validation["success"]:
            return 0

        user_id = validation["user_id"]

        current_time = time.time()

        request_times = (
            self._cleanup_user_requests(
                user_id,
                current_time
            )
        )

        return max(
            0,
            self.max_requests
            - len(request_times)
        )

    # ---------------------------------------------------------
    # GET REQUEST COUNT
    # ---------------------------------------------------------

    def get_request_count(
        self,
        user_id: str
    ) -> int:

        validation = self._validate_user_id(
            user_id
        )

        if not validation["success"]:
            return 0

        user_id = validation["user_id"]

        current_time = time.time()

        request_times = (
            self._cleanup_user_requests(
                user_id,
                current_time
            )
        )

        return len(
            request_times
        )

    # ---------------------------------------------------------
    # GET RETRY AFTER
    # ---------------------------------------------------------

    def get_retry_after(
        self,
        user_id: str
    ) -> float:

        validation = self._validate_user_id(
            user_id
        )

        if not validation["success"]:
            return 0

        user_id = validation["user_id"]

        current_time = time.time()

        request_times = (
            self._cleanup_user_requests(
                user_id,
                current_time
            )
        )

        if len(request_times) < self.max_requests:
            return 0

        retry_after = (
            self.window_seconds
            - (
                current_time
                - request_times[0]
            )
        )

        return max(
            0,
            round(
                retry_after,
                2
            )
        )

    # ---------------------------------------------------------
    # RESET USER
    # ---------------------------------------------------------

    def reset_user(
        self,
        user_id: str
    ) -> dict:

        validation = self._validate_user_id(
            user_id
        )

        if not validation["success"]:
            return validation

        user_id = validation["user_id"]

        existed = (
            user_id in self._requests
        )

        if existed:
            del self._requests[user_id]

        return {
            "success": True,
            "reset": existed,
            "message": "Rate limit reset successfully."
        }

    # ---------------------------------------------------------
    # CLEANUP ALL USERS
    # ---------------------------------------------------------

    def cleanup_expired_requests(
        self
    ) -> dict:

        current_time = time.time()

        removed_users = 0
        removed_requests = 0

        for user_id in list(
            self._requests.keys()
        ):

            old_count = len(
                self._requests[user_id]
            )

            valid_requests = (
                self._cleanup_user_requests(
                    user_id,
                    current_time
                )
            )

            removed_requests += (
                old_count
                - len(valid_requests)
            )

            if not valid_requests:

                del self._requests[user_id]
                removed_users += 1

        return {
            "success": True,
            "removed_users": removed_users,
            "removed_requests": removed_requests,
            "message": "Expired rate-limit records cleaned successfully."
        }

    # ---------------------------------------------------------
    # CLEAR ALL
    # ---------------------------------------------------------

    def clear_all(
        self
    ) -> dict:

        count = len(
            self._requests
        )

        self._requests.clear()

        return {
            "success": True,
            "cleared_users": count,
            "message": "All rate-limit records cleared successfully."
        }

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def get_status(
        self
    ) -> dict:

        current_time = time.time()

        active_users = 0
        active_requests = 0

        for user_id in list(
            self._requests.keys()
        ):

            request_times = (
                self._cleanup_user_requests(
                    user_id,
                    current_time
                )
            )

            if request_times:
                active_users += 1
                active_requests += len(
                    request_times
                )

        return {
            "name": self.name,
            "available": True,
            "enabled": self.enabled,
            "max_requests": self.max_requests,
            "window_seconds": self.window_seconds,
            "active_users": active_users,
            "active_requests": active_requests,
            "message": "Rate limiter is operational."
        }