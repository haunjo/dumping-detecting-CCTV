import cv2
import time
import os
import shutil
path = "./data/images/2023_04_13_22/"

import torch

from data import ImageFromVideo
from data import ImageFromCam
from modules.detect import Detector
from modules.classify import Classifier
from modules.crop import crop_image


save_path = "./data/images/"

total = 0

human_detector = Detector()
dumping_classifier = Classifier()

print("Start")
# for i in range(10):
start = time.time()
cnt = 1
for img_path in os.listdir(path):
    src = os.path.join(path, img_path)
    image = cv2.imread(src)
    with torch.no_grad():
        det = human_detector.detect(image)

    for i, (*xyxy, conf, cls) in enumerate(reversed(det)):
        # xyxy -> (left_top_x, left_top_y, right_bottom_x, right_bottom_y)
        if cls == 0: # only save an image of person
            crropedImage = crop_image(image, tuple(map(float, xyxy)))
            pred, prob = dumping_classifier.classify(crropedImage)
#             if pred == "not throwing away":
            if pred == "throwing away" and prob >= 76:
                dest = os.path.join(save_path, pred)
                dest = os.path.join(dest, img_path)
                try:
                    shutil.copyfile(src, dest)
                except FileExistsError as e:
                    print(e)
                # print(f"{img_path} is saved.")
                print(cnt, pred, prob, img_path, xyxy)
                
                cnt += 1
                break
                # code to save the image in DB

#     total += (time.time() - start)
    
# print(f"avg: {total/10}s")

print("End")