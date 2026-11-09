# -*- coding: utf-8 -*-
JS_SIMULATION_LOOP = r'''
// ==========================================
// 5. SIMULATION & ANIMATION TICK LOOP
// ==========================================
let lastTime = performance.now();
let logSpawnTimer = 0;
let craneTimer = 0;
let cargoShipState = "docked";
let cargoShipCargo = 0;
let helicopterTimer = 0;
let saveTimer = 0;

function animate(time) {
    requestAnimationFrame(animate);
    const dt = Math.min(0.1, (time - lastTime) / 1000);
    lastTime = time;

    // Smooth Camera Transition (Cinematic Zone Glide)
    camera.position.lerp(targetCamPos, 0.08);
    currentLookAt.lerp(targetLookAt, 0.08);
    camera.lookAt(currentLookAt);

    // 1. Water Ripple Effect
    if (riverMesh) {
        riverMesh.position.y = 0.02 + Math.sin(time * 0.002) * 0.02;
    }

    // 2. Helicopter VIP Investor Routine
    if (helicopterMesh && helicopterMesh.userData.rotor) {
        helicopterMesh.userData.rotor.rotation.y += dt * 25;
        helicopterTimer += dt;
        if (helicopterTimer > 75) {
            helicopterTimer = 0;
            const vipBonus = Math.round(500 * (gameState.woodTier + 1) * 3);
            gameState.coins += vipBonus;
            gameState.totalEarned += vipBonus;
            audio.playSfx('fanfare');
            showToast(`🚁 VIP Billionaire landed at Helipad! +💵 ${formatNumber(vipBonus)}`);
            const screenP = toScreenXY(new THREE.Vector3(-26, 2, 22));
            floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y, `+💵 ${formatNumber(vipBonus)} VIP!`, "#f59e0b", 22));
        }
    }

    // 3. Zone 1: Lumberjack Tree Chopping
    const garyBonus = (gameState.managers.gary || 1) * 0.5;
    const spawnRateLv = gameState.upgrades.spawnRate || 1;
    logSpawnTimer += dt * (0.8 + spawnRateLv * 0.2 + garyBonus);

    if (lumberjackMesh && lumberjackMesh.userData.armGroup) {
        lumberjackMesh.userData.swingTimer += dt * 4;
        lumberjackMesh.userData.armGroup.rotation.x = Math.sin(lumberjackMesh.userData.swingTimer) * 0.8;
    }

    if (logSpawnTimer >= 2.0) {
        logSpawnTimer = 0;
        audio.playSfx('chop');

        // Spawn rolling log in 3D
        spawnRollingLog();
    }

    // 4. Update Rolling 3D Logs on Conveyor & Continuous Saw Spinning
    const convSpeedLv = gameState.upgrades.convSpeed || 1;
    const sawSpeedLv = gameState.upgrades.sawSpeed || 1;
    const tylerBonus = (gameState.managers.tyler || 0) * 0.6;
    const effectiveSawSpeed = 1.0 + sawSpeedLv * 0.25 + tylerBonus;

    // Saws spin continuously
    sawMeshes.forEach((sm, sIdx) => {
        if (sm.userData.blade) {
            sm.userData.blade.rotation.z += dt * 20 * effectiveSawSpeed;
        }
    });

    for (let i = rollingLogs3D.length - 1; i >= 0; i--) {
        const log = rollingLogs3D[i];
        log.mesh.position.x += 4.5 * dt * (1 + convSpeedLv * 0.18);
        log.mesh.rotation.z -= dt * 6;

        // Debarker interaction
        if (log.mesh.position.x > -12 && log.mesh.position.x < -10) {
            log.mesh.scale.set(0.9, 0.9, 0.9);
        }

        // Saw Blade interaction
        if (log.mesh.position.x >= -8 && log.mesh.position.x <= 2) {
            // Spawn sparks
            const screenP = toScreenXY(log.mesh.position);
            for (let s = 0; s < 2; s++) {
                particles2D.push(new Particle2D(
                    screenP.x + (Math.random() - 0.5) * 20,
                    screenP.y + (Math.random() - 0.5) * 20,
                    (Math.random() - 0.5) * 4,
                    -Math.random() * 4 - 2,
                    "#facc15",
                    Math.random() * 3 + 2,
                    0.4
                ));
            }
        }

        // Mill Complete -> Planks to Yard
        if (log.mesh.position.x > 2.5) {
            scene.remove(log.mesh);
            rollingLogs3D.splice(i, 1);

            gameState.stats.logsProcessed++;
            gameState.stats.planksMilled += 2;

            // Advance active orders
            ORDER_DEFS.forEach(ord => {
                gameState.ordersProgress[ord.id] = (gameState.ordersProgress[ord.id] || 0) + 1;
            });

            updateLumberTowers3D();
            checkAchievements();
            checkWoodTierUnlock();
        }
    }

    // 5. Zone 3: Forklift Patrol Routine
    if (forkliftMesh) {
        const rogerBonus = (gameState.managers.roger || 0) * 0.75;
        forkliftMesh.userData.patrolProgress += dt * (0.8 + rogerBonus);
        const cycle = Math.sin(forkliftMesh.userData.patrolProgress);
        forkliftMesh.position.z = 8 + cycle * 4;
        if (forkliftMesh.userData.forks) {
            forkliftMesh.userData.forks.position.y = 0.4 + Math.max(0, cycle) * 0.8;
        }
    }

    // 6. Gantry Crane Hoist & Cargo Ship
    const craneSpeedLv = gameState.upgrades.craneSpeed || 1;
    craneTimer += dt * (1 + craneSpeedLv * 0.2);

    if (gantryCraneGroup && gantryCraneGroup.userData.trolley) {
        gantryCraneGroup.userData.timer += dt * 1.2;
        gantryCraneGroup.userData.trolley.position.x = Math.sin(gantryCraneGroup.userData.timer) * 4.5;
        gantryCraneGroup.userData.hoist.position.x = gantryCraneGroup.userData.trolley.position.x;
        gantryCraneGroup.userData.hoist.position.y = 4.0 + Math.cos(gantryCraneGroup.userData.timer * 2) * 1.2;
    }

    // Cargo Ship Export Sailing Cycle
    if (cargoShipMesh) {
        const drakeBonus = (gameState.managers.drake || 0) * 0.5;
        const maxCargo = gameState.expansions.panamax_wharf ? 8 : 4;

        if (cargoShipState === "docked") {
            if (craneTimer >= 2.0) {
                craneTimer = 0;
                cargoShipCargo++;
                const screenP = toScreenXY(new THREE.Vector3(28, 2, 6));
                floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y, `🚢 Container Loaded (${cargoShipCargo}/${maxCargo})`, "#38bdf8", 13));

                if (cargoShipCargo >= maxCargo) {
                    cargoShipState = "sailing";
                    audio.playSfx('honk');
                    showToast("🚢 Cargo Ship 'S.S. LOG JAM' Departing with Bulk Export!");
                }
            }
        } else if (cargoShipState === "sailing") {
            cargoShipMesh.position.z += (6.0 + drakeBonus * 3) * dt;
            if (cargoShipMesh.position.z > 55.0) {
                cargoShipMesh.position.z = -55.0;
                cargoShipState = "returning";

                const tier = WOOD_TIERS[gameState.woodTier];
                const wharfMult = gameState.expansions.panamax_wharf ? 3.0 : 1.0;
                const drakeCashMult = 1.0 + (gameState.managers.drake || 0);
                const payout = Math.round(1200 * tier.value * wharfMult * drakeCashMult * (1 + (gameState.upgrades.woodValue || 0) * 0.2));

                gameState.coins += payout;
                gameState.totalEarned += payout;
                gameState.stats.cargoShipped++;
                audio.playSfx('cash');

                const screenP = toScreenXY(new THREE.Vector3(30, 2, 10));
                floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y, `+💵 ${formatNumber(payout)} BULK EXPORT!`, "#38bdf8", 22));
            }
        } else if (cargoShipState === "returning") {
            cargoShipMesh.position.z += (6.0 + drakeBonus * 3) * dt;
            if (cargoShipMesh.position.z >= 6.0) {
                cargoShipMesh.position.z = 6.0;
                cargoShipCargo = 0;
                cargoShipState = "docked";
                showToast("⚓ 'S.S. LOG JAM' Docked at Harbor Wharf");
            }
        }
    }

    // 7. Zone 5: Delivery Truck Fleet Simulation
    updateTrucksSimulation(dt);

    // 8. 2D Canvas Overlay Particles & Texts
    render2DOverlay(dt);

    // 9. Periodic HUD & Auto-Save
    saveTimer += dt;
    if (saveTimer >= 20) {
        saveTimer = 0;
        Storage.saveLocal();
        Storage.syncCloud();
    }

    updateHUD();

    // 10. CRUCIAL: Render 3D Three.js Scene!
    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

function spawnRollingLog() {
    const logGeo = new THREE.CylinderGeometry(0.35, 0.4, 2.2, 12);
    const tier = WOOD_TIERS[gameState.woodTier];
    const logMat = new THREE.MeshStandardMaterial({ color: tier.color, roughness: 0.7 });
    const logMesh = new THREE.Mesh(logGeo, logMat);
    logMesh.rotation.z = Math.PI / 2;
    logMesh.position.set(-13, 1.35, -12);
    logMesh.castShadow = true;
    scene.add(logMesh);

    rollingLogs3D.push({ mesh: logMesh });
}

function updateTrucksSimulation(dt) {
    const desiredTrucks = Math.min(4, Math.max(1, gameState.upgrades.truckCount || 1));
    while (trucks3D.length < desiredTrucks) {
        trucks3D.push(new Truck3D(trucks3D.length));
    }

    const truckSpeedLv = gameState.upgrades.truckSpeed || 1;
    const meganBonus = (gameState.managers.megan || 0) * 0.5;
    const speed = (9.0 + truckSpeedLv * 1.5 + meganBonus);

    let hasAnyJam = false;

    trucks3D.forEach((truck, idx) => {
        if (truck.isJammed) {
            hasAnyJam = true;
            truck.setEmoji("😡");
            return;
        }

        if (truck.state === "driving_in") {
            truck.group.position.z += speed * dt;
            if (truck.group.position.z >= 6 + idx * 5.0) {
                truck.group.position.z = 6 + idx * 5.0;
                truck.state = "loading";
                truck.setEmoji("📦");
                truck.loadTimer = 0;
            }
        } else if (truck.state === "loading") {
            truck.loadTimer = (truck.loadTimer || 0) + dt;
            if (truck.loadTimer >= 1.5) {
                truck.state = "driving_out";
                truck.setEmoji("🚚");

                // Check for random traffic jam (if no express highway expansion)
                if (!gameState.expansions.express_highway && Math.random() < 0.12 && !gameState.managers.megan) {
                    truck.isJammed = true;
                    truck.setEmoji("😡");
                }
            }
        } else if (truck.state === "driving_out") {
            truck.group.position.z += speed * dt;
            if (truck.group.position.z >= 55.0) {
                // Delivered cargo!
                truck.group.position.z = -45.0;
                truck.state = "driving_in";
                truck.setEmoji(null);

                const tier = WOOD_TIERS[gameState.woodTier];
                const sophiaBonus = 1.0 + (gameState.managers.sophia || 0) * 0.35;
                const acornMult = 1.0 + gameState.goldenAcorns * 0.05;
                const payout = Math.round(65 * tier.value * sophiaBonus * acornMult * (1 + (gameState.upgrades.woodValue || 0) * 0.2));

                gameState.coins += payout;
                gameState.totalEarned += payout;
                gameState.stats.deliveries++;
                audio.playSfx('cash');

                const screenP = toScreenXY(truck.group.position);
                floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y, `+💵 ${formatNumber(payout)}`, "#34d399", 16));
            }
        }
    });

    const banner = document.getElementById("banner-quick-action");
    if (banner) banner.style.display = hasAnyJam ? "flex" : "none";
}

function render2DOverlay(dt) {
    overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

    for (let i = particles2D.length - 1; i >= 0; i--) {
        if (!particles2D[i].update(dt)) {
            particles2D.splice(i, 1);
        } else {
            particles2D[i].draw(overlayCtx);
        }
    }

    for (let i = floatingTexts2D.length - 1; i >= 0; i--) {
        if (!floatingTexts2D[i].update(dt)) {
            floatingTexts2D.splice(i, 1);
        } else {
            floatingTexts2D[i].draw(overlayCtx);
        }
    }
}

function updateHUD() {
    document.getElementById("coin-counter").textContent = formatNumber(gameState.coins);
    document.getElementById("acorn-count").textContent = gameState.goldenAcorns;

    const tier = WOOD_TIERS[gameState.woodTier];
    document.getElementById("badge-wood-tier").textContent = `🌲 ${tier.name}`;
}

function checkWoodTierUnlock() {
    if (gameState.woodTier < WOOD_TIERS.length - 1) {
        const next = WOOD_TIERS[gameState.woodTier + 1];
        if (gameState.totalEarned >= next.unlockCost) {
            gameState.woodTier++;
            audio.playSfx('fanfare');
            showToast(`🌟 Promoted to ${next.name} Timber Tier!`);
            updateLumberTowers3D();
        }
    }
}

function checkAchievements() {
    ACHIEVEMENTS.forEach(ach => {
        if (!gameState.achievements.includes(ach.id) && ach.cond(gameState)) {
            gameState.achievements.push(ach.id);
            gameState.coins += ach.reward;
            audio.playSfx('fanfare');
            showToast(`🏅 Achievement Unlocked: ${ach.name}! +💵 ${formatNumber(ach.reward)}`);
        }
    });
}

// ==========================================
// 6. UI SETUP & EVENT LISTENERS
// ==========================================
function setupUI() {
    // Audio initialises on first touch/click anywhere
    window.addEventListener("pointerdown", () => {
        audio.init();
    }, { once: true });

    // Zone Navigation Pills
    document.querySelectorAll(".zone-pill").forEach(btn => {
        btn.onclick = () => {
            switchZoneCamera(btn.dataset.zone);
            audio.playSfx('click');
        };
    });

    // Bottom Navigation Dock Tabs
    document.querySelectorAll(".dock-tab").forEach(tab => {
        tab.onclick = () => {
            const modalId = tab.dataset.modal;
            document.querySelectorAll(".dock-tab").forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            openModal(modalId);
            audio.playSfx('click');
        };
    });

    // Modal Close Buttons
    document.querySelectorAll(".modal-close").forEach(btn => {
        btn.onclick = () => {
            closeModal(btn.dataset.close);
            audio.playSfx('click');
        };
    });

    // Buy Multiplier tabs in Shop
    document.querySelectorAll(".mult-tab").forEach(tab => {
        tab.onclick = () => {
            document.querySelectorAll(".mult-tab").forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            buyMultiplier = tab.dataset.mult;
            renderShopUI();
            audio.playSfx('click');
        };
    });

    // Quick Action Banner (Unjam all trucks)
    document.getElementById("banner-quick-action").onclick = () => {
        trucks3D.forEach(t => {
            if (t.isJammed) {
                t.isJammed = false;
                t.setEmoji("✨");
                gameState.stats.jamsCleared++;
                gameState.coins += 150;
                setTimeout(() => t.setEmoji(null), 1200);
            }
        });
        audio.playSfx('cash');
        showToast("✨ All trucks unjammed!");
    };

    // Top HUD Buttons
    document.getElementById("btn-daily").onclick = () => openModal("modal-daily");
    document.getElementById("btn-achievements").onclick = () => openModal("modal-achievements");
    document.getElementById("btn-leaderboard").onclick = () => openModal("modal-leaderboard");
    document.getElementById("btn-settings-toggle").onclick = () => openModal("modal-settings");
    document.getElementById("btn-user-auth").onclick = () => openModal("modal-auth");

    // Audio SFX / Music Toggles
    const sfxBtn = document.getElementById("toggle-sfx");
    sfxBtn.onclick = () => {
        audio.sfxEnabled = !audio.sfxEnabled;
        sfxBtn.textContent = `SFX: ${audio.sfxEnabled ? 'ON' : 'OFF'}`;
    };

    const musicBtn = document.getElementById("toggle-music");
    musicBtn.onclick = () => {
        audio.musicEnabled = !audio.musicEnabled;
        musicBtn.textContent = `Music: ${audio.musicEnabled ? 'ON' : 'OFF'}`;
        if (audio.musicEnabled) audio.startMusic();
    };

    document.getElementById("btn-audio-toggle").onclick = () => {
        audio.init();
        audio.sfxEnabled = !audio.sfxEnabled;
        audio.musicEnabled = audio.sfxEnabled;
        if (audio.musicEnabled) audio.startMusic();
        showToast(`Sound: ${audio.sfxEnabled ? 'ON' : 'OFF'}`);
    };

    // Daily Claim
    document.getElementById("btn-claim-daily").onclick = () => {
        gameState.coins += 1000 * gameState.dailyStreak;
        gameState.totalEarned += 1000 * gameState.dailyStreak;
        audio.playSfx('cash');
        closeModal("modal-daily");
        showToast(`🎁 Claimed Day ${gameState.dailyStreak} Reward! +💵 ${formatNumber(1000 * gameState.dailyStreak)}`);
    };

    // Settings
    document.getElementById("setting-server-url").value = gameState.settings.serverUrl || API_CONFIG.BASE_URL;
    document.getElementById("btn-save-settings").onclick = () => {
        gameState.settings.serverUrl = document.getElementById("setting-server-url").value.trim();
        Storage.saveLocal();
        Storage.syncCloud();
        showToast("Settings saved and synced!");
        closeModal("modal-settings");
    };

    document.getElementById("btn-reset-game").onclick = () => {
        if (confirm("Reset all game progress? This cannot be undone!")) {
            gameState = createDefaultState();
            Storage.saveLocal();
            location.reload();
        }
    };

    // Cloud Auth Login / Register
    document.getElementById("btn-login-cloud").onclick = async () => {
        const u = document.getElementById("auth-username").value.trim();
        const p = document.getElementById("auth-password").value.trim();
        if (!u || !p) return;
        const msg = document.getElementById("auth-status-msg");
        msg.textContent = "Connecting to Xperia phone...";
        try {
            const baseUrl = gameState.settings.serverUrl || API_CONFIG.BASE_URL;
            const res = await fetch(`${baseUrl}${API_CONFIG.AUTH_ENDPOINT}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: u, password: p, action: "login" })
            });
            const data = await res.json();
            if (data.success) {
                currentUser = { username: u };
                localStorage.setItem(Storage.USER_KEY, JSON.stringify(currentUser));
                if (data.save) gameState = data.save;
                msg.textContent = `Welcome back, ${u}!`;
                setTimeout(() => closeModal("modal-auth"), 1200);
            } else {
                msg.textContent = `Login failed: ${data.detail || 'check password'}`;
            }
        } catch(e) {
            msg.textContent = `Cloud error: ${e.message}`;
        }
    };

    document.getElementById("btn-register-cloud").onclick = async () => {
        const u = document.getElementById("auth-username").value.trim();
        const p = document.getElementById("auth-password").value.trim();
        if (!u || !p) return;
        const msg = document.getElementById("auth-status-msg");
        msg.textContent = "Registering Tycoon...";
        try {
            const baseUrl = gameState.settings.serverUrl || API_CONFIG.BASE_URL;
            const res = await fetch(`${baseUrl}${API_CONFIG.AUTH_ENDPOINT}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: u, password: p, action: "register" })
            });
            const data = await res.json();
            if (data.success) {
                currentUser = { username: u };
                localStorage.setItem(Storage.USER_KEY, JSON.stringify(currentUser));
                msg.textContent = `Registered! Syncing save...`;
                Storage.syncCloud();
                setTimeout(() => closeModal("modal-auth"), 1200);
            } else {
                msg.textContent = `Register failed: ${data.detail || 'username taken'}`;
            }
        } catch(e) {
            msg.textContent = `Cloud error: ${e.message}`;
        }
    };
}

function checkOfflineEarnings() {
    if (gameState.lastSaveTime) {
        const elapsedSec = Math.min(API_CONFIG.OFFLINE_MAX_HOURS * 3600, (Date.now() - gameState.lastSaveTime) / 1000);
        if (elapsedSec > 45) {
            const tier = WOOD_TIERS[gameState.woodTier];
            const offlineRate = Math.max(5, (gameState.stats.deliveries > 0 ? (gameState.totalEarned / Math.max(60, gameState.stats.playTime || 60)) : 12) * 0.4);
            const earned = Math.round(elapsedSec * offlineRate);

            if (earned > 25) {
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
    }
}

// ------------------------------------------
// INITIALIZE
// ------------------------------------------
window.addEventListener("DOMContentLoaded", () => {
    const saved = Storage.loadLocal();
    if (saved) gameState = saved;

    const savedUser = localStorage.getItem(Storage.USER_KEY);
    if (savedUser) {
        try { currentUser = JSON.parse(savedUser); } catch(e) {}
    }

    init3DScene();
    setupUI();
    checkOfflineEarnings();
    requestAnimationFrame(animate);
});
'''
