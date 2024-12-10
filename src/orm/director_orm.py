from src.database import async_session_factory
from sqlalchemy import select, delete
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
async def delete_worker(id: int):
    async with async_session_factory() as session:
        await session.execute(
            delete(WorkerModel).filter(WorkerModel.id == id)
        )
        await session.commit()
async def get_worker(id: int):
    async with async_session_factory() as session:
        res_orm = await session.execute(
            select(WorkerModel).options(joinedload(WorkerModel.position_at_work)).filter(WorkerModel.id == id)
        )
        res_scalars = res_orm.scalars().first()
        return WorkerGetDTO.model_validate(res_scalars, from_attributes=True)
async def update_worker(id: int, worker: WorkerPostDTO):
    async with async_session_factory() as session:
        worker_orm = await session.get(WorkerModel, id)
        worker_orm.position_at_work = await session.get(PositionAtWorkModel, worker.position_at_work.id)
        worker_orm.surname = worker.surname
        worker_orm.name = worker.name
        worker_orm.patronymic = worker.patronymic
        worker_orm.phone_number = worker.phone_number
        await session.commit()

async def update_position_at_work(id: int, salary: int):
    async with async_session_factory() as session:
        position_at_work = await session.get(PositionAtWorkModel, id)
        position_at_work.salary = salary
        await session.commit()
