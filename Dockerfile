# Production Multi-Stage Dockerfile for Universal DCF Engine
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY Finance_FP&A_Portfolio/shared/requirements.txt ./requirements-base.txt
RUN pip install --no-cache-dir --user -r requirements-base.txt
RUN pip install --no-cache-dir --user fastapi uvicorn pydantic pydantic-settings sqlalchemy scipy python-multipart httpx

# Final Minimal Runtime Stage
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

COPY backend/ ./backend/
COPY output/ ./output/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
