with open('build_index_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add ship sound to SoundEngine
old_sound = '''            } else if (type === 'saw') {'''
new_sound = '''            } else if (type === 'ship') {
                [85, 110].forEach(f => {
                    const osc = this.ctx.createOscillator();
                    const g = this.ctx.createGain();
                    osc.type = "sawtooth";
                    osc.frequency.setValueAtTime(f, now);
                    g.gain.setValueAtTime(0.15, now);
                    g.gain.exponentialRampToValueAtTime(0.001, now + 0.9);
                    osc.connect(g); g.connect(this.sfxGain);
                    osc.start(now); osc.stop(now + 0.9);
                });
            } else if (type === 'saw') {'''
text = text.replace(old_sound, new_sound)

# 2. Add cargo ship state
old_trucks_var = '''let trucks = [];'''
new_trucks_var = '''let trucks = [];
let cargoShip = { x: 17.0, y: 7.0, state: "docked", cargo: 0, maxCargo: 6, wakeTimer: 0 };'''
text = text.replace(old_trucks_var, new_trucks_var)

# 3. Remove static ship from background canvas
old_bg_ship = '''    // Cargo Ship
    const sp = toIso(17, 7, 0.1);
    bgCtx.fillStyle = "#f8fafc"; // White hull
    bgCtx.beginPath();
    bgCtx.ellipse(sp.x + 10, sp.y, 34, 16, 0, 0, Math.PI * 2);
    bgCtx.fill();
    bgCtx.fillStyle = "#0284c7"; // Blue deck cabin
    bgCtx.fillRect(sp.x - 4, sp.y - 12, 16, 12);'''
new_bg_ship = '''    // Pier Water Edge
    const sp = toIso(16.5, 7, 0);
    bgCtx.fillStyle = "rgba(0,0,0,0.15)";
    bgCtx.fillRect(sp.x - 10, sp.y - 15, 20, 45);'''
text = text.replace(old_bg_ship, new_bg_ship)

# 4. Add Cargo Ship simulation into updateProductionLine
old_truck_loop = '''    // Crane loading from Tower to Docked Truck'''
new_truck_loop = '''    // Cargo Ship Bulk Export System
    if (cargoShip.state === "docked") {
        if (lumberTowerCount >= 6 && cargoShip.cargo < cargoShip.maxCargo && craneTimer >= 1.6) {
            craneTimer = 0;
            lumberTowerCount = Math.max(0, lumberTowerCount - 2);
            cargoShip.cargo++;
            const shP = toIso(cargoShip.x, cargoShip.y, 0.5);
            floatingTexts.push(new FloatingText(shP.x, shP.y, "🚢 Ship Loaded!", "#38bdf8", 13));
            if (cargoShip.cargo >= cargoShip.maxCargo) {
                cargoShip.state = "sailing";
                audio.playSfx('ship');
                showCelebratoryBanner("🚢 CARGO SHIP DEPARTING WITH BULK EXPORT!");
            }
        }
    } else if (cargoShip.state === "sailing") {
        cargoShip.y += 1.8 * dt * speedMult;
        // Water wake particles
        if (Math.random() < 0.4) {
            const shP = toIso(cargoShip.x, cargoShip.y, 0);
            particles.push(new Particle(shP.x - 10, shP.y, (Math.random() - 0.5) * 20, 10, "#e0f2fe", 3, 0.6));
        }
        if (cargoShip.y > 22.0) {
            cargoShip.y = -6.0;
            cargoShip.state = "returning";
            // Huge Bulk Export Payout!
            const tier = WOOD_TIERS[gameState.woodTier];
            const bulkPayout = Math.round(cargoShip.maxCargo * 40 * tier.value * (1 + (gameState.upgrades.woodValue || 0) * 0.15));
            gameState.coins += bulkPayout;
            gameState.totalEarned += bulkPayout;
            audio.playSfx('cash');
            const dp = toIso(16.0, 14.0, 0);
            floatingTexts.push(new FloatingText(dp.x, dp.y, `+💵 ${formatNumber(bulkPayout)} BULK EXPORT!`, "#38bdf8", 22));
        }
    } else if (cargoShip.state === "returning") {
        cargoShip.y += 2.0 * dt * speedMult;
        if (cargoShip.y >= 7.0) {
            cargoShip.y = 7.0;
            cargoShip.cargo = 0;
            cargoShip.state = "docked";
            audio.playSfx('ship');
            showToast("🚢 Cargo Ship returned to harbor dock!");
        }
    }

    // Crane loading from Tower to Docked Truck'''
text = text.replace(old_truck_loop, new_truck_loop)

# 5. Render Cargo Ship dynamically in renderGameEntities
old_render_end = '''    // 7. Delivery Trucks with Traffic Jam Emojis
    trucks.forEach(t => drawTruckEntity(mainCtx, t));'''
new_render_end = '''    // 7. Dynamic Cargo Ship & Foaming Wakes
    const shP = toIso(cargoShip.x, cargoShip.y, 0.1);
    const shBob = Math.sin(Date.now() * 0.003) * 2;

    // Ship Water Wake
    if (cargoShip.state !== "docked") {
        mainCtx.strokeStyle = "rgba(255,255,255,0.4)";
        mainCtx.lineWidth = 2;
        mainCtx.beginPath();
        mainCtx.ellipse(shP.x, shP.y + 12 + shBob, 36, 14, 0, 0, Math.PI * 2);
        mainCtx.stroke();
    }

    // Ship Hull
    mainCtx.fillStyle = "#f8fafc";
    mainCtx.beginPath();
    mainCtx.ellipse(shP.x + 8, shP.y + shBob, 38, 18, 0, 0, Math.PI * 2);
    mainCtx.fill();
    mainCtx.strokeStyle = "#94a3b8";
    mainCtx.lineWidth = 1.5;
    mainCtx.stroke();

    // Cargo Hold with Planks
    if (cargoShip.cargo > 0) {
        for (let c = 0; c < cargoShip.cargo; c++) {
            drawIsoBox(mainCtx, cargoShip.x - 0.2, cargoShip.y - 0.4 + c * 0.15, 0.2 + shBob * 0.02, 0.7, 0.5, 0.2, tier.plankColor, tier.barkColor, tier.barkColor);
        }
    }

    // Cabin
    mainCtx.fillStyle = "#0284c7";
    mainCtx.fillRect(shP.x - 8, shP.y - 14 + shBob, 18, 14);
    mainCtx.fillStyle = "#e0f2fe";
    mainCtx.fillRect(shP.x - 4, shP.y - 10 + shBob, 6, 5);

    // 8. Delivery Trucks with Traffic Jam Emojis
    trucks.forEach(t => drawTruckEntity(mainCtx, t));'''
text = text.replace(old_render_end, new_render_end)

with open('build_index_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("build_index_v2.py updated with dynamic cargo ship bulk export system!")
