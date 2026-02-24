# Use official Hugging Face base image with torch and transformers pre-installed
FROM huggingface/transformers-cpu:latest

# Set working directory
WORKDIR /app

# Install system dependencies (some are already there, but we ensure)
USER root
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user (Hugging Face requirement)
# The base image might already have a user, but we ensure ours exists
RUN useradd -m -u 1000 user || echo "User already exists"
USER user
ENV PATH="/home/user/.local/bin:$PATH"
ENV PYTHONPATH="/app/backend"

# Copy everything from root
COPY --chown=user . .

# Install only the lightweight dependencies not in the base image
RUN pip install --no-cache-dir fastapi uvicorn python-multipart requests pydantic pillow scikit-learn numpy

# Expose port 7860
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
