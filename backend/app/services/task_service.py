"""Task business logic.

All rules live here: how a task is created, how a partial update is applied,
how the list is filtered/searched, and how stats are computed. Routers stay thin
(HTTP only) and repositories stay thin (storage only).
"""

from __future__ import annotations

from app.domain.models import Status, Task
from app.repositories.base import TaskRepository
from app.schemas.task import TaskCreate, TaskStats, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when an operation targets a task id that does not exist."""

    def __init__(self, task_id: str) -> None:
        super().__init__(f"Task '{task_id}' not found")
        self.task_id = task_id


# A sentinel "show everything" filter value, alongside the real statuses.
STATUS_FILTER_ALL = "all"


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repo = repository

    def create(self, data: TaskCreate) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            priority=data.priority,
            due_date=data.due_date,
        )
        return self._repo.add(task)

    def get(self, task_id: str) -> Task:
        task = self._repo.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def list(self, status: str = STATUS_FILTER_ALL, search: str = "") -> list[Task]:
        tasks = self._repo.list_all()
        if status != STATUS_FILTER_ALL:
            tasks = [t for t in tasks if t.status.value == status]
        query = search.strip().lower()
        if query:
            tasks = [t for t in tasks if query in t.title.lower()]
        return tasks

    def update(self, task_id: str, data: TaskUpdate) -> Task:
        task = self.get(task_id)
        # Only apply fields the client actually sent (partial update).
        changes = data.model_dump(exclude_unset=True)
        for field_name, value in changes.items():
            setattr(task, field_name, value)
        task.touch()
        return self._repo.update(task)

    def delete(self, task_id: str) -> None:
        if not self._repo.delete(task_id):
            raise TaskNotFoundError(task_id)

    def stats(self) -> TaskStats:
        tasks = self._repo.list_all()
        completed = sum(1 for t in tasks if t.status is Status.COMPLETED)
        return TaskStats(
            all=len(tasks),
            open=len(tasks) - completed,
            completed=completed,
        )
