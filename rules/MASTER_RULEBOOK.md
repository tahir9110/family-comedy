# MASTER SITCOM RULEBOOK (v4.0 - BULBULAY & NADANIYAAN EDITION)

### 1. COMEDIC PERSONAS & ARCHETYPES (PAKISTANI SITCOM DNA):
- **@Abbu (Mehmood Sahab / Yasir Style):** Sarcastic, dry, practical, deadpan delivery, questioning @Beta's intelligence with witty one-liners.
- **@Ammi (Momo / Rahat Style):** Innocently cheerful, delightfully clueless, delivers savage burns with an affectionate smile (iconic tropes like forgetting names, sweet roasts).
- **@Beta (Nabeel / Danish Style):** Always referred to as "their 25-year-old grown adult son @Beta". Over-dramatic, thinks he is a Bollywood superstar/billionaire, whines passionately when roasted.

### 2. YOUTUBE ANTI-TEMPLATE & MONETIZATION SAFETY:
- To prevent YouTube "Inauthentic / Repetitive Content" demonetization, EVERY episode must rotate:
  * **Locations:** Rotate between Dining Table, Lounge, Kitchen, Courtyard/Sehan, Porch/Car, Rooftop/Chhat.
  * **Postures & Staging:** Vary sitting vs. standing (e.g., all 3 sitting at the table; @Abbu standing while @Beta sits; all 3 standing in the kitchen).
  * **First Speaker & Story Prop:** Alternate who speaks first and always include a visual story prop (e.g., electricity bill, tea cup, phone, car keys).

### 3. GOOGLE FLOW WORKFLOW (THE HYBRID PRODUCER PROTOCOL):
- **SCENE 1 (Reference-to-Video / R2V):** 
  * AI automatically drafts and submits Scene 1 via `flow-text-to-video` using character tags `@Abbu`, `@Ammi`, and `@Beta` and authentic Urdu script.
  * AI monitors and downloads Clip 1 to `output/episode_X_clip1.mp4`.
  * AI automatically extracts the exact last frame to `temp/episode_X_last_frame.png`.
- **SCENE 2 (I2V / Continuation - The One-Click Hand-off):**
  * *No @ Tags Rule:* Google Flow automatically disables @ tags when a frame is attached. NEVER use "@" tags in Scene 2.
  * *Handoff:* AI prepares the exact starting frame `temp/episode_X_last_frame.png` and drafts the Scene 2 continuation prompt (authentic Urdu script, prop lock, anti-smile rule).
  * *Human Producer Action:* The user does a single click on the Submit arrow `->` (or hits Enter) in Flow to trigger Scene 2 cleanly without automation stalling.
- **POST-PRODUCTION & STITCHING:**
  * As soon as Clip 2 downloads, AI takes back over automatically:
  * Copies Clip 2 to `output/episode_X_clip2.mp4`.
  * Runs FFmpeg `stitch_and_polish` with audio normalization into `output/episode_X_final.mp4`.
  * Logs the completed episode into `data/history_ledger.json`.

### 4. VISUAL-TO-SCRIPT LOGIC, PROP LOCK & EMOTION LOCK:
- **Spatial Position Lock (Left, Center, Right):** To prevent characters from swapping left-and-right sides midway through a clip or jumping across the frame, explicitly declare their exact screen staging: `@Beta on screen-LEFT, @Ammi in the CENTER, and @Abbu on screen-RIGHT (All characters stay locked in these positions without crossing over or switching sides).`
- **Static Tripod Camera Lock:** Omni Flash will cut across the 180-degree axis to focus on the speaker unless explicitly prevented. Always include: `"Static tripod camera shot: Keep a fixed, stationary medium-wide shot with NO camera angle switching, NO reverse-shot cuts, NO camera flips, and NO close-ups."`
- **Eyeline Lock & No Fourth Wall Break:** Characters must **NEVER** look directly into the camera lens like vloggers or presenters. When speaking or reacting, they must turn their heads and look directly at each other in profile or three-quarter view (e.g., `@Beta turns his head to look directly at @Abbu while speaking (never looking at the camera)`).
- **Physical Prop Lock:** Never allow characters to magically drop, lose, or duplicate props between seconds (e.g., "He keeps holding the smartphone firmly in both hands throughout the clip and does NOT drop it").
- Never write jokes that contradict locked clothing or physical actions on screen.
- **Anti-Smile Rule:** In Scene 1 & 2, explicitly instruct: "(do NOT make @Beta smile at the end of the clip)" — the roasted character must maintain an annoyed, offended, whiny desi pout while the parents smile.

### 5. AUDIO & THE STRICT "8 + 6" FORMULA WITH REAL URDU SCRIPT:
- **Real Urdu Script (Phonetic Accuracy):** To prevent robotic or wrong Roman Urdu pronunciations (e.g., mispronouncing 'ulta', 'chal', 'q'), ALWAYS write spoken dialogue in **authentic Urdu script** followed by the transliteration:
  * Example: `At 0:00, Abbu speaks in Urdu: میرا واٹس ایپ ویڈیو کیوں نہیں چل رہا؟ (Mera WhatsApp video kiyun nahi chal raha?)`
  * Example: `At 0:04, Ammi replies in Urdu: کیونکہ فون الٹا پکڑا ہے! (Kiyunke phone ulta pakra hai!)`
- Pacing Prompt: "Natural, expressive Pakistani sitcom comedy delivery in the style of Bulbulay. Each character speaks their line once cleanly."
- Word Count per 8-second clip (2 speakers):
  * Speaker 1: 7 to 9 words max.
  * Speaker 2 (after the 0:04 switch): MUST BE A TIGHT 4 TO 6 WORD PUNCHLINE.
  (Never exceed this limit so the audio never loops, stutters, or eats words).

### 6. VIRAL STAGE DRAMA JUGATS & ANTI-SILENCE RULES:
- **Pakistani Stage Drama & Jugat Culture:** Move away from dry or tame jokes. Use iconic, viral stage drama and sitcom roast traditions (inspired by Amanullah, Sohail Ahmed, Shakeel Siddiqui, Naseem Vicky, and Bulbulay).
- **Anti-Silence & Zero Dead Air:** Never leave awkward gaps or silence between lines. Speaker 1 speaks from 0:00 to 0:03; Speaker 2 cuts in instantly at 0:03 with no pause, delivering rapid-fire punchlines with expressive laughter/roasting. Always include:
  `"Fast-paced Pakistani stage drama comedic timing with rapid witty banter and ZERO dead silence between dialogues. Dialogue delivery flows back-to-back immediately."`
- **Celebrity / Prominent Person Policy Guard:** Google Flow strictly blocks prompts containing real living public figures (e.g., "Fawad Khan", "Babar Azam"). ALWAYS use generic archetypes: *"filmi hero"*, *"superstar"*, *"cricket captain"*, *"celebrity model"*.


