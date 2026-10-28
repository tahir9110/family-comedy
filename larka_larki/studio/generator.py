import os
import json
import random
import re
import urllib.request
from pathlib import Path

HISTORY_LEDGER_PATH = "data/history_ledger.json"

COUPLE_WARDROBE_SETS = [
    {
        "id": "casual_streetwear",
        "name": "Casual Streetwear (Hoodie & Kurti)",
        "larka": "an olive-green casual streetwear hoodie with black cargo trousers",
        "larki": "a stylish embroidered pastel-pink kurti with white culottes and chiffon dupatta"
    },
    {
        "id": "cafe_chic",
        "name": "Cafe Chic (Denim Jacket & Royal Blue)",
        "larka": "a light-blue denim jacket over a white casual tee with dark denim jeans",
        "larki": "a royal-blue printed floral lawn kurti with slim white trousers"
    },
    {
        "id": "college_casual",
        "name": "College Casual (Checkered Shirt & Yellow Kurti)",
        "larka": "a red-and-navy checkered casual button-up shirt with rolled sleeves and khaki chinos",
        "larki": "a mustard-yellow printed cotton kurti with a floral printed scarf"
    },
    {
        "id": "evening_trendy",
        "name": "Evening Trendy (Black Polo & Maroon Lawn)",
        "larka": "a fitted black polo t-shirt with charcoal jeans and sneakers",
        "larki": "a deep maroon embroidered lawn suit with a printed chiffon dupatta"
    }
]

COUPLE_PRESETS = [
    {
        "id": "court_bhaga",
        "title": "بھگا کر لے جا (Court Kacheri Drama)",
        "location": "Modern Cafe / Coffee Shop",
        "prop": "Paper envelope and smartphone",
        "scenes": [
            {
                "scene_num": 1,
                "speaker_at_00": "Larka",
                "dialogue_at_00": "اب بس ایک ہی راستہ بچا ہے! (Ab bas ek hi raasta bacha hai!)",
                "speaker_at_03": "Larki",
                "dialogue_at_03": "کیا؟ (Kya?)"
            },
            {
                "scene_num": 2,
                "speaker_at_00": "Larka",
                "dialogue_at_00": "تو مجھے بھگا کر لے جا! (Tu mujhe bhaga kar le ja!)",
                "speaker_at_03": "Larka",
                "dialogue_at_03": "معاملہ کورٹ کچہری تک پہنچا، تو وہ تیری سن تو لیں گے! (Maamla court-kacheri tak pahuncha, toh woh teri sun toh lenge!)"
            },
            {
                "scene_num": 3,
                "speaker_at_00": "Larki",
                "dialogue_at_00": "اچھا؟ (Achha?)",
                "speaker_at_03": "Larki",
                "dialogue_at_03": "کیا؟ بھگا کر؟ پر لڑکے تو تم ہو نا! (Kya? Bhaga kar? Par larkay toh tum ho na!)"
            },
            {
                "scene_num": 4,
                "speaker_at_00": "Larka",
                "dialogue_at_00": "وہی تو! تو لڑکی ہے، تیری سن تو لیں گے! (Wohi toh! Tu larki hai, teri sun toh lenge!)",
                "speaker_at_03": None,
                "dialogue_at_03": None
            }
        ]
    },
    {
        "id": "cafe_bill",
        "title": "کیفے کا بل (Wallet Bhool Gaya)",
        "location": "Modern Cafe Table",
        "prop": "Restaurant bill tray and coffee cups",
        "scenes": [
            {
                "scene_num": 1,
                "speaker_at_00": "Larka",
                "dialogue_at_00": "یار میں والٹ گھر بھول آیا ہوں، آج بل تم دے دو! (Yaar main wallet ghar bhool aaya hoon, aaj bill tum de do!)",
                "speaker_at_03": "Larki",
                "dialogue_at_03": "تمہارا والٹ صرف بل دیتے وقت ہی گھر کیوں رہ جاتا ہے؟ (Tumhara wallet sirf bill dete waqt hi ghar kiyun reh jata hai?)"
            },
            {
                "scene_num": 2,
                "speaker_at_00": "Larka",
                "dialogue_at_00": "قسم لے لو محبت میں حساب کتاب نہیں ہوتا! (Qasam le lo mohabbat mein hisaab kitaab nahi hota!)",
                "speaker_at_03": "Larki",
                "dialogue_at_03": "محبت اپنی جگہ، برتن اب تم ہی دھوؤ گے! (Mohabbat apni jagah, bartan ab tum hi dhoo-o ge!)"
            }
        ]
    },
    {
        "id": "diet_burger",
        "title": "ڈائٹنگ اور برگر (Diet Drama)",
        "location": "Fast Food Corner",
        "prop": "Big juicy burger and fries",
        "scenes": [
            {
                "scene_num": 1,
                "speaker_at_00": "Larka",
                "dialogue_at_00": "تم تو کہہ رہی تھیں کہ سخت ڈائٹنگ پر ہو؟ (Tum toh keh rahi theen ke sakht dieting par ho?)",
                "speaker_at_03": "Larki",
                "dialogue_at_03": "ہاں تو یہ برگر ڈائٹ کولڈ ڈرنک کے ساتھ کھا رہی ہوں نا! (Haan toh yeh burger diet cold drink ke saath kha rahi hoon na!)"
            },
            {
                "scene_num": 2,
                "speaker_at_00": "Larka",
                "dialogue_at_00": "واہ! ایسی سائنس کس یونیورسٹی میں پڑھاتے ہیں؟ (Wah! Aisi science kis university mein parhate hain?)",
                "speaker_at_03": "Larki",
                "dialogue_at_03": "جہاں تم جیسے سوال پوچھنے والوں کو داخلہ نہیں ملتا! (Jahan tum jaise sawal poochne walon ko dakhla nahi milta!)"
            }
        ]
    }
]

def get_gemini_api_key():
    """Locates the AI Studio API key from project folders."""
    candidates = [
        Path(r"D:\Family Comedy\aistuio free key.txt"),
        Path(r"D:\Larka Larki\aistuio free key.txt"),
        Path(__file__).resolve().parent.parent / "aistuio free key.txt",
        Path("aistuio free key.txt")
    ]
    for p in candidates:
        if p.exists():
            try:
                k = p.read_text(encoding="utf-8").strip()
                if k:
                    return k
            except Exception:
                pass
    return None

def clean_devanagari(text):
    """Safety filter: guarantees zero Hindi/Devanagari characters slip into Urdu output."""
    if not text:
        return ""
    replacements = {
        "अच्छा": "اچھا", "क्या": "کیا", "लड़के": "لڑکے", "लड़का": "لڑکا",
        "लड़की": "لڑکی", "पर": "پر", "तो": "تو", "तुम": "تم", "हो": "ہو",
        "री": "ری", "के": "کے", "کی": "کی", "का": "کا", "है": "ہے", "ہیں": "ہیں"
    }
    for dev, urd in replacements.items():
        text = text.replace(dev, urd)
    text = re.sub(r'[\u0900-\u097F]+', '', text)
    return text.strip()

def get_next_episode_id():
    if os.path.exists(HISTORY_LEDGER_PATH):
        try:
            with open(HISTORY_LEDGER_PATH, "r", encoding="utf-8") as f:
                ledger = json.load(f)
                if ledger:
                    return max(item.get("episode_id", 0) for item in ledger) + 1
        except Exception:
            pass
    return 1

def get_wardrobe_by_id(wardrobe_id=None):
    if wardrobe_id:
        for w in COUPLE_WARDROBE_SETS:
            if w["id"] == wardrobe_id:
                return w
    ep_id = get_next_episode_id()
    return COUPLE_WARDROBE_SETS[(ep_id - 1) % len(COUPLE_WARDROBE_SETS)]

def format_multi_scene_prompts(data, wardrobe=None):
    """Generates precise video prompts for as many scenes as the script requires (2, 3, 4, 5+ scenes)."""
    if not wardrobe:
        wardrobe = get_wardrobe_by_id()

    title = data.get("title", "Larka & Larki Comedy")
    location = data.get("location", "Modern Cafe")
    prop = data.get("prop", "Smartphone and coffee cup")
    raw_scenes = data.get("scenes", [])

    formatted_scenes = []

    for sc in raw_scenes:
        num = sc.get("scene_num", len(formatted_scenes) + 1)
        dialogues = sc.get("dialogues", [])

        # Backward compatibility if dialogues list is not present
        if not dialogues:
            d00 = sc.get("dialogue_at_00")
            sp00 = sc.get("speaker_at_00", "Larka")
            if d00:
                dialogues.append({"timestamp": "0:00", "speaker": sp00, "line": d00})
            d03 = sc.get("dialogue_at_03")
            sp03 = sc.get("speaker_at_03", "Larki")
            if d03:
                dialogues.append({"timestamp": "0:03", "speaker": sp03, "line": d03})

        # Build simple, clean dialogue script format
        script_lines = []
        for beat in dialogues:
            sp = beat.get("speaker", "Larka")
            line = clean_devanagari(beat.get("line") or beat.get("dialogue", ""))
            if not line:
                continue

            is_larka = "larka" in str(sp).lower() or "boy" in str(sp).lower()
            name = "Boy" if is_larka else "Girl"
            tag = "@Larka" if is_larka else "@Larki"
            script_lines.append({"name": name, "tag": tag, "line": line, "is_larka": is_larka})

        # Build the dialogue block as a simple script
        if num == 1:
            dialogue_script = "Dialogue script (characters face each other, never look at camera):\n"
            for sl in script_lines:
                dialogue_script += f'{sl["tag"]} ({sl["name"]}): "{sl["line"]}"\n'
        else:
            dialogue_script = "Dialogue script (characters face each other, never look at camera):\n"
            for sl in script_lines:
                desc = "the young man" if sl["is_larka"] else "the young woman"
                dialogue_script += f'{desc} ({sl["name"]}): "{sl["line"]}"\n'

        if num == 1:
            prop_desc = f" with {prop.lower()} featured between them" if prop else ""

            # Step 1: Keyframe Image Prompt (T2I)
            image_prompt = (
                f"Cinematic keyframe production still photograph. "
                f"Keep their facial features consistent with the attached @Larka and @Larki character references. "
                f"@Larka wears {wardrobe['larka']}, @Larki wears {wardrobe['larki']}. "
                f"Pakistani {location.lower()} setting{prop_desc}. "
                f"Interior decor constraint: Plain clean walls with modern simple abstract art or landscape painting only. Absolutely NO Arabic script, NO calligraphy wall frames, NO religious verses, and NO text on walls or banners. "
                f"Camera & Optics: Shot on 50mm prime cinematic lens with natural shallow depth of field, softly blurred background. Fixed eye-level medium-wide shot with smooth stable framing, no jittery camera motion, no cuts, no reverse angles. "
                f"Open 3/4 Camera Staging with realistic depth: Both characters are angled toward the camera lens in an open 3/4 stance with natural realistic spatial distance, so BOTH characters' full faces, eyes, and mouth expressions are clearly visible simultaneously. "
                f"@Larka stands or sits on screen-LEFT angled in a three-quarter stance toward the camera, and @Larki stands or sits on screen-RIGHT angled in a three-quarter stance toward the camera. "
                f"NEITHER character has their back turned to the camera. Spacious natural staging with proper environmental depth, strictly NO cramped side-by-side squishing. "
                f"Lighting & Atmosphere: Soft natural directional lighting with gentle ambient shadows, warm cinematic color grade. "
                f"Negative Constraints: Completely clean plain walls with NO Arabic script, NO framed calligraphy, NO religious verses. Strictly NO text on clothing, NO extra fingers, NO blurry facial artifacts. "
                f"Single still frame keyframe photograph, razor sharp facial focus, natural eyes looking toward scene, perfectly positioned for subsequent video animation. Ultra photorealistic 8k aesthetic, 9:16 vertical video composition."
            )

            # Step 2: Video Motion / Lip-Sync Prompt (I2V)
            i2v_prompt = (
                f"Animate seamlessly from this exact starting keyframe image, strictly maintaining identical character faces, clothing, environment, and lighting. "
                f"Fixed medium-wide stationary eye-level camera, no cuts, no panning, no camera motion. "
                f"{dialogue_script}"
                f"Characters look at each other with expressive comedic timing and natural mouth articulation, never directly into the camera lens. No unscripted dialogue. Continuous 10-second single take, photorealistic smooth motion."
            )

            # Direct Text-to-Video
            prompt_text = (
                f"Keep their facial features consistent with the attached @Larka and @Larki character references. "
                f"@Larka wears {wardrobe['larka']}, @Larki wears {wardrobe['larki']}. "
                f"Pakistani {location.lower()} setting{prop_desc}. "
                f"Interior decor constraint: Plain clean walls with modern simple abstract art or landscape painting only. Absolutely NO Arabic script, NO calligraphy wall frames, NO religious verses, and NO text on walls or banners. "
                f"Camera & Optics: Shot on 50mm prime cinematic lens with subtle shallow depth of field, softly blurred background. Fixed eye-level medium-wide shot with smooth stable framing, no jittery camera motion, no cuts, no reverse angles. "
                f"Open 3/4 Camera Staging with realistic depth: Both characters are angled toward the camera lens in an open 3/4 stance with natural realistic spatial distance, so BOTH characters' full faces, eyes, and mouth expressions are clearly visible simultaneously. "
                f"@Larka stands or sits on screen-LEFT angled in a three-quarter stance toward the camera, and @Larki stands or sits on screen-RIGHT angled in a three-quarter stance toward the camera. "
                f"NEITHER character has their back turned to the camera. Spacious natural staging with proper environmental depth, strictly NO cramped side-by-side squishing. DO NOT swap their positions. "
                f"Fixed medium-wide camera shot, stationary camera, no cuts, no close-ups, no reverse angles. "
                f"{dialogue_script}"
                f"Characters look at each other with expressive comedic timing, never directly into the camera lens. No unscripted dialogue. Ultra photorealistic 8k cinematic aesthetic, 9:16 vertical video composition."
            )
        else:
            # Scene 2, 3, 4, 5... (Image-to-Video Continuation with ZERO @ tags!)
            image_prompt = ""
            i2v_prompt = (
                f"Continue seamlessly from this exact starting frame, same faces, outfits, lighting. "
                f"Same positions: young man on screen-LEFT, young woman on screen-RIGHT. Do not swap. "
                f"Fixed medium-wide camera, no cuts, no zooms. "
                f"{dialogue_script}"
                f"Characters look at each other, never at camera. No unscripted dialogue."
            )
            prompt_text = i2v_prompt

        formatted_scenes.append({
            "scene_num": num,
            "title": f"Scene {num} Prompt ({'Initial T2V with @Tags' if num == 1 else f'Part {num} Continuation • ZERO @Tags'})",
            "prompt": prompt_text,
            "image_prompt": image_prompt,
            "i2v_prompt": i2v_prompt,
            "dialogues": dialogues
        })

    s1_prompt = formatted_scenes[0]["prompt"] if formatted_scenes else ""
    s2_prompt = formatted_scenes[1]["prompt"] if len(formatted_scenes) > 1 else s1_prompt
    img_prompt = formatted_scenes[0].get("image_prompt", "") if formatted_scenes else ""
    i2v_p = formatted_scenes[0].get("i2v_prompt", "") if formatted_scenes else ""

    return {
        "title": title,
        "location": location,
        "prop": prop,
        "wardrobe": wardrobe,
        "total_scenes": len(formatted_scenes),
        "scenes": formatted_scenes,
        "image_prompt": img_prompt,
        "i2v_prompt": i2v_p,
        "video_prompt": s1_prompt,
        "scene1_prompt": s1_prompt,
        "scene2_prompt": s2_prompt
    }

def get_openai_api_key():
    """Locates and extracts the OpenAI API key from project folders."""
    candidates = [
        Path(r"D:\Family Comedy\openai key.txt"),
        Path(r"D:\Larka Larki\openai key.txt"),
        Path(__file__).resolve().parent.parent / "openai key.txt",
        Path("openai key.txt")
    ]
    for p in candidates:
        if p.exists():
            try:
                content = p.read_text(encoding="utf-8")
                m = re.search(r'sk-[a-zA-Z0-9_\-]+', content)
                if m:
                    return m.group(0)
            except Exception:
                pass
    return None

def parse_with_openai(prompt):
    """Calls OpenAI gpt-5 (with gpt-4o fallback) to parse the script into structured JSON."""
    key = get_openai_api_key()
    if not key:
        return None
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    # Primary high-end models: gpt-5.4 first, then gpt-5, then gpt-4o
    openai_models = ["gpt-5.4", "gpt-5", "gpt-4o", "gpt-4.1"]
    for model in openai_models:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a professional Pakistani comedy dialogue supervisor. Return only clean, valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        # GPT-5 is a deep reasoning model and takes 25-40 seconds for complex JSON
        model_timeout = 50 if "gpt-5" in model else 25
        try:
            with urllib.request.urlopen(req, timeout=model_timeout) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                content = res["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as e:
            print(f"[OpenAI {model} Error]: {e}")
            continue
    return None

def parse_with_gemini(prompt):
    """Fallback: Calls Gemini API to parse script into structured JSON."""
    api_key = get_gemini_api_key()
    if not api_key:
        return None
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }
    models_to_try = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-flash-latest"]
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=14) as resp:
                res = json.loads(resp.read().decode())
                raw_out = res["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(raw_out)
        except Exception:
            continue
    return None

def call_ai_multi_scene_parse(raw_text):
    """Parses full user script across scenes using OpenAI as primary, Gemini as fallback."""
    prompt = f"""You are an expert Pakistani comedy dialogue supervisor.
The user provided their own script in Roman Urdu or Urdu for a Pakistani comedy sketch between two characters (@Larka and @Larki).

CRITICAL STRICT RULES:
1. PRESERVE 100% OF THE USER'S DIALOGUES AND JOKES:
   - DO NOT DROP OR OMIT ANY LINE! Every single line provided by the user must appear in the output.
   - DO NOT REWRITE OR INVENT DIFFERENT JOKES. Keep the user's exact story and comedic premise.
2. SHORT-WORD / SINGLE-WORD SAFETY EXPANSION (CRITICAL FOR VIDEO AI):
   - Ultra-short lines (1 to 2 words, like "Kya?", "Hain?", "Kyun?", "Achha?") confuse video AI speech generation and cause speaker-swapping bugs.
   - You MUST expand any bare 1-2 word line into a natural, full conversational phrase based on the context.
   - Example 1: If user wrote "Larki: Kya?", expand to "کیا؟ کونسا راستہ؟ (Kya? Konsa raasta?)" or "کیا کہہ رہے ہو؟ (Kya keh rahe ho?)".
   - Example 2: If user wrote "Larki: Achha?", expand to "اچھا؟ واقعی؟ (Achha? Waqayi?)".
   - DO NOT leave any dialogue line as a single bare word! Give each line at least 3-5 words so the video character has enough speech time.
3. GRAMMAR & TYPO CORRECTION:
   - Fix spelling mistakes, typos, and grammatical errors (e.g. "Teri sun Tou ley gey" -> "تیری سن تو لیں گے! (Teri sun toh lenge!)").
4. CONVERT TO AUTHENTIC URDU SCRIPT:
   - Provide the pure Urdu script (Perso-Arabic letters: حروفِ تہجی) followed by clean Roman Urdu in parentheses:
     Format: "اردو مکالمہ (Clean Roman Urdu)"
   - STRICTLY NO HINDI / DEVANAGARI!
5. TIMELINE PACING (10-SECOND CLIPS):
   - In Google Flow, each generated video clip is 10 seconds long.
   - Split the dialogues logically across scenes so dialogues are well-timed and natural (not rushed, and not leaving giant empty gaps).
   - Typically, a 10-second scene contains 2 to 3 dialogue turns (e.g. at timestamps "0:00", "0:03", "0:06").
   - If dialogue has 4+ lines, split into Scene 1, Scene 2 (or Scene 3 if needed).
   - For each scene, return:
     - "scene_num": integer (1, 2, 3...)
     - "dialogues": array of objects:
       [
         {{"timestamp": "0:00", "speaker": "Larka", "line": "اب بس ایک ہی راستہ بچا ہے! (Ab bas ek hi raasta bacha hai!)"}},
         {{"timestamp": "0:03", "speaker": "Larki", "line": "کیا؟ کونسا راستہ بچا ہے؟ (Kya? Konsa raasta bacha hai?)"}}
       ]
6. DYNAMIC SCRIPT-DRIVEN LOCATION & PROPS:
   - Analyze the script's theme and comedic vibe to pick the PERFECT Pakistani location and matching physical props.
   - Do NOT just default to cafe if the conversation fits somewhere else!
   - Diverse location options include:
     * "Cozy Pakistani Restaurant / Dhaba" (with food plates, chai karak cups, water bottle)
     * "College Campus Garden / Lawns" (sitting on a wooden bench with textbooks and backpacks)
     * "Vibrant College Cafeteria" (cafeteria table with cold drinks, samosa plate, and student IDs)
     * "Modern Trendy Cafe" (aesthetic wooden table with iced latte cups and smartphones)
     * "Chaotic Lahore / Karachi Street Corner" (with street carts, bun kabab wrapper, and tea stall)
     * "Park Walking Path / Bench" (surrounded by trees and flowering bushes with sunglasses and water bottle)
     * "Shopping Mall Food Court" (tray with fast-food packaging and shopping bags)
     * "Rooftop Terrace at Sunset" (with tea glasses and scenic Pakistani city skyline background)
   - Choose a setting and matching prop that enhances the humor and visual realism of the characters' interaction.
   - "title": Short catchy comedy title (Urdu + Roman)
   - "location": Descriptive setting in English (e.g. "College Campus Garden on a wooden bench" or "Vibrant College Cafeteria")
   - "prop": Natural props fitting that location in English (e.g. "Textbooks, notebooks, and cold drink bottles")

Respond ONLY with a valid JSON object matching this schema:
{{
  "title": "Title (Urdu + Roman)",
  "location": "English location",
  "prop": "English prop",
  "scenes": [
    {{
      "scene_num": 1,
      "dialogues": [
        {{"timestamp": "0:00", "speaker": "Larka", "line": "اردو متن (Roman Urdu)"}}
      ]
    }}
  ]
}}

User Script:
\"\"\"{raw_text}\"\"\"
"""

    # 1. Try OpenAI first (User's primary key)
    data = parse_with_openai(prompt)
    if not data or not data.get("scenes"):
        # 2. Fallback to Gemini if OpenAI fails or quota full
        print("[AI Parser]: Falling back to Gemini API...")
        data = parse_with_gemini(prompt)

    if data and data.get("scenes"):
        for sc in data.get("scenes", []):
            for d in sc.get("dialogues", []):
                if d.get("line"):
                    d["line"] = clean_devanagari(d["line"])
            if sc.get("dialogue_at_00"):
                sc["dialogue_at_00"] = clean_devanagari(sc["dialogue_at_00"])
            if sc.get("dialogue_at_03"):
                sc["dialogue_at_03"] = clean_devanagari(sc["dialogue_at_03"])
        return data

    return None

def call_gemini_multi_scene_parse(raw_text):
    """Backward compatibility alias."""
    return call_ai_multi_scene_parse(raw_text)

def get_joke_by_id(joke_id, wardrobe_id=None):
    wardrobe = get_wardrobe_by_id(wardrobe_id)
    for joke in COUPLE_PRESETS:
        if joke["id"] == joke_id:
            return format_multi_scene_prompts(joke, wardrobe=wardrobe)
    return None

def smart_parse_raw_text(raw_text, wardrobe_id=None):
    wardrobe = get_wardrobe_by_id(wardrobe_id)

    # 1. Try AI multi-scene parsing (OpenAI primary, Gemini fallback)
    ai_data = call_ai_multi_scene_parse(raw_text)
    if ai_data and ai_data.get("scenes"):
        return format_multi_scene_prompts(ai_data, wardrobe=wardrobe)

    # 2. Offline Fallback: Partition user lines into 2 lines per scene
    clean = raw_text.strip()
    raw_lines = [line.strip() for line in clean.splitlines() if line.strip()]

    extracted = []
    for line in raw_lines:
        m = re.match(r'^(larka|larki|boy|girl|ladka|ladki)\s*[:：\-]\s*(.*)$', line, flags=re.IGNORECASE)
        if m:
            speaker = "Larka" if any(k in m.group(1).lower() for k in ["larka", "boy", "ladka"]) else "Larki"
            content = m.group(2).strip()
            extracted.append((speaker, content))
        else:
            extracted.append(("Larka" if len(extracted) % 2 == 0 else "Larki", line))

    fallback_scenes = []
    for i in range(0, len(extracted), 2):
        s_num = (i // 2) + 1
        sp1, d1 = extracted[i]
        sp2, d2 = extracted[i+1] if i+1 < len(extracted) else (None, None)
        fallback_scenes.append({
            "scene_num": s_num,
            "speaker_at_00": sp1,
            "dialogue_at_00": d1,
            "speaker_at_03": sp2,
            "dialogue_at_03": d2
        })

    fallback_data = {
        "title": "Larka & Larki Comedy",
        "location": "Modern Cafe / Street Corner",
        "prop": "Smartphone and coffee cup",
        "scenes": fallback_scenes
    }
    return format_multi_scene_prompts(fallback_data, wardrobe=wardrobe)
