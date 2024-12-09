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
        res_dto = [PositionAtWorkGetDTO.model_validate(i, from_attributes=True) for i in res_list]
        return res_dto
