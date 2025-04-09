FROM python:3.9.18-slim-bullseye

WORKDIR /app

# Copy only requirement file first to use Docker layer cache
COPY requirements.txt .

# Install system + Python dependencies
RUN apt-get update && apt-get install -y \
    gcc libffi-dev libfreetype6-dev libjpeg-dev zlib1g-dev \
    python3-dev build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# THEN copy the rest of the app
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
