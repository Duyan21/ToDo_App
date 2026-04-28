import pytest
from src.app import create_app
from src.database.models import db, User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield app


@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(
            name='Test User',
            email='test@example.com',
            password_hash=generate_password_hash('Test123456')
        )
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def authenticated_client(client, app, test_user):
    with app.app_context():
        with client.session_transaction() as sess:
            sess['user_id'] = test_user
        yield client