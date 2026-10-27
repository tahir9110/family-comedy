// State
let currentEpisodeId = 1;
let currentTitle = "";
let currentLocation = "";
let currentProp = "";
let couplePresets = [];
let wardrobesList = [];
let currentWardrobeId = null;
let currentActiveJokeId = null;
let currentScenesList = [];
let currentLastFramePath = "";

document.addEventListener("DOMContentLoaded", () => {
  initStudio();
  setupDropzones();
});

async function initStudio() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    
    currentEpisodeId = data.next_episode_id;
    couplePresets = data.couple_presets || [];
    wardrobesList = data.wardrobes || [];

    // Update Header Badges
    document.getElementById("badge-current-ep").textContent = `EPISODE ${currentEpisodeId}`;
    document.getElementById("badge-total-eps").textContent = `${data.history.length} Done`;
    document.getElementById("count-history").textContent = data.history.length;

    // Render Wardrobe Pills
    renderWardrobePills(wardrobesList);

    // Render 1-Click Couple Presets Grid
    renderCouplePresetsGrid(couplePresets);

    // Render History Ledger
    renderHistory(data.history);

    // Select the first joke automatically on load (e.g. Court Bhaga Kar)
    if (couplePresets.length > 0) {
      selectViralJoke(couplePresets[0].id);
    }
  } catch (err) {
    showToast("Error connecting to Larka & Larki Studio backend: " + err.message);
  }
}

function renderWardrobePills(wardrobes) {
  const container = document.getElementById("wardrobe-pills-container");
  container.innerHTML = "";

  // Auto-Rotate Pill
  const autoPill = document.createElement("button");
  autoPill.className = "wardrobe-pill active";
  autoPill.id = "wardrobe-pill-auto";
  autoPill.textContent = "🎲 Auto-Rotate (Fresh Every Episode)";
  autoPill.onclick = () => selectWardrobe(null);
  container.appendChild(autoPill);

  wardrobes.forEach(w => {
    const pill = document.createElement("button");
    pill.className = "wardrobe-pill";
    pill.id = `wardrobe-pill-${w.id}`;
    pill.textContent = `👔 ${w.name}`;
    pill.onclick = () => selectWardrobe(w.id);
    container.appendChild(pill);
  });
}

function selectWardrobe(wardrobeId) {
  currentWardrobeId = wardrobeId;
  document.querySelectorAll(".wardrobe-pill").forEach(p => p.classList.remove("active"));
  const activePill = document.getElementById(wardrobeId ? `wardrobe-pill-${wardrobeId}` : "wardrobe-pill-auto");
  if (activePill) activePill.classList.add("active");

  if (currentActiveJokeId) {
    selectViralJoke(currentActiveJokeId);
  } else {
    const rawVal = document.getElementById("smart-raw-input").value.trim();
    if (rawVal) {
      handleSmartParse();
    }
  }
}

function renderCouplePresetsGrid(presets) {
  const container = document.getElementById("couple-presets-container");
  container.innerHTML = "";
  
  presets.forEach((j, index) => {
    const btn = document.createElement("button");
    btn.className = `viral-joke-btn ${index === 0 ? 'active' : ''}`;
    btn.id = `joke-btn-${j.id}`;
    btn.onclick = () => selectViralJoke(j.id);
    btn.innerHTML = `
      <div class="viral-joke-title">${j.title}</div>
      <div class="viral-joke-sub">📍 ${j.location} • 📦 ${j.prop}</div>
    `;
    container.appendChild(btn);
  });
}

async function selectViralJoke(jokeId) {
  currentActiveJokeId = jokeId;
  document.querySelectorAll(".viral-joke-btn").forEach(b => b.classList.remove("active"));
  const activeBtn = document.getElementById(`joke-btn-${jokeId}`);
  if (activeBtn) activeBtn.classList.add("active");

  try {
    let url = `/api/select-viral-joke?joke_id=${encodeURIComponent(jokeId)}`;
    if (currentWardrobeId) {
      url += `&wardrobe_id=${encodeURIComponent(currentWardrobeId)}`;
    }
    const res = await fetch(url, { method: "POST" });
    if (!res.ok) throw new Error("Failed to load preset joke");
    const data = await res.json();
    applyMultiSceneData(data);
    showToast(`Loaded preset: ${data.title}`);
  } catch (err) {
    showToast("Error loading preset: " + err.message);
  }
}

async function handleSmartParse() {
  const rawText = document.getElementById("smart-raw-input").value.trim();
  if (!rawText) {
    showToast("Please paste a script or dialogue first!");
    return;
  }

  // Deactivate preset buttons
  currentActiveJokeId = null;
  document.querySelectorAll(".viral-joke-btn").forEach(b => b.classList.remove("active"));

  showToast("⏳ AI Analyzing & Pacing Dialogue into Scenes...");

  try {
    let url = "/api/smart-parse";
    if (currentWardrobeId) {
      url += `?wardrobe_id=${encodeURIComponent(currentWardrobeId)}`;
    }
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ raw_text: rawText })
    });
    if (!res.ok) throw new Error("Smart parse failed");
    const data = await res.json();

    applyMultiSceneData(data);
    showToast(`✨ Generated ${currentScenesList.length} Scenes without rushing dialogue!`);
  } catch (err) {
    showToast("Error parsing script: " + err.message);
  }
}

function applyMultiSceneData(data) {
  currentTitle = data.title;
  currentLocation = data.location;
  currentProp = data.prop;

  // Extract scenes array
  if (data.scenes && Array.isArray(data.scenes) && data.scenes.length > 0) {
    currentScenesList = data.scenes;
  } else {
    currentScenesList = [
      {
        scene_num: 1,
        title: "Scene 1 Prompt (Initial T2V with @Tags)",
        prompt: data.scene1_prompt || ""
      },
      {
        scene_num: 2,
        title: "Scene 2 Prompt (Part 2 Continuation • ZERO @Tags)",
        prompt: data.scene2_prompt || ""
      }
    ];
  }

  // Update Metadata Badges safely
  const metaTitle = document.getElementById("meta-title");
  if (metaTitle) metaTitle.textContent = `🎬 ${currentTitle}`;
  const metaLoc = document.getElementById("meta-location");
  if (metaLoc) metaLoc.textContent = `📍 ${currentLocation}`;
  const metaProp = document.getElementById("meta-prop");
  if (metaProp) metaProp.textContent = `📦 ${currentProp}`;
  const scenesBadge = document.getElementById("meta-scenes-count");
  if (scenesBadge) {
    scenesBadge.textContent = `🎞️ ${currentScenesList.length} Scenes Planned`;
  }

  // Render Dynamic Scene Cards in Step 1
  renderDynamicSceneCards(currentScenesList);

  // Safely update Step 1 & Step 2 prompt textboxes if present in DOM
  const s1Box = document.getElementById("prompt-s1-text");
  if (s1Box && currentScenesList.length > 0) {
    s1Box.value = currentScenesList[0].prompt;
  }
  const s2Box = document.getElementById("prompt-s2-text");
  if (s2Box && currentScenesList.length > 1) {
    s2Box.value = currentScenesList[1].prompt;
  }
}

function renderDynamicSceneCards(scenes) {
  const container = document.getElementById("dynamic-prompts-container");
  if (!container) return;
  container.innerHTML = "";

  scenes.forEach(sc => {
    const isT2V = sc.scene_num === 1;
    const card = document.createElement("div");
    card.className = "prompt-output-box mt-3";
    card.id = `prompt-card-scene-${sc.scene_num}`;

    card.innerHTML = `
      <div class="prompt-header">
        <span class="prompt-title">🎬 Scene ${sc.scene_num} Prompt (${isT2V ? 'Initial T2V with @Tags' : `Part ${sc.scene_num} Continuation • ZERO @Tags`})</span>
        <button class="btn btn-sm btn-accent" onclick="copyScenePrompt(${sc.scene_num})">📋 Copy Scene ${sc.scene_num} Prompt</button>
      </div>
      <textarea id="prompt-text-scene-${sc.scene_num}" class="studio-textarea" readonly rows="5">${sc.prompt}</textarea>
      <div class="prompt-hint">${isT2V ? '💡 In Flow: Attach character references (@Larka & @Larki). Generate Clip 1.' : `💡 In Flow: Upload Clip ${sc.scene_num - 1}'s extracted last frame, paste this prompt, and hit Enter.`}</div>
    `;

    container.appendChild(card);
  });
}

function copyScenePrompt(sceneNum) {
  const sc = currentScenesList.find(s => s.scene_num === sceneNum);
  if (!sc || !sc.prompt) {
    showToast(`Scene ${sceneNum} prompt not found!`);
    return;
  }
  navigator.clipboard.writeText(sc.prompt).then(() => {
    showToast(`Copied Scene ${sceneNum} Prompt to Clipboard!`);
  }).catch(() => {
    showToast("Failed to copy automatically. Please select text and copy manually.");
  });
}

function copyPrompt(sceneType) {
  const idx = sceneType === 'scene1' ? 0 : 1;
  if (currentScenesList[idx]) {
    copyScenePrompt(currentScenesList[idx].scene_num);
  }
}

function copyFramePath() {
  if (!currentLastFramePath) {
    showToast("No frame extracted yet!");
    return;
  }
  navigator.clipboard.writeText(currentLastFramePath).then(() => {
    showToast("Image path copied to clipboard!");
  }).catch(() => {
    showToast("Failed to copy image path.");
  });
}

function setupDropzones() {
  ['clip1', 'clip2'].forEach(key => {
    const dropzone = document.getElementById(`dropzone-${key}`);
    const input = document.getElementById(`file-${key}`);
    if (!dropzone || !input) return;

    dropzone.addEventListener("click", () => input.click());

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
      });
    });

    dropzone.addEventListener("drop", (e) => {
      const files = e.dataTransfer.files;
      if (files.length > 0 && files[0].type.includes("mp4")) {
        input.files = files;
        handleFileSelect(key);
      } else {
        showToast("Please drop an MP4 video file.");
      }
    });
  });
}

async function handleFileSelect(type) {
  const input = document.getElementById(`file-${type}`);
  if (!input || !input.files || input.files.length === 0) return;

  const file = input.files[0];
  const filenameEl = document.getElementById(`filename-${type}`);
  if (filenameEl) filenameEl.textContent = file.name;

  const clipNum = type === 'clip1' ? 1 : 2;
  const formData = new FormData();
  formData.append("episode_id", currentEpisodeId);
  formData.append("clip_num", clipNum);
  formData.append("file", file);

  showToast(`Uploading and processing Clip ${clipNum}...`);

  try {
    const res = await fetch("/api/import-clip", {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Upload failed");

    currentLastFramePath = data.frame_path;
    const imgEl = document.getElementById("img-last-frame");
    if (imgEl) imgEl.src = data.frame_url;
    const pathEl = document.getElementById("text-frame-path");
    if (pathEl) pathEl.textContent = data.frame_path;
    const frameBox = document.getElementById("extracted-frame-box");
    if (frameBox) frameBox.classList.remove("hidden");

    // Suggest next scene prompt
    const nextSceneNum = clipNum + 1;
    const nextSc = currentScenesList.find(s => s.scene_num === nextSceneNum);
    if (nextSc) {
      const s2Box = document.getElementById("prompt-s2-text");
      if (s2Box) s2Box.value = nextSc.prompt;
    }

    showToast(`✅ Clip ${clipNum} imported & last frame extracted!`);
  } catch (err) {
    showToast("Error processing video: " + err.message);
  }
}

async function autoDetectClip(clipNum) {
  showToast("Scanning Downloads folder for latest MP4...");
  try {
    const res = await fetch("/api/detect-download");
    const data = await res.json();
    const downloads = data.downloads || [];

    if (downloads.length === 0) {
      showToast("No MP4 files found in Downloads folder.");
      return;
    }

    const latest = downloads[0];
    const infoBox = document.getElementById(`detect-info-clip${clipNum}`);
    if (infoBox) {
      infoBox.innerHTML = `Found: <strong>${latest.name}</strong> (${latest.size_mb} MB) - ${latest.time_str}`;
    }

    const formData = new FormData();
    formData.append("episode_id", currentEpisodeId);
    formData.append("clip_num", clipNum);
    formData.append("file_path", latest.path);

    showToast(`Importing latest video as Clip ${clipNum}...`);

    const importRes = await fetch("/api/import-clip", {
      method: "POST",
      body: formData
    });
    const importData = await importRes.json();
    if (!importRes.ok) throw new Error(importData.detail || "Import failed");

    const filenameEl = document.getElementById(`filename-clip${clipNum}`);
    if (filenameEl) filenameEl.textContent = latest.name;

    currentLastFramePath = importData.frame_path;
    const imgEl = document.getElementById("img-last-frame");
    if (imgEl) imgEl.src = importData.frame_url;
    const pathEl = document.getElementById("text-frame-path");
    if (pathEl) pathEl.textContent = importData.frame_path;
    const frameBox = document.getElementById("extracted-frame-box");
    if (frameBox) frameBox.classList.remove("hidden");

    // Suggest next scene prompt
    const nextSceneNum = clipNum + 1;
    const nextSc = currentScenesList.find(s => s.scene_num === nextSceneNum);
    if (nextSc) {
      const s2Box = document.getElementById("prompt-s2-text");
      if (s2Box) s2Box.value = nextSc.prompt;
    }

    showToast(`✅ Clip ${clipNum} auto-imported & frame extracted!`);
  } catch (err) {
    showToast("Auto-detect error: " + err.message);
  }
}

async function runMasterStitch() {
  const btn = document.getElementById("btn-stitch");
  btn.disabled = true;
  btn.textContent = "⏳ STITCHING & POLISHING EPISODE...";

  try {
    const res = await fetch("/api/stitch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        episode_id: currentEpisodeId,
        title: currentTitle,
        location: currentLocation,
        prop: currentProp,
        first_speaker: "@Larka"
      })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Stitch failed");

    // Show final player
    const playerBox = document.getElementById("final-video-container");
    const player = document.getElementById("player-final-video");
    const downloadLink = document.getElementById("link-download-final");

    player.src = data.final_url;
    downloadLink.href = data.final_url;
    downloadLink.setAttribute("download", `larka_larki_episode_${currentEpisodeId}_final.mp4`);
    playerBox.classList.remove("hidden");

    // Refresh history
    renderHistory(data.history);
    document.getElementById("badge-total-eps").textContent = `${data.history.length} Done`;
    document.getElementById("count-history").textContent = data.history.length;

    showToast(`🎉 Episode ${currentEpisodeId} (${data.scenes_stitched || 2} scenes) stitched and saved to ledger!`);
  } catch (err) {
    showToast("Stitch error: " + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "🎬 STITCH MASTER EPISODE & UPDATE LEDGER";
  }
}

function renderHistory(history) {
  const list = document.getElementById("history-list");
  list.innerHTML = "";

  if (!history || history.length === 0) {
    list.innerHTML = `<div class="history-empty">No episodes completed yet. Episode 1 is queued and ready!</div>`;
    return;
  }

  history.slice().reverse().forEach(ep => {
    const card = document.createElement("div");
    card.className = "history-card";
    card.innerHTML = `
      <div class="history-card-header">
        <span class="history-card-ep">EP ${ep.episode_id}</span>
        <span class="history-card-date">${ep.date || 'Completed'}</span>
      </div>
      <div class="history-card-title">${ep.title}</div>
      <div class="history-card-meta">
        <span>📍 ${ep.location}</span>
        <span>📦 ${ep.main_prop || ep.prop}</span>
        ${ep.scenes_count ? `<span>🎞️ ${ep.scenes_count} scenes</span>` : ''}
      </div>
    `;
    list.appendChild(card);
  });
}

function showToast(message) {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("fade-out");
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
