import os
import sys
import json
import time
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

from scripts.pipeline_helper import extract_last_frame, stitch_and_polish
from studio.generator import (
    get_next_episode_id,
    load_ideas,
    get_joke_by_id,
    generate_prompt_for_joke,
    build_flow_prompt,
    CHARACTERS,
    HISTORY_LEDGER_PATH
)

app = FastAPI(title="Dost Comedy Studio (Shani & Mani)")

STATIC_DIR = BASE_DIR / "studio" / "static"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/temp", StaticFiles(directory=str(TEMP_DIR)), name="temp")
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

class CustomJokeRequest(BaseModel):
    title: str
    location: str
    prop: str
    speaker_00: str
    dialogue_00: str
    speaker_03: str
    dialogue_03: str

@app.get("/")
def read_root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return JSONResponse({"status": "Dost Comedy Studio Running on Port 8060"})

@app.get("/api/jokes")
def get_jokes():
    return JSONResponse(load_ideas())

@app.get("/api/characters")
def get_characters():
    return JSONResponse(CHARACTERS)

@app.post("/api/generate-prompt")
def generate_prompt_endpoint(req: CustomJokeRequest):
    prompt = build_flow_prompt(
        req.speaker_00, req.dialogue_00,
        req.speaker_03, req.dialogue_03,
        req.location, req.prop
    )
    return JSONResponse({
        "status": "success",
        "prompt": prompt,
        "title": req.title
    })

@app.get("/api/joke-prompt/{joke_id}")
def get_prompt_for_preloaded_joke(joke_id: str):
    joke = get_joke_by_id(joke_id)
    if not joke:
        raise HTTPException(status_code=404, detail="Joke not found")
    prompt = generate_prompt_for_joke(joke)
    return JSONResponse({
        "status": "success",
        "joke": joke,
        "prompt": prompt
    })

def scan_downloads_folder():
    folders = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Downloads/Video"),
        os.path.expanduser("~/Downloads/flow-auto")
    ]
    candidates = []
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for f in os.listdir(folder):
            if f.endswith(".mp4"):
                full = os.path.join(folder, f)
                try:
                    mtime = os.path.getmtime(full)
                    size = os.path.getsize(full)
                    candidates.append({
                        "name": f,
                        "path": full,
                        "mtime": mtime,
                        "size_mb": round(size / (1024 * 1024), 2),
                        "folder": folder
                    })
                except Exception:
                    pass
    candidates.sort(key=lambda x: x["mtime"], reverse=True)
    return candidates[:25]

@app.get("/api/recent-downloads")
def get_recent_downloads():
    return JSONResponse(scan_downloads_folder())

if __name__ == "__main__":
    import uvicorn
    print("\n========================================================")
    print("       STARTING DOST COMEDY STUDIO (SHANI & MANI)")
    print("========================================================")
    print("URL: http://localhost:8060\n")
    uvicorn.run(app, host="127.0.0.1", port=8060)
