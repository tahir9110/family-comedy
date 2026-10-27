# 🎭 Pakistani Family Sitcom Studio

Automated AI-assisted script-to-video workflow and prompt generation studio for Pakistani comedy sitcoms (inspired by classic shows like *Bulbulay*, *Nadaaniyaan*, etc.), built for **Google Flow**, **OpenAI GPT-5/4o**, and **Gemini**.

---

## 🌟 Key Features

1. **Dual Web Studios**:
   - **Family Comedy Studio** (`http://localhost:8055`): Starring `@Abbu`, `@Ammi`, and `@Beta`.
   - **Larka Larki Studio** (`http://localhost:8001`): Starring `@Larka` and `@Larki`.
2. **Google Flow Timing & Scene Management**:
   - Fixed 10.01-second clip budgeting (1 clip for 3-4 line jokes, 2 clips for 2 scenes, 3 clips max).
   - Prevents dialogue drag and hallucinated pauses.
3. **Short-Line Safety Expansion**:
   - Automatically expands 1-2 word lines (e.g. "Kya?", "Kyun?") into 4-5 word complete natural sentences to prevent Google Flow TTS speaker-swapping glitches.
4. **Narrative Camera Staging & Body Lock**:
   - Enforces stationary camera, no cuts, no reverse angles.
   - Spatial character consistency across scenes.
   - Strict `BODY LOCK` on rear/over-the-shoulder perspectives.
5. **Cultural Safety & Taboo Elimination**:
   - Hardcoded negative prompts ensuring plain modern walls with **zero Arabic calligraphy, verses, or wall banners**.
6. **Dual AI Engine**:
   - Primary: OpenAI `gpt-5` / `gpt-4o` (with 50s timeout handling).
   - Fallback: Google Gemini (`gemini-2.5-flash` / `gemini-1.5-pro`).
7. **Production & YouTube Monetization Guidelines**:
   - Includes high-resolution Urdu infographic poster for video editors.
   - Channel logo (1:1) and wide banner (16:9) branding assets in `output/branding/`.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- Dependencies: `pip install fastapi uvicorn pillow arabic-reshaper python-bidi google-genai openai requests`

### 2. Run Studios
Double-click `start_studio.bat` or run:
```bash
# Terminal 1 - Family Comedy Studio (Port 8055)
python -m uvicorn studio.server:app --host 127.0.0.1 --port 8055 --reload

# Terminal 2 - Larka Larki Studio (Port 8001)
python -m larka_larki.studio.server
```

---

## 📁 Repository Structure
```text
├── .agents/
│   └── skills/
│       └── pakistani-sitcom-studio/SKILL.md
├── AGENTS.md
├── generate_rules_card.py
├── output/
│   ├── branding/
│   │   ├── channel_logo.jpg
│   │   └── channel_banner_cover.jpg
│   └── youtube_monetization_rules_urdu.png
├── studio/
│   ├── generator.py
│   ├── server.py
│   └── ...
├── larka_larki/
│   └── studio/
└── README.md
```

---

## 📜 License
MIT License. Created by Tahir & Team.
