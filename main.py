import time
import os

from data import ImageFromVideo
from data import ImageFromCam
from modules.detect import Detector
from modules.classify import Classifier
from modules.crop import crop_image

import torch
#ImageFromVideo.get_image('data/video/2023032319.mov')

# Initialize a class instance
human_detector = Detector()
dumping_classifier = Classifier()

start = time.time()
path = "./data/images/2023_04_01_15"
for img_path in os.listdir(path):
    img_path = os.path.join(path, img_path)
    with torch.no_grad():
        det = human_detector.detect(img_path)

    for i, (*xyxy, conf, cls) in enumerate(reversed(det)):
        # xyxy -> (left_bottom_x, left_bottom_y, right_top_x, right_top_y)
        if cls == 0: # only save an image of person
            crropedImage = crop_image(img_path, tuple(map(float, xyxy)))
            pred = dumping_classifier.classify(crropedImage)
            print(pred)
            if pred == "Dumping":
                print(img_path)
                # code to save the image in DB
        
print(time.time() - start)