# FastAPI Data Warehouse

## Overview

This FastAPI application functions as a data warehouse, managing data synchronization from multiple external APIs, handling webhook inputs, and providing efficient data retrieval. It uses SQLAlchemy with SQLite for data storage, incorporates input validation with Pydantic.

## Features

- CRUD operations for customer and campaign data
- Webhook endpoint for data ingestion
- Data synchronization from CRM and marketing APIs
- Asynchronous processing
- Comprehensive error handling and logging
- Unit and integration testing

## Project Setup

### Prerequisites

- Python 3.8 or later
- `pip` (Python package installer)

### Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/mukeshjain1992/berrydev-challange.git
    cd berrydev-challange
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Database Migrations:**

    ```bash
    alembic upgrade head
    ```

5. **Run the Application:**

    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the Application:**

    Open your browser and navigate to `http://127.0.0.1:8000`. The FastAPI interactive documentation will be available at `http://127.0.0.1:8000/docs`.

## API Endpoints

### POST /webhook

**Description:** Receives data from a webhook. This endpoint accepts data for customers and campaigns and stores it in the database.

**Request:**

```http
POST /webhook
Content-Type: application/json

{
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
```

**Response:**

- **200 OK**

  ```json
  {
    "message": "Webhook received."
  }
  ```

### GET /data

**Description:** Retrieves stored customer and campaign data with pagination.

**Request:**

```http
GET /data?offset=0&limit=10
```

**Response:**

- **200 OK**

  ```json
  {
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
  ```

### GET /sync/{source}

**Description:** Triggers synchronization for a specific data source (`crm` or `marketing`).

**Request:**

```http
GET /sync/crm
```

or

```http
GET /sync/marketing
```

**Response:**

- **200 OK**

  ```json
  {
    "message": "Sync started for CRM data."
  }
  ```

  or

  ```json
  {
    "message": "Sync started for Marketing data."
  }
  ```

### GET /tasks

**Description:** Lists all running background tasks.

**Request:**

```http
GET /tasks
```

**Response:**

- **200 OK**

  ```json
  [
    {
      "task_id": 1,
      "status": "running",
      "source": "crm"
    }
  ]
  ```

### POST /tasks/cancel

**Description:** Cancels a specific background task.

**Request:**

```http
POST /tasks/cancel
Content-Type: application/json

{
  "task_id": 1
}
```

**Response:**

- **200 OK**

  ```json
  {
    "message": "Task cancelled successfully."
  }
  ```

- **422 Unprocessable Entity** (if `task_id` is missing or invalid)

  ```json
  {
    "detail": "Invalid task_id"
  }
  ```

## Testing

### Running Tests

To run the unit and integration tests, use:

```bash
pytest
```

### Test Coverage

Tests cover:
- Webhook data reception
- Data retrieval
- Data synchronization
- Task management

Ensure that the application is running and the database is properly initialized before running tests.

## Usage of AI

- **AI in Data Management:** AI techniques were utilized to optimize data handling and synchronization logic, especially for managing background tasks and ensuring data consistency across different sources.