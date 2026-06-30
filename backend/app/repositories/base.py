"""Repository contract.

The service depends only on this interface, never on a concrete store. Swapping
in-memory for SQL is therefore a one-line change in the factory. Filtering,
search and stats deliberately live in the service (one place, easy to test), so
the repository stays a thin CRUD boundary.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.models import Task


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task:
        """Persist a new task and return it."""

    @abstractmethod
    def get(self, task_id: str) -> Task | None:
        """Return the task or ``None`` if it does not exist."""

    @abstractmethod
    def list_all(self) -> list[Task]:
        """Return all tasks (newest first)."""

    @abstractmethod
    def update(self, task: Task) -> Task:
        """Persist changes to an existing task and return it."""

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Delete a task; return ``True`` if a task was removed."""
