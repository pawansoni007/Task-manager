"""Aggregate API router.

All sub-routers are mounted under a single ``/api`` prefix here, so ``main.py``
only needs to include one router and stays free of endpoint wiring.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.routers import health, tasks

api_router = APIRouter(prefix="/api")
api_router.include_router(tasks.router)
api_router.include_router(health.router)
