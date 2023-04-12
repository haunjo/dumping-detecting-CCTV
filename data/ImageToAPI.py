import ImageFromCam
import ImageFromVideo
import requests

url =  "http://203.253.13.20:8000/files/"
filename = "images/2023_04_12_191946.jpg"

with open(filename, "rb") as f:
    contents = f.read()

files = {"file" : (filename, contents, "image/jpg")}

response = requests.post(url, files = files)
print(response.json())



