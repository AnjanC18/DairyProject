# Use secure and compatible base image
FROM python:3.9.18-slim-bullseye

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install system dependencies required by reportlab and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
