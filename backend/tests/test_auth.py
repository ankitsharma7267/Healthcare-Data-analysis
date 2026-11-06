import pytest
from app import create_app
from app.extensions import db
from app.models import User, RevokedToken

@pytest.fixture()
def client():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key-that-is-long-enough",
        "JWT_SECRET_KEY": "test-jwt-secret-key-that-is-long-enough",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "FRONTEND_ORIGIN": "http://localhost:5173",
        "RATELIMIT_ENABLED": False,
    })
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_register_login_me_and_logout(client):
    registered = client.post("/api/v1/auth/register", json={
        "email": "student@example.com", "password": "a-long-test-password-123"
    })
    assert registered.status_code == 201
    assert registered.json["user"]["role"] == "analyst"

    with client.application.app_context():
        user = User.query.filter_by(email="student@example.com").one()
        assert user.password_hash != "a-long-test-password-123"
        assert user.password_hash.startswith("$argon2")

    login = client.post("/api/v1/auth/login", json={
        "email": "student@example.com", "password": "a-long-test-password-123"
    })
    assert login.status_code == 200
    token = login.json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 200
    assert client.get("/api/v1/overview", headers=headers).status_code == 200
    assert client.post("/api/v1/auth/logout", headers=headers).status_code == 200
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 401

def test_public_registration_cannot_assign_admin(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "attempt@example.com", "password": "a-long-test-password-123", "role": "admin"
    })
    assert response.status_code == 201
    assert response.json["user"]["role"] == "analyst"

def test_short_password_is_rejected(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "short@example.com", "password": "tiny"
    })
    assert response.status_code == 400
