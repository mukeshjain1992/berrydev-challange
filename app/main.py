from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import tasks
from app.database import SessionLocal, engine
from app import models, crud

from fastapi import HTTPException


import logging

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Error getting database session: {e}")
    finally:
        db.close()

# POST /webhook: Handle webhook data
@app.post("/webhook")
async def handle_webhook(data: dict, db: Session = Depends(get_db)):
    try:
        crud.store_webhook_data(db, data)
        return {"status": "Webhook received"}
    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET /data: Retrieve stored data with pagination
@app.get("/data")
async def get_data(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        customers = crud.get_customers(db, offset=offset, limit=limit)
        campaigns = crud.get_campaigns(db, offset=offset, limit=limit)
        return {"data": {"customers": customers, "campaigns": campaigns}}
    except Exception as e:
        logging.error(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET /sync/{source}: Trigger sync for external API (CRM or Marketing)
@app.get("/sync/{source}")
async def sync_data(source: str, background_tasks: BackgroundTasks):
    try:
        if source == "crm":
            background_tasks.add_task(tasks.sync_crm_data)
        elif source == "marketing":
            background_tasks.add_task(tasks.sync_marketing_data)
        else:
            raise HTTPException(status_code=400, detail="Invalid source")
        return {"status": "Sync started"}
    except Exception as e:
        logging.error(f"Error triggering sync: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET /tasks: List all running background tasks
@app.get("/tasks")
async def list_tasks():
    try:
        return tasks.running_tasks
    except Exception as e:
        logging.error(f"Error listing tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# POST /tasks/cancel: Cancel a background task
@app.post("/tasks/cancel")
async def cancel_task(task_id: int):
    try:
        tasks.cancel_task(task_id)
        return {"status": "Task cancelled"}
    except Exception as e:
        logging.error(f"Error cancelling task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

