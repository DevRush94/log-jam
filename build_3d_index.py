# -*- coding: utf-8 -*-
"""
Generator for Log Jam - 1000x Stunning 3D WebGL / Three.js Overhaul
Matches Idle Lumber Empire / YouTube Shorts reference:
- Full 3D low-poly stylized models (trees, trucks, saws, crane, logs, cargo ship)
- Studio daylight with soft directional shadows
- Skyscraper lumber tower growing in 3D
- Traffic jam gridlock with 3D angry emoji bubbles (😡)
- In-world 3D upgrade pads clickable via raycasting
- Balanced, fast-paced idle economy with immediate dopamine progression
- Integrated FastAPI / Termux phone cloud save backend & leaderboard
"""

html_3d = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Log Jam: Mill Empire 3D</title>
    <!-- Three.js Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --panel-bg: rgba(15, 23, 42, 0.94);
            --panel-border: rgba(255, 255, 255, 0.12);
            --cash-green: #10b981;
            --cash-glow: rgba(16, 185, 129, 0.5);
            --gold: #f59e0b;
            --gold-glow: rgba(245, 158, 11, 0.45);
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
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
            background: #dbeafe;
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

        /* 3D WebGL Canvas Viewport */
        #webgl-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            outline: none;
            cursor: pointer;
        }

        /* 2D Overlay Canvas for Particles & Floating Texts */
        #overlay-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 2;
            pointer-events: none;
        }

        /* Top HUD Bar */
        .hud-top {
            position: absolute;
            top: 14px;
            left: 14px;
            right: 14px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            z-index: 10;
            pointer-events: none;
            gap: 12px;
        }

        .hud-left {
            display: flex;
            flex-direction: column;
            gap: 8px;
            pointer-events: auto;
        }

        .hud-row {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }

        /* YouTube Shorts Reference Money Pill */
        .cash-pill-box {
            background: rgba(15, 23, 42, 0.92);
            border: 2.5px solid #10b981;
            border-radius: 24px;
            padding: 8px 22px;
            display: flex;
            align-items: center;
            gap: 12px;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4), 0 0 18px var(--cash-glow);
            pointer-events: auto;
            min-width: 160px;
            transition: transform 0.12s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .cash-pill-box.bounce {
            transform: scale(1.12);
        }
        .cash-icon-badge {
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff;
            font-size: 15px;
            font-weight: 900;
            padding: 3px 9px;
            border-radius: 10px;
            letter-spacing: -0.5px;
            box-shadow: 0 2px 6px rgba(16, 185, 129, 0.4);
        }
        .cash-digits {
            font-size: 26px;
            font-weight: 900;
            color: #fff;
            letter-spacing: 0.5px;
            text-shadow: 0 2px 6px rgba(0,0,0,0.6);
        }
        .cash-rate-tag {
            font-size: 11px;
            font-weight: 800;
            color: #34d399;
            margin-top: 1px;
        }

        .hud-pill {
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid var(--panel-border);
            padding: 8px 14px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            font-weight: 800;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
        }
        .hud-pill:hover {
            transform: translateY(-2px);
            background: rgba(30, 41, 59, 0.95);
        }
        .hud-pill.tier {
            background: linear-gradient(135deg, #78350f, #451a03);
            border-color: #d97706;
            color: #fde68a;
        }
        .hud-pill.acorns {
            color: var(--gold);
            border-color: var(--gold-glow);
        }
        .hud-pill.leaderboard {
            color: #fef08a;
            border-color: rgba(254, 240, 138, 0.4);
        }
        .hud-pill.sync-status {
            font-size: 11px;
            color: var(--text-sub);
            cursor: default;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 6px #10b981;
        }
        .status-dot.syncing {
            background: #eab308;
            box-shadow: 0 0 6px #eab308;
            animation: pulse-dot 1s infinite;
        }
        .status-dot.offline {
            background: #ef4444;
            box-shadow: 0 0 6px #ef4444;
        }
        @keyframes pulse-dot {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.6; }
        }

        /* Traffic Jam Banner */
        #traffic-alert {
            position: absolute;
            top: 78px;
            left: 50%;
            transform: translateX(-50%) translateY(-150%);
            background: linear-gradient(135deg, #ef4444, #dc2626);
            border: 2px solid #fff;
            border-radius: 20px;
            padding: 8px 22px;
            font-size: 14px;
            font-weight: 900;
            color: #fff;
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.55);
            z-index: 15;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: none;
        }
        #traffic-alert.show {
            transform: translateX(-50%) translateY(0);
        }

        #event-banner {
            position: absolute;
            top: 72px;
            left: 50%;
            transform: translateX(-50%) translateY(-150%);
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #fff;
            padding: 10px 24px;
            border-radius: 24px;
            font-size: 15px;
            font-weight: 900;
            box-shadow: 0 8px 30px rgba(245, 158, 11, 0.6);
            z-index: 30;
            pointer-events: none;
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        #event-banner.show {
            transform: translateX(-50%) translateY(0);
        }

        /* Bottom Action Bar */
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
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid var(--panel-border);
            color: var(--text-main);
            padding: 9px 15px;
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
        }
        .pill-btn:hover {
            transform: translateY(-2px);
            border-color: rgba(255,255,255,0.35);
            background: rgba(30, 41, 59, 0.95);
        }
        .pill-btn:active {
            transform: translateY(1px);
        }
        .pill-btn.boost-btn {
            background: linear-gradient(135deg, #ef4444, #f97316);
            border: none;
            color: #fff;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.45);
        }

        /* 3D Upgrade Drawer & Mobile Bottom Sheet */
        #shop-panel {
            width: 420px;
            height: 100%;
            background: var(--panel-bg);
            border-left: 1px solid var(--panel-border);
            display: flex;
            flex-direction: column;
            z-index: 20;
            box-shadow: -8px 0 35px rgba(0,0,0,0.6);
            backdrop-filter: blur(14px);
            transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        }

        .shop-header {
            padding: 14px 18px 10px;
            border-bottom: 1px solid var(--panel-border);
            display: flex;
            flex-direction: column;
            gap: 10px;
            background: rgba(15, 23, 42, 0.7);
        }

        .shop-title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .shop-title {
            font-size: 17px;
            font-weight: 900;
            color: #fde68a;
            display: flex;
            align-items: center;
            gap: 8px;
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
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
        }

        .category-tabs {
            display: flex;
            gap: 6px;
            overflow-x: auto;
            padding-bottom: 2px;
        }
        .category-tabs::-webkit-scrollbar { display: none; }
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
        .cat-tab:hover { color: #fff; background: rgba(255,255,255,0.12); }
        .cat-tab.active {
            background: #10b981;
            color: #fff;
            border-color: #10b981;
            font-weight: 800;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
        }

        .shop-list {
            flex: 1;
            overflow-y: auto;
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .shop-list::-webkit-scrollbar { width: 6px; }
        .shop-list::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.15);
            border-radius: 3px;
        }

        /* 3D Upgrade Card */
        .upgrade-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.75), rgba(15, 23, 42, 0.85));
            border: 1px solid var(--panel-border);
            border-radius: 14px;
            padding: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
            position: relative;
        }
        .upgrade-card:hover {
            border-color: rgba(255,255,255,0.25);
            box-shadow: 0 6px 16px rgba(0,0,0,0.45);
        }
        .upgrade-card.can-buy {
            border-color: rgba(16, 185, 129, 0.45);
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
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
            color: #fde68a;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 1px 6px;
            border-radius: 8px;
            white-space: nowrap;
        }

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
            background: linear-gradient(90deg, #10b981, #f59e0b);
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
            color: #fde68a;
            font-weight: 700;
        }

        .upgrade-stat-row {
            font-size: 11px;
            color: #34d399;
            font-weight: 600;
        }

        /* 3D Tactile Buy Button */
        .buy-btn {
            position: relative;
            background: linear-gradient(180deg, #10b981 0%, #047857 100%);
            border: none;
            color: #fff;
            padding: 8px 12px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 900;
            cursor: pointer;
            box-shadow: 0 4px 0 #065f46, 0 6px 14px rgba(0,0,0,0.4);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-width: 90px;
            transition: transform 0.1s ease, box-shadow 0.1s ease;
            flex-shrink: 0;
        }
        .buy-btn:active {
            transform: translateY(3px);
            box-shadow: 0 1px 0 #065f46, 0 2px 6px rgba(0,0,0,0.4);
        }
        .buy-btn.can-buy {
            background: linear-gradient(180deg, #34d399 0%, #059669 100%);
            box-shadow: 0 4px 0 #047857, 0 6px 14px var(--cash-glow);
            animation: pulse-green 2s infinite;
        }
        @keyframes pulse-green {
            0%, 100% { box-shadow: 0 4px 0 #047857, 0 6px 14px var(--cash-glow); }
            50% { box-shadow: 0 4px 0 #047857, 0 8px 22px rgba(52, 211, 153, 0.85); }
        }
        .buy-btn.disabled {
            background: #1e293b;
            color: #64748b;
            cursor: pointer;
            box-shadow: 0 3px 0 #0f172a;
            opacity: 0.75;
            animation: none;
        }
        .buy-btn.maxed {
            background: linear-gradient(180deg, #f59e0b, #b45309);
            color: #fff;
            box-shadow: 0 4px 0 #78350f;
            cursor: default;
        }
        .buy-btn-level { font-size: 11px; opacity: 0.9; }
        .buy-btn-cost { font-size: 13px; display: flex; align-items: center; gap: 3px; }
        .buy-btn-need { font-size: 9px; color: #f87171; font-weight: 600; }

        /* Mobile Bottom Sheet */
        #shop-toggle-mobile {
            display: none;
            position: absolute;
            bottom: 14px;
            right: 14px;
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff;
            border: none;
            padding: 11px 20px;
            border-radius: 26px;
            font-weight: 900;
            font-size: 14px;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
            z-index: 10;
            cursor: pointer;
        }

        /* Modals */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.8);
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
        .modal-overlay.active { opacity: 1; pointer-events: auto; }
        .modal-card {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid var(--panel-border);
            border-radius: 22px;
            width: 100%;
            max-width: 460px;
            max-height: 85vh;
            overflow-y: auto;
            padding: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.7);
            display: flex;
            flex-direction: column;
            gap: 16px;
            position: relative;
            transform: scale(0.92);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .modal-overlay.active .modal-card { transform: scale(1); }
        .modal-header { display: flex; justify-content: space-between; align-items: center; }
        .modal-title { font-size: 20px; font-weight: 900; display: flex; align-items: center; gap: 8px; color: #fde68a; }
        .close-btn { background: none; border: none; color: var(--text-sub); font-size: 24px; cursor: pointer; padding: 4px; }
        .close-btn:hover { color: #fff; }

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
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        }
        .btn-primary:hover { filter: brightness(1.1); transform: translateY(-2px); }
        .btn-secondary {
            background: rgba(255,255,255,0.08);
            color: #fff;
            border: 1px solid var(--panel-border);
        }
        .btn-secondary:hover { background: rgba(255,255,255,0.16); }
        .btn-danger {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }

        .input-group { display: flex; flex-direction: column; gap: 6px; }
        .input-group label { font-size: 11px; font-weight: 800; color: var(--text-sub); text-transform: uppercase; }
        .input-field {
            width: 100%;
            background: rgba(0,0,0,0.35);
            border: 1px solid var(--panel-border);
            border-radius: 12px;
            padding: 12px 14px;
            color: #fff;
            font-size: 14px;
            outline: none;
        }
        .input-field:focus { border-color: #10b981; }
        .modal-btn-row { display: flex; gap: 10px; margin-top: 6px; }

        /* Start Screen */
        #start-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: radial-gradient(circle at center, #1e293b 0%, #090d16 100%);
            z-index: 200;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px;
            transition: opacity 0.5s ease;
        }
        #start-screen.hidden { opacity: 0; pointer-events: none; }
        .logo-box { text-align: center; margin-bottom: 36px; }
        .logo-main {
            font-size: 52px;
            font-weight: 900;
            background: linear-gradient(135deg, #fef08a 0%, #f59e0b 50%, #b45309 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
            margin-bottom: 6px;
        }
        .logo-sub { font-size: 16px; font-weight: 800; color: #94a3b8; letter-spacing: 4px; text-transform: uppercase; }
        .start-btn-box { display: flex; flex-direction: column; gap: 14px; width: 100%; max-width: 320px; }
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
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff;
            box-shadow: 0 6px 25px rgba(16, 185, 129, 0.45);
        }
        .btn-huge.guest:hover { transform: translateY(-2px); box-shadow: 0 10px 35px rgba(16, 185, 129, 0.65); }
        .btn-huge.auth {
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
            border: 1px solid var(--panel-border);
        }

        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: rgba(15, 23, 42, 0.96);
            border: 2px solid #10b981;
            border-radius: 30px;
            padding: 10px 24px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #fff;
            font-weight: 800;
            font-size: 14px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.6);
            z-index: 150;
            pointer-events: none;
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .toast.show { transform: translateX(-50%) translateY(0); }

        #tutorial-toast {
            position: absolute;
            bottom: 78px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.95);
            border: 2px solid #10b981;
            border-radius: 16px;
            padding: 10px 22px;
            font-size: 13px;
            font-weight: 800;
            color: #34d399;
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
            #shop-panel.open { transform: translateY(0); }
            #shop-toggle-mobile { display: block; }
            .hud-top { flex-direction: column; align-items: stretch; }
            .cash-pill-box { align-self: flex-end; }
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- Three.js 3D Viewport -->
    <canvas id="webgl-canvas"></canvas>
    <canvas id="overlay-canvas"></canvas>

    <!-- Top HUD -->
    <div class="hud-top">
        <div class="hud-left">
            <div class="hud-row">
                <!-- Wood Tier Banner -->
                <div class="hud-pill tier" id="btn-wood-tier" title="Wood Tier & Progress">
                    <span id="badge-tier-name">🪵 Pine Mill</span>
                    <span style="font-size:11px; opacity:0.85;" id="badge-tier-mult">x1.0</span>
                </div>

                <!-- Acorns -->
                <div class="hud-pill acorns" id="badge-acorns" title="Golden Acorns">
                    🌰 <span id="acorn-count">0</span>
                </div>

                <!-- Leaderboard -->
                <div class="hud-pill leaderboard" id="btn-open-leaderboard" title="Top Tycoons">
                    🏆 Leaderboard
                </div>

                <!-- Sync Status -->
                <div class="hud-pill sync-status" id="badge-sync" title="Save Status">
                    <span class="status-dot" id="sync-dot"></span>
                    <span id="badge-user">👤 Guest</span>
                    <span id="sync-text">✓ Saved</span>
                </div>
            </div>
        </div>

        <!-- YouTube Shorts Reference Money Pill [ 💵 22,450 ] -->
        <div class="cash-pill-box" id="hud-coin-box">
            <span class="cash-icon-badge">💵</span>
            <div>
                <div class="cash-digits" id="coin-counter">0</div>
                <div class="cash-rate-tag" id="income-counter">+💵 0/s</div>
            </div>
        </div>
    </div>

    <!-- Traffic Jam Alert Banner -->
    <div id="traffic-alert">
        <span>🚨 TRAFFIC JAM! Upgrade Docks or Road to clear the queue!</span>
    </div>

    <!-- Event Banner -->
    <div id="event-banner">⚡ RUSH HOUR! 2X SPEED!</div>

    <!-- Interactive 3-Step Guided Tutorial Hint -->
    <div id="tutorial-toast">👆 Step 1/3: Tap anywhere on the mill to boost speed!</div>

    <!-- Bottom Actions -->
    <div class="action-pills">
        <button class="pill-btn boost-btn" id="btn-tap-boost">⚡ Boost (Tap!)</button>
        <button class="pill-btn" id="btn-watch-boost">🎬 2x Boost (3m)</button>
        <button class="pill-btn" id="btn-daily">🎁 Daily Chest</button>
        <button class="pill-btn" id="btn-achievements">🎖️ Achievements</button>
        <button class="pill-btn" id="btn-prestige">🌰 Forest Reset</button>
        <button class="pill-btn" id="btn-settings">⚙️ Settings</button>
    </div>

    <button id="shop-toggle-mobile">🛒 Upgrades</button>

    <!-- Shop Sidebar -->
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
        <div class="logo-main">LOG JAM 3D</div>
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
        <div id="auth-msg" style="display:none; font-size:13px; padding:8px; border-radius:8px;"></div>
        <div class="input-group">
            <label>Username</label>
            <input type="text" class="input-field" id="auth-username" placeholder="3-20 characters" autocomplete="username">
        </div>
        <div class="input-group">
            <label>Password</label>
            <div style="position:relative; display:flex; align-items:center;">
                <input type="password" class="input-field" id="auth-password" placeholder="At least 6 characters" autocomplete="current-password">
                <button id="pwd-toggle" style="position:absolute; right:12px; background:none; border:none; color:var(--text-sub); cursor:pointer;">👁</button>
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
        <div class="input-group">
            <label>Backend / Cloud Server URL</label>
            <input type="text" class="input-field" id="setting-server-url" placeholder="https://customs-wins-wallace-ultimately.trycloudflare.com">
        </div>
        <div>
            <div style="font-size:13px; color:var(--text-sub); margin-bottom:8px;">
                Account: <strong id="settings-user-display" style="color:#fff;">Guest</strong>
            </div>
            <div class="modal-btn-row">
                <button class="btn-full btn-secondary" id="btn-sync-now">☁️ Sync Now</button>
                <button class="btn-full btn-secondary" id="btn-logout" style="display:none;">Logout</button>
            </div>
        </div>
        <div style="border-top:1px solid var(--panel-border); padding-top:12px;">
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
        <div id="leaderboard-list" style="display:flex; flex-direction:column; gap:6px; max-height:50vh; overflow-y:auto;">
            <div style="text-align:center; padding:20px; color:var(--text-sub);">Loading leaderboard...</div>
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
        <div id="achievements-list" style="display:flex; flex-direction:column; gap:8px; max-height:55vh; overflow-y:auto;"></div>
    </div>
</div>

<!-- Daily Chest Modal -->
<div class="modal-overlay" id="modal-daily">
    <div class="modal-card" style="text-align: center;">
        <div style="font-size: 46px; margin-bottom: 6px;">🎁</div>
        <div class="modal-title" style="justify-content: center;">Daily Lumber Chest</div>
        <p style="font-size: 13px; color: var(--text-sub); margin: 6px 0;" id="daily-streak-text">
            Day Streak: 1
        </p>
        <div style="font-size: 24px; font-weight: 800; color: #10b981; margin: 12px 0;" id="daily-reward-preview">
            +💵 1,000 Cash
        </div>
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
            Replant your forest and begin a fresh operation! You will reset cash and station levels, but gain permanent <strong>Golden Acorns</strong>.
        </p>
        <div style="background: rgba(245,158,11,0.1); border: 1px solid var(--gold-glow); padding: 14px; border-radius: 14px; text-align:center;">
            <div style="font-size: 11px; color: var(--text-sub); text-transform: uppercase; font-weight: 800;">Permanent Rewards</div>
            <div style="font-size: 28px; font-weight: 900; color: var(--gold); margin: 6px 0;" id="prestige-acorns-gain">+0 Acorns</div>
            <div style="font-size: 13px; color: #10b981; font-weight: 700;" id="prestige-boost-gain">+0% Global Profit Forever</div>
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
 * LOG JAM 3D: MILL EMPIRE
 * Commercial-grade WebGL 3D Idle Tycoon Game
 * Powered by Three.js & zero bloatware
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
    { name: "Pine",    color: 0xc4a35a, barkColor: 0x6b4a2a, hexColor: "#c4a35a", value: 1.0,   unlockCost: 0 },
    { name: "Oak",     color: 0x966533, barkColor: 0x4f3115, hexColor: "#966533", value: 3.5,   unlockCost: 2000 },
    { name: "Maple",   color: 0xc24b27, barkColor: 0x571c0b, hexColor: "#c24b27", value: 12.0,  unlockCost: 25000 },
    { name: "Ebony",   color: 0x2a2830, barkColor: 0x141318, hexColor: "#2a2830", value: 45.0,  unlockCost: 350000 },
    { name: "Golden",  color: 0xffd700, barkColor: 0xb39200, hexColor: "#ffd700", value: 200.0, unlockCost: 5000000 }
];

// Rebalanced, addictive, immediate progression curve
const UPGRADE_DEFS = [
    { id: "spawnRate",   name: "Log Feed Rate",       category: "forest",    icon: "🌲", baseCost: 15,    costMult: 1.12, maxLv: 100, desc: "Feed trees faster onto conveyor" },
    { id: "convSpeed",   name: "Conveyor Speed",      category: "forest",    icon: "⏩", baseCost: 20,    costMult: 1.12, maxLv: 100, desc: "Faster roller belts" },
    { id: "sawCount",    name: "Gantry Saws",         category: "sawmill",   icon: "🪚", baseCost: 50,    costMult: 1.45, maxLv: 6,   desc: "Adds overhead swinging saws" },
    { id: "sawSpeed",    name: "Blade Speed & Cut",   category: "sawmill",   icon: "⚡", baseCost: 30,    costMult: 1.13, maxLv: 100, desc: "Fast cuts & plank output" },
    { id: "sortSpeed",   name: "Sorting Chutes",      category: "sawmill",   icon: "📦", baseCost: 40,    costMult: 1.12, maxLv: 100, desc: "Pushes cut planks to tower" },
    { id: "stackCap",    name: "Tower Height",        category: "logistics", icon: "📚", baseCost: 45,    costMult: 1.14, maxLv: 100, desc: "Skyscraper stack capacity" },
    { id: "craneSpeed",  name: "Gantry Crane",        category: "logistics", icon: "🏗️", baseCost: 60,    costMult: 1.13, maxLv: 100, desc: "Fast hoist onto trucks" },
    { id: "dockCount",   name: "Loading Bays",        category: "logistics", icon: "🚏", baseCost: 150,   costMult: 1.80, maxLv: 3,   desc: "Adds truck loading docks" },
    { id: "truckCount",  name: "Truck Fleet",         category: "fleet",     icon: "🚛", baseCost: 100,   costMult: 1.65, maxLv: 6,   desc: "More orange delivery trucks" },
    { id: "truckCap",    name: "Truck Flatbed Bed",   category: "fleet",     icon: "📐", baseCost: 75,    costMult: 1.16, maxLv: 100, desc: "Carry more lumber bundles" },
    { id: "truckSpeed",  name: "Highway Speed",       category: "fleet",     icon: "💨", baseCost: 65,    costMult: 1.12, maxLv: 100, desc: "Quicker road transit" },
    { id: "roadUpgrade", name: "Road Expansion",      category: "fleet",     icon: "🛣️", baseCost: 200,   costMult: 1.70, maxLv: 5,   desc: "Wider lanes & clears traffic jams" },
    { id: "woodValue",   name: "Lumber Price",        category: "fleet",     icon: "💰", baseCost: 90,    costMult: 1.18, maxLv: 100, desc: "Cash multiplier per plank" }
];

const ACHIEVEMENTS = [
    { id: "first_log",   name: "First Cut",           icon: "🪓", desc: "Cut your first log",              cond: s => s.stats.logsProcessed >= 1,   reward: 30 },
    { id: "logs_50",     name: "Lumberjack",          icon: "🌲", desc: "Cut 50 logs",                     cond: s => s.stats.logsProcessed >= 50,  reward: 150 },
    { id: "logs_500",    name: "Master Faller",       icon: "🪵", desc: "Cut 500 logs",                    cond: s => s.stats.logsProcessed >= 500, reward: 1500 },
    { id: "first_truck", name: "Cargo Away!",         icon: "🚛", desc: "Complete 1 truck delivery",       cond: s => s.stats.deliveries >= 1,      reward: 50 },
    { id: "trucks_25",   name: "Fleet Logistician",   icon: "🛣️", desc: "Complete 25 truck deliveries",    cond: s => s.stats.deliveries >= 25,     reward: 600 },
    { id: "coins_1k",    name: "Small Business",      icon: "💵", desc: "Earn 1,000 total cash",          cond: s => s.totalEarned >= 1000,        reward: 100 },
    { id: "coins_100k",  name: "Log Jam Mogul",       icon: "💰", desc: "Earn 100,000 total cash",        cond: s => s.totalEarned >= 100000,      reward: 3500 },
    { id: "tier_oak",    name: "Hardwood Era",        icon: "🍂", desc: "Unlock Oak wood tier",            cond: s => s.woodTier >= 1,              reward: 300 },
    { id: "jam_cleared", name: "Traffic Controller",  icon: "🚨", desc: "Clear a 4-truck traffic jam",     cond: s => s.stats.jamsCleared >= 1,     reward: 400 }
];

// Diegetic 3D In-World Upgrade Pads (matching 5xpM-hsYo3w.jpg)
const WORLD_UPGRADE_PADS = [
    { id: "pad_saw",   defId: "sawSpeed",   label: "UPGRADE SAWS",  icon: "🪚", pos: [-6, 0.2, -4] },
    { id: "pad_crane", defId: "craneSpeed", label: "UPGRADE CRANE", icon: "🏗️", pos: [2, 0.2, -4] },
    { id: "pad_fleet", defId: "truckCount", label: "MORE TRUCKS",   icon: "🚛", pos: [8, 0.2, 0] },
    { id: "pad_road",  defId: "roadUpgrade",label: "WIDEN ROAD",    icon: "🛣️", pos: [8, 0.2, 7] }
];

function formatNumber(num) {
    if (isNaN(num) || num === null || num === undefined) return "0";
    if (num < 1000) return Math.floor(num).toLocaleString();
    const suffixes = ["", "K", "M", "B", "T", "aa", "ab", "ac"];
    const exp = Math.floor(Math.log10(num) / 3);
    if (exp >= suffixes.length) return num.toExponential(2);
    const scaled = num / Math.pow(10, exp * 3);
    return scaled.toFixed(scaled < 10 ? 2 : 1) + suffixes[exp];
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str).replace(/[&<>"']/g, m => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[m]));
}

async function sha256(str) {
    if (!window.crypto || !window.crypto.subtle) {
        let h = 0; for (let i = 0; i < str.length; i++) h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
        return Math.abs(h).toString(16).padStart(16, "0");
    }
    const enc = new TextEncoder().encode(str);
    const buf = await window.crypto.subtle.digest("SHA-256", enc);
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
}

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
// 2. AUDIO SYNTHESIZER
// ==========================================
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.sfxEnabled = true;
        this.musicEnabled = true;
        this.sfxGain = null;
    }
    init() {
        if (this.ctx) return;
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        this.ctx = new AudioCtx();
        this.sfxGain = this.ctx.createGain();
        this.sfxGain.gain.value = 0.35;
        this.sfxGain.connect(this.ctx.destination);
    }
    resume() {
        if (this.ctx && this.ctx.state === 'suspended') this.ctx.resume();
    }
    playSfx(type) {
        if (!this.sfxEnabled || !this.ctx) return;
        this.resume();
        const now = this.ctx.currentTime;
        try {
            if (type === 'cash') {
                const osc = this.ctx.createOscillator();
                const g = this.ctx.createGain();
                osc.type = "sine";
                osc.frequency.setValueAtTime(850, now);
                osc.frequency.exponentialRampToValueAtTime(1700, now + 0.12);
                g.gain.setValueAtTime(0.25, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
                osc.connect(g); g.connect(this.sfxGain);
                osc.start(now); osc.stop(now + 0.12);
            } else if (type === 'upgrade') {
                [523, 659, 783, 1046].forEach((f, idx) => {
                    const osc = this.ctx.createOscillator();
                    const g = this.ctx.createGain();
                    osc.type = "triangle";
                    const t = now + idx * 0.05;
                    osc.frequency.setValueAtTime(f, t);
                    g.gain.setValueAtTime(0.2, t);
                    g.gain.exponentialRampToValueAtTime(0.001, t + 0.12);
                    osc.connect(g); g.connect(this.sfxGain);
                    osc.start(t); osc.stop(t + 0.12);
                });
            } else if (type === 'honk') {
                [220, 310].forEach(f => {
                    const osc = this.ctx.createOscillator();
                    const g = this.ctx.createGain();
                    osc.type = "sawtooth";
                    osc.frequency.setValueAtTime(f, now);
                    g.gain.setValueAtTime(0.08, now);
                    g.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
                    osc.connect(g); g.connect(this.sfxGain);
                    osc.start(now); osc.stop(now + 0.2);
                });
            } else if (type === 'saw') {
                const osc = this.ctx.createOscillator();
                const g = this.ctx.createGain();
                osc.type = "sawtooth";
                osc.frequency.setValueAtTime(140, now);
                osc.frequency.linearRampToValueAtTime(220, now + 0.1);
                g.gain.setValueAtTime(0.09, now);
                g.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                osc.connect(g); g.connect(this.sfxGain);
                osc.start(now); osc.stop(now + 0.1);
            }
        } catch(e) {}
    }
}
const audio = new SoundEngine();

// ==========================================
// 3. GAME STATE & PROGRESSION
// ==========================================
function createDefaultState() {
    return {
        coins: 100, // Generous starting capital for immediate dopamine
        totalEarned: 100,
        woodTier: 0,
        goldenAcorns: 0,
        prestigeCount: 0,
        upgrades: {
            spawnRate: 1,
            convSpeed: 1,
            sawCount: 1,
            sawSpeed: 1,
            sortSpeed: 1,
            stackCap: 1,
            craneSpeed: 1,
            dockCount: 1,
            truckCount: 1,
            truckCap: 1,
            truckSpeed: 1,
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
            jamsCleared: 0,
            playTime: 0
        },
        settings: {
            sfx: true,
            music: true,
            serverUrl: API_CONFIG.BASE_URL
        },
        tutorialStep: 0,
        saveVersion: 2,
        lastSaveTime: Date.now()
    };
}

let gameState = createDefaultState();
let currentUser = null;
let buyMultiplier = 1;
let currentCategory = "all";
let tapBoostRemaining = 0;
let watchBoostRemaining = 0;
let rushHourRemaining = 0;
let isTrafficJam = false;

// Storage
const Storage = {
    GUEST_KEY: "logjam_save_guest_3d",
    USER_KEY_PREFIX: "logjam_save_user_3d_",
    ACTIVE_USER_KEY: "logjam_active_user",

    saveLocal() {
        gameState.lastSaveTime = Date.now();
        const key = currentUser ? (this.USER_KEY_PREFIX + currentUser.username.toLowerCase()) : this.GUEST_KEY;
        try {
            localStorage.setItem(key, JSON.stringify(gameState));
            if (currentUser) localStorage.setItem(this.ACTIVE_USER_KEY, JSON.stringify(currentUser));
            updateSyncIndicator("✓ Saved", "saved");
        } catch (e) {}
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
            updateSyncIndicator(data.ok ? "✓ Synced" : "⚠ Offline", data.ok ? "saved" : "offline");
        } catch (e) {
            updateSyncIndicator("⚠ Offline", "offline");
        }
    }
};

function updateSyncIndicator(msg, state = "saved") {
    const el = document.getElementById("sync-text");
    const dot = document.getElementById("sync-dot");
    if (el) el.textContent = msg;
    if (dot) dot.className = "status-dot " + state;
}

// ==========================================
// 4. THREE.JS 3D SCENE & ENGINE
// ==========================================
let scene, camera, renderer, raycaster, mouse;
let worldPadMeshes = [];
let truckMeshes = [];
let logMeshes = [];
let towerStackMeshes = [];
let sawMeshes = [];
let gantryCraneGroup;
let pointingHandSprite;
let cargoShipMesh;

// Overlay 2D Particles & Text
const overlayCanvas = document.getElementById("overlay-canvas");
const overlayCtx = overlayCanvas.getContext("2d");
let particles2D = [];
let floatingTexts2D = [];

class Particle2D {
    constructor(x, y, vx, vy, color, size, life) {
        this.x = x; this.y = y; this.vx = vx; this.vy = vy;
        this.color = color; this.size = size; this.life = life; this.maxLife = life;
    }
    update(dt) { this.x += this.vx * dt; this.y += this.vy * dt; this.life -= dt; }
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

class FloatingText2D {
    constructor(x, y, text, color = "#10b981", size = 18) {
        this.x = x; this.y = y; this.text = text; this.color = color;
        this.size = size; this.life = 1.2; this.maxLife = 1.2;
    }
    update(dt) { this.y -= 28 * dt; this.life -= dt; }
    draw(ctx) {
        const a = Math.max(0, this.life / this.maxLife);
        ctx.save();
        ctx.globalAlpha = a;
        ctx.fillStyle = this.color;
        ctx.font = `900 ${this.size}px ${getComputedStyle(document.body).fontFamily}`;
        ctx.textAlign = "center";
        ctx.shadowColor = "rgba(0,0,0,0.85)";
        ctx.shadowBlur = 4;
        ctx.fillText(this.text, this.x, this.y);
        ctx.restore();
    }
}

function init3DScene() {
    const canvas = document.getElementById("webgl-canvas");
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;

    // Scene with Soft Sky Fog
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xdbeafe);
    scene.fog = new THREE.FogExp2(0xdbeafe, 0.012);

    // Isometric Perspective Camera (matching mobile tycoon game bird's eye view)
    camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 1000);
    camera.position.set(24, 28, 24);
    camera.lookAt(1, 1, 0);

    // WebGL Renderer with Soft Shadows
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    // Studio Daylight & Ambient Lighting
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x86efac, 0.7);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfffbeb, 1.1);
    dirLight.position.set(20, 35, 15);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 1024;
    dirLight.shadow.mapSize.height = 1024;
    dirLight.shadow.camera.near = 0.5;
    dirLight.shadow.camera.far = 100;
    const d = 25;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    scene.add(dirLight);

    buildEnvironment();
    buildMachinery();
    buildWorldUpgradePads();
    init3DPointingHand();

    window.addEventListener("resize", onWindowResize);
    canvas.addEventListener("click", onCanvas3DClick);
}

function onWindowResize() {
    const canvas = document.getElementById("webgl-canvas");
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;

    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);

    const dpr = window.devicePixelRatio || 1;
    overlayCanvas.width = w * dpr;
    overlayCanvas.height = h * dpr;
    overlayCtx.resetTransform();
    overlayCtx.scale(dpr, dpr);
}

// Build 3D Terrain, Forest, Roads, River
function buildEnvironment() {
    // 1. Lush Green Grass Base
    const grassGeo = new THREE.BoxGeometry(50, 1, 50);
    const grassMat = new THREE.MeshStandardMaterial({ color: 0x4ade80, roughness: 0.8 });
    const grassMesh = new THREE.Mesh(grassGeo, grassMat);
    grassMesh.position.y = -0.5;
    grassMesh.receiveShadow = true;
    scene.add(grassMesh);

    // 2. Factory Dirt Yard
    const yardGeo = new THREE.BoxGeometry(18, 0.05, 14);
    const yardMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.9 });
    const yardMesh = new THREE.Mesh(yardGeo, yardMat);
    yardMesh.position.set(0, 0.03, 0);
    yardMesh.receiveShadow = true;
    scene.add(yardMesh);

    // 3. Asphalt Highway & Bridge
    const roadMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7 });
    const roadGeo = new THREE.BoxGeometry(4.5, 0.06, 32);
    const roadMesh = new THREE.Mesh(roadGeo, roadMat);
    roadMesh.position.set(8.5, 0.04, 2);
    roadMesh.receiveShadow = true;
    scene.add(roadMesh);

    // Painted White Dashed Lines
    const dashMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    for (let z = -12; z <= 16; z += 3) {
        const dashGeo = new THREE.BoxGeometry(0.3, 0.07, 1.5);
        const dashMesh = new THREE.Mesh(dashGeo, dashMat);
        dashMesh.position.set(8.5, 0.05, z);
        scene.add(dashMesh);
    }

    // Wooden Bridge across the river
    const bridgeMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.8 });
    const bridgeGeo = new THREE.BoxGeometry(5.2, 0.4, 7);
    const bridgeMesh = new THREE.Mesh(bridgeGeo, bridgeMat);
    bridgeMesh.position.set(8.5, 0.25, 12);
    bridgeMesh.castShadow = true;
    bridgeMesh.receiveShadow = true;
    scene.add(bridgeMesh);

    // 4. Sparkling River
    const riverGeo = new THREE.PlaneGeometry(12, 50);
    const riverMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.1, metalness: 0.3 });
    const riverMesh = new THREE.Mesh(riverGeo, riverMat);
    riverMesh.rotation.x = -Math.PI / 2;
    riverMesh.position.set(16, 0.02, 0);
    scene.add(riverMesh);

    // 5. Berthed Cargo Ship & Pier
    const dockGeo = new THREE.BoxGeometry(3, 0.2, 10);
    const dockMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.7 });
    const dockMesh = new THREE.Mesh(dockGeo, dockMat);
    dockMesh.position.set(12, 0.1, 4);
    dockMesh.receiveShadow = true;
    scene.add(dockMesh);

    // Cargo Ship
    const shipGroup = new THREE.Group();
    const hullGeo = new THREE.BoxGeometry(3.5, 1.2, 9);
    const hullMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.5 });
    const hullMesh = new THREE.Mesh(hullGeo, hullMat);
    hullMesh.position.y = 0.5;
    hullMesh.castShadow = true;
    shipGroup.add(hullMesh);

    const cabinGeo = new THREE.BoxGeometry(2.8, 1.2, 2.8);
    const cabinMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.5 });
    const cabinMesh = new THREE.Mesh(cabinGeo, cabinMat);
    cabinMesh.position.set(0, 1.6, -2.5);
    cabinMesh.castShadow = true;
    shipGroup.add(cabinMesh);

    shipGroup.position.set(15.5, 0, 4);
    scene.add(shipGroup);
    cargoShipMesh = shipGroup;

    // 6. Perimeter Low-Poly Pine Trees
    const treePositions = [
        [-16, -16], [-12, -16], [-8, -16], [-4, -16], [0, -16], [4, -16],
        [-16, -12], [-16, -8], [-16, -4], [-16, 0], [-16, 4], [-16, 8],
        [-16, 12], [-14, 15], [-10, 16], [-6, 16], [0, 16]
    ];
    treePositions.forEach(([tx, tz]) => createLowPolyPine(tx, tz));
}

function createLowPolyPine(x, z) {
    const group = new THREE.Group();

    // Trunk
    const trunkGeo = new THREE.CylinderGeometry(0.3, 0.4, 1.5, 6);
    const trunkMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.9, flatShading: true });
    const trunk = new THREE.Mesh(trunkGeo, trunkMat);
    trunk.position.y = 0.75;
    trunk.castShadow = true;
    group.add(trunk);

    // 3 Foliage Cones
    const foliageColors = [0x14532d, 0x166534, 0x15803d];
    foliageColors.forEach((col, idx) => {
        const coneGeo = new THREE.ConeGeometry(2.0 - idx * 0.35, 1.8, 6);
        const coneMat = new THREE.MeshStandardMaterial({ color: col, roughness: 0.8, flatShading: true });
        const cone = new THREE.Mesh(coneGeo, coneMat);
        cone.position.y = 1.8 + idx * 0.9;
        cone.castShadow = true;
        group.add(cone);
    });

    group.position.set(x, 0, z);
    scene.add(group);
}

// Build 3D Factory Machinery: Spawner, Conveyor, Saws, Skyscraper Stack, Gantry Crane
function buildMachinery() {
    // 1. Forest Intake Bunker (Spawner)
    const bunkerGeo = new THREE.BoxGeometry(2.5, 2.2, 2.5);
    const bunkerMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 });
    const bunker = new THREE.Mesh(bunkerGeo, bunkerMat);
    bunker.position.set(-12, 1.1, -7);
    bunker.castShadow = true;
    scene.add(bunker);

    // 2. Industrial Conveyor Bed
    const convGeo = new THREE.BoxGeometry(8, 0.4, 1.6);
    const convMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.5 });
    const conv = new THREE.Mesh(convGeo, convMat);
    conv.position.set(-7, 0.9, -7);
    conv.castShadow = true;
    conv.receiveShadow = true;
    scene.add(conv);

    // Guard Rails
    const railMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4 });
    const rail1 = new THREE.Mesh(new THREE.BoxGeometry(8, 0.2, 0.1), railMat);
    rail1.position.set(-7, 1.2, -7.8);
    const rail2 = new THREE.Mesh(new THREE.BoxGeometry(8, 0.2, 0.1), railMat);
    rail2.position.set(-7, 1.2, -6.2);
    scene.add(rail1); scene.add(rail2);

    // 3. Gantry Saws with Overhead Arch Frames
    updateSaws3D();

    // 4. Yellow Gantry Crane on Rails
    gantryCraneGroup = new THREE.Group();
    const towerGeo = new THREE.BoxGeometry(0.8, 5.5, 0.8);
    const craneMat = new THREE.MeshStandardMaterial({ color: 0xeab308, roughness: 0.4 });
    const tower = new THREE.Mesh(towerGeo, craneMat);
    tower.position.y = 2.75;
    tower.castShadow = true;
    gantryCraneGroup.add(tower);

    // Crane Arm
    const armGeo = new THREE.BoxGeometry(8, 0.6, 0.8);
    const arm = new THREE.Mesh(armGeo, craneMat);
    arm.position.set(3, 5.2, 0);
    arm.castShadow = true;
    gantryCraneGroup.add(arm);

    // Red Hoist Block
    const hoistGeo = new THREE.BoxGeometry(0.9, 0.7, 0.9);
    const hoistMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.4 });
    const hoist = new THREE.Mesh(hoistGeo, hoistMat);
    hoist.position.set(3, 4.2, 0);
    gantryCraneGroup.add(hoist);

    gantryCraneGroup.position.set(2, 0, -2);
    scene.add(gantryCraneGroup);

    // 5. Skyscraper Lumber Tower (matching 5xpM-hsYo3w.jpg)
    updateLumberTower3D();
}

function updateSaws3D() {
    sawMeshes.forEach(s => scene.remove(s));
    sawMeshes = [];

    const numSaws = Math.min(6, Math.max(1, gameState.upgrades.sawCount || 1));
    for (let i = 0; i < numSaws; i++) {
        const sawGroup = new THREE.Group();
        const archGeo = new THREE.BoxGeometry(0.4, 2.4, 2.2);
        const archMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.7 });
        const arch = new THREE.Mesh(archGeo, archMat);
        arch.position.y = 1.2;
        arch.castShadow = true;
        sawGroup.add(arch);

        // Spinning Stainless Steel Blade
        const bladeGeo = new THREE.CylinderGeometry(0.9, 0.9, 0.06, 16);
        const bladeMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.2, metalness: 0.8 });
        const blade = new THREE.Mesh(bladeGeo, bladeMat);
        blade.rotation.x = Math.PI / 2;
        blade.position.y = 1.1;
        sawGroup.add(blade);

        sawGroup.position.set(-6 + (i * 0.9), 0, -7);
        scene.add(sawGroup);
        sawMeshes.push(sawGroup);
    }
}

function updateLumberTower3D() {
    towerStackMeshes.forEach(m => scene.remove(m));
    towerStackMeshes = [];

    const tier = WOOD_TIERS[gameState.woodTier];
    const layers = Math.min(22, Math.max(2, Math.floor(gameState.stats.logsProcessed / 2) + 4));

    for (let l = 0; l < layers; l++) {
        const plankGeo = new THREE.BoxGeometry(3.6, 0.25, 3.6);
        const plankMat = new THREE.MeshStandardMaterial({ color: tier.color, roughness: 0.7 });
        const plankMesh = new THREE.Mesh(plankGeo, plankMat);
        plankMesh.position.set(0, 0.2 + l * 0.26, 0);
        plankMesh.castShadow = true;
        plankMesh.receiveShadow = true;
        scene.add(plankMesh);
        towerStackMeshes.push(plankMesh);
    }
}

// Build 3D Diegetic Upgrade Pads on Ground (matching 5xpM-hsYo3w.jpg)
function buildWorldUpgradePads() {
    worldPadMeshes = [];
    WORLD_UPGRADE_PADS.forEach(pad => {
        const group = new THREE.Group();

        // 3D Beveled Box
        const padGeo = new THREE.BoxGeometry(3.2, 0.35, 2.4);
        const padMat = new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.4 });
        const padMesh = new THREE.Mesh(padGeo, padMat);
        padMesh.position.y = 0.17;
        padMesh.castShadow = true;
        padMesh.receiveShadow = true;
        group.add(padMesh);

        // High-res Dynamic Canvas Label
        const canvasTex = createPadTexture(pad);
        const tex = new THREE.CanvasTexture(canvasTex);
        const labelMat = new THREE.MeshBasicMaterial({ map: tex, transparent: true });
        const labelGeo = new THREE.PlaneGeometry(3.0, 2.2);
        const labelMesh = new THREE.Mesh(labelGeo, labelMat);
        labelMesh.rotation.x = -Math.PI / 2;
        labelMesh.position.y = 0.36;
        group.add(labelMesh);

        group.position.set(pad.pos[0], pad.pos[1], pad.pos[2]);
        group.userData = { pad, padMesh, labelMesh, tex, canvasTex };
        scene.add(group);
        worldPadMeshes.push(group);
    });
}

function createPadTexture(pad) {
    const canvas = document.createElement("canvas");
    canvas.width = 256; canvas.height = 192;
    const ctx = canvas.getContext("2d");
    renderPadCanvas(ctx, pad);
    return canvas;
}

function renderPadCanvas(ctx, pad) {
    const def = UPGRADE_DEFS.find(u => u.id === pad.defId);
    const curLv = gameState.upgrades[pad.defId] || 0;
    const isMax = curLv >= (def.maxLv || 100);
    const cost = Math.round(def.baseCost * Math.pow(def.costMult, curLv));
    const canAfford = !isMax && gameState.coins >= cost;

    ctx.clearRect(0, 0, 256, 192);

    // Rounded Box Background
    ctx.fillStyle = canAfford ? "#10b981" : "#1e293b";
    ctx.beginPath();
    ctx.roundRect(8, 8, 240, 176, 20);
    ctx.fill();

    // Glowing border
    ctx.strokeStyle = canAfford ? "#6ee7b7" : "rgba(255,255,255,0.2)";
    ctx.lineWidth = canAfford ? 8 : 4;
    ctx.stroke();

    // Icon + Label
    ctx.fillStyle = "#ffffff";
    ctx.font = "900 24px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(`${pad.icon} ${pad.label}`, 128, 65);

    // Cost
    ctx.fillStyle = canAfford ? "#fef08a" : "#94a3b8";
    ctx.font = "900 32px sans-serif";
    ctx.fillText(isMax ? 'MAX' : `💵 ${formatNumber(cost)}`, 128, 130);
}

function updateWorldPadsUI() {
    worldPadMeshes.forEach(group => {
        const { pad, padMesh, tex, canvasTex } = group.userData;
        const ctx = canvasTex.getContext("2d");
        renderPadCanvas(ctx, pad);
        tex.needsUpdate = true;

        const def = UPGRADE_DEFS.find(u => u.id === pad.defId);
        const curLv = gameState.upgrades[pad.defId] || 0;
        const cost = Math.round(def.baseCost * Math.pow(def.costMult, curLv));
        const canAfford = curLv < (def.maxLv || 100) && gameState.coins >= cost;

        padMesh.material.color.setHex(canAfford ? 0x10b981 : 0x1e293b);
    });
}

function init3DPointingHand() {
    const canvas = document.createElement("canvas");
    canvas.width = 128; canvas.height = 128;
    const ctx = canvas.getContext("2d");
    ctx.font = "80px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("👆", 64, 90);

    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, transparent: true });
    pointingHandSprite = new THREE.Sprite(mat);
    pointingHandSprite.scale.set(3.5, 3.5, 1);
    pointingHandSprite.position.set(8, 3.5, 7);
    pointingHandSprite.visible = false;
    scene.add(pointingHandSprite);
}

// 3D Delivery Trucks (Chunky, glossy, toy-like)
class Truck3D {
    constructor(id, dockIdx) {
        this.id = id;
        this.dockIdx = dockIdx;
        this.state = "driving_in";
        this.cargo = 0;
        this.isJammed = false;
        this.z = -14 - id * 4.5;
        this.targetZ = 0;

        this.group = new THREE.Group();

        // Cab (Orange)
        const cabGeo = new THREE.BoxGeometry(2.0, 1.6, 2.4);
        const cabMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.3 });
        const cab = new THREE.Mesh(cabGeo, cabMat);
        cab.position.set(0, 1.2, 1.0);
        cab.castShadow = true;
        this.group.add(cab);

        // Windshield
        const glassGeo = new THREE.BoxGeometry(1.8, 0.8, 0.2);
        const glassMat = new THREE.MeshStandardMaterial({ color: 0xe0f2fe, roughness: 0.1, metalness: 0.2 });
        const glass = new THREE.Mesh(glassGeo, glassMat);
        glass.position.set(0, 1.4, 2.2);
        this.group.add(glass);

        // Flatbed (Slate Grey)
        const bedGeo = new THREE.BoxGeometry(2.2, 0.4, 3.5);
        const bedMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 });
        const bed = new THREE.Mesh(bedGeo, bedMat);
        bed.position.set(0, 0.8, -1.8);
        bed.castShadow = true;
        this.group.add(bed);

        // 4 Wheels
        const wheelGeo = new THREE.CylinderGeometry(0.4, 0.4, 0.3, 12);
        const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 });
        [[-1.1, 0.4, 1.0], [1.1, 0.4, 1.0], [-1.1, 0.4, -2.5], [1.1, 0.4, -2.5]].forEach(([wx, wy, wz]) => {
            const wheel = new THREE.Mesh(wheelGeo, wheelMat);
            wheel.rotation.z = Math.PI / 2;
            wheel.position.set(wx, wy, wz);
            this.group.add(wheel);
        });

        // 3D Emoji Speech Bubble Billboard (😡 / 😊)
        this.emojiCanvas = document.createElement("canvas");
        this.emojiCanvas.width = 128; this.emojiCanvas.height = 128;
        this.emojiCtx = this.emojiCanvas.getContext("2d");
        this.emojiTex = new THREE.CanvasTexture(this.emojiCanvas);
        const emojiMat = new THREE.SpriteMaterial({ map: this.emojiTex, transparent: true });
        this.emojiSprite = new THREE.Sprite(emojiMat);
        this.emojiSprite.scale.set(2.4, 2.4, 1);
        this.emojiSprite.position.set(0, 3.4, 0);
        this.emojiSprite.visible = false;
        this.group.add(this.emojiSprite);

        this.group.position.set(8.5, 0, this.z);
        scene.add(this.group);
    }

    setEmoji(emoji) {
        if (!emoji) {
            this.emojiSprite.visible = false;
            return;
        }
        this.emojiSprite.visible = true;
        this.emojiCtx.clearRect(0, 0, 128, 128);
        // Speech Bubble
        this.emojiCtx.fillStyle = "#ffffff";
        this.emojiCtx.beginPath();
        this.emojiCtx.arc(64, 52, 44, 0, Math.PI * 2);
        this.emojiCtx.fill();
        this.emojiCtx.strokeStyle = emoji === "😡" ? "#ef4444" : "#10b981";
        this.emojiCtx.lineWidth = 6;
        this.emojiCtx.stroke();
        // Emoji text
        this.emojiCtx.font = "52px sans-serif";
        this.emojiCtx.textAlign = "center";
        this.emojiCtx.fillText(emoji, 64, 70);
        this.emojiTex.needsUpdate = true;
    }
}

// 3D Cylinder Logs rolling along the conveyor
class Log3D {
    constructor() {
        this.x = -11.0;
        this.cutProgress = 0;
        this.isSliced = false;

        const tier = WOOD_TIERS[gameState.woodTier];
        const logGeo = new THREE.CylinderGeometry(0.55, 0.55, 2.2, 12);
        const logMat = new THREE.MeshStandardMaterial({ color: tier.color, roughness: 0.8 });
        this.mesh = new THREE.Mesh(logGeo, logMat);
        this.mesh.rotation.z = Math.PI / 2;
        this.mesh.position.set(this.x, 1.6, -7);
        this.mesh.castShadow = true;
        scene.add(this.mesh);
    }
}

// ==========================================
// 5. PRODUCTION LINE & TRAFFIC ENGINE
// ==========================================
let spawnTimer = 0;
let craneTimer = 0;

function update3DProductionLine(dt) {
    const speedMult = (tapBoostRemaining > 0 ? 1.6 : 1.0) *
                      (rushHourRemaining > 0 ? 2.0 : 1.0) *
                      (watchBoostRemaining > 0 ? 2.0 : 1.0);

    // 1. Log Spawning
    const spawnRateLv = gameState.upgrades.spawnRate || 1;
    const spawnInterval = Math.max(0.35, (1.8 / (1 + spawnRateLv * 0.16)) / speedMult);
    spawnTimer += dt;
    if (spawnTimer >= spawnInterval && logMeshes.length < 10) {
        spawnTimer = 0;
        logMeshes.push(new Log3D());
    }

    // 2. Conveyor & Gantry Saws
    const convSpeedLv = gameState.upgrades.convSpeed || 1;
    const convSpeed = (2.2 + convSpeedLv * 0.18) * speedMult;
    const sawSpeedLv = gameState.upgrades.sawSpeed || 1;
    const cutDuration = Math.max(0.2, (0.9 / (1 + sawSpeedLv * 0.2)) / speedMult);

    for (let i = logMeshes.length - 1; i >= 0; i--) {
        const log = logMeshes[i];
        if (log.x >= -6.5 && log.x < -4.5) {
            log.cutProgress += dt;
            // Saw blade spin & sparks
            sawMeshes.forEach(sm => {
                sm.children[1].rotation.y += 25 * dt;
            });
            if (Math.random() < 0.4) {
                audio.playSfx('saw');
                const screenP = toScreenXY(new THREE.Vector3(log.x, 2, -7));
                for (let k = 0; k < 3; k++) {
                    particles2D.push(new Particle2D(
                        screenP.x, screenP.y,
                        (Math.random() - 0.5) * 60,
                        -Math.random() * 50 - 20,
                        Math.random() > 0.4 ? "#f59e0b" : "#fcd34d",
                        3, 0.4
                    ));
                }
            }

            if (log.cutProgress >= cutDuration) {
                scene.remove(log.mesh);
                logMeshes.splice(i, 1);
                gameState.stats.logsProcessed++;
                updateLumberTower3D();
                continue;
            }
        } else {
            log.x += convSpeed * dt;
            log.mesh.position.x = log.x;
            log.mesh.rotation.y += 4 * dt; // Rolling animation
        }
    }

    // 3. Yellow Gantry Crane Hoist
    const craneSpeedLv = gameState.upgrades.craneSpeed || 1;
    craneTimer += dt * (1 + craneSpeedLv * 0.22) * speedMult;

    // 4. Truck Fleet & Traffic Jam
    const maxTrucks = Math.min(6, Math.max(1, gameState.upgrades.truckCount || 1));
    const numDocks = Math.min(3, Math.max(1, gameState.upgrades.dockCount || 1));
    const truckSpeedLv = gameState.upgrades.truckSpeed || 1;
    const truckSpeed = (3.2 + truckSpeedLv * 0.3) * speedMult;

    while (truckMeshes.length < maxTrucks) {
        truckMeshes.push(new Truck3D(truckMeshes.length, truckMeshes.length % numDocks));
    }

    let jammedCount = 0;
    truckMeshes.forEach((t, idx) => {
        const dockTargetZ = 0.5 + (t.dockIdx % numDocks) * 3.5;

        // Check if vehicle ahead is blocking
        let isBlocked = false;
        for (let j = 0; j < truckMeshes.length; j++) {
            if (j !== idx && truckMeshes[j].z > t.z && (truckMeshes[j].z - t.z) < 4.2) {
                isBlocked = true;
                break;
            }
        }

        if (isBlocked) {
            t.isJammed = true;
            jammedCount++;
            t.setEmoji("😡");
        } else {
            t.isJammed = false;
            if (t.state === "leaving") t.setEmoji("😊");
            else t.setEmoji(null);
        }

        if (!isBlocked && t.state === "driving_in") {
            if (t.z < dockTargetZ) {
                t.z += truckSpeed * dt;
            } else {
                t.state = "docked";
            }
        } else if (t.state === "docked") {
            // Crane loading
            if (craneTimer >= 1.2) {
                craneTimer = 0;
                t.cargo++;
                t.state = "leaving";
                audio.playSfx('honk');
            }
        } else if (!isBlocked && t.state === "leaving") {
            t.z += truckSpeed * dt;

            // Across River Bridge -> Cash Payout!
            if (t.z > 20.0) {
                t.z = -14.0;
                t.state = "driving_in";
                t.cargo = 0;

                const tier = WOOD_TIERS[gameState.woodTier];
                const payout = Math.round(50 * tier.value * (1 + (gameState.upgrades.woodValue || 0) * 0.2) * (1 + gameState.goldenAcorns * 0.05) * speedMult);

                gameState.coins += payout;
                gameState.totalEarned += payout;
                gameState.stats.deliveries++;

                // Bounce Money HUD
                const cashBox = document.getElementById("hud-coin-box");
                if (cashBox) {
                    cashBox.classList.add("bounce");
                    setTimeout(() => cashBox.classList.remove("bounce"), 150);
                }

                audio.playSfx('cash');
                const screenP = toScreenXY(new THREE.Vector3(8.5, 2, 14));
                floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y, `+💵 ${formatNumber(payout)}`, "#10b981", 22));

                for (let k = 0; k < 12; k++) {
                    particles2D.push(new Particle2D(
                        screenP.x, screenP.y,
                        (Math.random() - 0.5) * 80,
                        -Math.random() * 80 - 20,
                        "#10b981", 4, 0.8
                    ));
                }

                if (gameState.tutorialStep === 2) {
                    gameState.tutorialStep = 3;
                    showToast("🎉 Tutorial Complete! Build your 3D empire!");
                    updateTutorial();
                }
            }
        }

        t.group.position.z = t.z;
    });

    // Traffic Jam Alert & Hand Pointer Trigger (matching 5xpM-hsYo3w.jpg)
    const trafficBanner = document.getElementById("traffic-alert");
    if (jammedCount >= 3) {
        if (!isTrafficJam) {
            isTrafficJam = true;
            audio.playSfx('honk');
        }
        trafficBanner.classList.add("show");
        pointingHandSprite.visible = true;
        pointingHandSprite.position.y = 3.5 + Math.sin(Date.now() * 0.008) * 0.6;
    } else {
        if (isTrafficJam) {
            isTrafficJam = false;
            gameState.stats.jamsCleared++;
            showToast("🎉 Traffic Jam Cleared! Trucks speeding across bridge!");
        }
        trafficBanner.classList.remove("show");
        if (gameState.tutorialStep !== 1) pointingHandSprite.visible = false;
    }

    checkMilestones();
}

function toScreenXY(pos) {
    const v = pos.clone().project(camera);
    const canvas = document.getElementById("webgl-canvas");
    return {
        x: (v.x * 0.5 + 0.5) * canvas.clientWidth,
        y: (-(v.y * 0.5) + 0.5) * canvas.clientHeight
    };
}

// Raycasting: Direct 3D In-World Clicks on Upgrade Pads & Ground
function onCanvas3DClick(e) {
    const canvas = document.getElementById("webgl-canvas");
    const rect = canvas.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / canvas.clientWidth) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / canvas.clientHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);

    // Check click on 3D upgrade pads
    for (const group of worldPadMeshes) {
        const intersects = raycaster.intersectObjects(group.children, true);
        if (intersects.length > 0) {
            handleUpgradeClick(group.userData.pad.defId);

            // 3D Squash & Stretch spring bounce
            group.scale.set(1.15, 0.85, 1.15);
            setTimeout(() => group.scale.set(1, 1, 1), 180);
            return;
        }
    }

    // Tap on Mill -> Speed Boost & Cash
    applyTapBoost(e.clientX - rect.left, e.clientY - rect.top);
}

function applyTapBoost(x, y) {
    tapBoostRemaining = 8;
    gameState.stats.taps++;
    gameState.coins += 5; // Active tap gives cash reward
    gameState.totalEarned += 5;

    floatingTexts2D.push(new FloatingText2D(x, y, "+💵 5 BOOST!", "#f59e0b", 18));
    for (let k = 0; k < 6; k++) {
        particles2D.push(new Particle2D(x, y, (Math.random() - 0.5) * 60, (Math.random() - 0.5) * 60, "#f59e0b", 3, 0.5));
    }

    if (gameState.tutorialStep === 0) {
        gameState.tutorialStep = 1;
        updateTutorial();
    }
}

// ==========================================
// 6. UPGRADE SYSTEM & SHOP UI
// ==========================================
const shopCardsMap = new Map();

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
                    <span class="upgrade-level-tag js-lv">Lv.1</span>
                </div>
                <div class="milestone-bar-wrap">
                    <div class="milestone-track">
                        <div class="milestone-fill js-milestone-fill"></div>
                    </div>
                    <div class="milestone-sub">
                        <span class="js-milestone-label">1/10</span>
                        <span class="milestone-bonus js-milestone-bonus">+2x at Lv.10</span>
                    </div>
                </div>
                <div class="upgrade-stat-row js-stat-row">+18% throughput</div>
            </div>
            <button class="buy-btn js-buy-btn" data-id="${def.id}">
                <span class="buy-btn-level js-btn-level">+1</span>
                <span class="buy-btn-cost js-btn-cost">💵 15</span>
                <span class="buy-btn-need js-btn-need" style="display:none;"></span>
            </button>
        `;

        const buyBtn = card.querySelector(".js-buy-btn");
        buyBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            handleUpgradeClick(def.id);
        });

        list.appendChild(card);

        shopCardsMap.set(def.id, {
            card, def,
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
    document.querySelectorAll(".cat-tab").forEach(tab => tab.classList.toggle("active", tab.dataset.cat === cat));
    shopCardsMap.forEach(({ card, def }) => {
        card.style.display = (cat === "all" || def.category === cat) ? "flex" : "none";
    });
}

function updateShopUI() {
    shopCardsMap.forEach(({ card, def, lvEl, mFillEl, mLabelEl, mBonusEl, statEl, buyBtn, btnLvEl, btnCostEl, btnNeedEl }) => {
        const curLv = gameState.upgrades[def.id] || 0;
        const isMax = curLv >= (def.maxLv || 100);
        let cost = 0;
        let lv = curLv;
        const targetAdds = buyMultiplier === "max" ? 100 : Number(buyMultiplier);
        let count = 0;
        while (count < targetAdds && lv < (def.maxLv || 100)) {
            const singleCost = Math.round(def.baseCost * Math.pow(def.costMult, lv));
            if (buyMultiplier === "max" && (cost + singleCost > gameState.coins)) break;
            cost += singleCost;
            lv++;
            count++;
        }

        const canAfford = !isMax && count > 0 && gameState.coins >= cost;
        lvEl.textContent = `Lv.${curLv}`;
        const milestone = getMilestoneInfo(curLv, def.maxLv);
        mFillEl.style.width = `${milestone.pct}%`;
        mLabelEl.textContent = isMax ? 'MAXED' : `${curLv}/${milestone.next}`;
        mBonusEl.textContent = milestone.isMaxMilestone ? 'Max Bonus!' : `+2x at Lv.${milestone.next}`;

        card.classList.toggle("can-buy", canAfford);
        buyBtn.classList.toggle("can-buy", canAfford);
        buyBtn.classList.toggle("disabled", !canAfford && !isMax);
        buyBtn.classList.toggle("maxed", isMax);

        if (isMax) {
            btnLvEl.textContent = '🌟';
            btnCostEl.textContent = 'MAX';
            btnNeedEl.style.display = 'none';
        } else {
            btnLvEl.textContent = `+${count || 1}`;
            btnCostEl.textContent = `💵 ${formatNumber(cost)}`;
            if (!canAfford && cost > gameState.coins) {
                btnNeedEl.style.display = 'block';
                btnNeedEl.textContent = `Need ${formatNumber(cost - gameState.coins)}`;
            } else {
                btnNeedEl.style.display = 'none';
            }
        }
    });

    updateWorldPadsUI();
}

function handleUpgradeClick(defId) {
    const def = UPGRADE_DEFS.find(u => u.id === defId);
    if (!def) return;
    const curLv = gameState.upgrades[defId] || 0;
    let cost = 0;
    let lv = curLv;
    const targetAdds = buyMultiplier === "max" ? 100 : Number(buyMultiplier);
    let count = 0;
    while (count < targetAdds && lv < (def.maxLv || 100)) {
        const singleCost = Math.round(def.baseCost * Math.pow(def.costMult, lv));
        if (buyMultiplier === "max" && (cost + singleCost > gameState.coins)) break;
        cost += singleCost;
        lv++;
        count++;
    }

    if (count > 0 && gameState.coins >= cost) {
        gameState.coins -= cost;
        const newLv = curLv + count;
        gameState.upgrades[defId] = newLv;
        audio.playSfx('upgrade');

        if (defId === "sawCount") updateSaws3D();

        [10, 25, 50, 100].forEach(m => {
            if (curLv < m && newLv >= m) {
                showCelebratoryBanner(`🎉 MILESTONE! ${def.name} reached Lv.${m}! 2x Speed Boost!`);
            }
        });

        const screenCenter = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        floatingTexts2D.push(new FloatingText2D(screenCenter.x, screenCenter.y, `Level UP! +${count}`, "#10b981", 24));

        for (let k = 0; k < 20; k++) {
            particles2D.push(new Particle2D(
                screenCenter.x, screenCenter.y,
                (Math.random() - 0.5) * 120,
                -Math.random() * 80 - 30,
                ["#10b981", "#f59e0b", "#38bdf8", "#ec4899"][k % 4],
                4, 0.8
            ));
        }

        if (gameState.tutorialStep === 1) {
            gameState.tutorialStep = 2;
            updateTutorial();
        }

        updateShopUI();
    } else {
        const cardObj = shopCardsMap.get(defId);
        if (cardObj) {
            cardObj.card.classList.add("shake");
            setTimeout(() => cardObj.card.classList.remove("shake"), 400);
        }
        showToast(`Need 💵 ${formatNumber(cost - gameState.coins)} more cash!`);
    }
}

function updateTutorial() {
    const tut = document.getElementById("tutorial-toast");
    if (!tut) return;
    if (gameState.tutorialStep === 0) {
        tut.textContent = "👆 Step 1/3: Tap anywhere on the mill to boost speed & cash!";
        tut.style.display = "block";
    } else if (gameState.tutorialStep === 1) {
        tut.textContent = "🟩 Step 2/3: Tap the green 3D upgrade pads on the ground!";
        tut.style.display = "block";
        pointingHandSprite.visible = true;
    } else if (gameState.tutorialStep === 2) {
        tut.textContent = "🚛 Step 3/3: Watch trucks deliver lumber—clear traffic jams!";
        tut.style.display = "block";
        pointingHandSprite.visible = false;
    } else {
        tut.style.display = "none";
        pointingHandSprite.visible = false;
    }
}

function checkMilestones() {
    ACHIEVEMENTS.forEach(ach => {
        if (!gameState.achievements.includes(ach.id) && ach.cond(gameState)) {
            gameState.achievements.push(ach.id);
            gameState.coins += ach.reward;
            showCelebratoryBanner(`🏆 ${ach.name}! +💵 ${formatNumber(ach.reward)}`);
            audio.playSfx('cash');
        }
    });

    if (gameState.woodTier < WOOD_TIERS.length - 1) {
        const nextTier = WOOD_TIERS[gameState.woodTier + 1];
        if (gameState.totalEarned >= nextTier.unlockCost) {
            gameState.woodTier++;
            showCelebratoryBanner(`🪵 Unlocked ${nextTier.name} Wood! Value x${nextTier.value}`);
            audio.playSfx('upgrade');
            updateLumberTower3D();
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
// 7. MODALS & UI HANDLERS
// ==========================================
function setupUI() {
    document.querySelectorAll(".mult-btn").forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll(".mult-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            buyMultiplier = btn.dataset.mult;
            updateShopUI();
        };
    });

    document.querySelectorAll(".cat-tab").forEach(tab => {
        tab.onclick = () => filterShopCategory(tab.dataset.cat);
    });

    const mobileBtn = document.getElementById("shop-toggle-mobile");
    const shopPanel = document.getElementById("shop-panel");
    mobileBtn.onclick = () => {
        shopPanel.classList.toggle("open");
        mobileBtn.textContent = shopPanel.classList.contains("open") ? "✕ Close" : "🛒 Upgrades";
    };

    document.getElementById("btn-tap-boost").onclick = () => applyTapBoost(window.innerWidth / 2, window.innerHeight / 2);
    document.getElementById("btn-watch-boost").onclick = () => {
        watchBoostRemaining = 180;
        showCelebratoryBanner("🎬 2X BOOST ACTIVE FOR 3 MINUTES!");
        audio.playSfx('upgrade');
    };

    document.getElementById("btn-daily").onclick = () => openModal("modal-daily");
    document.getElementById("btn-close-daily").onclick = () => closeModal("modal-daily");
    document.getElementById("btn-claim-daily").onclick = () => {
        gameState.coins += 1000;
        gameState.totalEarned += 1000;
        audio.playSfx('cash');
        closeModal("modal-daily");
        showToast("Claimed 💵 1,000 Cash!");
    };

    document.getElementById("btn-achievements").onclick = openAchievementsModal;
    document.getElementById("achievements-close").onclick = () => closeModal("modal-achievements");

    document.getElementById("btn-open-leaderboard").onclick = openLeaderboardModal;
    document.getElementById("leaderboard-close").onclick = () => closeModal("modal-leaderboard");
    document.getElementById("btn-refresh-leaderboard").onclick = fetchLeaderboard;

    document.getElementById("btn-prestige").onclick = openPrestigeModal;
    document.getElementById("prestige-close").onclick = () => closeModal("modal-prestige");
    document.getElementById("btn-cancel-prestige").onclick = () => closeModal("modal-prestige");

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
        document.getElementById("start-screen").classList.remove("hidden");
    };

    document.getElementById("btn-reset-save").onclick = () => {
        if (confirm("Reset all game data? This cannot be undone!")) {
            localStorage.clear();
            location.reload();
        }
    };

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

    document.getElementById("auth-close").onclick = () => closeModal("modal-auth");
    document.getElementById("pwd-toggle").onclick = () => {
        const f = document.getElementById("auth-password");
        f.type = f.type === "password" ? "text" : "password";
    };
    document.getElementById("btn-do-login").onclick = () => performAuth(false);
    document.getElementById("btn-do-register").onclick = () => performAuth(true);
}

function openModal(id) { document.getElementById(id)?.classList.add("active"); }
function closeModal(id) { document.getElementById(id)?.classList.remove("active"); }

function openAchievementsModal() {
    const list = document.getElementById("achievements-list");
    list.innerHTML = "";
    ACHIEVEMENTS.forEach(ach => {
        const isDone = gameState.achievements.includes(ach.id);
        const card = document.createElement("div");
        card.style.cssText = "background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:10px 12px; display:flex; align-items:center; gap:12px;";
        card.innerHTML = `
            <div style="font-size:24px;">${ach.icon}</div>
            <div style="flex:1;">
                <div style="font-weight:800; font-size:13px;">${escapeHtml(ach.name)}</div>
                <div style="font-size:11px; color:var(--text-sub);">${escapeHtml(ach.desc)}</div>
                <div style="font-size:11px; font-weight:800; color:#10b981;">+💵 ${formatNumber(ach.reward)}</div>
            </div>
            <div style="font-size:11px; font-weight:800; padding:4px 8px; border-radius:8px; background:${isDone ? '#047857' : 'rgba(255,255,255,0.08)'}; color:${isDone ? '#a7f3d0' : 'var(--text-sub)'};">
                ${isDone ? '✓ Done' : 'Locked'}
            </div>
        `;
        list.appendChild(card);
    });
    openModal("modal-achievements");
}

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
                row.style.cssText = `display:flex; align-items:center; justify-content:space-between; padding:10px 12px; background:rgba(0,0,0,0.3); border:1px solid ${isMe ? '#10b981' : 'rgba(255,255,255,0.06)'}; border-radius:12px; font-size:13px;`;
                row.innerHTML = `
                    <div style="font-weight:900; width:32px;">${rankLabel}</div>
                    <div style="flex:1; font-weight:800;">${escapeHtml(user.username)} ${isMe ? '(You)' : ''}</div>
                    <div style="font-weight:900; color:#10b981;">💵 ${formatNumber(user.totalEarned || user.coins || 0)}</div>
                `;
                list.appendChild(row);
            });
        }
    } catch(e) {
        list.innerHTML = `<div style="text-align:center; padding:20px; color:#f87171;">Could not reach cloud leaderboard.<br><small style="color:var(--text-sub);">Check Wi-Fi or server tunnel status.</small></div>`;
    }
}

function openPrestigeModal() {
    const acornsToGain = Math.max(0, Math.floor(Math.sqrt((gameState.totalEarned || 0) / 10000)) - (gameState.goldenAcorns || 0));
    const nextBoost = (gameState.goldenAcorns + acornsToGain) * 5;
    document.getElementById("prestige-acorns-gain").textContent = `+${acornsToGain} Golden Acorns`;
    document.getElementById("prestige-boost-gain").textContent = `+${nextBoost}% Global Profit Forever`;

    document.getElementById("btn-do-prestige").onclick = () => {
        if (acornsToGain <= 0) {
            showToast("Earn more cash to unlock Golden Acorns on reset!");
            return;
        }
        gameState.goldenAcorns += acornsToGain;
        gameState.prestigeCount++;
        gameState.coins = 100;
        gameState.upgrades = createDefaultState().upgrades;
        audio.playSfx('upgrade');
        showCelebratoryBanner(`🌲 Forest Replanted! +${acornsToGain} Golden Acorns Claimed!`);
        closeModal("modal-prestige");
        updateShopUI();
    };
    openModal("modal-prestige");
}

async function performAuth(isRegister) {
    const userField = document.getElementById("auth-username");
    const pwdField = document.getElementById("auth-password");
    const msg = document.getElementById("auth-msg");
    const username = userField.value.trim();
    const password = pwdField.value;

    if (username.length < 3 || username.length > 20 || password.length < 6) {
        msg.style.display = "block";
        msg.style.background = "rgba(239,68,68,0.2)";
        msg.style.color = "#f87171";
        msg.textContent = "Username 3-20 chars, password min 6 chars.";
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
            msg.style.display = "block";
            msg.textContent = data.error || "Auth failed";
            return;
        }

        currentUser = { username: data.user.username, passwordHash, token: data.token };
        closeModal("modal-auth");
        document.getElementById("start-screen").classList.add("hidden");

        const localSave = Storage.loadLocal(username);
        const cloudSave = data.save;
        if (cloudSave && cloudSave.totalEarned) {
            gameState = cloudSave;
        } else if (localSave) {
            gameState = localSave;
            Storage.syncToCloud();
        }
        onGameStarted();
    } catch(e) {
        msg.style.display = "block";
        msg.textContent = "Cannot reach server. Check tunnel URL.";
    }
}

function onGameStarted() {
    document.getElementById("badge-user").textContent = currentUser ? `👤 ${escapeHtml(currentUser.username)}` : "👤 Guest";
    initShopCards();

    // Auto-save interval
    setInterval(() => {
        Storage.saveLocal();
        Storage.syncToCloud();
    }, API_CONFIG.SAVE_INTERVAL_MS);

    // Random Tycoon Events
    setInterval(() => {
        if (Math.random() < 0.5) {
            rushHourRemaining = 30;
            showCelebratoryBanner("⚡ RUSH HOUR! 2X SPEED FOR 30s!");
            audio.playSfx('upgrade');
        }
    }, 45000);
}

// ==========================================
// 8. MAIN 60FPS ANIMATION LOOP
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

        update3DProductionLine(dt);

        // Three.js Render
        renderer.render(scene, camera);

        // Render 2D Overlay Particles & Floating Cash
        const w = overlayCanvas.width;
        const h = overlayCanvas.height;
        overlayCtx.clearRect(0, 0, w, h);

        particles2D.forEach((p, idx) => {
            p.update(dt);
            p.draw(overlayCtx);
            if (p.life <= 0) particles2D.splice(idx, 1);
        });

        floatingTexts2D.forEach((ft, idx) => {
            ft.update(dt);
            ft.draw(overlayCtx);
            if (ft.life <= 0) floatingTexts2D.splice(idx, 1);
        });

        // Update Top HUD
        document.getElementById("coin-counter").textContent = formatNumber(gameState.coins);
        document.getElementById("acorn-count").textContent = gameState.goldenAcorns;

        const curTier = WOOD_TIERS[gameState.woodTier];
        document.getElementById("badge-tier-name").textContent = `🪵 ${curTier.name} Mill`;
        document.getElementById("badge-tier-mult").textContent = `x${curTier.value}`;

        const approxRate = (2.2 + (gameState.upgrades.convSpeed || 1) * 0.18) * 4 * curTier.value * (1 + (gameState.upgrades.woodValue || 0) * 0.2) * (1 + gameState.goldenAcorns * 0.05);
        document.getElementById("income-counter").textContent = `+💵 ${formatNumber(approxRate)}/s`;

        updateShopUI();
    }

    requestAnimationFrame(gameLoop);
}

window.addEventListener("beforeunload", () => Storage.saveLocal());
document.addEventListener("visibilitychange", () => { if (document.hidden) Storage.saveLocal(); });

window.addEventListener("DOMContentLoaded", () => {
    init3DScene();
    setupUI();
    onWindowResize();
    requestAnimationFrame(gameLoop);

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
    f.write(html_3d)

print(f"Successfully generated 3D WebGL index.html ({len(html_3d)} bytes)")
