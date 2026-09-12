from fastapi import APIRouter

from app.integrations.email.provider import EmailProvider
from app.integrations.calendar.provider import CalendarProvider
from app.integrations.cloud_storage.provider import CloudStorageProvider
from app.integrations.education.provider import EducationProvider
from app.integrations.booking.provider import BookingProvider
from app.integrations.shopping.provider import ShoppingProvider
from app.integrations.social.provider import SocialProvider


router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"]
)


providers = {
    "email": EmailProvider(),
    "calendar": CalendarProvider(),
    "cloud_storage": CloudStorageProvider(),
    "education": EducationProvider(),
    "booking": BookingProvider(),
    "shopping": ShoppingProvider(),
    "social": SocialProvider()
}


@router.get("/status")
def integration_status():

    return {
        "success": True,
        "service": "integrations",
        "status": "ready",
        "providers": {
            name: provider.get_status()
            for name, provider in providers.items()
        }
    }


@router.get("/")
def get_integrations():

    return {
        "success": True,
        "integrations": [
            provider.get_status()
            for provider in providers.values()
        ]
    }


@router.get("/{provider_name}")
def get_integration(provider_name: str):

    provider = providers.get(
        provider_name
    )

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