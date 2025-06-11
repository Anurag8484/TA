# Dockerfile

FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    curl \
    build-essential \
    && apt-get clean

# Install uv globally
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies globally using uv
RUN uv venv --system-site-packages && uv pip install -r requirements.txt

# Expose port required by university evaluation
EXPOSE 8000

# Run the Flask app on container startup
CMD ["uv", "run", "-m", "app.api.app"]
