import os
import json
import random
import re
import urllib.request
from pathlib import Path

IDEAS_BANK_PATH = "data/ideas_bank.json"
HISTORY_LEDGER_PATH = "data/history_ledger.json"

VIRAL_FRIEND_JOKES = [
    {
        "id": "roza_bike",
        "title": "موٹر سائیکل کا روزہ (Motorcycle Roza)",
        "location": "House Porch / Driveway",
        "prop": "Old motorcycle",
        "scenes": [
            {
                "scene_num": 1,
                "speaker_at_00": "Beta",
                "dialogue_at_00": "ابو پٹرول ختم نہیں ہوا، موٹر سائیکل کا آج روزہ ہے! (Abbu petrol khatam nahi hua, motorcycle ka aaj roza hai!)",
                "speaker_at_03": "Abbu",
                "dialogue_at_03": "ہاں اور شام کو افطاری میں تیرے گردے بیچ کر پٹرول ڈلوائیں گے! (Haan aur shaam ko iftari mein tere gurday bech kar petrol dalwayein ge!)"
            },
            {
                "scene_num": 2,
                "speaker_at_00": "Beta",
                "dialogue_at_00": "امی ابو کو بولیں غصہ نہ کریں، ثواب کا کام ہے! (Ammi Abbu ko bolein ghussa na karein, sawab ka kaam hai!)",
                "speaker_at_03": "Ammi",
                "dialogue_at_03": "بیٹا اس کا روزہ ہے تو اب دھکا بھی یہی لگائے گی! (Beta is ka roza hai toh ab dhakka bhi yehi lagaye gi!)"
            }
        ]
    },
    {
        "id": "loadshedding_candle",
        "title": "لوڈشیڈنگ اور موبائل (Loadshedding & Candle)",
        "location": "Living Room Sofa",
        "prop": "Wax candle and smartphone",
        "scenes": [
            {
                "scene_num": 1,
                "speaker_at_00": "Beta",
                "dialogue_at_00": "امی لائٹ چلی گئی ہے، میرا موبائل مرنے والا ہے! (Ammi light chali gayi hai, mera mobile marne wala hai!)",
                "speaker_at_03": "Ammi",
                "dialogue_at_03": "بیٹا وہ سامنے موم بتی پڑی ہے، جلدی سے جلا لو! (Beta woh samnay mom batti pari hai, jaldi se jala lo!)"
            },
            {
                "scene_num": 2,
                "speaker_at_00": "Beta",
                "dialogue_at_00": "امی موم بتی سے موبائل چارج ہو جائے گا کیا؟ (Ammi mom batti se mobile charge ho jaye ga kya?)",
                "speaker_at_03": "Abbu",
                "dialogue_at_03": "ہاں فون موم بتی کے اوپر رکھ، تاکہ خرچہ اور عقل دونوں جلیں! (Haan phone mom batti ke ooper rakh, taakay kharcha aur aqal dono jalein!)"
            }
        ]
    },
    {
        "id": "jugaad_fan",
        "title": "پاکستانی جگاڑ پنکھا (Manual Fan Jugaad)",
        "location": "Bed Room",
        "prop": "Ceiling fan and long wooden broom handle",
        "scenes": [
            {
                "scene_num": 1,
                "speaker_at_00": "Beta",
                "dialogue_at_00": "ابو پنکھا بند تھا، میں اسے جھاڑو سے گھما رہا ہوں! (Abbu pankha band tha, main isay jharoo se ghuma raha hoon!)",
                "speaker_at_03": "Abbu",
                "dialogue_at_03": "یہ کیا پاگل پن کر رہے ہو؟ (Yeh kya pagal pan kar rahay ho?)"
            },
            {
                "scene_num": 2,
                "speaker_at_00": "Beta",
                "dialogue_at_00": "ابو یہ پاکستانی جگاڑ ہے، بجلی کا بل بھی کم اور ہوا بھی پوری! (Abbu yeh Pakistani jugaad hai, bijli ka bill bhi kam aur hawa bhi poori!)",
                "speaker_at_03": "Ammi",
                "dialogue_at_03": "شاباش! کل کو روٹی بھی تصویر دیکھ کر کھا لینا، راشن کا خرچہ بھی بچے گا! (Shabash! Kal ko roti bhi tasweer dekh kar kha lena, ration ka kharcha bhi bachay ga!)"
            }
        ]
    }
]

WARDROBE_SETS = [
    {
        "id": "casual_modern",
        "name": "Casual Western (Maroon Polo & Royal Blue)",
        "beta": "a stylish maroon casual polo t-shirt with blue denim jeans",
        "ammi": "a bright royal blue printed lawn suit with floral chiffon dupatta",
        "abbu": "a crisp white shalwar kameez with a light brown tweed waistcoat"
    },
    {
        "id": "festive_kurta",
        "name": "Festive Desi (Black Kurta & Mustard Lawn)",
        "beta": "a stylish black festive cotton kurta with rolled sleeves",
        "ammi": "a vibrant mustard yellow embroidered kurta with floral dupatta",
        "abbu": "a charcoal grey shalwar kameez with a sleek dark waistcoat"
    },
    {
        "id": "pastel_summer",
        "name": "Summer Pastels (Sky Blue & Peach Lawn)",
        "beta": "a light sky-blue casual linen shirt with rolled cuffs and khaki trousers",
        "ammi": "a soft peach pastel shalwar kameez with printed lawn dupatta",
        "abbu": "a classic beige cotton kurta pyjama"
    },
    {
        "id": "cozy_evening",
        "name": "Evening Warm (Olive Hoodie & Deep Maroon)",
        "beta": "an olive green casual hoodie sweater with dark trousers",
        "ammi": "a deep maroon embroidered silk-blend kurta suit",
        "abbu": "a navy blue pathani suit with a tailored Nehru vest"
    },
    {
        "id": "traditional_lahori",
        "name": "Traditional Lahori (Mustard Kurta & Mint Green)",
        "beta": "a mustard yellow casual cotton kurta with dark jeans",
        "ammi": "a mint green embroidered lawn suit with printed dupatta",
        "abbu": "a crisp off-white cotton kurta with a brown waistcoat"
    }
]

def get_gemini_api_key():
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
    return 9

def get_wardrobe_by_id(wardrobe_id=None):
    if wardrobe_id:
        for w in WARDROBE_SETS:
            if w["id"] == wardrobe_id:
                return w
    ep_id = get_next_episode_id()
    return WARDROBE_SETS[(ep_id - 1) % len(WARDROBE_SETS)]

def get_family_speaker_info(name):
    clean = str(name).strip().lower()
    if any(k in clean for k in ["ammi", "mother", "maa", "mom", "bahu"]):
        return {
            "tag": "@Ammi",
            "desc": "the dramatic mother (Ammi)",
            "pronoun": "her",
            "screen_pos": "in the CENTER"
        }
    elif any(k in clean for k in ["abbu", "father", "baap", "dad", "sasur"]):
        return {
            "tag": "@Abbu",
            "desc": "the strict older father (Abbu)",
            "pronoun": "his",
            "screen_pos": "on screen-RIGHT"
        }
    elif any(k in clean for k in ["boss", "manager", "officer", "doctor", "teacher", "ustaad", "dukaandar", "shopkeeper", "police", "interviewer"]):
        tag_name = clean.capitalize()
        return {
            "tag": f"@{tag_name}",
            "desc": f"the strict {clean} (authority figure)",
            "pronoun": "his",
            "screen_pos": "on screen-RIGHT"
        }
    else:
        # Relatable young protagonist: Mulazim, Employee, Student, Patient, Customer, or Beta
        return {
            "tag": "@Beta",
            "desc": "the 25-year-old grown adult son (Beta)",
            "pronoun": "his",
            "screen_pos": "on screen-LEFT"
        }

def format_family_multi_scene_prompts(data, wardrobe=None):
    if not wardrobe:
        wardrobe = get_wardrobe_by_id()

    title = data.get("title", "Pakistani Sitcom Episode")
    location = data.get("location", "Living Room Sofa")
    prop = data.get("prop", "Hand prop")
    raw_scenes = data.get("scenes", [])

    formatted_scenes = []

    for sc in raw_scenes:
        num = sc.get("scene_num", len(formatted_scenes) + 1)
        dialogues = sc.get("dialogues", [])

        # Backward compatibility if dialogues list is not present
        if not dialogues:
            d00 = sc.get("dialogue_at_00")
            sp00 = sc.get("speaker_at_00", "Beta")
            if d00:
                dialogues.append({"timestamp": "0:00", "speaker": sp00, "line": d00})
            d03 = sc.get("dialogue_at_03")
            sp03 = sc.get("speaker_at_03", "Abbu")
            if d03:
                dialogues.append({"timestamp": "0:03", "speaker": sp03, "line": d03})

        # Build simple, clean dialogue script format
        script_lines = []
        for beat in dialogues:
            sp_name = beat.get("speaker", "Beta")
            line = clean_devanagari(beat.get("line") or beat.get("dialogue", ""))
            if not line:
                continue

            sp_info = get_family_speaker_info(sp_name)
            script_lines.append({"tag": sp_info["tag"], "desc": sp_info["desc"], "line": line})

        # Build the dialogue block as a simple script
        if num == 1:
            dialogue_script = "Dialogue script (characters face each other, never look at camera):\n"
            for sl in script_lines:
                dialogue_script += f'{sl["tag"]}: "{sl["line"]}"\n'
        else:
            dialogue_script = "Dialogue script (characters face each other, never look at camera):\n"
            for sl in script_lines:
                dialogue_script += f'{sl["desc"]}: "{sl["line"]}"\n'

        # Determine which characters actually have dialogue or are involved in this scene
        speakers_in_scene = set()
        for sl in script_lines:
            speakers_in_scene.add(sl["tag"])

        has_beta = "@Beta" in speakers_in_scene
        has_ammi = "@Ammi" in speakers_in_scene
        has_abbu = "@Abbu" in speakers_in_scene

        staging_text = sc.get("staging") or data.get("staging") or ""
        is_staircase_scene = (
            "stair" in location.lower() or 
            "steps" in location.lower() or 
            "stair" in str(staging_text).lower()
        )

        if num == 1:
            prop_desc = f" with {prop.lower()} featured in the scene" if prop else ""
            
            # 1. Abbu & Ammi Duo (Husband & Wife banter - e.g. door conversation, living room, kitchen)
            if has_abbu and has_ammi and not has_beta:
                chars_present = "@Abbu and @Ammi"
                wardrobe_desc = f"@Ammi wears {wardrobe['ammi']}, @Abbu wears {wardrobe['abbu']}"
                pos_desc = (
                    "Side-profile two-shot in 3/4 angle: The camera captures both characters from an angled profile perspective so BOTH characters' full faces, eyes, and mouth expressions are clearly visible to the camera simultaneously. "
                    "@Ammi is on screen-LEFT angled in a three-quarter stance toward the camera, while @Abbu is on screen-RIGHT angled in a three-quarter stance toward the camera. "
                    "NEITHER character has their back turned to the camera. Both faces are in clear view throughout the entire clip as they converse. DO NOT swap their positions. @Beta is NOT in this frame. "
                    "FACIAL EMOTION LOCK: Characters maintain expressive comedic facial reactions consistent with the punchline (shocked, exasperated or smirking), never laughing at their own insult"
                )
                dialogue_instruction = "Dialogue script (@Abbu and @Ammi face each other with fast comedic timing, never look directly into camera lens):\n"

            # 2. Abbu & Beta Duo (Father & Son banter)
            elif has_abbu and has_beta and not has_ammi:
                chars_present = "@Abbu and @Beta"
                wardrobe_desc = f"@Beta wears {wardrobe['beta']}, @Abbu wears {wardrobe['abbu']}"
                pos_desc = (
                    "Side-profile two-shot in 3/4 angle: The camera captures both characters from an angled profile perspective so BOTH characters' full faces, eyes, and mouth expressions are clearly visible to the camera simultaneously. "
                    "@Beta stands or sits on screen-LEFT angled in a three-quarter stance toward the camera, while @Abbu is on screen-RIGHT angled in a three-quarter stance toward the camera. "
                    "NEITHER character has their back turned to the camera. Both faces are in clear view throughout the entire clip as they converse. DO NOT swap their positions. @Ammi is NOT in this frame. "
                    "FACIAL EMOTION LOCK: @Beta must NOT smile or laugh at the punchline; @Beta keeps a crestfallen, offended, or shocked reaction throughout. Only @Abbu chuckles or smiles"
                )
                dialogue_instruction = "Dialogue script (@Beta and @Abbu face each other with fast comedic timing, never look directly into camera lens):\n"

            # 3. Ammi & Beta Duo (Mother & Son)
            elif has_ammi and has_beta and not has_abbu:
                chars_present = "@Ammi and @Beta"
                wardrobe_desc = f"@Beta wears {wardrobe['beta']}, @Ammi wears {wardrobe['ammi']}"
                if is_staircase_scene:
                    pos_desc = (
                        "Over-the-shoulder rear shot / back view from behind @Ammi: The camera is placed directly behind @Ammi, "
                        "showing the back of her head and shoulders. @Ammi stands at the bottom step with her entire body and front facing directly into the wooden staircase, "
                        "looking straight UP at the ascending stairs toward the second-floor landing. "
                        "Her back is to the camera throughout the entire clip. Her face and gaze are directed straight up the stairs. "
                        "@Abbu is NOT in this frame"
                    )
                    dialogue_instruction = "Dialogue script (@Ammi shouts straight UP the stairs from behind camera perspective):\n"
                else:
                    pos_desc = (
                        "Side-profile two-shot in 3/4 angle: The camera captures both characters from an angled profile perspective so BOTH characters' full faces, eyes, and mouth expressions are clearly visible to the camera simultaneously. "
                        "@Beta stands on screen-LEFT angled in a three-quarter stance toward the camera, while @Ammi stands on screen-RIGHT angled in a three-quarter stance toward the camera. "
                        "NEITHER character has their back turned to the camera. Both faces are in clear view throughout the entire clip as they converse. DO NOT swap their positions. @Abbu is NOT in this frame"
                    )
                    dialogue_instruction = "Dialogue script (@Beta and @Ammi face each other with fast comedic timing, never look directly into camera lens):\n"

            # 4. Ammi Alone
            elif has_ammi and not has_beta and not has_abbu:
                chars_present = "@Ammi"
                wardrobe_desc = f"@Ammi wears {wardrobe['ammi']}"
                if is_staircase_scene:
                    pos_desc = (
                        "Over-the-shoulder rear shot / back view from behind @Ammi: The camera is placed directly behind @Ammi, "
                        "showing the back of her head and shoulders. @Ammi stands at the bottom step with her entire body and front facing directly into the wooden staircase, "
                        "looking straight UP at the ascending stairs toward the second-floor landing. "
                        "Her back is to the camera throughout the entire clip. Her face and gaze are directed straight up the stairs. "
                        "Neither @Abbu nor @Beta are visible in this frame"
                    )
                    dialogue_instruction = "Dialogue script (@Ammi shouts straight UP the stairs from behind camera perspective):\n"
                else:
                    pos_desc = "@Ammi is in CENTER frame looking expressive. Neither @Abbu nor @Beta are visible in this frame"
                    dialogue_instruction = "Dialogue script (@Ammi speaks with expressive comedic timing, never looks at camera):\n"

            # 5. Beta Alone
            elif has_beta and not has_ammi and not has_abbu:
                chars_present = "@Beta"
                wardrobe_desc = f"@Beta wears {wardrobe['beta']}"
                pos_desc = "@Beta is in CENTER frame looking exasperated. Neither @Ammi nor @Abbu are visible in this frame"
                dialogue_instruction = "Dialogue script (Beta speaks to himself exasperated):\n"

            # 6. Abbu Alone
            elif has_abbu and not has_ammi and not has_beta:
                chars_present = "@Abbu"
                wardrobe_desc = f"@Abbu wears {wardrobe['abbu']}"
                pos_desc = "@Abbu is in CENTER frame looking thoughtful or amused. Neither @Ammi nor @Beta are visible in this frame"
                dialogue_instruction = "Dialogue script (Abbu speaks with witty comedic delivery):\n"

            # 7. Workplace / External Scene (@Beta paired with @Boss, @Doctor, @Teacher, etc.)
            external_speakers = [s for s in speakers_in_scene if s not in ["@Beta", "@Ammi", "@Abbu"]]
            if has_beta and external_speakers and not has_ammi and not has_abbu:
                ext_tag = external_speakers[0]
                chars_present = f"@Beta reference"
                if "boss" in ext_tag.lower():
                    wardrobe_desc = f"@Beta wears a slightly crumpled light-blue office shirt with dark trousers. Alongside him is {ext_tag}, a stern 50-year-old Pakistani corporate manager wearing a formal charcoal suit and tie"
                    pos_desc = (
                        f"Side-profile two-shot in 3/4 angle: The camera is positioned so that BOTH characters' full faces and facial expressions are clearly visible to the camera at the same time. "
                        f"@Beta stands on screen-LEFT angled in a three-quarter stance toward the camera, and {ext_tag} sits on screen-RIGHT behind the desk angled toward the camera. "
                        f"NEITHER character has their back turned to the camera. Both faces are clearly seen emoting throughout. "
                        f"FACIAL EMOTION LOCK: {ext_tag} is furious and demanding, while @Beta keeps an anxious, fidgety comedic expression, never smiling at the scolding. "
                        f"DO NOT swap their positions. Neither @Ammi nor @Abbu are in this frame"
                    )
                else:
                    ext_name = ext_tag.replace("@", "")
                    wardrobe_desc = f"@Beta wears {wardrobe['beta']}. Alongside him is {ext_tag}, an authoritative Pakistani {ext_name}"
                    pos_desc = (
                        f"Side-profile two-shot in 3/4 angle: The camera is positioned so that BOTH characters' full faces and facial expressions are clearly visible to the camera at the same time. "
                        f"@Beta stands on screen-LEFT angled in a three-quarter stance toward the camera, and {ext_tag} is on screen-RIGHT as the authority figure angled toward the camera. "
                        f"NEITHER character has their back turned to the camera. Both faces are clearly seen emoting throughout. DO NOT swap their positions. Neither @Ammi nor @Abbu are in this frame"
                    )
                dialogue_instruction = f"Dialogue script ({ext_tag} and @Beta face each other with fast comedic timing, never look directly into camera lens):\n"

            # 8. Default: All Three Together (Family Sitcom)
            else:
                chars_present = "@Abbu, @Ammi, and @Beta"
                wardrobe_desc = f"@Beta wears {wardrobe['beta']}, @Ammi wears {wardrobe['ammi']}, @Abbu wears {wardrobe['abbu']}"
                pos_desc = (
                    "Open three-quarter staging: @Beta is on screen-LEFT angled 3/4 toward the camera, @Ammi is in CENTER, and @Abbu is on screen-RIGHT angled 3/4 toward the camera. "
                    "All three faces and facial expressions are clearly visible to the camera. NEITHER character turns their back to the lens. DO NOT swap their positions. @Beta must NOT smile at the punchline"
                )
                dialogue_instruction = "Dialogue script (characters face each other, never look directly into camera lens):\n"

            # Rebuild dialogue script with specific instruction
            dialogue_script = dialogue_instruction
            for sl in script_lines:
                dialogue_script += f'{sl["tag"]}: "{sl["line"]}"\n'

            loc_clean = location.lower()
            if any(k in loc_clean for k in ["office", "cabin", "clinic", "hospital", "shop", "street", "college", "school", "classroom"]):
                setting_prefix = f"Pakistani {location.lower()} setting"
            else:
                setting_prefix = f"Pakistani house {location.lower()} setting"

            prompt_text = (
                f"Keep their facial features consistent with the attached {chars_present}. "
                f"{wardrobe_desc}. "
                f"{setting_prefix}{prop_desc}. "
                f"{pos_desc}. "
                f"Camera & Optics: Shot on 50mm prime cinematic lens with natural shallow depth of field, softly blurred background. Fixed eye-level medium-wide shot with smooth stable framing, no jittery camera motion, no cuts, no reverse angles. "
                f"Lighting & Atmosphere: Soft natural directional indoor lighting with gentle ambient shadows, warm cinematic Pakistani drama aesthetic. "
                f"Negative Constraints: Interior decor constraint: Plain clean walls with modern geometric wallpaper or simple landscape painting only. Absolutely NO Arabic script, NO calligraphy wall frames, NO religious verses, NO text on clothing or walls, NO extra fingers or distorted limbs. "
                f"{dialogue_script}"
                f"Continuous action: Characters maintain their initial body orientation and direction throughout without turning towards the camera. No unscripted dialogue. Ultra photorealistic 8k cinematic sitcom aesthetic, 9:16 vertical video composition."
            )
        else:
            # Scene 2, 3... Intelligent Continuation
            if is_staircase_scene and has_beta:
                action_desc = (
                    "Gradual walking descent: The adult son (Beta) begins up at the top landing and slowly walks down the wooden steps step-by-step into frame. "
                    "As he reaches the lower steps, he pauses resting his hand on the wooden banister, looking down at Ammi with an amused, exasperated comedic expression before speaking. "
                    "@Ammi remains stationed at the bottom step with her back to camera looking up at him. "
                )
            else:
                action_desc = "Characters maintain their spatial positions facing each other, continuing their comedic conversation seamlessly. "

            prompt_text = (
                f"Continue seamlessly from this exact starting frame, keeping the exact same location, lighting, and wardrobe. "
                f"{action_desc}"
                f"Fixed medium-wide camera, no cuts, no zooms. "
                f"{dialogue_script}"
                f"Characters do not look into the camera lens. No unscripted dialogue."
            )

        formatted_scenes.append({
            "scene_num": num,
            "title": f"Scene {num} Prompt ({'Initial T2V with @Tags' if num == 1 else f'Part {num} Continuation • ZERO @Tags'})",
            "prompt": prompt_text,
            "dialogues": dialogues
        })

    s1_prompt = formatted_scenes[0]["prompt"] if formatted_scenes else ""
    s2_prompt = formatted_scenes[1]["prompt"] if len(formatted_scenes) > 1 else s1_prompt

    return {
        "title": title,
        "location": location,
        "prop": prop,
        "wardrobe": wardrobe,
        "total_scenes": len(formatted_scenes),
        "scenes": formatted_scenes,
        "scene1_prompt": s1_prompt,
        "scene2_prompt": s2_prompt
    }

def format_prompts(joke_data, wardrobe=None):
    """Backward compatibility alias for server.py"""
    return format_family_multi_scene_prompts(joke_data, wardrobe=wardrobe)

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

def parse_with_openai_family(prompt):
    """Calls OpenAI gpt-5 (with gpt-4o fallback) to parse the family script into structured JSON."""
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
                {"role": "system", "content": "You are a professional Pakistani sitcom comedy dialogue supervisor. Return only clean, valid JSON."},
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
            print(f"[OpenAI Family {model} Error]: {e}")
            continue
    return None

def parse_with_gemini_family(prompt):
    """Fallback: Calls Gemini API to parse family script into structured JSON."""
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

def call_ai_multi_scene_parse_family(raw_text):
    """Parses full user script across scenes using OpenAI as primary, Gemini as fallback."""
    prompt = f"""You are an expert Pakistani sitcom comedy dialogue supervisor.
The user provided their own script in Roman Urdu or Urdu for a Pakistani family sitcom featuring @Beta (son), @Ammi (mother), and @Abbu (father).

CRITICAL STRICT RULES:
1. PRESERVE 100% OF THE USER'S DIALOGUES AND JOKES:
   - DO NOT DROP OR OMIT ANY LINE! Every single line provided by the user must appear in the output.
   - DO NOT REWRITE OR INVENT DIFFERENT JOKES. Keep the user's exact story and comedic premise.
2. SHORT-WORD / SINGLE-WORD SAFETY EXPANSION (CRITICAL FOR VIDEO AI):
   - Ultra-short lines (1 to 2 words, like "Kya?", "Hain?", "Kyun?", "Achha?") confuse video AI speech generation and cause speaker-swapping bugs.
   - You MUST expand any bare 1-2 word line into a natural, full conversational phrase based on the context.
   - Example 1: If user wrote "Kya?", expand to "کیا؟ کیا کہہ رہے ہو؟ (Kya? Kya keh rahe ho?)" or context-appropriate question.
   - Example 2: If user wrote "Achha?", expand to "اچھا؟ واقعی؟ (Achha? Waqayi?)".
   - DO NOT leave any dialogue line as a single bare word! Give each line at least 3-5 words so the video character has enough speech time.
3. ACCURATE PHONETIC URDU SPELLING & PRONUNCIATION:
   - Make sure tricky Urdu idioms and English loanwords are written phonetically clear so video TTS does NOT mispronounce them:
   - Example 1: "Joru ka ghulam" must be written strictly as "جورو کا غلام (Joru ka ghulaam)". Do NOT write it as "جوڑوں" or anything that sounds like "joints / joron"!
   - Example 2: English sports/slang terms: "Hat-trick" (cricket bowling hat-trick). When writing Urdu, spell it phonetically as "ہَیٹ ٹرِک (Hat-trick)" or write the Roman Urdu "Hat-trick" clearly so TTS does NOT pronounce it as "Heat-trick" (ہیٹ)!
   - "Ran mureed" -> "رن مرید (Ran mureed)".
   - Fix grammatical slips while preserving raw comedic anger/emotion!
4. CONVERT TO AUTHENTIC URDU SCRIPT:
   - Provide the pure Urdu script (Perso-Arabic letters: حروفِ تہجی) followed by clean Roman Urdu in parentheses:
     Format: "اردو مکالمہ (Clean Roman Urdu)"
   - STRICTLY NO HINDI / DEVANAGARI!
5. TIMELINE PACING & SCENE BUDGET (CRITICAL):
   - In Google Flow, each generated video clip is fixed at 10 seconds.
   - DO NOT UNNECESSARILY SPLIT A SHORT JOKE INTO MULTIPLE SCENES!
   - If a script has 3 to 4 short snappy lines between 2 characters in the same room (e.g. Rishta joke: Beta asks, Abbu answers, Beta asks why, Abbu punchline):
     * KEEP IT IN 1 SINGLE SCENE (10 seconds total)!
     * Timing: 0:00 (Beta), 0:02 (Abbu), 0:05 (Beta), 0:07 (Abbu punchline).
     * This avoids dragging or stretching dialogue across 20 seconds!
   - ONLY split into Scene 1 and Scene 2 IF:
     * The script has 5 or more dialogue lines, OR
     * There is an actual location or perspective transition (e.g. Ammi calling downstairs in Scene 1, Beta walking down in Scene 2).
   - COMEDIC REACTION & EMOTION LOCK:
     * When @Beta receives bad news, an insult, or a marriage rejection ("inqaar" / "awara loafer"):
       @Beta must NEVER smile or smirk at the end of the clip!
       @Beta must maintain an offended, disappointed, or stunned jaw-dropped expression!
       Only the person delivering the roast/punchline (@Abbu) may chuckle or smile.
6. DYNAMIC SCRIPT-DRIVEN LOCATION, STAGING & PROPS:
   - READ THE SCRIPT CONTEXT CAREFULLY!
   - If Ammi is shouting "nechy aja" (come downstairs), DO NOT place the family sitting together on a sofa sipping tea!
     Instead choose: "Ground floor hallway near wooden staircase" with "Ammi looking up toward staircase shouting, Abbu holding newspaper looking alarmed".
   - If Beta is in his bedroom or coming down, stage it accordingly!
   - Other location options:
     * "Ground floor near staircase / Hallway" (Ammi shouting upstairs toward son's room)
     * "Traditional Pakistani Living Room" (seated on sofa/charpai with teacups and television remote)
     * "Family Dining Table / Dastarkhwan" (with traditional breakfast plates, parathas, and chai kettle)
     * "Pakistani Home Kitchen" (with cooking pots, spice jars, and rolling pin belan)
     * "Home Courtyard (Sehan) / Veranda" (under open sky with potted plants and steel glasses)
     * "Rooftop Terrace at Sunset" (with charpai, tea thermos, and laundry drying line in background)
   - "title": Short catchy comedy title (Urdu + Roman)
   - "location": Descriptive setting matching the script's actual narrative (e.g. "Hallway near bottom of staircase looking up", "Pakistani corporate office cabin with executive desk and laptop", "Doctor clinic", "Street dhaba")
   - "staging": Brief note on who is present and what they are doing (e.g. "@Ammi standing near stairs looking up shouting, @Abbu seated on chair watching", "@Boss seated behind desk shouting angrily, @Beta standing nervously in front")
   - "prop": Natural props fitting that location in English (e.g. "Wooden staircase railing, morning newspaper, and tea cup", "Executive wooden desk, laptop, office files, and office chair")
7. SITCOM UNIVERSE CASTING RULE (WORKPLACE & EXTERNAL JOKES):
   - Our sitcom series stars @Beta (the 25-year-old young adult son / relatable protagonist), @Abbu (father / elder figure), and @Ammi (mother).
   - When the user submits external, workplace, or non-family comedy scripts (e.g., Boss vs Employee/Mulazim, Doctor vs Patient, Teacher vs Student, Police vs Chor, Shopkeeper vs Customer):
     * ALWAYS CAST @Beta as the young protagonist (Employee/Mulazim, Patient, Student, Customer, etc.)!
     * In the "speaker" field, map the young employee/protagonist strictly to "Beta"!
     * In the "speaker" field, map the authority figure to "Boss" (or "Doctor", "Teacher", etc.)!
     * Example: For a Boss vs Mulazim joke, the speakers MUST be "Boss" and "Beta"!
     * Set "location" to the workplace/external setting (e.g. "Corporate office cabin with executive desk and laptop")!

Respond ONLY with a valid JSON object matching this schema:
{{
  "title": "Title (Urdu + Roman)",
  "location": "English location",
  "staging": "English staging description",
  "prop": "English prop",
  "scenes": [
    {{
      "scene_num": 1,
      "dialogues": [
        {{"timestamp": "0:00", "speaker": "Ammi", "line": "اردو متن (Roman Urdu)"}}
      ]
    }}
  ]
}}

User Script:
\"\"\"{raw_text}\"\"\"
"""

    # 1. Try OpenAI first (User's primary key)
    data = parse_with_openai_family(prompt)
    if not data or not data.get("scenes"):
        # 2. Fallback to Gemini if OpenAI fails or quota full
        print("[AI Family Parser]: Falling back to Gemini API...")
        data = parse_with_gemini_family(prompt)

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

def call_gemini_multi_scene_parse_family(raw_text):
    """Backward compatibility alias."""
    return call_ai_multi_scene_parse_family(raw_text)

def get_joke_by_id(joke_id, wardrobe_id=None):
    wardrobe = get_wardrobe_by_id(wardrobe_id)
    for joke in VIRAL_FRIEND_JOKES:
        if joke["id"] == joke_id:
            return format_family_multi_scene_prompts(joke, wardrobe=wardrobe)
    return None

def smart_parse_raw_text(raw_text, wardrobe_id=None):
    wardrobe = get_wardrobe_by_id(wardrobe_id)

    # 1. Try AI multi-scene parsing (OpenAI primary, Gemini fallback)
    ai_data = call_ai_multi_scene_parse_family(raw_text)
    if ai_data and ai_data.get("scenes"):
        return format_family_multi_scene_prompts(ai_data, wardrobe=wardrobe)

    # 2. Offline Fallback: Partition user lines into 2 lines per scene
    clean = raw_text.strip()
    raw_lines = [line.strip() for line in clean.splitlines() if line.strip()]

    extracted = []
    for line in raw_lines:
        m = re.match(r'^(beta|ammi|abbu|boy|girl|دوست|بندہ|مہمان)\s*[:：\-]\s*(.*)$', line, flags=re.IGNORECASE)
        if m:
            speaker_tag = m.group(1).capitalize()
            content = m.group(2).strip()
            extracted.append((speaker_tag, content))
        else:
            extracted.append(("Beta" if len(extracted) % 2 == 0 else "Ammi", line))

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
        "title": "Pakistani Comedy Jugat",
        "location": "Living Room Sofa",
        "prop": "Hand prop",
        "scenes": fallback_scenes
    }
    return format_family_multi_scene_prompts(fallback_data, wardrobe=wardrobe)
