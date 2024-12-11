from pydantic import BaseModel

class UserDTO(BaseModel):
    login: str
    password: str