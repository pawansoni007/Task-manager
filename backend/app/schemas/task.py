"""Pydantic DTOs — the HTTP contract.

These define request/response shapes and validation rules. They are kept
separate from the domain model so the API can evolve independently and so all
JSON is camelCase (via ``alias_generator``) while Python stays snake_case.
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from app.domain.models import Priority, Status


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


def _require_non_empty_title(value: str) -> str:
    # The one hard validation rule from the brief: title is required and must
    # not be empty/whitespace.
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("title must not be empty")
    return cleaned


class TaskCreate(_CamelModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    priority: Priority | None = None
    due_date: date | None = None

    _validate_title = field_validator("title")(_require_non_empty_title)


class TaskUpdate(_CamelModel):
    """Partial update — every field optional. Used for both edit and complete."""

    title: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: Status | None = None
    priority: Priority | None = None
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def _validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _require_non_empty_title(value)


class TaskOut(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: str
    title: str
    description: str
    status: Status
    priority: Priority | None
    due_date: date | None
    created_at: datetime
    updated_at: datetime


class TaskStats(_CamelModel):
    all: int
    open: int
    completed: int
