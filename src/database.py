from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

async_engine = create_async_engine(url=settings.async_refer_to_db(), echo=True)
async_session_factory = async_sessionmaker(async_engine)
