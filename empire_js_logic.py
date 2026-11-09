# -*- coding: utf-8 -*-
JS_GAME_LOGIC = r'''
// ==========================================
// 4. GAME STATE & ECONOMY ENGINE
// ==========================================
function createDefaultState() {
    return {
        coins: 100,
        goldenAcorns: 0,
        woodTier: 0,
        prestigeCount: 0,
        totalEarned: 100,
        lastSaveTime: Date.now(),
        upgrades: {
            spawnRate: 1,
            convSpeed: 1,
            sawSpeed: 1,
            sawCount: 1,
            craneSpeed: 1,
            truckSpeed: 1,
            truckCount: 1,
            woodValue: 0
        },
        expansions: {},
        managers: {
            gary: 1,
            tyler: 0,
            roger: 0,
            drake: 0,
            megan: 0,
            sophia: 0
        },
        ordersProgress: {
            order_1: 0,
            order_2: 0,
            order_3: 0,
            order_4: 0
        },
        stats: {
            logsProcessed: 0,
            planksMilled: 0,
            deliveries: 0,
            cargoShipped: 0,
            jamsCleared: 0,
            playTime: 0
        },
        achievements: [],
        dailyStreak: 1,
        lastDailyClaim: 0,
        settings: {
            sfx: true,
            music: true,
            serverUrl: API_CONFIG.BASE_URL
        }
    };
}

let gameState = createDefaultState();
let currentUser = null;
let buyMultiplier = "1";

// ------------------------------------------
// STORAGE & CLOUD SYNC (Xperia Termux Server)
// ------------------------------------------
const Storage = {
    LOCAL_KEY: "logjam_save_v2",
    USER_KEY: "logjam_active_user",

    saveLocal() {
        gameState.lastSaveTime = Date.now();
        localStorage.setItem(this.LOCAL_KEY, JSON.stringify(gameState));
    },

    loadLocal() {
        try {
            const raw = localStorage.getItem(this.LOCAL_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch(e) { return null; }
    },

    async syncCloud() {
        if (!currentUser) return;
        const baseUrl = gameState.settings.serverUrl || API_CONFIG.BASE_URL;
        try {
            const res = await fetch(`${baseUrl}${API_CONFIG.SAVE_ENDPOINT}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: currentUser.username,
                    save: gameState,
                    leaderboard_entry: {
                        username: currentUser.username,
                        coins: gameState.coins,
                        total_earned: gameState.totalEarned,
                        wood_tier: gameState.woodTier,
                        prestige_count: gameState.prestigeCount,
                        timestamp: Date.now()
                    }
                })
            });
            if (res.ok) {
                updateSyncStatus("☁️ Cloud Synced", "#34d399");
            }
        } catch(e) {
            updateSyncStatus("💾 Saved Locally", "#94a3b8");
        }
    },

    async fetchLeaderboard() {
        const baseUrl = gameState.settings.serverUrl || API_CONFIG.BASE_URL;
        try {
            const res = await fetch(`${baseUrl}${API_CONFIG.LEADERBOARD_ENDPOINT}`);
            if (res.ok) return await res.json();
        } catch(e) {}
        return null;
    }
};

function updateSyncStatus(msg, color) {
    const el = document.getElementById("badge-wood-tier");
    if (el) {
        const tier = WOOD_TIERS[gameState.woodTier];
        el.textContent = `🌲 ${tier.name}`;
    }
}

function formatNumber(num) {
    if (!num || isNaN(num)) return "0";
    if (num < 1000) return Math.floor(num).toLocaleString();
    const suffixes = ["", "K", "M", "B", "T", "Qd"];
    const i = Math.floor(Math.log10(num) / 3);
    const formatted = (num / Math.pow(10, i * 3)).toFixed(1);
    return `${formatted}${suffixes[i] || ""}`;
}

function showToast(msg) {
    const container = document.getElementById("toast-container");
    const div = document.createElement("div");
    div.className = "toast-msg";
    div.textContent = msg;
    container.appendChild(div);
    setTimeout(() => div.remove(), 2500);
}

// ------------------------------------------
// MODAL & SCREEN CONTROLLER
// ------------------------------------------
function openModal(id) {
    document.querySelectorAll(".modal-overlay").forEach(m => m.classList.remove("active"));
    const modal = document.getElementById(id);
    if (modal) modal.classList.add("active");

    if (id === "modal-expansion") renderExpansionsUI();
    if (id === "modal-managers") renderManagersUI();
    if (id === "modal-orders") renderOrdersUI();
    if (id === "modal-analytics") renderAnalyticsUI();
    if (id === "modal-upgrades") renderShopUI();
    if (id === "modal-prestige") renderPrestigeUI();
    if (id === "modal-achievements") renderAchievementsUI();
    if (id === "modal-leaderboard") loadLeaderboardUI();
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove("active");
}

// ------------------------------------------
// SCREEN 1: EXPANSIONS & LAND PURCHASE
// ------------------------------------------
function renderExpansionsUI() {
    const container = document.getElementById("expansion-list-container");
    container.innerHTML = "";

    EXPANSION_SECTORS.forEach(sec => {
        const isOwned = !!gameState.expansions[sec.id];
        const canAfford = !isOwned && gameState.coins >= sec.cost;

        const card = document.createElement("div");
        card.className = `expansion-card ${isOwned ? 'unlocked' : ''}`;
        card.innerHTML = `
            <div class="expansion-info">
                <div class="expansion-icon">${sec.icon}</div>
                <div class="expansion-meta">
                    <h4>${sec.name}</h4>
                    <p>${sec.desc}</p>
                </div>
            </div>
            <div>
                ${isOwned 
                    ? `<span class="expansion-badge">✓ UNLOCKED</span>`
                    : `<button class="btn-full btn-primary" style="min-width: 110px; font-size: 13px; padding: 8px 12px;" ${!canAfford ? 'disabled' : ''} onclick="buyExpansion('${sec.id}')">
                         💵 ${formatNumber(sec.cost)}
                       </button>`
                }
            </div>
        `;
        container.appendChild(card);
    });
}

function buyExpansion(id) {
    const sec = EXPANSION_SECTORS.find(s => s.id === id);
    if (!sec || gameState.expansions[id]) return;
    if (gameState.coins >= sec.cost) {
        gameState.coins -= sec.cost;
        gameState.expansions[id] = true;
        audio.playSfx('fanfare');
        showToast(`🎉 Unlocked ${sec.name}!`);
        renderExpansionsUI();
        Storage.saveLocal();
    }
}

// ------------------------------------------
// SCREEN 2: MANAGERS & CREW
// ------------------------------------------
function renderManagersUI() {
    const container = document.getElementById("managers-list-container");
    container.innerHTML = "";

    MANAGER_DEFS.forEach(mgr => {
        const curLv = gameState.managers[mgr.id] || 0;
        const isHired = curLv > 0;
        const cost = mgr.costType === "acorns" ? mgr.cost : (mgr.cost * (curLv + 1));
        const canAfford = mgr.costType === "acorns" ? (gameState.goldenAcorns >= cost) : (gameState.coins >= cost);

        const card = document.createElement("div");
        card.className = `manager-card ${mgr.rarity}`;
        card.innerHTML = `
            <div class="manager-top">
                <div class="manager-avatar">${mgr.avatar}</div>
                <div class="manager-details">
                    <h4>${mgr.name}</h4>
                    <div class="manager-role">${mgr.role}</div>
                    <div class="manager-stars">${'★'.repeat(Math.max(1, curLv))}${'☆'.repeat(Math.max(0, 5 - curLv))}</div>
                </div>
            </div>
            <div class="manager-desc">${mgr.desc}</div>
            <button class="btn-full btn-primary" style="font-size: 13px; padding: 8px;" ${!canAfford ? 'disabled' : ''} onclick="upgradeManager('${mgr.id}')">
                ${isHired ? `Promote (${mgr.costType === 'acorns' ? '🌰 ' : '💵 '}${formatNumber(cost)})` : `Hire (${mgr.costType === 'acorns' ? '🌰 ' : '💵 '}${formatNumber(cost)})`}
            </button>
        `;
        container.appendChild(card);
    });
}

function upgradeManager(id) {
    const mgr = MANAGER_DEFS.find(m => m.id === id);
    if (!mgr) return;
    const curLv = gameState.managers[id] || 0;
    const cost = mgr.costType === "acorns" ? mgr.cost : (mgr.cost * (curLv + 1));

    if (mgr.costType === "acorns") {
        if (gameState.goldenAcorns >= cost) {
            gameState.goldenAcorns -= cost;
            gameState.managers[id] = curLv + 1;
            audio.playSfx('fanfare');
            showToast(`⭐ Promoted ${mgr.name}!`);
        }
    } else {
        if (gameState.coins >= cost) {
            gameState.coins -= cost;
            gameState.managers[id] = curLv + 1;
            audio.playSfx('fanfare');
            showToast(`⭐ Promoted ${mgr.name}!`);
        }
    }
    renderManagersUI();
    Storage.saveLocal();
}

// ------------------------------------------
// SCREEN 3: COMMERCIAL ORDERS & CONTRACTS
// ------------------------------------------
function renderOrdersUI() {
    const container = document.getElementById("orders-list-container");
    container.innerHTML = "";

    ORDER_DEFS.forEach(ord => {
        const progress = gameState.ordersProgress[ord.id] || 0;
        const isComplete = progress >= ord.reqPlanks;
        const pct = Math.min(100, Math.round((progress / ord.reqPlanks) * 100));

        const card = document.createElement("div");
        card.className = "order-card";
        card.innerHTML = `
            <div class="order-header">
                <div class="order-title">
                    <span>${ord.icon}</span>
                    <span>${ord.title}</span>
                </div>
                <div style="font-size: 12px; font-weight: 700; color: ${isComplete ? '#34d399' : 'var(--text-sub)'};">
                    ${progress} / ${ord.reqPlanks} Planks
                </div>
            </div>
            <div class="order-progress-track">
                <div class="order-progress-fill" style="width: ${pct}%;"></div>
            </div>
            <div class="order-footer">
                <div style="color: var(--gold); font-weight: 700;">
                    Reward: +💵 ${formatNumber(ord.rewardCoins)} ${ord.rewardAcorns > 0 ? `+ 🌰 ${ord.rewardAcorns}` : ''}
                </div>
                <button class="btn-primary" style="padding: 6px 14px; border-radius: 8px; font-size: 12px;" ${!isComplete ? 'disabled' : ''} onclick="claimOrder('${ord.id}')">
                    ${isComplete ? 'Collect Reward' : 'In Progress'}
                </button>
            </div>
        `;
        container.appendChild(card);
    });
}

function claimOrder(id) {
    const ord = ORDER_DEFS.find(o => o.id === id);
    if (!ord) return;
    if ((gameState.ordersProgress[id] || 0) >= ord.reqPlanks) {
        gameState.ordersProgress[id] = 0;
        gameState.coins += ord.rewardCoins;
        gameState.totalEarned += ord.rewardCoins;
        gameState.goldenAcorns += (ord.rewardAcorns || 0);
        audio.playSfx('cash');
        showToast(`🎉 Contract fulfilled! +💵 ${formatNumber(ord.rewardCoins)}`);
        renderOrdersUI();
        Storage.saveLocal();
    }
}

// ------------------------------------------
// SCREEN 4: FACTORY ANALYTICS & BOTTLENECK DETECTOR
// ------------------------------------------
function renderAnalyticsUI() {
    const spawnRateLv = gameState.upgrades.spawnRate || 1;
    const sawSpeedLv = gameState.upgrades.sawSpeed || 1;
    const sawCount = gameState.upgrades.sawCount || 1;
    const truckCount = gameState.upgrades.truckCount || 1;
    const truckSpeedLv = gameState.upgrades.truckSpeed || 1;
    const tier = WOOD_TIERS[gameState.woodTier];

    const harvestRate = Math.round(spawnRateLv * 14);
    const sawCapacity = Math.round(sawSpeedLv * sawCount * 12);
    const truckCapacity = Math.round(truckCount * truckSpeedLv * 10);
    const revenueRate = Math.round(truckCapacity * 50 * tier.value);

    document.getElementById("metric-harvest-rate").textContent = `${harvestRate} logs/m`;
    document.getElementById("metric-saw-rate").textContent = `${sawCapacity} p/m`;
    document.getElementById("metric-yard-fill").textContent = `${Math.min(60, towerStackMeshes.length * 2)} / 60`;
    document.getElementById("metric-revenue-rate").textContent = `💵 ${formatNumber(revenueRate)}/m`;

    const box = document.getElementById("bottleneck-status-box");
    const headline = document.getElementById("bottleneck-headline");
    const detail = document.getElementById("bottleneck-detail");
    const fixBtn = document.getElementById("btn-fix-bottleneck");

    if (sawCapacity < harvestRate * 0.8) {
        box.className = "bottleneck-box warning";
        headline.textContent = "⚠️ Sawmill Bottleneck";
        detail.textContent = "Raw logs are entering faster than your circular blades can slice them! Logs will pile up.";
        fixBtn.style.display = "block";
        fixBtn.textContent = "Quick Fix: Upgrade Saw Blade RPM";
        fixBtn.onclick = () => { closeModal("modal-analytics"); buyUpgrade("sawSpeed"); };
    } else if (truckCapacity < sawCapacity * 0.75) {
        box.className = "bottleneck-box warning";
        headline.textContent = "⚠️ Logistics Bottleneck";
        detail.textContent = "Planks are stacking up faster than your truck fleet can haul! Deploy more delivery trucks.";
        fixBtn.style.display = "block";
        fixBtn.textContent = "Quick Fix: Buy Extra Delivery Truck";
        fixBtn.onclick = () => { closeModal("modal-analytics"); buyUpgrade("truckCount"); };
    } else {
        box.className = "bottleneck-box optimal";
        headline.textContent = "⚡ Optimal Tycoon Equilibrium";
        detail.textContent = "Timber harvest, sawmill blades, and logistics trucks are perfectly balanced!";
        fixBtn.style.display = "none";
    }
}

// ------------------------------------------
// SCREEN 5: MACHINERY UPGRADES SHOP
// ------------------------------------------
function renderShopUI() {
    const container = document.getElementById("shop-items-container");
    container.innerHTML = "";

    UPGRADE_DEFS.forEach(def => {
        const curLv = gameState.upgrades[def.id] || 0;
        const isMax = curLv >= (def.maxLv || 100);

        let count = 1;
        let cost = 0;
        if (buyMultiplier === "1") {
            count = 1;
            cost = Math.round(def.baseCost * Math.pow(def.costMult, curLv));
        } else if (buyMultiplier === "10") {
            count = Math.min(10, (def.maxLv || 100) - curLv);
            for (let c = 0; c < count; c++) {
                cost += Math.round(def.baseCost * Math.pow(def.costMult, curLv + c));
            }
        } else if (buyMultiplier === "max") {
            count = 0;
            let tempCost = 0;
            while (curLv + count < (def.maxLv || 100)) {
                const singleCost = Math.round(def.baseCost * Math.pow(def.costMult, curLv + count));
                if (tempCost + singleCost > gameState.coins) break;
                tempCost += singleCost;
                count++;
            }
            cost = tempCost;
            if (count === 0) cost = Math.round(def.baseCost * Math.pow(def.costMult, curLv));
        }

        const canAfford = !isMax && count > 0 && gameState.coins >= cost;

        const card = document.createElement("div");
        card.className = "shop-card";
        card.innerHTML = `
            <div class="shop-card-info">
                <div class="shop-card-icon">${def.icon}</div>
                <div>
                    <div style="font-weight: 800; font-size: 14px;">${def.name} <span style="color: var(--cyan); font-size: 12px;">Lv. ${curLv}</span></div>
                    <div style="font-size: 11px; color: var(--text-sub);">${def.desc}</div>
                </div>
            </div>
            <button class="shop-card-btn" ${!canAfford ? 'disabled' : ''} onclick="buyUpgrade('${def.id}')">
                ${isMax ? 'MAX' : `+${count || 1}<br>💵 ${formatNumber(cost)}`}
            </button>
        `;
        container.appendChild(card);
    });
}

function buyUpgrade(defId) {
    const def = UPGRADE_DEFS.find(u => u.id === defId);
    if (!def) return;
    const curLv = gameState.upgrades[defId] || 0;
    const isMax = curLv >= (def.maxLv || 100);
    if (isMax) return;

    let count = 1;
    let cost = 0;
    if (buyMultiplier === "1") {
        count = 1;
        cost = Math.round(def.baseCost * Math.pow(def.costMult, curLv));
    } else if (buyMultiplier === "10") {
        count = Math.min(10, (def.maxLv || 100) - curLv);
        for (let c = 0; c < count; c++) {
            cost += Math.round(def.baseCost * Math.pow(def.costMult, curLv + c));
        }
    } else if (buyMultiplier === "max") {
        count = 0;
        let tempCost = 0;
        while (curLv + count < (def.maxLv || 100)) {
            const singleCost = Math.round(def.baseCost * Math.pow(def.costMult, curLv + count));
            if (tempCost + singleCost > gameState.coins) break;
            tempCost += singleCost;
            count++;
        }
        cost = tempCost;
    }

    if (count > 0 && gameState.coins >= cost) {
        gameState.coins -= cost;
        gameState.upgrades[defId] = curLv + count;
        audio.playSfx('cash');
        showToast(`⚡ Upgraded ${def.name} (+${count})!`);

        if (defId === "sawCount") updateSaws3D();
        updateWorldPadsUI();
        renderShopUI();
        Storage.saveLocal();
    } else {
        audio.playSfx('click');
        showToast(`Need 💵 ${formatNumber(cost - gameState.coins)} more cash!`);
    }
}

// ------------------------------------------
// SCREEN 6: PRESTIGE & EMPIRE REBIRTH
// ------------------------------------------
function renderPrestigeUI() {
    const acornsToGain = Math.max(0, Math.floor(Math.sqrt((gameState.totalEarned || 0) / 10000)));
    const currentBoost = gameState.goldenAcorns * 5;
    document.getElementById("prestige-gain-val").textContent = `+${acornsToGain} 🌰`;
    document.getElementById("prestige-boost-val").textContent = `Current Acorn Boost: +${currentBoost}% permanent income`;

    const btn = document.getElementById("btn-prestige-confirm");
    btn.disabled = acornsToGain < 1;
    btn.onclick = () => {
        if (acornsToGain < 1) return;
        gameState.goldenAcorns += acornsToGain;
        gameState.prestigeCount++;
        gameState.coins = 150;
        gameState.woodTier = 0;
        gameState.upgrades = createDefaultState().upgrades;
        audio.playSfx('fanfare');
        closeModal("modal-prestige");
        showToast(`🌟 Empire Reborn with +${acornsToGain} Golden Acorns!`);
        updateSaws3D();
        updateLumberTowers3D();
        updateWorldPadsUI();
        Storage.saveLocal();
    };
}

// ------------------------------------------
// SCREEN 7: ACHIEVEMENTS
// ------------------------------------------
function renderAchievementsUI() {
    const container = document.getElementById("achievements-list-container");
    container.innerHTML = "";

    ACHIEVEMENTS.forEach(ach => {
        const isDone = gameState.achievements.includes(ach.id);
        const card = document.createElement("div");
        card.style.cssText = "background: rgba(255,255,255,0.03); border: 1px solid var(--panel-border); border-radius: 14px; padding: 12px; display: flex; align-items: center; justify-content: space-between;";
        card.innerHTML = `
            <div>
                <div style="font-weight: 800; font-size: 14px;">${ach.name}</div>
                <div style="font-size: 11px; color: var(--text-sub);">${ach.desc}</div>
            </div>
            <div style="font-weight: 800; font-size: 12px; color: ${isDone ? '#34d399' : 'var(--text-sub)'};">
                ${isDone ? '✓ COMPLETED' : `+💵 ${formatNumber(ach.reward)}`}
            </div>
        `;
        container.appendChild(card);
    });
}

// ------------------------------------------
// SCREEN 8: CLOUD LEADERBOARD
// ------------------------------------------
async function loadLeaderboardUI() {
    const container = document.getElementById("leaderboard-list-container");
    container.innerHTML = '<div style="text-align: center; color: var(--text-sub); padding: 16px;">Contacting Xperia Cloud...</div>';

    const data = await Storage.fetchLeaderboard();
    container.innerHTML = "";

    if (data && data.leaderboard && data.leaderboard.length > 0) {
        data.leaderboard.forEach((entry, idx) => {
            const row = document.createElement("div");
            row.style.cssText = "display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(255,255,255,0.04); border-radius: 10px;";
            row.innerHTML = `
                <div style="font-weight: 700;">#${idx + 1} 👤 ${entry.username}</div>
                <div style="font-weight: 800; color: #10b981;">💵 ${formatNumber(entry.total_earned)}</div>
            `;
            container.appendChild(row);
        });
    } else {
        container.innerHTML = '<div style="text-align: center; color: var(--text-sub); padding: 16px;">No global records yet. Be the first Tycoon!</div>';
    }
}
'''

