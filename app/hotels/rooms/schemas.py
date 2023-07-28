from typing import List, Optional

from pydantic import BaseModel


class SRoomInfo(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    services: List[str]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int

    class Config:
        orm_mode = True