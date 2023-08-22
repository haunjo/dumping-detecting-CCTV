from fastapi import FastAPI, File, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import cv2
import torch
import base64
import numpy as np
import pymysql
import threading
import time
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
from data.Send_S3 import send_s3
from data.Send_mysql import send_mysql
from modules.detect import Detector
from modules.classify import Classifier
from modules.crop import crop_image


human_detector = Detector()
dumping_classifier = Classifier()


app = FastAPI()

def connect(id, contents):
    conn = pymysql.connect(
        host='43.200.109.246',
        user='johaun', 
        password='8312', 
        db= 'SCV', 
        charset='utf8')
    send_mysql(id, contents, conn)
    conn.close()


#이미지를 전달받아 분류 알고리즘 실행
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
                send_s3(pil_image, content["filename"])
                print(content["filename"])
                connect(content["cctvid"], content["filename"])
                #print(cnt, pred, prob, xyxy)
                return JSONResponse({"filename" : content["filename"], "action" : pred, "prob" : prob/100})
                # code to save the image in DB
            #connect(content["filename"])
    return JSONResponse({"filename" : content["filename"], "action" : "None"})

#API 통신 테스트를 위한 default 함수
@app.get("/")
async def root():
    return {"message" : "hello world"}




    