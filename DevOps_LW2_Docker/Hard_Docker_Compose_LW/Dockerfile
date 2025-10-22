FROM python:3.12-slim
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install -r requirements.txt
