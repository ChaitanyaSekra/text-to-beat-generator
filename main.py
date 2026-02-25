# main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from generator import generate_beat
from pathlib import Path

app = FastAPI()
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(prompt_request: PromptRequest):
    prompt = prompt_request.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        filepath = generate_beat(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

    filename = Path(filepath).name
    return {"download_url": f"/download/{filename}"}

@app.get("/download/{filename}")
def download(filename: str):
    path = Path("generated_beats") / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path, media_type="audio/wav", filename=filename)
