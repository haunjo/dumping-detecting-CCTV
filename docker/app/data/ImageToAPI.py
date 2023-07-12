import ImageFromCam
import ImageFromVideo

import requests
import base64
import cv2
import json



url =  "http://haunserver.shop/files/"


def VideoToAPI():
    for data in ImageFromVideo.get_image('test.mp4'):
        _, img_encoded = cv2.imencode('.jpg', data["image"])
        img_str = base64.b64encode(img_encoded).decode('utf-8')
        request = {"image": img_str, "filename" : f'{data["filename"]}'}
        response = requests.post(url, data=json.dumps(request))
def CamToAPI(): 
    for data in ImageFromCam.get_image():
        _, img_encoded = cv2.imencode('.jpg', data["image"])
        img_str = base64.b64encode(img_encoded).decode('utf-8')
        request = {"image": img_str, "filename" : f'{data["filename"]}'}
        response = requests.post(url, data=json.dumps(request))

if __name__=="__main__":
    #VideoToAPI()
    CamToAPI()

