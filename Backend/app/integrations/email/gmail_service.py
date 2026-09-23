import base64
import json
import os
from datetime import datetime, timezone
from email.mime.text import MIMEText

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from app.security.token_manager import TokenManager


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


class GmailService:
    """
    Gmail API service layer.

    Uses securely stored OAuth tokens from TokenManager.

    If the access token has expired, the refresh token is used
    to obtain a new access token automatically.
    """

    PROVIDER = "gmail"

    GMAIL_SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
    ]

    def __init__(self):
        self.token_manager = TokenManager()

        self.client_secret_file = os.getenv(
            "GOOGLE_CLIENT_SECRET_FILE"
        )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def get_status(self) -> dict:
        """
        Return Gmail service status.
        """

        try:
            return {
                "name": "gmail_service",
                "provider": self.PROVIDER,
                "available": True,
                "token_storage": "database",
                "encrypted_tokens": True,
                "scopes": self.GMAIL_SCOPES,
                "message": (
                    "Gmail service is ready."
                )
            }

        except Exception as error:
            return {
                "name": "gmail_service",
                "provider": self.PROVIDER,
                "available": False,
                "message": str(error)
            }

    # ---------------------------------------------------------
    # GOOGLE CLIENT CONFIGURATION
    # ---------------------------------------------------------

    def _get_client_credentials(self):
        """
        Load Google OAuth client_id and client_secret
        from the existing Google client secret file.
        """

        if not self.client_secret_file:
            return {
                "success": False,
                "message": (
                    "GOOGLE_CLIENT_SECRET_FILE is not configured."
                )
            }

        if not os.path.exists(self.client_secret_file):
            return {
                "success": False,
                "message": (
                    "Google client secret file not found."
                )
            }

        try:

            with open(
                self.client_secret_file,
                "r",
                encoding="utf-8"
            ) as file:

                client_config = json.load(file)

            # Google OAuth client-secret files normally contain
            # either "web" or "installed" configuration.
            oauth_config = (
                client_config.get("web")
                or client_config.get("installed")
            )

            if not isinstance(oauth_config, dict):
                return {
                    "success": False,
                    "message": (
                        "Invalid Google OAuth client "
                        "configuration."
                    )
                }

            client_id = oauth_config.get(
                "client_id"
            )

            client_secret = oauth_config.get(
                "client_secret"
            )

            if not client_id:
                return {
                    "success": False,
                    "message": (
                        "Google OAuth client_id is missing."
                    )
                }

            if not client_secret:
                return {
                    "success": False,
                    "message": (
                        "Google OAuth client_secret is missing."
                    )
                }

            return {
                "success": True,
                "client_id": client_id,
                "client_secret": client_secret
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Failed to load Google OAuth "
                    "client configuration."
                ),
                "error": str(error)
            }

    # ---------------------------------------------------------
    # TOKEN / CREDENTIALS
    # ---------------------------------------------------------

    def _get_credentials(
        self,
        user_id: int
    ):
        """
        Retrieve Gmail OAuth credentials.

        Expired access tokens are allowed here because
        GmailService can refresh them using the stored
        refresh token and Google OAuth client credentials.
        """

        token_result = self.token_manager.get_token(
            user_id=user_id,
            provider=self.PROVIDER,
            allow_expired=True
        )

        if not token_result.get("success"):
            return {
                "success": False,
                "message": (
                    token_result.get(
                        "message",
                        "Gmail token not found."
                    )
                )
            }

        access_token = token_result.get(
            "access_token"
        )

        refresh_token = token_result.get(
            "refresh_token"
        )

        if not access_token:
            return {
                "success": False,
                "message": (
                    "Gmail access token is missing."
                )
            }

        try:

            # -------------------------------------------------
            # LOAD GOOGLE CLIENT CREDENTIALS
            # -------------------------------------------------

            client_result = (
                self._get_client_credentials()
            )

            if not client_result.get("success"):
                return client_result

            client_id = client_result[
                "client_id"
            ]

            client_secret = client_result[
                "client_secret"
            ]

            # -------------------------------------------------
            # CREATE GOOGLE CREDENTIALS
            # -------------------------------------------------

            credentials = Credentials(
                token=access_token,
                refresh_token=refresh_token,
                token_uri=(
                    "https://oauth2.googleapis.com/token"
                ),
                client_id=client_id,
                client_secret=client_secret,
                scopes=self.GMAIL_SCOPES
            )

            # -------------------------------------------------
            # REFRESH EXPIRED ACCESS TOKEN
            # -------------------------------------------------

            if credentials.expired:

                if not refresh_token:
                    return {
                        "success": False,
                        "message": (
                            "Gmail access token has expired "
                            "and no refresh token is available."
                        )
                    }

                credentials.refresh(
                    Request()
                )

                new_access_token = (
                    credentials.token
                )

                if not new_access_token:
                    return {
                        "success": False,
                        "message": (
                            "Gmail token refresh did not "
                            "return a new access token."
                        )
                    }

                # Google normally returns a new expiry.
                new_expires_at = None

                if credentials.expiry:

                    expiry = credentials.expiry

                    if expiry.tzinfo is None:
                        expiry = expiry.replace(
                            tzinfo=timezone.utc
                        )

                    new_expires_at = (
                        expiry.isoformat()
                    )

                # -------------------------------------------------
                # STORE REFRESHED TOKEN
                # -------------------------------------------------

                store_result = (
                    self.token_manager.store_token(
                        user_id=user_id,
                        provider=self.PROVIDER,
                        access_token=new_access_token,
                        refresh_token=refresh_token,
                        expires_at=new_expires_at
                    )
                )

                if not store_result.get("success"):
                    return {
                        "success": False,
                        "message": (
                            "Gmail access token was refreshed "
                            "but could not be stored."
                        ),
                        "error": store_result.get(
                            "message"
                        )
                    }

                access_token = new_access_token

            return {
                "success": True,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": (
                    credentials.expiry
                )
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Failed to create Gmail credentials."
                ),
                "error": str(error)
            }

    # ---------------------------------------------------------
    # BUILD SERVICE
    # ---------------------------------------------------------

    def _build_service(
        self,
        user_id: int
    ):
        """
        Build an authenticated Gmail API client.
        """

        credentials_result = self._get_credentials(
            user_id=user_id
        )

        if not credentials_result.get("success"):
            return credentials_result

        try:

            client_result = (
                self._get_client_credentials()
            )

            if not client_result.get("success"):
                return client_result

            credentials = Credentials(
                token=credentials_result[
                    "access_token"
                ],
                refresh_token=credentials_result.get(
                    "refresh_token"
                ),
                token_uri=(
                    "https://oauth2.googleapis.com/token"
                ),
                client_id=client_result[
                    "client_id"
                ],
                client_secret=client_result[
                    "client_secret"
                ],
                scopes=self.GMAIL_SCOPES
            )

            service = build(
                "gmail",
                "v1",
                credentials=credentials
            )

            return {
                "success": True,
                "service": service
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Failed to build Gmail API service."
                ),
                "error": str(error)
            }

    # ---------------------------------------------------------
    # GET PROFILE
    # ---------------------------------------------------------

    def get_profile(
        self,
        user_id: int
    ) -> dict:
        """
        Get the authenticated user's Gmail profile.
        """

        service_result = self._build_service(
            user_id=user_id
        )

        if not service_result.get("success"):
            return service_result

        try:

            profile = (
                service_result["service"]
                .users()
                .getProfile(
                    userId="me"
                )
                .execute()
            )

            return {
                "success": True,
                "email_address": profile.get(
                    "emailAddress"
                ),
                "messages_total": profile.get(
                    "messagesTotal"
                ),
                "threads_total": profile.get(
                    "threadsTotal"
                ),
                "message": (
                    "Gmail profile retrieved successfully."
                )
            }

        except HttpError as error:

            return {
                "success": False,
                "message": (
                    "Gmail API request failed."
                ),
                "error": str(error)
            }

        except Exception as error:

            return {
                "success": False,
                "message": str(error)
            }

    # ---------------------------------------------------------
    # SEND EMAIL
    # ---------------------------------------------------------

    def send_email(
        self,
        user_id: int,
        recipient: str,
        subject: str,
        message: str
    ) -> dict:
        """
        Send an email through Gmail.
        """

        if not recipient:
            return {
                "success": False,
                "message": "Recipient is required."
            }

        if not subject:
            return {
                "success": False,
                "message": "Subject is required."
            }

        if not message:
            return {
                "success": False,
                "message": "Message is required."
            }

        service_result = self._build_service(
            user_id=user_id
        )

        if not service_result.get("success"):
            return service_result

        try:

            email_message = MIMEText(
                message,
                "plain",
                "utf-8"
            )

            email_message["to"] = recipient
            email_message["subject"] = subject

            raw_message = (
                base64.urlsafe_b64encode(
                    email_message.as_bytes()
                ).decode("utf-8")
            )

            send_body = {
                "raw": raw_message
            }

            sent_message = (
                service_result["service"]
                .users()
                .messages()
                .send(
                    userId="me",
                    body=send_body
                )
                .execute()
            )

            return {
                "success": True,
                "status": "sent",
                "action": "send",
                "message_id": sent_message.get(
                    "id"
                ),
                "thread_id": sent_message.get(
                    "threadId"
                ),
                "recipient": recipient,
                "subject": subject,
                "message": (
                    "Email sent successfully through Gmail."
                )
            }

        except HttpError as error:

            print("=" * 70)
            print("GMAIL SEND HTTP ERROR")
            print("ERROR TYPE:", type(error).__name__)
            print("ERROR:", repr(error))
            print("ERROR STRING:", str(error))
            print("=" * 70)

            return {
                "success": False,
                "status": "failed",
                "message": (
                    "Gmail email sending failed."
                ),
                "error": str(error)
            }

        except Exception as error:

            print("=" * 70)
            print("GMAIL SEND GENERAL ERROR")
            print("ERROR TYPE:", type(error).__name__)
            print("ERROR:", repr(error))
            print("ERROR STRING:", str(error))
            print("=" * 70)

            return {
                "success": False,
                "status": "failed",
                "message": str(error),
                "error": str(error)
            }

    # ---------------------------------------------------------
    # LIST MESSAGES
    # ---------------------------------------------------------

    def list_messages(
        self,
        user_id: int,
        max_results: int = 10
    ) -> dict:
        """
        List recent Gmail messages.
        """

        if max_results < 1:
            max_results = 1

        if max_results > 100:
            max_results = 100

        service_result = self._build_service(
            user_id=user_id
        )

        if not service_result.get("success"):
            return service_result

        try:

            response = (
                service_result["service"]
                .users()
                .messages()
                .list(
                    userId="me",
                    maxResults=max_results
                )
                .execute()
            )

            messages = response.get(
                "messages",
                []
            )

            return {
                "success": True,
                "count": len(messages),
                "messages": messages,
                "next_page_token": response.get(
                    "nextPageToken"
                ),
                "message": (
                    "Gmail messages retrieved successfully."
                )
            }

        except HttpError as error:

            return {
                "success": False,
                "message": (
                    "Gmail API request failed."
                ),
                "error": str(error)
            }

        except Exception as error:

            return {
                "success": False,
                "message": str(error)
            }