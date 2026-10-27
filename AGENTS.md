# Pakistani Family Sitcom Studio - Project Instructions & Guidelines

This repository contains the full automated production pipeline for Pakistani comedy sitcoms (Family Comedy & Larka Larki) designed for Google Flow, OpenAI GPT-5/4o, Gemini, and YouTube Shorts monetization.

---

## 🚀 Studios & Servers
- **Family Comedy Studio**: `http://localhost:8000/` (Characters: `@Abbu`, `@Ammi`, `@Beta`)
  - Server file: [studio/server.py](file:///d:/Family%20Comedy/studio/server.py)
  - Generator logic: [studio/generator.py](file:///d:/Family%20Comedy/studio/generator.py)
- **Larka Larki Studio**: `http://localhost:8001/` (Characters: `@Larka`, `@Larki`)
  - Server file: `d:\Family Comedy\larka_larki\studio\server.py`
  - Generator logic: `d:\Family Comedy\larka_larki\studio\generator.py`

---

## ⚡ Google Flow Rules
- **Container Duration**: Fixed 10.01 seconds.
- **Duration Budget**: Short 3-4 line jokes MUST be kept to **1 clip (10 seconds)**.
- **Short-Line Safety Expansion**: Expand 1-2 word lines (e.g. "Par kyun?") to 4-5 words (e.g. "ارے پر کیوں ابو؟ مجھے وجہ تو بتائیں!") to prevent Google Flow TTS speaker-swapping bugs.
- **Negative Constraint (Safety)**: Plain walls only. **Absolutely NO Arabic script, NO calligraphy wall frames, NO religious verses on walls.**
- **Camera Staging**: Fixed medium-wide, stationary, no cuts, no reverse angles. Use `Over-the-shoulder rear shot / back view` with strict `BODY LOCK` when looking away from camera.
- **Facial Emotion Lock**: Keep punchline recipient shocked/offended, do NOT let them laugh at their own insult.

---

## 🛡️ Dual AI Engine
- **Primary**: OpenAI `gpt-5` / `gpt-4o` via `openai key.txt` (50s timeout).
- **Silent Fallback**: Gemini (`gemini-2.5-flash` / `gemini-1.5-pro`) via `aistuio free key.txt`.

---

## 📺 YouTube Monetization & Branding Assets
- **Channel Logo**: [output/branding/channel_logo.jpg](file:///d:/Family%20Comedy/output/branding/channel_logo.jpg)
- **Channel Banner (16:9)**: [output/branding/channel_banner_cover.jpg](file:///d:/Family%20Comedy/output/branding/channel_banner_cover.jpg)
- **Urdu Monetization Poster**: [output/youtube_monetization_rules_urdu.png](file:///d:/Family%20Comedy/output/youtube_monetization_rules_urdu.png)
- **Altered or Synthetic Content**: Always mark **YES** during upload.
- **Editing Standard**: Add animated Urdu subtitles, comic pop colors, sound effects, and watermark.
