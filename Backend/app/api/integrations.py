from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User

from app.integrations.email.provider import EmailProvider
from app.integrations.email.gmail_oauth import GmailOAuth

from app.integrations.calendar.provider import CalendarProvider
from app.integrations.calendar.oauth import (
    create_authorization_url as create_calendar_authorization_url,
    validate_state as validate_calendar_state,
    exchange_code_for_token as exchange_calendar_code,
    get_configuration_status as get_calendar_oauth_status
)

from app.integrations.cloud_storage.provider import CloudStorageProvider
from app.integrations.education.provider import EducationProvider
from app.integrations.booking.provider import BookingProvider
from app.integrations.shopping.provider import ShoppingProvider
from app.integrations.social.provider import SocialProvider

from app.security.oauth_manager import OAuthManager
from app.security.token_manager import TokenManager


router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"]
)


# ---------------------------------------------------------
# PROVIDERS
# ---------------------------------------------------------

providers = {
    "email": EmailProvider(),
    "calendar": CalendarProvider(),
    "cloud_storage": CloudStorageProvider(),
    "education": EducationProvider(),
    "booking": BookingProvider(),
    "shopping": ShoppingProvider(),
    "social": SocialProvider()
}


# ---------------------------------------------------------
# SECURITY / OAUTH MANAGERS
# ---------------------------------------------------------

oauth_manager = OAuthManager()
token_manager = TokenManager()
gmail_oauth = GmailOAuth()


# ---------------------------------------------------------
# INTEGRATION STATUS
# ---------------------------------------------------------

@router.get("/status")
def integration_status():

    return {
        "success": True,
        "service": "integrations",
        "status": "ready",
        "providers": {
            name: provider.get_status()
            for name, provider in providers.items()
        },
        "oauth": oauth_manager.get_status(),
        "tokens": token_manager.get_status(),
        "gmail_oauth": gmail_oauth.get_status(),
        "calendar_oauth": get_calendar_oauth_status()
    }


# ---------------------------------------------------------
# GET ALL INTEGRATIONS
# ---------------------------------------------------------

@router.get("/")
def get_integrations():

    return {
        "success": True,
        "integrations": [
            provider.get_status()
            for provider in providers.values()
        ]
    }


# ---------------------------------------------------------
# GET SPECIFIC INTEGRATION
# ---------------------------------------------------------

@router.get("/{provider_name}")
def get_integration(provider_name: str):

    provider = providers.get(provider_name)

    if provider is None:
        return {
            "success": False,
            "message": (
                f"Integration '{provider_name}' "
                "was not found."
            )
        }

    return {
        "success": True,
        "integration": provider.get_status()
    }


# ---------------------------------------------------------
# GMAIL AUTHORIZE
# ---------------------------------------------------------

@router.get("/gmail/authorize")
def gmail_authorize(
    user_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # VALIDATE USER ID
    # -----------------------------------------------------

    if user_id <= 0:
        return {
            "success": False,
            "provider": "gmail",
            "message": (
                "user_id must be greater than zero."
            )
        }

    # -----------------------------------------------------
    # FIND USER IN DATABASE
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_active.is_(True)
        )
        .first()
    )

    if user is None:
        return {
            "success": False,
            "provider": "gmail",
            "message": (
                "Active user was not found "
                "for the provided user_id."
            )
        }

    # -----------------------------------------------------
    # CREATE GMAIL AUTHORIZATION URL
    # -----------------------------------------------------

    result = gmail_oauth.create_authorization_url(
        user_id=user.id
    )

    if not result["success"]:
        return result

    # -----------------------------------------------------
    # CREATE OAUTH CONNECTION
    # -----------------------------------------------------

    connection_result = oauth_manager.create_connection(
        user_id=str(user.id),
        provider="gmail",
        scopes=gmail_oauth.GMAIL_SCOPES
    )

    if not connection_result["success"]:
        return connection_result

    # -----------------------------------------------------
    # REDIRECT USER TO GOOGLE
    # -----------------------------------------------------

    return RedirectResponse(
        url=result["authorization_url"]
    )


# ---------------------------------------------------------
# GMAIL CALLBACK
# ---------------------------------------------------------

@router.get("/gmail/callback")
def gmail_callback(
    request: Request,
    db: Session = Depends(get_db)
):

    query_params = request.query_params

    # -----------------------------------------------------
    # GOOGLE AUTHORIZATION ERROR
    # -----------------------------------------------------

    error = query_params.get("error")

    if error:

        state = query_params.get("state")

        if state:
            gmail_oauth.remove_state(state)

        return {
            "success": False,
            "provider": "gmail",
            "message": (
                "Gmail authorization was not completed."
            ),
            "error": error
        }

    # -----------------------------------------------------
    # GET CODE AND STATE
    # -----------------------------------------------------

    code = query_params.get("code")
    state = query_params.get("state")

    if not code:
        return {
            "success": False,
            "provider": "gmail",
            "message": (
                "Authorization code is missing."
            )
        }

    if not state:
        return {
            "success": False,
            "provider": "gmail",
            "message": (
                "OAuth state is missing."
            )
        }

    # -----------------------------------------------------
    # VALIDATE OAUTH STATE
    # -----------------------------------------------------

    state_result = gmail_oauth.validate_state(state)

    if not state_result["success"]:
        return state_result

    user_id = state_result["user_id"]

    # -----------------------------------------------------
    # VERIFY DATABASE USER
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_active.is_(True)
        )
        .first()
    )

    if user is None:
        return {
            "success": False,
            "provider": "gmail",
            "message": (
                "Active database user was not found "
                "for this OAuth request."
            )
        }

    # -----------------------------------------------------
    # EXCHANGE AUTHORIZATION CODE
    # -----------------------------------------------------

    authorization_response = str(request.url)

    token_result = gmail_oauth.exchange_code(
        state=state,
        authorization_response=authorization_response
    )

    if not token_result["success"]:
        return token_result

    # -----------------------------------------------------
    # GET TOKEN INFORMATION
    # -----------------------------------------------------

    user_id = token_result["user_id"]
    scopes = token_result["scopes"]

    # -----------------------------------------------------
    # STORE TOKEN
    # -----------------------------------------------------

    token_store_result = token_manager.store_token(
        user_id=str(user_id),
        provider="gmail",
        access_token=token_result["access_token"],
        refresh_token=token_result["refresh_token"],
        expires_at=token_result["expires_at"]
    )

    if not token_store_result["success"]:
        return {
            "success": False,
            "provider": "gmail",
            "message": (
                "Gmail authorization succeeded, "
                "but secure token storage failed."
            )
        }

    # -----------------------------------------------------
    # AUTHORIZE OAUTH CONNECTION
    # -----------------------------------------------------

    authorization_result = (
        oauth_manager.authorize_connection_with_scopes(
            user_id=str(user_id),
            provider="gmail",
            scopes=scopes
        )
    )

    if not authorization_result["success"]:
        return {
            "success": False,
            "provider": "gmail",
            "message": (
                "Gmail token was stored, "
                "but OAuth connection could not be authorized."
            )
        }

    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return {
        "success": True,
        "provider": "gmail",
        "user_id": user_id,
        "connection_id": (
            authorization_result["connection_id"]
        ),
        "token_id": token_store_result["token_id"],
        "status": "AUTHORIZED",
        "scopes": scopes,
        "message": (
            "Gmail connected successfully. "
            "OAuth token is stored securely."
        )
    }


# ---------------------------------------------------------
# GOOGLE CALENDAR AUTHORIZE
# ---------------------------------------------------------

@router.get("/calendar/authorize")
def calendar_authorize(
    user_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # VALIDATE USER ID
    # -----------------------------------------------------

    if user_id <= 0:
        return {
            "success": False,
            "provider": "google_calendar",
            "message": (
                "user_id must be greater than zero."
            )
        }

    # -----------------------------------------------------
    # FIND USER IN DATABASE
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_active.is_(True)
        )
        .first()
    )

    if user is None:
        return {
            "success": False,
            "provider": "google_calendar",
            "message": (
                "Active user was not found "
                "for the provided user_id."
            )
        }

    # -----------------------------------------------------
    # CREATE CALENDAR AUTHORIZATION URL
    # -----------------------------------------------------

    result = create_calendar_authorization_url(
        user_id=user.id
    )

    if not result["success"]:
        return result

    # -----------------------------------------------------
    # CREATE OAUTH CONNECTION
    # -----------------------------------------------------

    connection_result = oauth_manager.create_connection(
        user_id=str(user.id),
        provider="google_calendar",
        scopes=result["scopes"]
    )

    if not connection_result["success"]:
        return connection_result

    # -----------------------------------------------------
    # REDIRECT USER TO GOOGLE
    # -----------------------------------------------------

    return RedirectResponse(
        url=result["authorization_url"]
    )


# ---------------------------------------------------------
# GOOGLE CALENDAR CALLBACK
# ---------------------------------------------------------

@router.get("/calendar/callback")
def calendar_callback(
    request: Request,
    db: Session = Depends(get_db)
):

    query_params = request.query_params

    # -----------------------------------------------------
    # GOOGLE AUTHORIZATION ERROR
    # -----------------------------------------------------

    error = query_params.get("error")

    if error:
        return {
            "success": False,
            "provider": "google_calendar",
            "message": (
                "Google Calendar authorization "
                "was not completed."
            ),
            "error": error
        }

    # -----------------------------------------------------
    # GET CODE AND STATE
    # -----------------------------------------------------

    code = query_params.get("code")
    state = query_params.get("state")

    if not code:
        return {
            "success": False,
            "provider": "google_calendar",
            "message": (
                "Authorization code is missing."
            )
        }

    if not state:
        return {
            "success": False,
            "provider": "google_calendar",
            "message": (
                "OAuth state is missing."
            )
        }

    # -----------------------------------------------------
    # VALIDATE OAUTH STATE
    # -----------------------------------------------------

    state_result = validate_calendar_state(state)

    if not state_result["success"]:
        return state_result

    user_id = state_result["user_id"]

    # -----------------------------------------------------
    # VERIFY DATABASE USER
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_active.is_(True)
        )
        .first()
    )

    if user is None:
        return {
            "success": False,
            "provider": "google_calendar",
            "message": (
                "Active database user was not found "
                "for this OAuth request."
            )
        }

    # -----------------------------------------------------
    # EXCHANGE AUTHORIZATION CODE
    # -----------------------------------------------------

    token_result = exchange_calendar_code(
        code=code,
        state=state
    )

    if not token_result["success"]:
        return token_result

    # -----------------------------------------------------
    # GET TOKEN INFORMATION
    # -----------------------------------------------------

    scopes = token_result["scopes"]

    # -----------------------------------------------------
    # STORE TOKEN SECURELY
    # -----------------------------------------------------

    token_store_result = token_manager.store_token(
        user_id=str(user_id),
        provider="google_calendar",
        access_token=token_result["access_token"],
        refresh_token=token_result["refresh_token"],
        expires_at=token_result["expires_at"]
    )

    if not token_store_result["success"]:
        return {
            "success": False,
            "provider": "google_calendar",
            "message": (
                "Calendar authorization succeeded, "
                "but secure token storage failed."
            )
        }

    # -----------------------------------------------------
    # AUTHORIZE OAUTH CONNECTION
    # -----------------------------------------------------

    authorization_result = (
        oauth_manager.authorize_connection_with_scopes(
            user_id=str(user_id),
            provider="google_calendar",
            scopes=scopes
        )
    )

    if not authorization_result["success"]:
        return {
            "success": False,
            "provider": "google_calendar",
            "message": (
                "Calendar token was stored, "
                "but OAuth connection could not be authorized."
            )
        }

    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return {
        "success": True,
        "provider": "google_calendar",
        "user_id": user_id,
        "connection_id": (
            authorization_result["connection_id"]
        ),
        "token_id": token_store_result["token_id"],
        "status": "AUTHORIZED",
        "scopes": scopes,
        "message": (
            "Google Calendar connected successfully. "
            "OAuth token is stored securely."
        )
    }