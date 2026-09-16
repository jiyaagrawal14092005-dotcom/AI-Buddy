from fastapi import APIRouter

from app.integrations.booking.provider import BookingProvider


router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

booking_provider = BookingProvider()


@router.get("/status")
def booking_status():
    return {
        "success": True,
        "service": "booking",
        "provider": booking_provider.get_status()
    }


@router.post("/connect")
def connect_booking():
    return booking_provider.connect()


@router.post("/disconnect")
def disconnect_booking():
    return booking_provider.disconnect()


@router.post("/create")
def create_booking(
    user_id: int,
    service: str,
    date: str,
    time: str,
    details: str = ""
):
    return booking_provider.execute(
        action="create",
        parameters={
            "user_id": user_id,
            "service": service,
            "date": date,
            "time": time,
            "details": details
        }
    )


@router.get("/list")
def list_bookings(
    user_id: int
):
    return booking_provider.execute(
        action="list",
        parameters={
            "user_id": user_id
        }
    )


@router.get("/{booking_id}")
def get_booking(
    booking_id: str,
    user_id: int
):
    return booking_provider.execute(
        action="get",
        parameters={
            "user_id": user_id,
            "booking_id": booking_id
        }
    )


@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: str,
    user_id: int
):
    return booking_provider.execute(
        action="cancel",
        parameters={
            "user_id": user_id,
            "booking_id": booking_id
        }
    )