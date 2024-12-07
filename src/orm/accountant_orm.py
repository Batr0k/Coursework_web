from src.database import async_session_factory
from src.models.base_model import PaymentModel, CostPerMonthModel, OccupantModel, RoomModel, RoomTypeModel
from sqlalchemy import select, text
from datetime import date
from sqlalchemy.orm import selectinload, joinedload
from src.schemas.accountant_shemas import PaymentGetDTO, CostPerMonthGetDTO, OccupantGetDTO
async def select_payments():
    async with async_session_factory() as session:
        res_orm = await session.execute(
            select(PaymentModel).options(joinedload(PaymentModel.occupant)).options(joinedload(PaymentModel.cost_per_month).joinedload(CostPerMonthModel.room_type))
        )
        res_list = res_orm.scalars().all()
        res_dto = [PaymentGetDTO.model_validate(i, from_attributes=True) for i in res_list]
        return res_dto
async def select_cost_per_month():
    async with async_session_factory() as session:
        res_orm = await session.execute(
            select(CostPerMonthModel).options(joinedload(CostPerMonthModel.room_type))
        )
        res_list = res_orm.scalars().all()
        res_dto = [CostPerMonthGetDTO.model_validate(i, from_attributes=True) for i in res_list]
        return res_dto
async def select_occupants():
    async with async_session_factory() as session:
        res_orm = await session.execute(
            select(OccupantModel)
        )
        res_list = res_orm.scalars().all()
        res_dto = [OccupantGetDTO.model_validate(i, from_attributes=True) for i in res_list]
        return res_dto


async def insert_payment(occupant_id: int, number_of_month_paid: int, payment_date: date):
    async with async_session_factory() as session:
        occupant = await session.get(OccupantModel, occupant_id)
        result = await session.execute(
            select(CostPerMonthModel)
            .join(RoomTypeModel, RoomTypeModel.id == CostPerMonthModel.room_type_id)
            .join(RoomModel, RoomModel.room_type_id == RoomTypeModel.id)
            .join(OccupantModel, OccupantModel.room_id == RoomModel.id)
            .where(OccupantModel.id == occupant_id)
            .where(CostPerMonthModel.price_date <= payment_date)  # Условие по дате
            .order_by(CostPerMonthModel.price_date.desc())  # Сортируем по дате, чтобы выбрать самую новую
            .options(selectinload(CostPerMonthModel.room_type))
            .limit(1)  # Ограничиваем результат одной записью
        )
        cost_per_month = result.scalars().first()
        session.add(PaymentModel(payment_date=payment_date, number_of_month_paid=number_of_month_paid, occupant=occupant, cost_per_month=cost_per_month))
        await session.commit()