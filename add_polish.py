with open('build_3d_index.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Offline Earnings Modal in HTML
old_modal = '''<!-- Daily Chest Modal -->'''
new_modal = '''<!-- Welcome Back / Offline Earnings Modal -->
<div class="modal-overlay" id="modal-welcome">
    <div class="modal-card" style="text-align: center;">
        <div style="font-size: 46px; margin-bottom: 8px;">🎉</div>
        <div class="modal-title" style="justify-content: center;">Welcome Back, Tycoon!</div>
        <p style="font-size: 14px; color: var(--text-sub); margin: 6px 0 12px;">
            While you were away, your mill kept processing lumber!
        </p>
        <div style="font-size: 30px; font-weight: 900; color: #10b981; margin-bottom: 16px;">
            +💵 <span id="offline-earned-val">0</span>
        </div>
        <button class="btn-full btn-primary" id="btn-claim-offline">Collect Cash</button>
    </div>
</div>

<!-- Daily Chest Modal -->'''
text = text.replace(old_modal, new_modal)

# 2. Add Chiptune Music to SoundEngine
old_sound_engine = '''    init() {
        if (this.ctx) return;
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        this.ctx = new AudioCtx();
        this.sfxGain = this.ctx.createGain();
        this.sfxGain.gain.value = 0.35;
        this.sfxGain.connect(this.ctx.destination);
    }'''

new_sound_engine = '''    init() {
        if (this.ctx) return;
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        this.ctx = new AudioCtx();
        this.sfxGain = this.ctx.createGain();
        this.sfxGain.gain.value = 0.35;
        this.sfxGain.connect(this.ctx.destination);

        this.musicGain = this.ctx.createGain();
        this.musicGain.gain.value = 0.07;
        this.musicGain.connect(this.ctx.destination);
        this.nextNoteTime = 0;
        this.noteIndex = 0;
        this.isPlayingMusic = false;
        this.melody = [
            261.63, 329.63, 392.00, 523.25, 392.00, 329.63,
            293.66, 349.23, 440.00, 523.25, 440.00, 349.23,
            329.63, 392.00, 523.25, 659.25, 523.25, 392.00,
            293.66, 392.00, 493.88, 587.33, 493.88, 392.00
        ];
        if (this.musicEnabled) this.startMusic();
    }

    startMusic() {
        if (!this.ctx || this.isPlayingMusic) return;
        this.isPlayingMusic = true;
        this.nextNoteTime = this.ctx.currentTime + 0.1;
        this.scheduleMusic();
    }

    scheduleMusic() {
        if (!this.isPlayingMusic || !this.musicEnabled || !this.ctx) return;
        while (this.nextNoteTime < this.ctx.currentTime + 0.5) {
            const freq = this.melody[this.noteIndex % this.melody.length];
            this.playChiptuneNote(freq, this.nextNoteTime, 0.18);
            this.nextNoteTime += 0.22;
            this.noteIndex++;
        }
        setTimeout(() => this.scheduleMusic(), 150);
    }

    playChiptuneNote(freq, time, dur) {
        if (!this.ctx || !this.musicEnabled) return;
        try {
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            osc.type = "triangle";
            osc.frequency.setValueAtTime(freq, time);
            g.gain.setValueAtTime(0.06, time);
            g.gain.exponentialRampToValueAtTime(0.001, time + dur);
            osc.connect(g);
            g.connect(this.musicGain);
            osc.start(time);
            osc.stop(time + dur);
        } catch(e) {}
    }'''
text = text.replace(old_sound_engine, new_sound_engine)

# 3. Add Smooth Camera Drag / Orbit Controls
old_canvas_events = '''    window.addEventListener("resize", onWindowResize);
    canvas.addEventListener("click", onCanvas3DClick);'''

new_canvas_events = '''    window.addEventListener("resize", onWindowResize);
    setup3DCameraControls(canvas);
    canvas.addEventListener("click", onCanvas3DClick);'''
text = text.replace(old_canvas_events, new_canvas_events)

old_resize_fn = '''function onWindowResize() {'''
new_camera_controls = '''let isDragging = false;
let hasDragged = false;
let previousPointerPos = { x: 0, y: 0 };
let cameraAngle = Math.PI / 4;
let cameraDistance = 38;
let cameraHeight = 28;

function updateCameraPos() {
    camera.position.x = Math.sin(cameraAngle) * cameraDistance;
    camera.position.z = Math.cos(cameraAngle) * cameraDistance;
    camera.position.y = cameraHeight;
    camera.lookAt(1, 1, 0);
}

function setup3DCameraControls(canvas) {
    updateCameraPos();

    window.addEventListener("wheel", (e) => {
        cameraDistance = Math.max(20, Math.min(55, cameraDistance + e.deltaY * 0.03));
        updateCameraPos();
    }, { passive: true });

    canvas.addEventListener("pointerdown", (e) => {
        isDragging = true;
        hasDragged = false;
        previousPointerPos = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener("pointermove", (e) => {
        if (!isDragging) return;
        const dx = e.clientX - previousPointerPos.x;
        const dy = e.clientY - previousPointerPos.y;
        previousPointerPos = { x: e.clientX, y: e.clientY };

        if (Math.abs(dx) > 2 || Math.abs(dy) > 2) {
            hasDragged = true;
            cameraAngle += dx * 0.008;
            cameraHeight = Math.max(16, Math.min(42, cameraHeight - dy * 0.08));
            updateCameraPos();
        }
    });

    window.addEventListener("pointerup", () => {
        isDragging = false;
    });
}

function onWindowResize() {'''
text = text.replace(old_resize_fn, new_camera_controls)

# Ignore raycast click if player was dragging the camera
old_click_handler = '''function onCanvas3DClick(e) {'''
new_click_handler = '''function onCanvas3DClick(e) {
    if (hasDragged) { hasDragged = false; return; }'''
text = text.replace(old_click_handler, new_click_handler)

# 4. Add Cargo Ship state & Sailing Animation
old_crane_block = '''    // 3. Yellow Gantry Crane Hoist
    const craneSpeedLv = gameState.upgrades.craneSpeed || 1;
    craneTimer += dt * (1 + craneSpeedLv * 0.22) * speedMult;'''

new_crane_block = '''    // 3. Yellow Gantry Crane Hoist & Cargo Ship Export
    const craneSpeedLv = gameState.upgrades.craneSpeed || 1;
    craneTimer += dt * (1 + craneSpeedLv * 0.22) * speedMult;

    if (cargoShipMesh) {
        if (!window.cargoShipState) {
            window.cargoShipState = "docked";
            window.cargoShipCargo = 0;
        }

        if (window.cargoShipState === "docked") {
            if (craneTimer >= 1.6) {
                craneTimer = 0;
                window.cargoShipCargo++;
                const screenP = toScreenXY(new THREE.Vector3(15.5, 2, 4));
                floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y, "🚢 Ship Loaded!", "#38bdf8", 14));
                if (window.cargoShipCargo >= 4) {
                    window.cargoShipState = "sailing";
                    audio.playSfx('honk');
                    showCelebratoryBanner("🚢 CARGO SHIP DEPARTING WITH BULK EXPORT!");
                }
            }
        } else if (window.cargoShipState === "sailing") {
            cargoShipMesh.position.z += 4.5 * dt * speedMult;
            if (cargoShipMesh.position.z > 24.0) {
                cargoShipMesh.position.z = -14.0;
                window.cargoShipState = "returning";
                const tier = WOOD_TIERS[gameState.woodTier];
                const bulkPayout = Math.round(350 * tier.value * (1 + (gameState.upgrades.woodValue || 0) * 0.2));
                gameState.coins += bulkPayout;
                gameState.totalEarned += bulkPayout;
                audio.playSfx('cash');
                const screenP = toScreenXY(new THREE.Vector3(15.5, 2, 10));
                floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y, `+💵 ${formatNumber(bulkPayout)} BULK EXPORT!`, "#38bdf8", 22));
            }
        } else if (window.cargoShipState === "returning") {
            cargoShipMesh.position.z += 4.5 * dt * speedMult;
            if (cargoShipMesh.position.z >= 4.0) {
                cargoShipMesh.position.z = 4.0;
                window.cargoShipCargo = 0;
                window.cargoShipState = "docked";
                showToast("🚢 Cargo Ship docked at the harbor pier!");
            }
        }
    }'''
text = text.replace(old_crane_block, new_crane_block)

# 5. Add Offline Earnings check in onGameStarted
old_on_started = '''function onGameStarted() {
    document.getElementById("badge-user").textContent = currentUser ? `👤 ${escapeHtml(currentUser.username)}` : "👤 Guest";
    initShopCards();'''

new_on_started = '''function onGameStarted() {
    document.getElementById("badge-user").textContent = currentUser ? `👤 ${escapeHtml(currentUser.username)}` : "👤 Guest";
    initShopCards();

    // Offline Earnings
    if (gameState.lastSaveTime) {
        const elapsedSec = Math.min(API_CONFIG.OFFLINE_MAX_HOURS * 3600, (Date.now() - gameState.lastSaveTime) / 1000);
        if (elapsedSec > 40) {
            const tier = WOOD_TIERS[gameState.woodTier];
            const offlineRate = Math.max(4, (gameState.stats.deliveries > 0 ? (gameState.totalEarned / Math.max(60, gameState.stats.playTime)) : 10) * 0.4);
            const earned = Math.round(elapsedSec * offlineRate);

            if (earned > 20) {
                document.getElementById("offline-earned-val").textContent = formatNumber(earned);
                openModal("modal-welcome");
                document.getElementById("btn-claim-offline").onclick = () => {
                    gameState.coins += earned;
                    gameState.totalEarned += earned;
                    closeModal("modal-welcome");
                    audio.playSfx('cash');
                };
            }
        }
    }'''
text = text.replace(old_on_started, new_on_started)

# 6. Add Music toggle in setupUI
old_toggle_sfx = '''    document.getElementById("toggle-sfx").onclick = (e) => {
        audio.sfxEnabled = !audio.sfxEnabled;
        gameState.settings.sfx = audio.sfxEnabled;
        e.target.textContent = `SFX: ${audio.sfxEnabled ? 'ON' : 'OFF'}`;
    };'''

new_toggle_sfx = '''    document.getElementById("toggle-sfx").onclick = (e) => {
        audio.sfxEnabled = !audio.sfxEnabled;
        gameState.settings.sfx = audio.sfxEnabled;
        e.target.textContent = `SFX: ${audio.sfxEnabled ? 'ON' : 'OFF'}`;
    };

    document.getElementById("toggle-music").onclick = (e) => {
        audio.musicEnabled = !audio.musicEnabled;
        gameState.settings.music = audio.musicEnabled;
        e.target.textContent = `Music: ${audio.musicEnabled ? 'ON' : 'OFF'}`;
        if (audio.musicEnabled) audio.startMusic();
    };'''
text = text.replace(old_toggle_sfx, new_toggle_sfx)

with open('build_3d_index.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("build_3d_index.py successfully patched with polish!")
