from src.database import async_session_factory
from src.models.base_model import OccupantModel, RoomModel, PaymentModel, FurnitureModel, RoomTypeModel
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload, joinedload
from datetime import date
from sqlalchemy.orm import selectinload, joinedload
from src.schemas.komendant_schemas import OccupantGetDTO, RoomTypePostDTO, RoomPostDTO, FloorPostDTO, FurniturePostDTO, FurnitureGetDTO
import asyncio

async def add_occupant(surname, name, patronymic, phone_number, room, birth_date=date(2001, 9, 12),
                       check_in_date=date(2023, 8, 31),  payments=None):
    async with async_session_factory() as session:
        room = await session.get(RoomModel, room["number"])
        occupant = OccupantModel(surname=surname, name=name, patronymic=patronymic, phone_number=phone_number,
                                 birth_date=birth_date, check_in_date=check_in_date, room=room)
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
    async with async_session_factory() as session:
        stmt = (
            select(OccupantModel).options(joinedload(OccupantModel.room)).options(selectinload(OccupantModel.payments))
            .filter_by(id=id)
        )
        res_orm = await session.execute(stmt)
        res_dto = OccupantGetDTO.model_validate(res_orm.scalars().one_or_none(), from_attributes=True)
        return res_dto


async def update_occupant(id: int, surname, name, patronymic, phone_number, room, birth_date=date(2001, 9, 12),
                       check_in_date=date(2023, 8, 31), payments=None):
    async with async_session_factory() as session:
        stmt = (
            select(OccupantModel).options(joinedload(OccupantModel.room)).options(selectinload(OccupantModel.payments)).filter_by(id=id)

        )
        room = await session.get(RoomModel, room["number"])
        res_orm = await session.execute(stmt)
        occupant = res_orm.scalars().first()
        occupant.surname = surname
        occupant.name = name
        occupant.patronymic = patronymic
        occupant.phone_number = phone_number
        occupant.birth_date = birth_date
        occupant.check_in_date = check_in_date
        occupant.payments = payments if payments is not None else []
        occupant.room = room if room is not None else None
        await session.commit()
# Получение всех комнат
async def select_rooms():
    async with async_session_factory() as session:
        stmt = (
            select(RoomModel)
            .options(
                joinedload(RoomModel.room_type),  # Жадная загрузка room_type
                selectinload(RoomModel.occupants),  # Оптимизированная загрузка occupants
                selectinload(RoomModel.furniture),  # Оптимизированная загрузка furniture
                joinedload(RoomModel.floor)  # Жадная загрузка floor
            )
        )
        res_orm = await session.execute(stmt)
        res_table = res_orm.scalars().all()
        res_dto = [RoomPostDTO.model_validate(row, from_attributes=True) for row in res_table]
        return res_dto
async def select_furniture():
    async with async_session_factory() as session:
        stmt = (
            select(FurnitureModel).options(joinedload(FurnitureModel.room))
        )
        res_orm = await session.execute(stmt)
        res_table = res_orm.scalars().all()
        res_dto = [FurnitureGetDTO.model_validate(row, from_attributes=True) for row in res_table]
        return res_dto
async def select_furniture_by_id(id: int):
    async with async_session_factory() as session:
        res_orm = await session.execute(
            select(FurnitureModel).options(joinedload(FurnitureModel.room)).filter_by(id=id)
        )
        res_dto = FurnitureGetDTO.model_validate(res_orm.scalars().one_or_none(), from_attributes=True)
        return res_dto
async def update_furniture_description_and_room(id: int, description, room, name, cost):
    async with async_session_factory() as session:
        furniture = await session.get(FurnitureModel, id)
        room = await session.get(RoomModel, room["number"])
        furniture.description = description
        furniture.room = room
        await session.commit()

async def select_free_rooms():
    async with async_session_factory() as session:
        result = await session.execute(text("""
        select rooms.id, rooms.number from rooms join room_types on room_types.id = rooms.room_type_id left join occupants on
        occupants.room_id = rooms.id
        group by rooms.id, rooms.number, room_types.max_occupants
        having count(occupants.id) < room_types.max_occupants
        order by rooms.number"""))
        result = [list(row) for row in result.fetchall()]
        return result

# asyncio.run(select_free_rooms())




