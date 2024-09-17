import pytest
from app.database import SessionLocal, engine
from app import crud, models
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Create a new database session for testing
@pytest.fixture(scope='module')
def test_db():
    Session = sessionmaker(bind=engine)
    db = Session()
    yield db
    db.close()

def test_store_customers(test_db):
    # Create tables
    models.Base.metadata.create_all(bind=engine)

    customer_data = [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com"
        }
    ]
    crud.store_customers(test_db, customer_data)
    customer = test_db.query(models.Customer).filter_by(id=1).first()
    assert customer is not None
    assert customer.name == "Alice"
    assert customer.email == "alice@example.com"

def test_store_campaigns(test_db):
    models.Base.metadata.create_all(bind=engine)
    campaign_data = [
        {
            "id": 101,
            "name": "Winter Sale",
            "status": "active",
            "start_date": "2024-12-01T00:00:00"
        }
    ]
    crud.store_campaigns(test_db, campaign_data)
    campaign = test_db.query(models.Campaign).filter_by(id=101).first()
    assert campaign is not None
    assert campaign.name == "Winter Sale"
    assert campaign.status == "active"
    assert campaign.start_date == datetime(2024, 12, 1)

