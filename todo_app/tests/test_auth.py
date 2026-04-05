import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_register_success(client):
    response = client.post("/api/register", json={
        "name": "Simone",
        "email": "simone@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Đăng ký thành công"

    with client.application.app_context():
        user = User.query.filter_by(email="simone@example.com").first()
        assert user is not None
        assert user.name == "Simone"

def test_register_duplicate_email(client):
    client.post("/api/register", json={
        "name": "Simone",
        "email": "simone@example.com",
        "password": "secret123"
    })
    
    response = client.post("/api/register", json={
        "name": "Simone2",
        "email": "simone@example.com",
        "password": "secret456"
    })
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email đã tồn tại"

def test_signin_success(client):
    client.post("/api/register", json={
        "name": "Simone",
        "email": "simone@example.com",
        "password": "secret123"
    })
    response = client.post("/api/signin", json={
        "email": "simone@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Đăng nhập thành công"

def test_signin_wrong_password(client):
    client.post("/api/register", json={
        "name": "Simone",
        "email": "simone@example.com",
        "password": "secret123"
    })

    response = client.post("/api/signin", json={
        "email": "simone@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 400
    assert response.get_json()["error"] == "Email hoặc mật khẩu không đúng"