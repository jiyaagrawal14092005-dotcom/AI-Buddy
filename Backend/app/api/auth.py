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
# PASSWORD VERIFICATION
# ---------------------------------

def verify_password(
    password: str,
    stored_password_hash: str
) -> bool:

    try:

        salt, expected_hash = stored_password_hash.split("$", 1)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        ).hex()

        return secrets.compare_digest(
            actual_hash,
            expected_hash
        )

    except (ValueError, TypeError):

        return False


# ---------------------------------
# USER RESPONSE HELPER
# ---------------------------------

def user_response(user: User) -> dict:

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at
    }


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
            "user": user_response(new_user)
        }

    except Exception as error:

        db.rollback()

        return {
            "success": False,
            "message": "User registration failed.",
            "error": str(error)
        }


# ---------------------------------
# USER LOGIN
# ---------------------------------

@router.post("/login")
def login_user(
    credentials: dict,
    db: Session = Depends(get_db)
):

    email = str(
        credentials.get("email", "")
    ).strip().lower()

    password = str(
        credentials.get("password", "")
    )

    if not email or not password:

        return {
            "success": False,
            "message": "Email and password are required."
        }

    # ---------------------------------
    # FIND USER
    # ---------------------------------

    user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if user is None:

        return {
            "success": False,
            "message": "Invalid email or password."
        }

    # ---------------------------------
    # CHECK ACCOUNT STATUS
    # ---------------------------------

    if not user.is_active:

        return {
            "success": False,
            "message": "User account is inactive."
        }

    # ---------------------------------
    # VERIFY PASSWORD
    # ---------------------------------

    if not verify_password(
        password,
        user.password_hash
    ):

        return {
            "success": False,
            "message": "Invalid email or password."
        }

    # ---------------------------------
    # LOGIN SUCCESS
    # ---------------------------------

    return {
        "success": True,
        "message": "Login successful.",
        "user": user_response(user)
    }


# ---------------------------------
# UPDATE USER PROFILE
# ---------------------------------

@router.put("/profile")
def update_user_profile(
    profile_data: dict,
    db: Session = Depends(get_db)
):

    user_id = profile_data.get("user_id")
    username = str(
        profile_data.get("username", "")
    ).strip()

    # ---------------------------------
    # VALIDATE USER ID
    # ---------------------------------

    if user_id is None:

        return {
            "success": False,
            "message": "User ID is required."
        }

    try:

        user_id = int(user_id)

    except (TypeError, ValueError):

        return {
            "success": False,
            "message": "Invalid user ID."
        }

    # ---------------------------------
    # VALIDATE USERNAME
    # ---------------------------------

    if not username:

        return {
            "success": False,
            "message": "Name cannot be empty."
        }

    if len(username) > 100:

        return {
            "success": False,
            "message": "Name cannot exceed 100 characters."
        }

    # ---------------------------------
    # FIND USER
    # ---------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if user is None:

        return {
            "success": False,
            "message": "User not found."
        }

    # ---------------------------------
    # CHECK DUPLICATE USERNAME
    # ---------------------------------

    existing_username = (
        db.query(User)
        .filter(
            User.username == username,
            User.id != user_id
        )
        .first()
    )

    if existing_username is not None:

        return {
            "success": False,
            "message": "Username already exists."
        }

    # ---------------------------------
    # UPDATE USERNAME
    # ---------------------------------

    user.username = username

    try:

        db.commit()

        db.refresh(user)

        return {
            "success": True,
            "message": "Profile updated successfully.",
            "user": user_response(user)
        }

    except Exception as error:

        db.rollback()

        return {
            "success": False,
            "message": "Profile update failed.",
            "error": str(error)
        }


# ---------------------------------
# CURRENT USER
# ---------------------------------

@router.get("/me")
def get_current_user(
    email: str | None = None,
    db: Session = Depends(get_db)
):

    if not email:

        return {
            "success": False,
            "message": "No authenticated user."
        }

    user = (
        db.query(User)
        .filter(
            User.email == email.strip().lower()
        )
        .first()
    )

    if user is None:

        return {
            "success": False,
            "message": "User not found."
        }

    return {
        "success": True,
        "user": user_response(user)
    }


# ---------------------------------
# LOGOUT
# ---------------------------------

@router.post("/logout")
def logout_user():

    return {
        "success": True,
        "message": "Logout successful."
    }