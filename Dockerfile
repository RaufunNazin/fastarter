FROM python:3.13-slim

# Install system dependencies (required for some python packages like psycopg2 or bcrypt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Use a shell script or a combined command to handle migrations and seeding before startup
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000