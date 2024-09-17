import asyncio
import logging
from app.api import fetch_crm_data, fetch_marketing_data
from app.database import SessionLocal
from app import crud

running_tasks = {}

logger = logging.getLogger(__name__)

async def sync_crm_data():
    """
    Sync CRM data from the Berry API and store it in the database.

    This is an asynchronous function that fetches the CRM data from the Berry API
    and stores it in the customers table of the database. The function also marks
    the sync as completed by setting the "crm_sync" key in the running_tasks
    dictionary to "completed".

    :return: None
    """
    try:
        db = SessionLocal()
        customers = await fetch_crm_data()
        crud.store_customers(db, customers)
        running_tasks["crm_sync"] = "completed"
        db.close()
    except Exception as e:
        logger.error(f"Error syncing CRM data: {e}")

async def sync_marketing_data():
    """
    Sync marketing data from the Berry API and store it in the database.

    This is an asynchronous function that fetches the marketing data from the Berry API
    and stores it in the campaigns table of the database. The function also marks
    the sync as completed by setting the "marketing_sync" key in the running_tasks
    dictionary to "completed".

    :return: None
    """
    try:
        db = SessionLocal()
        campaigns = await fetch_marketing_data()
        crud.store_campaigns(db, campaigns)
        running_tasks["marketing_sync"] = "completed"
        db.close()
    except Exception as e:
        logger.error(f"Error syncing marketing data: {e}")

def cancel_task(task_id: int):
    """
    Cancel a background task.

    This is a dummy implementation of the cancel_task function. In a real application,
    you would need to implement logic to cancel the task.

    :param task_id: The ID of the task to cancel.
    :return: None
    """
    running_tasks.pop(task_id, None)

