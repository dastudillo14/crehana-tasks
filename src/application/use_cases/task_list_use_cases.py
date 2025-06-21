from datetime import datetime
from typing import List, Optional
from ...domain.entities.task_list import TaskList
from ...domain.repositories.task_list_repository import TaskListRepository
from ...domain.repositories.task_repository import TaskRepository
from ..dtos.task_list_dtos import (
    CreateTaskListRequest, UpdateTaskListRequest, TaskListResponse
)


class TaskListUseCases:
    def __init__(self, task_list_repo: TaskListRepository, task_repo: TaskRepository):
        self.task_list_repo = task_list_repo
        self.task_repo = task_repo

    async def create_task_list(self, request: CreateTaskListRequest) -> TaskListResponse:
        """Create a new task list"""
        task_list = TaskList(
            title=request.title,
            description=request.description,
            created_at=datetime.utcnow()
        )
        
        created_task_list = await self.task_list_repo.create(task_list)
        
        return TaskListResponse(
            id=created_task_list.id,
            title=created_task_list.title,
            description=created_task_list.description,
            completion_percentage=created_task_list.completion_percentage,
            total_tasks=created_task_list.total_tasks,
            completed_tasks=created_task_list.completed_tasks,
            created_at=created_task_list.created_at,
            updated_at=created_task_list.updated_at
        )

    async def get_task_list(self, task_list_id: int) -> Optional[TaskListResponse]:
        """Get a task list by ID"""
        task_list = await self.task_list_repo.get_by_id(task_list_id)
        if not task_list:
            return None
        
        # Get tasks for this list
        tasks = await self.task_repo.get_by_task_list_id(task_list_id)
        task_list.tasks = tasks
        
        return TaskListResponse(
            id=task_list.id,
            title=task_list.title,
            description=task_list.description,
            completion_percentage=task_list.completion_percentage,
            total_tasks=task_list.total_tasks,
            completed_tasks=task_list.completed_tasks,
            created_at=task_list.created_at,
            updated_at=task_list.updated_at
        )

    async def get_all_task_lists(self) -> List[TaskListResponse]:
        """Get all task lists"""
        task_lists = await self.task_list_repo.get_all()
        
        result = []
        for task_list in task_lists:
            # Get tasks for each list
            tasks = await self.task_repo.get_by_task_list_id(task_list.id)
            task_list.tasks = tasks
            
            result.append(TaskListResponse(
                id=task_list.id,
                title=task_list.title,
                description=task_list.description,
                completion_percentage=task_list.completion_percentage,
                total_tasks=task_list.total_tasks,
                completed_tasks=task_list.completed_tasks,
                created_at=task_list.created_at,
                updated_at=task_list.updated_at
            ))
        
        return result

    async def update_task_list(self, task_list_id: int, request: UpdateTaskListRequest) -> Optional[TaskListResponse]:
        """Update a task list"""
        task_list = await self.task_list_repo.get_by_id(task_list_id)
        if not task_list:
            return None
        
        # Update fields if provided
        if request.title is not None:
            task_list.title = request.title
        if request.description is not None:
            task_list.description = request.description
        
        task_list.updated_at = datetime.utcnow()
        
        updated_task_list = await self.task_list_repo.update(task_list)
        
        # Get tasks for this list
        tasks = await self.task_repo.get_by_task_list_id(task_list_id)
        updated_task_list.tasks = tasks
        
        return TaskListResponse(
            id=updated_task_list.id,
            title=updated_task_list.title,
            description=updated_task_list.description,
            completion_percentage=updated_task_list.completion_percentage,
            total_tasks=updated_task_list.total_tasks,
            completed_tasks=updated_task_list.completed_tasks,
            created_at=updated_task_list.created_at,
            updated_at=updated_task_list.updated_at
        )

    async def delete_task_list(self, task_list_id: int) -> bool:
        """Delete a task list and all its tasks"""
        # First delete all tasks in the list
        await self.task_repo.delete_by_task_list_id(task_list_id)
        
        # Then delete the task list
        return await self.task_list_repo.delete(task_list_id) 