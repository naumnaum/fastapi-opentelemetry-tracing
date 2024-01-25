FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim-2024-01-22

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
