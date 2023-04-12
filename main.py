import time
import os

from data import ImageFromVideo
from data import ImageFromCam

from modules.detect import Detector
from modules.classify import Classifier
from modules.crop import crop_image



import torch

# ImageFromVideo.get_image('data/images/IMG_1031.MOV')


# Initialize a class instance
human_detector = Detector()
dumping_classifier = Classifier()

start = time.time()
# path = "./data/images/"
# for img_path in os.listdir(path):
#     img_path = os.path.join(path, img_path)
with torch.no_grad():
    det = human_detector.detect('data/images/2023_04_12_191946.jpg')

    for i, (*xyxy, conf, cls) in enumerate(reversed(det)):
        print(xyxy, cls)
        # xyxy -> (left_bottom_x, left_bottom_y, right_top_x, right_top_y)
        if cls == 0: # only save an image of person
            crropedImage = crop_image('data/images/2023_04_12_191946.jpg', tuple(map(float, xyxy)))
            pred = dumping_classifier.classify(crropedImage)
            print(pred)
            if pred == "Dumping":
                print('data/images/2023_04_12_191946.jpg')
                # code to save the image in DB
        
print(time.time() - start)
