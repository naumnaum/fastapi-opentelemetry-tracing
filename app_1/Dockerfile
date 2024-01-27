#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim-2024-01-22
FROM python:3.10.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .