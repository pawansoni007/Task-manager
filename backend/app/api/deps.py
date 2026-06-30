"""Dependency injection wiring.

A single ``TaskService`` (with its repository) is built once and shared across
requests. Routers ask for it via ``Depends(get_task_service)``, which also makes
it trivial to override with a fresh in-memory service in tests.
"""

from __future__ import annotations

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.repositories.factory import build_repository
from app.services.task_service import TaskService

_service: TaskService | None = None


def get_task_service(settings: Settings = Depends(get_settings)) -> TaskService:
    global _service
    if _service is None:
        _service = TaskService(build_repository(settings))
    return _service
