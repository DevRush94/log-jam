# -*- coding: utf-8 -*-
"""
Generator script for index.html with completely revamped UI,
intuitive station inspector, live upgrade event listeners, category tabs,
tactile tycoon design, and full backend integration.
"""

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Log Jam: Mill Empire</title>
    <style>
        :root {
            --bg-dark: #0f131c;
            --panel-bg: rgba(20, 25, 37, 0.95);
            --panel-border: rgba(255, 255, 255, 0.12);
            --gold: #ffcf33;
            --gold-glow: rgba(255, 207, 51, 0.45);
            --gold-dark: #b38600;
            --wood-bark: #4a2f1b;
            --wood-mid: #85532a;
            --wood-light: #d69854;
            --wood-board: #613b1f;
            --emerald: #38a169;
            --emerald-hover: #48bb78;
            --emerald-glow: rgba(72, 187, 120, 0.5);
            --ruby: #e53e3e;
            --blue: #3182ce;
            --purple: #805ad5;
            --text-main: #f7fafc;
            --text-sub: #a0aec0;
            --text-muted: #718096;
            --font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: var(--bg-dark);
            font-family: var(--font-family);
            color: var(--text-main);
        }

        #game-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            display: flex;
            overflow: hidden;
        }

        /* Canvas Viewport */
        #canvas-wrapper {
            position: relative;
            flex: 1;
            height: 100%;
            overflow: hidden;
            cursor: pointer;
        }

        canvas {
            display: block;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }

        #bg-canvas { z-index: 1; }
        #main-canvas { z-index: 2; }
        #ui-canvas { z-index: 3; pointer-events: none; }

        /* Top HUD Bar */
        .hud-top {
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            z-index: 10;
            pointer-events: none;
            gap: 10px;
        }

        .hud-left-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            pointer-events: auto;
        }

        .hud-pill-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            align-items: center;
        }

        /* Wood Tier Banner with Progress */
        .wood-tier-banner {
            background: linear-gradient(135deg, #7a4620, #4d2b12);
            border: 2px solid var(--wood-light);
            box-shadow: 0 4px 14px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.25);
            border-radius: 14px;
            padding: 6px 12px;
            display: flex;
            flex-direction: column;
            gap: 3px;
            min-width: 180px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .wood-tier-banner:hover {
            transform: translateY(-2px);
        }
        .wood-tier-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            font-weight: 800;
            color: #ffe082;
            text-shadow: 0 1px 3px rgba(0,0,0,0.7);
        }
        .wood-mult-badge {
            background: rgba(0,0,0,0.35);
            padding: 1px 6px;
            border-radius: 8px;
            font-size: 11px;
            color: var(--gold);
        }
        .wood-progress-track {
            width: 100%;
            height: 6px;
            background: rgba(0,0,0,0.45);
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .wood-progress-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #f6ad55, #ecc94b);
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        .wood-next-label {
            font-size: 10px;
            color: rgba(255,255,255,0.75);
            font-weight: 600;
        }

        .hud-badge {
            background: rgba(18, 22, 33, 0.9);
            border: 1px solid var(--panel-border);
            padding: 6px 12px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            font-weight: 800;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
        }
        .hud-badge:hover {
            transform: translateY(-2px);
            background: rgba(28, 35, 52, 0.95);
        }

        .hud-badge.acorns {
            color: var(--gold);
            border-color: rgba(255, 207, 51, 0.4);
            box-shadow: 0 4px 14px rgba(255, 207, 51, 0.15);
        }
        .hud-badge.leaderboard {
            color: #ffe082;
            border-color: rgba(255, 224, 130, 0.4);
        }
        .hud-badge.sync-status {
            font-size: 11px;
            font-weight: 600;
            color: var(--text-sub);
            cursor: default;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #48bb78;
            box-shadow: 0 0 6px #48bb78;
        }
        .status-dot.syncing {
            background: #ecc94b;
            box-shadow: 0 0 6px #ecc94b;
            animation: pulse-dot 1s infinite;
        }
        .status-dot.offline {
            background: #f56565;
            box-shadow: 0 0 6px #f56565;
        }
        @keyframes pulse-dot {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.6; }
        }

        /* Top Right Coin Bank */
        .hud-coin-box {
            background: linear-gradient(135deg, rgba(22, 28, 44, 0.95), rgba(13, 17, 27, 0.95));
            border: 2px solid var(--gold);
            border-radius: 16px;
            padding: 8px 18px;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            backdrop-filter: blur(10px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.5), 0 0 16px rgba(255, 207, 51, 0.25);
            pointer-events: auto;
            min-width: 160px;
            transition: transform 0.12s ease;
        }
        .hud-coin-box.bounce {
            transform: scale(1.08);
        }
        .coin-val {
            font-size: 24px;
            font-weight: 900;
            color: var(--gold);
            display: flex;
            align-items: center;
            gap: 6px;
            letter-spacing: 0.5px;
            text-shadow: 0 2px 8px rgba(255, 207, 51, 0.4);
        }
        .income-rate {
            font-size: 12px;
            font-weight: 700;
            color: #68d391;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* Station Inspector Card (Tap anywhere on machine to open) */
        #station-inspector {
            position: absolute;
            top: 76px;
            left: 50%;
            transform: translateX(-50%) translateY(-150%);
            background: rgba(18, 24, 38, 0.95);
            border: 2px solid var(--gold);
            border-radius: 16px;
            padding: 12px 18px;
            display: flex;
            align-items: center;
            gap: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6), 0 0 20px rgba(255, 207, 51, 0.2);
            z-index: 25;
            backdrop-filter: blur(12px);
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            max-width: 90vw;
        }
        #station-inspector.show {
            transform: translateX(-50%) translateY(0);
        }
        .inspector-icon {
            font-size: 28px;
            background: rgba(255, 207, 51, 0.12);
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--gold-glow);
        }
        .inspector-details {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .inspector-title {
            font-size: 15px;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .inspector-status {
            font-size: 11px;
            font-weight: 700;
            color: #68d391;
        }
        .inspector-status.bottleneck {
            color: #fc8181;
            animation: pulse-dot 1s infinite;
        }
        .inspector-stats {
            font-size: 11px;
            color: var(--text-sub);
        }
        .inspector-btn-quick-buy {
            background: linear-gradient(135deg, var(--emerald), var(--emerald-hover));
            border: none;
            color: #fff;
            padding: 8px 14px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 4px 10px var(--emerald-glow);
            white-space: nowrap;
            transition: transform 0.15s;
        }
        .inspector-btn-quick-buy:hover {
            transform: translateY(-2px);
        }
        .inspector-close-btn {
            background: none;
            border: none;
            color: var(--text-sub);
            font-size: 20px;
            cursor: pointer;
            padding: 4px;
        }
        .inspector-close-btn:hover { color: #fff; }

        /* Celebratory Event / Milestone Banner */
        #event-banner {
            position: absolute;
            top: 70px;
            left: 50%;
            transform: translateX(-50%) translateY(-140px);
            background: linear-gradient(135deg, #ff7e5f, #feb47b);
            color: #fff;
            padding: 10px 24px;
            border-radius: 30px;
            font-size: 15px;
            font-weight: 900;
            box-shadow: 0 8px 30px rgba(255, 126, 95, 0.6);
            z-index: 30;
            pointer-events: none;
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.4);
        }
        #event-banner.show {
            transform: translateX(-50%) translateY(0);
        }

        /* Action Pill Bar (Bottom Left) */
        .action-pills {
            position: absolute;
            bottom: 14px;
            left: 14px;
            display: flex;
            gap: 8px;
            z-index: 10;
            flex-wrap: wrap;
        }

        .pill-btn {
            background: linear-gradient(135deg, rgba(26, 32, 48, 0.9), rgba(18, 22, 33, 0.95));
            border: 1px solid var(--panel-border);
            color: var(--text-main);
            padding: 9px 14px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            transition: all 0.2s ease;
            position: relative;
        }
        .pill-btn:hover {
            transform: translateY(-2px);
            border-color: rgba(255,255,255,0.35);
            background: rgba(35, 43, 64, 0.95);
        }
        .pill-btn:active {
            transform: translateY(1px);
        }
        .pill-btn.boost-btn {
            background: linear-gradient(135deg, #e53e3e, #dd6b20);
            border: none;
            color: #fff;
            box-shadow: 0 4px 15px rgba(229, 62, 62, 0.5);
        }
        .pill-badge-alert {
            position: absolute;
            top: -5px;
            right: -5px;
            background: #e53e3e;
            color: #fff;
            font-size: 10px;
            font-weight: 900;
            border-radius: 10px;
            padding: 2px 6px;
            border: 2px solid var(--bg-dark);
            animation: pulse-dot 1.5s infinite;
        }

        /* Desktop Sidebar & Mobile Bottom Sheet */
        #shop-panel {
            width: 410px;
            height: 100%;
            background: var(--panel-bg);
            border-left: 1px solid var(--panel-border);
            display: flex;
            flex-direction: column;
            z-index: 20;
            box-shadow: -8px 0 30px rgba(0,0,0,0.5);
            backdrop-filter: blur(14px);
            transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        }

        .shop-header {
            padding: 14px 18px 10px;
            border-bottom: 1px solid var(--panel-border);
            display: flex;
            flex-direction: column;
            gap: 10px;
            background: rgba(14, 18, 27, 0.6);
        }

        .shop-title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .shop-title {
            font-size: 17px;
            font-weight: 900;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #ffe082;
            letter-spacing: 0.3px;
        }

        .buy-mult-toggle {
            display: flex;
            background: rgba(0,0,0,0.4);
            border-radius: 14px;
            padding: 2px;
            border: 1px solid var(--panel-border);
        }

        .mult-btn {
            background: none;
            border: none;
            color: var(--text-sub);
            padding: 5px 12px;
            font-size: 11px;
            font-weight: 800;
            cursor: pointer;
            border-radius: 12px;
            transition: all 0.2s ease;
        }

        .mult-btn.active {
            background: linear-gradient(135deg, var(--emerald), var(--emerald-hover));
            color: #fff;
            box-shadow: 0 2px 8px var(--emerald-glow);
        }

        /* Shop Category Filter Tabs */
        .category-tabs {
            display: flex;
            gap: 6px;
            overflow-x: auto;
            padding-bottom: 2px;
        }
        .category-tabs::-webkit-scrollbar {
            display: none;
        }
        .cat-tab {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            color: var(--text-sub);
            padding: 5px 10px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .cat-tab:hover {
            color: #fff;
            background: rgba(255,255,255,0.12);
        }
        .cat-tab.active {
            background: var(--gold);
            color: #11151f;
            border-color: var(--gold);
            font-weight: 800;
            box-shadow: 0 2px 8px var(--gold-glow);
        }

        .shop-list {
            flex: 1;
            overflow-y: auto;
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .shop-list::-webkit-scrollbar {
            width: 6px;
        }
        .shop-list::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.15);
            border-radius: 3px;
        }

        /* 3D Tactile Tycoon Upgrade Card */
        .upgrade-card {
            background: linear-gradient(135deg, rgba(32, 39, 58, 0.75), rgba(20, 25, 38, 0.85));
            border: 1px solid var(--panel-border);
            border-radius: 14px;
            padding: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        .upgrade-card:hover {
            border-color: rgba(255,255,255,0.25);
            box-shadow: 0 6px 16px rgba(0,0,0,0.45);
        }
        .upgrade-card.can-buy {
            border-color: rgba(72, 187, 120, 0.45);
            box-shadow: 0 4px 16px rgba(72, 187, 120, 0.15);
        }
        .upgrade-card.shake {
            animation: shake 0.4s ease-in-out;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-6px); }
            40%, 80% { transform: translateX(6px); }
        }

        .upgrade-icon-box {
            font-size: 26px;
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: rgba(0,0,0,0.35);
            border: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .upgrade-info {
            flex: 1;
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }

        .upgrade-title-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
        }

        .upgrade-name {
            font-size: 13px;
            font-weight: 800;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .upgrade-level-tag {
            font-size: 11px;
            font-weight: 800;
            color: var(--gold);
            background: rgba(255,207,51,0.15);
            border: 1px solid rgba(255,207,51,0.3);
            padding: 1px 6px;
            border-radius: 8px;
            white-space: nowrap;
        }

        /* Milestone Bar */
        .milestone-bar-wrap {
            display: flex;
            flex-direction: column;
            gap: 2px;
            margin: 2px 0;
        }
        .milestone-track {
            width: 100%;
            height: 5px;
            background: rgba(0,0,0,0.4);
            border-radius: 3px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.06);
        }
        .milestone-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #48bb78, #ecc94b);
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        .milestone-sub {
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: var(--text-sub);
            font-weight: 600;
        }
        .milestone-bonus {
            color: var(--gold);
            font-weight: 700;
        }

        .upgrade-stat-row {
            font-size: 11px;
            color: #68d391;
            font-weight: 600;
        }

        /* 3D Tactile Buy Button */
        .buy-btn {
            position: relative;
            background: linear-gradient(180deg, #38a169 0%, #276749 100%);
            border: none;
            color: #fff;
            padding: 8px 12px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 900;
            cursor: pointer;
            box-shadow: 0 4px 0 #1c4934, 0 6px 14px rgba(0,0,0,0.4);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-width: 90px;
            transition: transform 0.1s ease, box-shadow 0.1s ease, filter 0.15s ease;
            flex-shrink: 0;
        }
        .buy-btn:active {
            transform: translateY(3px);
            box-shadow: 0 1px 0 #1c4934, 0 2px 6px rgba(0,0,0,0.4);
        }
        .buy-btn.can-buy {
            background: linear-gradient(180deg, #48bb78 0%, #2f855a 100%);
            box-shadow: 0 4px 0 #22543d, 0 6px 14px var(--emerald-glow);
            animation: pulse-emerald 2s infinite;
        }
        @keyframes pulse-emerald {
            0%, 100% { box-shadow: 0 4px 0 #22543d, 0 6px 14px var(--emerald-glow); }
            50% { box-shadow: 0 4px 0 #22543d, 0 8px 22px rgba(72, 187, 120, 0.85); }
        }
        .buy-btn.disabled {
            background: #232a3b;
            color: #64748b;
            cursor: pointer;
            box-shadow: 0 3px 0 #141824;
            opacity: 0.75;
            animation: none;
        }
        .buy-btn.disabled:active {
            transform: translateY(2px);
            box-shadow: 0 1px 0 #141824;
        }
        .buy-btn.maxed {
            background: linear-gradient(180deg, #d69e2e, #b7791f);
            color: #fff;
            box-shadow: 0 4px 0 #744210;
            cursor: default;
        }
        .buy-btn-level {
            font-size: 11px;
            opacity: 0.9;
        }
        .buy-btn-cost {
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 3px;
        }
        .buy-btn-need {
            font-size: 9px;
            color: #fca5a5;
            font-weight: 600;
        }

        /* Mobile Bottom Sheet & Overlay */
        #shop-toggle-mobile {
            display: none;
            position: absolute;
            bottom: 14px;
            right: 14px;
            background: linear-gradient(135deg, var(--gold), #f6ad55);
            color: #1a1e29;
            border: none;
            padding: 11px 20px;
            border-radius: 26px;
            font-weight: 900;
            font-size: 14px;
            box-shadow: 0 6px 20px var(--gold-glow);
            z-index: 10;
            cursor: pointer;
            transition: transform 0.2s;
        }
        #shop-toggle-mobile:hover {
            transform: scale(1.05);
        }

        /* Modals */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.78);
            backdrop-filter: blur(10px);
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }

        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .modal-card {
            background: linear-gradient(135deg, #1b2130, #131722);
            border: 1px solid var(--panel-border);
            border-radius: 22px;
            width: 100%;
            max-width: 460px;
            max-height: 85vh;
            overflow-y: auto;
            padding: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.7), 0 0 25px rgba(255,207,51,0.15);
            display: flex;
            flex-direction: column;
            gap: 16px;
            position: relative;
            transform: scale(0.92);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .modal-overlay.active .modal-card {
            transform: scale(1);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-title {
            font-size: 20px;
            font-weight: 900;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #ffe082;
        }

        .close-btn {
            background: none;
            border: none;
            color: var(--text-sub);
            font-size: 24px;
            cursor: pointer;
            padding: 4px;
        }
        .close-btn:hover { color: #fff; }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .input-group label {
            font-size: 11px;
            font-weight: 800;
            color: var(--text-sub);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .input-wrap {
            position: relative;
            display: flex;
            align-items: center;
        }

        .input-field {
            width: 100%;
            background: rgba(0,0,0,0.35);
            border: 1px solid var(--panel-border);
            border-radius: 12px;
            padding: 12px 14px;
            color: #fff;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }

        .input-field:focus {
            border-color: var(--gold);
        }

        .pwd-toggle {
            position: absolute;
            right: 12px;
            background: none;
            border: none;
            color: var(--text-sub);
            cursor: pointer;
            font-size: 14px;
        }

        .modal-btn-row {
            display: flex;
            gap: 10px;
            margin-top: 6px;
        }

        .btn-full {
            flex: 1;
            padding: 12px;
            border-radius: 12px;
            font-weight: 900;
            font-size: 14px;
            cursor: pointer;
            border: none;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--gold), #f6ad55);
            color: #11151f;
            box-shadow: 0 4px 15px var(--gold-glow);
        }
        .btn-primary:hover {
            filter: brightness(1.1);
            transform: translateY(-2px);
        }

        .btn-secondary {
            background: rgba(255,255,255,0.08);
            color: #fff;
            border: 1px solid var(--panel-border);
        }
        .btn-secondary:hover {
            background: rgba(255,255,255,0.16);
        }

        .btn-danger {
            background: rgba(245, 101, 101, 0.2);
            color: var(--ruby);
            border: 1px solid rgba(245, 101, 101, 0.4);
        }
        .btn-danger:hover {
            background: rgba(245, 101, 101, 0.35);
        }

        .inline-msg {
            font-size: 13px;
            padding: 8px 12px;
            border-radius: 8px;
            display: none;
        }
        .inline-msg.error {
            display: block;
            background: rgba(245, 101, 101, 0.15);
            color: #fc8181;
            border: 1px solid rgba(245, 101, 101, 0.3);
        }
        .inline-msg.success {
            display: block;
            background: rgba(72, 187, 120, 0.15);
            color: #68d391;
            border: 1px solid rgba(72, 187, 120, 0.3);
        }

        /* Leaderboard Modal Table */
        .leaderboard-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
            max-height: 50vh;
            overflow-y: auto;
            margin: 6px 0;
        }
        .leader-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 12px;
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            font-size: 13px;
        }
        .leader-row.me {
            border-color: var(--gold);
            background: rgba(255, 207, 51, 0.12);
        }
        .leader-rank {
            font-weight: 900;
            width: 32px;
        }
        .leader-name {
            flex: 1;
            font-weight: 800;
            color: #fff;
        }
        .leader-score {
            font-weight: 900;
            color: var(--gold);
        }

        /* Achievements Modal List */
        .achievements-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            max-height: 55vh;
            overflow-y: auto;
        }
        .ach-card {
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 10px 12px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .ach-card.completed {
            border-color: rgba(72, 187, 120, 0.4);
            background: rgba(72, 187, 120, 0.08);
        }
        .ach-icon {
            font-size: 26px;
        }
        .ach-info {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .ach-title {
            font-size: 13px;
            font-weight: 800;
            color: #fff;
        }
        .ach-desc {
            font-size: 11px;
            color: var(--text-sub);
        }
        .ach-reward {
            font-size: 11px;
            font-weight: 800;
            color: var(--gold);
        }
        .ach-status-badge {
            font-size: 11px;
            font-weight: 800;
            padding: 4px 8px;
            border-radius: 8px;
            background: rgba(255,255,255,0.08);
            color: var(--text-sub);
        }
        .ach-status-badge.claimed {
            background: #276749;
            color: #9ae6b4;
        }

        /* 7-Day Daily Chest Streak Layout */
        .daily-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin: 12px 0;
        }
        .daily-day-card {
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 10px 4px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            font-size: 11px;
        }
        .daily-day-card.claimed {
            border-color: #38a169;
            background: rgba(56, 161, 105, 0.15);
        }
        .daily-day-card.today {
            border-color: var(--gold);
            background: rgba(255, 207, 51, 0.15);
            animation: pulse-emerald 2s infinite;
        }
        .daily-day-card.mega {
            grid-column: span 2;
            background: linear-gradient(135deg, rgba(255,207,51,0.2), rgba(221,107,32,0.2));
            border-color: var(--gold);
        }

        /* Start Screen */
        #start-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: radial-gradient(circle at center, #232c3f 0%, #0d111a 100%);
            z-index: 200;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px;
            transition: opacity 0.5s ease;
        }

        #start-screen.hidden {
            opacity: 0;
            pointer-events: none;
        }

        .logo-box {
            text-align: center;
            margin-bottom: 36px;
        }

        .logo-main {
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(135deg, #ffe082 0%, #ffb300 50%, #d77618 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 8px 30px rgba(255, 179, 0, 0.4);
            letter-spacing: -1px;
            margin-bottom: 6px;
        }

        .logo-sub {
            font-size: 16px;
            font-weight: 800;
            color: #a0aec0;
            letter-spacing: 4px;
            text-transform: uppercase;
        }

        .start-btn-box {
            display: flex;
            flex-direction: column;
            gap: 14px;
            width: 100%;
            max-width: 330px;
        }

        .btn-huge {
            padding: 16px 24px;
            border-radius: 18px;
            font-size: 16px;
            font-weight: 900;
            cursor: pointer;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: all 0.25s ease;
        }

        .btn-huge.guest {
            background: linear-gradient(135deg, #48bb78, #2f855a);
            color: #fff;
            box-shadow: 0 6px 25px rgba(72, 187, 120, 0.45);
        }
        .btn-huge.guest:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 35px rgba(72, 187, 120, 0.65);
        }

        .btn-huge.auth {
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
            border: 1px solid var(--panel-border);
        }
        .btn-huge.auth:hover {
            background: rgba(255, 255, 255, 0.16);
            transform: translateY(-2px);
        }

        /* Achievements Toast */
        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: rgba(20, 26, 40, 0.96);
            border: 2px solid var(--gold);
            border-radius: 30px;
            padding: 10px 24px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #fff;
            font-weight: 800;
            font-size: 14px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.6), 0 0 20px var(--gold-glow);
            z-index: 150;
            pointer-events: none;
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .toast.show {
            transform: translateX(-50%) translateY(0);
        }

        /* Tutorial Toast */
        #tutorial-toast {
            position: absolute;
            bottom: 78px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(18, 24, 38, 0.95);
            border: 1px solid var(--gold);
            border-radius: 16px;
            padding: 10px 22px;
            font-size: 13px;
            font-weight: 800;
            color: var(--gold);
            z-index: 12;
            pointer-events: none;
            box-shadow: 0 6px 25px rgba(0,0,0,0.6);
            animation: bounce 1.8s infinite;
            white-space: nowrap;
        }

        @keyframes bounce {
            0%, 100% { transform: translateX(-50%) translateY(0); }
            50% { transform: translateX(-50%) translateY(-6px); }
        }

        /* Responsive Breakpoints */
        @media (max-width: 820px) {
            #shop-panel {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 62vh;
                border-left: none;
                border-top: 2px solid var(--panel-border);
                transform: translateY(100%);
            }
            #shop-panel.open {
                transform: translateY(0);
            }
            #shop-toggle-mobile {
                display: block;
            }
            .hud-top {
                flex-direction: column;
                align-items: stretch;
            }
            .hud-coin-box {
                align-self: flex-end;
            }
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- Layered Canvases -->
    <div id="canvas-wrapper">
        <canvas id="bg-canvas"></canvas>
        <canvas id="main-canvas"></canvas>
        <canvas id="ui-canvas"></canvas>

        <!-- Top HUD -->
        <div class="hud-top">
            <div class="hud-left-group">
                <div class="hud-pill-row">
                    <!-- Wood Tier Banner with Progress Bar -->
                    <div class="wood-tier-banner" id="btn-wood-tier" title="Click to view wood tiers">
                        <div class="wood-tier-header">
                            <span id="badge-tier-name">🪵 Pine Mill</span>
                            <span class="wood-mult-badge" id="badge-tier-mult">x1.0 Value</span>
                        </div>
                        <div class="wood-progress-track">
                            <div class="wood-progress-fill" id="wood-tier-fill"></div>
                        </div>
                        <div class="wood-next-label" id="wood-next-label">Next: Oak Wood (2.5K coins)</div>
                    </div>

                    <!-- Golden Acorns Counter -->
                    <div class="hud-badge acorns" id="badge-acorns" title="Golden Acorns from Forest Resets">
                        🌰 <span id="acorn-count">0</span>
                    </div>

                    <!-- Leaderboard Trophy Button -->
                    <div class="hud-badge leaderboard" id="btn-open-leaderboard" title="View Global Tycoon Leaderboard">
                        🏆 Leaderboard
                    </div>

                    <!-- Cloud Sync Status Indicator -->
                    <div class="hud-badge sync-status" id="badge-sync" title="Save Status">
                        <span class="status-dot" id="sync-dot"></span>
                        <span id="badge-user">👤 Guest</span>
                        <span id="sync-text">✓ Saved</span>
                    </div>
                </div>
            </div>

            <!-- Big Glowing Tycoon Coin Bank -->
            <div class="hud-coin-box" id="hud-coin-box">
                <div class="coin-val">🪙 <span id="coin-counter">0</span></div>
                <div class="income-rate"><span>📈</span> <span id="income-counter">+$0/s</span></div>
            </div>
        </div>

        <!-- Interactive Station Inspector Card (Shows on machine tap) -->
        <div id="station-inspector">
            <div class="inspector-icon" id="insp-icon">🪚</div>
            <div class="inspector-details">
                <div class="inspector-title">
                    <span id="insp-title">BuzzSaw Station</span>
                    <span class="inspector-status" id="insp-status">🟢 Active</span>
                </div>
                <div class="inspector-stats" id="insp-stats">Throughput: 100% • Level 1</div>
            </div>
            <button class="inspector-btn-quick-buy" id="insp-quick-buy">
                Upgrade (🪙 40)
            </button>
            <button class="inspector-close-btn" id="insp-close">&times;</button>
        </div>

        <!-- Celebratory Event & Milestone Banner -->
        <div id="event-banner">⚡ RUSH HOUR! 2X SPEED!</div>

        <!-- Tutorial Hint -->
        <div id="tutorial-toast">💡 Tap anywhere on the mill to boost speed, or tap machines to inspect!</div>

        <!-- Action Pills Bar -->
        <div class="action-pills">
            <button class="pill-btn boost-btn" id="btn-tap-boost">⚡ Boost (Tap!)</button>
            <button class="pill-btn" id="btn-watch-boost">🎬 2x Boost (3m)</button>
            <button class="pill-btn" id="btn-daily">
                🎁 Daily Chest
                <span class="pill-badge-alert" id="daily-badge" style="display:none;">1</span>
            </button>
            <button class="pill-btn" id="btn-achievements">
                🎖️ Achievements
                <span class="pill-badge-alert" id="ach-badge" style="display:none;">!</span>
            </button>
            <button class="pill-btn" id="btn-prestige">🌰 Forest Reset</button>
            <button class="pill-btn" id="btn-settings">⚙️ Settings</button>
        </div>

        <button id="shop-toggle-mobile">🛒 Upgrades</button>
    </div>

    <!-- Upgrade Shop Sidebar / Bottom Sheet -->
    <div id="shop-panel">
        <div class="shop-header">
            <div class="shop-title-row">
                <div class="shop-title">🪵 Mill Upgrades</div>
                <div class="buy-mult-toggle">
                    <button class="mult-btn active" data-mult="1">x1</button>
                    <button class="mult-btn" data-mult="10">x10</button>
                    <button class="mult-btn" data-mult="max">MAX</button>
                </div>
            </div>
            <!-- Category Tabs -->
            <div class="category-tabs">
                <button class="cat-tab active" data-cat="all">⭐ All</button>
                <button class="cat-tab" data-cat="forest">🌲 Forest & Belts</button>
                <button class="cat-tab" data-cat="sawmill">🪚 Sawmill</button>
                <button class="cat-tab" data-cat="logistics">🏗️ Logistics</button>
                <button class="cat-tab" data-cat="fleet">🚛 Fleet & Road</button>
            </div>
        </div>
        <div class="shop-list" id="shop-list"></div>
    </div>
</div>

<!-- Start Screen -->
<div id="start-screen">
    <div class="logo-box">
        <div class="logo-main">LOG JAM</div>
        <div class="logo-sub">Mill Empire</div>
    </div>
    <div class="start-btn-box">
        <button class="btn-huge guest" id="btn-start-guest">▶ PLAY AS GUEST</button>
        <button class="btn-huge auth" id="btn-start-auth">🔑 LOGIN / REGISTER</button>
    </div>
</div>

<!-- Auth Modal -->
<div class="modal-overlay" id="modal-auth">
    <div class="modal-card">
        <div class="modal-header">
            <div class="modal-title">🔑 Cloud Account</div>
            <button class="close-btn" id="auth-close">&times;</button>
        </div>
        <div class="inline-msg" id="auth-msg"></div>
        <div class="input-group">
            <label>Username</label>
            <input type="text" class="input-field" id="auth-username" placeholder="3-20 characters" autocomplete="username">
        </div>
        <div class="input-group">
            <label>Password</label>
            <div class="input-wrap">
                <input type="password" class="input-field" id="auth-password" placeholder="At least 6 characters" autocomplete="current-password">
                <button class="pwd-toggle" id="pwd-toggle">👁</button>
            </div>
        </div>
        <div class="modal-btn-row">
            <button class="btn-full btn-primary" id="btn-do-login">Login</button>
            <button class="btn-full btn-secondary" id="btn-do-register">Register</button>
        </div>
    </div>
</div>

<!-- Settings Modal -->
<div class="modal-overlay" id="modal-settings">
    <div class="modal-card">
        <div class="modal-header">
            <div class="modal-title">⚙️ Mill Settings</div>
            <button class="close-btn" id="settings-close">&times;</button>
        </div>

        <div class="modal-btn-row">
            <button class="btn-full btn-secondary" id="toggle-sfx">SFX: ON</button>
            <button class="btn-full btn-secondary" id="toggle-music">Music: ON</button>
        </div>

        <div class="input-group" style="margin-top: 6px;">
            <label>Backend / Cloud Server URL</label>
            <input type="text" class="input-field" id="setting-server-url" placeholder="https://customs-wins-wallace-ultimately.trycloudflare.com">
        </div>

        <div id="settings-account-sec">
            <div style="font-size: 13px; color: var(--text-sub); margin-bottom: 8px;">
                Account: <strong id="settings-user-display" style="color: #fff;">Guest</strong>
            </div>
            <div class="modal-btn-row">
                <button class="btn-full btn-secondary" id="btn-sync-now">☁️ Sync Now</button>
                <button class="btn-full btn-secondary" id="btn-logout" style="display:none;">Logout</button>
            </div>
        </div>

        <div style="border-top: 1px solid var(--panel-border); padding-top: 12px; margin-top: 6px;">
            <button class="btn-full btn-danger" id="btn-reset-save">Reset Save Data</button>
        </div>
    </div>
</div>

<!-- Leaderboard Modal -->
<div class="modal-overlay" id="modal-leaderboard">
    <div class="modal-card">
        <div class="modal-header">
            <div class="modal-title">🏆 Top Lumber Tycoons</div>
            <button class="close-btn" id="leaderboard-close">&times;</button>
        </div>
        <p style="font-size: 12px; color: var(--text-sub);">
            Real-time rankings synced across all devices connected to the mill cloud!
        </p>
        <div class="leaderboard-list" id="leaderboard-list">
            <div style="text-align:center; padding: 20px; color: var(--text-sub);">Loading leaderboard...</div>
        </div>
        <button class="btn-full btn-secondary" id="btn-refresh-leaderboard">⟳ Refresh Rankings</button>
    </div>
</div>

<!-- Achievements Modal -->
<div class="modal-overlay" id="modal-achievements">
    <div class="modal-card">
        <div class="modal-header">
            <div class="modal-title">🎖️ Milestones & Achievements</div>
            <button class="close-btn" id="achievements-close">&times;</button>
        </div>
        <p style="font-size: 12px; color: var(--text-sub);" id="ach-summary-text">
            Complete tycoon milestones to earn extra coins and boosts!
        </p>
        <div class="achievements-list" id="achievements-list"></div>
    </div>
</div>

<!-- Conflict Resolution Modal -->
<div class="modal-overlay" id="modal-conflict">
    <div class="modal-card">
        <div class="modal-header">
            <div class="modal-title">☁️ Save Conflict</div>
        </div>
        <p style="font-size: 13px; color: var(--text-sub); line-height: 1.4;">
            We found both a cloud save and a local save on this device. Which progress would you like to keep?
        </p>
        <div id="conflict-details" style="font-size: 13px; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px;"></div>
        <div style="display:flex; flex-direction:column; gap:8px; margin-top:6px;">
            <button class="btn-full btn-primary" id="btn-keep-richer">🏆 Keep Whichever Earned More</button>
            <button class="btn-full btn-secondary" id="btn-keep-cloud">☁️ Keep Cloud Progress</button>
            <button class="btn-full btn-secondary" id="btn-keep-local">📱 Keep Device Progress</button>
        </div>
    </div>
</div>

<!-- Welcome Back / Offline Earnings Modal -->
<div class="modal-overlay" id="modal-welcome">
    <div class="modal-card" style="text-align: center;">
        <div style="font-size: 42px; margin-bottom: 8px;">🎉</div>
        <div class="modal-title" style="justify-content: center;">Welcome Back, Tycoon!</div>
        <p style="font-size: 14px; color: var(--text-sub); margin: 6px 0 12px;">
            While you were away, your mill kept processing lumber!
        </p>
        <div style="font-size: 28px; font-weight: 900; color: var(--gold); margin-bottom: 16px;">
            +🪙 <span id="offline-earned-val">0</span>
        </div>
        <button class="btn-full btn-primary" id="btn-claim-offline">Collect Coins</button>
    </div>
</div>

<!-- 7-Day Daily Chest Modal -->
<div class="modal-overlay" id="modal-daily">
    <div class="modal-card" style="text-align: center;">
        <div style="font-size: 46px; margin-bottom: 6px;">🎁</div>
        <div class="modal-title" style="justify-content: center;">Daily Lumber Chest</div>
        <p style="font-size: 13px; color: var(--text-sub); margin: 4px 0 10px;" id="daily-streak-text">
            Log in every day for escalating rewards!
        </p>
        <div class="daily-grid" id="daily-grid"></div>
        <button class="btn-full btn-primary" id="btn-claim-daily">Claim Today's Chest</button>
        <button class="btn-full btn-secondary" id="btn-close-daily" style="margin-top:6px;">Close</button>
    </div>
</div>

<!-- Forest Reset (Prestige) Modal -->
<div class="modal-overlay" id="modal-prestige">
    <div class="modal-card">
        <div class="modal-header">
            <div class="modal-title">🌰 Forest Reset (Prestige)</div>
            <button class="close-btn" id="prestige-close">&times;</button>
        </div>
        <p style="font-size: 13px; color: var(--text-sub); line-height: 1.4;">
            Replant your forest and begin a fresh operation! You will reset coins and station levels, but gain permanent <strong>Golden Acorns</strong>.
        </p>
        <div style="background: rgba(255,207,51,0.1); border: 1px solid var(--gold-glow); padding: 14px; border-radius: 14px; text-align:center;">
            <div style="font-size: 11px; color: var(--text-sub); text-transform: uppercase; font-weight: 800;">Permanent Rewards</div>
            <div style="font-size: 28px; font-weight: 900; color: var(--gold); margin: 6px 0;" id="prestige-acorns-gain">+0 Acorns</div>
            <div style="font-size: 13px; color: #68d391; font-weight: 700;" id="prestige-boost-gain">+0% Global Profit Forever</div>
        </div>
        <div class="modal-btn-row">
            <button class="btn-full btn-primary" id="btn-do-prestige">Reset & Claim Acorns</button>
            <button class="btn-full btn-secondary" id="btn-cancel-prestige">Cancel</button>
        </div>
    </div>
</div>

<!-- Toast -->
<div class="toast" id="toast-msg">🏆 Achievement Unlocked!</div>

<script>
/**
 * LOG JAM: MILL EMPIRE
 * Complete Canvas 2D Idle Tycoon Web Game
 * Self-contained HTML + CSS + JS (Zero CDN dependencies)
 * Compatible with FastAPI / Wings of Fire Python backends
 */

// ==========================================
// 1. CONFIG & TUNING CONSTANTS
// ==========================================
const API_CONFIG = {
    BASE_URL: (() => {
        if (typeof window !== 'undefined') {
            const h = window.location.hostname;
            if (h === 'localhost' || h === '127.0.0.1' || h.startsWith('192.168.') || h.endsWith('.trycloudflare.com')) {
                return window.location.origin;
            }
        }
        return "https://customs-wins-wallace-ultimately.trycloudflare.com";
    })(),
    AUTH:        { method: "POST", path: "/api/user/auth" },
    GET_USER:    { method: "GET",  path: "/api/user" },
    SAVE:        { method: "POST", path: "/api/user/save" },
    HEALTH:      { method: "GET",  path: "/api/health" },
    LEADERBOARD: { method: "GET",  path: "/api/leaderboard" },
    AUTH_MODE: "hash",
    REQUEST_TIMEOUT_MS: 8000,
    SAVE_INTERVAL_MS: 15000,
    OFFLINE_MAX_HOURS: 8
};

const WOOD_TIERS = [
    { name: "Pine",    color: "#c4a35a", barkColor: "#6b4a2a", plankColor: "#d9ba79", value: 1.0,   unlockCost: 0 },
    { name: "Oak",     color: "#966533", barkColor: "#4f3115", plankColor: "#b8834c", value: 3.5,   unlockCost: 2500 },
    { name: "Maple",   color: "#c24b27", barkColor: "#571c0b", plankColor: "#e66a43", value: 12.0,  unlockCost: 35000 },
    { name: "Ebony",   color: "#2a2830", barkColor: "#141318", plankColor: "#45424f", value: 45.0,  unlockCost: 500000 },
    { name: "Golden",  color: "#ffd700", barkColor: "#b39200", plankColor: "#ffe55c", value: 200.0, unlockCost: 8000000 }
];

const UPGRADE_DEFS = [
    { id: "spawnRate",   name: "Log Spawn Rate",      category: "forest",    icon: "🌲", baseCost: 15,    costMult: 1.15, maxLv: 100, desc: "Chop & feed logs faster" },
    { id: "convSpeed",   name: "Conveyor Speed",      category: "forest",    icon: "⏩", baseCost: 25,    costMult: 1.15, maxLv: 100, desc: "Faster roller belts" },
    { id: "sawCount",    name: "Number of Saws",      category: "sawmill",   icon: "🪚", baseCost: 80,    costMult: 1.75, maxLv: 6,   desc: "Adds up to 6 spinning saws" },
    { id: "sawSpeed",    name: "Saw Speed & Cut",     category: "sawmill",   icon: "⚡", baseCost: 40,    costMult: 1.16, maxLv: 100, desc: "Quicker cuts & more planks" },
    { id: "sortSpeed",   name: "Sorting Arms",        category: "sawmill",   icon: "📦", baseCost: 50,    costMult: 1.15, maxLv: 100, desc: "Faster mechanical sorting" },
    { id: "stackCap",    name: "Stack Capacity",      category: "logistics", icon: "📚", baseCost: 70,    costMult: 1.18, maxLv: 100, desc: "Taller piles in yard" },
    { id: "craneSpeed",  name: "Crane Speed",         category: "logistics", icon: "🏗️", baseCost: 90,    costMult: 1.16, maxLv: 100, desc: "Quick stack pickup & hoist" },
    { id: "dockCount",   name: "Loading Docks",       category: "logistics", icon: "🚏", baseCost: 250,   costMult: 2.20, maxLv: 3,   desc: "Adds simultaneous truck bays" },
    { id: "truckCount",  name: "Truck Fleet",         category: "fleet",     icon: "🚛", baseCost: 180,   costMult: 1.85, maxLv: 5,   desc: "More delivery trucks on route" },
    { id: "truckCap",    name: "Truck Cargo Bed",     category: "fleet",     icon: "📐", baseCost: 110,   costMult: 1.22, maxLv: 100, desc: "Carry more stacks per trip" },
    { id: "truckSpeed",  name: "Truck Highway Speed", category: "fleet",     icon: "💨", baseCost: 95,    costMult: 1.15, maxLv: 100, desc: "Quicker road transit" },
    { id: "roadUpgrade", name: "Road Quality",        category: "fleet",     icon: "🛣️", baseCost: 350,   costMult: 1.90, maxLv: 5,   desc: "Paved lanes & wider bridge" },
    { id: "woodValue",   name: "Market Value",        category: "fleet",     icon: "💰", baseCost: 150,   costMult: 1.25, maxLv: 100, desc: "Direct sale price multiplier" }
];

const ACHIEVEMENTS = [
    { id: "first_log",   name: "First Cut",           icon: "🪓", desc: "Process your first log",         cond: s => s.stats.logsProcessed >= 1,   reward: 20 },
    { id: "logs_50",     name: "Lumberjack",          icon: "🌲", desc: "Cut 50 logs",                    cond: s => s.stats.logsProcessed >= 50,  reward: 100 },
    { id: "logs_500",    name: "Master Faller",       icon: "🪵", desc: "Cut 500 logs",                   cond: s => s.stats.logsProcessed >= 500, reward: 1000 },
    { id: "first_truck", name: "Cargo Away!",         icon: "🚛", desc: "Complete 1 truck delivery",      cond: s => s.stats.deliveries >= 1,      reward: 35 },
    { id: "trucks_25",   name: "Fleet Logistician",   icon: "🛣️", desc: "Complete 25 truck deliveries",   cond: s => s.stats.deliveries >= 25,     reward: 500 },
    { id: "coins_1k",    name: "Small Business",      icon: "🪙", desc: "Earn 1,000 total coins",         cond: s => s.totalEarned >= 1000,        reward: 50 },
    { id: "coins_100k",  name: "Log Jam Mogul",       icon: "💰", desc: "Earn 100,000 total coins",       cond: s => s.totalEarned >= 100000,      reward: 2500 },
    { id: "coins_1m",    name: "Mill Millionaire",    icon: "💎", desc: "Earn 1,000,000 total coins",     cond: s => s.totalEarned >= 1000000,     reward: 15000 },
    { id: "tier_oak",    name: "Hardwood Era",        icon: "🍂", desc: "Unlock Oak wood tier",           cond: s => s.woodTier >= 1,              reward: 250 },
    { id: "tier_maple",  name: "Fine Furniture",      icon: "🍁", desc: "Unlock Maple wood tier",         cond: s => s.woodTier >= 2,              reward: 1500 },
    { id: "tier_golden", name: "Midas Lumber",        icon: "⭐", desc: "Unlock Golden Wood tier",        cond: s => s.woodTier >= 4,              reward: 50000 },
    { id: "saws_max",    name: "Buzzing Mill",        icon: "🪚", desc: "Max out saw count (6 saws)",     cond: s => (s.upgrades.sawCount||0)>=6,  reward: 2000 },
    { id: "docks_max",   name: "Busy Harbor",         icon: "🚏", desc: "Max out loading docks (3 docks)",cond: s => (s.upgrades.dockCount||0)>=3, reward: 3000 },
    { id: "tap_100",     name: "Hands On Manager",    icon: "👆", desc: "Tap scene 100 times",            cond: s => s.stats.taps >= 100,          reward: 200 },
    { id: "first_reset", name: "New Beginnings",      icon: "🌰", desc: "Perform 1 Forest Reset",         cond: s => s.prestigeCount >= 1,         reward: 500 },
    { id: "splash_event",name: "River Splash!",       icon: "💦", desc: "A truck took a dip in the river",cond: s => s.stats.splashCount >= 1,    reward: 150 },
    { id: "golden_log",  name: "Golden Discovery",    icon: "🌟", desc: "Catch a Golden Log",             cond: s => s.stats.goldenLogs >= 1,      reward: 300 }
];

// Interactive Stations Definition for Canvas Taps & Inspector
const STATIONS = [
    { id: "spawner",   name: "Forest Spawner",     category: "forest",    icon: "🌲", x: 0.5,  y: 3.5, defId: "spawnRate" },
    { id: "conveyor",  name: "Roller Conveyor",    category: "forest",    icon: "⏩", x: 2.5,  y: 3.5, defId: "convSpeed" },
    { id: "saws",      name: "BuzzSaw Station",    category: "sawmill",   icon: "🪚", x: 4.5,  y: 3.5, defId: "sawSpeed", secondaryDefId: "sawCount" },
    { id: "sorter",    name: "Sorting Machine",    category: "sawmill",   icon: "📦", x: 6.5,  y: 3.5, defId: "sortSpeed" },
    { id: "yard",      name: "Stacking Yard",      category: "logistics", icon: "📚", x: 8.5,  y: 5.0, defId: "stackCap" },
    { id: "crane",     name: "Heavy Duty Crane",   category: "logistics", icon: "🏗️", x: 10.5, y: 5.0, defId: "craneSpeed" },
    { id: "docks",     name: "Loading Bays",       category: "logistics", icon: "🚏", x: 14.0, y: 5.0, defId: "dockCount", secondaryDefId: "truckCount" },
    { id: "highway",   name: "Delivery Highway",   category: "fleet",     icon: "🚛", x: 14.0, y: 8.5, defId: "truckSpeed", secondaryDefId: "truckCap" },
    { id: "bridge",    name: "Wooden River Bridge",category: "fleet",     icon: "🌉", x: 14.0, y: 12.0,defId: "roadUpgrade", secondaryDefId: "woodValue" }
];

// Daily Chest Rewards (7-day calendar)
const DAILY_REWARDS = [
    { day: 1, coins: 500,     acorns: 0 },
    { day: 2, coins: 1500,    acorns: 0 },
    { day: 3, coins: 4000,    acorns: 0 },
    { day: 4, coins: 10000,   acorns: 0 },
    { day: 5, coins: 25000,   acorns: 1 },
    { day: 6, coins: 60000,   acorns: 2 },
    { day: 7, coins: 150000,  acorns: 5, isMega: true }
];

// ==========================================
// 2. HELPER UTILITIES
// ==========================================
function formatNumber(num) {
    if (isNaN(num) || num === null || num === undefined) return "0";
    if (num < 1000) return Math.floor(num).toLocaleString();
    const suffixes = ["", "K", "M", "B", "T", "aa", "ab", "ac", "ad", "ae", "af"];
    const exp = Math.floor(Math.log10(num) / 3);
    if (exp >= suffixes.length) return num.toExponential(2);
    const scaled = num / Math.pow(10, exp * 3);
    return scaled.toFixed(scaled < 10 ? 2 : 1) + suffixes[exp];
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str).replace(/[&<>"']/g, m => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[m]));
}

async function sha256(str) {
    if (!window.crypto || !window.crypto.subtle) {
        let h = 0;
        for (let i = 0; i < str.length; i++) h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
        return Math.abs(h).toString(16).padStart(16, "0");
    }
    const enc = new TextEncoder().encode(str);
    const buf = await window.crypto.subtle.digest("SHA-256", enc);
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
}

// Milestone info for upgrade levels (Lv 10, 25, 50, 100 give 2x boosts)
function getMilestoneInfo(level, maxLv = 100) {
    const milestones = [10, 25, 50, 100].filter(m => m <= maxLv);
    for (let i = 0; i < milestones.length; i++) {
        const m = milestones[i];
        if (level < m) {
            const prev = i === 0 ? 0 : milestones[i - 1];
            const pct = Math.min(100, Math.max(0, ((level - prev) / (m - prev)) * 100));
            return { next: m, prev, pct, mult: Math.pow(2, i), isMaxMilestone: false };
        }
    }
    return { next: maxLv, prev: milestones[milestones.length - 1] || 0, pct: 100, mult: Math.pow(2, milestones.length), isMaxMilestone: true };
}

function getMilestoneMultiplier(level) {
    let mult = 1;
    if (level >= 10) mult *= 2;
    if (level >= 25) mult *= 2;
    if (level >= 50) mult *= 2;
    if (level >= 100) mult *= 2;
    return mult;
}

// ==========================================
// 3. WEB AUDIO SYNTHESIZER
// ==========================================
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.sfxEnabled = true;
        this.musicEnabled = true;
        this.musicGain = null;
        this.sfxGain = null;
        this.nextNoteTime = 0;
        this.noteIndex = 0;
        this.isPlayingMusic = false;
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
        this.musicGain.gain.value = 0.08;
        this.musicGain.connect(this.ctx.destination);

        if (this.musicEnabled) this.startMusic();
    }

    resume() {
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
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
            g.gain.setValueAtTime(0.08, time);
            g.gain.exponentialRampToValueAtTime(0.001, time + dur);
            osc.connect(g);
            g.connect(this.musicGain);
            osc.start(time);
            osc.stop(time + dur);
        } catch(e) {}
    }

    playSfx(type) {
        if (!this.sfxEnabled || !this.ctx) return;
        this.resume();
        const now = this.ctx.currentTime;
        try {
            if (type === 'coin') {
                const osc = this.ctx.createOscillator();
                const g = this.ctx.createGain();
                osc.type = "sine";
                osc.frequency.setValueAtTime(880, now);
                osc.frequency.exponentialRampToValueAtTime(1760, now + 0.12);
                g.gain.setValueAtTime(0.25, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
                osc.connect(g);
                g.connect(this.sfxGain);
                osc.start(now);
                osc.stop(now + 0.12);
            } else if (type === 'saw') {
                const osc = this.ctx.createOscillator();
                const g = this.ctx.createGain();
                osc.type = "sawtooth";
                osc.frequency.setValueAtTime(160, now);
                osc.frequency.linearRampToValueAtTime(240, now + 0.1);
                g.gain.setValueAtTime(0.12, now);
                g.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
                osc.connect(g);
                g.connect(this.sfxGain);
                osc.start(now);
                osc.stop(now + 0.15);
            } else if (type === 'clunk') {
                const osc = this.ctx.createOscillator();
                const g = this.ctx.createGain();
                osc.type = "square";
                osc.frequency.setValueAtTime(120, now);
                osc.frequency.exponentialRampToValueAtTime(40, now + 0.1);
                g.gain.setValueAtTime(0.25, now);
                g.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                osc.connect(g);
                g.connect(this.sfxGain);
                osc.start(now);
                osc.stop(now + 0.1);
            } else if (type === 'horn') {
                [220, 330].forEach(f => {
                    const osc = this.ctx.createOscillator();
                    const g = this.ctx.createGain();
                    osc.type = "sawtooth";
                    osc.frequency.setValueAtTime(f, now);
                    g.gain.setValueAtTime(0.1, now);
                    g.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
                    osc.connect(g);
                    g.connect(this.sfxGain);
                    osc.start(now);
                    osc.stop(now + 0.25);
                });
            } else if (type === 'upgrade') {
                [523.25, 659.25, 783.99, 1046.50].forEach((f, idx) => {
                    const osc = this.ctx.createOscillator();
                    const g = this.ctx.createGain();
                    osc.type = "sine";
                    const t = now + idx * 0.06;
                    osc.frequency.setValueAtTime(f, t);
                    g.gain.setValueAtTime(0.2, t);
                    g.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
                    osc.connect(g);
                    g.connect(this.sfxGain);
                    osc.start(t);
                    osc.stop(t + 0.1);
                });
            } else if (type === 'milestone') {
                [440, 554.37, 659.25, 880, 1108.73].forEach((f, idx) => {
                    const osc = this.ctx.createOscillator();
                    const g = this.ctx.createGain();
                    osc.type = "triangle";
                    const t = now + idx * 0.08;
                    osc.frequency.setValueAtTime(f, t);
                    g.gain.setValueAtTime(0.3, t);
                    g.gain.exponentialRampToValueAtTime(0.001, t + 0.2);
                    osc.connect(g);
                    g.connect(this.sfxGain);
                    osc.start(t);
                    osc.stop(t + 0.2);
                });
            } else if (type === 'tap') {
                const osc = this.ctx.createOscillator();
                const g = this.ctx.createGain();
                osc.type = "sine";
                osc.frequency.setValueAtTime(400, now);
                osc.frequency.exponentialRampToValueAtTime(200, now + 0.04);
                g.gain.setValueAtTime(0.1, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
                osc.connect(g);
                g.connect(this.sfxGain);
                osc.start(now);
                osc.stop(now + 0.04);
            } else if (type === 'error') {
                const osc = this.ctx.createOscillator();
                const g = this.ctx.createGain();
                osc.type = "sawtooth";
                osc.frequency.setValueAtTime(140, now);
                osc.frequency.setValueAtTime(100, now + 0.08);
                g.gain.setValueAtTime(0.15, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
                osc.connect(g);
                g.connect(this.sfxGain);
                osc.start(now);
                osc.stop(now + 0.16);
            }
        } catch(e) {}
    }
}
const audio = new SoundEngine();

// ==========================================
// 4. GAME STATE & PROGRESSION
// ==========================================
function createDefaultState() {
    return {
        coins: 0,
        totalEarned: 0,
        woodTier: 0,
        goldenAcorns: 0,
        prestigeCount: 0,
        upgrades: {
            spawnRate: 0,
            convSpeed: 0,
            sawCount: 1,
            sawSpeed: 0,
            sortSpeed: 0,
            stackCap: 0,
            craneSpeed: 0,
            dockCount: 1,
            truckCount: 1,
            truckCap: 0,
            truckSpeed: 0,
            roadUpgrade: 0,
            woodValue: 0
        },
        achievements: [],
        dailyStreak: 0,
        lastDailyClaim: 0,
        stats: {
            logsProcessed: 0,
            deliveries: 0,
            taps: 0,
            splashCount: 0,
            goldenLogs: 0,
            playTime: 0
        },
        settings: {
            sfx: true,
            music: true,
            serverUrl: API_CONFIG.BASE_URL
        },
        tutorialStep: 0,
        saveVersion: 1,
        lastSaveTime: Date.now()
    };
}

let gameState = createDefaultState();
let currentUser = null;
let buyMultiplier = 1;
let currentCategory = "all";
let selectedStation = null;
let tapBoostRemaining = 0;
let watchBoostRemaining = 0;
let rushHourRemaining = 0;

// Cache map of upgrade cards for live updating without DOM recreation
const shopCardsMap = new Map();

// ==========================================
// 5. STORAGE & CLOUD API MODULE
// ==========================================
const Storage = {
    GUEST_KEY: "logjam_save_guest",
    USER_KEY_PREFIX: "logjam_save_user_",
    ACTIVE_USER_KEY: "logjam_active_user",

    saveLocal() {
        gameState.lastSaveTime = Date.now();
        const key = currentUser ? (this.USER_KEY_PREFIX + currentUser.username.toLowerCase()) : this.GUEST_KEY;
        try {
            localStorage.setItem(key, JSON.stringify(gameState));
            if (currentUser) {
                localStorage.setItem(this.ACTIVE_USER_KEY, JSON.stringify(currentUser));
            }
            updateSyncIndicator("✓ Saved", "saved");
        } catch (e) {
            console.warn("Local storage write error:", e);
        }
    },

    loadLocal(username = null) {
        const key = username ? (this.USER_KEY_PREFIX + username.toLowerCase()) : (currentUser ? (this.USER_KEY_PREFIX + currentUser.username.toLowerCase()) : this.GUEST_KEY);
        try {
            const raw = localStorage.getItem(key);
            if (raw) return JSON.parse(raw);
        } catch (e) {}
        return null;
    },

    async syncToCloud() {
        if (!currentUser) return;
        updateSyncIndicator("⟳ Syncing...", "syncing");
        const url = (gameState.settings.serverUrl || API_CONFIG.BASE_URL) + API_CONFIG.SAVE.path;
        try {
            const controller = new AbortController();
            const tid = setTimeout(() => controller.abort(), API_CONFIG.REQUEST_TIMEOUT_MS);
            const resp = await fetch(url, {
                method: API_CONFIG.SAVE.method,
                headers: {
                    "Content-Type": "application/json",
                    ...(currentUser.token ? { "Authorization": `Bearer ${currentUser.token}` } : {})
                },
                body: JSON.stringify({
                    username: currentUser.username,
                    passwordHash: currentUser.passwordHash,
                    save: gameState,
                    updated_at: Date.now()
                }),
                signal: controller.signal
            });
            clearTimeout(tid);
            const data = await resp.json();
            if (data.ok) {
                updateSyncIndicator("✓ Synced", "saved");
            } else {
                updateSyncIndicator("⚠ Offline", "offline");
            }
        } catch (e) {
            updateSyncIndicator("⚠ Offline", "offline");
        }
    }
};

function updateSyncIndicator(msg, state = "saved") {
    const el = document.getElementById("sync-text");
    const dot = document.getElementById("sync-dot");
    if (el) el.textContent = msg;
    if (dot) {
        dot.className = "status-dot " + state;
    }
}

// ==========================================
// 6. ISOMETRIC 2D RENDERER & VISUALS
// ==========================================
const TILE_W = 60;
const TILE_H = 30;

function toIso(x, y, z = 0) {
    return {
        x: (x - y) * (TILE_W / 2),
        y: (x + y) * (TILE_H / 2) - z * 18
    };
}

function fromIso(screenX, screenY) {
    const dx = screenX - camera.x;
    const dy = screenY - camera.y;
    const gx = (dx / (TILE_W / 2) + dy / (TILE_H / 2)) / 2;
    const gy = (dy / (TILE_H / 2) - dx / (TILE_W / 2)) / 2;
    return { x: gx, y: gy };
}

class Particle {
    constructor(x, y, vx, vy, color, size, life) {
        this.x = x; this.y = y;
        this.vx = vx; this.vy = vy;
        this.color = color;
        this.size = size;
        this.life = life;
        this.maxLife = life;
    }
    update(dt) {
        this.x += this.vx * dt;
        this.y += this.vy * dt;
        this.life -= dt;
    }
    draw(ctx) {
        const a = Math.max(0, this.life / this.maxLife);
        ctx.save();
        ctx.globalAlpha = a;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

class FloatingText {
    constructor(x, y, text, color = "#ffcf33", size = 16) {
        this.x = x; this.y = y;
        this.text = text;
        this.color = color;
        this.size = size;
        this.life = 1.2;
        this.maxLife = 1.2;
    }
    update(dt) {
        this.y -= 28 * dt;
        this.life -= dt;
    }
    draw(ctx) {
        const a = Math.max(0, this.life / this.maxLife);
        ctx.save();
        ctx.globalAlpha = a;
        ctx.fillStyle = this.color;
        ctx.font = `900 ${this.size}px ${getComputedStyle(document.body).fontFamily}`;
        ctx.textAlign = "center";
        ctx.shadowColor = "rgba(0,0,0,0.85)";
        ctx.shadowBlur = 5;
        ctx.fillText(this.text, this.x, this.y);
        ctx.restore();
    }
}

let particles = [];
let floatingTexts = [];
let logs = [];
let planks = [];
let stacks = [];
let trucks = [];

const bgCanvas = document.getElementById("bg-canvas");
const mainCanvas = document.getElementById("main-canvas");
const uiCanvas = document.getElementById("ui-canvas");
const bgCtx = bgCanvas.getContext("2d");
const mainCtx = mainCanvas.getContext("2d");
const uiCtx = uiCanvas.getContext("2d");

let camera = { x: 0, y: 0, zoom: 1 };

function resizeCanvases() {
    const dpr = window.devicePixelRatio || 1;
    const w = bgCanvas.parentElement.clientWidth;
    const h = bgCanvas.parentElement.clientHeight;

    [bgCanvas, mainCanvas, uiCanvas].forEach(c => {
        c.width = w * dpr;
        c.height = h * dpr;
        const ctx = c.getContext("2d");
        ctx.resetTransform();
        ctx.scale(dpr, dpr);
    });

    camera.x = w / 2;
    camera.y = h / 2 - 40;
    renderBackground();
}
window.addEventListener("resize", resizeCanvases);

function renderBackground() {
    const w = bgCanvas.parentElement.clientWidth;
    const h = bgCanvas.parentElement.clientHeight;
    bgCtx.clearRect(0, 0, w, h);

    bgCtx.save();
    bgCtx.translate(camera.x, camera.y);

    // Terrain Tiles
    for (let x = -4; x <= 16; x++) {
        for (let y = -2; y <= 16; y++) {
            const p = toIso(x, y, 0);
            let fill = (x >= 13 && x <= 15) ? "#444652" : // Paved Asphalt Road
                       (x > 15) ? "#3182ce" : // Deep River
                       ((x + y) % 2 === 0 ? "#5ea332" : "#56962e"); // Vibrant Grass

            if (x >= 4 && x <= 11 && y >= 3 && y <= 9) {
                fill = "#b8956a"; // Dirt Mill Yard
            }

            bgCtx.fillStyle = fill;
            bgCtx.beginPath();
            bgCtx.moveTo(p.x, p.y);
            bgCtx.lineTo(p.x + TILE_W / 2, p.y + TILE_H / 2);
            bgCtx.lineTo(p.x, p.y + TILE_H);
            bgCtx.lineTo(p.x - TILE_W / 2, p.y + TILE_H / 2);
            bgCtx.closePath();
            bgCtx.fill();
        }
    }

    // Road Markings
    for (let y = -2; y <= 15; y += 2) {
        const rp = toIso(14, y, 0);
        bgCtx.fillStyle = "#ffffff";
        bgCtx.fillRect(rp.x - 2, rp.y + 12, 4, 8);
    }

    // Wooden Bridge
    const bp = toIso(14, 11, 0.2);
    bgCtx.fillStyle = "#8a5c36";
    bgCtx.fillRect(bp.x - 36, bp.y - 10, 72, 30);
    bgCtx.strokeStyle = "#5a3c20";
    bgCtx.lineWidth = 2;
    bgCtx.strokeRect(bp.x - 36, bp.y - 10, 72, 30);

    // Pine Trees
    const treeCoords = [
        [-3,-1], [-2,-1], [-1,-1], [0,-1], [1,-1],
        [-3,1], [-3,3], [-3,5], [-3,7], [-2,9], [-1,11],
        [2,12], [4,13], [6,14], [8,14]
    ];
    treeCoords.forEach(([tx, ty]) => {
        const tp = toIso(tx, ty, 0);
        drawPineTree(bgCtx, tp.x, tp.y);
    });

    bgCtx.restore();
}

function drawPineTree(ctx, x, y) {
    ctx.fillStyle = "rgba(0,0,0,0.18)";
    ctx.beginPath();
    ctx.ellipse(x, y + 14, 16, 8, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#5c3c1e";
    ctx.fillRect(x - 3, y - 4, 6, 16);

    const foliage = ["#1b5e20", "#2e7d32", "#388e3c"];
    foliage.forEach((c, idx) => {
        ctx.fillStyle = c;
        ctx.beginPath();
        ctx.moveTo(x, y - 36 - idx * 12);
        ctx.lineTo(x + 18 - idx * 2, y - 10 - idx * 12);
        ctx.lineTo(x - 18 + idx * 2, y - 10 - idx * 12);
        ctx.closePath();
        ctx.fill();
    });
}

function drawIsoBox(ctx, x, y, z, w, h, d, topColor, leftColor, rightColor) {
    const p = toIso(x, y, z);
    const sw = w * (TILE_W / 2);
    const sh = h * (TILE_H / 2);
    const sz = d * 18;

    // Top Face
    ctx.fillStyle = topColor;
    ctx.beginPath();
    ctx.moveTo(p.x, p.y - sz);
    ctx.lineTo(p.x + sw, p.y + sh - sz);
    ctx.lineTo(p.x, p.y + sh * 2 - sz);
    ctx.lineTo(p.x - sw, p.y + sh - sz);
    ctx.closePath();
    ctx.fill();

    // Left Face
    ctx.fillStyle = leftColor;
    ctx.beginPath();
    ctx.moveTo(p.x - sw, p.y + sh - sz);
    ctx.lineTo(p.x, p.y + sh * 2 - sz);
    ctx.lineTo(p.x, p.y + sh * 2);
    ctx.lineTo(p.x - sw, p.y + sh);
    ctx.closePath();
    ctx.fill();

    // Right Face
    ctx.fillStyle = rightColor;
    ctx.beginPath();
    ctx.moveTo(p.x + sw, p.y + sh - sz);
    ctx.lineTo(p.x, p.y + sh * 2 - sz);
    ctx.lineTo(p.x, p.y + sh * 2);
    ctx.lineTo(p.x + sw, p.y + sh);
    ctx.closePath();
    ctx.fill();
}

function drawLogEntity(ctx, log) {
    const tier = WOOD_TIERS[log.tier] || WOOD_TIERS[0];
    const p = toIso(log.x, log.y, log.z);
    const rad = 14;

    ctx.fillStyle = "rgba(0,0,0,0.2)";
    ctx.beginPath();
    ctx.ellipse(p.x, p.y + 4, rad, rad * 0.5, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = tier.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y - 10, rad, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = tier.barkColor;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    ctx.strokeStyle = tier.barkColor;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(p.x, p.y - 10, rad * 0.5, 0, Math.PI * 2);
    ctx.stroke();

    const faceX = p.x;
    const faceY = p.y - 10;

    if (log.state === 'panic') {
        ctx.fillStyle = "#fff";
        ctx.beginPath();
        ctx.arc(faceX - 5, faceY - 2, 4, 0, Math.PI * 2);
        ctx.arc(faceX + 5, faceY - 2, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#000";
        ctx.beginPath();
        ctx.arc(faceX - 5, faceY - 3, 2, 0, Math.PI * 2);
        ctx.arc(faceX + 5, faceY - 3, 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#222";
        ctx.beginPath();
        ctx.arc(faceX, faceY + 5, 3.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#63b3ed";
        ctx.beginPath();
        ctx.arc(faceX + 9, faceY - 8, 2, 0, Math.PI * 2);
        ctx.fill();
    } else {
        ctx.fillStyle = "#222";
        ctx.beginPath();
        ctx.arc(faceX - 4, faceY - 2, 2, 0, Math.PI * 2);
        ctx.arc(faceX + 4, faceY - 2, 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = "#222";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(faceX, faceY + 2, 3.5, 0.1, Math.PI - 0.1);
        ctx.stroke();
    }
}

function drawTruckEntity(ctx, t) {
    const p = toIso(t.x, t.y, 0);
    const bodyColor = t.color || "#e53e3e";
    const wobble = t.onBridge ? Math.sin(Date.now() * 0.02) * 3 : 0;

    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.beginPath();
    ctx.ellipse(p.x, p.y + 10, 24, 12, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#2d3748";
    ctx.fillRect(p.x - 18, p.y + 2 + wobble, 8, 8);
    ctx.fillRect(p.x + 10, p.y + 2 + wobble, 8, 8);

    drawIsoBox(ctx, t.x - 0.2, t.y, 0.2 + wobble * 0.02, 0.6, 0.6, 0.8, bodyColor, "#c53030", "#9b2c2c");

    ctx.fillStyle = "#bee3f8";
    ctx.fillRect(p.x - 4, p.y - 16 + wobble, 10, 6);

    drawIsoBox(ctx, t.x + 0.5, t.y, 0.1 + wobble * 0.02, 0.8, 0.7, 0.4, "#718096", "#4a5568", "#2d3748");

    if (t.cargoStacks > 0) {
        const tier = WOOD_TIERS[gameState.woodTier];
        for (let s = 0; s < t.cargoStacks; s++) {
            drawIsoBox(ctx, t.x + 0.5, t.y, 0.5 + s * 0.3 + wobble * 0.02, 0.6, 0.5, 0.25, tier.plankColor, tier.barkColor, tier.barkColor);
        }
    }
}

// ==========================================
// 7. PRODUCTION LINE SYSTEMS
// ==========================================
let spawnTimer = 0;
let craneTimer = 0;

function updateProductionLine(dt) {
    const speedMult = (tapBoostRemaining > 0 ? 1.5 : 1.0) *
                      (rushHourRemaining > 0 ? 2.0 : 1.0) *
                      (watchBoostRemaining > 0 ? 2.0 : 1.0);

    // 1. Spawner
    const spawnRateLv = gameState.upgrades.spawnRate || 0;
    const spawnMilestoneMult = getMilestoneMultiplier(spawnRateLv);
    const spawnInterval = Math.max(0.3, (2.2 / (1 + spawnRateLv * 0.18)) / (speedMult * spawnMilestoneMult));
    spawnTimer += dt;
    if (spawnTimer >= spawnInterval) {
        spawnTimer = 0;
        if (logs.length < 18) {
            logs.push({
                x: 0.5,
                y: 3.5,
                z: 0.2,
                tier: gameState.woodTier,
                state: "happy",
                cutProgress: 0,
                id: Math.random()
            });
            audio.playSfx('clunk');
        }
    }

    // 2. Conveyor & Saws
    const convSpeedLv = gameState.upgrades.convSpeed || 0;
    const convMilestoneMult = getMilestoneMultiplier(convSpeedLv);
    const convSpeed = (1.5 + convSpeedLv * 0.15) * speedMult * convMilestoneMult;
    const numSaws = Math.min(6, Math.max(1, gameState.upgrades.sawCount || 1));
    const sawSpeedLv = gameState.upgrades.sawSpeed || 0;
    const sawMilestoneMult = getMilestoneMultiplier(sawSpeedLv);
    const cutDuration = Math.max(0.2, (1.4 / (1 + sawSpeedLv * 0.2)) / (speedMult * sawMilestoneMult));

    for (let i = logs.length - 1; i >= 0; i--) {
        const log = logs[i];
        if (log.x >= 3.0 && log.x < 4.5) {
            log.state = "panic";
        }

        if (log.x >= 4.5 && log.x < 5.0) {
            log.cutProgress += dt;
            if (Math.random() < 0.35) {
                const lp = toIso(log.x, log.y, log.z);
                particles.push(new Particle(
                    lp.x + (Math.random() - 0.5) * 16,
                    lp.y - 12 + (Math.random() - 0.5) * 8,
                    (Math.random() - 0.5) * 40,
                    -Math.random() * 50 - 20,
                    Math.random() > 0.4 ? "#f6ad55" : "#ecc94b",
                    Math.random() * 3 + 1,
                    0.4
                ));
                audio.playSfx('saw');
            }

            if (log.cutProgress >= cutDuration) {
                logs.splice(i, 1);
                gameState.stats.logsProcessed++;

                const segments = 2 + Math.min(3, Math.floor((gameState.upgrades.sawSpeed || 0) / 10));
                for (let s = 0; s < segments; s++) {
                    planks.push({
                        x: 5.2 + s * 0.2,
                        y: 3.5,
                        z: 0.2,
                        tier: log.tier,
                        targetStack: Math.floor(Math.random() * 3)
                    });
                }
                continue;
            }
        } else {
            log.x += convSpeed * dt;
        }
    }

    // 3. Sorter & Stacking Yard
    const sortSpeedLv = gameState.upgrades.sortSpeed || 0;
    const sortSpeed = (2.0 + sortSpeedLv * 0.2) * speedMult;
    const stackCapLv = gameState.upgrades.stackCap || 0;
    const maxPlanksPerStack = 6 + stackCapLv * 2;

    while (stacks.length < 3) {
        stacks.push({
            x: 8.5,
            y: 3.5 + stacks.length * 1.5,
            count: 0,
            tier: gameState.woodTier
        });
    }

    for (let pIdx = planks.length - 1; pIdx >= 0; pIdx--) {
        const plank = planks[pIdx];
        const targetStack = stacks[plank.targetStack];

        if (plank.x < targetStack.x) {
            plank.x += sortSpeed * dt;
        } else if (plank.y < targetStack.y) {
            plank.y += sortSpeed * dt;
        } else {
            if (targetStack.count < maxPlanksPerStack) {
                targetStack.count++;
                targetStack.tier = plank.tier;
                planks.splice(pIdx, 1);
                audio.playSfx('clunk');
            }
        }
    }

    // 4. Crane System
    const craneSpeedLv = gameState.upgrades.craneSpeed || 0;
    craneTimer += dt * (1 + craneSpeedLv * 0.2) * speedMult;

    const fullStack = stacks.find(s => s.count >= maxPlanksPerStack);
    const numDocks = Math.min(3, Math.max(1, gameState.upgrades.dockCount || 1));

    if (fullStack && trucks.some(t => t.state === "docked" && t.cargoStacks < t.maxCapacity)) {
        if (craneTimer >= 1.5) {
            craneTimer = 0;
            const targetTruck = trucks.find(t => t.state === "docked" && t.cargoStacks < t.maxCapacity);
            if (targetTruck) {
                fullStack.count = 0;
                targetTruck.cargoStacks++;
                audio.playSfx('clunk');

                const cp = toIso(targetTruck.x, targetTruck.y, 0.8);
                floatingTexts.push(new FloatingText(cp.x, cp.y, "📦 Loaded!", "#68d391", 13));
            }
        }
    }

    // 5. Truck Fleet & Highway
    const maxTrucks = Math.min(5, Math.max(1, gameState.upgrades.truckCount || 1));
    const truckCapLv = gameState.upgrades.truckCap || 0;
    const truckCapacity = 2 + Math.floor(truckCapLv / 4);
    const truckSpeedLv = gameState.upgrades.truckSpeed || 0;
    const truckSpeed = (2.2 + truckSpeedLv * 0.25) * speedMult;

    while (trucks.length < maxTrucks) {
        trucks.push({
            x: 14.0,
            y: -2.0 - trucks.length * 2.2,
            cargoStacks: 0,
            maxCapacity: truckCapacity,
            state: "driving_in",
            dockIndex: trucks.length % numDocks,
            color: ["#e53e3e", "#dd6b20", "#3182ce", "#38a169", "#805ad5"][trucks.length % 5],
            onBridge: false
        });
    }

    trucks.forEach(t => {
        t.maxCapacity = truckCapacity;
        const dockY = 4.0 + (t.dockIndex % numDocks) * 2.0;

        if (t.state === "driving_in") {
            if (t.y < dockY) {
                t.y += truckSpeed * dt;
            } else {
                t.state = "docked";
                audio.playSfx('clunk');
            }
        } else if (t.state === "docked") {
            if (t.cargoStacks >= t.maxCapacity) {
                t.state = "leaving";
                audio.playSfx('horn');
            }
        } else if (t.state === "leaving") {
            t.y += truckSpeed * dt;

            if (t.y >= 10.5 && t.y <= 13.0) {
                t.onBridge = true;
                if (!t.splashChecked && Math.random() < 0.015) {
                    t.splashChecked = true;
                    gameState.stats.splashCount++;
                    const tp = toIso(t.x, t.y, 0);
                    floatingTexts.push(new FloatingText(tp.x, tp.y, "💦 SPLASH!", "#63b3ed", 20));
                    audio.playSfx('clunk');
                    for (let k = 0; k < 25; k++) {
                        particles.push(new Particle(tp.x, tp.y, (Math.random() - 0.5) * 80, -Math.random() * 60 - 20, "#bee3f8", 3, 0.8));
                    }
                }
            } else {
                t.onBridge = false;
            }

            if (t.y > 16.0) {
                t.state = "driving_in";
                t.y = -2.0;
                t.splashChecked = false;
                t.onBridge = false;

                const tier = WOOD_TIERS[gameState.woodTier];
                const woodValLv = gameState.upgrades.woodValue || 0;
                const acornMult = 1 + (gameState.goldenAcorns * 0.05);
                const payout = Math.round(
                    t.cargoStacks * 12 * tier.value *
                    (1 + woodValLv * 0.15) *
                    acornMult *
                    speedMult
                );

                t.cargoStacks = 0;
                gameState.coins += payout;
                gameState.totalEarned += payout;
                gameState.stats.deliveries++;

                // Bounce coin bank
                const coinBank = document.getElementById("hud-coin-box");
                if (coinBank) {
                    coinBank.classList.add("bounce");
                    setTimeout(() => coinBank.classList.remove("bounce"), 150);
                }

                audio.playSfx('coin');
                const dp = toIso(14.0, 15.0, 0);
                floatingTexts.push(new FloatingText(dp.x, dp.y - 20, `+$${formatNumber(payout)}`, "#ffcf33", 18));

                for (let c = 0; c < 12; c++) {
                    particles.push(new Particle(
                        dp.x, dp.y - 20,
                        (Math.random() - 0.5) * 70,
                        -Math.random() * 80 - 20,
                        "#ffcf33",
                        Math.random() * 3 + 2,
                        0.7
                    ));
                }
            }
        }
    });

    checkMilestones();
}

function renderGameEntities(dt) {
    const w = mainCanvas.parentElement.clientWidth;
    const h = mainCanvas.parentElement.clientHeight;
    mainCtx.clearRect(0, 0, w, h);

    mainCtx.save();
    mainCtx.translate(camera.x, camera.y);

    // Selected Station Pedestal Ring
    if (selectedStation) {
        const sp = toIso(selectedStation.x, selectedStation.y, 0);
        mainCtx.save();
        mainCtx.strokeStyle = "#ffcf33";
        mainCtx.lineWidth = 3;
        mainCtx.setLineDash([8, 6]);
        mainCtx.lineDashOffset = -Date.now() * 0.02;
        mainCtx.beginPath();
        mainCtx.ellipse(sp.x, sp.y + 10, 42, 22, 0, 0, Math.PI * 2);
        mainCtx.stroke();
        mainCtx.restore();
    }

    // Machinery Housings
    drawIsoBox(mainCtx, 0.5, 3.5, 0, 1.2, 1.2, 0.8, "#4a5568", "#2d3748", "#1a202c");
    drawIsoBox(mainCtx, 2.5, 3.5, 0, 3.2, 0.8, 0.3, "#718096", "#4a5568", "#2d3748");

    const numSaws = Math.min(6, Math.max(1, gameState.upgrades.sawCount || 1));
    for (let s = 0; s < numSaws; s++) {
        const sx = 4.5;
        const sy = 3.2 + (s - (numSaws - 1) / 2) * 0.35;
        drawIsoBox(mainCtx, sx, sy, 0.3, 0.4, 0.4, 0.9, "#a0aec0", "#718096", "#4a5568");

        const sp = toIso(sx, sy, 0.9);
        mainCtx.fillStyle = "#e2e8f0";
        mainCtx.beginPath();
        mainCtx.arc(sp.x, sp.y, 11, 0, Math.PI * 2);
        mainCtx.fill();
        mainCtx.strokeStyle = "#4a5568";
        mainCtx.lineWidth = 2;
        mainCtx.stroke();
    }

    stacks.forEach(st => {
        drawIsoBox(mainCtx, st.x, st.y, 0, 0.9, 0.9, 0.15, "#a0aec0", "#718096", "#4a5568");
        if (st.count > 0) {
            const tier = WOOD_TIERS[st.tier];
            for (let c = 0; c < Math.min(st.count, 12); c++) {
                drawIsoBox(mainCtx, st.x, st.y, 0.15 + c * 0.12, 0.7, 0.7, 0.1, tier.plankColor, tier.barkColor, tier.barkColor);
            }
        }
    });

    const cp = toIso(10.5, 5.0, 0);
    mainCtx.fillStyle = "#e53e3e";
    mainCtx.fillRect(cp.x - 4, cp.y - 45, 8, 45);
    mainCtx.fillRect(cp.x - 30, cp.y - 45, 60, 6);

    logs.forEach(log => drawLogEntity(mainCtx, log));

    planks.forEach(plk => {
        const tier = WOOD_TIERS[plk.tier];
        drawIsoBox(mainCtx, plk.x, plk.y, plk.z, 0.4, 0.3, 0.1, tier.plankColor, tier.barkColor, tier.barkColor);
    });

    trucks.forEach(t => drawTruckEntity(mainCtx, t));

    // Bottleneck Alert
    if (logs.length >= 12) {
        const ap = toIso(4.5, 3.5, 1.2);
        mainCtx.fillStyle = "#f56565";
        mainCtx.font = "bold 16px sans-serif";
        mainCtx.textAlign = "center";
        mainCtx.fillText("⚠️ UPGRADE SAWS!", ap.x, ap.y);
    }

    mainCtx.restore();

    // Overlay Canvas
    uiCtx.clearRect(0, 0, w, h);
    uiCtx.save();
    uiCtx.translate(camera.x, camera.y);

    particles.forEach((p, idx) => {
        p.update(dt);
        p.draw(uiCtx);
        if (p.life <= 0) particles.splice(idx, 1);
    });

    floatingTexts.forEach((ft, idx) => {
        ft.update(dt);
        ft.draw(uiCtx);
        if (ft.life <= 0) floatingTexts.splice(idx, 1);
    });

    uiCtx.restore();
}

// Milestone & Achievement Checks
function checkMilestones() {
    let newlyClaimable = false;
    ACHIEVEMENTS.forEach(ach => {
        if (!gameState.achievements.includes(ach.id) && ach.cond(gameState)) {
            gameState.achievements.push(ach.id);
            gameState.coins += ach.reward;
            showCelebratoryBanner(`🏆 ${ach.name}! +🪙${formatNumber(ach.reward)}`);
            audio.playSfx('milestone');
            newlyClaimable = true;
        }
    });

    if (newlyClaimable) {
        const b = document.getElementById("ach-badge");
        if (b) b.style.display = "block";
    }

    // Wood Tier progression
    if (gameState.woodTier < WOOD_TIERS.length - 1) {
        const nextTier = WOOD_TIERS[gameState.woodTier + 1];
        if (gameState.totalEarned >= nextTier.unlockCost) {
            gameState.woodTier++;
            showCelebratoryBanner(`🪵 Unlocked ${nextTier.name} Wood! Value x${nextTier.value}`);
            audio.playSfx('milestone');
        }
    }
}

function showCelebratoryBanner(msg) {
    const banner = document.getElementById("event-banner");
    if (!banner) return;
    banner.textContent = msg;
    banner.classList.add("show");
    setTimeout(() => banner.classList.remove("show"), 4200);
}

function showToast(msg) {
    const el = document.getElementById("toast-msg");
    if (!el) return;
    el.textContent = msg;
    el.classList.add("show");
    setTimeout(() => el.classList.remove("show"), 3200);
}

// ==========================================
// 8. UPGRADE SYSTEM & LIVE EVENT LISTENERS
// ==========================================
function getUpgradeCost(def, currentLv, mult) {
    let cost = 0;
    let lv = currentLv;
    const targetAdds = mult === "max" ? 100 : Number(mult);

    let count = 0;
    while (count < targetAdds && lv < (def.maxLv || 100)) {
        const singleCost = Math.round(def.baseCost * Math.pow(def.costMult, lv));
        if (mult === "max" && (cost + singleCost > gameState.coins)) break;
        cost += singleCost;
        lv++;
        count++;
    }
    return { cost, levelsToAdd: count };
}

// Create Card DOM nodes once, avoiding DOM destruction on every frame
function initShopCards() {
    const list = document.getElementById("shop-list");
    if (!list) return;
    list.innerHTML = "";
    shopCardsMap.clear();

    UPGRADE_DEFS.forEach(def => {
        const card = document.createElement("div");
        card.className = "upgrade-card";
        card.dataset.id = def.id;
        card.dataset.cat = def.category;

        card.innerHTML = `
            <div class="upgrade-icon-box">${def.icon}</div>
            <div class="upgrade-info">
                <div class="upgrade-title-row">
                    <span class="upgrade-name">${escapeHtml(def.name)}</span>
                    <span class="upgrade-level-tag js-lv">Lv.0</span>
                </div>
                <div class="milestone-bar-wrap">
                    <div class="milestone-track">
                        <div class="milestone-fill js-milestone-fill"></div>
                    </div>
                    <div class="milestone-sub">
                        <span class="js-milestone-label">0/10</span>
                        <span class="milestone-bonus js-milestone-bonus">+2x at Lv.10</span>
                    </div>
                </div>
                <div class="upgrade-stat-row js-stat-row">+15% efficiency</div>
            </div>
            <button class="buy-btn js-buy-btn" data-id="${def.id}">
                <span class="buy-btn-level js-btn-level">+1</span>
                <span class="buy-btn-cost js-btn-cost">🪙 15</span>
                <span class="buy-btn-need js-btn-need" style="display:none;"></span>
            </button>
        `;

        // Direct Event Listener checking live state on click
        const buyBtn = card.querySelector(".js-buy-btn");
        buyBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            handleUpgradeClick(def.id);
        });

        // Clicking card inspects corresponding station
        card.addEventListener("click", () => {
            const st = STATIONS.find(s => s.defId === def.id || s.secondaryDefId === def.id);
            if (st) selectStation(st);
        });

        list.appendChild(card);

        shopCardsMap.set(def.id, {
            card,
            def,
            lvEl: card.querySelector(".js-lv"),
            mFillEl: card.querySelector(".js-milestone-fill"),
            mLabelEl: card.querySelector(".js-milestone-label"),
            mBonusEl: card.querySelector(".js-milestone-bonus"),
            statEl: card.querySelector(".js-stat-row"),
            buyBtn,
            btnLvEl: card.querySelector(".js-btn-level"),
            btnCostEl: card.querySelector(".js-btn-cost"),
            btnNeedEl: card.querySelector(".js-btn-need")
        });
    });

    filterShopCategory(currentCategory);
    updateShopUI();
}

function filterShopCategory(cat) {
    currentCategory = cat;
    document.querySelectorAll(".cat-tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.cat === cat);
    });

    shopCardsMap.forEach(({ card, def }) => {
        const visible = (cat === "all" || def.category === cat);
        card.style.display = visible ? "flex" : "none";
    });
}

// Live update of costs, affordable classes, and progress bars
function updateShopUI() {
    shopCardsMap.forEach(({ card, def, lvEl, mFillEl, mLabelEl, mBonusEl, statEl, buyBtn, btnLvEl, btnCostEl, btnNeedEl }) => {
        const curLv = gameState.upgrades[def.id] || 0;
        const isMax = curLv >= (def.maxLv || 100);
        const { cost, levelsToAdd } = getUpgradeCost(def, curLv, buyMultiplier);
        const canAfford = !isMax && levelsToAdd > 0 && gameState.coins >= cost;

        // Level and Milestone info
        lvEl.textContent = `Lv.${curLv}`;
        const milestone = getMilestoneInfo(curLv, def.maxLv);
        mFillEl.style.width = `${milestone.pct}%`;
        mLabelEl.textContent = isMax ? 'MAXED' : `${curLv}/${milestone.next}`;
        mBonusEl.textContent = milestone.isMaxMilestone ? 'Max Bonus!' : `+2x at Lv.${milestone.next}`;

        // Efficiency text
        const adds = levelsToAdd > 0 ? levelsToAdd : 1;
        statEl.textContent = isMax ? 'Maximum Capacity reached' : `+${adds * 15}% station throughput`;

        // Buy button state
        card.classList.toggle("can-buy", canAfford);
        buyBtn.classList.toggle("can-buy", canAfford);
        buyBtn.classList.toggle("disabled", !canAfford && !isMax);
        buyBtn.classList.toggle("maxed", isMax);

        if (isMax) {
            btnLvEl.textContent = '🌟';
            btnCostEl.textContent = 'MAX';
            btnNeedEl.style.display = 'none';
        } else {
            btnLvEl.textContent = `+${levelsToAdd || 1}`;
            btnCostEl.textContent = `🪙 ${formatNumber(cost)}`;
            if (!canAfford && cost > gameState.coins) {
                btnNeedEl.style.display = 'block';
                btnNeedEl.textContent = `Need ${formatNumber(cost - gameState.coins)}`;
            } else {
                btnNeedEl.style.display = 'none';
            }
        }
    });

    // Update Station Inspector if active
    if (selectedStation) {
        updateInspectorCard(selectedStation);
    }
}

function handleUpgradeClick(defId) {
    const def = UPGRADE_DEFS.find(u => u.id === defId);
    if (!def) return;
    const curLv = gameState.upgrades[defId] || 0;
    const { cost, levelsToAdd } = getUpgradeCost(def, curLv, buyMultiplier);

    if (levelsToAdd > 0 && gameState.coins >= cost) {
        // Successful Purchase
        gameState.coins -= cost;
        const newLv = curLv + levelsToAdd;
        gameState.upgrades[defId] = newLv;
        audio.playSfx('upgrade');

        // Check Milestone reach (Lv 10, 25, 50, 100)
        [10, 25, 50, 100].forEach(m => {
            if (curLv < m && newLv >= m) {
                showCelebratoryBanner(`🎉 MILESTONE! ${def.name} reached Lv.${m}! 2x Speed Boost!`);
                audio.playSfx('milestone');
            }
        });

        // Floating level up text
        const midP = toIso(6, 4, 1.0);
        floatingTexts.push(new FloatingText(midP.x, midP.y, `Level UP! +${levelsToAdd}`, "#48bb78", 20));

        // Confetti Burst
        for (let k = 0; k < 20; k++) {
            particles.push(new Particle(
                midP.x, midP.y,
                (Math.random() - 0.5) * 100,
                -Math.random() * 80 - 30,
                ["#48bb78", "#ecc94b", "#4299e1", "#f56565"][k % 4],
                4,
                0.8
            ));
        }

        updateShopUI();
    } else {
        // Cannot afford -> Shake animation and feedback
        audio.playSfx('error');
        const cardObj = shopCardsMap.get(defId);
        if (cardObj) {
            cardObj.card.classList.add("shake");
            setTimeout(() => cardObj.card.classList.remove("shake"), 400);
        }
        showToast(`Need 🪙 ${formatNumber(cost - gameState.coins)} more coins!`);
    }
}

// ==========================================
// 9. STATION INSPECTOR & CANVAS INTERACTION
// ==========================================
function selectStation(st) {
    selectedStation = st;
    audio.playSfx('tap');

    const insp = document.getElementById("station-inspector");
    insp.classList.add("show");
    updateInspectorCard(st);
}

function updateInspectorCard(st) {
    const insp = document.getElementById("station-inspector");
    if (!insp) return;

    document.getElementById("insp-icon").textContent = st.icon;
    document.getElementById("insp-title").textContent = st.name;

    const def = UPGRADE_DEFS.find(u => u.id === st.defId);
    const lv = gameState.upgrades[st.defId] || 0;
    const isBottleneck = (st.id === "saws" && logs.length >= 10) || (st.id === "yard" && stacks.every(s => s.count >= 8));

    const statusEl = document.getElementById("insp-status");
    if (isBottleneck) {
        statusEl.className = "inspector-status bottleneck";
        statusEl.textContent = "⚠️ Bottleneck Detected!";
    } else {
        statusEl.className = "inspector-status";
        statusEl.textContent = "🟢 Running Smoothly";
    }

    const { cost, levelsToAdd } = getUpgradeCost(def, lv, 1);
    document.getElementById("insp-stats").textContent = `Level ${lv} • Next milestone at Lv.${getMilestoneInfo(lv, def.maxLv).next}`;

    const quickBuyBtn = document.getElementById("insp-quick-buy");
    quickBuyBtn.textContent = `Upgrade (🪙 ${formatNumber(cost)})`;
    quickBuyBtn.onclick = () => {
        handleUpgradeClick(st.defId);
    };
}

function handleCanvasClick(e) {
    const rect = canvasWrapper.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    // Inverse Isometric Coordinates
    const gridPos = fromIso(clickX, clickY);

    // Check if clicked near any defined station
    let clickedStation = null;
    let minDist = 2.0;

    STATIONS.forEach(st => {
        const dist = Math.hypot(st.x - gridPos.x, st.y - gridPos.y);
        if (dist < minDist) {
            minDist = dist;
            clickedStation = st;
        }
    });

    if (clickedStation) {
        selectStation(clickedStation);
    } else {
        // Tapped open ground -> Tap Boost
        applyTapBoost(clickX - camera.x, clickY - camera.y);
    }
}

function applyTapBoost(localX = null, localY = null) {
    tapBoostRemaining = 8;
    gameState.stats.taps++;
    audio.playSfx('tap');

    const spawnX = localX !== null ? localX : toIso(6, 4, 0.5).x;
    const spawnY = localY !== null ? localY : toIso(6, 4, 0.5).y;

    floatingTexts.push(new FloatingText(spawnX, spawnY, "⚡ SPEED BOOST!", "#feb47b", 16));

    // Particle ripple
    for (let k = 0; k < 6; k++) {
        particles.push(new Particle(
            spawnX, spawnY,
            (Math.random() - 0.5) * 60,
            (Math.random() - 0.5) * 40,
            "#f6ad55",
            3,
            0.5
        ));
    }
}

// ==========================================
// 10. MODALS & UI EVENT HANDLERS
// ==========================================
const canvasWrapper = document.getElementById("canvas-wrapper");

function setupUI() {
    // Start Screen Handlers
    const startScreen = document.getElementById("start-screen");
    document.getElementById("btn-start-guest").onclick = () => {
        audio.init();
        const saved = Storage.loadLocal();
        if (saved) gameState = saved;
        startScreen.classList.add("hidden");
        onGameStarted();
    };

    document.getElementById("btn-start-auth").onclick = () => {
        audio.init();
        openModal("modal-auth");
    };

    // Canvas Clicks
    canvasWrapper.addEventListener("click", handleCanvasClick);

    // Inspector Close
    document.getElementById("insp-close").onclick = () => {
        selectedStation = null;
        document.getElementById("station-inspector").classList.remove("show");
    };

    // Category Tabs
    document.querySelectorAll(".cat-tab").forEach(tab => {
        tab.onclick = () => filterShopCategory(tab.dataset.cat);
    });

    // Multiplier Toggle
    document.querySelectorAll(".mult-btn").forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll(".mult-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            buyMultiplier = btn.dataset.mult;
            updateShopUI();
        };
    });

    // Mobile Shop Toggle
    const mobileBtn = document.getElementById("shop-toggle-mobile");
    const shopPanel = document.getElementById("shop-panel");
    mobileBtn.onclick = () => {
        shopPanel.classList.toggle("open");
        mobileBtn.textContent = shopPanel.classList.contains("open") ? "✕ Close" : "🛒 Upgrades";
    };

    // Action Bar Buttons
    document.getElementById("btn-tap-boost").onclick = () => applyTapBoost();
    document.getElementById("btn-watch-boost").onclick = () => {
        watchBoostRemaining = 180;
        showCelebratoryBanner("🎬 2X BOOST ACTIVE FOR 3 MINUTES!");
        audio.playSfx('upgrade');
    };

    document.getElementById("btn-daily").onclick = openDailyChestModal;
    document.getElementById("btn-achievements").onclick = openAchievementsModal;
    document.getElementById("btn-prestige").onclick = openPrestigeModal;

    // Leaderboard
    document.getElementById("btn-open-leaderboard").onclick = openLeaderboardModal;
    document.getElementById("leaderboard-close").onclick = () => closeModal("modal-leaderboard");
    document.getElementById("btn-refresh-leaderboard").onclick = fetchLeaderboard;

    // Wood Tier Click
    document.getElementById("btn-wood-tier").onclick = () => {
        const nextTier = WOOD_TIERS[gameState.woodTier + 1];
        if (nextTier) {
            showToast(`Next Tier: ${nextTier.name} at 🪙${formatNumber(nextTier.unlockCost)} total revenue!`);
        } else {
            showToast("Maximum Wood Tier reached! (Golden Lumber 🌟)");
        }
    };

    // Settings Modal Handlers
    document.getElementById("btn-settings").onclick = () => {
        document.getElementById("setting-server-url").value = gameState.settings.serverUrl || API_CONFIG.BASE_URL;
        document.getElementById("settings-user-display").textContent = currentUser ? currentUser.username : "Guest (Device Only)";
        document.getElementById("btn-logout").style.display = currentUser ? "block" : "none";
        openModal("modal-settings");
    };
    document.getElementById("settings-close").onclick = () => closeModal("modal-settings");

    document.getElementById("toggle-sfx").onclick = (e) => {
        audio.sfxEnabled = !audio.sfxEnabled;
        gameState.settings.sfx = audio.sfxEnabled;
        e.target.textContent = `SFX: ${audio.sfxEnabled ? 'ON' : 'OFF'}`;
        if (audio.sfxEnabled) audio.playSfx('coin');
    };

    document.getElementById("toggle-music").onclick = (e) => {
        audio.musicEnabled = !audio.musicEnabled;
        gameState.settings.music = audio.musicEnabled;
        e.target.textContent = `Music: ${audio.musicEnabled ? 'ON' : 'OFF'}`;
        if (audio.musicEnabled) audio.startMusic();
    };

    document.getElementById("btn-sync-now").onclick = () => {
        Storage.saveLocal();
        Storage.syncToCloud();
        showToast("Progress Synced to Cloud!");
    };

    document.getElementById("btn-logout").onclick = () => {
        currentUser = null;
        localStorage.removeItem(Storage.ACTIVE_USER_KEY);
        gameState = createDefaultState();
        closeModal("modal-settings");
        startScreen.classList.remove("hidden");
    };

    document.getElementById("btn-reset-save").onclick = () => {
        if (confirm("Reset all game data? This cannot be undone!")) {
            localStorage.clear();
            location.reload();
        }
    };

    // Auth Handlers
    document.getElementById("auth-close").onclick = () => closeModal("modal-auth");
    document.getElementById("pwd-toggle").onclick = () => {
        const f = document.getElementById("auth-password");
        f.type = f.type === "password" ? "text" : "password";
    };
    document.getElementById("btn-do-login").onclick = () => performAuth(false);
    document.getElementById("btn-do-register").onclick = () => performAuth(true);
}

function openModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add("active");
}
function closeModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove("active");
}

// Daily Chest Modal
function openDailyChestModal() {
    const grid = document.getElementById("daily-grid");
    grid.innerHTML = "";
    const streak = gameState.dailyStreak || 0;
    const canClaim = (Date.now() - (gameState.lastDailyClaim || 0)) > 20 * 3600 * 1000;

    DAILY_REWARDS.forEach((r, idx) => {
        const isClaimed = idx < (streak % 7);
        const isToday = idx === (streak % 7);
        const card = document.createElement("div");
        card.className = `daily-day-card ${isClaimed ? 'claimed' : ''} ${isToday ? 'today' : ''} ${r.isMega ? 'mega' : ''}`;
        card.innerHTML = `
            <div style="font-weight:800;">Day ${r.day}</div>
            <div style="font-size:24px;">${r.isMega ? '🏆' : (isClaimed ? '✓' : '🎁')}</div>
            <div style="color:var(--gold); font-weight:800;">+🪙${formatNumber(r.coins)}</div>
            ${r.acorns ? `<div style="color:var(--gold); font-size:10px;">+🌰${r.acorns}</div>` : ''}
        `;
        grid.appendChild(card);
    });

    const claimBtn = document.getElementById("btn-claim-daily");
    claimBtn.disabled = !canClaim;
    claimBtn.textContent = canClaim ? "Claim Today's Chest" : "Come back tomorrow!";

    claimBtn.onclick = () => {
        if (!canClaim) return;
        const reward = DAILY_REWARDS[streak % 7];
        gameState.coins += reward.coins;
        gameState.totalEarned += reward.coins;
        if (reward.acorns) gameState.goldenAcorns += reward.acorns;
        gameState.dailyStreak++;
        gameState.lastDailyClaim = Date.now();
        audio.playSfx('milestone');
        showCelebratoryBanner(`🎁 Claimed Day ${reward.day}! +🪙${formatNumber(reward.coins)}`);
        closeModal("modal-daily");
        document.getElementById("daily-badge").style.display = "none";
    };

    document.getElementById("btn-close-daily").onclick = () => closeModal("modal-daily");
    openModal("modal-daily");
}

// Achievements Modal
function openAchievementsModal() {
    const list = document.getElementById("achievements-list");
    list.innerHTML = "";
    const badge = document.getElementById("ach-badge");
    if (badge) badge.style.display = "none";

    let completedCount = 0;
    ACHIEVEMENTS.forEach(ach => {
        const isDone = gameState.achievements.includes(ach.id);
        if (isDone) completedCount++;

        const card = document.createElement("div");
        card.className = `ach-card ${isDone ? 'completed' : ''}`;
        card.innerHTML = `
            <div class="ach-icon">${ach.icon || '🎖️'}</div>
            <div class="ach-info">
                <div class="ach-title">${escapeHtml(ach.name)}</div>
                <div class="ach-desc">${escapeHtml(ach.desc)}</div>
                <div class="ach-reward">+🪙 ${formatNumber(ach.reward)} Coins</div>
            </div>
            <div class="ach-status-badge ${isDone ? 'claimed' : ''}">
                ${isDone ? '✓ Claimed' : 'Locked'}
            </div>
        `;
        list.appendChild(card);
    });

    document.getElementById("ach-summary-text").textContent = `Unlocked ${completedCount} / ${ACHIEVEMENTS.length} Achievements`;
    document.getElementById("achievements-close").onclick = () => closeModal("modal-achievements");
    openModal("modal-achievements");
}

// Leaderboard Modal & API Fetch
async function openLeaderboardModal() {
    openModal("modal-leaderboard");
    await fetchLeaderboard();
}

async function fetchLeaderboard() {
    const list = document.getElementById("leaderboard-list");
    list.innerHTML = `<div style="text-align:center; padding: 20px; color: var(--text-sub);">Connecting to mill network...</div>`;
    const url = (gameState.settings.serverUrl || API_CONFIG.BASE_URL) + API_CONFIG.LEADERBOARD.path;

    try {
        const resp = await fetch(url, { method: "GET" });
        const data = await resp.json();
        if (data.ok && data.leaderboard && data.leaderboard.length > 0) {
            list.innerHTML = "";
            data.leaderboard.forEach((user, idx) => {
                const isMe = currentUser && currentUser.username.toLowerCase() === user.username.toLowerCase();
                const rankIcons = ["🥇", "🥈", "🥉"];
                const rankLabel = idx < 3 ? rankIcons[idx] : `#${idx + 1}`;

                const row = document.createElement("div");
                row.className = `leader-row ${isMe ? 'me' : ''}`;
                row.innerHTML = `
                    <div class="leader-rank">${rankLabel}</div>
                    <div class="leader-name">${escapeHtml(user.username)} ${isMe ? '(You)' : ''}</div>
                    <div class="leader-score">🪙 $${formatNumber(user.totalEarned || user.coins || 0)}</div>
                `;
                list.appendChild(row);
            });
        } else {
            list.innerHTML = `<div style="text-align:center; padding: 20px; color: var(--text-sub);">No records yet. Be the first tycoon!</div>`;
        }
    } catch(e) {
        list.innerHTML = `
            <div style="text-align:center; padding: 20px; color: #fc8181;">
                Could not reach cloud leaderboard.<br>
                <small style="color:var(--text-sub);">Check Wi-Fi or server tunnel status.</small>
            </div>
        `;
    }
}

// Prestige (Forest Reset)
function openPrestigeModal() {
    const acornsToGain = Math.max(0, Math.floor(Math.sqrt((gameState.totalEarned || 0) / 10000)) - (gameState.goldenAcorns || 0));
    const nextBoost = (gameState.goldenAcorns + acornsToGain) * 5;

    document.getElementById("prestige-acorns-gain").textContent = `+${acornsToGain} Golden Acorns`;
    document.getElementById("prestige-boost-gain").textContent = `+${nextBoost}% Global Profit Forever`;

    document.getElementById("btn-do-prestige").onclick = () => {
        if (acornsToGain <= 0) {
            showToast("Earn more coins to unlock Golden Acorns on reset!");
            return;
        }

        gameState.goldenAcorns += acornsToGain;
        gameState.prestigeCount++;
        gameState.coins = 0;
        gameState.upgrades = createDefaultState().upgrades;
        logs = [];
        planks = [];
        trucks = [];

        audio.playSfx('milestone');
        showCelebratoryBanner(`🌲 Forest Replanted! +${acornsToGain} Golden Acorns Claimed!`);
        closeModal("modal-prestige");
        updateShopUI();
    };

    document.getElementById("prestige-close").onclick = () => closeModal("modal-prestige");
    document.getElementById("btn-cancel-prestige").onclick = () => closeModal("modal-prestige");
    openModal("modal-prestige");
}

// Authentication Workflow
async function performAuth(isRegister) {
    const userField = document.getElementById("auth-username");
    const pwdField = document.getElementById("auth-password");
    const msg = document.getElementById("auth-msg");

    const username = userField.value.trim();
    const password = pwdField.value;

    if (username.length < 3 || username.length > 20) {
        msg.className = "inline-msg error";
        msg.textContent = "Username must be 3-20 characters.";
        return;
    }
    if (password.length < 6) {
        msg.className = "inline-msg error";
        msg.textContent = "Password must be at least 6 characters.";
        return;
    }

    const passwordHash = await sha256(password);
    pwdField.value = "";

    const url = (gameState.settings.serverUrl || API_CONFIG.BASE_URL) + API_CONFIG.AUTH.path;
    try {
        const resp = await fetch(url, {
            method: API_CONFIG.AUTH.method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, passwordHash, isRegister })
        });
        const data = await resp.json();

        if (!data.ok) {
            msg.className = "inline-msg error";
            msg.textContent = data.error || "Authentication failed.";
            return;
        }

        currentUser = {
            username: data.user.username,
            passwordHash,
            token: data.token
        };

        closeModal("modal-auth");
        document.getElementById("start-screen").classList.add("hidden");

        const localSave = Storage.loadLocal(username);
        const cloudSave = data.save;

        if (cloudSave && cloudSave.totalEarned && localSave && localSave.totalEarned && Math.abs(cloudSave.totalEarned - localSave.totalEarned) > 100) {
            showConflictDialog(cloudSave, localSave);
        } else if (cloudSave && cloudSave.totalEarned) {
            gameState = cloudSave;
            onGameStarted();
        } else {
            if (localSave) gameState = localSave;
            Storage.syncToCloud();
            onGameStarted();
        }
    } catch (e) {
        msg.className = "inline-msg error";
        msg.textContent = "Cannot reach server. Check address or Cloudflare tunnel.";
    }
}

function showConflictDialog(cloudSave, localSave) {
    const details = document.getElementById("conflict-details");
    details.innerHTML = `
        <div>☁️ <strong>Cloud Save:</strong> $${formatNumber(cloudSave.totalEarned || 0)} total earned</div>
        <div style="margin-top:4px;">📱 <strong>Local Save:</strong> $${formatNumber(localSave.totalEarned || 0)} total earned</div>
    `;

    document.getElementById("btn-keep-cloud").onclick = () => {
        gameState = cloudSave;
        closeModal("modal-conflict");
        onGameStarted();
    };

    document.getElementById("btn-keep-local").onclick = () => {
        gameState = localSave;
        Storage.syncToCloud();
        closeModal("modal-conflict");
        onGameStarted();
    };

    document.getElementById("btn-keep-richer").onclick = () => {
        gameState = (cloudSave.totalEarned || 0) >= (localSave.totalEarned || 0) ? cloudSave : localSave;
        Storage.syncToCloud();
        closeModal("modal-conflict");
        onGameStarted();
    };

    openModal("modal-conflict");
}

function onGameStarted() {
    document.getElementById("badge-user").textContent = currentUser ? `👤 ${escapeHtml(currentUser.username)}` : "👤 Guest";
    initShopCards();

    // Offline Earnings
    if (gameState.lastSaveTime) {
        const elapsedSec = Math.min(API_CONFIG.OFFLINE_MAX_HOURS * 3600, (Date.now() - gameState.lastSaveTime) / 1000);
        if (elapsedSec > 60) {
            const offlineRate = Math.max(2, (gameState.stats.deliveries > 0 ? (gameState.totalEarned / Math.max(60, gameState.stats.playTime)) : 5) * 0.4);
            const earned = Math.round(elapsedSec * offlineRate);
            if (earned > 20) {
                document.getElementById("offline-earned-val").textContent = formatNumber(earned);
                openModal("modal-welcome");
                document.getElementById("btn-claim-offline").onclick = () => {
                    gameState.coins += earned;
                    gameState.totalEarned += earned;
                    closeModal("modal-welcome");
                    audio.playSfx('coin');
                };
            }
        }
    }

    // Auto-save interval
    setInterval(() => {
        Storage.saveLocal();
        Storage.syncToCloud();
    }, API_CONFIG.SAVE_INTERVAL_MS);

    // Random Tycoon Events
    setInterval(triggerRandomEvent, 45000);

    setTimeout(() => {
        const tut = document.getElementById("tutorial-toast");
        if (tut) tut.style.display = "none";
    }, 12000);
}

function triggerRandomEvent() {
    const roll = Math.random();
    if (roll < 0.45) {
        rushHourRemaining = 30;
        showCelebratoryBanner("⚡ RUSH HOUR! 2X PRODUCTION SPEED FOR 30s!");
        audio.playSfx('upgrade');
    } else if (roll < 0.8) {
        logs.push({
            x: 0.5,
            y: 3.5,
            z: 0.2,
            tier: 4,
            state: "happy",
            cutProgress: 0,
            id: Math.random()
        });
        showToast("⭐ A Rare Golden Log entered the conveyor!");
        gameState.stats.goldenLogs++;
    }
}

// ==========================================
// 11. MAIN ANIMATION LOOP
// ==========================================
let lastFrameTime = performance.now();

function gameLoop(time) {
    const dt = Math.min((time - lastFrameTime) / 1000, 0.1);
    lastFrameTime = time;

    if (!document.hidden) {
        gameState.stats.playTime += dt;
        if (tapBoostRemaining > 0) tapBoostRemaining = Math.max(0, tapBoostRemaining - dt);
        if (watchBoostRemaining > 0) watchBoostRemaining = Math.max(0, watchBoostRemaining - dt);
        if (rushHourRemaining > 0) rushHourRemaining = Math.max(0, rushHourRemaining - dt);

        updateProductionLine(dt);
        renderGameEntities(dt);

        // Update Top HUD
        document.getElementById("coin-counter").textContent = formatNumber(gameState.coins);
        document.getElementById("acorn-count").textContent = gameState.goldenAcorns;

        // Wood Tier Progression Bar in HUD
        const curTier = WOOD_TIERS[gameState.woodTier];
        document.getElementById("badge-tier-name").textContent = `🪵 ${curTier.name} Mill`;
        document.getElementById("badge-tier-mult").textContent = `x${curTier.value} Value`;

        const nextTier = WOOD_TIERS[gameState.woodTier + 1];
        if (nextTier) {
            const prevCost = curTier.unlockCost;
            const targetCost = nextTier.unlockCost;
            const pct = Math.min(100, Math.max(0, ((gameState.totalEarned - prevCost) / (targetCost - prevCost)) * 100));
            document.getElementById("wood-tier-fill").style.width = `${pct}%`;
            document.getElementById("wood-next-label").textContent = `Next: ${nextTier.name} Wood (${formatNumber(targetCost)} coins)`;
        } else {
            document.getElementById("wood-tier-fill").style.width = "100%";
            document.getElementById("wood-next-label").textContent = "🌟 Maximum Wood Tier!";
        }

        // Approximate income rate
        const approxRate = (1.5 + (gameState.upgrades.convSpeed || 0) * 0.15) * 4 * curTier.value * (1 + (gameState.upgrades.woodValue || 0) * 0.15) * (1 + gameState.goldenAcorns * 0.05);
        document.getElementById("income-counter").textContent = `+$${formatNumber(approxRate)}/s`;

        // Update Upgrade Shop Affordance in real time
        updateShopUI();
    }

    requestAnimationFrame(gameLoop);
}

// Lifecycle Init
window.addEventListener("beforeunload", () => {
    Storage.saveLocal();
});

document.addEventListener("visibilitychange", () => {
    if (document.hidden) Storage.saveLocal();
});

window.addEventListener("DOMContentLoaded", () => {
    resizeCanvases();
    setupUI();
    requestAnimationFrame(gameLoop);

    // Auto-login if remembered
    try {
        const raw = localStorage.getItem(Storage.ACTIVE_USER_KEY);
        if (raw) {
            currentUser = JSON.parse(raw);
            const saved = Storage.loadLocal();
            if (saved) gameState = saved;
            document.getElementById("start-screen").classList.add("hidden");
            onGameStarted();
        }
    } catch(e) {}
});
</script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated index.html ({len(html_content)} bytes)")

