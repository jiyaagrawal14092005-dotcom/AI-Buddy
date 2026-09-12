from datetime import datetime


class LongTermMemory:

    def __init__(self):

        self.memories = {}

    # ---------------------------------
    # SAVE MEMORY
    # ---------------------------------

    def save(
        self,
        key: str,
        value
    ) -> dict:

        if not isinstance(key, str):
            return {
                "success": False,
                "message": "Memory key must be text."
            }

        key = key.strip()

        if not key:
            return {
                "success": False,
                "message": "Memory key cannot be empty."
            }

        self.memories[key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }

        return {
            "success": True,
            "key": key,
            "value": value,
            "message": "Memory saved successfully."
        }

    # ---------------------------------
    # GET MEMORY
    # ---------------------------------

    def get(
        self,
        key: str
    ):

        if not isinstance(key, str):
            return {
                "success": False,
                "message": "Memory key must be text."
            }

        key = key.strip()

        if not key:
            return {
                "success": False,
                "message": "Memory key cannot be empty."
            }

        memory = self.memories.get(
            key
        )

        if memory is None:
            return {
                "success": False,
                "message": "Memory not found."
            }

        return {
            "success": True,
            "key": key,
            "value": memory["value"],
            "updated_at": memory["updated_at"]
        }

    # ---------------------------------
    # GET ALL MEMORIES
    # ---------------------------------

    def get_all(self) -> dict:

        return {
            key: value.copy()
            for key, value in self.memories.items()
        }

    # ---------------------------------
    # DELETE MEMORY
    # ---------------------------------

    def delete(
        self,
        key: str
    ) -> dict:

        if not isinstance(key, str):
            return {
                "success": False,
                "message": "Memory key must be text."
            }

        key = key.strip()

        if not key:
            return {
                "success": False,
                "message": "Memory key cannot be empty."
            }

        if key not in self.memories:
            return {
                "success": False,
                "message": "Memory not found."
            }

        del self.memories[key]

        return {
            "success": True,
            "key": key,
            "message": "Memory deleted successfully."
        }

    # ---------------------------------
    # CLEAR ALL MEMORIES
    # ---------------------------------

    def clear(self) -> dict:

        self.memories.clear()

        return {
            "success": True,
            "message": "Long-term memory cleared."
        }

    # ---------------------------------
    # MEMORY SIZE
    # ---------------------------------

    def size(self) -> int:

        return len(
            self.memories
        )

    # ---------------------------------
    # CHECK IF MEMORY EXISTS
    # ---------------------------------

    def exists(
        self,
        key: str
    ) -> bool:

        if not isinstance(key, str):
            return False

        key = key.strip()

        if not key:
            return False

        return key in self.memories