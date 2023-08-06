from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from config.env import DB_LOGIN, DB_PORT, DB_NAME, DB_PASS, DB_HOST

DATABASE_URL = f"postgresql+asyncpg://{DB_LOGIN}:{DB_PASS}@{DB_HOST}" \
               f":{DB_PORT}/{DB_NAME}"

Base = declarative_base()

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)
