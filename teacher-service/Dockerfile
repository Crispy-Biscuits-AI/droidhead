# ─────────────────────────────────────────────
# Stage 1: Runtime image
# ─────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Prevent Python from writing .pyc files & enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Optional: ensure UTF-8 everywhere
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Create app directory
WORKDIR /app

# System deps (build tools kept minimal)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency file(s)
# If you're using Poetry, swap this for pyproject.toml + poetry.lock
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# ─────────────────────────────────────────────
# Environment configuration
# ─────────────────────────────────────────────
# Where the GPT-OSS teacher lives (your LLM backend container)
ENV GPT_OSS_BASE_URL="http://gpt-oss:8080/v1"
ENV TEACHER_MODEL_NAME="gpt-oss:20b"

# Service runtime config
ENV TEACHER_PORT=8000

# ─────────────────────────────────────────────
# Expose port & default command
# ─────────────────────────────────────────────
EXPOSE 8000

# Assuming your FastAPI app lives at app/main.py with object "app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

