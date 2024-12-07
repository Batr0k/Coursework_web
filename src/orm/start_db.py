import datetime
from sqlalchemy import select
from src.models.base_model import Base
from src.database import async_engine
import asyncio
from src.database import async_session_factory
from src.models.base_model import (FloorModel, RoomTypeModel, CostPerMonthModel, RoomModel, FurnitureModel, PaymentModel,
                                   OccupantModel)
async def reload_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await insert_floors()
    await insert_room_type()
    await insert_cost_per_month()
    await insert_rooms()
    await insert_furniture()
    await insert_occupants()

async def insert_occupants():
    async with async_session_factory() as session:
        rooms = await session.execute(
            select(RoomModel).filter(RoomModel.id.in_([1,2,3,4]))
        )
        rooms = rooms.scalars().all()
        occupants = [
            OccupantModel(surname="Иванов", name="Иван", patronymic="Иванович", phone_number="88005553535",
                                 birth_date=datetime.date(1990, 6, 7),
                          check_in_date=datetime.date(2023, 11, 9), room=rooms[0]),
            OccupantModel(surname="Иванов", name="Иван", patronymic="Иванович", phone_number="88005553535",
                          birth_date=datetime.date(1990, 6, 7),
                          check_in_date=datetime.date(2023, 11, 9), room=rooms[1]),
            OccupantModel(surname="Иванов", name="Иван", patronymic="Иванович", phone_number="88005553535",
                          birth_date=datetime.date(1990, 6, 7),
                          check_in_date=datetime.date(2023, 11, 9), room=rooms[2]),
            OccupantModel(surname="Иванов", name="Иван", patronymic="Иванович", phone_number="88005553535",
                          birth_date=datetime.date(1990, 6, 7),
                          check_in_date=datetime.date(2023, 11, 9), room=rooms[3]),
        ]
        session.add_all(occupants)
        await session.commit()


async def insert_floors():
    async with async_session_factory() as session:
        floors = [FloorModel(number=i) for i in range(1, 17)]
        session.add_all(floors)
        await session.commit()
async def insert_room_type():
    async with async_session_factory() as session:
        roomTypes = [
            RoomTypeModel(max_occupants=1, area=9),
            RoomTypeModel(max_occupants=2, area=12),
            RoomTypeModel(max_occupants=3, area=18)
        ]
        session.add_all(roomTypes)
        await session.commit()
async def insert_cost_per_month():
    async with async_session_factory() as session:
        stmt = select(RoomTypeModel).order_by(RoomTypeModel.max_occupants)
        res_iter = await session.execute(stmt)
        res_orm = res_iter.scalars().all()
        costPerMonthList = [
            CostPerMonthModel(price_date=datetime.date(2024, 1,1), price=5000, room_type=res_orm[0]),
            CostPerMonthModel(price_date=datetime.date(2023, 1, 1), price=4000, room_type=res_orm[0]),
            CostPerMonthModel(price_date=datetime.date(2022, 1, 1), price=3000, room_type=res_orm[0]),
            CostPerMonthModel(price_date=datetime.date(2024, 1, 1), price=4000, room_type=res_orm[1]),
            CostPerMonthModel(price_date=datetime.date(2023, 1, 1), price=3000, room_type=res_orm[1]),
            CostPerMonthModel(price_date=datetime.date(2022, 1, 1), price=2000, room_type=res_orm[1]),
            CostPerMonthModel(price_date=datetime.date(2024, 1, 1), price=2000, room_type=res_orm[2]),
            CostPerMonthModel(price_date=datetime.date(2023, 1, 1), price=1500, room_type=res_orm[2]),
            CostPerMonthModel(price_date=datetime.date(2022, 1, 1), price=1000, room_type=res_orm[2]),
        ]
        session.add_all(costPerMonthList)
        await session.commit()
async def insert_rooms():
    async with async_session_factory() as session:
        stmt = select(FloorModel).order_by(FloorModel.number)
        res_iter = await session.execute(stmt)
        floor_list = res_iter.scalars().all()
        stmt = select(RoomTypeModel).order_by(RoomTypeModel.max_occupants)
        res_iter = await session.execute(stmt)
        room_type_list = res_iter.scalars().all()
        room_list = []
        room_count = 1
        for i in range(16):
            for j in range(10):
                room_list.append(RoomModel(number=room_count, floor=floor_list[i], room_type=room_type_list[j % 3]))
                room_count += 1
        session.add_all(room_list)
        await session.commit()
async def insert_payment():
    async with async_session_factory() as session:
        session.add(PaymentModel(payment_date=datetime.date(2024, 4,1), number_of_month_paid=2, occupant_id=1))
        await session.commit()

async def insert_furniture():
    async with async_session_factory() as session:
        rooms = [1, 2, 3, 4, 5, 6]
        result = await session.execute(
            select(RoomModel).filter(RoomModel.id.in_(rooms))
        )
        rooms_orm = result.scalars().all()
        furniture = [
            FurnitureModel(name="Шкаф IKEA", description="В идеальном состоянии", cost=23000, room=rooms_orm[0]),
            FurnitureModel(name="Шкаф Woods", description="В идеальном состоянии", cost=4000, room=rooms_orm[1]),
            FurnitureModel(name="Тумбочка IKEA", description="В идеальном состоянии", cost=10000, room=rooms_orm[2]),
            FurnitureModel(name="Тумбочка Woods", description="В идеальном состоянии", cost=10000, room=rooms_orm[3]),
            FurnitureModel(name="Холодильник Polis", description="В идеальном состоянии", cost=7000, room=rooms_orm[4]),
            FurnitureModel(name="Холодильник Cold", description="В идеальном состоянии", cost=17000, room=rooms_orm[5]),
        ]
        session.add_all(furniture)
        await session.commit()
asyncio.run(reload_db())


