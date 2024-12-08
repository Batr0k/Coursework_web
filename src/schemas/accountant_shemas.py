from pydantic import BaseModel
from datetime import date
from typing import Optional
class RoomTypePostDTO(BaseModel):
    max_occupants: int
    area: int
class RoomTypeGetDTO(RoomTypePostDTO):
    id: int
class OccupantPostDTO(BaseModel):
    name: str
    surname: str
    patronymic: str
    check_in_date: date
class OccupantGetDTO(OccupantPostDTO):
    id: int
class CostPerMonthPostDTO(BaseModel):
    price_date: date
    price: int
    room_type: RoomTypeGetDTO
class FurniturePostDTO(BaseModel):
    name: str
    description: str
    cost: int
class FurnitureGetDTO(FurniturePostDTO):
    id: int
class CostPerMonthGetDTO(CostPerMonthPostDTO):
    id: int
class PaymentPostDTO(BaseModel):
    payment_date: date
    number_of_month_paid: int
    cost_per_month: CostPerMonthGetDTO
    occupant: OccupantGetDTO

class PaymentGetDTO(PaymentPostDTO):
    id: int