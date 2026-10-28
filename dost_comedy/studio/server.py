import os
import sys
import json
import time
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

from scripts.pipeline_helper import extract_last_frame, stitch_and_polish
from studio.generator import (
    load_ideas,
    get_joke_by_id,
    generate_prompts_package,
    smart_parse_raw_text,
    CHARACTERS,
    HISTORY_LEDGER_PATH
)

app = FastAPI(title="Dost Comedy Studio (Aqib & Mani)")

# Cache-busting middleware to guarantee NO browser caching
@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

STATIC_DIR = BASE_DIR / "studio" / "static"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/temp", StaticFiles(directory=str(TEMP_DIR)), name="temp")
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

class SmartParseRequest(BaseModel):
    raw_text: str

@app.get("/")
def read_root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        response = FileResponse(str(index_file))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        return response
    return JSONResponse({"status": "Dost Comedy Studio Running on Port 8060"})

@app.get("/api/jokes")
def get_jokes():
    return JSONResponse(load_ideas())

@app.get("/api/characters")
def get_characters():
    return JSONResponse(CHARACTERS)

@app.post("/api/smart-parse")
def smart_parse_endpoint(req: SmartParseRequest):
    if not req.raw_text.strip():
        raise HTTPException(status_code=400, detail="Empty script text")
    pkg = smart_parse_raw_text(req.raw_text)
    return JSONResponse({
        "status": "success",
        "title": pkg["title"],
        "location": pkg["location"],
        "prop": pkg["prop"],
        "image_prompt": pkg["image_prompt"],
        "i2v_prompt": pkg["i2v_prompt"],
        "video_prompt": pkg["video_prompt"],
        "dialogue_00": pkg["dialogue_00"],
        "dialogue_03": pkg["dialogue_03"]
    })

@app.get("/api/joke-prompt/{joke_id}")
def get_prompt_for_preloaded_joke(joke_id: str):
    joke = get_joke_by_id(joke_id)
    if not joke:
        raise HTTPException(status_code=404, detail="Joke not found")
    pkg = generate_prompts_package(joke)
    return JSONResponse({
        "status": "success",
        "joke": joke,
        "title": pkg["title"],
        "location": pkg["location"],
        "prop": pkg["prop"],
        "image_prompt": pkg["image_prompt"],
        "i2v_prompt": pkg["i2v_prompt"],
        "video_prompt": pkg["video_prompt"],
        "dialogue_00": pkg["dialogue_00"],
        "dialogue_03": pkg["dialogue_03"]
    })

@app.post("/api/upload-preview-image")
async def upload_preview_image(file: UploadFile = File(...)):
    filename = f"preview_{int(time.time())}_{file.filename}"
    filepath = TEMP_DIR / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return JSONResponse({
        "status": "success",
        "url": f"/temp/{filename}",
        "name": file.filename
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
            if f.lower().endswith((".mp4", ".png", ".jpg", ".jpeg", ".webp")):
                full = os.path.join(folder, f)
                try:
                    mtime = os.path.getmtime(full)
                    size = os.path.getsize(full)
                    is_img = f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
                    candidates.append({
                        "name": f,
                        "path": full,
                        "mtime": mtime,
                        "size_mb": round(size / (1024 * 1024), 2),
                        "folder": folder,
                        "is_image": is_img
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
    print("       STARTING DOST COMEDY STUDIO (AQIB & MANI)")
    print("========================================================")
    print("URL: http://localhost:8060 (No-Cache Mode Active)\n")
    uvicorn.run("studio.server:app", host="127.0.0.1", port=8060, reload=True)
