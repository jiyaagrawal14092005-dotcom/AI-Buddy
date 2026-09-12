class ContextManager:

    def __init__(self, max_history: int = 10):

        if not isinstance(max_history, int):
            raise TypeError(
                "max_history must be an integer."
            )

        if max_history <= 0:
            raise ValueError(
                "max_history must be greater than 0."
            )

        self.max_history = max_history
        self.history = []

    # =================================
    # ADD CONVERSATION TO CONTEXT
    # =================================

    def add_message(
        self,
        user_message: str,
        assistant_response: str
    ):

        if not isinstance(user_message, str):
            raise TypeError(
                "user_message must be a string."
            )

        if not isinstance(assistant_response, str):
            raise TypeError(
                "assistant_response must be a string."
            )

        user_message = user_message.strip()
        assistant_response = assistant_response.strip()

        if not user_message:
            raise ValueError(
                "user_message cannot be empty."
            )

        if not assistant_response:
            raise ValueError(
                "assistant_response cannot be empty."
            )

        self.history.append({
            "user": user_message,
            "assistant": assistant_response
        })

        # Keep only recent conversations
        if len(self.history) > self.max_history:
            self.history.pop(0)

    # =================================
    # GET CONVERSATION HISTORY
    # =================================

    def get_history(self) -> list:

        return [
            message.copy()
            for message in self.history
        ]

    # =================================
    # GET LATEST CONVERSATION
    # =================================

    def get_latest(self):

        if not self.history:
            return None

        return self.history[-1].copy()

    # =================================
    # CLEAR CONTEXT
    # =================================

    def clear(self):

        self.history.clear()

    # =================================
    # NUMBER OF STORED CONVERSATIONS
    # =================================

    def size(self) -> int:

        return len(self.history)

    # =================================
    # CHECK WHETHER CONTEXT IS EMPTY
    # =================================

    def is_empty(self) -> bool:

        return len(self.history) == 0

    # =================================
    # GET RECENT CONVERSATIONS
    # =================================

    def get_recent(
        self,
        count: int = 5
    ) -> list:

        if not isinstance(count, int):
            raise TypeError(
                "count must be an integer."
            )

        if count <= 0:
            raise ValueError(
                "count must be greater than 0."
            )

        return [
            message.copy()
            for message in self.history[-count:]
        ]