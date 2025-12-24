FROM python:3-slim

WORKDIR /app

# Build deps for psycopg2-binary (libpq headers) and compiling wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    pkg-config \
    chromium \
    libjpeg-dev \
    libpng-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]

