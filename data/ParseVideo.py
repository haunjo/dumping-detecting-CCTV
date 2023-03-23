import cv2
import os

def get_video(path:str):
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

    try:
        if not os.path.exists(filepath[-10:-4]):
            os.makedirs("data/images/"+filepath[-10:-4])
    except OSError:
        print("Directory is already exists : " + filepath[-10:-4])
    
    count = 0
    
    while(video.isOpened()):
        ret, frame = video.read()
        if(int(video.get(1))% int(fps) == 0):
            cv2.imwrite("data/images/" + filepath[-10:-4] + f"/{filepath[-10:-4]}%0d.jpg"% count, frame)
            print("Saved frame number:" , str(int(video.get(1))))
            count += 1
        if(ret == False):
            break
    video.release()

