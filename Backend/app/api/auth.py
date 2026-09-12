import hashlib
import secrets

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.database.schemas import UserCreate


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ---------------------------------
# PASSWORD HASHING
# ---------------------------------

def hash_password(password: str) -> str:

    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return f"{salt}${password_hash}"


# ---------------------------------
# AUTHENTICATION STATUS
# ---------------------------------

@router.get("/status")
def authentication_status():

    return {
        "success": True,
        "service": "authentication",
        "status": "ready",
        "message": "Authentication API is ready."
    }


# ---------------------------------
# USER REGISTRATION
# ---------------------------------

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    username = user.username.strip()
    email = user.email.strip().lower()

    if not username:
        return {
            "success": False,
            "message": "Username cannot be empty."
        }

    if not email:
        return {
            "success": False,
            "message": "Email cannot be empty."
        }

    if not user.password:
        return {
            "success": False,
            "message": "Password cannot be empty."
        }

    # ---------------------------------
    # CHECK EXISTING USERNAME
    # ---------------------------------

    existing_username = (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )

    if existing_username is not None:

        return {
            "success": False,
            "message": "Username already exists."
        }

    # ---------------------------------
    # CHECK EXISTING EMAIL
    # ---------------------------------

    existing_email = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if existing_email is not None:

        return {
            "success": False,
            "message": "Email already exists."
        }

    # ---------------------------------
    # CREATE USER
    # ---------------------------------

    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(
            user.password
        ),
        is_active=True
    )

    try:

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return {
            "success": True,
            "message": "User registered successfully.",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "is_active": new_user.is_active,
                "created_at": new_user.created_at
            }
        }

    except Exception as error:

        db.rollback()

        return {
            "success": False,
            "message": "User registration failed.",
            "error": str(error)
        }