# syntax=docker/dockerfile:1
FROM python:3.11-slim as builder
WORKDIR /app
COPY ./app /app/app
COPY pyproject.toml requirements.txt* ./
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./app /app/app
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
