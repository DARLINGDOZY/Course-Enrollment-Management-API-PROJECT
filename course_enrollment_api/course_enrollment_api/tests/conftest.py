import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage.datastore import datastore

@pytest.fixture(autouse=True)
def reset_datastore():
    datastore.clear()

@pytest.fixture
def client():
    return TestClient(app)
