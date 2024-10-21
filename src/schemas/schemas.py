from pydantic import BaseModel, Field
from datetime import date


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



