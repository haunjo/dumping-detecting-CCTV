import cv2
import os
from time import localtime
from time import strftime

def get_image(path:str):
    print(cv2.__version__)
    print(" ======= Parsing Video data is : ", path)
    if path:
        filepath = path
    else:
        filepath = '2023032319.mov'

    video = cv2.VideoCapture(f'{filepath}')

    if not video.isOpened():
        print("Could not Open :", filepath)
        exit(0)
        
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    
    print("length :", length)
    print("width :", width)
    print("height :", height)
    print("fps :", fps, "\n")

    currunt_time = localtime()
    timestamp = strftime('%Y_%m_%d_%H', currunt_time)
    try:
        if not os.path.exists(timestamp):
            os.makedirs("data/images/"+timestamp)
    except OSError:
        print("Directory is already exists : " + timestamp)
    
    count = 0
    
    while(video.isOpened()):
        ret, img = video.read()
        if(int(video.get(1))% int(fps) == 0):
            tm = localtime()
            capturedtime = strftime('%Y_%m_%d_%H%M%S', tm)
            cv2.imwrite(f'data/images/{timestamp}/{capturedtime}.jpg', img)
            print("Saved frame number:" , str(int(video.get(1))))
            count += 1
            yield f'data/images/{timestamp}/{capturedtime}.jpg' # yield path of image
        if(ret == False):
            break
    video.release()

