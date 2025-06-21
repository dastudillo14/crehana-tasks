import pytest
from httpx import AsyncClient

from src.domain.entities.task import TaskPriority, TaskStatus

# --- Task API Integration Tests ---

@pytest.fixture
async def task_list(client: AsyncClient) -> int:
    """Fixture to create a default task list and return its ID."""
    response = await client.post("/task-lists/", json={"title": "Default List"})
    assert response.status_code == 201
    return response.json()["id"]


@pytest.mark.asyncio
async def test_create_task_in_list(client: AsyncClient, task_list: int):
    """Tests creating a task within a specific task list."""
    task_data = {"title": "My New Task", "priority": TaskPriority.HIGH}
    response = await client.post(f"/tasks/{task_list}/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My New Task"
    assert data["priority"] == TaskPriority.HIGH
    assert data["task_list_id"] == task_list


@pytest.mark.asyncio
async def test_get_tasks_by_list(client: AsyncClient, task_list: int):
    """Tests retrieving all tasks for a specific list."""
    # Create a task to ensure the list is not empty
    await client.post(f"/tasks/{task_list}/tasks", json={"title": "Task A"})
    response = await client.get(f"/tasks/{task_list}/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == "Task A"


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, task_list: int):
    """Tests updating a specific task."""
    # Create a task
    task_data = {"title": "Original Task Title"}
    create_response = await client.post(f"/tasks/{task_list}/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Task Title",
        "description": "Now with a description!",
        "priority": TaskPriority.LOW,
        "percentage": 50,
    }
    response = await client.put(f"/tasks/task/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task Title"
    assert data["priority"] == TaskPriority.LOW
    assert data["percentage"] == 50


@pytest.mark.asyncio
async def test_update_task_status(client: AsyncClient, task_list: int):
    """Tests updating only the status of a task."""
    # Create a task
    create_response = await client.post(f"/tasks/{task_list}/tasks", json={"title": "Task to update"})
    task_id = create_response.json()["id"]

    # Update status
    response = await client.patch(
        f"/tasks/task/{task_id}/status",
        json={"status": TaskStatus.COMPLETED},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == TaskStatus.COMPLETED
    assert data["percentage"] == 100  # Business logic check


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, task_list: int):
    """Tests deleting a task."""
    # Create a task
    create_response = await client.post(f"/tasks/{task_list}/tasks", json={"title": "To delete"})
    task_id = create_response.json()["id"]

    # Delete the task
    response = await client.delete(f"/tasks/task/{task_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = await client.get(f"/tasks/task/{task_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_filtered_tasks(client: AsyncClient, task_list: int):
    """Tests filtering tasks by status and priority."""
    # Create a variety of tasks
    await client.post(
        f"/tasks/{task_list}/tasks",
        json={"title": "High Prio", "priority": TaskPriority.HIGH, "status": TaskStatus.PENDING},
    )
    await client.post(
        f"/tasks/{task_list}/tasks",
        json={"title": "Low Prio", "priority": TaskPriority.LOW, "status": TaskStatus.COMPLETED},
    )
    await client.post(
        f"/tasks/{task_list}/tasks",
        json={"title": "High Prio Done", "priority": TaskPriority.HIGH, "status": TaskStatus.COMPLETED},
    )

    # Filter by priority=HIGH
    response = await client.get(f"/tasks/{task_list}/tasks/filtered?priority=high")
    assert response.status_code == 200
    data = response.json()
    assert len(data["filtered_tasks"]) == 2
    assert "High Prio" in [t["title"] for t in data["filtered_tasks"]]

    # Filter by status=COMPLETED
    response = await client.get(f"/tasks/{task_list}/tasks/filtered?status=completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data["filtered_tasks"]) == 2
    assert "Low Prio" in [t["title"] for t in data["filtered_tasks"]]

    # Filter by both
    response = await client.get(f"/tasks/{task_list}/tasks/filtered?priority=high&status=completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data["filtered_tasks"]) == 1
    assert data["filtered_tasks"][0]["title"] == "High Prio Done" 