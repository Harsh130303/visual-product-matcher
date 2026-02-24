# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user (Hugging Face requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Copy everything from root
COPY --chown=user . .

# Install dependencies from the copied backend folder
RUN pip install --no-cache-dir -r backend/requirements.txt

# The code expects 'data' to be accessible relative to the app
# Our new path logic in database.py will check both 'data/' and '../data/'

# Expose port 7860
EXPOSE 7860

# Command to run the application
# We run from the root, so we need to point to backend.main:app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
