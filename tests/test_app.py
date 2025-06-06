import pytest
import werkzeug
if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = "unknown"
from app import app, patients

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_patients():
    patients.clear()


def test_login_page_renders(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Your Name' in response.data


def test_add_note(client):
    # Log in as a patient
    response = client.post('/login', data={'name': 'Alice'}, follow_redirects=True)
    assert b'Welcome, Alice' in response.data

    # Add a note
    response = client.post('/add_note', data={'note': 'First note'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'First note' in response.data
