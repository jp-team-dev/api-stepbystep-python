import os

# When tests point to a dedicated Postgres URL, also override the main DATABASE_URL
TEST_URL = os.getenv("TEST_DATABASE_URL")
if TEST_URL:
    os.environ["DATABASE_URL"] = TEST_URL

import pytest
from sqlalchemy import text
from fastapi.testclient import TestClient
from sqlmodel import create_engine

from app import database
from app.main import app


@pytest.fixture(scope="module")
def test_engine():
    test_url = os.getenv("TEST_DATABASE_URL")
    if not test_url:
        raise RuntimeError("TEST_DATABASE_URL não configurado")
    engine = create_engine(test_url)
    database.engine = engine
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE card, lesson, module RESTART IDENTITY CASCADE;"))
        conn.commit()
    yield engine
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE card, lesson, module RESTART IDENTITY CASCADE;"))
        conn.commit()


@pytest.fixture
def client(test_engine):
    with TestClient(app) as c:
        yield c


def test_module_order_validation(client):
    invalid = {"title": "module", "order": 0}
    response = client.post("/learning/modules", json=invalid)
    assert response.status_code == 422
    assert "order must be greater than zero" in response.text

    invalid["order"] = -1
    response = client.post("/learning/modules", json=invalid)
    assert response.status_code == 422
    assert "order must be greater than zero" in response.text


def test_lesson_validation(client):
    module_resp = client.post("/learning/modules", json={"title": "valid", "order": 1})
    assert module_resp.status_code == 200
    module_id = module_resp.json()["id"]

    invalid = {"title": "lesson", "order": 0, "module_id": module_id}
    resp = client.post("/learning/lessons", json=invalid)
    assert resp.status_code == 422
    assert "order must be greater than zero" in resp.text

    invalid["order"] = 1
    invalid["module_id"] = -1
    resp = client.post("/learning/lessons", json=invalid)
    assert resp.status_code == 422
    assert "module_id must be positive" in resp.text

    invalid["module_id"] = 999
    resp = client.post("/learning/lessons", json=invalid)
    assert resp.status_code == 404


def test_card_validation(client):
    module_resp = client.post("/learning/modules", json={"title": "with lessons", "order": 2})
    module_id = module_resp.json()["id"]
    lesson_resp = client.post(
        "/learning/lessons",
        json={"title": "lesson", "order": 1, "module_id": module_id},
    )
    lesson_id = lesson_resp.json()["id"]

    payload = {"title": "card", "order": 0, "lesson_id": lesson_id}
    resp = client.post("/learning/cards", json=payload)
    assert resp.status_code == 422
    assert "order must be greater than zero" in resp.text

    payload["order"] = 1
    payload["lesson_id"] = -1
    resp = client.post("/learning/cards", json=payload)
    assert resp.status_code == 422
    assert "lesson_id must be positive" in resp.text

    payload["lesson_id"] = 999
    resp = client.post("/learning/cards", json=payload)
    assert resp.status_code == 404
