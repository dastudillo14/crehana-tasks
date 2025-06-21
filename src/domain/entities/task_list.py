from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .task import Task, TaskStatus


class TaskList(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    tasks: List[Task] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def completion_percentage(self) -> int:
        """Calculate the completion percentage of the task list"""
        if not self.tasks:
            return 0
        
        total_percentage = sum(task.percentage for task in self.tasks)
        return total_percentage // len(self.tasks)

    @property
    def total_tasks(self) -> int:
        return len(self.tasks)

    @property
    def completed_tasks(self) -> int:
        return len([task for task in self.tasks if task.status == TaskStatus.COMPLETED])

    def add_task(self, task: Task):
        task.task_list_id = self.id
        self.tasks.append(task)
        self.updated_at = datetime.utcnow()

    def remove_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.updated_at = datetime.utcnow()

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None) 