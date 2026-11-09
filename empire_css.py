# -*- coding: utf-8 -*-
CSS_CONTENT = r'''
        :root {
            --bg-color: #0b1120;
            --panel-bg: rgba(15, 23, 42, 0.94);
            --panel-border: rgba(255, 255, 255, 0.12);
            --cash-green: #10b981;
            --cash-glow: rgba(16, 185, 129, 0.5);
            --gold: #f59e0b;
            --gold-glow: rgba(245, 158, 11, 0.45);
            --cyan: #38bdf8;
            --purple: #a855f7;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --danger: #ef4444;
            --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
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

        #canvas-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            background: #dbeafe;
        }

        #webgl-canvas {
            width: 100%;
            height: 100%;
            display: block;
        }

        #overlay-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 2;
        }

        /* Top Header HUD */
        #top-hud {
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            z-index: 10;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            pointer-events: none;
        }

        .hud-group {
            display: flex;
            align-items: center;
            gap: 8px;
            pointer-events: auto;
        }

        .hud-pill {
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            border-radius: 9999px;
            padding: 6px 14px;
            display: flex;
            align-items: center;
            gap: 6px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
            font-size: 14px;
            font-weight: 700;
        }

        .cash-pill {
            color: var(--cash-green);
            border-color: rgba(16, 185, 129, 0.4);
            font-size: 16px;
            text-shadow: 0 0 10px var(--cash-glow);
        }

        .acorn-pill {
            color: var(--gold);
            border-color: rgba(245, 158, 11, 0.4);
            font-size: 14px;
        }

        .hud-btn {
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            color: var(--text-main);
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            cursor: pointer;
            backdrop-filter: blur(10px);
            transition: all 0.15s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.25);
        }

        .hud-btn:hover {
            transform: scale(1.08);
            border-color: var(--cyan);
        }

        .hud-btn:active {
            transform: scale(0.95);
        }

        /* Cinematic Zone Navigation Bar (Floating below top HUD) */
        #zone-nav-bar {
            position: absolute;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10;
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid var(--panel-border);
            padding: 4px 8px;
            border-radius: 9999px;
            backdrop-filter: blur(12px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.35);
            max-width: 95vw;
            overflow-x: auto;
            white-space: nowrap;
        }

        #zone-nav-bar::-webkit-scrollbar {
            display: none;
        }

        .zone-pill {
            background: transparent;
            border: none;
            color: var(--text-sub);
            padding: 6px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: all 0.2s ease;
        }

        .zone-pill:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.08);
        }

        .zone-pill.active {
            color: #0f172a;
            background: var(--cyan);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.6);
        }

        /* Quick Action Floating Bar */
        #quick-action-bar {
            position: absolute;
            top: 110px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9;
            display: flex;
            gap: 10px;
            pointer-events: none;
        }

        .action-banner {
            background: linear-gradient(135deg, #f59e0b, #ea580c);
            color: #fff;
            padding: 8px 18px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 16px rgba(234, 88, 12, 0.4);
            animation: bounce 1s infinite alternate ease-in-out;
            cursor: pointer;
            pointer-events: auto;
        }

        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-4px); }
        }

        /* Bottom Navigation Dock */
        #bottom-dock {
            position: absolute;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10;
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid var(--panel-border);
            padding: 6px 10px;
            border-radius: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.5);
            max-width: 98vw;
            overflow-x: auto;
        }

        #bottom-dock::-webkit-scrollbar {
            display: none;
        }

        .dock-tab {
            background: transparent;
            border: none;
            color: var(--text-sub);
            padding: 6px 10px;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
            cursor: pointer;
            transition: all 0.15s ease;
            position: relative;
            min-width: 58px;
        }

        .dock-tab .tab-icon {
            font-size: 20px;
        }

        .dock-tab .tab-label {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.3px;
            white-space: nowrap;
        }

        .dock-tab:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.08);
            transform: translateY(-2px);
        }

        .dock-tab:active {
            transform: scale(0.95);
        }

        .dock-tab.active {
            color: var(--cyan);
            background: rgba(56, 189, 248, 0.12);
        }

        .tab-badge {
            position: absolute;
            top: 2px;
            right: 6px;
            background: var(--danger);
            color: #fff;
            font-size: 9px;
            font-weight: 900;
            border-radius: 9999px;
            padding: 1px 5px;
            box-shadow: 0 0 6px var(--danger);
        }

        /* Modals & Screens */
        .modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(6px);
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
            padding: 14px;
        }

        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .modal-card {
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            border-radius: 24px;
            width: 100%;
            max-width: 580px;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 50px rgba(0,0,0,0.6);
            transform: translateY(20px) scale(0.96);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
        }

        .modal-overlay.active .modal-card {
            transform: translateY(0) scale(1);
        }

        .modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 18px 22px;
            border-bottom: 1px solid var(--panel-border);
            background: rgba(255, 255, 255, 0.02);
        }

        .modal-title {
            font-size: 18px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .modal-close {
            background: rgba(255, 255, 255, 0.08);
            border: none;
            color: var(--text-sub);
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .modal-close:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.16);
        }

        .modal-body {
            padding: 18px 22px;
            overflow-y: auto;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .modal-body::-webkit-scrollbar {
            width: 6px;
        }
        .modal-body::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 3px;
        }

        /* Generic Buttons & Cards */
        .btn-full {
            width: 100%;
            padding: 12px;
            border-radius: 14px;
            border: none;
            font-weight: 800;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #10b981, #059669);
            color: #ffffff;
            box-shadow: 0 4px 16px var(--cash-glow);
        }

        .btn-primary:hover {
            filter: brightness(1.1);
            transform: translateY(-1px);
        }

        .btn-primary:disabled {
            background: #334155;
            color: #64748b;
            box-shadow: none;
            cursor: not-allowed;
            transform: none;
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-main);
            border: 1px solid var(--panel-border);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.14);
        }

        /* Expansion & Land Buy Screen */
        .expansion-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }

        .expansion-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--panel-border);
            border-radius: 16px;
            padding: 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            transition: border-color 0.2s ease;
        }

        .expansion-card.unlocked {
            border-color: rgba(16, 185, 129, 0.4);
            background: rgba(16, 185, 129, 0.05);
        }

        .expansion-info {
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 1;
        }

        .expansion-icon {
            font-size: 32px;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
        }

        .expansion-meta h4 {
            font-size: 15px;
            font-weight: 800;
            margin-bottom: 2px;
        }

        .expansion-meta p {
            font-size: 12px;
            color: var(--text-sub);
            line-height: 1.3;
        }

        .expansion-badge {
            font-size: 11px;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 9999px;
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }

        /* Managers Screen */
        .managers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 12px;
        }

        .manager-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--panel-border);
            border-radius: 16px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            position: relative;
            overflow: hidden;
        }

        .manager-card.legendary {
            border-color: rgba(245, 158, 11, 0.5);
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(15, 23, 42, 0.95));
        }

        .manager-top {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .manager-avatar {
            font-size: 28px;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid var(--panel-border);
        }

        .manager-details h4 {
            font-size: 14px;
            font-weight: 800;
        }

        .manager-role {
            font-size: 11px;
            color: var(--text-sub);
        }

        .manager-stars {
            color: var(--gold);
            font-size: 12px;
            letter-spacing: 2px;
        }

        .manager-desc {
            font-size: 12px;
            color: var(--cyan);
            background: rgba(56, 189, 248, 0.08);
            padding: 6px 8px;
            border-radius: 8px;
            line-height: 1.3;
        }

        /* Orders Screen */
        .order-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--panel-border);
            border-radius: 16px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .order-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .order-title {
            font-size: 14px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .order-progress-track {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 9999px;
            height: 10px;
            overflow: hidden;
            position: relative;
        }

        .order-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981, #38bdf8);
            border-radius: 9999px;
            transition: width 0.3s ease;
        }

        .order-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
        }

        /* Factory Analytics Dashboard */
        .analytics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--panel-border);
            border-radius: 14px;
            padding: 12px;
            text-align: center;
        }

        .metric-val {
            font-size: 20px;
            font-weight: 900;
            color: var(--cyan);
            margin: 4px 0 2px;
        }

        .metric-label {
            font-size: 11px;
            color: var(--text-sub);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .bottleneck-box {
            padding: 14px;
            border-radius: 14px;
            border: 1px solid;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .bottleneck-box.optimal {
            background: rgba(16, 185, 129, 0.1);
            border-color: rgba(16, 185, 129, 0.4);
            color: #34d399;
        }

        .bottleneck-box.warning {
            background: rgba(239, 68, 68, 0.1);
            border-color: rgba(239, 68, 68, 0.4);
            color: #f87171;
        }

        /* Toast Notifications */
        #toast-container {
            position: absolute;
            bottom: 74px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 999;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            pointer-events: none;
        }

        .toast-msg {
            background: rgba(15, 23, 42, 0.94);
            border: 1px solid var(--panel-border);
            color: #ffffff;
            padding: 8px 16px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 700;
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            animation: fadeInOut 2.4s forwards ease;
        }

        @keyframes fadeInOut {
            0% { opacity: 0; transform: translateY(10px) scale(0.9); }
            10% { opacity: 1; transform: translateY(0) scale(1); }
            80% { opacity: 1; transform: translateY(0) scale(1); }
            100% { opacity: 0; transform: translateY(-10px) scale(0.95); }
        }

        /* Shop Multiplier selector */
        .shop-mult-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--panel-border);
        }

        .mult-tabs {
            display: flex;
            gap: 4px;
            background: rgba(255, 255, 255, 0.05);
            padding: 2px;
            border-radius: 8px;
        }

        .mult-tab {
            background: transparent;
            border: none;
            color: var(--text-sub);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
        }

        .mult-tab.active {
            background: var(--cyan);
            color: #0f172a;
        }

        .shop-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .shop-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--panel-border);
            border-radius: 14px;
            padding: 12px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        .shop-card-info {
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
        }

        .shop-card-icon {
            font-size: 24px;
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .shop-card-btn {
            background: linear-gradient(135deg, #10b981, #059669);
            border: none;
            color: #fff;
            padding: 8px 14px;
            border-radius: 10px;
            font-weight: 800;
            font-size: 13px;
            cursor: pointer;
            min-width: 90px;
            text-align: center;
        }

        .shop-card-btn:disabled {
            background: #334155;
            color: #64748b;
            cursor: not-allowed;
        }
'''
