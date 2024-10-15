# Реализуем паттерн Репозиторий,
# который позволяется работать с базой как с коллекцией объектов
from sqlalchemy import select

from database import new_session, TaskORM
from schemas import STask, STaskAdd


class TaskRepository:
    # TODO Паттерн UnitOfWork
    @classmethod
    async def add_one(cls, data: STaskAdd):
        async with new_session() as session:
            task_dict = data.model_dump()  # Приводим модель к словарю

            task = TaskORM(**task_dict)  # Новая строчка
            session.add(task)  # Добавляем объект в сессию (работа с транзакциями)
            await session.flush()  # Отправит изменения в базу и получит id
            await session.commit()  # Зафиксировали изменения
            return task.id

    @classmethod
    async def add_many(cls):
        pass

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskORM)  # Делаем запрос
            result = await session.execute(query)  # Обращаемся к таблице через сессию
            task_models = result.scalars().all()  # Получили все объекты базы данных
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]

            return task_schemas

