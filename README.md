
-----

# FastAPI Starter Code

A robust, production-ready FastAPI foundation using SQLAlchemy 2.0 and Alembic for database version control.

## Features

  * **Authentication:** JWT Token-based security with `python-jose` and `passlib`.
  * **User Management:** Register (`POST /users`), Login (`POST /login`), and profile retrieval (`GET /me`).
  * **Database Migrations:** Managed by Alembic (no `create_all` hacks).
  * **Input Validation:** Strict data typing and validation using Pydantic v2.
  * **CORS Enabled:** Pre-configured for local development with React/Vue/Next.js.
  * **Environment Safety:** Centralized configuration using `.env` files.

-----

## Setup & Installation

### 1\. Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2\. Configuration

Create a `.env` file in the root directory:

```env
DB_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_super_secret_random_string
ALGORITHM=HS256
```

-----

## Database Migrations (Alembic)

We use Alembic to handle database schema changes. This ensures your database stays in sync across different environments without losing data.

### First Time Setup

If you are starting with a fresh database, run the following to create your tables:

```bash
# Generate the initial migration script
alembic revision --autogenerate -m "Initial migration"

# Apply the migration to the database
alembic upgrade head
```

### Making Changes

Whenever you modify `schemas.py` (e.g., adding a new column or changing a data type):

1.  **Generate a script:**
    `alembic revision --autogenerate -m "add phone to user"`
2.  **Review the script:** Check `alembic/versions/` to ensure the `upgrade` and `downgrade` logic is correct.
3.  **Apply the change:**
    `alembic upgrade head`

### Common Commands

| Command | Action |
| :--- | :--- |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Revert the very last migration |
| `alembic current` | Show the current revision of your DB |
| `alembic history` | Show a log of all migrations |

-----

## Running the Application

Start the development server with hot-reload enabled:

```bash
uvicorn app.main:app --reload
```

The API documentation will be available at:

  * **Swagger UI:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
  * **ReDoc:** [http://localhost:8000/redoc](https://www.google.com/search?q=http://localhost:8000/redoc)

-----

## Project Structure

  * `app/schemas.py`: SQLAlchemy database schemas.
  * `app/models.py`: Pydantic schemas for request/response validation.
  * `app/routers/`: Modularized API endpoints.
  * `alembic/`: Database migration history and configuration.
  * `static/`: Placeholder for static file serving.

-----