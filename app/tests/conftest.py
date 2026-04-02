import pytest
import sys
from unittest.mock import MagicMock

mock_psycopg2 = MagicMock()
mock_extras = MagicMock()

sys.modules["psycopg2"] = mock_psycopg2
sys.modules["psycopg2.extras"] = mock_extras
sys.modules['psycopg2.pool'] = MagicMock()
sys.modules['redis'] = MagicMock()
sys.modules["pika"] = MagicMock()
sys.modules["elasticsearch"] = MagicMock()


# import the actual fastapi instance from main app
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    This fixture provides a fastapi testclient.
    whenever a test function needs it, it just ask for client as argument
    """
    with TestClient(app) as c:
        yield c