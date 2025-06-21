import pytest
from datetime import datetime
from src.domain.entities.task import Task, TaskStatus, TaskPriority

# --- Task Entity Unit Tests ---

def test_task_creation_defaults():
    """Tests that a Task is created with correct default values."""
    now = datetime.utcnow()
    task = Task(
        title="Default Test Task",
        task_list_id=1,
        created_at=now,
    )
    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.MEDIUM
    assert task.percentage == 0
    assert task.description is None


def test_update_status_to_completed():
    """Tests that updating status to COMPLETED sets percentage to 100."""
    task = Task(title="Test Task", task_list_id=1, percentage=50)
    task.update_status(TaskStatus.COMPLETED)
    assert task.status == TaskStatus.COMPLETED
    assert task.percentage == 100
    assert task.updated_at is not None


def test_update_status_to_pending():
    """Tests that updating status to PENDING sets percentage to 0."""
    task = Task(title="Test Task", task_list_id=1, percentage=50)
    task.update_status(TaskStatus.PENDING)
    assert task.status == TaskStatus.PENDING
    assert task.percentage == 0
    assert task.updated_at is not None


def test_update_status_other():
    """Tests that updating to other statuses doesn't auto-change percentage."""
    task = Task(title="Test Task", task_list_id=1, percentage=50)
    task.update_status(TaskStatus.IN_PROGRESS)
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.percentage == 50  # Percentage should not change
    assert task.updated_at is not None


def test_update_percentage():
    """Tests that percentage can be updated directly."""
    task = Task(title="Test Task", task_list_id=1)
    task.update_percentage(75)
    assert task.percentage == 75
    assert task.updated_at is not None


def test_update_percentage_invalid_value():
    """Tests that updating percentage with an invalid value raises a ValueError."""
    task = Task(title="Test Task", task_list_id=1)
    with pytest.raises(ValueError, match="Percentage must be between 0 and 100"):
        task.update_percentage(101)
    with pytest.raises(ValueError, match="Percentage must be between 0 and 100"):
        task.update_percentage(-1) 