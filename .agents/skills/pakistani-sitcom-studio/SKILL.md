---
name: pakistani-sitcom-studio
description: Complete guide and workflow for automated script-to-video generation, Google Flow 10s constraints, narrative camera staging, Urdu phonetics, taboo prevention, and YouTube monetization for Pakistani sitcoms.
---

# Pakistani Sitcom Studio Workflow & Rules

This skill documents the end-to-end architecture, rules, and best practices established for generating Pakistani comedy sitcoms (Family Comedy & Larka Larki) using Google Flow, OpenAI GPT-5/4o, Gemini, and YouTube monetization standards.

---

## 1. Google Flow Architecture & Video Timing Budget

1. **Fixed Container Duration**:
   - Google Flow video clips are strictly **10.01 seconds** long.
   - It cannot dynamically generate a 4-second or 14-second clip.
2. **Timing Budget Rules**:
   - **Single-Scene Jokes (3–4 lines)**: ALWAYS generate as **1 clip (10 seconds)**. Do NOT split a short joke into two scenes, otherwise Flow drags out pauses or hallucinate filler dialogue.
   - **Two-Scene Sketches (5–8 lines)**: Exactly **2 clips (20 seconds)**.
   - **Three-Scene Mini-Sitcoms (9–12 lines)**: Exactly **3 clips (30 seconds)**.
   - **Hard Cap**: Keep short comedy sketches between **10 to 30 seconds** for optimal YouTube Shorts retention (100%+ APV).

---

## 2. Audio & Speech Safety Rules

1. **Short-Line Safety Expansion**:
   - Google Flow's TTS engine often experiences **speaker swaps** or cuts off audio when a character's dialogue is too short (1–2 words like "Kya?", "Achha?").
   - **MANDATORY**: Automatically expand short interjections into 4–5 word natural dialogue sentences without altering comedic punchlines.
   - *Example*: Expand `"Par kyun?"` ➔ `"ارے پر کیوں ابو؟ مجھے وجہ تو بتائیں!"`
2. **Urdu Phonetics & Diacritics**:
   - For English loan words, add proper Urdu diacritics and Roman Urdu in parentheses to avoid mispronunciations.
   - *Example*: `"ہیٹ ٹرک"` can be mispronounced as "Heat-trick". Use `"ہَیٹ ٹرِک (Hat-trick)"`.
   - *Example*: Spell `"جورو کا غلام"` strictly with Perso-Arabic Urdu to ensure correct enunciation.

---

## 3. Camera Staging & Visual Positioning

1. **Side-Profile Two-Shot in 3/4 Angle (Both Faces Visible)**:
   - Always enforce: `Side-profile two-shot in 3/4 angle: The camera captures both characters from an angled profile perspective so BOTH characters' full faces, eyes, and mouth expressions are clearly visible to the camera simultaneously. NEITHER character has their back turned to the camera. Both faces are in clear view throughout the entire clip as they converse.`
   - This ensures both characters emote clearly and allows seamless post-production punch-in zooms in CapCut/Premiere without showing a character's back.
2. **Fixed Perspective & Optics**:
   - Always enforce: `Camera & Optics: Shot on 50mm prime cinematic lens with natural shallow depth of field, softly blurred background. Fixed eye-level medium-wide shot with smooth stable framing, no jittery camera motion, no cuts, no reverse angles.`
   - Lighting: `Lighting & Atmosphere: Soft natural directional lighting with gentle ambient shadows, warm cinematic color grade.`
3. **Spatial Anchors**:
   - **Family Comedy**: `@Beta` screen-LEFT, `@Ammi` CENTER, `@Abbu` screen-RIGHT.
   - **Larka Larki**: `@Larka` screen-LEFT, `@Larki` screen-RIGHT.
   - **Workplace**: `@Beta` screen-LEFT (employee), `@Boss` screen-RIGHT (authority).
4. **Over-The-Shoulder / Rear Views**:
   - When a character speaks looking away from the camera (e.g. Ammi calling upstairs from the staircase):
   - Always include: `Over-the-shoulder rear shot / back view from behind @Ammi. STRICT BODY LOCK: @Ammi stays facing up the stairs with back to the camera throughout the entire clip without turning around.`
4. **Multi-Scene Motion Continuation**:
   - If a character starts moving (e.g. coming down the stairs), Scene 2 must explicitly describe the character walking down step-by-step.
5. **Facial Emotion Lock**:
   - Prevent characters from ruining the joke setup:
   - *Example*: `@Beta must NOT smile or laugh at the punchline; @Beta keeps a crestfallen, offended, or shocked reaction throughout. Only @Abbu chuckles or smiles.`

---

## 4. Strict Safety & Taboo Prevention (Pakistan Context)

- **CRITICAL ZERO TOLERANCE**:
  - Never allow Arabic text, Quranic verses, calligraphy wall frames, or gibberish scripts on walls.
  - *Hardcoded Prompt Constraint*:
    `Interior decor constraint: Plain clean walls with modern simple abstract art or landscape painting only. Absolutely NO Arabic script, NO calligraphy wall frames, NO religious verses, and NO text on walls or banners.`
- **Content Sensitivity**:
  - Frame comedy banters cleanly (e.g. `lighthearted family comedy banter`) to prevent AI safety filters from misunderstanding playful words like "joru ka ghulam" or "awara".

---

## 5. Dual-Engine Generation Architecture

Both web studios implement dual-engine failover:
1. **Primary Engine**: OpenAI `gpt-5` / `gpt-4o` (reads user's free 1M tier key from `openai key.txt`). Uses a 50s timeout for complex JSON reasoning.
2. **Fallback Engine**: Google Gemini (`gemini-2.5-flash` / `gemini-1.5-pro` from `aistuio free key.txt`).

---

## 6. YouTube Monetization & Safe Upload Standards

To guarantee 100% safe monetization without "Reused Content" or AI strikes:
1. **Human Editorial Value**:
   - Always add animated Urdu subtitles in CapCut/Premiere (yellow/red/white pop fonts).
   - Add comedic sound effects (laugh track, whoosh, cartoon boing) on punchlines.
2. **Channel Watermark**:
   - Place `channel_logo.jpg` as an official watermark in the corner of all videos.
3. **Altered or Synthetic Content**:
   - Always select **YES** during upload when YouTube asks if the video contains altered or synthetic content.
4. **Episode Tagging & Description**:
   - Title format: `[Joke Title] 😂 | Ep [XX] #Shorts #Comedy`
   - Description must contain the official credit line:
     `• Original Pakistani Family Sitcom. Script & Direction by Our Channel.`
