from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from ...domain.entities.task import TaskStatus, TaskPriority


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TaskPriority = TaskPriority.MEDIUM
    percentage: int = Field(0, ge=0, le=100)


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    percentage: Optional[int] = Field(None, ge=0, le=100)


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    percentage: int
    priority: TaskPriority
    task_list_id: int
    created_at: datetime
    updated_at: Optional[datetime]


class TaskFilterRequest(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None 