FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDOWNWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .