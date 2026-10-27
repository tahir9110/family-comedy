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

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

from scripts.pipeline_helper import extract_last_frame, stitch_and_polish
from studio.generator import (
    get_next_episode_id,
    format_family_multi_scene_prompts,
    VIRAL_FRIEND_JOKES,
    WARDROBE_SETS,
    get_joke_by_id,
    smart_parse_raw_text,
    IDEAS_BANK_PATH,
    HISTORY_LEDGER_PATH
)

app = FastAPI(title="Pakistani Sitcom Studio")

# Static file mounts
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

class CustomPromptRequest(BaseModel):
    title: str
    location: str
    prop: str
    beta_s1: str
    ammi_s1: str
    beta_s2: str
    abbu_s2: str

class StitchRequest(BaseModel):
    episode_id: int
    title: str
    location: str
    prop: str
    first_speaker: str = "@Beta"

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
                        "time_str": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)),
                        "size_mb": round(size / (1024 * 1024), 2)
                    })
                except OSError:
                    pass
    candidates.sort(key=lambda x: x["mtime"], reverse=True)
    return candidates[:5]

@app.get("/")
def get_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Sitcom Studio backend running. Frontend loading..."}

@app.get("/api/status")
def get_status():
    history = []
    if os.path.exists(HISTORY_LEDGER_PATH):
        try:
            with open(HISTORY_LEDGER_PATH, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass

    ideas_bank = []
    if os.path.exists(IDEAS_BANK_PATH):
        try:
            with open(IDEAS_BANK_PATH, "r", encoding="utf-8") as f:
                ideas_bank = json.load(f)
        except Exception:
            pass

    next_id = get_next_episode_id()

    return {
        "next_episode_id": next_id,
        "history": history,
        "ideas_bank": ideas_bank,
        "wardrobes": WARDROBE_SETS,
        "viral_jokes": [
            {"id": j["id"], "title": j["title"], "location": j["location"], "prop": j["prop"]}
            for j in VIRAL_FRIEND_JOKES
        ]
    }

@app.get("/api/detect-download")
def detect_download():
    downloads = scan_downloads_folder()
    return {"downloads": downloads}

@app.post("/api/select-viral-joke")
def api_select_viral_joke(joke_id: str, wardrobe_id: Optional[str] = None):
    data = get_joke_by_id(joke_id, wardrobe_id)
    if not data:
        raise HTTPException(status_code=404, detail="Joke not found")
    return data

@app.post("/api/smart-parse")
def api_smart_parse(req: SmartParseRequest, wardrobe_id: Optional[str] = None):
    data = smart_parse_raw_text(req.raw_text, wardrobe_id)
    return data

@app.post("/api/import-clip")
async def import_clip(
    episode_id: int = Form(...),
    clip_num: int = Form(1),
    file_path: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    target_clip = OUTPUT_DIR / f"episode_{episode_id}_clip{clip_num}.mp4"
    target_frame = TEMP_DIR / f"episode_{episode_id}_last_frame_clip{clip_num}.png"

    if file:
        with open(target_clip, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    elif file_path and os.path.exists(file_path):
        shutil.copy2(file_path, target_clip)
    else:
        raise HTTPException(status_code=400, detail="No valid file or file_path provided")

    # Extract last frame using FFmpeg
    extract_last_frame(str(target_clip), str(target_frame))

    return {
        "success": True,
        "episode_id": episode_id,
        "clip_num": clip_num,
        "clip_path": str(target_clip),
        "frame_path": str(target_frame.resolve()),
        "frame_url": f"/temp/episode_{episode_id}_last_frame_clip{clip_num}.png?t={int(time.time())}"
    }

@app.post("/api/import-clip1")
async def import_clip1(
    episode_id: int = Form(...),
    file_path: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    return await import_clip(episode_id=episode_id, clip_num=1, file_path=file_path, file=file)

@app.post("/api/import-clip2")
async def import_clip2(
    episode_id: int = Form(...),
    file_path: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    return await import_clip(episode_id=episode_id, clip_num=2, file_path=file_path, file=file)

@app.post("/api/stitch")
def api_stitch(req: StitchRequest):
    clips = []
    for i in range(1, 15):
        c = OUTPUT_DIR / f"episode_{req.episode_id}_clip{i}.mp4"
        if c.exists():
            clips.append(str(c))
        else:
            if i > 2:
                break

    if len(clips) < 2:
        raise HTTPException(status_code=400, detail="At least 2 clips must be imported first before stitching")

    final_output = OUTPUT_DIR / f"episode_{req.episode_id}_final.mp4"

    # Run FFmpeg multi-clip stitch
    stitch_and_polish(clips, str(final_output))

    # Update ledger
    ledger = []
    if os.path.exists(HISTORY_LEDGER_PATH):
        try:
            with open(HISTORY_LEDGER_PATH, "r", encoding="utf-8") as f:
                ledger = json.load(f)
        except Exception:
            pass

    ledger = [item for item in ledger if item.get("episode_id") != req.episode_id]
    ledger.append({
        "episode_id": req.episode_id,
        "title": req.title,
        "location": req.location,
        "main_prop": req.prop,
        "first_speaker": req.first_speaker,
        "scenes_count": len(clips),
        "date": time.strftime("%Y-%m-%d")
    })

    with open(HISTORY_LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)

    return {
        "success": True,
        "episode_id": req.episode_id,
        "scenes_stitched": len(clips),
        "final_path": str(final_output.resolve()),
        "final_url": f"/output/episode_{req.episode_id}_final.mp4?t={int(time.time())}",
        "history": ledger
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("studio.server:app", host="127.0.0.1", port=8055, reload=True)
