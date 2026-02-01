# Dockerfile
FROM python:3.11-slim

# Basic system deps (often needed by sentencepiece)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code + model artifacts into the image
COPY infer.py .
COPY models ./models

# Default command shows help; grader can pass args to override
ENTRYPOINT ["python", "infer.py"]
