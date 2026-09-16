
import hashlib
import json
import os
import secrets
import base64
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow


load_dotenv()

# Google may return previously granted Gmail scopes along with
# the Calendar scope during incremental authorization.
# Allow those additional already-granted scopes.
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"


BASE_DIR = Path(__file__).resolve().parents[3]
STATE_FILE = BASE_DIR / "calendar_oauth_states.json"

CLIENT_SECRET_FILE = os.getenv("GOOGLE_CLIENT_SECRET_FILE")
REDIRECT_URI = os.getenv("GOOGLE_CALENDAR_REDIRECT_URI")


CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


def _create_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(
        code_verifier.encode("ascii")
    ).digest()

    return base64.urlsafe_b64encode(
        digest
    ).rstrip(b"=").decode("ascii")


def _validate_configuration():
    if not CLIENT_SECRET_FILE:
        raise ValueError(
            "GOOGLE_CLIENT_SECRET_FILE is not configured."
        )

    if not REDIRECT_URI:
        raise ValueError(
            "GOOGLE_CALENDAR_REDIRECT_URI is not configured."
        )

    client_secret_path = Path(CLIENT_SECRET_FILE)

    if not client_secret_path.exists():
        raise FileNotFoundError(
            "Google OAuth client secret file was not found: "
            f"{CLIENT_SECRET_FILE}"
        )


def _load_states() -> dict:
    if not STATE_FILE.exists():
        return {}

    try:
        with STATE_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

    except (OSError, json.JSONDecodeError):
        pass

    return {}


def _save_states(states: dict) -> None:
    with STATE_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            states,
            file,
            indent=2
        )


def create_authorization_url(user_id: int) -> dict:
    _validate_configuration()

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        return {
            "success": False,
            "message": "User ID must be a valid integer."
        }

    if user_id <= 0:
        return {
            "success": False,
            "message": "User ID must be greater than zero."
        }

    state = secrets.token_urlsafe(32)

    code_verifier = secrets.token_urlsafe(64)

    code_challenge = _create_code_challenge(
        code_verifier
    )

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=CALENDAR_SCOPES,
        redirect_uri=REDIRECT_URI,
        autogenerate_code_verifier=False
    )

    flow.code_verifier = code_verifier

    authorization_url, generated_state = (
        flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            state=state,
            prompt="consent",
            code_challenge=code_challenge,
            code_challenge_method="S256"
        )
    )

    states = _load_states()

    states[state] = {
        "user_id": user_id,
        "state": generated_state,
        "code_verifier": code_verifier
    }

    _save_states(states)

    return {
        "success": True,
        "authorization_url": authorization_url,
        "state": state,
        "user_id": user_id,
        "scopes": CALENDAR_SCOPES,
        "message": (
            "Calendar authorization URL created successfully."
        )
    }


def validate_state(state: str) -> dict:
    if not state:
        return {
            "success": False,
            "message": "OAuth state is required."
        }

    states = _load_states()

    state_data = states.get(state)

    if not state_data:
        return {
            "success": False,
            "message": "Invalid or expired OAuth state."
        }

    return {
        "success": True,
        "user_id": state_data.get("user_id"),
        "state": state,
        "code_verifier": state_data.get(
            "code_verifier"
        ),
        "message": (
            "OAuth state validated successfully."
        )
    }


def exchange_code_for_token(
    code: str,
    state: str
) -> dict:

    _validate_configuration()

    if not code:
        return {
            "success": False,
            "message": "Authorization code is required."
        }

    if not state:
        return {
            "success": False,
            "message": "OAuth state is required."
        }

    states = _load_states()

    state_data = states.get(state)

    if not state_data:
        return {
            "success": False,
            "message": "Invalid or expired OAuth state."
        }

    code_verifier = state_data.get(
        "code_verifier"
    )

    if not code_verifier:
        return {
            "success": False,
            "message": (
                "OAuth PKCE code verifier is missing."
            )
        }

    try:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=CALENDAR_SCOPES,
            state=state,
            redirect_uri=REDIRECT_URI,
            autogenerate_code_verifier=False
        )

        flow.code_verifier = code_verifier

        flow.fetch_token(
            code=code,
            code_verifier=code_verifier
        )

        credentials = flow.credentials

        granted_scopes = (
            list(credentials.scopes)
            if credentials.scopes
            else CALENDAR_SCOPES
        )

        # OAuth state is single-use.
        del states[state]
        _save_states(states)

        return {
            "success": True,
            "credentials": credentials,
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_at": (
                credentials.expiry.isoformat()
                if credentials.expiry
                else None
            ),
            "scopes": granted_scopes,
            "message": (
                "Calendar OAuth token received successfully."
            )
        }

    except Exception as error:
        return {
            "success": False,
            "message": [
                "Calendar OAuth token exchange failed.",
                str(error)
            ]
        }


def get_configuration_status() -> dict:
    client_secret_exists = False

    if CLIENT_SECRET_FILE:
        client_secret_exists = Path(
            CLIENT_SECRET_FILE
        ).exists()

    return {
        "provider": "google_calendar",
        "client_secret_configured": bool(
            CLIENT_SECRET_FILE
        ),
        "client_secret_exists": client_secret_exists,
        "redirect_uri_configured": bool(
            REDIRECT_URI
        ),
        "redirect_uri": REDIRECT_URI,
        "scopes": CALENDAR_SCOPES,
        "status": (
            "ready"
            if (
                CLIENT_SECRET_FILE
                and client_secret_exists
                and REDIRECT_URI
            )
            else "not_ready"
        )
    }
