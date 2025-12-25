import os

from flask import Flask, jsonify
from flask_alembic import Alembic
from redis import Redis
from database import db
from models import *
from services import PrintImage
from printing_queue import enqueue_print
from pydantic import BaseModel
from flask_pydantic import validate
from flask_cors import CORS
import random
from datetime import datetime, timedelta
from auth import authorized

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    db.init_app(app)
    alembic = Alembic()
    alembic.init_app(app)

    class AuthTokenRequestBody(BaseModel):
        duration_days: int
        password: str

    @app.post("/v1/auth/token")
    @validate()
    def create_auth_token(body: AuthTokenRequestBody):
        # Check if the password is correct
        if body.password != os.getenv("ADMIN_PASSWORD"):
            return jsonify({"status": "error", "message": "Invalid password"}), 401

        # Create a new token
        token = Token(value=f"{random.randint(100, 999)}-{random.randint(100, 999)}", expires_at=datetime.now() + timedelta(days=body.duration_days))
        db.session.add(token)
        db.session.commit()

        print_id = PrintImage(template_name="token", attributes={ "token": token.value }).call()
        return jsonify({"status": "ok", "payload": { "token": token.value }})

    @app.post("/v1/auth/verify")
    @authorized()
    def verify_auth_token():
        return jsonify({"status": "ok"})

    class TicketPrintRequestBody(BaseModel):
        title: str
        description: str
        assignee: str
        priority: str

    @app.post("/v1/print/ticket")
    @authorized()
    @validate()
    def create_ticket_print(body: TicketPrintRequestBody):        
        print_id = PrintImage(template_name="ticket", attributes=body.model_dump()).call()
        return jsonify({"status": "ok", "payload": { "print_id": print_id }})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5000)