"""Shared test fixtures.

Each test gets a fresh in-memory service so cases are isolated. The API test
client overrides the ``get_task_service`` dependency with that same service.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_task_service
from app.main import app
from app.repositories.memory import InMemoryTaskRepository
from app.services.task_service import TaskService


@pytest.fixture
def service() -> TaskService:
    return TaskService(InMemoryTaskRepository())


@pytest.fixture
def client(service: TaskService) -> TestClient:
    app.dependency_overrides[get_task_service] = lambda: service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
