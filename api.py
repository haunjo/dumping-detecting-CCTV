import main
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2

app = FastAPI()

@app.post("/files/")
async def create_file(file : UploadFile):
    content = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    with torch.no_grad():
        det = human_detector.detect(img)
    for i, (*xyxy, conf, cls) in enumerate(reversed(det)):
        # xyxy -> (left_bottom_x, left_bottom_y, right_top_x, right_top_y)
        if cls == 0: # only save an image of person
            crropedImage = crop_image(img_path, tuple(map(float, xyxy)))
            pred = dumping_classifier.classify(crropedImage)
            print(pred)
            if pred == "Dumping":
                print(img_path)
    return JSONResponse({"filename" : file.filename})

@app.get("/")
async def root():
    return {"message" : "hello world"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)