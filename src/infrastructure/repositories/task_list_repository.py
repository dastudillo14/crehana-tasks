from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from ...domain.entities.task_list import TaskList
from ...domain.repositories.task_list_repository import TaskListRepository
from ..models.task_list_model import TaskListModel


class SQLAlchemyTaskListRepository(TaskListRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_list: TaskList) -> TaskList:
        db_task_list = TaskListModel(
            title=task_list.title,
            description=task_list.description,
            created_at=task_list.created_at
        )
        
        self.session.add(db_task_list)
        await self.session.commit()
        await self.session.refresh(db_task_list)
        
        return TaskList(
            id=db_task_list.id,
            title=db_task_list.title,
            description=db_task_list.description,
            created_at=db_task_list.created_at,
            updated_at=db_task_list.updated_at
        )

    async def get_by_id(self, task_list_id: int) -> Optional[TaskList]:
        stmt = select(TaskListModel).where(TaskListModel.id == task_list_id)
        result = await self.session.execute(stmt)
        db_task_list = result.scalar_one_or_none()
        
        if not db_task_list:
            return None
        
        return TaskList(
            id=db_task_list.id,
            title=db_task_list.title,
            description=db_task_list.description,
            created_at=db_task_list.created_at,
            updated_at=db_task_list.updated_at
        )

    async def get_all(self) -> List[TaskList]:
        stmt = select(TaskListModel)
        result = await self.session.execute(stmt)
        db_task_lists = result.scalars().all()
        
        return [
            TaskList(
                id=db_task_list.id,
                title=db_task_list.title,
                description=db_task_list.description,
                created_at=db_task_list.created_at,
                updated_at=db_task_list.updated_at
            )
            for db_task_list in db_task_lists
        ]

    async def update(self, task_list: TaskList) -> TaskList:
        stmt = (
            update(TaskListModel)
            .where(TaskListModel.id == task_list.id)
            .values(
                title=task_list.title,
                description=task_list.description,
                updated_at=task_list.updated_at
            )
        )
        
        await self.session.execute(stmt)
        await self.session.commit()
        
        return task_list

    async def delete(self, task_list_id: int) -> bool:
        stmt = delete(TaskListModel).where(TaskListModel.id == task_list_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        return result.rowcount > 0 