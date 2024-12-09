from pydantic import BaseModel

class PositionAtWorkPostDTO(BaseModel):
    position: str
    salary: int

class PositionAtWorkGetDTO(PositionAtWorkPostDTO):
    id: int
class WorkerPostDTO(BaseModel):
    surname: str
    name: str
    patronymic: str
    phone_number: str
    position_at_work: PositionAtWorkGetDTO

class WorkerGetDTO(WorkerPostDTO):
    id: int