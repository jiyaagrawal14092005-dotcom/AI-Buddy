
from datetime import datetime
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from app.security.token_manager import TokenManager


class GoogleCalendarService:
    """
    Real Google Calendar API service for AI Buddy.

    Handles:
    - Google Calendar connection
    - Event creation
    - Event listing
    - Event retrieval
    - Event deletion
    """

    CALENDAR_SCOPES = [
        "https://www.googleapis.com/auth/calendar"
    ]

    def __init__(self):
        self.token_manager = TokenManager()

    def _validate_user_id(self, user_id: Any) -> tuple[bool, int | None, str | None]:
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return False, None, "User ID must be a valid integer."

        if user_id <= 0:
            return False, None, "User ID must be greater than zero."

        return True, user_id, None

    def _get_credentials(self, user_id: int) -> dict:
        success, validated_user_id, error = self._validate_user_id(
            user_id
        )

        if not success:
            return {
                "success": False,
                "message": error
            }

        token_result = self.token_manager.get_token(
            user_id=str(validated_user_id),
            provider="google_calendar"
        )

        if not token_result.get("success"):
            return {
                "success": False,
                "message": token_result.get(
                    "message",
                    "Google Calendar token was not found."
                )
            }

        access_token = token_result.get("access_token")
        refresh_token = token_result.get("refresh_token")

        if not access_token:
            return {
                "success": False,
                "message": (
                    "Google Calendar access token is missing."
                )
            }

        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=self.CALENDAR_SCOPES
        )

        return {
            "success": True,
            "credentials": credentials
        }

    def _build_service(self, user_id: int) -> dict:
        credentials_result = self._get_credentials(
            user_id=user_id
        )

        if not credentials_result.get("success"):
            return credentials_result

        try:
            service = build(
                "calendar",
                "v3",
                credentials=credentials_result["credentials"]
            )

            return {
                "success": True,
                "service": service
            }

        except Exception as error:
            return {
                "success": False,
                "message": (
                    "Google Calendar service could not be created.",
                    str(error)
                )
            }

    def get_calendar_list(
        self,
        user_id: int
    ) -> dict:
        """
        Get calendars available to the connected Google account.
        """

        service_result = self._build_service(
            user_id=user_id
        )

        if not service_result.get("success"):
            return service_result

        try:
            response = (
                service_result["service"]
                .calendarList()
                .list()
                .execute()
            )

            calendars = []

            for calendar in response.get("items", []):
                calendars.append({
                    "id": calendar.get("id"),
                    "summary": calendar.get("summary"),
                    "description": calendar.get("description"),
                    "primary": calendar.get("primary", False),
                    "time_zone": calendar.get("timeZone")
                })

            return {
                "success": True,
                "calendars": calendars,
                "count": len(calendars),
                "message": (
                    "Google Calendars retrieved successfully."
                )
            }

        except HttpError as error:
            return {
                "success": False,
                "message": (
                    "Google Calendar API request failed.",
                    str(error)
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": (
                    "Failed to retrieve Google Calendars.",
                    str(error)
                )
            }

    def create_event(
        self,
        user_id: int,
        title: str,
        date: str,
        time: str,
        details: str = "",
        calendar_id: str = "primary",
        duration_minutes: int = 60
    ) -> dict:
        """
        Create a real event in Google Calendar.

        date format:
            YYYY-MM-DD

        time format:
            HH:MM

        Example:
            2026-09-20
            14:30
        """

        success, validated_user_id, error = self._validate_user_id(
            user_id
        )

        if not success:
            return {
                "success": False,
                "message": error
            }

        if not isinstance(title, str) or not title.strip():
            return {
                "success": False,
                "message": "Event title is required."
            }

        if not isinstance(date, str) or not date.strip():
            return {
                "success": False,
                "message": "Event date is required."
            }

        if not isinstance(time, str) or not time.strip():
            return {
                "success": False,
                "message": "Event time is required."
            }

        if not isinstance(details, str):
            return {
                "success": False,
                "message": "Event details must be a string."
            }

        try:
            start_datetime = datetime.strptime(
                f"{date.strip()} {time.strip()}",
                "%Y-%m-%d %H:%M"
            )

        except ValueError:
            return {
                "success": False,
                "message": (
                    "Date and time must use "
                    "YYYY-MM-DD and HH:MM format."
                )
            }

        try:
            duration_minutes = int(duration_minutes)

        except (TypeError, ValueError):
            return {
                "success": False,
                "message": (
                    "Duration must be a valid integer."
                )
            }

        if duration_minutes <= 0:
            return {
                "success": False,
                "message": (
                    "Duration must be greater than zero."
                )
            }

        from datetime import timedelta

        end_datetime = (
            start_datetime
            + timedelta(minutes=duration_minutes)
        )

        service_result = self._build_service(
            user_id=validated_user_id
        )

        if not service_result.get("success"):
            return service_result

        event_body = {
            "summary": title.strip(),
            "description": details.strip(),
            "start": {
                "dateTime": start_datetime.isoformat(),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
                "timeZone": "Asia/Kolkata"
            }
        }

        try:
            event = (
                service_result["service"]
                .events()
                .insert(
                    calendarId=calendar_id,
                    body=event_body
                )
                .execute()
            )

            return {
                "success": True,
                "status": "created",
                "action": "create",
                "event": {
                    "id": event.get("id"),
                    "title": event.get("summary"),
                    "description": event.get(
                        "description",
                        ""
                    ),
                    "start": event.get("start"),
                    "end": event.get("end"),
                    "html_link": event.get("htmlLink")
                },
                "message": (
                    "Google Calendar event created successfully."
                )
            }

        except HttpError as error:
            return {
                "success": False,
                "message": (
                    "Google Calendar event creation failed.",
                    str(error)
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": (
                    "Failed to create Google Calendar event.",
                    str(error)
                )
            }

    def list_events(
        self,
        user_id: int,
        max_results: int = 10,
        calendar_id: str = "primary"
    ) -> dict:
        """
        List upcoming Google Calendar events.
        """

        success, validated_user_id, error = self._validate_user_id(
            user_id
        )

        if not success:
            return {
                "success": False,
                "message": error
            }

        try:
            max_results = int(max_results)

        except (TypeError, ValueError):
            max_results = 10

        if max_results <= 0:
            max_results = 10

        if max_results > 100:
            max_results = 100

        service_result = self._build_service(
            user_id=validated_user_id
        )

        if not service_result.get("success"):
            return service_result

        try:
            response = (
                service_result["service"]
                .events()
                .list(
                    calendarId=calendar_id,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                    timeMin=datetime.utcnow().isoformat() + "Z"
                )
                .execute()
            )

            events = []

            for event in response.get("items", []):
                events.append({
                    "id": event.get("id"),
                    "title": event.get("summary"),
                    "description": event.get(
                        "description",
                        ""
                    ),
                    "start": event.get("start"),
                    "end": event.get("end"),
                    "status": event.get("status"),
                    "html_link": event.get("htmlLink")
                })

            return {
                "success": True,
                "status": "retrieved",
                "action": "list",
                "events": events,
                "count": len(events),
                "message": (
                    "Google Calendar events retrieved successfully."
                )
            }

        except HttpError as error:
            return {
                "success": False,
                "message": (
                    "Google Calendar event listing failed.",
                    str(error)
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": (
                    "Failed to retrieve Google Calendar events.",
                    str(error)
                )
            }

    def get_event(
        self,
        user_id: int,
        event_id: str,
        calendar_id: str = "primary"
    ) -> dict:
        """
        Get one Google Calendar event by ID.
        """

        success, validated_user_id, error = self._validate_user_id(
            user_id
        )

        if not success:
            return {
                "success": False,
                "message": error
            }

        if not isinstance(event_id, str) or not event_id.strip():
            return {
                "success": False,
                "message": "Event ID is required."
            }

        service_result = self._build_service(
            user_id=validated_user_id
        )

        if not service_result.get("success"):
            return service_result

        try:
            event = (
                service_result["service"]
                .events()
                .get(
                    calendarId=calendar_id,
                    eventId=event_id.strip()
                )
                .execute()
            )

            return {
                "success": True,
                "event": {
                    "id": event.get("id"),
                    "title": event.get("summary"),
                    "description": event.get(
                        "description",
                        ""
                    ),
                    "start": event.get("start"),
                    "end": event.get("end"),
                    "status": event.get("status"),
                    "html_link": event.get("htmlLink")
                },
                "message": (
                    "Google Calendar event retrieved successfully."
                )
            }

        except HttpError as error:
            return {
                "success": False,
                "message": (
                    "Google Calendar event retrieval failed.",
                    str(error)
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": (
                    "Failed to retrieve Google Calendar event.",
                    str(error)
                )
            }

    def delete_event(
        self,
        user_id: int,
        event_id: str,
        calendar_id: str = "primary"
    ) -> dict:
        """
        Delete a Google Calendar event.
        """

        success, validated_user_id, error = self._validate_user_id(
            user_id
        )

        if not success:
            return {
                "success": False,
                "message": error
            }

        if not isinstance(event_id, str) or not event_id.strip():
            return {
                "success": False,
                "message": "Event ID is required."
            }

        service_result = self._build_service(
            user_id=validated_user_id
        )

        if not service_result.get("success"):
            return service_result

        try:
            (
                service_result["service"]
                .events()
                .delete(
                    calendarId=calendar_id,
                    eventId=event_id.strip()
                )
                .execute()
            )

            return {
                "success": True,
                "status": "deleted",
                "action": "delete",
                "event_id": event_id.strip(),
                "message": (
                    "Google Calendar event deleted successfully."
                )
            }

        except HttpError as error:
            return {
                "success": False,
                "message": (
                    "Google Calendar event deletion failed.",
                    str(error)
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": (
                    "Failed to delete Google Calendar event.",
                    str(error)
                )
            }

    def get_status(self) -> dict:
        """
        Return service configuration status.
        """

        return {
            "service": "google_calendar",
            "provider": "google_calendar",
            "api": "Google Calendar API v3",
            "token_storage": "database",
            "encrypted_tokens": True,
            "status": "ready"
        }

