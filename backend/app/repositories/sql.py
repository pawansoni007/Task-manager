"""SQL repository — activated when ``DATABASE_URL`` is set.

Uses SQLAlchemy 2.0 and works with SQLite (local file) or Postgres (Render).
The ORM row is mapped to/from the storage-agnostic domain ``Task`` so the rest
of the app never sees SQLAlchemy types.
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.domain.models import Priority, Status, Task
from app.repositories.base import TaskRepository


class Base(DeclarativeBase):
    pass


class TaskRow(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(2000), default="")
    status: Mapped[Status] = mapped_column(default=Status.OPEN)
    priority: Mapped[Priority | None] = mapped_column(default=None)
    due_date: Mapped[date | None] = mapped_column(default=None)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    @classmethod
    def from_domain(cls, task: Task) -> "TaskRow":
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    def to_domain(self) -> Task:
        return Task(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            priority=self.priority,
            due_date=self.due_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def apply(self, task: Task) -> None:
        self.title = task.title
        self.description = task.description
        self.status = task.status
        self.priority = task.priority
        self.due_date = task.due_date
        self.updated_at = task.updated_at


class SqlTaskRepository(TaskRepository):
    def __init__(self, database_url: str) -> None:
        # SQLite needs this flag to be used across FastAPI's threads.
        connect_args = (
            {"check_same_thread": False} if database_url.startswith("sqlite") else {}
        )
        self._engine = create_engine(database_url, connect_args=connect_args)
        self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
        Base.metadata.create_all(self._engine)

    def _session(self) -> Session:
        return self._session_factory()

    def add(self, task: Task) -> Task:
        with self._session() as session:
            session.add(TaskRow.from_domain(task))
            session.commit()
        return task

    def get(self, task_id: str) -> Task | None:
        with self._session() as session:
            row = session.get(TaskRow, task_id)
            return row.to_domain() if row else None

    def list_all(self) -> list[Task]:
        with self._session() as session:
            rows = (
                session.query(TaskRow).order_by(TaskRow.created_at.desc()).all()
            )
            return [row.to_domain() for row in rows]

    def update(self, task: Task) -> Task:
        with self._session() as session:
            row = session.get(TaskRow, task.id)
            if row is None:
                # Caller (service) guarantees existence, but be defensive.
                session.add(TaskRow.from_domain(task))
            else:
                row.apply(task)
            session.commit()
        return task

    def delete(self, task_id: str) -> bool:
        with self._session() as session:
            row = session.get(TaskRow, task_id)
            if row is None:
                return False
            session.delete(row)
            session.commit()
            return True
