# Dockerfile - for huggingface deployment
FROM python:3.9-slim

WORKDIR /code

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and set permissions for data directory
RUN mkdir -p /code/data && \
    chown -R appuser:appuser /code/data

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set ownership of the application files
RUN chown -R appuser:appuser /code

# Switch to non-root user
USER appuser

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
