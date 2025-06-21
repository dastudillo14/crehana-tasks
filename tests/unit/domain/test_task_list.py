from src.domain.entities.task import Task, TaskStatus
from src.domain.entities.task_list import TaskList

# --- TaskList Entity Unit Tests ---

def test_empty_task_list_properties():
    """Tests the computed properties of a TaskList with no tasks."""
    task_list = TaskList(id=1, title="Empty List")
    assert task_list.total_tasks == 0
    assert task_list.completed_tasks == 0
    assert task_list.completion_percentage == 0


def test_task_list_properties_with_tasks():
    """Tests the computed properties of a TaskList with various tasks."""
    task1 = Task(id=1, title="T1", task_list_id=1, status=TaskStatus.COMPLETED, percentage=100)
    task2 = Task(id=2, title="T2", task_list_id=1, status=TaskStatus.IN_PROGRESS, percentage=50)
    task3 = Task(id=3, title="T3", task_list_id=1, status=TaskStatus.PENDING, percentage=0)
    task4 = Task(id=4, title="T4", task_list_id=1, status=TaskStatus.COMPLETED, percentage=100)

    task_list = TaskList(id=1, title="Test List", tasks=[task1, task2, task3, task4])

    assert task_list.total_tasks == 4
    assert task_list.completed_tasks == 2
    # Total percentage = (100 + 50 + 0 + 100) / 4 = 250 / 4 = 62.5
    # Integer division should result in 62.
    assert task_list.completion_percentage == 62


def test_task_list_with_single_task():
    """Tests the computed properties for a list with a single task."""
    task = Task(id=1, title="T1", task_list_id=1, status=TaskStatus.IN_PROGRESS, percentage=75)
    task_list = TaskList(id=1, title="Single Task List", tasks=[task])
    assert task_list.total_tasks == 1
    assert task_list.completed_tasks == 0
    assert task_list.completion_percentage == 75


def test_add_and_remove_task():
    """Tests that adding and removing tasks updates the list correctly."""
    task_list = TaskList(id=1, title="Dynamic List")
    task1 = Task(id=1, title="T1", task_list_id=1)
    task2 = Task(id=2, title="T2", task_list_id=1)

    task_list.add_task(task1)
    task_list.add_task(task2)
    assert task_list.total_tasks == 2
    assert task_list.tasks[0].title == "T1"
    assert task_list.get_task(1) is not None

    task_list.remove_task(1)
    assert task_list.total_tasks == 1
    assert task_list.get_task(1) is None
    assert task_list.get_task(2) is not None 