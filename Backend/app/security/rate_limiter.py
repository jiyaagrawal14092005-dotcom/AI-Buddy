import time


class RateLimiter:

    def __init__(
        self,
        max_requests: int = 10,
        window_seconds: int = 60
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self._requests = {}

    def allow_request(
        self,
        user_id: str
    ) -> dict:

        if not user_id:
            return {
                "allowed": False,
                "message": "User ID is required."
            }

        current_time = time.time()

        if user_id not in self._requests:
            self._requests[user_id] = []

        request_times = self._requests[user_id]

        request_times[:] = [
            timestamp
            for timestamp in request_times
            if current_time - timestamp < self.window_seconds
        ]

        if len(request_times) >= self.max_requests:
            return {
                "allowed": False,
                "remaining": 0,
                "message": "Rate limit exceeded."
            }

        request_times.append(current_time)

        remaining = self.max_requests - len(request_times)

        return {
            "allowed": True,
            "remaining": remaining,
            "message": "Request allowed."
        }

    def get_remaining_requests(
        self,
        user_id: str
    ) -> int:

        if user_id not in self._requests:
            return self.max_requests

        current_time = time.time()

        request_times = self._requests[user_id]

        valid_requests = [
            timestamp
            for timestamp in request_times
            if current_time - timestamp < self.window_seconds
        ]

        self._requests[user_id] = valid_requests

        return max(
            0,
            self.max_requests - len(valid_requests)
        )

    def reset_user(
        self,
        user_id: str
    ) -> dict:

        if user_id in self._requests:
            del self._requests[user_id]

        return {
            "success": True,
            "message": "Rate limit reset successfully."
        }