import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.postgres import SessionLocal
from app.models.sql_models import User

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    from app.db.postgres import engine
    from app.models.sql_models import Base
    Base.metadata.create_all(bind=engine)

def test_register():
    response = client.post(
        "/api/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code in [200, 400]

def test_login():
    client.post(
        "/api/auth/register",
        json={"name": "Login Test", "email": "login@example.com", "password": "pass123"}
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "pass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
