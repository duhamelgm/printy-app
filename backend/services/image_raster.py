import os
import uuid
from datetime import datetime
from PIL import Image, ImageOps
import numpy as np
from html2image import Html2Image
from liquid import render
import random

PRINTER_WIDTH = 576

class ImageRaster:
    def __init__(self, image: Image):
        self.image = image
        self.tmp_image_path = f"/app/tmp/{str(uuid.uuid4())}.png"
        self._im = self.prepare_image()

    def prepare_image(self) -> Image:
        # open the PNG again, and crop it to the content.
        img = self.image
        img = img.convert("RGB")

        # Choose orientation that yields the largest printable area (height is unbounded, width is capped at PRINTER_WIDTH).
        height_no_rotation = img.height * PRINTER_WIDTH / img.width
        height_if_rotated = img.width * PRINTER_WIDTH / img.height

        if height_if_rotated > height_no_rotation:
            img = img.rotate(90, expand=True)
        
        img = img.resize((PRINTER_WIDTH, int(img.height * PRINTER_WIDTH / img.width)))
        img = img.convert("L")  # convert to grayscale
        img = img.convert("1", dither=Image.FLOYDSTEINBERG)
        img = ImageOps.invert(img)

        img.save(self.tmp_image_path)

        return img

    def get_width(self) -> int:
      return self._im.width

    def get_height(self) -> int:
      return self._im.height

    def to_raster_format(self) -> bytes:
      return self._im.tobytes()

    def remove_tmp_image(self) -> None:
      os.remove(self.tmp_image_path)