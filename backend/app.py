import os
from typing import Dict

from flask import Flask, jsonify
from peewee import PostgresqlDatabase
from redis import Redis


def create_app() -> Flask:
    app = Flask(__name__)

    db_url = os.getenv("DATABASE_URL")
    redis_url = os.getenv("REDIS_URL")

    # Use peewee URL helper so DSNs like postgresql://user:pass@host:port/db work
    db = PostgresqlDatabase.from_url(db_url)
    redis_client = Redis.from_url(redis_url)

    def check_postgres() -> bool:
        try:
            db.connect(reuse_if_open=True)
            db.execute_sql("SELECT 1;")
            return True
        finally:
            if not db.is_closed():
                db.close()

    def check_redis() -> bool:
        redis_client.ping()
        return True

    def health_response() -> Dict[str, Dict[str, bool] | str]:
        postgres_ok = check_postgres()
        redis_ok = check_redis()
        overall_ok = postgres_ok and redis_ok
        status_code = 200 if overall_ok else 503
        payload = {
            "status": "ok" if overall_ok else "unhealthy",
            "services": {"postgres": postgres_ok, "redis": redis_ok},
        }
        return payload, status_code

    @app.route("/health", methods=["GET"])
    @app.route("/api/health", methods=["GET"])
    def health():
        payload, status_code = health_response()
        return jsonify(payload), status_code

    return app


app = create_app()


if __name__ == "__main__":
    # For local debugging; in containers the command is set in Dockerfile
    app.run(host="0.0.0.0", port=5000, debug=True)

