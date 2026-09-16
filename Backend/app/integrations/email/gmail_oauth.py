import json
import os
import secrets
from datetime import datetime, timezone

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


class GmailOAuth:
    """
    Handles Google Gmail OAuth 2.0 authorization.
    """

    GMAIL_SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
    ]

    def __init__(self):
        self.client_secret_file = os.getenv(
            "GOOGLE_CLIENT_SECRET_FILE"
        )

        self.redirect_uri = os.getenv(
            "GOOGLE_REDIRECT_URI",
            "http://127.0.0.1:8000/api/integrations/gmail/callback"
        )

        backend_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../../"
            )
        )

        self.state_file = os.path.join(
            backend_dir,
            "gmail_oauth_states.json"
        )

        self.pending_states = self._load_states()

    # ---------------------------------------------------------
    # USER ID VALIDATION
    # ---------------------------------------------------------

    def _validate_user_id(self, user_id):
        """
        Validate that user_id represents a valid
        database User.id.
        """

        if user_id is None:
            return {
                "success": False,
                "message": "user_id is required."
            }

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return {
                "success": False,
                "message": "user_id must be a valid integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "user_id must be greater than zero."
            }

        return {
            "success": True,
            "user_id": user_id
        }

    # ---------------------------------------------------------
    # STATE STORAGE
    # ---------------------------------------------------------

    def _load_states(self):
        """
        Load pending OAuth states from disk.
        """

        try:
            if not os.path.exists(self.state_file):
                return {}

            with open(
                self.state_file,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

        except Exception:
            return {}

    def _save_states(self):
        """
        Save pending OAuth states to disk.
        """

        try:
            with open(
                self.state_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.pending_states,
                    file,
                    indent=2
                )

        except Exception as exc:
            raise RuntimeError(
                "Unable to save Gmail OAuth state: "
                f"{exc}"
            )

    def _refresh_states(self):
        """
        Reload states from disk before reading them.
        """

        self.pending_states = self._load_states()

    # ---------------------------------------------------------
    # CONFIGURATION
    # ---------------------------------------------------------

    def _validate_configuration(self):
        if not self.client_secret_file:
            raise RuntimeError(
                "GOOGLE_CLIENT_SECRET_FILE is not configured."
            )

        if not os.path.exists(self.client_secret_file):
            raise RuntimeError(
                "Google client secret file not found: "
                f"{self.client_secret_file}"
            )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def get_status(self):
        configuration_ready = bool(
            self.client_secret_file
            and os.path.exists(self.client_secret_file)
        )

        self._refresh_states()

        return {
            "provider": "gmail",
            "service": "Gmail OAuth",
            "status": (
                "ready"
                if configuration_ready
                else "configuration_required"
            ),
            "configuration_ready": configuration_ready,
            "redirect_uri": self.redirect_uri,
            "scopes": self.GMAIL_SCOPES,
            "pending_states": len(self.pending_states)
        }

    # ---------------------------------------------------------
    # CREATE AUTHORIZATION URL
    # ---------------------------------------------------------

    def create_authorization_url(self, user_id):
        self._validate_configuration()

        user_result = self._validate_user_id(user_id)

        if not user_result["success"]:
            return user_result

        user_id = user_result["user_id"]

        state = secrets.token_urlsafe(32)

        flow = Flow.from_client_secrets_file(
            self.client_secret_file,
            scopes=self.GMAIL_SCOPES,
            redirect_uri=self.redirect_uri
        )

        authorization_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            state=state,
            prompt="consent"
        )

        self._refresh_states()

        # -------------------------------------------------
        # SAVE PKCE CODE VERIFIER
        # -------------------------------------------------

        self.pending_states[state] = {
            "user_id": user_id,
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "code_verifier": flow.code_verifier
        }

        self._save_states()

        return {
            "success": True,
            "authorization_url": authorization_url,
            "state": state,
            "user_id": user_id
        }

    # ---------------------------------------------------------
    # STATE VALIDATION
    # ---------------------------------------------------------

    def validate_state(self, state: str):
        if not state:
            return {
                "success": False,
                "message": "OAuth state is required."
            }

        self._refresh_states()

        state_data = self.pending_states.get(state)

        if state_data is None:
            return {
                "success": False,
                "message": "Invalid or expired OAuth state."
            }

        user_result = self._validate_user_id(
            state_data.get("user_id")
        )

        if not user_result["success"]:
            return {
                "success": False,
                "message": (
                    "OAuth state contains "
                    "an invalid user ID."
                )
            }

        return {
            "success": True,
            "user_id": user_result["user_id"],
            "state": state,
            "code_verifier": state_data.get(
                "code_verifier"
            )
        }

    # ---------------------------------------------------------
    # EXCHANGE AUTHORIZATION CODE
    # ---------------------------------------------------------

    def exchange_code(
        self,
        state: str,
        authorization_response: str
    ):
        self._validate_configuration()

        state_result = self.validate_state(state)

        if not state_result["success"]:
            return state_result

        try:
            flow = Flow.from_client_secrets_file(
                self.client_secret_file,
                scopes=self.GMAIL_SCOPES,
                state=state,
                redirect_uri=self.redirect_uri
            )

            # -------------------------------------------------
            # RESTORE PKCE CODE VERIFIER
            # -------------------------------------------------

            code_verifier = state_result.get(
                "code_verifier"
            )

            if code_verifier:
                flow.code_verifier = code_verifier

            flow.fetch_token(
                authorization_response=authorization_response
            )

            credentials = flow.credentials

            access_token = credentials.token
            refresh_token = credentials.refresh_token
            expiry = credentials.expiry

            if not access_token:
                return {
                    "success": False,
                    "message": (
                        "Google did not return "
                        "an access token."
                    )
                }

            expires_at = (
                expiry.isoformat()
                if expiry
                else None
            )

            user_id = state_result["user_id"]

            self.remove_state(state)

            return {
                "success": True,
                "user_id": user_id,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at,
                "scopes": self.GMAIL_SCOPES
            }

        except Exception as exc:
            return {
                "success": False,
                "message": (
                    "Gmail OAuth token exchange failed."
                ),
                "error": str(exc)
            }

    # ---------------------------------------------------------
    # STATE MANAGEMENT
    # ---------------------------------------------------------

    def get_pending_state(self, state: str):
        self._refresh_states()
        return self.pending_states.get(state)

    def remove_pending_state(self, state: str):
        self._refresh_states()
        self.pending_states.pop(state, None)
        self._save_states()

    def remove_state(self, state: str):
        self._refresh_states()
        self.pending_states.pop(state, None)
        self._save_states()

    # ---------------------------------------------------------
    # CREATE FLOW
    # ---------------------------------------------------------

    def create_flow(self, state: str):
        self._validate_configuration()

        if not state:
            raise ValueError(
                "OAuth state is required."
            )

        return Flow.from_client_secrets_file(
            self.client_secret_file,
            scopes=self.GMAIL_SCOPES,
            state=state,
            redirect_uri=self.redirect_uri
        )