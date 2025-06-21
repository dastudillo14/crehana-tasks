from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.task_list import TaskList


class TaskListRepository(ABC):
    """Repository interface for TaskList operations"""
    
    @abstractmethod
    async def create(self, task_list: TaskList) -> TaskList:
        """Create a new task list"""
        pass
    
    @abstractmethod
    async def get_by_id(self, task_list_id: int) -> Optional[TaskList]:
        """Get a task list by ID"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[TaskList]:
        """Get all task lists"""
        pass
    
    @abstractmethod
    async def update(self, task_list: TaskList) -> TaskList:
        """Update a task list"""
        pass
    
    @abstractmethod
    async def delete(self, task_list_id: int) -> bool:
        """Delete a task list"""
        pass 