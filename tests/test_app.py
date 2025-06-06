import os

os.environ.setdefault("SECRET_KEY", "test")

from app import app, init_db  # noqa: E402
import pytest  # noqa: E402
import werkzeug  # noqa: E402

if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = "unknown"


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    app.config["TESTING"] = True
    app.DATABASE = str(db_path)
    with app.app_context():
        init_db()
    with app.test_client() as client:
        yield client


def test_login_page_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Your Name" in response.data


def test_add_note(client):
    response = client.post(
        "/login",
        data={"name": "Alice"},
        follow_redirects=True,
    )
    assert b"Welcome, Alice" in response.data
    response = client.post(
        "/add_note",
        data={"note": "First note"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"First note" in response.data
