import os,sys
from pathlib import Path
from PIL import Image, ImageOps

# Silly debugging code. Will remove when I figure out what version(s) of Pillow play nice
try:
     Resampling = Image.Resampling
except AttributeError:
     Resampling = Image

def resize_image(image: Image.Image, target_size: int = 1000) -> Image.Image:
      """
      Resizes an image such that it's longest size equals 'target_size' (default 1000px)
      """

      # Determine current diensions
      width, height = image.size

      # Scale factors based on longest dimension
      scale = target_size / max(width, height)

      # Compute proportioned sizes
      new_height = round(height * scale)
      new_width = round(width * scale)

      # Returns the image
      return image.resize((new_width, new_height), Resampling.LANCZOS)


def place_image(image: Image.Image) -> Image.Image:
     """
     Places image on 1000x1000 white canvas and returns the image.
     """
     canvas = Image.new("RGB", (1000, 1000), (255, 255, 255)) # Creates a 1000 x 1000 white canvas with no alhpa channel 
     
     canvas_width, canvas_height = canvas.size
     image_width, image_height = image.size

     x = int((canvas_width - image_width) / 2)
     y = int((canvas_height - image_height) / 2)

     mask = img if img.mode in ("RGBA", "LA") else None

     canvas.paste(image, (x,y), mask)
     return(canvas)


ROOT_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = ROOT_DIR/"samples"/"input"
OUTPUT_DIR = ROOT_DIR/"samples"/"output"


for img_path in INPUT_DIR.iterdir():
    if img_path.suffix.lower() in (".jpg", ".jpeg", ".png"):
           with Image.open(img_path) as img:
                stem = img_path.stem # Everything before the file extension
                img = ImageOps.exif_transpose(img)
                if img.mode in {"RGBA", "LA"} or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGBA")
                else:
                     img = img.convert("RGB")
                img = resize_image(img)
                img = place_image(img)
                out_path = OUTPUT_DIR / f"{stem}.jpg"
                img.save(out_path, "JPEG", quality = 90) 