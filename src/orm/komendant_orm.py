from src.database import async_session_factory
from src.models.base_model import OccupantModel, RoomModel, PaymentModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from datetime import date
from sqlalchemy.orm import selectinload, joinedload
from src.schemas.schemas import OccupantGetDTO
import asyncio

async def add_occupant(surname, name, patronymic, photo, phone_number, birth_date=date(2001, 9, 12),
                       check_in_date=date(2023, 8, 31)):
    async with async_session_factory() as session:
        occupant = OccupantModel(surname=surname, name=name, patronymic=patronymic, photo=photo, phone_number=phone_number,
                                 birth_date=birth_date, check_in_date=check_in_date)
        session.add(occupant)
        await session.commit()


async def select_all_occupant():
    async with async_session_factory() as session:
        stmt = (
            select(OccupantModel).options(joinedload(OccupantModel.room)).options(selectinload(OccupantModel.payments))

        )
        res = await session.execute(stmt)
        result_table = res.scalars().all()
        result_dto = [OccupantGetDTO.model_validate(row, from_attributes=True) for row in result_table]
        return result_dto
async def get_occupant(id: int):
    async with (async_session_factory() as session):
        stmt = (
            select(OccupantModel).options(joinedload(OccupantModel.room)).options(selectinload(OccupantModel.payments))
            .filter_by(id=id)
        )
        res_orm = await session.execute(stmt)
        res_dto = OccupantGetDTO.model_validate(res_orm.scalars().one_or_none(), from_attributes=True)
        return res_dto
# asyncio.run(get_occupant(1))




