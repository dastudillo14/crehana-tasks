import pytest
from httpx import AsyncClient

# --- TaskList API Integration Tests ---

@pytest.mark.asyncio
async def test_create_and_get_task_list(client: AsyncClient):
    """Tests creating a task list and then retrieving it."""
    # Create a new task list
    response = await client.post(
        "/task-lists/",
        json={"title": "Test List 1", "description": "A test description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test List 1"
    assert "id" in data
    task_list_id = data["id"]

    # Get the created task list by its ID
    response = await client.get(f"/task-lists/{task_list_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_list_id
    assert data["title"] == "Test List 1"


@pytest.mark.asyncio
async def test_get_all_task_lists(client: AsyncClient):
    """Tests retrieving all task lists."""
    # Create a couple of task lists to ensure there's data
    await client.post("/task-lists/", json={"title": "List A"})
    await client.post("/task-lists/", json={"title": "List B"})

    response = await client.get("/task-lists/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert "List A" in [item["title"] for item in data]


@pytest.mark.asyncio
async def test_update_task_list(client: AsyncClient):
    """Tests updating an existing task list."""
    # Create a task list
    response = await client.post("/task-lists/", json={"title": "Original Title"})
    task_list_id = response.json()["id"]

    # Update the task list
    update_data = {"title": "Updated Title", "description": "Updated description"}
    response = await client.put(f"/task-lists/{task_list_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_delete_task_list(client: AsyncClient):
    """Tests deleting a task list."""
    # Create a task list
    response = await client.post("/task-lists/", json={"title": "To Be Deleted"})
    task_list_id = response.json()["id"]

    # Delete the task list
    response = await client.delete(f"/task-lists/{task_list_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = await client.get(f"/task-lists/{task_list_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_task_list(client: AsyncClient):
    """Tests that requesting a non-existent task list returns a 404 error."""
    response = await client.get("/task-lists/99999")
    assert response.status_code == 404 