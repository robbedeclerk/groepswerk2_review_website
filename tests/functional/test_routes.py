import pytest
from app import app, db
from app.models import User
from app.forms import RegistrationForm, LoginForm


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_register_page(client):
    """
    Tests is we the route exists.
    """
    response = client.get('/register')
    assert response.status_code == 200
