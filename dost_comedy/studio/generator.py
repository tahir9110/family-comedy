import os
import json
import random
import re
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IDEAS_BANK_PATH = BASE_DIR / "data" / "ideas_bank.json"
HISTORY_LEDGER_PATH = BASE_DIR / "data" / "history_ledger.json"

ROOT_DIR = BASE_DIR.parent
OPENAI_KEY_PATH = ROOT_DIR / "openai key.txt"
GEMINI_KEY_PATH = ROOT_DIR / "aistuio free key.txt"

CHARACTERS = {
    "@Aqib": {
        "name": "Aqib",
        "tag": "@Aqib",
        "role": "The Witty Hero (Brother Aqib)",
        "age": "24-25",
        "description": "Keep 1:1 facial identity and likeness strictly identical to the attached @Aqib reference photo. @Aqib is a Pakistani young man in his mid-20s with an oval-round face, sturdy build, warm olive South Asian complexion, jet black side-swept hair with a subtle forehead fringe, dark expressive almond eyes, natural thick eyebrows, a distinct neat dark mustache, and a trimmed chinstrap beard running along the jawline with clean cheeks. He wears a casual navy blue henley shirt with sleeves rolled up to mid-forearm. Highly expressive, energetic comedic body language."
    },
    "@Mani": {
        "name": "Mani",
        "tag": "@Mani",
        "role": "The Sarcastic Best Friend",
        "age": "24-25",
        "description": "Keep facial features consistent with the attached @Mani references. @Mani is a 25-year-old Pakistani young man with neatly groomed pompadour hairstyle, well-trimmed short beard and mustache, wearing an open denim jacket over a mustard yellow t-shirt. Sarcastic, skeptical, deadpan, and easily bewildered."
    }
}

DEFAULT_PROMPT_CONSTRAINTS = (
    "Camera & Optics: Shot on 50mm prime cinematic lens with subtle shallow depth of field, softly blurred background. "
    "Fixed eye-level medium-wide shot with smooth stable framing, no jittery camera motion, no cuts, no reverse angles. "
    "Side-profile two-shot in open 3/4 angle: Both characters stand or sit angled toward the camera lens in an open 3/4 stance, so BOTH characters' full faces, eyes, and mouth expressions are clearly visible to the camera at the same time. NEITHER character turns their back to the camera. "
    "Lighting & Atmosphere: Soft natural directional morning lighting with gentle ambient shadows, warm cinematic color grade. "
    "Buddy Comedy Tone: Lighthearted Pakistani buddy comedy atmosphere: Warm, natural friendship camaraderie, casual banter, relaxed comedic postures. Strictly NO aggressive face-off, NO confrontational fighting stance, NO stiff awkward standing. "
    "Negative Constraints: Background walls and surroundings are completely clean and plain with NO Arabic script, NO framed calligraphy, and NO religious verses on walls. Strictly NO text on clothing, NO extra fingers, NO blurry facial artifacts. Ultra photorealistic cinematic Hollywood-level 8k aesthetic, 9:16 vertical video composition."
)

def get_next_episode_id():
    os.makedirs(BASE_DIR / "data", exist_ok=True)
    if not os.path.exists(HISTORY_LEDGER_PATH):
        return 1
    try:
        with open(HISTORY_LEDGER_PATH, "r", encoding="utf-8") as f:
            ledger = json.load(f)
            return len(ledger) + 1
    except Exception:
        return 1

def load_ideas():
    if not os.path.exists(IDEAS_BANK_PATH):
        return []
    try:
        with open(IDEAS_BANK_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def get_joke_by_id(joke_id):
    ideas = load_ideas()
    for item in ideas:
        if str(item.get("id")) == str(joke_id):
            return item
    return None

def infer_staging(location, prop):
    loc_l = location.lower()
    prop_l = prop.lower()

    if "bike" in loc_l or "bike" in prop_l or "motorcycle" in loc_l or "motorcycle" in prop_l or "petrol" in prop_l:
        return (
            "Physical Staging: @Aqib is actively seated mounted on the black saddle of the parked motorcycle, "
            "his hands resting on the chrome handlebars and feet touching the ground, leaning slightly over the tank with an innocent, tired comedic expression. "
            "@Mani stands right beside the front wheel of the motorbike, leaning casually against the roadside curb with a sarcastic, mocking smirk, "
            "looking down toward @Aqib. Both angled in an open 3/4 stance toward the camera. Friendly buddy humor, NO fighting."
        )
    elif "dhaba" in loc_l or "chai" in loc_l or "tea" in prop_l:
        return (
            "Physical Staging: Both @Aqib and @Mani are comfortably seated on a rustic wooden bench at a 3/4 angle to the camera. "
            "Each friend holds a clear glass cup of hot steaming doodh patti tea. Relaxed seated posture, laughing and bantering like close friends."
        )
    elif "fan" in prop_l or "jugaad" in loc_l:
        return (
            "Physical Staging: @Aqib stands under the ceiling fan holding a long broomstick handle reaching up to nudge the fan blade with serious comic focus. "
            "@Mani sits relaxed nearby on a bed or chair, chuckling in disbelief at Aqib's absurd jugaad. Relaxed funny buddy interaction."
        )
    elif "sofa" in loc_l or "living" in loc_l or "room" in loc_l:
        return (
            "Physical Staging: Both friends are seated casually on a comfortable sofa in an open 3/4 stance toward the camera lens. "
            "Natural relaxed sitting postures with hand gestures, enjoying lighthearted comedic banter."
        )
    else:
        return (
            "Physical Staging: The two friends interact naturally in an open 3/4 stance toward the camera lens, "
            "with casual relaxed body language, expressive hand gestures, and playful buddy camaraderie. Strictly NO stiff face-off."
        )

def map_tag(spk):
    s = str(spk).lower()
    if "aqib" in s or "shani" in s:
        return "@Aqib"
    elif "mani" in s:
        return "@Mani"
    return spk

def build_image_prompt(speaker_00, speaker_03, location, prop, staging=None):
    """Step 1: Keyframe Image Prompt (Generate still image in Flow first to verify face, bike, and staging)."""
    aqib_desc = CHARACTERS["@Aqib"]["description"]
    mani_desc = CHARACTERS["@Mani"]["description"]
    if not staging:
        staging = infer_staging(location, prop)

    return (
        f"Cinematic keyframe production still photograph. "
        f"{aqib_desc} {mani_desc} "
        f"Setting: Pakistani {location} with {prop} clearly featured in the frame. "
        f"{staging} "
        f"{DEFAULT_PROMPT_CONSTRAINTS} "
        f"Single still frame keyframe photograph, razor sharp facial focus, natural eyes looking toward scene, perfectly positioned for subsequent video animation."
    )

def build_i2v_prompt(speaker_00, dialogue_00, speaker_03, dialogue_03):
    """Step 2: Motion/Lip-sync animation prompt (Animate the approved starting image)."""
    s1_tag = map_tag(speaker_00)
    s2_tag = map_tag(speaker_03)

    return (
        f"Animate seamlessly from this exact starting keyframe image, strictly maintaining identical character faces, clothing, motorbike, and lighting. "
        f"Fixed medium-wide stationary eye-level camera, no cuts, no panning, no camera motion. "
        f"At 00-03 seconds: {s1_tag} speaks first with full natural mouth articulation, casual friendly smirk, and talking hand motion: \"{dialogue_00}\", while {s2_tag} listens with responsive amused reaction. "
        f"At 03-08 seconds: {s2_tag} delivers their punchline with dramatic comedic facial expression and synchronized mouth movement: \"{dialogue_03}\", while {s1_tag} reacts in bewildered comedic shock or playful disbelief. "
        f"Continuous 10-second single take, photorealistic smooth motion."
    )

def build_flow_prompt(speaker_00, dialogue_00, speaker_03, dialogue_03, location, prop, staging=None):
    """Direct All-In-One Text-to-Video Prompt."""
    aqib_desc = CHARACTERS["@Aqib"]["description"]
    mani_desc = CHARACTERS["@Mani"]["description"]
    s1_tag = map_tag(speaker_00)
    s2_tag = map_tag(speaker_03)

    if not staging:
        staging = infer_staging(location, prop)

    return (
        f"{aqib_desc} {mani_desc} "
        f"Setting: Pakistani {location} with {prop} visible in the scene. "
        f"{staging} "
        f"{DEFAULT_PROMPT_CONSTRAINTS} "
        f"At 00-03 seconds: {s1_tag} delivers their line with full expressive mouth articulation, casual friendly smirk, and talking motion: \"{dialogue_00}\", while {s2_tag} listens with responsive amused reaction. "
        f"At 03-08 seconds: {s2_tag} delivers their punchline with dramatic comedic facial expression and synchronized mouth movement: \"{dialogue_03}\", while {s1_tag} reacts in bewildered comedic shock or playful disbelief. "
        f"Strictly continuous 10-second single take."
    )

def generate_prompts_package(joke_dict):
    sc1 = joke_dict.get("scene_1", {})
    spk1 = sc1.get("speaker_at_00", "Mani")
    dia1 = sc1.get("dialogue_at_00", "")
    spk2 = sc1.get("speaker_at_03", "Aqib")
    dia2 = sc1.get("dialogue_at_03", "")
    loc = joke_dict.get("location", "Streetside curb near a parked Honda CD70 motorbike")
    prp = joke_dict.get("prop", "Red Honda CD70 motorbike")
    staging = joke_dict.get("staging", None)
    
    return {
        "title": joke_dict.get("title", ""),
        "location": loc,
        "prop": prp,
        "image_prompt": build_image_prompt(spk1, spk2, loc, prp, staging),
        "i2v_prompt": build_i2v_prompt(spk1, dia1, spk2, dia2),
        "video_prompt": build_flow_prompt(spk1, dia1, spk2, dia2, loc, prp, staging)
    }

def generate_prompt_for_joke(joke_dict):
    pkg = generate_prompts_package(joke_dict)
    return pkg["video_prompt"]
