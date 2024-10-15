from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


# Создаем движок асинхронной базы данных
engine = create_async_engine(
    # URL состоит из названия БД, драйвера и названия файла/адрес
    "sqlite+aiosqlite:///tasks.db"
)

# Фабрика открытия сессий (открытие транзакций для работы с БД)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class TaskORM(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]


async def create_tables():
    # Async function for table creation
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    # Async function for table termination
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
