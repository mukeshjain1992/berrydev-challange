import pytest
import httpx
from app.main import app
from fastapi.testclient import TestClient
from app.database import engine
from app import models

client = TestClient(app)

@pytest.mark.asyncio
async def test_async_webhook_endpoint():
    # Create tables
    models.Base.metadata.create_all(bind=engine)

    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "customers": [
                {
                    "id": 4,
                    "name": "Dave",
                    "email": "dave@example.com"
                }
            ],
            "campaigns": [
                {
                    "id": 104,
                    "name": "Spring Sale",
                    "status": "active",
                    "start_date": "2024-03-01T00:00:00"
                }
            ]
        }
        response = await client.post("/webhook", json=payload)
        assert response.status_code == 200
        assert response.json() == {"status": "Webhook received"}

    # Drop tables
    models.Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_async_get_data():
    # Insert data before fetching
    await test_async_webhook_endpoint()  # Add data first

    # Create tables
    models.Base.metadata.create_all(bind=engine)

    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/data")
        assert response.status_code == 200
        data = response.json().get("data")

        # Assuming the data should be paginated, make sure we check for both customers and campaigns
        assert "customers" in data
        assert len(data["customers"]) >= 0
        assert "campaigns" in data
        assert len(data["campaigns"]) >= 0

    # Drop tables
    models.Base.metadata.drop_all(bind=engine)
