# Use an official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    APP_PROFILE=dev \
    GEMINI_API_KEY=<REPLACE_ME> \
    GOOGLE_APPLICATION_CREDENTIALS=<REPLACE_ME>

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    portaudio19-dev \  
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set PYTHONPATH so that local modules can be found
ENV PYTHONPATH=/app/src:$PYTHONPATH

WORKDIR /app

# COPY requirements.txt .
# Copy only the necessary files first for layer caching
COPY pyproject.toml poetry.lock ./

# RUN pip install -r requirements.txt

# Install dependencies
RUN poetry install --no-root --only main

COPY . .

# Run your application (replace with your actual entrypoint)
CMD ["python3", "run.py"]