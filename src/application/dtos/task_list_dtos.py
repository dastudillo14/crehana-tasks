from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .task_dtos import TaskResponse, TaskFilterRequest


class CreateTaskListRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class UpdateTaskListRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class TaskListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completion_percentage: int
    total_tasks: int
    completed_tasks: int
    created_at: datetime
    updated_at: Optional[datetime]


class TaskListWithTasksResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completion_percentage: int
    total_tasks: int
    completed_tasks: int
    tasks: List[TaskResponse]
    created_at: datetime
    updated_at: Optional[datetime]


class TaskListWithFilteredTasksResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completion_percentage: int
    total_tasks: int
    completed_tasks: int
    filtered_tasks: List[TaskResponse]
    filter_applied: "TaskFilterRequest"
    created_at: datetime
    updated_at: Optional[datetime]

TaskListWithFilteredTasksResponse.model_rebuild() 