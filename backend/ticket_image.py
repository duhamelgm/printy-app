import os
import uuid
from PIL import Image
import numpy as np
from html2image import Html2Image

class TicketImage:
    def __init__(self, template_name: str):
        self.template_name = template_name
        self.image_name = f"{str(uuid.uuid4())}.png"
        self.tmp_image_path = f"/app/tmp/{self.image_name}"

        self.save_image_from_html()
        self._im = self.crop_and_prepare_image()

    def save_image_from_html(self) -> None:
        hti = Html2Image(
          size=(576, 1000), 
          custom_flags=[
            "--no-sandbox",         
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-features=UseDBus",
            "--disable-setuid-sandbox"
          ],
          output_path="/app/tmp"
        )
        hti.screenshot(html_str=open(f"/app/templates/{self.template_name}.html", "r").read(), save_as=self.image_name)

    def crop_and_prepare_image(self) -> Image:
        # open the PNG again, and crop it to the content.
        img = Image.open(self.tmp_image_path)

        # Crop away all black in the image (assumes black is RGB (0,0,0) or RGBA (0,0,0,255))
        # Create a mask for all pixels not black, then get the bounding box
        if img.mode in ("RGBA", "LA"):
            # Ignore alpha, just use RGB
            bg = (0, 0, 0, 255) if img.mode == "RGBA" else (0, 0, 0, 255)
        else:
            bg = (0, 0, 0)
        # Create mask: white where not black, black where black
        def not_black(pixel):
            return pixel[:3] != (0, 0, 0)
        # If RGBA, convert to RGB and ignore alpha
        if img.mode not in ("RGB", "RGBA"):
            img_rgb = img.convert("RGB")
        else:
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