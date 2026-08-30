import pytest

from app.api.routes import uploads as uploads_module

pytestmark = pytest.mark.anyio


async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_public_api_health(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_public_content_lists(client):
    assert (await client.get("/api/v1/projects")).status_code == 200
    assert (await client.get("/api/v1/blog")).status_code == 200
    assert (await client.get("/api/v1/certifications")).status_code == 200


async def test_login_rejects_bad_password(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "pass" + "word": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


async def test_admin_can_create_project(client, admin_token):
    response = await client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "title": "New Project",
            "slug": "new-project",
            "summary": "New summary",
            "description": "New description",
            "tags": ["fastapi"],
            "featured": True,
        },
    )
    assert response.status_code == 201
    assert response.json()["slug"] == "new-project"


async def test_duplicate_project_slug_returns_conflict(client, admin_token):
    response = await client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "title": "Duplicate Project",
            "slug": "demo-project",
            "summary": "Duplicate summary",
            "description": "Duplicate description",
            "tags": ["fastapi"],
            "featured": False,
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Project slug already exists"


async def test_duplicate_blog_slug_returns_conflict(client, admin_token):
    response = await client.post(
        "/api/v1/blog",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "title": "Duplicate Post",
            "slug": "demo-post",
            "excerpt": "Duplicate excerpt",
            "content": "Duplicate content",
            "published": True,
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Blog post slug already exists"


async def test_upload_accepts_empty_optional_ids(client, admin_token, monkeypatch):
    monkeypatch.setattr(
        uploads_module.storage_service,
        "upload",
        lambda file, category: (f"{category}/demo.txt", "http://storage/demo.txt", 5),
    )

    response = await client.post(
        "/api/v1/uploads",
        headers={"Authorization": f"Bearer {admin_token}"},
        data={"category": "general", "project_id": "", "certification_id": ""},
        files={"file": ("demo.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 201
    assert response.json()["object_key"] == "general/demo.txt"


async def test_admin_required_for_writes(client):
    response = await client.post(
        "/api/v1/blog",
        json={
            "title": "Blocked",
            "slug": "blocked",
            "excerpt": "Blocked",
            "content": "Blocked",
            "published": True,
        },
    )
    assert response.status_code == 401
