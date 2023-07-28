from datetime import date
from typing import List

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import (CannotBookHotelForLongPeriod,
                            DateFromCannotBeAfterDateTo)
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.schemas import SHotel

router = APIRouter(prefix="/hotels",
                   tags=["Отели"])


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date,
    date_to: date,
) -> List[SHotel]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod 
    
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/{hotel_id}/rooms")
@cache(expire=20)
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> List[SRoomInfo]:
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    return rooms