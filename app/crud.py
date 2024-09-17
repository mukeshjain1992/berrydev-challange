import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import Customer, Campaign
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Store webhook data (you can customize based on what kind of data you're expecting)
def store_webhook_data(db: Session, data: dict):
    """
    Store webhook data in the database.
    This is just a placeholder implementation. Depending on the webhook content,
    you can process and store the data appropriately.
    """
    # Example of handling webhook data related to customers (adapt based on actual webhook schema)
    if "customers" in data:
        store_customers(db, data["customers"])
    if "campaigns" in data:
        store_campaigns(db, data["campaigns"])

# Get customers with pagination
def get_customers(db: Session, offset: int = 0, limit: int = 100):
    """
    Retrieve customers from the database with pagination.
    :param db: Database session
    :param offset: Starting point for pagination
    :param limit: Maximum number of records to retrieve
    :return: List of customers
    """
    try:
        return db.query(Customer).offset(offset).limit(limit).all()
    except Exception as e:
        logging.error(f"Error retrieving customers: {e}")
        return []

# Get campaigns with pagination (if needed for /data route later)
def get_campaigns(db: Session, offset: int = 0, limit: int = 100):
    """
    Retrieve campaigns from the database with pagination.
    :param db: Database session
    :param offset: Starting point for pagination
    :param limit: Maximum number of records to retrieve
    :return: List of campaigns
    """
    try:
        return db.query(Campaign).offset(offset).limit(limit).all()
    except Exception as e:
        logging.error(f"Error retrieving campaigns: {e}")
        return []

# Store customers from external CRM API into the database
def store_customers(db: Session, customers: list):
    """
    Store customer data into the database.
    :param db: Database session
    :param customers: List of customer data from CRM API
    """
    try:
        for customer_data in customers:
            # Check if the customer already exists in the database
            existing_customer = db.query(Customer).filter_by(id=customer_data['id']).first()
            
            if existing_customer:
                # Update the existing customer data
                existing_customer.name = customer_data['name']
                existing_customer.email = customer_data['email']
            else:
                # Create a new customer record
                new_customer = Customer(
                    id=customer_data['id'],
                    name=customer_data['name'],
                    email=customer_data['email']
                )
                db.add(new_customer)
        
        # Commit the transaction to persist the changes
        db.commit()
    except IntegrityError as e:
        logging.error(f"Error storing customers: {e}")
    except Exception as e:
        logging.error(f"Error storing customers: {e}")

# Store campaigns from external Marketing API into the database
def store_campaigns(db: Session, campaigns: list):
    """
    Store campaign data into the database.
    :param db: Database session
    :param campaigns: List of campaign data from Marketing API
    """
    try:
        for campaign_data in campaigns:
            # Parse start_date to a datetime object
            start_date = datetime.strptime(campaign_data['start_date'], "%Y-%m-%dT%H:%M:%S")
            
            # Check if the campaign already exists in the database
            existing_campaign = db.query(Campaign).filter_by(id=campaign_data['id']).first()
            
            if existing_campaign:
                # Update the existing campaign data
                existing_campaign.name = campaign_data['name']
                existing_campaign.status = campaign_data['status']
                existing_campaign.start_date = start_date
            else:
                # Create a new campaign record
                new_campaign = Campaign(
                    id=campaign_data['id'],
                    name=campaign_data['name'],
                    status=campaign_data['status'],
                    start_date=start_date
                )
                db.add(new_campaign)
        
        # Commit the transaction to persist the changes
        db.commit()
    except IntegrityError as e:
        logging.error(f"Error storing campaigns: {e}")
    except Exception as e:
        logging.error(f"Error storing campaigns: {e}")

