from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..application.dtos import (
    CreateTaskListRequest,
    UpdateTaskListRequest,
    TaskListResponse,
    CreateTaskRequest,
    UpdateTaskRequest,
    UpdateTaskStatusRequest,
    TaskResponse,
    TaskListWithFilteredTasksResponse,
)
from ..application.use_cases import TaskListUseCases, TaskUseCases
from ..domain.entities.task import TaskStatus, TaskPriority
from ..infrastructure.database import get_db_session
from ..infrastructure.repositories import (
    SQLAlchemyTaskListRepository,
    SQLAlchemyTaskRepository,
)

# Create routers
task_list_router = APIRouter(prefix="/task-lists", tags=["Task Lists"])
task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Dependency to get use cases
async def get_task_list_use_cases(session: AsyncSession = Depends(get_db_session)) -> TaskListUseCases:
    task_list_repo = SQLAlchemyTaskListRepository(session)
    task_repo = SQLAlchemyTaskRepository(session)
    return TaskListUseCases(task_list_repo, task_repo)


async def get_task_use_cases(session: AsyncSession = Depends(get_db_session)) -> TaskUseCases:
    task_list_repo = SQLAlchemyTaskListRepository(session)
    task_repo = SQLAlchemyTaskRepository(session)
    return TaskUseCases(task_repo, task_list_repo)


# Task List Routes
@task_list_router.post("/", response_model=TaskListResponse, status_code=201)
async def create_task_list(
    request: CreateTaskListRequest,
    use_cases: TaskListUseCases = Depends(get_task_list_use_cases)
):
    """Create a new task list"""
    return await use_cases.create_task_list(request)


@task_list_router.get("/", response_model=List[TaskListResponse])
async def get_all_task_lists(
    use_cases: TaskListUseCases = Depends(get_task_list_use_cases)
):
    """Get all task lists"""
    return await use_cases.get_all_task_lists()


@task_list_router.get("/{task_list_id}", response_model=TaskListResponse)
async def get_task_list(
    task_list_id: int,
    use_cases: TaskListUseCases = Depends(get_task_list_use_cases)
):
    """Get a specific task list by ID"""
    task_list = await use_cases.get_task_list(task_list_id)
    if not task_list:
        raise HTTPException(status_code=404, detail="Task list not found")
    return task_list


@task_list_router.put("/{task_list_id}", response_model=TaskListResponse)
async def update_task_list(
    task_list_id: int,
    request: UpdateTaskListRequest,
    use_cases: TaskListUseCases = Depends(get_task_list_use_cases)
):
    """Update a task list"""
    task_list = await use_cases.update_task_list(task_list_id, request)
    if not task_list:
        raise HTTPException(status_code=404, detail="Task list not found")
    return task_list


@task_list_router.delete("/{task_list_id}", status_code=204)
async def delete_task_list(
    task_list_id: int,
    use_cases: TaskListUseCases = Depends(get_task_list_use_cases)
):
    """Delete a task list and all its tasks"""
    success = await use_cases.delete_task_list(task_list_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task list not found")


# Task Routes
@task_router.post("/{task_list_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    task_list_id: int,
    request: CreateTaskRequest,
    use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    """Create a new task in a task list"""
    task = await use_cases.create_task(task_list_id, request)
    if not task:
        raise HTTPException(status_code=404, detail="Task list not found")
    return task


@task_router.get("/{task_list_id}/tasks", response_model=List[TaskResponse])
async def get_tasks_by_list(
    task_list_id: int,
    use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    """Get all tasks for a specific task list"""
    return await use_cases.get_tasks_by_list(task_list_id)


@task_router.get("/{task_list_id}/tasks/filtered", response_model=TaskListWithFilteredTasksResponse)
async def get_filtered_tasks(
    task_list_id: int,
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority"),
    use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    """Get filtered tasks by status and/or priority with completion percentage"""
    result = await use_cases.get_filtered_tasks(task_list_id, status, priority)
    if not result:
        raise HTTPException(status_code=404, detail="Task list not found")
    return result


@task_router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    """Get a specific task by ID"""
    task = await use_cases.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.put("/task/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    """Update a task"""
    task = await use_cases.update_task(task_id, request)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.patch("/task/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    request: UpdateTaskStatusRequest,
    use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    """Update task status"""
    task = await use_cases.update_task_status(task_id, request)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.delete("/task/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    """Delete a task"""
    success = await use_cases.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found") 