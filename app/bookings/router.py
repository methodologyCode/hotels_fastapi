from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.users.models import Users
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user)
    ) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", status_code=201)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id,
                                   booking.room_id,
                                   booking.date_from,
                                   booking.date_to)
    if not booking:
        raise RoomCannotBeBooked
    
    booking = parse_obj_as(SNewBooking, booking).dict()
    return booking


@router.delete("/{booking_id}")
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)