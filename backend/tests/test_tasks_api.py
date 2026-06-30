"""API tests via FastAPI TestClient (HTTP contract + status codes)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create(client: TestClient, title: str, **body) -> dict:
    response = client.post("/api/tasks", json={"title": title, **body})
    assert response.status_code == 201
    return response.json()


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_returns_camel_case_payload(client: TestClient) -> None:
    task = _create(client, "Write tests", description="cover the API")
    assert task["title"] == "Write tests"
    assert task["status"] == "open"
    assert "createdAt" in task and "updatedAt" in task
    assert task["dueDate"] is None


def test_create_rejects_empty_title(client: TestClient) -> None:
    response = client.post("/api/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_requires_title(client: TestClient) -> None:
    response = client.post("/api/tasks", json={"description": "no title"})
    assert response.status_code == 422


def test_list_and_filter(client: TestClient) -> None:
    open_task = _create(client, "Open one")
    done_task = _create(client, "Done one")
    client.patch(f"/api/tasks/{done_task['id']}", json={"status": "completed"})

    all_tasks = client.get("/api/tasks").json()
    assert len(all_tasks) == 2

    open_only = client.get("/api/tasks", params={"status": "open"}).json()
    assert [t["id"] for t in open_only] == [open_task["id"]]

    completed_only = client.get("/api/tasks", params={"status": "completed"}).json()
    assert [t["id"] for t in completed_only] == [done_task["id"]]


def test_invalid_status_filter_is_rejected(client: TestClient) -> None:
    response = client.get("/api/tasks", params={"status": "bogus"})
    assert response.status_code == 422


def test_search_by_title(client: TestClient) -> None:
    _create(client, "Buy milk")
    _create(client, "Walk dog")
    results = client.get("/api/tasks", params={"search": "MILK"}).json()
    assert [t["title"] for t in results] == ["Buy milk"]


def test_complete_and_edit(client: TestClient) -> None:
    task = _create(client, "Draft")
    completed = client.patch(
        f"/api/tasks/{task['id']}", json={"status": "completed"}
    ).json()
    assert completed["status"] == "completed"

    edited = client.patch(
        f"/api/tasks/{task['id']}", json={"title": "Final draft"}
    ).json()
    assert edited["title"] == "Final draft"
    assert edited["status"] == "completed"  # unchanged by the edit


def test_patch_missing_returns_404(client: TestClient) -> None:
    response = client.patch("/api/tasks/missing", json={"title": "x"})
    assert response.status_code == 404


def test_delete_then_list(client: TestClient) -> None:
    task = _create(client, "Temp")
    assert client.delete(f"/api/tasks/{task['id']}").status_code == 204
    assert client.get("/api/tasks").json() == []


def test_delete_missing_returns_404(client: TestClient) -> None:
    assert client.delete("/api/tasks/missing").status_code == 404


def test_stats_endpoint(client: TestClient) -> None:
    _create(client, "a")
    done = _create(client, "b")
    client.patch(f"/api/tasks/{done['id']}", json={"status": "completed"})
    stats = client.get("/api/tasks/stats").json()
    assert stats == {"all": 2, "open": 1, "completed": 1}
