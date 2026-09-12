from sqlalchemy.orm import Session

from app.database.models import Conversation, Memory
from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory
from app.memory.storage import MemoryStorage


class MemoryManager:

    def __init__(self):

        self.short_term = ShortTermMemory()

        self.long_term = LongTermMemory()

        self.storage = MemoryStorage(
            "memory.json"
        )

    # ---------------------------------
    # ADD CONVERSATION
    # ---------------------------------

    def add_conversation(
        self,
        user_message: str,
        assistant_response: str,
        user_id: int,
        db: Session
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

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        if not user_message.strip():
            return {
                "success": False,
                "message": "User message cannot be empty."
            }

        if not assistant_response.strip():
            return {
                "success": False,
                "message": "Assistant response cannot be empty."
            }

        user_message = user_message.strip()
        assistant_response = assistant_response.strip()

        try:

            conversation = Conversation(
                user_id=user_id,
                user_message=user_message,
                assistant_response=assistant_response
            )

            db.add(conversation)
            db.commit()
            db.refresh(conversation)

            short_term_result = self.short_term.add(
                user_message,
                assistant_response
            )

            return {
                "success": True,
                "conversation": {
                    "id": conversation.id,
                    "user_id": conversation.user_id,
                    "user_message": conversation.user_message,
                    "assistant_response": conversation.assistant_response,
                    "created_at": conversation.created_at
                },
                "short_term": short_term_result,
                "message": (
                    "Conversation saved successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Conversation could not be saved."
                ),
                "error": str(error)
            }

    # ---------------------------------
    # SAVE LONG-TERM MEMORY
    # ---------------------------------

    def save_memory(
        self,
        key: str,
        value,
        user_id: int,
        db: Session
    ):

        if not isinstance(key, str):
            return {
                "success": False,
                "message": "Memory key must be text."
            }

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        if not key.strip():
            return {
                "success": False,
                "message": "Memory key cannot be empty."
            }

        key = key.strip()

        result = self.long_term.save(
            key,
            value
        )

        if not isinstance(result, dict):
            return {
                "success": False,
                "message": "Invalid memory storage result."
            }

        if not result.get("success"):
            return result

        try:

            existing_memory = (
                db.query(Memory)
                .filter(
                    Memory.user_id == user_id,
                    Memory.memory_key == key
                )
                .first()
            )

            memory_value = str(value)

            if existing_memory is not None:

                existing_memory.memory_value = memory_value

                db.commit()
                db.refresh(existing_memory)

                memory = existing_memory

            else:

                memory = Memory(
                    user_id=user_id,
                    memory_key=key,
                    memory_value=memory_value
                )

                db.add(memory)
                db.commit()
                db.refresh(memory)

            persist_result = self._persist_long_term()

            if not persist_result.get("success"):

                return {
                    "success": False,
                    "message": (
                        "Memory was saved to database "
                        "but could not be saved to JSON storage."
                    ),
                    "storage": persist_result
                }

            return {
                "success": True,
                "memory": {
                    "id": memory.id,
                    "user_id": memory.user_id,
                    "memory_key": memory.memory_key,
                    "memory_value": memory.memory_value,
                    "created_at": memory.created_at,
                    "updated_at": memory.updated_at
                },
                "message": "Memory saved successfully."
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Memory could not be saved to database."
                ),
                "error": str(error)
            }

    # ---------------------------------
    # GET MEMORY
    # ---------------------------------

    def get_memory(
        self,
        key: str,
        user_id: int,
        db: Session
    ):

        if not isinstance(key, str):
            return None

        if not isinstance(user_id, int):
            return None

        if user_id <= 0:
            return None

        key = key.strip()

        if not key:
            return None

        try:

            memory = (
                db.query(Memory)
                .filter(
                    Memory.user_id == user_id,
                    Memory.memory_key == key
                )
                .first()
            )

            if memory is not None:

                return {
                    "id": memory.id,
                    "user_id": memory.user_id,
                    "memory_key": memory.memory_key,
                    "memory_value": memory.memory_value,
                    "created_at": memory.created_at,
                    "updated_at": memory.updated_at
                }

        except Exception:
            pass

        return self.long_term.get(
            key
        )

    # ---------------------------------
    # GET ALL MEMORIES
    # ---------------------------------

    def get_all_memories(
        self,
        user_id: int,
        db: Session
    ):

        if not isinstance(user_id, int):
            return []

        if user_id <= 0:
            return []

        try:

            memories = (
                db.query(Memory)
                .filter(
                    Memory.user_id == user_id
                )
                .order_by(
                    Memory.created_at.desc()
                )
                .all()
            )

            return [
                {
                    "id": memory.id,
                    "user_id": memory.user_id,
                    "memory_key": memory.memory_key,
                    "memory_value": memory.memory_value,
                    "created_at": memory.created_at,
                    "updated_at": memory.updated_at
                }
                for memory in memories
            ]

        except Exception:

            return []

    # ---------------------------------
    # GET CONVERSATION HISTORY
    # ---------------------------------

    def get_conversation_history(
        self,
        user_id: int,
        db: Session
    ):

        if not isinstance(user_id, int):
            return []

        if user_id <= 0:
            return []

        try:

            conversations = (
                db.query(Conversation)
                .filter(
                    Conversation.user_id == user_id
                )
                .order_by(
                    Conversation.created_at.asc()
                )
                .all()
            )

            return [
                {
                    "id": conversation.id,
                    "user_id": conversation.user_id,
                    "user_message": conversation.user_message,
                    "assistant_response": conversation.assistant_response,
                    "created_at": conversation.created_at
                }
                for conversation in conversations
            ]

        except Exception:

            return []

    # ---------------------------------
    # PERSIST LONG-TERM MEMORY
    # ---------------------------------

    def _persist_long_term(self):

        result = self.storage.save(
            self.long_term.get_all()
        )

        if result is None:
            return {
                "success": False,
                "message": (
                    "Memory storage returned no result."
                )
            }

        if not isinstance(result, dict):
            return {
                "success": False,
                "message": "Invalid memory storage result."
            }

        return result

    # ---------------------------------
    # LOAD MEMORIES
    # ---------------------------------

    def load_memories(self):

        data = self.storage.load()

        if data is None:
            return {
                "success": True,
                "message": "No stored memories found.",
                "count": 0
            }

        if not isinstance(data, dict):
            return {
                "success": False,
                "message": "Stored memory data is invalid."
            }

        if not data:
            return {
                "success": True,
                "message": "No stored memories found.",
                "count": 0
            }

        loaded_count = 0

        for key, value in data.items():

            if not isinstance(key, str):
                continue

            if isinstance(value, dict):

                actual_value = value.get(
                    "value",
                    value
                )

            else:

                actual_value = value

            result = self.long_term.save(
                key,
                actual_value
            )

            if (
                isinstance(result, dict)
                and result.get("success")
            ):
                loaded_count += 1

        return {
            "success": True,
            "message": "Memories loaded successfully.",
            "count": loaded_count
        }

    # ---------------------------------
    # DELETE MEMORY
    # ---------------------------------

    def delete_memory(
        self,
        key: str,
        user_id: int,
        db: Session
    ):

        if not isinstance(key, str):
            return {
                "success": False,
                "message": "Memory key must be text."
            }

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        key = key.strip()

        if not key:
            return {
                "success": False,
                "message": "Memory key cannot be empty."
            }

        try:

            memory = (
                db.query(Memory)
                .filter(
                    Memory.user_id == user_id,
                    Memory.memory_key == key
                )
                .first()
            )

            if memory is None:

                return {
                    "success": False,
                    "message": "Memory not found."
                }

            db.delete(memory)
            db.commit()

            result = self.long_term.delete(
                key
            )

            if (
                isinstance(result, dict)
                and result.get("success")
            ):

                persist_result = self._persist_long_term()

                if not persist_result.get("success"):

                    return {
                        "success": False,
                        "message": (
                            "Memory was deleted from "
                            "database but JSON storage "
                            "could not be updated."
                        ),
                        "storage": persist_result
                    }

            return {
                "success": True,
                "message": "Memory deleted successfully."
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Memory could not be deleted."
                ),
                "error": str(error)
            }

    # ---------------------------------
    # CLEAR ALL MEMORIES
    # ---------------------------------

    def clear_all(
        self,
        user_id: int,
        db: Session
    ):

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        try:

            memories = (
                db.query(Memory)
                .filter(
                    Memory.user_id == user_id
                )
                .all()
            )

            conversations = (
                db.query(Conversation)
                .filter(
                    Conversation.user_id == user_id
                )
                .all()
            )

            for memory in memories:
                db.delete(memory)

            for conversation in conversations:
                db.delete(conversation)

            db.commit()

            self.short_term.clear()

            self.long_term.clear()

            storage_result = self.storage.delete()

            if storage_result is None:

                return {
                    "success": False,
                    "message": (
                        "Database memories were cleared, "
                        "but JSON storage deletion failed."
                    )
                }

            if isinstance(storage_result, dict):

                if not storage_result.get(
                    "success",
                    True
                ):

                    return {
                        "success": False,
                        "message": (
                            "Database memories were cleared, "
                            "but JSON storage deletion failed."
                        ),
                        "storage": storage_result
                    }

            return {
                "success": True,
                "deleted_memories": len(memories),
                "deleted_conversations": len(conversations),
                "message": (
                    "All memories and conversations "
                    "cleared successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Memory data could not be cleared."
                ),
                "error": str(error)
            }