# -*- coding: utf-8 -*-
JS_DATA_AND_AUDIO = r'''
// ==========================================
// 1. CONFIGURATION & CONSTANTS
// ==========================================
const API_CONFIG = {
    BASE_URL: "https://customs-wins-wallace-ultimately.trycloudflare.com",
    ALT_URL: "http://192.168.1.200:8000",
    AUTH_ENDPOINT: "/api/user/auth",
    SAVE_ENDPOINT: "/api/user/save",
    LOAD_ENDPOINT: "/api/user",
    LEADERBOARD_ENDPOINT: "/api/leaderboard",
    HEALTH_ENDPOINT: "/api/health",
    AUTO_SAVE_INTERVAL: 20000,
    OFFLINE_MAX_HOURS: 8
};

const WOOD_TIERS = [
    { name: "Pine", color: 0x22c55e, hex: "#22c55e", value: 1.0, unlockCost: 0 },
    { name: "Cedar", color: 0xeab308, hex: "#eab308", value: 2.5, unlockCost: 2000 },
    { name: "Oak", color: 0xd97706, hex: "#d97706", value: 6.0, unlockCost: 15000 },
    { name: "Teak", color: 0xb45309, hex: "#b45309", value: 16.0, unlockCost: 80000 },
    { name: "Redwood", color: 0x991b1b, hex: "#991b1b", value: 45.0, unlockCost: 400000 },
    { name: "Golden Sequoia", color: 0xfbbf24, hex: "#fbbf24", value: 150.0, unlockCost: 2000000 }
];

const UPGRADE_DEFS = [
    { id: "spawnRate", name: "Forest Lumberjacks", icon: "🪓", baseCost: 18, costMult: 1.15, maxLv: 60, desc: "Faster tree harvesting & log delivery" },
    { id: "convSpeed", name: "Conveyor Belt Speed", icon: "⏩", baseCost: 35, costMult: 1.15, maxLv: 50, desc: "Accelerates timber transit through mill" },
    { id: "sawSpeed", name: "Saw Blade RPM", icon: "⚡", baseCost: 50, costMult: 1.16, maxLv: 60, desc: "Increases cutting speed & avoids log jams" },
    { id: "sawCount", name: "Gantry Saw Count", icon: "🪚", baseCost: 200, costMult: 2.2, maxLv: 6, desc: "Adds an extra spinning circular blade line" },
    { id: "craneSpeed", name: "Yard Forklift & Crane", icon: "🏗️", baseCost: 75, costMult: 1.16, maxLv: 40, desc: "Speeds up timber stacking & ship loading" },
    { id: "truckSpeed", name: "Delivery Truck Speed", icon: "🚚", baseCost: 60, costMult: 1.15, maxLv: 50, desc: "Reduces round-trip highway transit time" },
    { id: "truckCount", name: "Truck Fleet Size", icon: "🚛", baseCost: 250, costMult: 2.4, maxLv: 4, desc: "Deploys additional delivery flatbed trucks" },
    { id: "woodValue", name: "Timber Planer Finish", icon: "✨", baseCost: 90, costMult: 1.20, maxLv: 50, desc: "+20% cash value per sawn timber pallet" }
];

const EXPANSION_SECTORS = [
    { id: "redwood_tract", name: "Old Growth Timber Tract", icon: "🌲", cost: 800, desc: "Deep forest reserve with +50% log value and instant tree replanting." },
    { id: "twin_saws", name: "Twin Gang Saw Line", icon: "🪚", cost: 3500, desc: "Doubles primary sawmill throughput and prevents cutting jams." },
    { id: "hydraulic_debarker", name: "Hydraulic Debarker Hub", icon: "🪵", cost: 12000, desc: "Pre-treats raw logs, boosting sawn timber value by +40%." },
    { id: "forklift_fleet", name: "Robotic Forklift Fleet", icon: "🚜", cost: 30000, desc: "Deploys an automated forklift in the yard, doubling stack speed." },
    { id: "panamax_wharf", name: "Deepwater Panamax Wharf", icon: "🚢", cost: 75000, desc: "Upgrades cargo ship to 8 crates for 3x maritime export payouts." },
    { id: "express_highway", name: "Interstate 4-Lane Highway", icon: "🛣️", cost: 180000, desc: "Doubles delivery truck speed and permanently clears traffic jams." },
    { id: "vip_helipad", name: "Executive Helipad & Terminal", icon: "🚁", cost: 500000, desc: "Summons billionaire VIP investors for instant mega cash drops." }
];

const MANAGER_DEFS = [
    { id: "gary", name: "Foreman Gary", role: "Forest Chief", avatar: "🧔", rarity: "common", cost: 0, costType: "free", desc: "+50% faster tree harvesting in forest" },
    { id: "tyler", name: "Chief Tyler", role: "Master Sawyer", avatar: "👨‍🔧", rarity: "rare", cost: 450, costType: "cash", desc: "+60% saw throughput & prevents saw jams" },
    { id: "roger", name: "Roger Swift", role: "Yard Supervisor", avatar: "👷", rarity: "rare", cost: 1800, costType: "cash", desc: "Doubles forklift carrying capacity & speed" },
    { id: "drake", name: "Captain Drake", role: "Harbor Master", avatar: "👨‍✈️", rarity: "epic", cost: 8500, costType: "cash", desc: "Cargo ship sails 50% faster & pays 2x cash" },
    { id: "megan", name: "Megan Logistics", role: "Fleet Dispatcher", avatar: "👩‍💼", rarity: "epic", cost: 22000, costType: "cash", desc: "+1 extra truck & auto-unclogs jams" },
    { id: "sophia", name: "Sophia Sterling", role: "CFO / VIP", avatar: "💎", rarity: "legendary", cost: 5, costType: "acorns", desc: "+35% permanent revenue across entire empire" }
];

const ORDER_DEFS = [
    { id: "order_1", title: "Suburban Framing", icon: "🏡", reqPlanks: 25, rewardCoins: 2500, rewardAcorns: 0 },
    { id: "order_2", title: "Waterfront Boardwalk", icon: "⛵", reqPlanks: 60, rewardCoins: 8500, rewardAcorns: 1 },
    { id: "order_3", title: "Railroad Ties", icon: "🚂", reqPlanks: 140, rewardCoins: 24000, rewardAcorns: 2 },
    { id: "order_4", title: "Skyscraper Glulam Beams", icon: "🏙️", reqPlanks: 350, rewardCoins: 85000, rewardAcorns: 4 }
];

const ACHIEVEMENTS = [
    { id: "first_log", name: "First Cut", desc: "Process your first timber log", reward: 200, cond: s => s.stats.logsProcessed >= 1 },
    { id: "lumber_100", name: "Timber Baron", desc: "Process 100 timber logs", reward: 1500, cond: s => s.stats.logsProcessed >= 100 },
    { id: "fleet_ready", name: "Road Master", desc: "Own 3 or more delivery trucks", reward: 3000, cond: s => (s.upgrades.truckCount || 1) >= 3 },
    { id: "jam_buster", name: "Traffic Cop", desc: "Clear 10 traffic gridlocks", reward: 2500, cond: s => s.stats.jamsCleared >= 10 },
    { id: "bulk_shipper", name: "High Seas Trader", desc: "Dispatch the ocean cargo freighter", reward: 5000, cond: s => s.stats.cargoShipped >= 1 },
    { id: "land_owner", name: "Empire Expansion", desc: "Unlock your first land plot", reward: 4000, cond: s => Object.keys(s.expansions || {}).length >= 1 },
    { id: "crew_hired", name: "Dream Team", desc: "Hire 3 or more managers", reward: 6000, cond: s => Object.values(s.managers || {}).filter(m => m > 0).length >= 3 },
    { id: "oak_tier", name: "Hardwood Era", desc: "Reach Oak timber tier", reward: 10000, cond: s => s.woodTier >= 2 },
    { id: "millionaire", name: "Lumber Tycoon", desc: "Earn over 💵 1,000,000 total", reward: 50000, cond: s => s.totalEarned >= 1000000 },
    { id: "golden_rebirth", name: "Golden Harvest", desc: "Rebirth your empire for Golden Acorns", reward: 25000, cond: s => s.prestigeCount >= 1 }
];

// In-World 3D Upgrade Pads (Matching exact positions from 5xpM-hsYo3w.jpg reference)
const WORLD_UPGRADE_PADS = [
    { defId: "sawSpeed", label: "UPGRADE SAWS", icon: "🪚", pos: [-3.8, 0.1, -2.5] },
    { defId: "craneSpeed", label: "UPGRADE CRANE", icon: "🏗️", pos: [3.5, 0.1, -2.5] },
    { defId: "truckCount", label: "EXPAND FLEET", icon: "🚛", pos: [4.2, 0.1, 5.5] },
    { defId: "spawnRate", label: "LUMBERJACK", icon: "🪓", pos: [-3.8, 0.1, 5.5] }
];

// ==========================================
// 2. AUDIO & CHIPTUNE MUSIC ENGINE
// ==========================================
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.sfxEnabled = true;
        this.musicEnabled = true;
        this.sfxGain = null;
        this.musicGain = null;
        this.isPlayingMusic = false;
        this.nextNoteTime = 0;
        this.noteIndex = 0;
        this.melody = [
            261.63, 329.63, 392.00, 523.25, 392.00, 329.63,
            293.66, 349.23, 440.00, 523.25, 440.00, 349.23,
            329.63, 392.00, 523.25, 659.25, 523.25, 392.00,
            293.66, 392.00, 493.88, 587.33, 493.88, 392.00
        ];
    }

    init() {
        if (this.ctx) return;
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        this.ctx = new AudioCtx();
        this.sfxGain = this.ctx.createGain();
        this.sfxGain.gain.value = 0.35;
        this.sfxGain.connect(this.ctx.destination);

        this.musicGain = this.ctx.createGain();
        this.musicGain.gain.value = 0.06;
        this.musicGain.connect(this.ctx.destination);

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
            g.gain.setValueAtTime(0.05, time);
            g.gain.exponentialRampToValueAtTime(0.001, time + dur);
            osc.connect(g);
            g.connect(this.musicGain);
            osc.start(time);
            osc.stop(time + dur);
        } catch(e) {}
    }

    playSfx(type) {
        if (!this.sfxEnabled || !this.ctx) return;
        try {
            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.connect(gain);
            gain.connect(this.sfxGain);

            if (type === 'chop') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(140, now);
                osc.frequency.exponentialRampToValueAtTime(40, now + 0.08);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.08);
                osc.start(now); osc.stop(now + 0.08);
            } else if (type === 'saw') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(320, now);
                osc.frequency.linearRampToValueAtTime(450, now + 0.06);
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.07);
                osc.start(now); osc.stop(now + 0.07);
            } else if (type === 'cash') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(987.77, now);
                osc.frequency.setValueAtTime(1318.51, now + 0.08);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
                osc.start(now); osc.stop(now + 0.25);
            } else if (type === 'honk') {
                osc.type = 'square';
                osc.frequency.setValueAtTime(120, now);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
                osc.start(now); osc.stop(now + 0.5);
            } else if (type === 'click') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(440, now);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.04);
                osc.start(now); osc.stop(now + 0.04);
            } else if (type === 'fanfare') {
                [523.25, 659.25, 783.99, 1046.50].forEach((f, idx) => {
                    const o2 = this.ctx.createOscillator();
                    const g2 = this.ctx.createGain();
                    o2.connect(g2); g2.connect(this.sfxGain);
                    o2.type = 'triangle';
                    o2.frequency.setValueAtTime(f, now + idx * 0.09);
                    g2.gain.setValueAtTime(0.25, now + idx * 0.09);
                    g2.gain.exponentialRampToValueAtTime(0.01, now + idx * 0.09 + 0.2);
                    o2.start(now + idx * 0.09); o2.stop(now + idx * 0.09 + 0.2);
                });
            }
        } catch(e) {}
    }
}
const audio = new SoundEngine();
'''

