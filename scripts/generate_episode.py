import os
import sys
import json
import shutil
import subprocess
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from pipeline_helper import extract_last_frame, stitch_and_polish

def find_latest_download(after_timestamp):
    folders = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Downloads/Video")
    ]
    latest_file = None
    latest_mtime = after_timestamp
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for f in os.listdir(folder):
            if f.endswith(".mp4"):
                full = os.path.join(folder, f)
                try:
                    mtime = os.path.getmtime(full)
                    if mtime >= latest_mtime:
                        latest_mtime = mtime
                        latest_file = full
                except OSError:
                    pass
    return latest_file

def run_flow_video(prompt, target_path, duration="8", start_frame=None):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 100000:
        print(f"File already exists and valid: {target_path}")
        return target_path

    # Single-line clean prompt to avoid editor paste rejections
    clean_prompt = " ".join(prompt.split())
    start_time = time.time() - 5  # cushion for file creation time

    if start_frame:
        mode = "flow-frame-to-video"
        cmd = [
            "flow-auto.cmd",
            "generate",
            "create",
            mode,
            "--model", "omni-flash",
            "--aspect-ratio", "9:16",
            "--duration", str(duration),
            "--image", os.path.abspath(start_frame),
            "--prompt", clean_prompt,
            "--wait"
        ]
    else:
        mode = "flow-text-to-video"
        cmd = [
            "flow-auto.cmd",
            "generate",
            "create",
            mode,
            "--model", "omni-flash",
            "--aspect-ratio", "9:16",
            "--duration", str(duration),
            "--prompt", clean_prompt,
            "--wait"
        ]

    print(f"\n[Flow {mode}] Submitting job -> {target_path}")
    print(f"Prompt: {clean_prompt[:100]}...")

    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = proc.stdout + "\n" + proc.stderr
    lines = [l.strip() for l in output.splitlines() if l.strip()]

    downloaded = None
    for line in reversed(lines):
        if line.endswith(".mp4") and os.path.exists(line):
            downloaded = line
            break

    # If IDM or custom downloader moved it, look in downloads folders
    if not downloaded or not os.path.exists(downloaded):
        downloaded = find_latest_download(start_time)

    if downloaded and os.path.exists(downloaded):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(downloaded, target_path)
        print(f"✅ Successfully saved video from {downloaded} to: {target_path}")
        return target_path
    else:
        print(f"❌ Failed to download video for {target_path}. Output:\n{output[-400:]}")
        return None

def produce_episode(episode_id, title, location, main_prop, first_speaker, scene1_prompt, scene2_prompt, use_frame_continuation=False):
    print(f"==================================================")
    print(f"🎬 Starting Full Automated Production: Episode {episode_id} - '{title}'")
    print(f"==================================================")

    clip1_path = f"output/episode_{episode_id}_clip1.mp4"
    clip2_path = f"output/episode_{episode_id}_clip2.mp4"
    last_frame_path = f"temp/episode_{episode_id}_last_frame.png"
    final_output = f"output/episode_{episode_id}_final.mp4"

    # Step 1: Render Scene 1 (R2V via flow-text-to-video)
    print("\n--- STEP 1: Rendering Scene 1 (R2V) ---")
    c1 = run_flow_video(scene1_prompt, clip1_path, duration="8")
    if not c1:
        print("Aborting: Scene 1 failed to generate.")
        return False

    # Step 2: Extract Last Frame for visual archive
    print("\n--- STEP 2: Extracting exact last frame ---")
    extract_last_frame(clip1_path, last_frame_path)

    # Step 3: Render Scene 2 (Continuation & Punchline)
    print("\n--- STEP 3: Rendering Scene 2 (Continuation) ---")
    start_frame = last_frame_path if use_frame_continuation else None
    c2 = run_flow_video(scene2_prompt, clip2_path, duration="8", start_frame=start_frame)
    if not c2:
        print("Aborting: Scene 2 failed to generate.")
        return False

    # Step 4: Stitch Final Short
    print("\n--- STEP 4: Stitching Clips into Final Sitcom Short ---")
    stitch_and_polish(clip1_path, clip2_path, final_output)

    # Step 5: Update History Ledger
    ledger_path = "data/history_ledger.json"
    if os.path.exists(ledger_path):
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
    else:
        ledger = []

    ledger.append({
        "episode_id": episode_id,
        "title": title,
        "location": location,
        "main_prop": main_prop,
        "first_speaker": first_speaker,
        "date": time.strftime("%Y-%m-%d")
    })

    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)

    print(f"\n🎉 Episode {episode_id} complete and logged to {ledger_path}!")
    return True

if __name__ == "__main__":
    # Execution for Episode 8: "Filmi Hero Ya Chamgadar (Hero Look)"
    scene1 = (
        "Use the attached @Abbu, @Ammi, and @Beta character references so their faces and outfits stay consistent. "
        "In a lively Pakistani living room, their 25-year-old grown adult son @Beta stands proudly in the center adjusting his shirt collar like a movie superstar, while @Ammi and @Abbu sit together on the sofa watching him in disbelief. "
        "At 0:00, @Beta boasts enthusiastically with theatrical vanity in Urdu: امی سچ بتائیں، میں بالکل فلمی ہیرو لگ رہا ہوں نا؟ (Ammi sach batayein, main bilkul filmi hero lag raha hoon na?). "
        "At 0:03, @Ammi instantly cuts in without any pause with sharp sarcastic stage drama laughter and replies in Urdu: ہاں بیٹا، بس الٹا لٹک جاؤ، تو پوری چمگادڑ لگو گے! (Haan beta, bas ulta latak jao, toh poori chamgadar lago ge!). "
        "Physical prop lock: @Beta remains standing in the center holding his shirt collar throughout the clip. "
        "Fast-paced Pakistani stage drama comedic timing with rapid witty banter and ZERO dead silence between dialogues. Dialogue delivery flows back-to-back immediately. "
        "(do NOT make @Beta smile at the end of the clip). "
        "Keep a medium-wide shot and DO NOT cut to a close-up—ensure ALL THREE characters (@Abbu, @Ammi, and @Beta) are visible together in the final frame."
    )

    # Scene 2 (NO @ tags - for I2V continuation from Clip 1 last frame)
    scene2 = (
        "Continue seamlessly from this exact starting frame, keeping the exact same faces, outfits, and lighting. "
        "In the living room, the 25-year-old grown adult son in grey (Beta) stands in the center looking offended and hurt, while the mother in green (Ammi) smirks on the sofa, and the older father on the left (Abbu) looks up with deadpan sarcasm. "
        "At 0:00, the son (Beta) passionately whines turning to his father in Urdu: ابو آپ تو انصاف کریں، کیا میں ہیرو نہیں ہوں؟ (Abbu aap toh insaaf karein, kya main hero nahi hoon?). "
        "At 0:03, the older father (Abbu) instantly cuts in without any pause with sharp deadpan stage drama roast in Urdu: ہیرو تو ہے، بس تجھے دیکھ کر ہیروئن بھاگ گئی تھی! (Hero toh hai, bas tujhe dekh kar heroine bhaag gayi thi!). "
        "Physical prop lock: the son remains standing in the center. "
        "Fast-paced Pakistani stage drama comedic timing with rapid witty banter and ZERO dead silence between dialogues. Dialogue delivery flows back-to-back immediately. "
        "(do NOT make Beta smile at the end of the clip). "
        "Keep a medium-wide shot on all three characters."
    )

    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "scene1"

    if mode == "scene1":
        print("🎬 Running STEP 1: Scene 1 for Episode 8 (R2V with Real Urdu Script & Stage Drama Banter)")
        c1 = run_flow_video(scene1, "output/episode_8_clip1.mp4", duration="8")
        if c1:
            extract_last_frame("output/episode_8_clip1.mp4", "temp/episode_8_last_frame.png")
            with open("temp/prompt_scene2.txt", "w", encoding="utf-8") as f:
                f.write(scene2)
            print("✅ Scene 1 complete & last frame extracted to temp/episode_8_last_frame.png")
            print("✅ Scene 2 prompt written to temp/prompt_scene2.txt")
    elif mode == "stitch":
        print("🎬 Running Post-Production Stitch for Episode 8")
        stitch_and_polish("output/episode_8_clip1.mp4", "output/episode_8_clip2.mp4", "output/episode_8_final.mp4")
        
        # Log to ledger
        ledger_path = "data/history_ledger.json"
        if os.path.exists(ledger_path):
            with open(ledger_path, "r", encoding="utf-8") as f:
                ledger = json.load(f)
        else:
            ledger = []
        ledger.append({
            "episode_id": 8,
            "title": "Fawad Khan Ya Chamgadar (Hero Look)",
            "location": "Living Room Sofa",
            "main_prop": "Fancy collar",
            "first_speaker": "@Beta",
            "date": time.strftime("%Y-%m-%d")
        })
        with open(ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)
        print("🎉 Episode 8 logged into history ledger!")
    else:
        produce_episode(
            episode_id=8,
            title="Fawad Khan Ya Chamgadar (Hero Look)",
            location="Living Room Sofa",
            main_prop="Fancy collar",
            first_speaker="@Beta",
            scene1_prompt=scene1,
            scene2_prompt=scene2,
            use_frame_continuation=False
        )
