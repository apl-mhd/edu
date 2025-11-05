# Inside backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for pip packages, including pycairo deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    # FIX: Add these for pycairo/cairo compilation
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libgirepository1.0-dev \
    && rm -rf /var/lib/apt/lists/*


# Copy dependencies and install
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]