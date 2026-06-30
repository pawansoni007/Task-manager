"""Tasks router — HTTP surface for the task resource.

Thin by design: it parses/validates input via schemas, delegates to
``TaskService``, and maps domain errors to HTTP status codes. No business logic
lives here.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.api.deps import get_task_service
from app.schemas.task import TaskCreate, TaskOut, TaskStats, TaskUpdate
from app.services.task_service import (
    STATUS_FILTER_ALL,
    TaskNotFoundError,
    TaskService,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

StatusFilter = Query(
    default=STATUS_FILTER_ALL,
    pattern="^(all|open|completed)$",
    description="Filter by task status.",
)


@router.get("", response_model=list[TaskOut])
def list_tasks(
    status: str = StatusFilter,
    search: str = Query(default="", description="Case-insensitive title search."),
    service: TaskService = Depends(get_task_service),
) -> list[TaskOut]:
    return service.list(status=status, search=search)


@router.get("/stats", response_model=TaskStats)
def task_stats(service: TaskService = Depends(get_task_service)) -> TaskStats:
    return service.stats()


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskOut:
    return service.create(payload)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskOut:
    try:
        return service.update(task_id, payload)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> Response:
    try:
        service.delete(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
