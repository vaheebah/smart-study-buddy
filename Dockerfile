# Use Python slim image
FROM python:3.11-slim

# Install system dependencies required for FAISS & sentence-transformers
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create required folders
RUN mkdir -p faiss_index uploads models

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
