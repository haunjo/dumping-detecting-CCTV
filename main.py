from data import ImageFromVideo
from data import ImageFromCam
from fastapi import FastAPI

from modules.detect_person import detect
from modules.classify import classify


import torch
#ImageFromVideo.get_image('data/video/2023032319.mov')

if __name__ == "__main__":
    for img_path in ImageFromVideo.get_image('data/images/IMG_1031.MOV'): # get image path each second.
        with torch.no_grad():
            detect(img_path)
        try:
            classify(img_path)
        except FileNotFoundError as e:
            print(e)
# ImageFromCam.get_image()


