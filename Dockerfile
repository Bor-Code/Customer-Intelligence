FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/
RUN uv pip install --system -e .

EXPOSE 8000 8501
