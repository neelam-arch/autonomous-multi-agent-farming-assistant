import os
import uuid
import json
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from graph import run_agriculture_assistant
from typing import Optional

app = FastAPI(title="Agriculture Assistant API")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/chat")
async def chat(
    message: str = Form(...),
    history: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    image_path = None
    if image:
        ext = image.filename.split(".")[-1]
        image_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{ext}")
        with open(image_path, "wb") as f:
            f.write(await image.read())
            
    history_list = []
    if history:
        try:
            history_list = json.loads(history)
        except Exception:
            history_list = []

    response = run_agriculture_assistant(message, image_path, history=history_list)
        
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
