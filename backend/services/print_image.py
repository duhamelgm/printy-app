from .image_raster import ImageRaster
from models import Print
from database import db
from printing_queue import enqueue_print
import os

class PrintImage:
  def __init__(self, template_name: str, attributes: dict):
    self.template_name = template_name
    self.attributes = attributes

  def call(self) -> bytes:
    # Create the ticket image
    image = ImageRaster(template_name=self.template_name, attributes=self.attributes)

    # Save the print to the database
    print = Print(raster_data=image.to_raster_format(), image_width=image.get_width(), image_height=image.get_height())
    db.session.add(print)
    db.session.commit()

    # Enqueue the print for printing
    enqueue_print(print.id)

    if os.getenv("PYTHON_ENV") == "production":
      image.remove_tmp_image()

    return print.id