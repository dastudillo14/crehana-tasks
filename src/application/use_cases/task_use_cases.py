from datetime import datetime
from typing import List, Optional
from ...domain.entities.task import Task, TaskStatus, TaskPriority
from ...domain.repositories.task_repository import TaskRepository
from ...domain.repositories.task_list_repository import TaskListRepository
from ..dtos.task_dtos import (
    CreateTaskRequest, UpdateTaskRequest, UpdateTaskStatusRequest, TaskResponse, TaskFilterRequest
)
from ..dtos.task_list_dtos import TaskListWithFilteredTasksResponse


class TaskUseCases:
    def __init__(self, task_repo: TaskRepository, task_list_repo: TaskListRepository):
        self.task_repo = task_repo
        self.task_list_repo = task_list_repo

    async def create_task(self, task_list_id: int, request: CreateTaskRequest) -> Optional[TaskResponse]:
        """Create a new task in a task list"""
        # Verify task list exists
        task_list = await self.task_list_repo.get_by_id(task_list_id)
        if not task_list:
            return None
        
        task = Task(
            title=request.title,
            description=request.description,
            priority=request.priority,
            percentage=request.percentage,
            task_list_id=task_list_id,
            created_at=datetime.utcnow()
        )
        
        created_task = await self.task_repo.create(task)
        
        return TaskResponse(
            id=created_task.id,
            title=created_task.title,
            description=created_task.description,
            status=created_task.status,
            percentage=created_task.percentage,
            priority=created_task.priority,
            task_list_id=created_task.task_list_id,
            created_at=created_task.created_at,
            updated_at=created_task.updated_at
        )

    async def get_task(self, task_id: int) -> Optional[TaskResponse]:
        """Get a task by ID"""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            percentage=task.percentage,
            priority=task.priority,
            task_list_id=task.task_list_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    async def get_tasks_by_list(self, task_list_id: int) -> List[TaskResponse]:
        """Get all tasks for a specific task list"""
        tasks = await self.task_repo.get_by_task_list_id(task_list_id)
        
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                percentage=task.percentage,
                priority=task.priority,
                task_list_id=task.task_list_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]

    async def get_filtered_tasks(
        self, 
        task_list_id: int, 
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
    ) -> Optional[TaskListWithFilteredTasksResponse]:
        """Get filtered tasks by status and/or priority"""
        # Verify task list exists
        task_list = await self.task_list_repo.get_by_id(task_list_id)
        if not task_list:
            return None
        
        # Get filtered tasks
        filtered_tasks = await self.task_repo.get_filtered_tasks(task_list_id, status, priority)
        
        # Convert to response DTOs
        task_responses = [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                percentage=task.percentage,
                priority=task.priority,
                task_list_id=task.task_list_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in filtered_tasks
        ]
        
        # Create filter request for response
        filter_request = TaskFilterRequest(status=status, priority=priority)
        
        return TaskListWithFilteredTasksResponse(
            id=task_list.id,
            title=task_list.title,
            description=task_list.description,
            completion_percentage=task_list.completion_percentage,
            total_tasks=task_list.total_tasks,
            completed_tasks=task_list.completed_tasks,
            filtered_tasks=task_responses,
            filter_applied=filter_request,
            created_at=task_list.created_at,
            updated_at=task_list.updated_at
        )

    async def update_task(self, task_id: int, request: UpdateTaskRequest) -> Optional[TaskResponse]:
        """Update a task"""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        # Update fields if provided
        if request.title is not None:
            task.title = request.title
        if request.description is not None:
            task.description = request.description
        if request.priority is not None:
            task.priority = request.priority
        if request.percentage is not None:
            task.update_percentage(request.percentage)
        
        task.updated_at = datetime.utcnow()
        
        updated_task = await self.task_repo.update(task)
        
        return TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            status=updated_task.status,
            percentage=updated_task.percentage,
            priority=updated_task.priority,
            task_list_id=updated_task.task_list_id,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at
        )

    async def update_task_status(self, task_id: int, request: UpdateTaskStatusRequest) -> Optional[TaskResponse]:
        """Update task status"""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return None
        
        task.update_status(request.status)
        
        updated_task = await self.task_repo.update_status(task_id, request.status)
        
        return TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            status=updated_task.status,
            percentage=updated_task.percentage,
            priority=updated_task.priority,
            task_list_id=updated_task.task_list_id,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at
        )

    async def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        return await self.task_repo.delete(task_id) 