"""Unit tests for the service layer (business logic in isolation)."""

from __future__ import annotations

import pytest

from app.domain.models import Priority, Status
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskNotFoundError, TaskService


def _create(service: TaskService, title: str, **kwargs) -> str:
    task = service.create(TaskCreate(title=title, **kwargs))
    return task.id


def test_create_sets_defaults(service: TaskService) -> None:
    task = service.create(TaskCreate(title="Write report"))
    assert task.id
    assert task.status is Status.OPEN
    assert task.description == ""
    assert task.created_at == task.updated_at


def test_create_trims_title(service: TaskService) -> None:
    task = service.create(TaskCreate(title="  spaced  "))
    assert task.title == "spaced"


def test_create_with_optional_fields(service: TaskService) -> None:
    task = service.create(
        TaskCreate(title="Pay bill", priority=Priority.HIGH, dueDate="2026-07-01")
    )
    assert task.priority is Priority.HIGH
    assert str(task.due_date) == "2026-07-01"


def test_get_missing_raises(service: TaskService) -> None:
    with pytest.raises(TaskNotFoundError):
        service.get("nope")


def test_complete_via_update(service: TaskService) -> None:
    task_id = _create(service, "Ship it")
    updated = service.update(task_id, TaskUpdate(status=Status.COMPLETED))
    assert updated.status is Status.COMPLETED
    assert updated.updated_at >= updated.created_at


def test_edit_only_touches_sent_fields(service: TaskService) -> None:
    task_id = _create(service, "Original", description="keep me")
    updated = service.update(task_id, TaskUpdate(title="Renamed"))
    assert updated.title == "Renamed"
    assert updated.description == "keep me"  # untouched


def test_update_missing_raises(service: TaskService) -> None:
    with pytest.raises(TaskNotFoundError):
        service.update("nope", TaskUpdate(title="x"))


def test_delete_then_missing(service: TaskService) -> None:
    task_id = _create(service, "Temp")
    service.delete(task_id)
    with pytest.raises(TaskNotFoundError):
        service.get(task_id)


def test_delete_missing_raises(service: TaskService) -> None:
    with pytest.raises(TaskNotFoundError):
        service.delete("nope")


def test_filter_by_status(service: TaskService) -> None:
    open_id = _create(service, "Open task")
    done_id = _create(service, "Done task")
    service.update(done_id, TaskUpdate(status=Status.COMPLETED))

    open_only = service.list(status="open")
    completed_only = service.list(status="completed")

    assert [t.id for t in open_only] == [open_id]
    assert [t.id for t in completed_only] == [done_id]
    assert len(service.list(status="all")) == 2


def test_search_by_title_is_case_insensitive(service: TaskService) -> None:
    _create(service, "Buy Milk")
    _create(service, "Walk dog")
    results = service.list(search="milk")
    assert [t.title for t in results] == ["Buy Milk"]


def test_search_and_filter_combine(service: TaskService) -> None:
    a = _create(service, "Report draft")
    _create(service, "Report final")
    service.update(a, TaskUpdate(status=Status.COMPLETED))
    results = service.list(status="open", search="report")
    assert [t.title for t in results] == ["Report final"]


def test_stats_counts(service: TaskService) -> None:
    _create(service, "a")
    b = _create(service, "b")
    service.update(b, TaskUpdate(status=Status.COMPLETED))
    stats = service.stats()
    assert (stats.all, stats.open, stats.completed) == (2, 1, 1)


def test_list_newest_first(service: TaskService) -> None:
    first = _create(service, "first")
    second = _create(service, "second")
    ordered = [t.id for t in service.list()]
    assert ordered.index(second) < ordered.index(first)
