from .image_raster_html import ImageRasterHTML
from .image_raster import ImageRaster
from models import Print
from database import db
import os

class PrintImage:
  def __init__(self, template_name: str | None, image: Image | None, attributes: dict = {}):
    self.template_name = template_name
    self.attributes = attributes
    self.image = image

  def call(self) -> bytes:
    # Create the ticket image
    if self.image:
      image = ImageRaster(self.image)
    else:
      image = ImageRasterHTML(template_name=self.template_name, attributes=self.attributes)

    # Save the print to the database
    print = Print(raster_data=image.to_raster_format(), image_width=image.get_width(), image_height=image.get_height())
    db.session.add(print)
    db.session.commit()

    # Enqueue the print for printing
    enqueue_print(print.id)

    if os.getenv("PYTHON_ENV") == "production":
      image.remove_tmp_image()

    return print.id