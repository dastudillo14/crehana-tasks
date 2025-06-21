from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.task import Task, TaskStatus, TaskPriority


class TaskRepository(ABC):
    """Repository interface for Task operations"""
    
    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Create a new task"""
        pass
    
    @abstractmethod
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        pass
    
    @abstractmethod
    async def get_by_task_list_id(self, task_list_id: int) -> List[Task]:
        """Get all tasks for a specific task list"""
        pass
    
    @abstractmethod
    async def get_filtered_tasks(
        self, 
        task_list_id: int, 
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
    ) -> List[Task]:
        """Get filtered tasks by status and/or priority"""
        pass
    
    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Update a task"""
        pass
    
    @abstractmethod
    async def update_status(self, task_id: int, status: TaskStatus) -> Task:
        """Update task status"""
        pass
    
    @abstractmethod
    async def delete(self, task_id: int) -> bool:
        """Delete a task"""
        pass
    
    @abstractmethod
    async def delete_by_task_list_id(self, task_list_id: int) -> bool:
        """Delete all tasks for a specific task list"""
        pass 