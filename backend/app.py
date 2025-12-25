import os

from flask import Flask, jsonify
from flask_alembic import Alembic
from redis import Redis
from database import db
from models import *
from ticket_image import TicketImage
from printing_queue import enqueue_print
from pydantic import BaseModel
from flask_pydantic import validate
from flask_cors import CORS
import random
from datetime import datetime, timedelta

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

        # Create the token image
        token_image = TicketImage(template_name="token", attributes={ "token": token.value })
        raster_data = token_image.to_raster_format()
        token_image.remove_tmp_image()

        # Save the print to the database
        print = Print(raster_data=raster_data, image_width=token_image.get_width(), image_height=token_image.get_height())
        db.session.add(print)
        db.session.commit()

        # Enqueue the print for printing
        enqueue_print(print.id)

        return jsonify({"status": "ok", "payload": { "token": token.value }})

    class TicketPrintRequestBody(BaseModel):
        title: str
        description: str
        assignee: str
        priority: str

    @app.post("/v1/print/ticket")
    @validate()
    def create_ticket_print(body: TicketPrintRequestBody):        
        # Create the ticket image
        ticket_image = TicketImage(template_name="ticket", attributes=body.model_dump())
        raster_data = ticket_image.to_raster_format()

        # Save the print to the database
        print = Print(raster_data=raster_data, image_width=ticket_image.get_width(), image_height=ticket_image.get_height())
        db.session.add(print)
        db.session.commit()

        # Enqueue the print for printing
        enqueue_print(print.id)

        ticket_image.remove_tmp_image()

        return jsonify({"status": "ok", "payload": { "print_id": print.id }})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5000)