# --- Base image ---
FROM python:3.12-slim

# --- Environment variables ---
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/usr/src/security-platform-backend

# --- Set working directory ---
WORKDIR $APP_HOME

# --- Copy requirements and install dependencies ---
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- Copy the entire project ---
COPY . .

# --- Expose port ---
EXPOSE 8099

# --- Run Alembic migrations
CMD ["alembic", "upgrade", "head"]

# --- Start the Hypercorn server ---
CMD ["hypercorn", "project.app:app", "--bind", "0.0.0.0:8099", "--workers", "1", "--log-level", "info"]
