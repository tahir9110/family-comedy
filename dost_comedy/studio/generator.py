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
    },
    "@Judge": {
        "name": "Judge",
        "tag": "@Judge",
        "role": "Pakistani High Court Judge",
        "age": "55-60",
        "description": "Keep facial features consistent with the attached @Judge references. @Judge is a dignified 55-year-old Pakistani High Court judge with neat silver-grey side-parted hair, trim grey mustache, wire-rimmed spectacles, wearing a formal black judicial coat and white court advocate neckband collar over a dark suit. Authoritative, composed, and stern."
    },
    "@Doctor": {
        "name": "Doctor",
        "tag": "@Doctor",
        "role": "Pakistani Clinic Doctor",
        "age": "45-50",
        "description": "Keep facial features consistent with the attached @Doctor references. @Doctor is a 45-year-old Pakistani male doctor with neatly groomed hair, wearing a white medical lab coat with a stethoscope around his neck over a formal dress shirt. Professional, puzzled, and attentive."
    },
    "@Police": {
        "name": "Police Officer",
        "tag": "@Police",
        "role": "Pakistani Police Inspector",
        "age": "40-45",
        "description": "Keep facial features consistent with the attached @Police references. @Police is a 40-year-old Pakistani police officer with a sharp mustache, wearing a traditional olive-khaki Pakistan Police uniform with shoulder badges. Skeptical, commanding, and easily baffled."
    },
    "@Teacher": {
        "name": "School Master",
        "tag": "@Teacher",
        "role": "Pakistani School Teacher",
        "age": "50-55",
        "description": "Keep facial features consistent with the attached @Teacher references. @Teacher is a 50-year-old Pakistani school master with spectacles, wearing a traditional formal shalwar kameez with a Nehru waistcoat. Strict, disciplined, and expressive."
    }
}

DEFAULT_PROMPT_CONSTRAINTS = (
    "Camera & Optics: Shot on 50mm prime cinematic lens with subtle shallow depth of field, softly blurred background. "
    "Fixed eye-level medium-wide shot with smooth stable framing, no jittery camera motion, no cuts, no reverse angles. "
    "Side-profile two-shot in open 3/4 angle: Both characters stand or sit angled toward the camera lens in an open 3/4 stance, so BOTH characters' full faces, eyes, and mouth expressions are clearly visible to the camera at the same time. NEITHER character turns their back to the camera. "
    "Lighting & Atmosphere: Soft natural directional lighting with gentle ambient shadows, warm cinematic color grade. "
    "Tone & Performance: Expressive comedic timing, situational Pakistani comedy. Strictly NO aggressive face-off, NO physical violence, NO confrontational fighting stance. "
    "Negative Constraints: Background walls and surroundings are completely clean and plain with NO Arabic script, NO framed calligraphy, and NO religious verses on walls. Strictly NO text on clothing, NO extra fingers, NO blurry facial artifacts. Ultra photorealistic cinematic Hollywood-level 8k aesthetic, 9:16 vertical video composition."
)

def get_character_desc(tag):
    if tag in CHARACTERS:
        return CHARACTERS[tag]["description"]
    for k, v in CHARACTERS.items():
        if k.lower().replace("@", "") in tag.lower():
            return v["description"]
    return f"Keep facial features consistent with the attached {tag} references."

def get_openai_api_key():
    for p in [OPENAI_KEY_PATH, ROOT_DIR / "openai key.txt", Path("openai key.txt")]:
        if p.exists():
            try:
                content = p.read_text(encoding="utf-8")
                m = re.search(r'sk-[a-zA-Z0-9_\-]+', content)
                if m:
                    return m.group(0)
            except Exception:
                pass
    return None

def get_gemini_api_key():
    for p in [GEMINI_KEY_PATH, ROOT_DIR / "aistuio free key.txt", Path("aistuio free key.txt")]:
        if p.exists():
            try:
                k = p.read_text(encoding="utf-8").strip()
                if k:
                    return k
            except Exception:
                pass
    return None

def clean_devanagari(text):
    if not text:
        return ""
    replacements = {
        "अच्छा": "اچھا", "क्या": "کیا", "لڑکے": "لڑکے", "لڑکا": "لڑکا",
        "لड़की": "لڑکی", "पर": "پر", "तो": "تو", "तुम": "تم", "हो": "ہو",
        "री": "ری", "के": "کے", "کی": "کی", "کا": "کا", "है": "ہے", "ہیں": "ہیں"
    }
    for dev, urd in replacements.items():
        text = text.replace(dev, urd)
    text = re.sub(r'[\u0900-\u097F]+', '', text)
    return text.strip()

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

def infer_staging(location, prop, s1_tag="@Mani", s2_tag="@Aqib"):
    loc_l = location.lower()
    prop_l = prop.lower()

    if "judge" in loc_l or "judge" in prop_l or "court" in loc_l or "court" in prop_l or "phansi" in prop_l or "phansi" in loc_l or "adalat" in loc_l or s1_tag == "@Judge" or s2_tag == "@Judge":
        return (
            "Physical Staging: In a formal Pakistani High Court courtroom, @Judge sits with dignified authority behind an elevated dark polished mahogany judicial bench with a wooden gavel and legal case law files. "
            "@Aqib stands inside the traditional wooden accused dock / witness box (kathehra) angled in an open 3/4 profile toward the bench and camera lens, "
            "resting his hands casually on the wooden railing with an innocent, witty deadpan smirk as he delivers his audacious answer. Both faces and reactions are clearly visible to the camera. Strictly NO outdoor hanging scaffold, NO ropes, NO physical violence."
        )
    elif "bike" in loc_l or "bike" in prop_l or "motorcycle" in loc_l or "motorcycle" in prop_l or "petrol" in prop_l:
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
    elif "doctor" in loc_l or "clinic" in loc_l or "hospital" in loc_l or s1_tag == "@Doctor" or s2_tag == "@Doctor":
        return (
            "Physical Staging: In a clean Pakistani medical clinic, @Doctor sits behind a consultation desk with a stethoscope and medical charts. "
            "@Aqib sits casually on the patient chair across the desk in an open 3/4 angle to the camera, explaining his condition with animated comedic hand gestures. Both faces clearly visible."
        )
    elif "police" in loc_l or "thana" in loc_l or s1_tag == "@Police" or s2_tag == "@Police":
        return (
            "Physical Staging: Inside a Pakistani police station (thana), @Police sits behind an official wooden desk with case registers. "
            "@Aqib stands in front of the desk in an open 3/4 stance facing the officer and camera, defending himself with witty humorous hand gestures."
        )
    elif "fan" in prop_l or "jugaad" in loc_l:
        return (
            "Physical Staging: @Aqib stands under the ceiling fan holding a long broomstick handle reaching up to nudge the fan blade with serious comic focus. "
            "@Mani sits relaxed nearby on a bed or chair, chuckling in disbelief at Aqib's absurd jugaad. Relaxed funny buddy interaction."
        )
    elif "sofa" in loc_l or "living" in loc_l or "room" in loc_l:
        return (
            "Physical Staging: Both characters are seated casually on a comfortable sofa in an open 3/4 stance toward the camera lens. "
            "Natural relaxed sitting postures with hand gestures, enjoying lighthearted comedic banter."
        )
    else:
        return (
            "Physical Staging: The two characters interact naturally in an open 3/4 stance toward the camera lens, "
            "with casual relaxed body language, expressive hand gestures, and playful comedic camaraderie. Strictly NO stiff face-off."
        )

def map_tag(spk):
    s = str(spk).lower()
    if "aqib" in s or "shani" in s or "bonda" in s or "banda" in s or "mulzim" in s or "accused" in s or "aadmi" in s:
        return "@Aqib"
    elif "judge" in s or "jaj" in s or "adalat" in s:
        return "@Judge"
    elif "doctor" in s or "dr" in s:
        return "@Doctor"
    elif "police" in s or "inspector" in s or "havaldar" in s or "thana" in s:
        return "@Police"
    elif "teacher" in s or "master" in s or "ustad" in s:
        return "@Teacher"
    elif "mani" in s or "dost" in s or "friend" in s:
        return "@Mani"
    return f"@{spk.replace('@', '').strip().capitalize()}"

def build_image_prompt(speaker_00, speaker_03, location, prop, staging=None, custom_desc=None):
    """Step 1: Keyframe Image Prompt (Generate still image in Flow first to verify face, setting, and staging)."""
    s1_tag = map_tag(speaker_00)
    s2_tag = map_tag(speaker_03)

    desc1 = (custom_desc and custom_desc.get(s1_tag)) or get_character_desc(s1_tag)
    desc2 = (custom_desc and custom_desc.get(s2_tag)) or get_character_desc(s2_tag)

    if not staging:
        staging = infer_staging(location, prop, s1_tag, s2_tag)
    elif not staging.strip().lower().startswith("physical staging:"):
        staging = f"Physical Staging: {staging.strip()}"

    loc_str = location if location.lower().startswith("pakistani") else f"Pakistani {location}"

    return (
        f"Cinematic keyframe production still photograph. "
        f"{desc1} {desc2} "
        f"Setting: {loc_str} with {prop} clearly featured in the frame. "
        f"{staging} "
        f"{DEFAULT_PROMPT_CONSTRAINTS} "
        f"Single still frame keyframe photograph, razor sharp facial focus, natural eyes looking toward scene, perfectly positioned for subsequent video animation."
    )

def build_i2v_prompt(speaker_00, dialogue_00, speaker_03, dialogue_03):
    """Step 2: Motion/Lip-sync animation prompt (Animate the approved starting image)."""
    s1_tag = map_tag(speaker_00)
    s2_tag = map_tag(speaker_03)

    return (
        f"Animate seamlessly from this exact starting keyframe image, strictly maintaining identical character faces, clothing, environment, and lighting. "
        f"Fixed medium-wide stationary eye-level camera, no cuts, no panning, no camera motion. "
        f"At 00-03 seconds: {s1_tag} speaks first with full natural mouth articulation, serious or comedic facial expression, and talking hand motion: \"{dialogue_00}\", while {s2_tag} listens with responsive reaction. "
        f"At 03-08 seconds: {s2_tag} delivers their punchline with dramatic comedic facial expression and synchronized mouth movement: \"{dialogue_03}\", while {s1_tag} reacts in bewildered comedic shock or disbelief. "
        f"Continuous 10-second single take, photorealistic smooth motion."
    )

def build_flow_prompt(speaker_00, dialogue_00, speaker_03, dialogue_03, location, prop, staging=None, custom_desc=None):
    """Direct All-In-One Text-to-Video Prompt."""
    s1_tag = map_tag(speaker_00)
    s2_tag = map_tag(speaker_03)
    desc1 = (custom_desc and custom_desc.get(s1_tag)) or get_character_desc(s1_tag)
    desc2 = (custom_desc and custom_desc.get(s2_tag)) or get_character_desc(s2_tag)

    if not staging:
        staging = infer_staging(location, prop, s1_tag, s2_tag)
    elif not staging.strip().lower().startswith("physical staging:"):
        staging = f"Physical Staging: {staging.strip()}"

    loc_str = location if location.lower().startswith("pakistani") else f"Pakistani {location}"

    return (
        f"{desc1} {desc2} "
        f"Setting: {loc_str} with {prop} visible in the scene. "
        f"{staging} "
        f"{DEFAULT_PROMPT_CONSTRAINTS} "
        f"At 00-03 seconds: {s1_tag} delivers their line with full expressive mouth articulation and talking motion: \"{dialogue_00}\", while {s2_tag} listens with responsive reaction. "
        f"At 03-08 seconds: {s2_tag} delivers their punchline with dramatic comedic facial expression and synchronized mouth movement: \"{dialogue_03}\", while {s1_tag} reacts in bewildered comedic shock or disbelief. "
        f"Strictly continuous 10-second single take."
    )

def generate_prompts_package(joke_dict, custom_desc=None):
    sc1 = joke_dict.get("scene_1", {})
    spk1 = sc1.get("speaker_at_00", "Mani")
    dia1 = clean_devanagari(sc1.get("dialogue_at_00", ""))
    spk2 = sc1.get("speaker_at_03", "Aqib")
    dia2 = clean_devanagari(sc1.get("dialogue_at_03", ""))
    loc = joke_dict.get("location", "Streetside curb near a parked Honda CD70 motorbike")
    prp = joke_dict.get("prop", "Red Honda CD70 motorbike")
    staging = joke_dict.get("staging", None)
    
    return {
        "title": joke_dict.get("title", "Dost Comedy Episode"),
        "location": loc,
        "prop": prp,
        "speaker_00": spk1,
        "dialogue_00": dia1,
        "speaker_03": spk2,
        "dialogue_03": dia2,
        "staging": staging,
        "image_prompt": build_image_prompt(spk1, spk2, loc, prp, staging, custom_desc),
        "i2v_prompt": build_i2v_prompt(spk1, dia1, spk2, dia2),
        "video_prompt": build_flow_prompt(spk1, dia1, spk2, dia2, loc, prp, staging, custom_desc)
    }

def smart_parse_raw_text(raw_text):
    """Parses any raw joke, fixes grammar, expands short lines, and generates the complete prompt package.
    Lets AI (OpenAI/Gemini) intelligently determine the ideal Pakistani venue, authentic props, character roles, and custom physical staging.
    """
    clean = raw_text.strip()
    
    # Try AI parse first
    prompt = f"""You are an elite Pakistani comedy script supervisor and cinematic director for AI video production (Google Flow).
Analyze the user's raw joke or comedy dialogue and intelligently determine the ideal Pakistani venue, authentic props, character roles, and physical staging.

CORE PRINCIPLES (LET THE SCRIPT DICTATE THE SCENE):
1. VENUE & LOCATION:
   - Autonomously choose the most authentic, funny, and contextually accurate Pakistani venue that fits the joke premise.
   - Examples: High Court Courtroom, Men's Barber Shop (Nai ki dukan), Roadside Chai Dhaba, Motor Mechanic Workshop, Doctor Clinic, Police Station (Thana), Sweet Shop (Mithai ki dukan), Vegetable/Fruit Stall, Bachelor Living Room, Roadside CD70 Motorbike curb, etc.
   - NEVER use generic or mismatched venues. If the script is a court joke, place it in a Pakistani High Court courtroom. If about a barber, in a barber shop. If about two buddies, at a dhaba or on a CD70 motorbike.

2. PROPS:
   - Identify 2-3 authentic, realistic props that belong in this venue (e.g. mahogany judge bench and gavel; barber mirror, cape, and scissors; steaming tea glasses and rustic wooden bench; spanners and greasy motorcycle parts).
   - NEVER suggest violent, gory, or execution props (Strictly NO hanging scaffolds, NO ropes).

3. CHARACTERS & CASTING:
   - The witty comedic punchline hero is ALWAYS @Aqib (Pakistani young man, brother Aqib).
   - The other character should naturally fit the joke (e.g. @Mani for buddy jokes, @Judge for court trials, @Doctor for clinics, @Police for police/thana, @Barber for salon, @Shopkeeper for bazaar, @Teacher for classroom, etc.).
   - If the character is not @Aqib or @Mani, provide a concise visual description in 'character_00_desc' (age, clothing, hair, role).

4. PHYSICAL STAGING (CRITICAL FOR GOOGLE FLOW VIDEO):
   - You MUST write the 'staging' description following these strict cinematographic rules:
     * Side-profile two-shot in open 3/4 angle: Both characters stand or sit angled toward the camera lens in an open 3/4 stance, so BOTH characters' full faces, eyes, and mouth expressions are clearly visible to the camera at the same time.
     * NEITHER character turns their back to the camera.
     * Describe natural interaction: sitting postures, hands resting, expressive gestures, playful comedic banter.
     * Strictly NO aggressive face-off, NO confrontational fighting stance.

5. DIALOGUE & TIMING:
   - Short-Line Safety Expansion: If any dialogue is 1-2 words (like "Kyun?", "Kya?"), expand it to 4-5 words (e.g. "ارے پر کیوں جناب؟ مجھے وجہ تو بتائیں!").
   - Fix grammar and typos. Format: 'اردو مکالمہ (Clean Roman Urdu)'.
   - speaker_00 speaks at 00-03 seconds (sets up the premise).
   - speaker_03 delivers the comedic punchline at 03-08 seconds.

Return ONLY valid JSON in this exact schema:
{{
  "title": "Punchy Urdu/English Title",
  "location": "Authentic Pakistani Venue",
  "prop": "Authentic props visible in the scene",
  "speaker_00": "Name or tag (e.g., Mani, Judge, Doctor, Barber, Police)",
  "character_00_desc": "Visual appearance description if not @Aqib or @Mani (e.g., 'Keep facial features consistent with @Judge. 55-year-old Pakistani judge in black judicial coat and white neckband.')",
  "dialogue_00": "اردو مکالمہ (Clean Roman Urdu)",
  "speaker_03": "Aqib",
  "staging": "Physical Staging: In the authentic venue, character_00 sits/stands... while @Aqib stands/sits in an open 3/4 angle facing the camera and character... both faces fully visible...",
  "dialogue_03": "اردو مکالمہ (Clean Roman Urdu)"
}}"""

    ai_result = None
    key = get_openai_api_key()
    if key:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
        openai_models = ["gpt-5.4", "gpt-5", "gpt-4o"]
        for model in openai_models:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are an expert Pakistani comedy script supervisor and director. Return only clean JSON."},
                    {"role": "user", "content": f"{prompt}\n\nRAW USER SCRIPT:\n{clean}"}
                ],
                "response_format": {"type": "json_object"}
            }
            try:
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=25) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    ai_result = json.loads(res["choices"][0]["message"]["content"])
                    print(f"[OpenAI Success]: Script processed using {model}")
                    break
            except Exception as e:
                print(f"[OpenAI Error on {model}]:", e)

    if not ai_result:
        gemini_key = get_gemini_api_key()
        if gemini_key:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": f"{prompt}\n\nRAW USER SCRIPT:\n{clean}"}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            try:
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=12) as resp:
                    res = json.loads(resp.read().decode())
                    raw_out = res["candidates"][0]["content"]["parts"][0]["text"]
                    ai_result = json.loads(raw_out)
            except Exception as e:
                print("[Gemini Parse Error]:", e)

    # Fallback if AI offline
    if not ai_result or not ai_result.get("dialogue_03"):
        lines = [l.strip() for l in clean.splitlines() if l.strip()]
        d1 = lines[0] if len(lines) > 0 else "اوئے عاقب، کیا کر رہے ہو؟"
        d2 = lines[1] if len(lines) > 1 else "کچھ نہیں بھائی، بس زندگی سے تنگ آ گیا ہوں!"
        ai_result = {
            "title": "پاکستانی دوست کامیڈی",
            "location": "Roadside Street Corner",
            "prop": "Casual street surroundings",
            "speaker_00": "Mani",
            "dialogue_00": d1,
            "speaker_03": "Aqib",
            "dialogue_03": d2
        }

    joke_dict = {
        "title": ai_result.get("title", "دوست کامیڈی"),
        "location": ai_result.get("location", "Roadside Chai Dhaba"),
        "prop": ai_result.get("prop", "Tea glasses"),
        "staging": ai_result.get("staging"),
        "scene_1": {
            "speaker_at_00": ai_result.get("speaker_00", "Mani"),
            "dialogue_at_00": ai_result.get("dialogue_00", ""),
            "speaker_at_03": ai_result.get("speaker_03", "Aqib"),
            "dialogue_at_03": ai_result.get("dialogue_03", "")
        }
    }

    custom_desc = {}
    s1_tag = map_tag(ai_result.get("speaker_00", "Mani"))
    if ai_result.get("character_00_desc"):
        custom_desc[s1_tag] = ai_result["character_00_desc"].strip()

    return generate_prompts_package(joke_dict, custom_desc=custom_desc)
