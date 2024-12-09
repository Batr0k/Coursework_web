from src.database import async_session_factory
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from src.models.base_model import WorkerModel, PositionAtWorkModel
from src.schemas.director_schemas import PositionAtWorkPostDTO, PositionAtWorkGetDTO, WorkerPostDTO, WorkerGetDTO

async def select_workers():
    async with async_session_factory() as session:
        res_orm = await session.execute(
            select(WorkerModel).options(joinedload(WorkerModel.position_at_work))
        )
        res_list = res_orm.scalars().all()
        res_dto = [WorkerGetDTO.model_validate(i, from_attributes=True) for i in res_list]
        return res_dto
async def select_position_at_work():
    async with async_session_factory() as session:
        res_orm = await session.execute(
            select(PositionAtWorkModel)
        )
        res_list = res_orm.scalars().all()
        res_dto = [PositionAtWorkGetDTO.model_validate(i, from_attributes=True) for i in res_list]
        return res_dto
async def insert_worker(worker: WorkerPostDTO):
    async with async_session_factory() as session:
        position = await session.get(PositionAtWorkModel, worker.position_at_work.id)
        session.add(WorkerModel(name=worker.name, surname=worker.surname, patronymic=worker.patronymic, position_at_work=position, phone_number=worker.phone_number))
        await session.commit()
