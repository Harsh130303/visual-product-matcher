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

# Create a non-root user for security (Hugging Face requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Copy requirements and install dependencies
# We assume the build context is the repository root
COPY --chown=user backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code and data
COPY --chown=user backend/ .
COPY --chown=user data/ /app/data

# Ensure the data path is correctly set in environment if needed, 
# but our code uses relative paths (.. from backend), so we need to match that structure.
# Currently database.py uses: os.path.join(os.path.dirname(__file__), "..", "data", "products.json")
# If main.py is in /app/, then __file__ is /app/main.py. 
# dirname is /app/. ".." from /app/ is /. So it looks for /data/products.json.
# Let's adjust the COPY to match the expected structure.

USER root
RUN mkdir -p /data && chown user:user /data
USER user
COPY --chown=user data/ /data/

# Expose the port FastAPI will run on
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
