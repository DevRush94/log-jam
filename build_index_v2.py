# -*- coding: utf-8 -*-
"""
Generator for Log Jam - YouTube Shorts Reference Match:
Features:
- Dense low-poly pine forest border
- Skyscraper towering lumber stack
- Cargo ship & harbor crane
- Orange delivery trucks with angry emoji bubbles (😡) during traffic jam
- In-world 3D green upgrade pads (UPGRADE 200 💵) directly clickable on the canvas
- Flying banknote cash particles (+💵 100)
- Clean top money badge [ 💵 22,450 ]
- Full idle tycoon progression, cloud saves, achievements, and leaderboard
"""

html_code = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Log Jam: Mill Empire</title>
    <style>
        :root {
            --bg-color: #0f131c;
            --panel-bg: rgba(18, 24, 38, 0.96);
            --panel-border: rgba(255, 255, 255, 0.12);
            --cash-green: #22c55e;
            --cash-glow: rgba(34, 197, 94, 0.45);
            --gold: #ffcf33;
            --gold-glow: rgba(255, 207, 51, 0.45);
            --wood-bark: #4a2f1b;
            --wood-mid: #85532a;
            --wood-light: #d69854;
            --truck-orange: #ea580c;
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
            background: var(--bg-color);
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
            top: 12px;
            left: 12px;
            right: 12px;
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

        /* Clean Cash Pill matching YouTube Short */
        .cash-pill-box {
            background: rgba(15, 23, 42, 0.92);
            border: 2.5px solid #10b981;
            border-radius: 20px;
            padding: 8px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            backdrop-filter: blur(10px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.5), 0 0 15px rgba(16, 185, 129, 0.3);
            pointer-events: auto;
            min-width: 150px;
            transition: transform 0.12s ease;
        }
        .cash-pill-box.bounce {
            transform: scale(1.1);
        }
        .cash-icon-badge {
            background: linear-gradient(135deg, #10b981, #059669);
            color: #fff;
            font-size: 14px;
            font-weight: 900;
            padding: 2px 8px;
            border-radius: 8px;
            letter-spacing: -0.5px;
            box-shadow: 0 2px 6px rgba(16, 185, 129, 0.4);
        }
        .cash-digits {
            font-size: 24px;
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

        /* Pill Buttons */
        .hud-pill {
            background: rgba(18, 24, 38, 0.9);
            border: 1px solid var(--panel-border);
            padding: 7px 14px;
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
            background: #22c55e;
            box-shadow: 0 0 6px #22c55e;
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

        /* In-Canvas Traffic Jam Alert Banner */
        #traffic-alert {
            position: absolute;
            top: 76px;
            left: 50%;
            transform: translateX(-50%) translateY(-150%);
            background: linear-gradient(135deg, #ef4444, #dc2626);
            border: 2px solid #fff;
            border-radius: 20px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: 900;
            color: #fff;
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.5);
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

        /* Celebratory Milestone / Event Banner */
        #event-banner {
            position: absolute;
            top: 70px;
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

        /* Desktop Upgrade Drawer & Mobile Bottom Sheet */
        #shop-panel {
            width: 420px;
            height: 100%;
            background: var(--panel-bg);
            border-left: 1px solid var(--panel-border);
            display: flex;
            flex-direction: column;
            z-index: 20;
            box-shadow: -8px 0 30px rgba(0,0,0,0.6);
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
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: #fff;
            box-shadow: 0 2px 8px rgba(34, 197, 94, 0.4);
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
            border-color: rgba(34, 197, 94, 0.45);
            box-shadow: 0 4px 16px rgba(34, 197, 94, 0.15);
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
            background: linear-gradient(90deg, #22c55e, #f59e0b);
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
            background: linear-gradient(180deg, #22c55e 0%, #15803d 100%);
            border: none;
            color: #fff;
            padding: 8px 12px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 900;
            cursor: pointer;
            box-shadow: 0 4px 0 #166534, 0 6px 14px rgba(0,0,0,0.4);
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
            box-shadow: 0 1px 0 #166534, 0 2px 6px rgba(0,0,0,0.4);
        }
        .buy-btn.can-buy {
            background: linear-gradient(180deg, #34d399 0%, #059669 100%);
            box-shadow: 0 4px 0 #065f46, 0 6px 14px var(--cash-glow);
            animation: pulse-green 2s infinite;
        }
        @keyframes pulse-green {
            0%, 100% { box-shadow: 0 4px 0 #065f46, 0 6px 14px var(--cash-glow); }
            50% { box-shadow: 0 4px 0 #065f46, 0 8px 22px rgba(52, 211, 153, 0.85); }
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
        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
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
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: #fff;
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
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
        .input-field:focus { border-color: #22c55e; }
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
            font-size: 50px;
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
            background: linear-gradient(135deg, #22c55e, #15803d);
            color: #fff;
            box-shadow: 0 6px 25px rgba(34, 197, 94, 0.45);
        }
        .btn-huge.guest:hover { transform: translateY(-2px); box-shadow: 0 10px 35px rgba(34, 197, 94, 0.65); }
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
            border: 2px solid #22c55e;
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
    <div id="canvas-wrapper">
        <canvas id="bg-canvas"></canvas>
        <canvas id="main-canvas"></canvas>
        <canvas id="ui-canvas"></canvas>

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

            <!-- YouTube Shorts Style Clean Cash Box -->
            <div class="cash-pill-box" id="hud-coin-box">
                <span class="cash-icon-badge">💵</span>
                <div>
                    <div class="cash-digits" id="coin-counter">0</div>
                    <div class="cash-rate-tag" id="income-counter">+💵 0/s</div>
                </div>
            </div>
        </div>

        <!-- In-Canvas Traffic Jam Alert -->
        <div id="traffic-alert">
            <span>🚨 TRAFFIC JAM! Upgrade Docks or Road to clear the queue!</span>
        </div>

        <!-- Event Banner -->
        <div id="event-banner">⚡ RUSH HOUR! 2X SPEED!</div>

        <!-- Interactive 3-Step Tutorial Hint -->
        <div id="tutorial-toast">💡 Tap anywhere on the mill or click the green 3D upgrade pads!</div>

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
    </div>

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
        <div style="font-size: 24px; font-weight: 800; color: #22c55e; margin: 12px 0;" id="daily-reward-preview">
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
        <div style="background: rgba(255,207,51,0.1); border: 1px solid var(--gold-glow); padding: 14px; border-radius: 14px; text-align:center;">
            <div style="font-size: 11px; color: var(--text-sub); text-transform: uppercase; font-weight: 800;">Permanent Rewards</div>
            <div style="font-size: 28px; font-weight: 900; color: var(--gold); margin: 6px 0;" id="prestige-acorns-gain">+0 Acorns</div>
            <div style="font-size: 13px; color: #22c55e; font-weight: 700;" id="prestige-boost-gain">+0% Global Profit Forever</div>
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
 * Designed to mirror Idle Lumber Empire / YouTube Shorts reference
 */

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
    { id: "spawnRate",   name: "Log Feed Rate",       category: "forest",    icon: "🌲", baseCost: 15,    costMult: 1.15, maxLv: 100, desc: "Feed trees faster onto line" },
    { id: "convSpeed",   name: "Conveyor Speed",      category: "forest",    icon: "⏩", baseCost: 25,    costMult: 1.15, maxLv: 100, desc: "Faster roller belts" },
    { id: "sawCount",    name: "Gantry Saws",         category: "sawmill",   icon: "🪚", baseCost: 80,    costMult: 1.75, maxLv: 6,   desc: "Adds overhead swinging saws" },
    { id: "sawSpeed",    name: "Blade Speed & Cut",   category: "sawmill",   icon: "⚡", baseCost: 40,    costMult: 1.16, maxLv: 100, desc: "Fast cuts & plank output" },
    { id: "sortSpeed",   name: "Sorting Chutes",      category: "sawmill",   icon: "📦", baseCost: 50,    costMult: 1.15, maxLv: 100, desc: "Pushes cut planks to stack" },
    { id: "stackCap",    name: "Tower Height",        category: "logistics", icon: "📚", baseCost: 70,    costMult: 1.18, maxLv: 100, desc: "Massive high-rise stack" },
    { id: "craneSpeed",  name: "Gantry Crane",        category: "logistics", icon: "🏗️", baseCost: 90,    costMult: 1.16, maxLv: 100, desc: "Fast hoist onto trucks" },
    { id: "dockCount",   name: "Loading Bays",        category: "logistics", icon: "🚏", baseCost: 250,   costMult: 2.20, maxLv: 3,   desc: "Adds truck loading docks" },
    { id: "truckCount",  name: "Truck Fleet",         category: "fleet",     icon: "🚛", baseCost: 180,   costMult: 1.85, maxLv: 6,   desc: "More orange delivery trucks" },
    { id: "truckCap",    name: "Truck Flatbed Bed",   category: "fleet",     icon: "📐", baseCost: 110,   costMult: 1.22, maxLv: 100, desc: "Carry more lumber bundles" },
    { id: "truckSpeed",  name: "Highway Speed",       category: "fleet",     icon: "💨", baseCost: 95,    costMult: 1.15, maxLv: 100, desc: "Quicker delivery transit" },
    { id: "roadUpgrade", name: "Road Expansion",      category: "fleet",     icon: "🛣️", baseCost: 350,   costMult: 1.90, maxLv: 5,   desc: "Wider lanes & eliminates jams" },
    { id: "woodValue",   name: "Lumber Price",        category: "fleet",     icon: "💰", baseCost: 150,   costMult: 1.25, maxLv: 100, desc: "Cash multiplier per plank" }
];

const ACHIEVEMENTS = [
    { id: "first_log",   name: "First Cut",           icon: "🪓", desc: "Cut your first log",              cond: s => s.stats.logsProcessed >= 1,   reward: 20 },
    { id: "logs_50",     name: "Lumberjack",          icon: "🌲", desc: "Cut 50 logs",                     cond: s => s.stats.logsProcessed >= 50,  reward: 100 },
    { id: "logs_500",    name: "Master Faller",       icon: "🪵", desc: "Cut 500 logs",                    cond: s => s.stats.logsProcessed >= 500, reward: 1000 },
    { id: "first_truck", name: "Cargo Away!",         icon: "🚛", desc: "Complete 1 truck delivery",       cond: s => s.stats.deliveries >= 1,      reward: 35 },
    { id: "trucks_25",   name: "Fleet Logistician",   icon: "🛣️", desc: "Complete 25 truck deliveries",    cond: s => s.stats.deliveries >= 25,     reward: 500 },
    { id: "coins_1k",    name: "Small Business",      icon: "💵", desc: "Earn 1,000 total cash",          cond: s => s.totalEarned >= 1000,        reward: 50 },
    { id: "coins_100k",  name: "Log Jam Mogul",       icon: "💰", desc: "Earn 100,000 total cash",        cond: s => s.totalEarned >= 100000,      reward: 2500 },
    { id: "tier_oak",    name: "Hardwood Era",        icon: "🍂", desc: "Unlock Oak wood tier",            cond: s => s.woodTier >= 1,              reward: 250 },
    { id: "jam_cleared", name: "Traffic Controller",  icon: "🚨", desc: "Clear a 4-truck traffic jam",     cond: s => s.stats.jamsCleared >= 1,     reward: 300 }
];

// Diegetic 3D In-World Upgrade Pads (matching YouTube Shorts)
const WORLD_UPGRADE_PADS = [
    { id: "pad_saw",   defId: "sawSpeed",   label: "UPGRADE SAWS",  icon: "🪚", x: 4.8,  y: 2.2 },
    { id: "pad_crane", defId: "craneSpeed", label: "UPGRADE CRANE", icon: "🏗️", x: 10.5, y: 3.5 },
    { id: "pad_fleet", defId: "truckCount", label: "MORE TRUCKS",   icon: "🚛", x: 14.0, y: 3.0 },
    { id: "pad_road",  defId: "roadUpgrade",label: "WIDEN ROAD",    icon: "🛣️", x: 14.0, y: 8.5 }
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

// Audio Engine
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.sfxEnabled = true;
        this.musicEnabled = true;
        this.sfxGain = null;
        this.musicGain = null;
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
                osc.frequency.setValueAtTime(900, now);
                osc.frequency.exponentialRampToValueAtTime(1800, now + 0.1);
                g.gain.setValueAtTime(0.2, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
                osc.connect(g); g.connect(this.sfxGain);
                osc.start(now); osc.stop(now + 0.1);
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
                [240, 320].forEach(f => {
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
                g.gain.setValueAtTime(0.1, now);
                g.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
                osc.connect(g); g.connect(this.sfxGain);
                osc.start(now); osc.stop(now + 0.12);
            }
        } catch(e) {}
    }
}
const audio = new SoundEngine();

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
            jamsCleared: 0,
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
let tapBoostRemaining = 0;
let watchBoostRemaining = 0;
let rushHourRemaining = 0;
let isTrafficJam = false;

// Storage
const Storage = {
    GUEST_KEY: "logjam_save_guest",
    USER_KEY_PREFIX: "logjam_save_user_",
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

// Isometric Projection
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

class FloatingText {
    constructor(x, y, text, color = "#22c55e", size = 16) {
        this.x = x; this.y = y; this.text = text; this.color = color;
        this.size = size; this.life = 1.2; this.maxLife = 1.2;
    }
    update(dt) { this.y -= 26 * dt; this.life -= dt; }
    draw(ctx) {
        const a = Math.max(0, this.life / this.maxLife);
        ctx.save();
        ctx.globalAlpha = a;
        ctx.fillStyle = this.color;
        ctx.font = `900 ${this.size}px ${getComputedStyle(document.body).fontFamily}`;
        ctx.textAlign = "center";
        ctx.shadowColor = "rgba(0,0,0,0.8)";
        ctx.shadowBlur = 4;
        ctx.fillText(this.text, this.x, this.y);
        ctx.restore();
    }
}

let particles = [];
let floatingTexts = [];
let logs = [];
let planks = [];
let lumberTowerCount = 4; // High-rise stack pile
let trucks = [];
let looseChips = [];

const bgCanvas = document.getElementById("bg-canvas");
const mainCanvas = document.getElementById("main-canvas");
const uiCanvas = document.getElementById("ui-canvas");
const bgCtx = bgCanvas.getContext("2d");
const mainCtx = mainCanvas.getContext("2d");
const uiCtx = uiCanvas.getContext("2d");
let camera = { x: 0, y: 0 };

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

    camera.x = w / 2 - 20;
    camera.y = h / 2 - 50;
    renderBackground();
}
window.addEventListener("resize", resizeCanvases);

// Render 3D Low-Poly Forest & Background
function renderBackground() {
    const w = bgCanvas.parentElement.clientWidth;
    const h = bgCanvas.parentElement.clientHeight;
    bgCtx.clearRect(0, 0, w, h);

    bgCtx.save();
    bgCtx.translate(camera.x, camera.y);

    // Ground Terrain
    for (let x = -4; x <= 16; x++) {
        for (let y = -2; y <= 16; y++) {
            const p = toIso(x, y, 0);
            let fill = (x >= 13 && x <= 15) ? "#334155" : // Asphalt Road
                       (x > 15) ? "#0284c7" : // River
                       ((x + y) % 2 === 0 ? "#4ade80" : "#22c55e"); // Bright Stylized Grass

            if (x >= 4 && x <= 11 && y >= 3 && y <= 9) {
                fill = "#d97706"; // Factory Yard Sandy Dirt
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

    // Road Lane Lines
    for (let y = -2; y <= 15; y += 2) {
        const rp = toIso(14, y, 0);
        bgCtx.fillStyle = "#ffffff";
        bgCtx.fillRect(rp.x - 2, rp.y + 12, 4, 8);
    }

    // Wooden Bridge
    const bp = toIso(14, 11, 0.2);
    bgCtx.fillStyle = "#b45309";
    bgCtx.fillRect(bp.x - 36, bp.y - 10, 72, 30);
    bgCtx.strokeStyle = "#78350f";
    bgCtx.lineWidth = 2;
    bgCtx.strokeRect(bp.x - 36, bp.y - 10, 72, 30);

    // Dense Low-Poly Pine Forest on Perimeter
    const treeCoords = [
        [-3,-1], [-2,-1], [-1,-1], [0,-1], [1,-1],
        [-3,1], [-3,3], [-3,5], [-3,7], [-2,9], [-1,11],
        [2,12], [4,13], [6,14], [8,14]
    ];
    treeCoords.forEach(([tx, ty]) => {
        const tp = toIso(tx, ty, 0);
        drawLowPolyPine(bgCtx, tp.x, tp.y);
    });

    // Harbor Dock Pier & Berthed Cargo Ship
    const dp = toIso(16, 5, 0);
    bgCtx.fillStyle = "#94a3b8"; // Concrete dock apron
    bgCtx.fillRect(dp.x - 20, dp.y - 15, 40, 50);

    // Cargo Ship
    const sp = toIso(17, 7, 0.1);
    bgCtx.fillStyle = "#f8fafc"; // White hull
    bgCtx.beginPath();
    bgCtx.ellipse(sp.x + 10, sp.y, 34, 16, 0, 0, Math.PI * 2);
    bgCtx.fill();
    bgCtx.fillStyle = "#0284c7"; // Blue deck cabin
    bgCtx.fillRect(sp.x - 4, sp.y - 12, 16, 12);

    bgCtx.restore();
}

function drawLowPolyPine(ctx, x, y) {
    ctx.fillStyle = "rgba(0,0,0,0.18)";
    ctx.beginPath();
    ctx.ellipse(x, y + 14, 18, 9, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#78350f";
    ctx.fillRect(x - 3, y - 4, 6, 16);

    const foliageColors = ["#14532d", "#166534", "#15803d"];
    foliageColors.forEach((c, idx) => {
        ctx.fillStyle = c;
        ctx.beginPath();
        ctx.moveTo(x, y - 38 - idx * 12);
        ctx.lineTo(x + 20 - idx * 2, y - 10 - idx * 12);
        ctx.lineTo(x - 20 + idx * 2, y - 10 - idx * 12);
        ctx.closePath();
        ctx.fill();
    });
}

function drawIsoBox(ctx, x, y, z, w, h, d, topColor, leftColor, rightColor) {
    const p = toIso(x, y, z);
    const sw = w * (TILE_W / 2);
    const sh = h * (TILE_H / 2);
    const sz = d * 18;

    // Top
    ctx.fillStyle = topColor;
    ctx.beginPath();
    ctx.moveTo(p.x, p.y - sz);
    ctx.lineTo(p.x + sw, p.y + sh - sz);
    ctx.lineTo(p.x, p.y + sh * 2 - sz);
    ctx.lineTo(p.x - sw, p.y + sh - sz);
    ctx.closePath();
    ctx.fill();

    // Left
    ctx.fillStyle = leftColor;
    ctx.beginPath();
    ctx.moveTo(p.x - sw, p.y + sh - sz);
    ctx.lineTo(p.x, p.y + sh * 2 - sz);
    ctx.lineTo(p.x, p.y + sh * 2);
    ctx.lineTo(p.x - sw, p.y + sh);
    ctx.closePath();
    ctx.fill();

    // Right
    ctx.fillStyle = rightColor;
    ctx.beginPath();
    ctx.moveTo(p.x + sw, p.y + sh - sz);
    ctx.lineTo(p.x, p.y + sh * 2 - sz);
    ctx.lineTo(p.x, p.y + sh * 2);
    ctx.lineTo(p.x + sw, p.y + sh);
    ctx.closePath();
    ctx.fill();
}

// Draw In-World Diegetic 3D Upgrade Pad
function drawWorldUpgradePad(ctx, pad) {
    const def = UPGRADE_DEFS.find(u => u.id === pad.defId);
    if (!def) return;
    const curLv = gameState.upgrades[pad.defId] || 0;
    const isMax = curLv >= (def.maxLv || 100);
    const cost = Math.round(def.baseCost * Math.pow(def.costMult, curLv));
    const canAfford = !isMax && gameState.coins >= cost;

    const p = toIso(pad.x, pad.y, 0.05);

    // Base Pad Box
    const topCol = canAfford ? "#22c55e" : "#334155";
    const leftCol = canAfford ? "#16a34a" : "#1e293b";
    const rightCol = canAfford ? "#15803d" : "#0f172a";

    // Pad shadow
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.beginPath();
    ctx.ellipse(p.x, p.y + 12, 38, 18, 0, 0, Math.PI * 2);
    ctx.fill();

    drawIsoBox(ctx, pad.x, pad.y, 0.05, 1.2, 1.2, 0.2, topCol, leftCol, rightCol);

    // Glowing border if affordable
    if (canAfford) {
        ctx.strokeStyle = "#4ade80";
        ctx.lineWidth = 2.5;
        const sw = 1.2 * (TILE_W / 2);
        const sh = 1.2 * (TILE_H / 2);
        ctx.beginPath();
        ctx.moveTo(p.x, p.y - 4);
        ctx.lineTo(p.x + sw, p.y + sh - 4);
        ctx.lineTo(p.x, p.y + sh * 2 - 4);
        ctx.lineTo(p.x - sw, p.y + sh - 4);
        ctx.closePath();
        ctx.stroke();
    }

    // Text on Pad
    ctx.fillStyle = "#ffffff";
    ctx.font = "900 11px sans-serif";
    ctx.textAlign = "center";
    ctx.shadowColor = "rgba(0,0,0,0.7)";
    ctx.shadowBlur = 3;
    ctx.fillText(`${pad.icon} ${pad.label}`, p.x, p.y + 14);

    ctx.fillStyle = canAfford ? "#fef08a" : "#cbd5e1";
    ctx.font = "900 12px sans-serif";
    ctx.fillText(isMax ? 'MAX' : `💵 ${formatNumber(cost)}`, p.x, p.y + 26);
}

// Draw Orange Flatbed Delivery Truck with Traffic Jam Emoji Bubbles
function drawTruckEntity(ctx, t) {
    const p = toIso(t.x, t.y, 0);
    const wobble = t.onBridge ? Math.sin(Date.now() * 0.02) * 3 : 0;

    // Truck Shadow
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.beginPath();
    ctx.ellipse(p.x, p.y + 10, 24, 12, 0, 0, Math.PI * 2);
    ctx.fill();

    // Wheels
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(p.x - 18, p.y + 2 + wobble, 8, 8);
    ctx.fillRect(p.x + 10, p.y + 2 + wobble, 8, 8);

    // Truck Cab (Orange / White)
    drawIsoBox(ctx, t.x - 0.2, t.y, 0.2 + wobble * 0.02, 0.6, 0.6, 0.8, "#ea580c", "#c2410c", "#9a3412");

    // Windshield
    ctx.fillStyle = "#e0f2fe";
    ctx.fillRect(p.x - 4, p.y - 16 + wobble, 10, 6);

    // Flatbed
    drawIsoBox(ctx, t.x + 0.5, t.y, 0.1 + wobble * 0.02, 0.8, 0.7, 0.4, "#64748b", "#475569", "#334155");

    // Loaded Stacks
    if (t.cargoStacks > 0) {
        const tier = WOOD_TIERS[gameState.woodTier];
        for (let s = 0; s < t.cargoStacks; s++) {
            drawIsoBox(ctx, t.x + 0.5, t.y, 0.5 + s * 0.3 + wobble * 0.02, 0.6, 0.5, 0.25, tier.plankColor, tier.barkColor, tier.barkColor);
        }
    }

    // Traffic Jam Angry Emoji Bubble (😡) if waiting in queue
    if (t.isJammed) {
        const bob = Math.sin(Date.now() * 0.008 + t.id) * 3;
        const bx = p.x;
        const by = p.y - 38 + bob;

        // White speech bubble pin
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(bx, by, 14, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ef4444";
        ctx.lineWidth = 2;
        ctx.stroke();

        // Pin tail
        ctx.beginPath();
        ctx.moveTo(bx - 4, by + 12);
        ctx.lineTo(bx, by + 18);
        ctx.lineTo(bx + 4, by + 12);
        ctx.fill();

        // Angry Face (😡)
        ctx.font = "16px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("😡", bx, by + 6);
    }
}

// Production Line Systems
let spawnTimer = 0;
let craneTimer = 0;

function updateProductionLine(dt) {
    const speedMult = (tapBoostRemaining > 0 ? 1.5 : 1.0) *
                      (rushHourRemaining > 0 ? 2.0 : 1.0) *
                      (watchBoostRemaining > 0 ? 2.0 : 1.0);

    // 1. Spawner
    const spawnRateLv = gameState.upgrades.spawnRate || 0;
    const spawnInterval = Math.max(0.3, (2.0 / (1 + spawnRateLv * 0.18)) / speedMult);
    spawnTimer += dt;
    if (spawnTimer >= spawnInterval && logs.length < 16) {
        spawnTimer = 0;
        logs.push({
            x: 0.5, y: 3.5, z: 0.2,
            tier: gameState.woodTier,
            cutProgress: 0,
            id: Math.random()
        });
    }

    // 2. Conveyor & Gantry Saws
    const convSpeedLv = gameState.upgrades.convSpeed || 0;
    const convSpeed = (1.6 + convSpeedLv * 0.15) * speedMult;
    const numSaws = Math.min(6, Math.max(1, gameState.upgrades.sawCount || 1));
    const sawSpeedLv = gameState.upgrades.sawSpeed || 0;
    const cutDuration = Math.max(0.2, (1.3 / (1 + sawSpeedLv * 0.2)) / speedMult);

    for (let i = logs.length - 1; i >= 0; i--) {
        const log = logs[i];
        if (log.x >= 4.5 && log.x < 5.0) {
            log.cutProgress += dt;
            if (Math.random() < 0.35) {
                const lp = toIso(log.x, log.y, log.z);
                particles.push(new Particle(
                    lp.x + (Math.random() - 0.5) * 16,
                    lp.y - 12 + (Math.random() - 0.5) * 8,
                    (Math.random() - 0.5) * 40,
                    -Math.random() * 50 - 20,
                    Math.random() > 0.4 ? "#f59e0b" : "#fcd34d",
                    Math.random() * 3 + 1,
                    0.4
                ));
                audio.playSfx('saw');
            }

            if (log.cutProgress >= cutDuration) {
                logs.splice(i, 1);
                gameState.stats.logsProcessed++;

                // Chutes transfer cut lumber into the skyscraper pile
                const segments = 3 + Math.min(3, Math.floor((gameState.upgrades.sawSpeed || 0) / 10));
                lumberTowerCount = Math.min(25, lumberTowerCount + segments);
                continue;
            }
        } else {
            log.x += convSpeed * dt;
        }
    }

    // 3. Crane System
    const craneSpeedLv = gameState.upgrades.craneSpeed || 0;
    craneTimer += dt * (1 + craneSpeedLv * 0.2) * speedMult;

    const numDocks = Math.min(3, Math.max(1, gameState.upgrades.dockCount || 1));
    const maxTrucks = Math.min(6, Math.max(1, gameState.upgrades.truckCount || 1));
    const truckCapLv = gameState.upgrades.truckCap || 0;
    const truckCapacity = 2 + Math.floor(truckCapLv / 4);
    const truckSpeedLv = gameState.upgrades.truckSpeed || 0;
    const truckSpeed = (2.2 + truckSpeedLv * 0.25) * speedMult;

    // Ensure truck fleet count
    while (trucks.length < maxTrucks) {
        trucks.push({
            x: 14.0,
            y: -2.0 - trucks.length * 2.4,
            cargoStacks: 0,
            maxCapacity: truckCapacity,
            state: "driving_in",
            dockIndex: trucks.length % numDocks,
            isJammed: false,
            id: Math.random(),
            onBridge: false
        });
    }

    // Crane loading from Tower to Docked Truck
    const targetTruck = trucks.find(t => t.state === "docked" && t.cargoStacks < t.maxCapacity);
    if (lumberTowerCount >= 4 && targetTruck && craneTimer >= 1.4) {
        craneTimer = 0;
        lumberTowerCount = Math.max(0, lumberTowerCount - 3);
        targetTruck.cargoStacks++;
        const cp = toIso(targetTruck.x, targetTruck.y, 0.8);
        floatingTexts.push(new FloatingText(cp.x, cp.y, "📦 Loaded!", "#22c55e", 13));
    }

    // Truck Movement & "Log Jam" Detection
    let jammedCount = 0;
    trucks.forEach((t, idx) => {
        t.maxCapacity = truckCapacity;
        const dockY = 4.0 + (t.dockIndex % numDocks) * 2.0;

        // Check if blocked by vehicle ahead
        let blocked = false;
        for (let j = 0; j < trucks.length; j++) {
            if (j !== idx && trucks[j].y > t.y && (trucks[j].y - t.y) < 1.8) {
                blocked = true;
                break;
            }
        }

        if (blocked) {
            t.isJammed = true;
            jammedCount++;
        } else {
            t.isJammed = false;
        }

        if (!blocked && t.state === "driving_in") {
            if (t.y < dockY) {
                t.y += truckSpeed * dt;
            } else {
                t.state = "docked";
            }
        } else if (t.state === "docked") {
            if (t.cargoStacks >= t.maxCapacity) {
                t.state = "leaving";
                audio.playSfx('honk');
            }
        } else if (!blocked && t.state === "leaving") {
            t.y += truckSpeed * dt;

            if (t.y >= 10.5 && t.y <= 13.0) {
                t.onBridge = true;
            } else {
                t.onBridge = false;
            }

            // Delivered across the bridge! Cash Payout!
            if (t.y > 16.0) {
                t.state = "driving_in";
                t.y = -2.0;
                t.cargoStacks = 0;
                t.onBridge = false;

                const tier = WOOD_TIERS[gameState.woodTier];
                const woodValLv = gameState.upgrades.woodValue || 0;
                const acornMult = 1 + (gameState.goldenAcorns * 0.05);
                const payout = Math.round(t.maxCapacity * 15 * tier.value * (1 + woodValLv * 0.15) * acornMult * speedMult);

                gameState.coins += payout;
                gameState.totalEarned += payout;
                gameState.stats.deliveries++;

                // Bounce cash box
                const cashBox = document.getElementById("hud-coin-box");
                if (cashBox) {
                    cashBox.classList.add("bounce");
                    setTimeout(() => cashBox.classList.remove("bounce"), 150);
                }

                audio.playSfx('cash');
                const dp = toIso(14.0, 15.0, 0);
                floatingTexts.push(new FloatingText(dp.x, dp.y - 20, `+💵 ${formatNumber(payout)}`, "#22c55e", 20));

                for (let c = 0; c < 12; c++) {
                    particles.push(new Particle(
                        dp.x, dp.y - 20,
                        (Math.random() - 0.5) * 70,
                        -Math.random() * 80 - 20,
                        "#22c55e",
                        Math.random() * 3 + 2,
                        0.7
                    ));
                }
            }
        }
    });

    // Traffic Jam Alert Banner
    const trafficBanner = document.getElementById("traffic-alert");
    if (jammedCount >= 3) {
        if (!isTrafficJam) {
            isTrafficJam = true;
            audio.playSfx('honk');
        }
        trafficBanner.classList.add("show");
    } else {
        if (isTrafficJam) {
            isTrafficJam = false;
            gameState.stats.jamsCleared++;
            showToast("🎉 Log Jam Cleared! Traffic moving smoothly!");
        }
        trafficBanner.classList.remove("show");
    }

    checkMilestones();
}

function renderGameEntities(dt) {
    const w = mainCanvas.parentElement.clientWidth;
    const h = mainCanvas.parentElement.clientHeight;
    mainCtx.clearRect(0, 0, w, h);

    mainCtx.save();
    mainCtx.translate(camera.x, camera.y);

    // 1. Spawner & Conveyor Belt Line
    drawIsoBox(mainCtx, 0.5, 3.5, 0, 1.2, 1.2, 0.8, "#475569", "#334155", "#1e293b");
    drawIsoBox(mainCtx, 2.5, 3.5, 0, 3.2, 0.8, 0.3, "#64748b", "#475569", "#334155");

    // 2. Gantry Saws with Overhead Arches
    const numSaws = Math.min(6, Math.max(1, gameState.upgrades.sawCount || 1));
    for (let s = 0; s < numSaws; s++) {
        const sx = 4.5;
        const sy = 3.2 + (s - (numSaws - 1) / 2) * 0.35;

        // Overhead Gantry Pillars
        drawIsoBox(mainCtx, sx, sy, 0.3, 0.3, 0.3, 1.1, "#1e293b", "#0f172a", "#020617");

        // Spinning Circular Steel Saw
        const sp = toIso(sx, sy, 1.1);
        mainCtx.fillStyle = "#e2e8f0";
        mainCtx.beginPath();
        mainCtx.arc(sp.x, sp.y, 12, 0, Math.PI * 2);
        mainCtx.fill();
        mainCtx.strokeStyle = "#94a3b8";
        mainCtx.lineWidth = 2;
        mainCtx.stroke();
    }

    // 3. THE SKYSCRAPER LUMBER TOWER (matching 5xpM-hsYo3w.jpg)
    const tier = WOOD_TIERS[gameState.woodTier];
    const towerLayers = Math.min(18, Math.max(2, Math.floor(lumberTowerCount)));
    for (let l = 0; l < towerLayers; l++) {
        drawIsoBox(mainCtx, 8.5, 5.0, 0.15 + l * 0.18, 1.1, 1.1, 0.14, tier.plankColor, tier.barkColor, tier.barkColor);
    }
    // Loose logs and chips around tower base
    const baseP = toIso(8.5, 5.0, 0);
    mainCtx.fillStyle = tier.barkColor;
    mainCtx.fillRect(baseP.x - 28, baseP.y + 12, 14, 6);
    mainCtx.fillRect(baseP.x + 14, baseP.y + 8, 16, 5);

    // 4. Yellow Gantry Crane on Rails
    const cp = toIso(10.5, 5.0, 0);
    mainCtx.fillStyle = "#eab308"; // Gantry Crane Yellow
    mainCtx.fillRect(cp.x - 5, cp.y - 50, 10, 50); // Tower
    mainCtx.fillRect(cp.x - 35, cp.y - 50, 70, 7);  // Arm
    mainCtx.fillStyle = "#ef4444"; // Red hoist block
    mainCtx.fillRect(cp.x + 10, cp.y - 35, 12, 10);

    // 5. In-World Diegetic 3D Upgrade Pads (UPGRADE 200 💵)
    WORLD_UPGRADE_PADS.forEach(pad => drawWorldUpgradePad(mainCtx, pad));

    // 6. Moving Logs on Conveyor
    logs.forEach(log => {
        const lp = toIso(log.x, log.y, log.z);
        mainCtx.fillStyle = "rgba(0,0,0,0.2)";
        mainCtx.beginPath();
        mainCtx.ellipse(lp.x, lp.y + 4, 14, 7, 0, 0, Math.PI * 2);
        mainCtx.fill();

        mainCtx.fillStyle = tier.color;
        mainCtx.beginPath();
        mainCtx.arc(lp.x, lp.y - 10, 14, 0, Math.PI * 2);
        mainCtx.fill();
        mainCtx.strokeStyle = tier.barkColor;
        mainCtx.lineWidth = 2.5;
        mainCtx.stroke();
    });

    // 7. Delivery Trucks with Traffic Jam Emojis
    trucks.forEach(t => drawTruckEntity(mainCtx, t));

    mainCtx.restore();

    // Render Overlay Canvas (Particles & Floating Texts)
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

function checkMilestones() {
    ACHIEVEMENTS.forEach(ach => {
        if (!gameState.achievements.includes(ach.id) && ach.cond(gameState)) {
            gameState.achievements.push(ach.id);
            gameState.coins += ach.reward;
            showCelebratoryBanner(`🏆 ${ach.name}! +💵 ${formatNumber(ach.reward)}`);
            audio.playSfx('cash');
        }
    });

    // Wood Tier progression
    if (gameState.woodTier < WOOD_TIERS.length - 1) {
        const nextTier = WOOD_TIERS[gameState.woodTier + 1];
        if (gameState.totalEarned >= nextTier.unlockCost) {
            gameState.woodTier++;
            showCelebratoryBanner(`🪵 Unlocked ${nextTier.name} Wood! Value x${nextTier.value}`);
            audio.playSfx('upgrade');
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

// Shop Card Management
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
                <div class="upgrade-stat-row js-stat-row">+15% throughput</div>
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

        [10, 25, 50, 100].forEach(m => {
            if (curLv < m && newLv >= m) {
                showCelebratoryBanner(`🎉 MILESTONE! ${def.name} reached Lv.${m}! 2x Boost Unlocked!`);
            }
        });

        const midP = toIso(6, 4, 1.0);
        floatingTexts.push(new FloatingText(midP.x, midP.y, `Level UP! +${count}`, "#22c55e", 20));

        for (let k = 0; k < 20; k++) {
            particles.push(new Particle(
                midP.x, midP.y,
                (Math.random() - 0.5) * 100,
                -Math.random() * 80 - 30,
                ["#22c55e", "#f59e0b", "#38bdf8", "#ef4444"][k % 4],
                4, 0.8
            ));
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

// Canvas Interaction: Tap In-World 3D Upgrade Pads directly!
const canvasWrapper = document.getElementById("canvas-wrapper");

function handleCanvasClick(e) {
    const rect = canvasWrapper.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;
    const gridPos = fromIso(clickX, clickY);

    // Check if clicked directly on an in-world upgrade pad
    for (const pad of WORLD_UPGRADE_PADS) {
        if (Math.hypot(pad.x - gridPos.x, pad.y - gridPos.y) < 1.3) {
            handleUpgradeClick(pad.defId);
            return;
        }
    }

    // Otherwise tap ground -> Speed Boost
    applyTapBoost(clickX - camera.x, clickY - camera.y);
}

function applyTapBoost(localX = null, localY = null) {
    tapBoostRemaining = 8;
    gameState.stats.taps++;
    const spawnX = localX !== null ? localX : toIso(6, 4, 0.5).x;
    const spawnY = localY !== null ? localY : toIso(6, 4, 0.5).y;
    floatingTexts.push(new FloatingText(spawnX, spawnY, "⚡ SPEED BOOST!", "#f59e0b", 16));
}

// Setup Modals & Handlers
function setupUI() {
    canvasWrapper.addEventListener("click", handleCanvasClick);

    // Multiplier Toggle
    document.querySelectorAll(".mult-btn").forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll(".mult-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            buyMultiplier = btn.dataset.mult;
            updateShopUI();
        };
    });

    // Category Tabs
    document.querySelectorAll(".cat-tab").forEach(tab => {
        tab.onclick = () => filterShopCategory(tab.dataset.cat);
    });

    // Mobile Drawer
    const mobileBtn = document.getElementById("shop-toggle-mobile");
    const shopPanel = document.getElementById("shop-panel");
    mobileBtn.onclick = () => {
        shopPanel.classList.toggle("open");
        mobileBtn.textContent = shopPanel.classList.contains("open") ? "✕ Close" : "🛒 Upgrades";
    };

    // Action Pills
    document.getElementById("btn-tap-boost").onclick = () => applyTapBoost();
    document.getElementById("btn-watch-boost").onclick = () => {
        watchBoostRemaining = 180;
        showCelebratoryBanner("🎬 2X BOOST ACTIVE FOR 3 MINUTES!");
        audio.playSfx('upgrade');
    };

    // Modals
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

    // Start Screen
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

    // Auth
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
                <div style="font-size:11px; font-weight:800; color:#22c55e;">+💵 ${formatNumber(ach.reward)}</div>
            </div>
            <div style="font-size:11px; font-weight:800; padding:4px 8px; border-radius:8px; background:${isDone ? '#15803d' : 'rgba(255,255,255,0.08)'}; color:${isDone ? '#bbf7d0' : 'var(--text-sub)'};">
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
                row.style.cssText = `display:flex; align-items:center; justify-content:space-between; padding:10px 12px; background:rgba(0,0,0,0.3); border:1px solid ${isMe ? '#22c55e' : 'rgba(255,255,255,0.06)'}; border-radius:12px; font-size:13px;`;
                row.innerHTML = `
                    <div style="font-weight:900; width:32px;">${rankLabel}</div>
                    <div style="flex:1; font-weight:800;">${escapeHtml(user.username)} ${isMe ? '(You)' : ''}</div>
                    <div style="font-weight:900; color:#22c55e;">💵 ${formatNumber(user.totalEarned || user.coins || 0)}</div>
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
        gameState.coins = 0;
        gameState.upgrades = createDefaultState().upgrades;
        logs = [];
        lumberTowerCount = 4;
        trucks = [];
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

    setTimeout(() => {
        const tut = document.getElementById("tutorial-toast");
        if (tut) tut.style.display = "none";
    }, 12000);
}

// Main 60fps Loop
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

        const curTier = WOOD_TIERS[gameState.woodTier];
        document.getElementById("badge-tier-name").textContent = `🪵 ${curTier.name} Mill`;
        document.getElementById("badge-tier-mult").textContent = `x${curTier.value}`;

        const approxRate = (1.6 + (gameState.upgrades.convSpeed || 0) * 0.15) * 4 * curTier.value * (1 + (gameState.upgrades.woodValue || 0) * 0.15) * (1 + gameState.goldenAcorns * 0.05);
        document.getElementById("income-counter").textContent = `+💵 ${formatNumber(approxRate)}/s`;

        updateShopUI();
    }

    requestAnimationFrame(gameLoop);
}

window.addEventListener("beforeunload", () => Storage.saveLocal());
document.addEventListener("visibilitychange", () => { if (document.hidden) Storage.saveLocal(); });

window.addEventListener("DOMContentLoaded", () => {
    resizeCanvases();
    setupUI();
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
    f.write(html_code)

print("Successfully written index.html matching YouTube Short reference!")
