import os
import uuid
from datetime import datetime
from PIL import Image, ImageOps
import numpy as np
from html2image import Html2Image
from liquid import render
import random

class ImageRasterHTML:
    def __init__(self, template_name: str, attributes: dict):
        self.template_name = template_name
        self.image_name = f"{str(uuid.uuid4())}.png"
        self.tmp_image_path = f"/app/tmp/{self.image_name}"
        self.attributes = attributes
        self.save_image_from_html()
        self._im = self.crop_and_prepare_image()

    def save_image_from_html(self) -> None:
        hti = Html2Image(
          size=(576, 2000), 
          custom_flags=[
            "--no-sandbox",         
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-features=UseDBus",
            "--disable-setuid-sandbox"
          ],
          output_path="/app/tmp"
        )

        html_str = open(f"/app/templates/{self.template_name}.html", "r").read()
        html_str = render(html_str, **{ **self.attributes, "timestamp": datetime.now().isoformat(), "ticket_id": f"HOME-{random.randint(100, 999)}" })

        hti.screenshot(html_str=html_str, save_as=self.image_name)

    def crop_and_prepare_image(self) -> Image:
        # open the PNG again, and crop it to the content.
        img = Image.open(self.tmp_image_path)
        img_rgb = img.convert("RGB")

        # Make a mask where all nonblack are white (1)
        arr = np.array(img_rgb)
        is_not_black = np.any(arr != [0,0,0], axis=-1)
        
        mask = Image.fromarray((is_not_black*255).astype("uint8"))
        bbox = mask.getbbox()
        img = img.crop(bbox)

        img = img.convert("L")  # convert to grayscale
        threshold = 254  # Lower value -> more pixels go to black
        img.point(lambda x: 255 if x > threshold else 0, mode="1")
        img = ImageOps.invert(img)
        img = img.convert("1")

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