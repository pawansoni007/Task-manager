"""In-memory repository — the zero-config default.

Backed by a dict and guarded by a lock so it is safe under FastAPI's threaded
request handling. Data lives only for the process lifetime; see the README for
the persistence limitation and how ``DATABASE_URL`` makes it durable.
"""

from __future__ import annotations

import threading

from app.domain.models import Task
from app.repositories.base import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._lock = threading.Lock()

    def add(self, task: Task) -> Task:
        with self._lock:
            self._tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list_all(self) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.created_at, reverse=True)

    def update(self, task: Task) -> Task:
        with self._lock:
            self._tasks[task.id] = task
        return task

    def delete(self, task_id: str) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None
