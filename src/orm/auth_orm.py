import hashlib
from src.database import async_session_factory
from sqlalchemy import select
from src.schemas.auth_schemas import UserDTO
from src.models.base_model import UserModel
def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
async def find_user(login: str):
    async with async_session_factory() as session:
        res = await session.execute(
            select(UserModel).filter(UserModel.login == login)
        )
        user = res.scalars().first()
        if user is None:
            return None
        user_dto = UserDTO.model_validate(user, from_attributes=True)
        return user_dto