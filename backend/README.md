# Marcus's Bicycle E-commerce Platform - Backend

This directory contains the Python FastAPI backend for the custom bicycle e-commerce platform.

## Setup

1.  Create a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment variables:
    *   Copy `.env.example` to `.env`.
    *   Fill in the required values in `.env` (especially `DATABASE_URL`).
4.  Set up the PostgreSQL database specified in `DATABASE_URL`.
5.  Apply database migrations:
    ```bash
    alembic upgrade head
    ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

## Running Tests

```bash
pytest
``` 