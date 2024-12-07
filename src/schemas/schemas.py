from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class PaymentDTO(BaseModel):
    payment_date: date
    number_of_month_paid: int

class RoomDTO(BaseModel):
    number: int

class OccupantPostDTO(BaseModel):
    surname: str
    name: str
    patronymic: str
    photo: str
    phone_number: str
    birth_date: date
    check_in_date: date
    payments: list["PaymentDTO"] | None = None
    room: RoomDTO | None

class OccupantGetDTO(OccupantPostDTO):
    id: int
class FloorPostDTO(BaseModel):
    number: int
class RoomTypePostDTO(BaseModel):
    max_occupants: int
    area: int
class RoomPostDTO(BaseModel):
    number: int
    floor: FloorPostDTO
    room_type: RoomTypePostDTO
class FurniturePostDTO(BaseModel):
    name: str
    description: str
    cost: int
    room: Optional[RoomPostDTO]

