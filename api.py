from fastapi import FastAPI, File, Request
from fastapi.responses import JSONResponse
import cv2
import torch
import time
import os
import base64
import numpy as np
from io import BytesIO
from PIL import Image

from data import ImageFromVideo
from data import ImageFromCam
from data import Send_S3
from modules.detect import Detector
from modules.classify import Classifier
from modules.crop import crop_image

import torch


app = FastAPI()


@app.post("/files/")
async def create_file(file : Request):
    content = await file.json()
    img_data = base64.b64decode(content["image"])
    pil_image = Image.open(BytesIO(img_data))
    cv_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    with torch.no_grad():
        det = human_detector.detect(cv_img)
    for i, (*xyxy, conf, cls) in enumerate(reversed(det)):
        # xyxy -> (left_top_x, left_top_y, right_bottom_x, right_bottom_y)
        if cls == 0: # only save an image of person
            crropedImage = crop_image(cv_img, tuple(map(float, xyxy)))
            pred, prob = dumping_classifier.classify(crropedImage)
            if pred == "throwing away" and prob >= 70:
                Send_S3.send_s3(pil_image, content["filename"])
                #print(cnt, pred, prob, xyxy)
                return JSONResponse({"filename" : content["filename"], "action" : pred, "prob" : prob/100})
                # code to save the image in DB
            Send_S3.send_s3(pil_image, content["filename"])
    return JSONResponse({"filename" : content["filename"], "action" : "None"})

@app.get("/")
async def root():
    return {"message" : "hello world"}

if __name__ == "__main__":
    human_detector = Detector()
    dumping_classifier = Classifier()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)
    