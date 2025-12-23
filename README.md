# Printy App Boilerplate

Dockerized starter stack with a Flask backend, placeholder frontend folder, PostgreSQL, and Redis.

## Structure
- `backend/`: Flask app with a simple health check.
- `frontend/`: Empty placeholder for future UI.
- `docker-compose.yml`: Orchestrates backend, Postgres, Redis.

## Getting Started
1) Build and start the stack:
```bash
docker compose up --build
```

2) Check health endpoint:
- http://localhost:5000/health

## Environment
- Postgres: `postgres:postgres@db:5432/postgres`
- Redis: `redis://redis:6379/0`

## Backend Development (optional)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
FLASK_APP=app.py flask run --port 5000
```

