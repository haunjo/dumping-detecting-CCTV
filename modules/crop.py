# Crop an image based on a specific coordinate
from PIL import Image

def crop_image(img, coordinates: tuple) -> Image.Image:
    image = Image.open(img)
    croppedImage = image.crop(coordinates)
    return croppedImage