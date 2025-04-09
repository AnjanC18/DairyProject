FROM python:3.9-alpine

WORKDIR /app
COPY . /app

# Install required system packages for dependencies like reportlab
RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev py3-pip build-base freetype-dev

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
