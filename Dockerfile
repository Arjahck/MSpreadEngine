# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (build-essential for numpy/scipy if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Note: Pinning versions to avoid the NumPy 2.0 / SciPy issue
COPY requirements.txt .
RUN pip install --no-cache-dir "numpy<2.0.0" "scipy" "networkx" "fastapi" "uvicorn[standard]" "pydantic<2.0.0" "websockets" "tqdm"

# Copy project
COPY . .

# Expose the API port
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py", "run", "--host", "0.0.0.0", "--port", "8000"]