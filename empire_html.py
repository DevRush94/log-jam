# -*- coding: utf-8 -*-
HTML_MARKUP = r'''
    <!-- 3D WebGL Canvas & 2D Particle Overlay -->
    <div id="canvas-container">
        <canvas id="webgl-canvas"></canvas>
        <canvas id="overlay-canvas"></canvas>
    </div>

    <!-- Top Header HUD -->
    <header id="top-hud">
        <div class="hud-group">
            <div class="hud-pill cash-pill">
                <span>💵</span>
                <span id="coin-counter">0</span>
            </div>
            <div class="hud-pill acorn-pill">
                <span>🌰</span>
                <span id="acorn-count">0</span>
            </div>
            <div class="hud-pill" id="badge-wood-tier" style="color: #6ee7b7; font-size: 13px;">
                🌲 Pine
            </div>
        </div>

        <div class="hud-group">
            <button class="hud-btn" id="btn-daily" title="Daily Rewards">🎁</button>
            <button class="hud-btn" id="btn-achievements" title="Achievements">🏅</button>
            <button class="hud-btn" id="btn-leaderboard" title="Leaderboard">🌍</button>
            <button class="hud-btn" id="btn-audio-toggle" title="Sound Toggle">🔊</button>
            <button class="hud-btn" id="btn-settings-toggle" title="Settings">⚙️</button>
            <button class="hud-btn" id="btn-user-auth" title="Cloud Account">👤</button>
        </div>
    </header>

    <!-- Cinematic Zone Navigation Bar (Camera Switcher) -->
    <nav id="zone-nav-bar">
        <button class="zone-pill active" data-zone="overview">🌍 Overview</button>
        <button class="zone-pill" data-zone="forest">🌲 Forest Camp</button>
        <button class="zone-pill" data-zone="sawmill">🪚 Sawmill Plant</button>
        <button class="zone-pill" data-zone="yard">📦 Stacking Yard</button>
        <button class="zone-pill" data-zone="harbor">🚢 Cargo Harbor</button>
        <button class="zone-pill" data-zone="highway">🚛 Express Highway</button>
        <button class="zone-pill" data-zone="hq">🏢 Empire HQ</button>
    </nav>

    <!-- Quick Action / Jam Floating Banner -->
    <div id="quick-action-bar">
        <div class="action-banner" id="banner-quick-action" style="display: none;">
            <span>🚨</span>
            <span id="banner-action-text">Traffic Jam! Tap trucks to clear!</span>
        </div>
    </div>

    <!-- Toast Notifications -->
    <div id="toast-container"></div>

    <!-- Bottom Navigation Dock -->
    <div id="bottom-dock">
        <button class="dock-tab" data-modal="modal-expansion">
            <span class="tab-icon">🏭</span>
            <span class="tab-label">Land</span>
        </button>
        <button class="dock-tab" data-modal="modal-managers">
            <span class="tab-icon">👷</span>
            <span class="tab-label">Crew</span>
            <span class="tab-badge" id="badge-crew-dot" style="display: none;">!</span>
        </button>
        <button class="dock-tab" data-modal="modal-orders">
            <span class="tab-icon">📋</span>
            <span class="tab-label">Orders</span>
            <span class="tab-badge" id="badge-orders-dot" style="display: none;">1</span>
        </button>
        <button class="dock-tab" data-modal="modal-analytics">
            <span class="tab-icon">📊</span>
            <span class="tab-label">Stats</span>
        </button>
        <button class="dock-tab active" data-modal="modal-upgrades">
            <span class="tab-icon">🛍️</span>
            <span class="tab-label">Shop</span>
        </button>
        <button class="dock-tab" data-modal="modal-prestige">
            <span class="tab-icon">🏆</span>
            <span class="tab-label">Empire</span>
        </button>
    </div>

    <!-- SCREEN 1: Factory Expansions & Land Plots Modal -->
    <div class="modal-overlay" id="modal-expansion">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">🏭 Empire Land Expansions</div>
                <button class="modal-close" data-close="modal-expansion">✕</button>
            </div>
            <div class="modal-body">
                <p style="font-size: 13px; color: var(--text-sub);">
                    Acquire industrial sectors and natural timber reserves to expand your factory territory and permanently boost capacity.
                </p>
                <div class="expansion-grid" id="expansion-list-container">
                    <!-- Dynamic Expansion Cards -->
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 2: Managers & Crew Modal -->
    <div class="modal-overlay" id="modal-managers">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">👷 Crew & Operations Managers</div>
                <button class="modal-close" data-close="modal-managers">✕</button>
            </div>
            <div class="modal-body">
                <p style="font-size: 13px; color: var(--text-sub);">
                    Hire and promote expert foremen, master sawyers, crane operators, and dispatchers to automate and supercharge production!
                </p>
                <div class="managers-grid" id="managers-list-container">
                    <!-- Dynamic Manager Cards -->
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 3: Commercial Orders & Contracts Modal -->
    <div class="modal-overlay" id="modal-orders">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">📋 Commercial Orders & Contracts</div>
                <button class="modal-close" data-close="modal-orders">✕</button>
            </div>
            <div class="modal-body">
                <p style="font-size: 13px; color: var(--text-sub);">
                    Deliver timber bundles to multinational construction contracts for massive Cash payouts and rare Golden Acorns!
                </p>
                <div style="display: flex; flex-direction: column; gap: 12px;" id="orders-list-container">
                    <!-- Dynamic Orders Cards -->
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 4: Factory Analytics & Bottlenecks Modal -->
    <div class="modal-overlay" id="modal-analytics">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">📊 Factory Analytics & Bottlenecks</div>
                <button class="modal-close" data-close="modal-analytics">✕</button>
            </div>
            <div class="modal-body">
                <div class="bottleneck-box optimal" id="bottleneck-status-box">
                    <div style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 14px;">
                        <span id="bottleneck-icon">⚡</span>
                        <span id="bottleneck-headline">Optimal Throughput</span>
                    </div>
                    <div style="font-size: 12px; line-height: 1.4;" id="bottleneck-detail">
                        All mill lines and logistics are running in equilibrium.
                    </div>
                    <button class="btn-full btn-secondary" id="btn-fix-bottleneck" style="display: none; padding: 6px; font-size: 12px; margin-top: 4px;">
                        Quick Fix: Upgrade Saws
                    </button>
                </div>

                <div class="analytics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Forest Harvest Rate</div>
                        <div class="metric-val" id="metric-harvest-rate">0 logs/m</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Sawmill Throughput</div>
                        <div class="metric-val" id="metric-saw-rate">0 p/m</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Lumber Yard Fill</div>
                        <div class="metric-val" id="metric-yard-fill">0 / 60</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Cash Output Rate</div>
                        <div class="metric-val" id="metric-revenue-rate">💵 0 /m</div>
                    </div>
                </div>

                <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--panel-border); border-radius: 14px; padding: 14px; font-size: 12px; color: var(--text-sub);">
                    <div style="font-weight: 700; color: #fff; margin-bottom: 6px;">💡 Tycoon Pro Tip</div>
                    Balancing tree harvesting with saw speed prevents conveyor starvation, while upgrading the highway keeps your timber stacks from hitting warehouse capacity limits!
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 5: Machinery Upgrades Shop Modal -->
    <div class="modal-overlay" id="modal-upgrades">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">🛍️ Machinery Upgrades</div>
                <button class="modal-close" data-close="modal-upgrades">✕</button>
            </div>
            <div class="modal-body">
                <div class="shop-mult-row">
                    <span style="font-size: 13px; font-weight: 700; color: var(--text-sub);">Buy Multiplier:</span>
                    <div class="mult-tabs">
                        <button class="mult-tab active" data-mult="1">1x</button>
                        <button class="mult-tab" data-mult="10">10x</button>
                        <button class="mult-tab" data-mult="max">MAX</button>
                    </div>
                </div>
                <div class="shop-list" id="shop-items-container">
                    <!-- Dynamic Upgrade Cards -->
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 6: Prestige & Empire Rebirth Modal -->
    <div class="modal-overlay" id="modal-prestige">
        <div class="modal-card" style="text-align: center;">
            <div class="modal-header">
                <div class="modal-title">🏆 Empire Franchise & Rebirth</div>
                <button class="modal-close" data-close="modal-prestige">✕</button>
            </div>
            <div class="modal-body" style="align-items: center;">
                <div style="font-size: 48px; margin: 6px 0;">🌰</div>
                <h3 style="font-size: 18px; font-weight: 800;">Sell Empire for Golden Acorns</h3>
                <p style="font-size: 13px; color: var(--text-sub); max-width: 400px; line-height: 1.4;">
                    Liquidate your current sawmill to international timber investors. Each Golden Acorn grants a permanent <strong>+5% revenue multiplier</strong> across all wood tiers!
                </p>

                <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 16px; padding: 14px; width: 100%; max-width: 420px; margin: 8px 0;">
                    <div style="font-size: 12px; color: var(--text-sub); text-transform: uppercase;">Acorns Gained on Rebirth</div>
                    <div style="font-size: 32px; font-weight: 900; color: var(--gold); margin: 4px 0;" id="prestige-gain-val">+0 🌰</div>
                    <div style="font-size: 12px; color: #34d399;" id="prestige-boost-val">Current boost: +0% revenue</div>
                </div>

                <button class="btn-full btn-primary" id="btn-prestige-confirm" style="background: linear-gradient(135deg, #f59e0b, #d97706); max-width: 420px;">
                    Claim Acorns & Expand Empire
                </button>
            </div>
        </div>
    </div>

    <!-- SCREEN 7: Achievements Modal -->
    <div class="modal-overlay" id="modal-achievements">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">🏅 Milestones & Achievements</div>
                <button class="modal-close" data-close="modal-achievements">✕</button>
            </div>
            <div class="modal-body" id="achievements-list-container">
                <!-- Dynamic Achievement Cards -->
            </div>
        </div>
    </div>

    <!-- SCREEN 8: Cloud Leaderboard Modal -->
    <div class="modal-overlay" id="modal-leaderboard">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">🌍 Global Tycoon Leaderboard</div>
                <button class="modal-close" data-close="modal-leaderboard">✕</button>
            </div>
            <div class="modal-body">
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: var(--text-sub); padding-bottom: 6px; border-bottom: 1px solid var(--panel-border);">
                    <span>RANK & TYCOON</span>
                    <span>NET WORTH</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 8px;" id="leaderboard-list-container">
                    <div style="text-align: center; padding: 20px; color: var(--text-sub);">Loading global ranks from Xperia Cloud...</div>
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 9: Daily Rewards Modal -->
    <div class="modal-overlay" id="modal-daily">
        <div class="modal-card" style="text-align: center;">
            <div class="modal-header">
                <div class="modal-title">🎁 Daily Login Streak</div>
                <button class="modal-close" data-close="modal-daily">✕</button>
            </div>
            <div class="modal-body" style="align-items: center;">
                <div style="font-size: 40px; margin: 4px 0;">📦</div>
                <h4 style="font-size: 16px;">Day <span id="daily-day-num">1</span> Streak Reward!</h4>
                <div style="font-size: 26px; font-weight: 900; color: #10b981; margin: 8px 0;" id="daily-reward-val">+💵 1,000</div>
                <button class="btn-full btn-primary" id="btn-claim-daily" style="max-width: 320px;">Open Reward Chest</button>
            </div>
        </div>
    </div>

    <!-- SCREEN 10: Settings Modal -->
    <div class="modal-overlay" id="modal-settings">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">⚙️ Game Settings</div>
                <button class="modal-close" data-close="modal-settings">✕</button>
            </div>
            <div class="modal-body">
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
                    <span style="font-weight: 700;">Sound Effects (SFX)</span>
                    <button class="btn-secondary" id="toggle-sfx" style="padding: 6px 14px; border-radius: 8px;">SFX: ON</button>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
                    <span style="font-weight: 700;">Chiptune Music</span>
                    <button class="btn-secondary" id="toggle-music" style="padding: 6px 14px; border-radius: 8px;">Music: ON</button>
                </div>
                <div style="padding: 8px 0;">
                    <label style="font-size: 12px; color: var(--text-sub); display: block; margin-bottom: 4px;">Cloud Backend API Endpoint</label>
                    <input type="text" id="setting-server-url" style="width: 100%; padding: 10px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid var(--panel-border); color: #fff; font-size: 13px;">
                </div>
                <div style="display: flex; gap: 8px; margin-top: 10px;">
                    <button class="btn-full btn-secondary" id="btn-save-settings">Save & Sync</button>
                    <button class="btn-full" id="btn-reset-game" style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);">Reset Save</button>
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 11: Cloud Auth Modal -->
    <div class="modal-overlay" id="modal-auth">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">👤 Xperia Cloud Sync</div>
                <button class="modal-close" data-close="modal-auth">✕</button>
            </div>
            <div class="modal-body">
                <p style="font-size: 13px; color: var(--text-sub);">
                    Sync your tycoon progress across devices directly to the Xperia phone backend!
                </p>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <input type="text" id="auth-username" placeholder="Tycoon Username" style="padding: 10px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid var(--panel-border); color: #fff;">
                    <input type="password" id="auth-password" placeholder="Password" style="padding: 10px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid var(--panel-border); color: #fff;">
                </div>
                <div style="display: flex; gap: 8px; margin-top: 6px;">
                    <button class="btn-full btn-primary" id="btn-login-cloud">Log In</button>
                    <button class="btn-full btn-secondary" id="btn-register-cloud">Register</button>
                </div>
                <div style="font-size: 12px; color: #34d399; text-align: center;" id="auth-status-msg"></div>
            </div>
        </div>
    </div>

    <!-- SCREEN 12: Welcome Back / Offline Earnings Modal -->
    <div class="modal-overlay" id="modal-welcome">
        <div class="modal-card" style="text-align: center;">
            <div style="font-size: 46px; margin: 12px 0 6px;">🎉</div>
            <div class="modal-title" style="justify-content: center; font-size: 20px;">Welcome Back, Tycoon!</div>
            <p style="font-size: 13px; color: var(--text-sub); margin: 6px 0 14px;">
                While you were away, your mill and lumberjacks kept processing timber!
            </p>
            <div style="font-size: 32px; font-weight: 900; color: #10b981; margin-bottom: 16px;">
                +💵 <span id="offline-earned-val">0</span>
            </div>
            <button class="btn-full btn-primary" id="btn-claim-offline" style="max-width: 320px; margin: 0 auto 12px;">Collect Cash</button>
        </div>
    </div>

    <!-- Start / Splash Screen -->
    <div id="start-screen">
        <div style="font-size: 64px; animation: bounce 1.5s infinite alternate ease-in-out;">🪵</div>
        <h1 style="font-size: 32px; font-weight: 900; letter-spacing: -0.5px; background: linear-gradient(135deg, #10b981, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            LOG JAM: 3D LUMBER EMPIRE
        </h1>
        <p style="font-size: 14px; color: var(--text-sub); max-width: 360px; line-height: 1.5;">
            Build a massive timber empire across vast forests, multi-blade sawmills, skyscraper storage yards, cargo harbors, and express highways!
        </p>
        <button class="btn-full btn-primary" id="btn-start-game" style="max-width: 280px; font-size: 17px; padding: 14px;">
            START PLAYING ▶
        </button>
    </div>
'''
