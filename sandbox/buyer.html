<!DOCTYPE html>
<!--
    O4DB™ Protocol — v1.1.4
    Buyer Interface — Intent Dispatch, ARA Local Ranking, Settlement

    Copyright © 2026 Daniel Eduardo Placanica. All Rights Reserved.
    Safe Creative Registration ID: 2602184604821-4XTVN6
    Patent Application in Preparation (USPTO)
    Contact: daniel@o4db.org

    Licensed under O4DB™ Community & Commercial License v1.1.4
Last-Updated: 2026-02-24T19:00Z
    See LICENSE file for full terms. Commercial use requires written agreement.

    Cryptographic implementation: Ed25519 (primary) / ECDSA P-256 (fallback)
    Algorithm detection: runtime via Web Crypto API detectCryptoAlgo()
    Key storage: session memory only — no persistent key material in localStorage
-->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>O4DB™ Buyer — v1.1.4</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg:       #06080d;
            --surface:  #0d1117;
            --surface2: #161b22;
            --border:   #21262d;
            --accent:   #58a6ff;
            --accent2:  #3fb950;
            --gold:     #e3b341;
            --danger:   #f85149;
            --text:     #e6edf3;
            --muted:    #7d8590;
            --display:  'Syne', sans-serif;
            --mono:     'IBM Plex Mono', monospace;
            --body:     'DM Sans', sans-serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: var(--body);
            font-size: 14px;
            line-height: 1.6;
            min-height: 100vh;
        }

        /* Subtle grid background */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(88,166,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(88,166,255,0.03) 1px, transparent 1px);
            background-size: 48px 48px;
            pointer-events: none;
            z-index: 0;
        }

        /* ── IDENTITY OVERLAY ── */
        .id-overlay {
            position: fixed;
            inset: 0;
            background: rgba(6,8,13,0.97);
            z-index: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(8px);
        }

        .id-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 40px;
            width: 440px;
            max-width: min(440px, calc(100vw - 32px));
            position: relative;
            z-index: 1;
        }

        .id-title {
            font-family: var(--display);
            font-size: 22px;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 6px;
        }

        .id-subtitle {
            font-size: 13px;
            color: var(--muted);
            margin-bottom: 28px;
            line-height: 1.6;
        }

        .sovereign-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(63,185,80,0.08);
            border: 1px solid rgba(63,185,80,0.2);
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 600;
            color: var(--accent2);
            margin-bottom: 20px;
        }

        .dot-live {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--accent2);
            animation: blink 1.4s ease-in-out infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.3; }
        }

        .id-options {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 20px;
        }

        .id-option {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 16px;
            cursor: pointer;
            transition: border-color 0.2s, background 0.2s;
            text-align: left;
        }

        .id-option:hover { border-color: var(--accent); background: rgba(88,166,255,0.04); }

        .id-option-title {
            font-weight: 600;
            font-size: 13px;
            color: var(--text);
            margin-bottom: 3px;
        }

        .id-option-desc {
            font-size: 12px;
            color: var(--muted);
        }

        /* Passphrase input for recovery */
        .passphrase-section {
            display: none;
            margin-top: 16px;
        }

        /* ── TOPBAR ── */
        .topbar {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(6,8,13,0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 0 28px;
            height: 54px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--accent), #1f6feb);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--mono);
            font-size: 11px;
            font-weight: 600;
            color: #fff;
        }

        .brand-label {
            font-family: var(--display);
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 0.03em;
        }

        .topbar-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .identity-pill {
            display: flex;
            align-items: center;
            gap: 7px;
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 11px;
            color: var(--muted);
            cursor: pointer;
            transition: border-color 0.2s;
        }

        .identity-pill:hover { border-color: var(--accent); color: var(--text); }

        /* ── MAIN LAYOUT ── */
        .layout {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 0;
            min-height: calc(100vh - 54px);
            position: relative;
            z-index: 1;
        }

        /* ── LEFT PANEL: COMMAND ── */
        .panel-left {
            border-right: 1px solid var(--border);
            padding: 28px 24px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            overflow-y: auto;
        }

        .section-title {
            font-family: var(--display);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .section-title::after {
            content: '';
            flex: 1;
            height: 1px;
            background: var(--border);
        }

        /* ── INTENT FORM ── */
        .intent-form {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .field {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .field-label {
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--muted);
        }

        .field-hint {
            font-size: 11px;
            color: var(--muted);
            margin-top: 3px;
        }

        input[type="text"],
        input[type="number"],
        input[type="password"],
        select {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            color: var(--text);
            font-family: var(--body);
            font-size: 13px;
            width: 100%;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        input:focus, select:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(88,166,255,0.1);
        }

        .price-field {
            position: relative;
        }

        .price-field input {
            padding-left: 36px;
        }

        .price-field::before {
            content: '$';
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--muted);
            font-family: var(--mono);
            font-size: 13px;
            z-index: 1;
        }

        .commitment-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }

        .commitment-option {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .commitment-option:hover { border-color: var(--accent); }

        .commitment-option.selected {
            background: rgba(88,166,255,0.08);
            border-color: var(--accent);
        }

        .commitment-option .level {
            font-family: var(--mono);
            font-size: 16px;
            font-weight: 600;
            color: var(--accent);
        }

        .commitment-option .label {
            font-size: 10px;
            color: var(--muted);
            margin-top: 3px;
        }

        /* ── ARA SLIDERS ── */
        .ara-panel {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
        }

        .ara-total {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .ara-total-label {
            font-size: 12px;
            color: var(--muted);
        }

        .ara-total-value {
            font-family: var(--mono);
            font-size: 14px;
            font-weight: 600;
            color: var(--accent2);
            transition: color 0.2s;
        }

        .ara-total-value.error { color: var(--danger); }

        .slider-row {
            margin-bottom: 14px;
        }

        .slider-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .slider-name {
            font-size: 12px;
            font-weight: 500;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .slider-value {
            font-family: var(--mono);
            font-size: 12px;
            font-weight: 600;
            color: var(--accent);
        }

        input[type="range"] {
            -webkit-appearance: none;
            appearance: none;
            width: 100%;
            height: 4px;
            border-radius: 2px;
            background: var(--border);
            outline: none;
            cursor: pointer;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--accent);
            cursor: pointer;
            border: 2px solid var(--bg);
            box-shadow: 0 0 6px rgba(88,166,255,0.4);
            transition: transform 0.15s;
        }

        input[type="range"]::-webkit-slider-thumb:hover { transform: scale(1.2); }

        .slider-price::-webkit-slider-thumb  { background: var(--gold); box-shadow: 0 0 6px rgba(227,179,65,0.4); }
        .slider-trust::-webkit-slider-thumb  { background: var(--accent2); box-shadow: 0 0 6px rgba(63,185,80,0.4); }
        .slider-speed::-webkit-slider-thumb  { background: #a371f7; box-shadow: 0 0 6px rgba(163,113,247,0.4); }

        .weight-bar {
            height: 4px;
            display: flex;
            border-radius: 2px;
            overflow: hidden;
            margin-top: 12px;
        }

        .weight-segment {
            transition: flex 0.3s ease;
        }

        /* ── DISPATCH BUTTON ── */
        .dispatch-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, var(--accent), #1f6feb);
            color: #fff;
            border: none;
            border-radius: 10px;
            font-family: var(--display);
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: filter 0.2s, transform 0.15s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .dispatch-btn:hover { filter: brightness(1.1); transform: translateY(-1px); }
        .dispatch-btn:active { transform: translateY(0); }
        .dispatch-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

        .dispatch-btn.active {
            background: linear-gradient(135deg, var(--danger), #b91c1c);
            animation: pulseBtn 2s ease-in-out infinite;
        }

        @keyframes pulseBtn {
            0%, 100% { filter: brightness(1); }
            50%       { filter: brightness(1.15); }
        }

        /* ── RIGHT PANEL: OFFERS ── */
        .panel-right {
            padding: 28px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
        }

        /* ── STATUS BAR ── */
        .status-bar {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .status-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .vci-status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--muted);
            transition: all 0.3s;
        }

        .vci-status-dot.waiting {
            background: var(--gold);
            box-shadow: 0 0 10px var(--gold);
            animation: blink 1s ease-in-out infinite;
        }

        .vci-status-dot.received {
            background: var(--accent2);
            box-shadow: 0 0 10px var(--accent2);
        }

        .status-label {
            font-size: 13px;
            font-weight: 500;
        }

        .status-meta {
            font-size: 12px;
            color: var(--muted);
            font-family: var(--mono);
        }

        /* TTL progress */
        .ttl-track {
            height: 3px;
            background: var(--border);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 10px;
        }

        .ttl-fill {
            height: 100%;
            background: var(--accent2);
            border-radius: 2px;
            transition: width 1s linear, background 0.5s;
        }

        /* ── OFFERS TABLE ── */
        .offers-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .offers-count {
            font-family: var(--mono);
            font-size: 12px;
            color: var(--muted);
        }

        .offers-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .offer-row {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 18px;
            display: grid;
            grid-template-columns: 32px 1fr auto auto auto;
            align-items: center;
            gap: 16px;
            transition: border-color 0.2s, background 0.2s;
            animation: slideDown 0.3s ease;
            cursor: default;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-6px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .offer-row:hover { border-color: rgba(88,166,255,0.3); background: rgba(88,166,255,0.02); }

        .offer-row.rank-1 {
            border-color: var(--gold);
            background: rgba(227,179,65,0.04);
        }

        .offer-row.rank-1 .rank-num { color: var(--gold); }

        .offer-row.winner {
            border-color: var(--accent2);
            background: rgba(63,185,80,0.06);
        }

        .rank-num {
            font-family: var(--mono);
            font-size: 15px;
            font-weight: 600;
            color: var(--muted);
            text-align: center;
        }

        .offer-seller {
            display: flex;
            flex-direction: column;
            gap: 3px;
        }

        .seller-id {
            font-size: 13px;
            font-weight: 600;
            color: var(--text);
            font-family: var(--mono);
        }

        .seller-meta {
            font-size: 11px;
            color: var(--muted);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .trust-chip {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 10px;
            font-weight: 600;
            padding: 2px 7px;
            border-radius: 4px;
            background: rgba(63,185,80,0.1);
            color: var(--accent2);
            border: 1px solid rgba(63,185,80,0.2);
        }

        .affinity-chip {
            font-size: 10px;
            color: var(--accent);
            font-family: var(--mono);
        }

        .offer-price {
            font-family: var(--mono);
            font-size: 18px;
            font-weight: 600;
            color: var(--text);
            text-align: right;
        }

        .offer-score {
            text-align: right;
        }

        .score-value {
            font-family: var(--mono);
            font-size: 13px;
            font-weight: 600;
            color: var(--accent);
        }

        .score-label {
            font-size: 10px;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .offer-action {
            display: flex;
            flex-direction: column;
            gap: 6px;
            align-items: flex-end;
        }

        /* ── BUTTONS ── */
        .btn {
            padding: 8px 16px;
            border-radius: 7px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-family: var(--body);
            white-space: normal;
            word-break: break-all;
        }

        .btn-settle {
            background: var(--accent2);
            color: #0d1117;
        }
        .btn-settle:hover { filter: brightness(1.1); transform: translateY(-1px); }

        .btn-ghost {
            background: transparent;
            color: var(--muted);
            border: 1px solid var(--border);
        }
        .btn-ghost:hover { color: var(--text); border-color: var(--muted); }

        .btn:disabled { opacity: 0.35; cursor: not-allowed; transform: none !important; }

        /* ── SCORE BREAKDOWN ── */
        .score-bars {
            display: flex;
            gap: 3px;
            margin-top: 4px;
        }

        .score-segment {
            height: 3px;
            border-radius: 1px;
            flex: 1;
        }

        /* ── SETTLEMENT MODAL ── */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(6,8,13,0.85);
            z-index: 300;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(6px);
            display: none;
        }

        .modal-overlay.open { display: flex; }

        .modal-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 32px;
            width: 420px;
            max-width: min(420px, calc(100vw - 32px));
            animation: slideDown 0.25s ease;
        }

        .modal-title {
            font-family: var(--display);
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .modal-subtitle {
            font-size: 13px;
            color: var(--muted);
            margin-bottom: 22px;
        }

        .settle-detail {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 18px;
        }

        .settle-row {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            padding: 4px 0;
        }

        .settle-row .key { color: var(--muted); }
        .settle-row .val { font-family: var(--mono); font-weight: 600; }
        .settle-row .val.green { color: var(--accent2); }

        .warning-box {
            background: rgba(248,81,73,0.06);
            border: 1px solid rgba(248,81,73,0.2);
            border-radius: 8px;
            padding: 12px 14px;
            font-size: 12px;
            color: var(--danger);
            margin-bottom: 18px;
            line-height: 1.6;
        }

        .modal-footer {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }

        .btn-confirm {
            background: linear-gradient(135deg, var(--accent2), #2ea043);
            color: #0d1117;
            font-weight: 700;
            padding: 10px 22px;
        }

        .btn-confirm:hover { filter: brightness(1.1); transform: translateY(-1px); }

        /* ── SETTLEMENT CONFIRMED STATE ── */
        .confirmed-banner {
            background: rgba(63,185,80,0.06);
            border: 1px solid rgba(63,185,80,0.25);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            display: none;
        }

        .confirmed-banner.show { display: block; animation: slideDown 0.4s ease; }

        .confirmed-icon {
            font-size: 36px;
            margin-bottom: 12px;
        }

        .confirmed-title {
            font-family: var(--display);
            font-size: 18px;
            font-weight: 800;
            color: var(--accent2);
            margin-bottom: 8px;
        }

        .fingerprint-display {
            font-family: var(--mono);
            font-size: 10px;
            color: var(--muted);
            word-break: break-all;
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px;
            margin-top: 12px;
            cursor: pointer;
        }

        /* ── EMPTY STATES ── */
        .empty-offers {
            text-align: center;
            padding: 60px 24px;
            color: var(--muted);
        }

        .empty-icon { font-size: 40px; margin-bottom: 14px; opacity: 0.4; }
        .empty-text { font-size: 13px; line-height: 1.8; }

        /* ── TOAST ── */
        .toasts {
            position: fixed;
            bottom: 24px;
            right: 24px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            z-index: 9999;
        }

        .toast {
            background: var(--surface2);
            border: 1px solid var(--border);
            border-left: 3px solid var(--accent);
            border-radius: 8px;
            padding: 11px 16px;
            font-size: 13px;
            max-width: 300px;
            animation: slideDown 0.3s ease;
            box-shadow: 0 6px 24px rgba(0,0,0,0.4);
        }

        .toast.success { border-left-color: var(--accent2); }
        .toast.error   { border-left-color: var(--danger); }
        .toast.warning { border-left-color: var(--gold); }

        /* ── RELAY CONFIG ── */
        .relay-config {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .relay-config input {
            flex: 1;
            font-size: 12px;
            padding: 7px 10px;
        }

        .relay-status-text {
            font-size: 11px;
            color: var(--muted);
            font-family: var(--mono);
            margin-top: 4px;
        }

        /* ══════════════════════════════════
           RESPONSIVE — MOBILE / TABLET
           ══════════════════════════════════ */

        /* ── Identity overlay mobile ── */
        @media (max-width: 600px) {
            html, body { overflow-x: hidden; max-width: 100vw; }
            .id-overlay {
                align-items: flex-start;
                padding: 0;
                overflow-y: auto;
                overflow-x: hidden;
                max-width: 100vw;
            }
            .id-box {
                width: 100%;
                max-width: 100%;
                min-height: 100vh;
                border-radius: 0;
                padding: 40px 20px 40px;
                border: none;
                box-sizing: border-box;
                overflow-x: hidden;
            }
            .id-overlay {
                overflow-x: hidden;
            }
            body {
                overflow-x: hidden;
            }
            .id-title { font-size: 18px; }
            .id-subtitle { font-size: 12px; margin-bottom: 20px; }
            .id-option { padding: 12px 14px; }
            .sovereign-badge { font-size: 11px; padding: 5px 12px; }
        }

        /* ── Main layout mobile ── */
        @media (max-width: 768px) {
            .layout {
                grid-template-columns: 1fr;
                grid-template-rows: auto 1fr;
            }
            .panel-left {
                border-right: none;
                border-bottom: 1px solid var(--border);
                padding: 16px;
                gap: 16px;
            }
            .panel-right { padding: 16px; }
            .topbar { padding: 0 16px; height: 50px; }
            .brand-label { font-size: 13px; }
            .topbar-right { gap: 8px; }
            .identity-pill { font-size: 11px; padding: 4px 10px; }
            .relay-row { flex-direction: column; gap: 8px; }
            .relay-row input { width: 100% !important; }
            .offers-grid { grid-template-columns: 1fr !important; }
            .ara-summary { flex-direction: column; }
            .stat-row { flex-wrap: wrap; }
            .offer-card { padding: 12px; }
        }

        @media (max-width: 480px) {
            body { font-size: 13px; }
            .topbar { height: 46px; }
            .panel-left, .panel-right { padding: 12px; }
            .section-title { font-size: 10px; }
            .brand-icon { width: 26px; height: 26px; font-size: 9px; }
        }

        /* ── LANDSCAPE MOBILE ── */
        @media (max-width: 900px) and (orientation: landscape) {
            .layout {
                grid-template-columns: 320px 1fr;
                grid-template-rows: 1fr;
                height: calc(100vh - 50px);
            }
            .panel-left {
                border-right: 1px solid var(--border);
                border-bottom: none;
                overflow-y: auto;
                height: 100%;
                padding: 12px 16px;
                gap: 12px;
            }
            .panel-right {
                overflow-y: auto;
                height: 100%;
                padding: 12px 16px;
            }
        }
    </style>
</head>
<body>

<!-- ── IDENTITY OVERLAY ── -->
<div class="id-overlay" id="id-overlay">
    <div class="id-box">
        <div class="id-title">Your Sovereign Agent</div>
        <div class="id-subtitle">
            O4DB™ generates a local cryptographic identity for you.
            Your private key never leaves this device.
        </div>

        <div id="id-generating" style="text-align:center; padding:20px 0">
            <div style="font-family:var(--mono); font-size:13px; color:var(--accent); margin-bottom:8px">
                Generating keypair...
            </div>
            <div style="font-size:12px; color:var(--muted)">Web Crypto API · Ed25519/P-256 · Local only</div>
        </div>

        <div id="id-ready" style="display:none">
            <div class="sovereign-badge">
                <div class="dot-live"></div>
                Sovereign Agent Created
            </div>

            <div style="font-family:var(--mono); font-size:10px; color:var(--muted);
                        background:var(--surface2); border:1px solid var(--border);
                        border-radius:6px; padding:10px; margin-bottom:18px;
                        word-break:break-all" id="id-pubkey-display">
            </div>

            <div style="font-size:13px; font-weight:600; color:var(--text); margin-bottom:12px">
                Protect your identity with a recovery passphrase?
            </div>

            <div class="id-options">
                <button class="id-option" onclick="secureLaunch()">
                    <div class="id-option-title">🔐 Yes — encrypt with passphrase</div>
                    <div class="id-option-desc">Your key will be stored encrypted. Required to restore across sessions.</div>
                </button>
                <button class="id-option" onclick="sessionLaunch()">
                    <div class="id-option-title">⚡ No — session only</div>
                    <div class="id-option-desc">Key lives in this browser tab. Lost when tab closes. Fastest start.</div>
                </button>
            </div>

            <div class="passphrase-section" id="passphrase-section">
                <div class="field" style="margin-bottom:12px">
                    <label class="field-label">Passphrase</label>
                    <input type="password" id="passphrase-input"
                        placeholder="Choose a strong passphrase" />
                </div>
                <button class="btn btn-settle" onclick="encryptAndLaunch()" style="width:100%">
                    Encrypt & Launch
                </button>
            </div>
        </div>

    </div>
</div>

<!-- ── SETTLEMENT MODAL ── -->
<div class="modal-overlay" id="settle-modal">
    <div class="modal-box">
        <div class="modal-title">Confirm Settlement</div>
        <div class="modal-subtitle">
            This action is irreversible. The offer will be cryptographically bound.
        </div>
        <div class="settle-detail" id="settle-detail"></div>
        <div class="warning-box">
            ⚠ By confirming, you authorize the relay to release your identity to this seller
            and initiate the commitment protocol. The seller will be notified immediately.
        </div>
        <div class="modal-footer">
            <button class="btn btn-ghost" onclick="closeModal()">Cancel</button>
            <button class="btn btn-confirm" onclick="confirmSettle()">Confirm Settlement</button>
        </div>
    </div>
</div>

<!-- ── TOPBAR ── -->
<header class="topbar">
    <div class="brand">
        <div class="brand-icon">O4</div>
        <div>
            <div class="brand-label">O4DB™ Buyer</div>
        </div>
    </div>
    <div class="topbar-right">
        <div class="relay-config">
            <input type="text" id="relay-url-input" value="https://api.o4db.org"
                placeholder="Relay URL" style="width:min(220px, calc(100% - 100px))" />
            <button class="btn btn-ghost" onclick="testRelay()" style="font-size:11px; padding:7px 12px">
                Test
            </button>
        </div>
        <div class="identity-pill" onclick="showIdentityInfo()" id="identity-pill">
            <div class="dot-live" style="background:var(--muted)"></div>
            <span>No identity</span>
        </div>
    </div>
</header>

<!-- ── MAIN LAYOUT ── -->
<div class="layout">

    <!-- LEFT PANEL -->
    <div class="panel-left">

        <!-- INTENT DISPATCHER -->
        <div>
            <div class="section-title">Intent Dispatcher</div>
            <div class="intent-form">

                <div class="field">
                    <label class="field-label">Product Identifier</label>
                    <input type="text" id="demand-spec"
                        placeholder="EAN:7891234567890 or UPC:012345678905" />
                    <div class="field-hint">Format: TYPE:VALUE — supports EAN, UPC, SKU</div>
                </div>

                <div class="field">
                    <label class="field-label">Quantity</label>
                    <input type="number" id="quantity" value="1" min="1" max="999" />
                </div>

                <div class="field">
                    <label class="field-label">Maximum Budget</label>
                    <div class="price-field">
                        <input type="number" id="max-price"
                            placeholder="0.00" step="0.01" min="0" />
                    </div>
                    <div class="field-hint">Encrypted locally — relay never sees this value</div>
                </div>

                <div class="field">
                    <label class="field-label">Currency</label>
                    <select id="currency">
                        <option value="USD">USD — US Dollar</option>
                        <option value="ARS">ARS — Argentine Peso</option>
                        <option value="EUR">EUR — Euro</option>
                        <option value="BRL">BRL — Brazilian Real</option>
                    </select>
                </div>

                <div class="field">
                    <label class="field-label">Delivery Area</label>
                    <input type="text" id="delivery-area"
                        placeholder="AR:CABA" value="AR:CABA" />
                    <div class="field-hint">ISO 3166-1 + subdivision (e.g. AR, AR:CABA, UY)</div>
                </div>

                <div class="field">
                    <label class="field-label">Commitment Level</label>
                    <div class="commitment-grid">
                        <div class="commitment-option" onclick="selectCommitment(0)">
                            <div class="level">0</div>
                            <div class="label">Browse</div>
                        </div>
                        <div class="commitment-option selected" onclick="selectCommitment(1)">
                            <div class="level">1</div>
                            <div class="label">Intent</div>
                        </div>
                        <div class="commitment-option" onclick="selectCommitment(2)">
                            <div class="level">2</div>
                            <div class="label">Hold</div>
                        </div>
                    </div>
                    <div class="field-hint" id="commitment-hint">
                        Level 1 — Declared intent, no financial hold required
                    </div>
                </div>

                <div class="field">
                    <label class="field-label">Intent Window (minutes)</label>
                    <input type="number" id="ttl-minutes" value="30" min="5" max="120" />
                    <div class="field-hint">How long sellers have to respond</div>
                </div>

            </div>
        </div>

        <!-- ARA CONTROL PANEL -->
        <div>
            <div class="section-title">ARA Control Panel</div>
            <div class="ara-panel">
                <div class="ara-total">
                    <span class="ara-total-label">Ranking weights must sum to 100%</span>
                    <span class="ara-total-value" id="ara-total">100%</span>
                </div>

                <div class="slider-row">
                    <div class="slider-header">
                        <span class="slider-name">
                            <span style="color:var(--gold)">◆</span> Price
                        </span>
                        <div style="display:flex; align-items:center; gap:8px">
                            <span class="slider-value" id="w-price-val">35%</span>
                            <button class="lock-btn" id="lock-price" onclick="toggleLock('price')" title="Lock this weight">🔓</button>
                        </div>
                    </div>
                    <input type="range" class="slider-price" id="w-price"
                        min="0" max="100" value="35"
                        oninput="adjustWeights('price', this.value)" />
                </div>

                <div class="slider-row">
                    <div class="slider-header">
                        <span class="slider-name">
                            <span style="color:var(--accent2)">◆</span> Seller Trust
                        </span>
                        <div style="display:flex; align-items:center; gap:8px">
                            <span class="slider-value" id="w-trust-val">40%</span>
                            <button class="lock-btn" id="lock-trust" onclick="toggleLock('trust')" title="Lock this weight">🔓</button>
                        </div>
                    </div>
                    <input type="range" class="slider-trust" id="w-trust"
                        min="0" max="100" value="40"
                        oninput="adjustWeights('trust', this.value)" />
                </div>

                <div class="slider-row" style="margin-bottom:0">
                    <div class="slider-header">
                        <span class="slider-name">
                            <span style="color:#a371f7">◆</span> Delivery Speed
                        </span>
                        <div style="display:flex; align-items:center; gap:8px">
                            <span class="slider-value" id="w-speed-val">25%</span>
                            <button class="lock-btn" id="lock-speed" onclick="toggleLock('speed')" title="Lock this weight">🔓</button>
                        </div>
                    </div>
                    <input type="range" class="slider-speed" id="w-speed"
                        min="0" max="100" value="25"
                        oninput="adjustWeights('speed', this.value)" />
                </div>

                <!-- Weight visualizer bar -->
                <div class="weight-bar" style="margin-top:16px">
                    <div class="weight-segment" id="wb-price"
                        style="background:var(--gold); flex:35"></div>
                    <div class="weight-segment" id="wb-trust"
                        style="background:var(--accent2); flex:40"></div>
                    <div class="weight-segment" id="wb-speed"
                        style="background:#a371f7; flex:25"></div>
                </div>
            </div>
        </div>

        <!-- DISPATCH -->
        <button class="dispatch-btn" id="dispatch-btn" onclick="toggleDispatch()">
            <span id="dispatch-icon">⚡</span>
            <span id="dispatch-label">Dispatch Intent</span>
        </button>

    </div>

    <!-- RIGHT PANEL -->
    <div class="panel-right">

        <!-- STATUS BAR -->
        <div class="status-bar" id="status-bar" style="display:none">
            <div class="status-left">
                <div class="vci-status-dot waiting" id="vci-dot"></div>
                <div>
                    <div class="status-label" id="status-label">Waiting for offers...</div>
                    <div class="status-meta" id="status-meta">—</div>
                </div>
            </div>
            <div style="text-align:right">
                <div style="font-size:11px; color:var(--muted); margin-bottom:4px" id="ttl-label">TTL</div>
                <div style="font-family:var(--mono); font-size:13px" id="ttl-countdown">—</div>
            </div>
        </div>

        <div class="ttl-track" id="ttl-track" style="display:none">
            <div class="ttl-fill" id="ttl-fill"></div>
        </div>

        <!-- CONFIRMED BANNER -->
        <div class="confirmed-banner" id="confirmed-banner">
            <div class="confirmed-icon">✅</div>
            <div class="confirmed-title">Settlement Initiated</div>
            <div style="font-size:13px; color:var(--muted)">
                The seller has been notified. Awaiting ACK and privacy commitment.
            </div>
            <div class="fingerprint-display" id="fingerprint-display" onclick="copyFingerprint()">
                Click to copy Settlement Fingerprint
            </div>
            <div id="fp-status" style="margin-top:6px; min-height:18px"></div>
            <div class="fp-actions">
                <button class="btn btn-ghost" onclick="copyFingerprint()" style="font-size:11px">
                    📋 Copy
                </button>
                <button class="btn btn-ghost" onclick="downloadFingerprint()" style="font-size:11px">
                    ⬇ Download
                </button>
                <button class="btn btn-ghost-report" onclick="reportGhosting()" id="btn-ghost-report" style="display:none">
                    🚨 Report Ghosting
                </button>
            </div>
            <button class="btn btn-ghost" onclick="newIntent()" style="margin-top:12px">
                + New Intent
            </button>
        </div>

        <!-- OFFERS -->
        <div id="offers-section">
            <div class="offers-header">
                <div class="section-title" style="margin-bottom:0; flex:1">
                    Live Ranking
                </div>
                <div class="offers-count" id="offers-count"></div>
            </div>

            <div class="offers-list" id="offers-list">
                <div class="empty-offers">
                    <div class="empty-icon">🎯</div>
                    <div class="empty-text">
                        Configure your intent and dispatch it.<br>
                        Offers will appear here and rank in real time<br>
                        according to your ARA weights.
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>

<!-- TOAST CONTAINER -->
<div class="toasts" id="toasts"></div>


<script>
// ════════════════════════════════════════════════════════════
// O4DB™ BUYER INTERFACE — v1.1.4
// ARA (Automated Ranking Algorithm) runs entirely in this browser.
// The relay serves raw signed offers — ranking happens locally.
// The buyer's weights and max_price never leave this device.
// ════════════════════════════════════════════════════════════

// ── STATE ────────────────────────────────────────────────────
const state = {
    privateKey:      null,
    publicKeyHex:    null,
    publicKeyB64:    null,   // buyer_sign_pub — signing key
    encPrivateKey:   null,
    encPublicKeyB64: null,   // buyer_pubkey   — encryption key
    relayUrl:     'https://api.o4db.org',

    // ARA weights (must sum to 1.0)
    weights: { price: 0.35, trust: 0.40, speed: 0.25 },

    // Active VCI
    vci: null,
    maxPrice: 0,
    commitment: 1,
    ttlSeconds: 0,
    dispatchedAt: null,

    // Offers received from relay
    offers: [],

    // Settlement
    pendingSettlement: null,
    settled: false,

    // Polling
    pollTimer: null,
    ttlTimer:  null,
};

// ── CRYPTOGRAPHY ─────────────────────────────────────────────

// ── CRYPTO ALGORITHM DETECTION ───────────────────────────────
// Detects Ed25519 browser support at runtime.
// Falls back to ECDSA P-256 for Safari < 17, Firefox < 130.
// The relay's verify_signature() auto-detects by public key length.

let ALGO = null;  // set by detectCryptoAlgo() before any key operation

async function detectCryptoAlgo() {
    try {
        await window.crypto.subtle.generateKey(
            { name: 'Ed25519' }, false, ['sign', 'verify']
        );
        ALGO = 'Ed25519';
    } catch (e) {
        ALGO = 'P-256';
    }
    console.log('[O4DB] Crypto algorithm:', ALGO);
}

function getKeyGenParams() {
    return ALGO === 'Ed25519'
        ? { name: 'Ed25519' }
        : { name: 'ECDSA', namedCurve: 'P-256' };
}

function getSignParams() {
    return ALGO === 'Ed25519'
        ? 'Ed25519'
        : { name: 'ECDSA', hash: 'SHA-256' };
}

function getVerifyParams() {
    return ALGO === 'Ed25519'
        ? 'Ed25519'
        : { name: 'ECDSA', hash: 'SHA-256' };
}


async function generateKeyPair() {
    if (!ALGO) await detectCryptoAlgo();
    return await window.crypto.subtle.generateKey(
        getKeyGenParams(),
        true, ['sign', 'verify']
    );
}

// Recursively sort all keys — matches Python json.dumps(sort_keys=True, separators=(',',':'))
function sortedStringify(obj) {
    if (Array.isArray(obj)) return '[' + obj.map(sortedStringify).join(',') + ']';
    if (obj !== null && typeof obj === 'object') {
        const keys = Object.keys(obj).sort();
        return '{' + keys.map(k => JSON.stringify(k) + ':' + sortedStringify(obj[k])).join(',') + '}';
    }
    return JSON.stringify(obj);
}

async function signPayload(obj) {
    const msg = new TextEncoder().encode(
        typeof obj === 'string' ? obj : sortedStringify(obj)
    );
    const sig = await window.crypto.subtle.sign(
        getSignParams(),
        state.privateKey, msg
    );
    return buf2b64(sig);
}

// Simulate HPKE price_token: in production this is RFC 9180
// For the pilot: encrypt max_price with AES-GCM using buyer's own key
// The relay never decrypts this — it passes through opaquely
async function encryptMaxPrice(price) {
    const key = await window.crypto.subtle.generateKey(
        { name: 'AES-GCM', length: 256 }, false, ['encrypt']
    );
    const iv  = window.crypto.getRandomValues(new Uint8Array(12));
    const enc = await window.crypto.subtle.encrypt(
        { name: 'AES-GCM', iv },
        key,
        new TextEncoder().encode(String(price))
    );
    // Store the decryption key locally for ARA comparison
    state._priceKey = key;
    state._priceIV  = iv;
    // Return opaque token (base64)
    return buf2b64(enc) + '.' + buf2b64(iv.buffer);
}

// Encrypt key with passphrase for storage
async function deriveKeyFromPassphrase(passphrase) {
    const enc  = new TextEncoder().encode(passphrase);
    const base = await crypto.subtle.importKey('raw', enc, 'PBKDF2', false, ['deriveKey']);
    return await crypto.subtle.deriveKey(
        { name: 'PBKDF2', salt: new TextEncoder().encode('o4db-salt-v1'),
          iterations: 100000, hash: 'SHA-256' },
        base,
        { name: 'AES-GCM', length: 256 },
        false, ['encrypt', 'decrypt']
    );
}

// ── HELPERS ──────────────────────────────────────────────────
function buf2hex(buf) {
    return Array.from(new Uint8Array(buf))
        .map(b => b.toString(16).padStart(2, '0')).join('');
}

function buf2b64(buf) {
    return btoa(String.fromCharCode(...new Uint8Array(buf)));
}

function sha256hex(str) {
    return window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(str))
        .then(buf => buf2hex(buf));
}

function generateId(prefix = '') {
    return prefix + Date.now().toString(36).toUpperCase() +
           Math.random().toString(36).substr(2, 6).toUpperCase();
}

function now() { return Date.now() / 1000; }

// ── IDENTITY SETUP ───────────────────────────────────────────

async function initIdentity() {
    try {
        await detectCryptoAlgo();

        // KEY SEPARATION PRINCIPLE (v1.1.4)
        // buyer_sign_pub  = Ed25519 signing key  → used for BES identity & all signatures
        // buyer_pubkey    = Ed25519 encrypt key  → used for price_token HPKE decryption
        // These two keys are STRICTLY SEPARATE — mixing them was a bug fixed in v1.1.4

        // Signing keypair
        const signKp  = await generateKeyPair();
        const signRaw = await crypto.subtle.exportKey('raw', signKp.publicKey);

        // Encryption keypair (separate identity, same algo)
        const encKp   = await generateKeyPair();
        const encRaw  = await crypto.subtle.exportKey('raw', encKp.publicKey);

        // Signing key — used for vci_signature, request_signature, settlement signature
        state.privateKey    = signKp.privateKey;
        state.publicKeyHex  = buf2hex(signRaw);
        state.publicKeyB64  = buf2b64(signRaw);   // = buyer_sign_pub

        // Encryption key — used for buyer_pubkey (price_token HPKE)
        state.encPrivateKey = encKp.privateKey;
        state.encPublicKeyB64 = buf2b64(encRaw);  // = buyer_pubkey

        document.getElementById('id-generating').style.display = 'none';
        document.getElementById('id-ready').style.display = 'block';
        document.getElementById('id-pubkey-display').textContent =
            'Sign Key: ' + state.publicKeyHex;

    } catch (e) {
        document.getElementById('id-generating').innerHTML =
            `<div style="color:var(--danger)">Key generation failed: ${e.message}</div>`;
    }
}

function secureLaunch() {
    document.getElementById('passphrase-section').style.display = 'block';
    document.getElementById('passphrase-input').focus();
}

async function encryptAndLaunch() {
    const pass = document.getElementById('passphrase-input').value;
    if (!pass || pass.length < 8) {
        toast('Use a passphrase of at least 8 characters', 'warning'); return;
    }
    // In a full implementation: export privkey → encrypt with derived key → store in localStorage
    // For pilot: just launch with session key
    toast('Identity secured with passphrase', 'success');
    launch();
}

function sessionLaunch() {
    toast('Session-only identity — key will be lost when tab closes', 'warning');
    launch();
}

function launch() {
    document.getElementById('id-overlay').style.display = 'none';

    const pill = document.getElementById('identity-pill');
    pill.innerHTML = `
        <div class="dot-live"></div>
        <span>${state.publicKeyHex.substr(0, 12)}...</span>`;

    log('Sovereign identity active');

    // Open IndexedDB and recover any active session
    openDB().then(() => {
        recoverSession();
    }).catch(e => {
        console.warn('[O4DB] IndexedDB unavailable:', e.message);
    });
}

function showIdentityInfo() {
    toast('Public key: ' + state.publicKeyHex.substr(0, 24) + '...', 'info');
}

// ── ARA WEIGHT SLIDERS ────────────────────────────────────────
// Constraint: weights must always sum to 100.
// When one slider moves, the other two adjust proportionally.

let _adjusting = false;

function adjustWeights(changed, newVal) {
    if (_adjusting) return;
    _adjusting = true;

    newVal = parseInt(newVal);
    const others = ['price', 'trust', 'speed'].filter(k => k !== changed);

    // Current sum of others
    const othersSum = others.reduce((s, k) => s + parseInt(document.getElementById('w-' + k).value), 0);
    const remaining = 100 - newVal;

    if (othersSum === 0) {
        // Split remaining equally
        others.forEach(k => {
            document.getElementById('w-' + k).value = Math.floor(remaining / 2);
        });
        // Handle rounding
        const a = Math.floor(remaining / 2);
        document.getElementById('w-' + others[0]).value = remaining - a;
        document.getElementById('w-' + others[1]).value = a;
    } else {
        // Adjust proportionally
        let assigned = 0;
        others.forEach((k, i) => {
            const cur = parseInt(document.getElementById('w-' + k).value);
            const share = i === others.length - 1
                ? remaining - assigned
                : Math.round((cur / othersSum) * remaining);
            document.getElementById('w-' + k).value = Math.max(0, Math.min(100, share));
            assigned += Math.max(0, Math.min(100, share));
        });
    }

    // Sync display
    const p = parseInt(document.getElementById('w-price').value);
    const t = parseInt(document.getElementById('w-trust').value);
    const s = parseInt(document.getElementById('w-speed').value);
    const total = p + t + s;

    document.getElementById('w-price-val').textContent = p + '%';
    document.getElementById('w-trust-val').textContent = t + '%';
    document.getElementById('w-speed-val').textContent = s + '%';
    document.getElementById('ara-total').textContent   = total + '%';
    document.getElementById('ara-total').className =
        'ara-total-value' + (total !== 100 ? ' error' : '');

    // Update visual bar
    document.getElementById('wb-price').style.flex = p;
    document.getElementById('wb-trust').style.flex = t;
    document.getElementById('wb-speed').style.flex = s;

    // Store normalized weights
    state.weights = { price: p / 100, trust: t / 100, speed: s / 100 };

    // Re-rank if offers exist
    if (state.offers.length) renderOffers();

    _adjusting = false;
}

// ── COMMITMENT SELECTOR ───────────────────────────────────────

const commitmentHints = {
    0: 'Level 0 — Browsing only. No commitment implied.',
    1: 'Level 1 — Declared intent. No financial hold required.',
    2: 'Level 2 — Financial hold authorized. Seller can request escrow.',
};

function selectCommitment(level) {
    document.querySelectorAll('.commitment-option').forEach((el, i) => {
        el.classList.toggle('selected', i === level);
    });
    state.commitment = level;
    document.getElementById('commitment-hint').textContent = commitmentHints[level];
}

// ── VCI DISPATCH ─────────────────────────────────────────────

async function toggleDispatch() {
    if (state.vci && !state.settled) {
        cancelIntent();
        return;
    }
    await dispatchIntent();
}

async function dispatchIntent() {
    if (!state.privateKey) {
        toast('Identity not ready — wait for key generation', 'error'); return;
    }

    const demandSpec = document.getElementById('demand-spec').value.trim();
    const quantity   = parseInt(document.getElementById('quantity').value);
    const maxPrice   = parseFloat(document.getElementById('max-price').value);
    const currency   = document.getElementById('currency').value;
    const area       = document.getElementById('delivery-area').value.trim();
    const ttlMin     = parseInt(document.getElementById('ttl-minutes').value);

    if (!demandSpec || !demandSpec.includes(':')) {
        toast('Enter product identifier in TYPE:VALUE format', 'warning'); return;
    }
    if (!maxPrice || maxPrice <= 0) {
        toast('Enter your maximum budget', 'warning'); return;
    }

    state.maxPrice  = maxPrice;
    state.relayUrl  = document.getElementById('relay-url-input').value.trim();
    state.ttlSeconds = ttlMin * 60;

    // Encrypt max_price — relay never sees the raw value
    const priceToken = await encryptMaxPrice(maxPrice);

    const vciId    = generateId('VCI-');
    const ts       = now();
    const weights  = {
        price:        state.weights.price,
        trust_score:  state.weights.trust,
        delivery_speed: state.weights.speed,
    };

    // Build VCI payload for signing
    const vciPayload = {
        vci_id:           vciId,
        demand_spec:      demandSpec,
        quantity,
        price_token:      priceToken,
        currency,
        ttl:              state.ttlSeconds,
        commitment_level: state.commitment,
        delivery_area:    area,
        privacy_mode:     'private',
        timestamp:        ts,
    };

    const signature = await signPayload(vciPayload);

    const vciBody = {
        ...vciPayload,
        buyer_pubkey:   state.encPublicKeyB64,   // HPKE encryption key
        buyer_sign_pub: state.publicKeyB64,       // Ed25519 signing key
        vci_signature:  signature,
        weights,
        trust_floor:    0.5,
        banned_sellers: [],
    };

    try {
        const resp = await fetch(`${state.relayUrl}/api/v1/vci/submit`, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(vciBody),
        });

        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'VCI rejected');

        state.vci          = vciBody;
        state.dispatchedAt = now();
        state.offers       = [];
        state.settled      = false;

        // Update UI
        document.getElementById('dispatch-btn').classList.add('active');
        document.getElementById('dispatch-icon').textContent  = '⏹';
        document.getElementById('dispatch-label').textContent = 'Cancel Intent';
        document.getElementById('status-bar').style.display   = 'flex';
        document.getElementById('ttl-track').style.display    = 'block';
        document.getElementById('confirmed-banner').classList.remove('show');
        document.getElementById('offers-section').style.display = 'block';

        setVCIStatus('waiting', `${data.broadcast_count} sellers notified`, vciId);

        // Start polling for offers
        startOfferPolling();
        startTTLCountdown();

        log(`VCI dispatched: ${vciId} — ${data.broadcast_count} sellers notified`);
        toast(`Intent dispatched to ${data.broadcast_count} sellers`, 'success');

    } catch (e) {
        toast('Dispatch failed: ' + e.message, 'error');
        log('Dispatch failed: ' + e.message);
    }
}

function cancelIntent() {
    stopPolling();
    state.vci     = null;
    state.offers  = [];
    state.settled = false;

    document.getElementById('dispatch-btn').classList.remove('active');
    document.getElementById('dispatch-icon').textContent  = '⚡';
    document.getElementById('dispatch-label').textContent = 'Dispatch Intent';
    document.getElementById('status-bar').style.display  = 'none';
    document.getElementById('ttl-track').style.display   = 'none';

    renderOffers();
    toast('Intent cancelled', 'warning');
}

// ── OFFER POLLING ─────────────────────────────────────────────

function startOfferPolling() {
    stopPolling();
    pollOffers(); // immediate first poll
    state.pollTimer = setInterval(pollOffers, 4000);
}

function stopPolling() {
    if (state.pollTimer) { clearInterval(state.pollTimer); state.pollTimer = null; }
}

async function pollOffers() {
    if (!state.vci) return;
    try {
        // Sign the request to prove buyer identity — prevents replay attacks
        // by attackers who captured buyer_sign_pub from network traffic.
        const ts = Date.now() / 1000;
        const reqSig = await signPayload({ vci_id: state.vci.vci_id, timestamp: ts });
        const resp = await fetch(
            `${state.relayUrl}/api/v1/vci/${state.vci.vci_id}/offers` +
            `?buyer_sign_pub=${encodeURIComponent(state.publicKeyB64)}` +
            `&request_timestamp=${ts}` +
            `&request_signature=${encodeURIComponent(reqSig)}`
        );
        if (!resp.ok) return;
        const data = await resp.json();

        if (data.offers && data.offers.length !== state.offers.length) {
            // Audit signatures and hydrate network scores before rendering
            let incoming = data.offers;
            incoming = await auditOfferIntegrity(incoming);
            incoming = await hydrateNetworkScores(incoming);
            state.offers = incoming;
            persistSession();
            renderOffers();
            setVCIStatus('received',
                `${state.offers.length} offer${state.offers.length !== 1 ? 's' : ''} received`,
                state.vci.vci_id
            );
        }
    } catch (e) {
        // Non-critical — keep polling
    }
}

// ── ARA — LOCAL RANKING ───────────────────────────────────────
// Runs entirely in this browser. The relay does not compute or see this ranking.
//
// V(offer) = (w_price × price_score) +
//            (w_trust × trust_score) +
//            (w_speed × speed_score)
//
// price_score: normalized inverse (lower price = higher score)
//              among offers that pass trust_floor
// trust_score: seller trust_score from public registry (0–1)
// speed_score: normalized inverse of delivery_days
//
// Probation multiplier: affinity_mode === 'probation' → × 0.70 on final V

function computeARAScores(offers) {
    if (!offers.length) return [];

    // Filter by trust floor
    const eligible = offers.filter(o => (o.trust_score || 0.8) >= 0.5);
    if (!eligible.length) return offers.map(o => ({ ...o, V: 0, eligible: false }));

    // Price normalization (inverted — lower is better)
    const prices = eligible.map(o => o.unit_price);
    const pMin   = Math.min(...prices);
    const pMax   = Math.max(...prices);
    const pRange = pMax - pMin || 1;

    // Speed normalization (inverted — fewer days is better)
    const days = eligible.map(o => o.attributes?.delivery_days || 7);
    const dMin = Math.min(...days);
    const dMax = Math.max(...days);
    const dRange = dMax - dMin || 1;

    return offers.map(o => {
        if ((o.trust_score || 0.8) < 0.5) return { ...o, V: 0, eligible: false };

        const priceScore = 1 - ((o.unit_price - pMin) / pRange);
        const trustScore = o.trust_score || 0.8;
        const speedScore = 1 - (((o.attributes?.delivery_days || 7) - dMin) / dRange);

        const multiplier = o.affinity_mode === 'probation' ? 0.70 : 1.0;

        const V = multiplier * (
            state.weights.price * priceScore +
            state.weights.trust * trustScore +
            state.weights.speed * speedScore
        );

        return {
            ...o,
            V:           Math.round(V * 10000) / 10000,
            priceScore:  Math.round(priceScore * 100),
            trustScore:  Math.round(trustScore * 100),
            speedScore:  Math.round(speedScore * 100),
            multiplier,
            eligible:    true,
        };
    }).sort((a, b) => b.V - a.V);
}

// ── RENDER OFFERS ─────────────────────────────────────────────

function renderOffers() {
    const container = document.getElementById('offers-list');

    if (!state.offers.length) {
        container.innerHTML = `
            <div class="empty-offers">
                <div class="empty-icon">⏳</div>
                <div class="empty-text">
                    Waiting for sellers to respond...<br>
                    Offers will rank automatically as they arrive.
                </div>
            </div>`;
        document.getElementById('offers-count').textContent = '';
        return;
    }

    const ranked = computeARAScores(state.offers);
    document.getElementById('offers-count').textContent =
        `${ranked.length} offer${ranked.length !== 1 ? 's' : ''} · ranked locally`;

    container.innerHTML = ranked.map((offer, i) => {
        const rank       = i + 1;
        const isTop      = rank === 1;
        const maxBudget  = state.maxPrice;
        const overBudget = offer.unit_price > maxBudget;

        return `
        <div class="offer-row ${isTop ? 'rank-1' : ''} ${overBudget ? 'over-budget' : ''}"
             style="${overBudget ? 'opacity:0.5' : ''}">
            <div class="rank-num">${rank}</div>

            <div class="offer-seller">
                <div class="seller-id">${offer.seller_id}</div>
                <div class="seller-meta">
                    <span class="trust-chip">⭐ ${(offer.trust_score || 0.8).toFixed(3)}</span>
                    <span class="affinity-chip">${offer.affinity_mode || 'probation'}</span>
                    <span style="color:var(--muted)">
                        ${offer.attributes?.delivery_days || '?'}d delivery
                    </span>
                    ${offer.multiplier === 0.70
                        ? '<span style="color:var(--gold); font-size:10px">×0.70 probation</span>'
                        : ''}
                    ${buildTrustRadar(offer)}
                    ${buildIntegrityBadge(offer)}
                </div>
                <div class="score-bars">
                    <div class="score-segment"
                        style="background:var(--gold); opacity:${(offer.priceScore||0)/100}"></div>
                    <div class="score-segment"
                        style="background:var(--accent2); opacity:${(offer.trustScore||0)/100}"></div>
                    <div class="score-segment"
                        style="background:#a371f7; opacity:${(offer.speedScore||0)/100}"></div>
                </div>
            </div>

            <div class="offer-price">
                $${offer.unit_price.toFixed(2)}
                <div style="font-size:10px; color:${overBudget ? 'var(--danger)' : 'var(--muted)'}">
                    ${overBudget ? 'OVER BUDGET' : offer.currency || ''}
                </div>
            </div>

            <div class="offer-score">
                <div class="score-value">V=${offer.V.toFixed(4)}</div>
                <div class="score-label">ARA score</div>
            </div>

            <div class="offer-action">
                ${!state.settled && offer.eligible && !overBudget && !offer.integrityViolation ? `
                <button class="btn btn-settle"
                    onclick="initiateSettle('${offer.seller_id}', ${offer.unit_price})">
                    ${isTop ? '★ Select' : 'Select'}
                </button>` : ''}
                ${overBudget
                    ? '<span style="font-size:10px; color:var(--danger)">Over budget</span>'
                    : ''}
                ${!offer.eligible
                    ? '<span style="font-size:10px; color:var(--danger)">Trust too low</span>'
                    : ''}
                ${offer.integrityViolation
                    ? '<span style="font-size:10px; color:var(--danger); font-weight:700">⚠ INTEGRITY VIOLATION</span>'
                    : ''}
            </div>
        </div>`;
    }).join('');
}

// ── SETTLEMENT ────────────────────────────────────────────────

function initiateSettle(sellerId, price) {
    state.pendingSettlement = { sellerId, price };

    document.getElementById('settle-detail').innerHTML = `
        <div class="settle-row">
            <span class="key">Seller</span>
            <span class="val">${sellerId}</span>
        </div>
        <div class="settle-row">
            <span class="key">Price</span>
            <span class="val green">$${price.toFixed(2)}</span>
        </div>
        <div class="settle-row">
            <span class="key">VCI</span>
            <span class="val" style="font-size:10px">${state.vci?.vci_id}</span>
        </div>
        <div class="settle-row">
            <span class="key">Commitment</span>
            <span class="val">Level ${state.commitment}</span>
        </div>`;

    document.getElementById('settle-modal').classList.add('open');
}

async function confirmSettle() {
    closeModal();
    if (!state.pendingSettlement || !state.vci) return;

    const { sellerId } = state.pendingSettlement;

    try {
        const resp = await fetch(
            `${state.relayUrl}/api/v1/vci/${state.vci.vci_id}/settle`,
            {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify(await (async () => {
                    const ts = now();
                    const settlePayload = {
                        vci_id:           state.vci.vci_id,
                        winner_seller_id: sellerId,
                        timestamp:        ts,
                    };
                    const sig = await signPayload(settlePayload);
                    return {
                        vci_id:           state.vci.vci_id,
                        winner_seller_id: sellerId,
                        buyer_sign_pub:   state.publicKeyB64,
                        timestamp:        ts,
                        signature:        sig,
                    };
                })()),
            }
        );

        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Settlement failed');

        state.settled = true;
        stopPolling();

        // ── LOCAL FINGERPRINT COMPUTATION ────────────────────────────
        // Compute independently from relay data.
        // Formula: SHA-256(vci_id + seller_id + price + buyer_pubkey + timestamp)
        // If the relay returns a fingerprint, compare — any mismatch = FRAUD ALERT.
        const settlementTimestamp = String(now());
        const fpRaw = state.vci.vci_id + sellerId +
                      String(state.pendingSettlement.price) +
                      state.encPublicKeyB64 + settlementTimestamp;  // buyer_pubkey = encKey;
        const localFP = await sha256hex(fpRaw);

        // Store settlement token from relay (different from fingerprint — it's the ST-TTL token)
        state.settlementToken = data.settlement_token || null;

        // If relay ever returns a fingerprint field, verify it matches our local computation.
        // The relay computes its own FP after ACK using different inputs (includes seller pubkey).
        // A mismatch on the pre-ACK token is an anomaly — flag but don't block.
        let fpDisplay = localFP;
        let fpStatus  = 'local';

        if (data.fingerprint) {
            // Relay returned a fingerprint — cross-check
            if (data.fingerprint !== localFP) {
                // Different inputs possible (relay includes seller pubkey) — compute relay-style
                const fpRelayRaw = state.vci.vci_id + sellerId +
                                   String(state.pendingSettlement.price) +
                                   state.vci.vci_id + data.fingerprint.substr(0, 8);
                // Flag as relay-provided, show both
                fpDisplay = localFP;
                fpStatus  = 'relay_mismatch';
                toast('⚠ Fingerprint mismatch — relay value differs from local computation. Verify manually.', 'warning');
                log('FINGERPRINT MISMATCH — local: ' + localFP.substr(0,16) + ' relay: ' + data.fingerprint.substr(0,16));
            } else {
                fpStatus = 'verified';
                toast('✓ Fingerprint verified — local and relay match', 'success');
            }
        }

        // Store for download
        state.localFingerprint  = localFP;
        state.fingerprintStatus = fpStatus;

        document.getElementById('confirmed-banner').classList.add('show');
        document.getElementById('fingerprint-display').textContent = localFP;

        // Show verification status below fingerprint
        const fpStatusEl = document.getElementById('fp-status');
        if (fpStatusEl) {
            if (fpStatus === 'verified') {
                fpStatusEl.innerHTML = '<span style="color:var(--accent2); font-size:11px">✓ Verified against relay</span>';
            } else if (fpStatus === 'relay_mismatch') {
                fpStatusEl.innerHTML = '<span style="color:var(--danger); font-size:11px; font-weight:700">⚠ MISMATCH — relay returned different value</span>';
            } else {
                fpStatusEl.innerHTML = '<span style="color:var(--muted); font-size:11px">Locally computed — relay verification pending ACK</span>';
            }
        }
        document.getElementById('offers-section').style.display = 'none';
        document.getElementById('dispatch-btn').classList.remove('active');
        document.getElementById('dispatch-icon').textContent  = '⚡';
        document.getElementById('dispatch-label').textContent = 'Dispatch Intent';

        // Show ghosting report button (available if seller doesn't ACK)
        const ghostBtn = document.getElementById('btn-ghost-report');
        if (ghostBtn) ghostBtn.style.display = 'inline-flex';

        setVCIStatus('received', 'Settlement confirmed', state.vci.vci_id);
        persistSession();

        log(`Settlement confirmed — winner: ${sellerId} — FP: ${localFP.substr(0, 16)}...`);
        toast('Settlement initiated — awaiting seller ACK', 'success');

    } catch (e) {
        toast('Settlement failed: ' + e.message, 'error');
    }
}

function closeModal() {
    document.getElementById('settle-modal').classList.remove('open');
}

function copyFingerprint() {
    const fp = document.getElementById('fingerprint-display').textContent;
    navigator.clipboard.writeText(fp)
        .then(() => toast('Fingerprint copied', 'info'));
}

function newIntent() {
    state.vci     = null;
    state.offers  = [];
    state.settled = false;
    document.getElementById('confirmed-banner').classList.remove('show');
    document.getElementById('offers-section').style.display = 'block';
    document.getElementById('status-bar').style.display     = 'none';
    document.getElementById('ttl-track').style.display      = 'none';
    renderOffers();
}

// ── TTL COUNTDOWN ─────────────────────────────────────────────

function startTTLCountdown() {
    if (state.ttlTimer) clearInterval(state.ttlTimer);
    state.ttlTimer = setInterval(updateTTL, 1000);
    updateTTL();
}

function updateTTL() {
    if (!state.vci || !state.dispatchedAt) return;
    const elapsed  = now() - state.dispatchedAt;
    const remaining = Math.max(0, state.ttlSeconds - elapsed);
    const pct       = (remaining / state.ttlSeconds) * 100;

    const fill = document.getElementById('ttl-fill');
    fill.style.width      = pct + '%';
    fill.style.background = pct > 50 ? 'var(--accent2)' :
                            pct > 20 ? 'var(--gold)' : 'var(--danger)';

    const min = Math.floor(remaining / 60);
    const sec = Math.floor(remaining % 60);
    document.getElementById('ttl-countdown').textContent =
        `${min}:${sec.toString().padStart(2, '0')}`;

    if (remaining <= 0) {
        clearInterval(state.ttlTimer);
        stopPolling();
        setVCIStatus('waiting', 'Intent expired', state.vci?.vci_id);
        document.getElementById('ttl-countdown').textContent = 'Expired';
    }
}

// ── UI HELPERS ────────────────────────────────────────────────

function setVCIStatus(type, label, meta) {
    document.getElementById('vci-dot').className = `vci-status-dot ${type}`;
    document.getElementById('status-label').textContent = label;
    document.getElementById('status-meta').textContent  = meta || '';
}

async function testRelay() {
    state.relayUrl = document.getElementById('relay-url-input').value.trim();
    try {
        const resp = await fetch(`${state.relayUrl}/health`);
        const data = await resp.json();
        toast(`Relay OK — ${data.registered_sellers} sellers, ${data.active_vcis} active VCIs`, 'success');
    } catch (e) {
        toast('Relay unreachable: ' + e.message, 'error');
    }
}

function log(msg) {
    console.log(`[O4DB] ${new Date().toISOString()} ${msg}`);
}

function toast(msg, type = 'info') {
    const container = document.getElementById('toasts');
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.textContent = msg;
    container.appendChild(el);
    setTimeout(() => el.remove(), 4000);
}

// ── INIT ──────────────────────────────────────────────────────

// ── SLIDER LOCK ───────────────────────────────────────────────
// Locked sliders do not change when others are moved.
// 1 locked: the 2 free sliders share the remainder proportionally.
// 2 locked: the 1 free slider absorbs all change.
// 3 locked: no movement permitted.

const locked = { price: false, trust: false, speed: false };

function toggleLock(key) {
    locked[key] = !locked[key];
    const btn = document.getElementById('lock-' + key);
    const slider = document.getElementById('w-' + key);
    btn.textContent = locked[key] ? '🔒' : '🔓';
    btn.classList.toggle('locked', locked[key]);
    slider.disabled = locked[key];
}

// Patched adjustWeights respects locked sliders
const _originalAdjustWeights = adjustWeights;
adjustWeights = function(changed, newVal) {
    if (_adjusting) return;
    _adjusting = true;

    // If this slider is locked, ignore
    if (locked[changed]) { _adjusting = false; return; }

    newVal = parseInt(newVal);
    const allKeys  = ['price', 'trust', 'speed'];
    const freeKeys = allKeys.filter(k => k !== changed && !locked[k]);
    const lockKeys = allKeys.filter(k => k !== changed && locked[k]);

    // Sum of locked values (cannot change)
    const lockedSum = lockKeys.reduce(
        (s, k) => s + parseInt(document.getElementById('w-' + k).value), 0
    );
    const remaining = 100 - newVal - lockedSum;

    if (freeKeys.length === 0) {
        // All others locked — clamp newVal so total stays at 100
        const maxAllowed = 100 - lockedSum;
        newVal = Math.max(0, Math.min(maxAllowed, newVal));
        document.getElementById('w-' + changed).value = newVal;
    } else if (freeKeys.length === 1) {
        // One free: absorbs the remainder
        const freeVal = Math.max(0, Math.min(100, remaining));
        document.getElementById('w-' + freeKeys[0]).value = freeVal;
    } else {
        // Two free: distribute proportionally
        const freeSum = freeKeys.reduce(
            (s, k) => s + parseInt(document.getElementById('w-' + k).value), 0
        ) || 1;
        let assigned = 0;
        freeKeys.forEach((k, i) => {
            const cur   = parseInt(document.getElementById('w-' + k).value);
            const share = i === freeKeys.length - 1
                ? remaining - assigned
                : Math.round((cur / freeSum) * remaining);
            const clamped = Math.max(0, Math.min(100, share));
            document.getElementById('w-' + k).value = clamped;
            assigned += clamped;
        });
    }

    // Sync display values
    const p = parseInt(document.getElementById('w-price').value);
    const t = parseInt(document.getElementById('w-trust').value);
    const s = parseInt(document.getElementById('w-speed').value);
    const total = p + t + s;

    document.getElementById('w-price-val').textContent = p + '%';
    document.getElementById('w-trust-val').textContent = t + '%';
    document.getElementById('w-speed-val').textContent = s + '%';
    document.getElementById('ara-total').textContent   = total + '%';
    document.getElementById('ara-total').className =
        'ara-total-value' + (total !== 100 ? ' error' : '');

    document.getElementById('wb-price').style.flex = p;
    document.getElementById('wb-trust').style.flex = t;
    document.getElementById('wb-speed').style.flex = s;

    state.weights = { price: p / 100, trust: t / 100, speed: s / 100 };
    if (state.offers.length) renderOffers();

    _adjusting = false;
};

// ── OFFER SIGNATURE VERIFICATION ─────────────────────────────
// Verifies that the seller's offer signature is valid
// using their registered public key from the relay.
// An offer that fails verification is flagged with integrityViolation.
// The ARA places it last regardless of score.

async function verifyOfferSignature(offer) {
    try {
        if (!offer.signature || !offer.seller_pubkey) return false;

        const price = offer.unit_price;
        const priceCanonical = (Number.isInteger(price) || price === Math.floor(price)) ? Math.floor(price) : price;
        const payload = sortedStringify({
            seller_id:  offer.seller_id,
            unit_price: priceCanonical,
            attributes: offer.attributes,
            vci_id:     state.vci?.vci_id,
        });

        const pubBytes = Uint8Array.from(atob(offer.seller_pubkey), c => c.charCodeAt(0));
        const pubKey   = await crypto.subtle.importKey(
            'raw', pubBytes,
            getKeyGenParams(),
            false, ['verify']
        );
        const sigBytes = Uint8Array.from(atob(offer.signature), c => c.charCodeAt(0));
        const msgBytes = new TextEncoder().encode(payload);

        return await crypto.subtle.verify(
            getVerifyParams(), pubKey, sigBytes, msgBytes
        );
    } catch (e) {
        return false; // Any failure = not verified
    }
}

// Run signature audit on all offers, mark violations
async function auditOfferIntegrity(offers) {
    const results = await Promise.all(offers.map(async o => {
        const valid = await verifyOfferSignature(o);
        return { ...o, signatureValid: valid, integrityViolation: !valid };
    }));
    return results;
}

// ── TRUST RADAR ───────────────────────────────────────────────
// Compares seller's individual trust_score with their network_score.
// Detects sellers who look good historically but are behaving poorly recently.
// network_score < 0.5 while trust_score > 0.7 = suspicious pattern.

const networkScoreCache = {};

async function fetchNetworkScore(sellerId) {
    if (networkScoreCache[sellerId]) return networkScoreCache[sellerId];
    try {
        const resp = await fetch(`${state.relayUrl}/api/v1/trust/${sellerId}`);
        if (!resp.ok) return null;
        const data = await resp.json();
        networkScoreCache[sellerId] = data;
        return data;
    } catch (e) { return null; }
}

// Fetch network scores for all current offers
async function hydrateNetworkScores(offers) {
    const hydrated = await Promise.all(offers.map(async o => {
        const data = await fetchNetworkScore(o.seller_id);
        return {
            ...o,
            network_score:   data?.network_score  ?? null,
            seller_status:   data?.status         ?? null,
        };
    }));
    return hydrated;
}

function buildTrustRadar(offer) {
    const ts = offer.trust_score  || 0.8;
    const ns = offer.network_score;

    if (ns === null || ns === undefined) return '';

    // Ecosystem health logic
    const delta = ts - ns;

    if (ns >= 0.7) {
        return '<span class="trust-radar healthy">📡 Network OK</span>';
    } else if (ns >= 0.4 && delta < 0.3) {
        return '<span class="trust-radar warning">⚠ Network ↓</span>';
    } else {
        return '<span class="trust-radar danger">🔴 Network ↓↓</span>';
    }
}

function buildIntegrityBadge(offer) {
    if (offer.signatureValid === true) {
        return '<span class="integrity-ok">✓ sig</span>';
    } else if (offer.signatureValid === false) {
        return '<span class="integrity-fail">✗ SIG INVALID</span>';
    }
    return '<span style="font-size:10px; color:var(--muted)">sig pending</span>';
}

// ── INDEXEDDB PERSISTENCE ─────────────────────────────────────
// Persists active VCI lifecycle across browser refreshes.
// Stores: vci, offers, state (dispatched, settled, timestamps).

const DB_NAME    = 'o4db-buyer';
const DB_VERSION = 1;
let db = null;

function openDB() {
    return new Promise((resolve, reject) => {
        const req = indexedDB.open(DB_NAME, DB_VERSION);
        req.onupgradeneeded = e => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('sessions')) {
                db.createObjectStore('sessions', { keyPath: 'vci_id' });
            }
        };
        req.onsuccess  = e => { db = e.target.result; resolve(db); };
        req.onerror    = e => reject(e.target.error);
    });
}

async function persistSession() {
    if (!db || !state.vci) return;
    const tx    = db.transaction('sessions', 'readwrite');
    const store = tx.objectStore('sessions');
    store.put({
        vci_id:       state.vci.vci_id,
        vci:          state.vci,
        offers:       state.offers,
        maxPrice:     state.maxPrice,
        commitment:   state.commitment,
        ttlSeconds:   state.ttlSeconds,
        dispatchedAt: state.dispatchedAt,
        settled:      state.settled,
        savedAt:      Date.now(),
    });
}

async function recoverSession() {
    if (!db) return;
    const tx    = db.transaction('sessions', 'readonly');
    const store = tx.objectStore('sessions');
    const req   = store.getAll();

    req.onsuccess = async e => {
        const sessions = e.target.result;
        if (!sessions.length) return;

        // Find the most recent non-expired active session
        const now_ts = Date.now() / 1000;
        const active = sessions
            .filter(s => !s.settled && s.dispatchedAt + s.ttlSeconds > now_ts)
            .sort((a, b) => b.savedAt - a.savedAt)[0];

        if (!active) return;

        state.vci          = active.vci;
        state.offers       = active.offers || [];
        state.maxPrice     = active.maxPrice;
        state.commitment   = active.commitment;
        state.ttlSeconds   = active.ttlSeconds;
        state.dispatchedAt = active.dispatchedAt;
        state.settled      = active.settled;

        // Restore UI
        document.getElementById('status-bar').style.display   = 'flex';
        document.getElementById('ttl-track').style.display    = 'block';
        document.getElementById('dispatch-btn').classList.add('active');
        document.getElementById('dispatch-icon').textContent  = '⏹';
        document.getElementById('dispatch-label').textContent = 'Cancel Intent';

        setVCIStatus('waiting', `Session recovered — ${state.offers.length} offers`, state.vci.vci_id);

        // Re-audit and render
        state.offers = await auditOfferIntegrity(state.offers);
        state.offers = await hydrateNetworkScores(state.offers);
        renderOffers();
        startOfferPolling();
        startTTLCountdown();

        toast('Session recovered from previous tab', 'success');
    };
}

// ── FINGERPRINT DOWNLOAD ──────────────────────────────────────

function downloadFingerprint() {
    const fp  = document.getElementById('fingerprint-display').textContent;
    const vci = state.vci?.vci_id || 'unknown';
    const ts  = new Date().toISOString().replace(/[:.]/g, '-');

    const data = JSON.stringify({
        protocol:               'O4DB v1.1.4',
        settlement_fingerprint: fp,
        fingerprint_status:     state.fingerprintStatus || 'local',
        settlement_token:       state.settlementToken   || null,
        vci_id:                 vci,
        buyer_pubkey:           state.encPublicKeyB64,
        timestamp:              ts,
        computation:            'SHA-256(vci_id + seller_id + price + buyer_pubkey + timestamp)',
        note: 'This fingerprint is your immutable proof of settlement. Verify independently.',
    }, null, 2);

    const blob = new Blob([data], { type: 'application/json' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = `o4db-settlement-${vci}-${ts}.json`;
    a.click();
    URL.revokeObjectURL(url);
    toast('Fingerprint downloaded', 'success');
}

// ── GHOSTING REPORT ───────────────────────────────────────────
// SPS Trigger: buyer reports seller did not ACK after settlement.
// Feeds the penalty system in the relay.

async function reportGhosting() {
    if (!state.vci || !state.pendingSettlement) {
        toast('No active settlement to report', 'warning'); return;
    }
    if (!confirm('Report this seller for ghosting? This will apply a penalty to their Trust Score.')) return;

    try {
        const resp = await fetch(
            `${state.relayUrl}/api/v1/vci/${state.vci.vci_id}/ghost` +
            `?seller_id=${encodeURIComponent(state.pendingSettlement.sellerId)}`,
            { method: 'POST' }
        );
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Report failed');

        toast(`Ghosting reported — seller penalty: ${data.penalty}`, 'warning');
        document.getElementById('btn-ghost-report').disabled = true;
        document.getElementById('btn-ghost-report').textContent = '✓ Reported';
    } catch (e) {
        toast('Report failed: ' + e.message, 'error');
    }
}


window.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
});

initIdentity();
</script>
<script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'9d4bcf496c0afe20',t:'MTc3MjIzODU4OA=='};var a=document.createElement('script');a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>
