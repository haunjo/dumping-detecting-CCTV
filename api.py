import main
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/files/")
async def create_file(file : UploadFile):
    content = await file.read()
    
        
    return JSONResponse({"filename" : file.filename})

@app.get("/")
async def root():
    return {"message" : "hello world"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)