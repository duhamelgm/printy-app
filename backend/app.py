import os

from flask import Flask, jsonify
from flask_alembic import Alembic
from redis import Redis
from database import db
from models import *
from ticket_image import TicketImage
from printing_queue import enqueue_print

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    db.init_app(app)
    alembic = Alembic()
    alembic.init_app(app)

    @app.post("/print/ticket")
    def create_ticket_print():
        # Create the ticket image
        ticket_image = TicketImage(template_name="ticket")
        raster_data = ticket_image.to_raster_format()

        # Save the print to the database
        print = Print(raster_data=raster_data, image_width=ticket_image.get_width(), image_height=ticket_image.get_height())
        db.session.add(print)
        db.session.commit()

        # Enqueue the print for printing
        enqueue_print(print.id)

        ticket_image.remove_tmp_image()

        return jsonify({"status": "ok", "print_id": print.id})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5000)