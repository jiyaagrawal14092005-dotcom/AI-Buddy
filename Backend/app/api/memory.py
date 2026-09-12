from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.memory.manager import MemoryManager


router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)


memory_manager = MemoryManager()


@router.get("/status")
def memory_status():

    return {
        "success": True,
        "service": "memory",
        "status": "ready",
        "database": "connected"
    }


@router.get("/history")
def get_memory_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    return {
        "success": True,
        "history": memory_manager.get_conversation_history(
            user_id,
            db
        )
    }


@router.post("/remember")
def remember(
    user_id: int,
    user_message: str,
    assistant_response: str,
    db: Session = Depends(get_db)
):

    return memory_manager.add_conversation(
        user_message,
        assistant_response,
        user_id,
        db
    )


@router.post("/save")
def save_memory(
    user_id: int,
    key: str,
    value: str,
    db: Session = Depends(get_db)
):

    return memory_manager.save_memory(
        key,
        value,
        user_id,
        db
    )


@router.get("/all")
def get_all_memories(
    user_id: int,
    db: Session = Depends(get_db)
):

    return {
        "success": True,
        "memories": memory_manager.get_all_memories(
            user_id,
            db
        )
    }


@router.delete("/clear")
def clear_memory(
    user_id: int,
    db: Session = Depends(get_db)
):

    return memory_manager.clear_all(
        user_id,
        db
    )


@router.get("/{key}")
def get_memory(
    key: str,
    user_id: int,
    db: Session = Depends(get_db)
):

    memory = memory_manager.get_memory(
        key,
        user_id,
        db
    )

    if memory is None:

        return {
            "success": False,
            "message": "Memory not found."
        }

    return {
        "success": True,
        "memory": memory
    }


@router.delete("/{key}")
def delete_memory(
    key: str,
    user_id: int,
    db: Session = Depends(get_db)
):

    return memory_manager.delete_memory(
        key,
        user_id,
        db
    )