import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

# Initialize the test client
client = TestClient(app)

# Setup and teardown for the database
@pytest.fixture(scope='module', autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)

def test_webhook_endpoint():
    payload = {
        "customers": [
            {
                "id": 2,
                "name": "Bob",
                "email": "bob@example.com"
            }
        ],
        "campaigns": [
            {
                "id": 102,
                "name": "Holiday Sale",
                "status": "inactive",
                "start_date": "2024-12-01T00:00:00"
            }
        ]
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "Webhook received"}

def test_get_data():
    # Insert test data
    client.post("/webhook", json={
        "customers": [{"id": 3, "name": "Charlie", "email": "charlie@example.com"}],
        "campaigns": [{"id": 103, "name": "Black Friday", "status": "active", "start_date": "2024-11-24T00:00:00"}]
    })
    response = client.get("/data")
    assert response.status_code == 200
    data = response.json().get("data")
    print(data)
    assert len(data["customers"]) > 0
    assert len(data["campaigns"]) > 0

def test_sync_crm():
    response = client.get("/sync/crm")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"status": "Sync started"}

def test_sync_marketing():
    response = client.get("/sync/marketing")
    assert response.status_code == 200
    assert response.json() == {"status": "Sync started"}

def test_tasks_endpoint():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_cancel_task():
    response = client.post("/tasks/cancel", json={"task_id": 1})
    assert response.status_code == 422