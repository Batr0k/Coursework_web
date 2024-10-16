from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

async_engine = create_async_engine(settings.async_refer_to_db(), echo=True)
async_session = async_sessionmaker(async_engine)
