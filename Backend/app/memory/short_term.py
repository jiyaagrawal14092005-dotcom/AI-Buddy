from datetime import datetime


class ShortTermMemory:

    def __init__(
        self,
        max_items: int = 10
    ):

        if not isinstance(max_items, int):
            raise TypeError(
                "Maximum memory items must be an integer."
            )

        if max_items <= 0:
            raise ValueError(
                "Maximum memory items must be greater than 0."
            )

        self.max_items = max_items

        self.memories = []

    # ---------------------------------
    # ADD CONVERSATION
    # ---------------------------------

    def add(
        self,
        user_message: str,
        assistant_response: str
    ):

        if not isinstance(user_message, str):
            return {
                "success": False,
                "message": "User message must be text."
            }

        if not isinstance(assistant_response, str):
            return {
                "success": False,
                "message": "Assistant response must be text."
            }

        user_message = user_message.strip()
        assistant_response = assistant_response.strip()

        if not user_message:
            return {
                "success": False,
                "message": "User message cannot be empty."
            }

        if not assistant_response:
            return {
                "success": False,
                "message": "Assistant response cannot be empty."
            }

        memory = {
            "user_message": user_message,
            "assistant_response": assistant_response,
            "timestamp": datetime.now().isoformat()
        }

        self.memories.append(memory)

        if len(self.memories) > self.max_items:
            self.memories.pop(0)

        return {
            "success": True,
            "memory": memory,
            "message": "Conversation added to short-term memory."
        }

    # ---------------------------------
    # GET ALL MEMORIES
    # ---------------------------------

    def get_all(self) -> list:

        return self.memories.copy()

    # ---------------------------------
    # GET LATEST MEMORY
    # ---------------------------------

    def get_latest(self):

        if not self.memories:
            return None

        return self.memories[-1]

    # ---------------------------------
    # CLEAR MEMORY
    # ---------------------------------

    def clear(self):

        self.memories.clear()

        return {
            "success": True,
            "message": "Short-term memory cleared."
        }

    # ---------------------------------
    # MEMORY SIZE
    # ---------------------------------

    def size(self) -> int:

        return len(self.memories)

    # ---------------------------------
    # CHECK IF MEMORY IS EMPTY
    # ---------------------------------

    def is_empty(self) -> bool:

        return len(self.memories) == 0