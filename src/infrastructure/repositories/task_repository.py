from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from ...domain.entities.task import Task, TaskStatus, TaskPriority
from ...domain.repositories.task_repository import TaskRepository
from ..models.task_model import TaskModel


def _map_to_entity(db_task: TaskModel) -> Task:
    """Maps a TaskModel object to a Task domain entity."""
    return Task(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        status=db_task.status,
        percentage=db_task.percentage,
        priority=db_task.priority,
        task_list_id=db_task.task_list_id,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        """Initializes the repository with a database session."""
        self.session = session

    async def create(self, task: Task) -> Task:
        """Creates a new task in the database."""
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            status=task.status,
            percentage=task.percentage,
            priority=task.priority,
            task_list_id=task.task_list_id,
            created_at=task.created_at
        )
        
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        
        return _map_to_entity(db_task)

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Gets a task by its ID."""
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        result = await self.session.execute(stmt)
        db_task = result.scalar_one_or_none()
        
        return _map_to_entity(db_task) if db_task else None

    async def get_by_task_list_id(self, task_list_id: int) -> List[Task]:
        """Gets all tasks associated with a task list."""
        stmt = select(TaskModel).where(TaskModel.task_list_id == task_list_id)
        result = await self.session.execute(stmt)
        db_tasks = result.scalars().all()
        
        return [_map_to_entity(db_task) for db_task in db_tasks]

    async def get_filtered_tasks(
        self,
        task_list_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
    ) -> List[Task]:
        """Gets tasks filtered by status and/or priority."""
        stmt = select(TaskModel).where(TaskModel.task_list_id == task_list_id)
        
        if status:
            stmt = stmt.where(TaskModel.status == status)
        if priority:
            stmt = stmt.where(TaskModel.priority == priority)
        
        result = await self.session.execute(stmt)
        db_tasks = result.scalars().all()
        
        return [_map_to_entity(db_task) for db_task in db_tasks]

    async def update(self, task: Task) -> Task:
        """Updates an existing task."""
        stmt = (
            update(TaskModel)
            .where(TaskModel.id == task.id)
            .values(
                title=task.title,
                description=task.description,
                status=task.status,
                percentage=task.percentage,
                priority=task.priority,
                updated_at=task.updated_at
            )
        )
        
        await self.session.execute(stmt)
        await self.session.commit()
        
        return task

    async def update_status(self, task_id: int, status: TaskStatus) -> Task:
        """Updates the status of a task."""
        stmt = (
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(
                status=status,
                updated_at=datetime.utcnow()
            )
        )
        
        await self.session.execute(stmt)
        await self.session.commit()
        
        # Get the updated task
        updated_task = await self.get_by_id(task_id)
        if not updated_task:
            # This case should ideally not be reached if the update was successful
            # and the task existed. But as a safeguard:
            raise RuntimeError(f"Task with id {task_id} not found after update.")
        return updated_task

    async def delete(self, task_id: int) -> bool:
        """Deletes a task by its ID."""
        stmt = delete(TaskModel).where(TaskModel.id == task_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        return result.rowcount > 0

    async def delete_by_task_list_id(self, task_list_id: int) -> bool:
        """Deletes all tasks associated with a task list."""
        stmt = delete(TaskModel).where(TaskModel.task_list_id == task_list_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        return result.rowcount > 0 