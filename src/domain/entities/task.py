from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    percentage: int = Field(0, ge=0, le=100)
    priority: TaskPriority = TaskPriority.MEDIUM
    task_list_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator('percentage')
    def validate_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Percentage must be between 0 and 100')
        return v

    def update_status(self, new_status: TaskStatus):
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        # Auto-update percentage based on status
        if new_status == TaskStatus.COMPLETED:
            self.percentage = 100
        elif new_status == TaskStatus.PENDING:
            self.percentage = 0

    def update_percentage(self, new_percentage: int):
        if new_percentage < 0 or new_percentage > 100:
            raise ValueError('Percentage must be between 0 and 100')
        self.percentage = new_percentage
        self.updated_at = datetime.utcnow() 