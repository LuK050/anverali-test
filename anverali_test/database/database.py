import os

import dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

dotenv.load_dotenv()
_user: str = os.getenv("POSTGRES_USER")
_password: str = os.getenv("POSTGRES_PASSWORD")
_host: str = os.getenv("POSTGRES_HOST")
_db: str = os.getenv("POSTGRES_DB")
_port: str = os.getenv("POSTGRES_PORT")

engine = create_async_engine(
    f"postgresql+asyncpg://{_user}:{_password}@{_host}:{_port}/{_db}"
)

AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


async def init_models() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
