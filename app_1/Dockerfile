FROM python:3.10.11

WORKDIR app

COPY app_1/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY otel ./otel

COPY app_1/ .