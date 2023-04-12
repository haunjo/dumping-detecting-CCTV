# Crop an image based on a specific coordinate
import numpy as np

from PIL import Image


def crop_image(source: np.ndarray, coordinates: tuple) -> Image.Image:
    image = Image.fromarray(source)
    croppedImage = image.crop(coordinates)
    return croppedImage