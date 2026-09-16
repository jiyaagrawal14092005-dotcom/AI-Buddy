import base64
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.security.token_manager import TokenManager


class GmailService:
    """
    Gmail API service layer.

    Uses the securely stored OAuth token from TokenManager
    to communicate with the Gmail API.
    """

    PROVIDER = "gmail"

    GMAIL_SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
    ]

    def __init__(self):
        self.token_manager = TokenManager()

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

    def _get_credentials(
        self,
        user_id: int
    ):
        """
        Retrieve Gmail OAuth credentials for a user.
        """

        token_result = self.token_manager.get_token(
            user_id=user_id,
            provider=self.PROVIDER
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

        if not access_token:
            return {
                "success": False,
                "message": (
                    "Gmail access token is missing."
                )
            }

        return {
            "success": True,
            "access_token": access_token,
            "refresh_token": token_result.get(
                "refresh_token"
            ),
            "expires_at": token_result.get(
                "expires_at"
            )
        }

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
            from google.oauth2.credentials import (
                Credentials
            )

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
                    "Failed to build Gmail API service.",
                    str(error)
                )
            }

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
                .getProfile(userId="me")
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
                    "Gmail API request failed.",
                    str(error)
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": str(error)
            }

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

            raw_message = base64.urlsafe_b64encode(
                email_message.as_bytes()
            ).decode("utf-8")

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
            return {
                "success": False,
                "status": "failed",
                "message": (
                    "Gmail email sending failed.",
                    str(error)
                )
            }

        except Exception as error:
            return {
                "success": False,
                "status": "failed",
                "message": str(error)
            }

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
                    "Gmail API request failed.",
                    str(error)
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": str(error)
            }