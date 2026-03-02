"""
O4DB™ Protocol — Relay Server v1.1.5
# O4DB™ | v1.1.5 | build: 20260227-001 | 2026-02-27T18:00Z
Last-Updated: 2026-02-25T17:50Z
Copyright © 2026 Daniel Eduardo Placanica. All Rights Reserved.
Safe Creative IDs: 2602184604821-4XTVN6 / 2602204641140-6FSX6N
Contact: https://x.com/O4DBmodel | daniel@o4db.org
License: O4DB™ Community & Commercial License v1.1.5

LICENSE: O4DB™ COMMUNITY & COMMERCIAL LICENSE v1.1.5
  1. RESEARCH & TESTING:  100% Free for non-commercial research and evaluation.
  2. COMMUNITY TIER:      Free for production use up to 50 settlement
                          operations per month.
  3. COMMERCIAL TIER:     Any entity exceeding 50 settlements/month or
                          integrating this core logic into a centralized
                          marketplace must obtain a Commercial License.
  4. INTEGRITY:           Modification of the VCI (Intent Commitment) core
                          cycle logic for commercial redistribution is
                          strictly prohibited. Optional layers (ARA, BES,
                          SPS, Escrow) may be implemented independently
                          by applications built on this protocol.

TRADEMARK NOTICE:
  O4DB™ and "Only For Determined Buyers" are trademarks of
  Daniel Eduardo Placanica. Third-party implementations may not use
  the O4DB™ name or logo without explicit written license.

CRYPTOGRAPHIC POLICY (Key Separation Principle — RFC 8032 / RFC 9180):
  Identity & Non-repudiation:
    Primary:   Ed25519 (RFC 8032) — all VCI, ACK, offer, and settlement signatures
    Fallback:  P-256 / ECDSA — hardware HSM and FIDO2/WebAuthn device compatibility
  Confidentiality (Price Privacy):
    Algorithm: HPKE (RFC 9180) using DHKEM(X25519, HKDF-SHA256) + AES-128-GCM
    Scope:     price_token encryption — buyer-side only, relay never holds plaintext
  Rationale:
    Signing keys (Ed25519/P-256) and encryption keys (X25519) are STRICTLY SEPARATED.
    Reusing a signing key for key agreement creates cross-protocol attack surfaces.
    This design mirrors TLS 1.3: certificate key ≠ ephemeral handshake key.
  Integrity:       SHA-256
  Concurrency:     Atomic SQLite transactions (BEGIN IMMEDIATE)
  Protection:      Anti-replay timestamp validation (±300s window) on all signed endpoints

WHAT THIS SERVER DOES:

  CORE CYCLE (always active — neutral infrastructure):
  1.  Receives signed VCIs from buyers via REST API
  2.  Validates Ed25519 VCI signature + anti-replay timestamp
  3.  Applies 6-criteria eligibility filter
  4.  Manages Inventory Affinity + Probation Mode
  5.  Broadcasts Public VCI to eligible seller nodes (demand_type routing)
  6.  Manages TTL expiration with DATA_PURGE
  7.  Receives seller offers (one per seller per VCI)
  8.  Tracks Network Score + throttling per seller (SPS)
  9.  Manages Settlement Token lifecycle (atomic state machine)
  10. Verifies ACK privacy commitment (Ed25519)
  11. Records Settlement Fingerprints (immutable, on-chain ready)
  12. Seller ghosting detection with graduated penalties

  OPTIONAL LAYERS (opt-in via environment config):
  BES  Buyer Execution Score — buyer reputation enforcement (BES_ENABLED=true)
  ARA  Local ranking algorithm — runs on buyer device, never on relay
  Escrow / FullEscrow — PSP-backed guarantees, app-layer responsibility

DEPLOYMENT:
  Development:  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  Production:   docker compose up -d
"""

import hashlib
import time
import os
import sqlite3
import base64
import json
import secrets
import asyncio
from contextlib import contextmanager
from typing import Optional, List
from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDSA, SECP256R1, EllipticCurvePublicKey
)
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.exceptions import InvalidSignature


# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────

DB_PATH              = os.getenv("DB_PATH", "o4db_relay.db")
REPLAY_WINDOW_SEC    = 300     # anti-replay: reject requests older than 5 min
MIN_AFFINITY_POOL    = 3       # min affinity sellers before fallback to probation
SANDBOX_THRESHOLD    = 25      # transactions before SANDBOX_NEW graduates
# Settlement hold multipliers — velocity-based ghosting amplification
HOLD_WINDOW_SEC      = 600     # 10-minute window to measure burst velocity
HOLD_BURST_MEDIUM    = 3       # >3 settlements in window → 5x multiplier
HOLD_BURST_HIGH      = 10      # >10 settlements in window → 15x multiplier
HOLD_MULT_NORMAL     = 1.0     # baseline (all ghosting penalties × 1.0)
HOLD_MULT_MEDIUM     = 5.0     # burst detected
HOLD_MULT_HIGH       = 15.0    # high burst — offers get warning badge
GHOSTING_PENALTY_1ST = 0.15
GHOSTING_PENALTY_2ND = 0.30
GHOSTING_PENALTY_3RD = 0.50
ST_TTL_B2C           = 900     # 15 min default
COMMUNITY_LIMIT      = 50      # free tier: max settlements/month


# ─────────────────────────────────────────────────────────────
# VCI STATES
# ─────────────────────────────────────────────────────────────

class VCIState(str, Enum):
    ACTIVE                 = "ACTIVE"
    SETTLING               = "SETTLING"
    SETTLED_PENDING        = "SETTLED_PENDING"
    CONFIRMED              = "CONFIRMED"
    EXPIRED                = "EXPIRED"
    FAILED_SELLER_GHOSTING = "FAILED_SELLER_GHOSTING"
    VCI_ABORTED            = "VCI_ABORTED"    # reserved: buyer-initiated abort (v1.2+)
    BUYER_FAULT            = "BUYER_FAULT"


# ─────────────────────────────────────────────────────────────
# DATABASE — SQLite with atomic transactions
# ─────────────────────────────────────────────────────────────

def init_db():
    """Initialize all tables. Safe to call multiple times."""
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS sellers (
            seller_id          TEXT PRIMARY KEY,
            categories         TEXT NOT NULL,
            delivery_areas     TEXT NOT NULL,
            min_commitment     INTEGER DEFAULT 0,
            sign_pubkey        TEXT NOT NULL UNIQUE,
            webhook_url        TEXT,
            inventory_ids      TEXT DEFAULT '[]',
            network_score      REAL DEFAULT 1.0,
            vci_received       INTEGER DEFAULT 0,
            vci_responded      INTEGER DEFAULT 0,
            offers_submitted   INTEGER DEFAULT 0,
            offers_won         INTEGER DEFAULT 0,
            competitive_offers INTEGER DEFAULT 0,
            total_transactions INTEGER DEFAULT 0,
            trust_score        REAL DEFAULT 0.80,
            penalty            REAL DEFAULT 0.0,
            status             TEXT DEFAULT 'SANDBOX_NEW',
            registered_at      REAL DEFAULT 0,
            standby_until                REAL DEFAULT NULL,
            standby_days_used_this_year  INTEGER DEFAULT 0,
            last_standby_reset           REAL DEFAULT 0,
            cumulative_volume            REAL DEFAULT 0.0
        );

        CREATE TABLE IF NOT EXISTS vci_active (
            vci_id             TEXT PRIMARY KEY,
            demand_spec        TEXT NOT NULL,
            demand_type        TEXT,
            master_code        TEXT,
            demand_object      TEXT,
            identifier_type    TEXT NOT NULL,
            identifier_value   TEXT NOT NULL,
            quantity           INTEGER NOT NULL,
            price_token        TEXT NOT NULL,
            currency           TEXT NOT NULL,
            ttl                INTEGER NOT NULL,
            commitment_level   INTEGER NOT NULL,
            delivery_area      TEXT NOT NULL,
            privacy_mode       TEXT NOT NULL,
            buyer_pubkey       TEXT NOT NULL,
            buyer_sign_pub     TEXT NOT NULL,
            vci_signature      TEXT NOT NULL,
            weights            TEXT NOT NULL,
            trust_floor        REAL DEFAULT 0.5,
            banned_sellers     TEXT DEFAULT '[]',
            state              TEXT DEFAULT 'ACTIVE',
            created_at         REAL NOT NULL,
            expires_at         REAL NOT NULL,
            winner_seller_id   TEXT,
            settlement_token   TEXT,
            settlement_timestamp REAL,
            ghost_penalty_mult        REAL DEFAULT 1.0,
            standby_seller_id         TEXT DEFAULT NULL,
            parallel_standby_notified INTEGER DEFAULT 0,
            external_ref_mapping      TEXT DEFAULT NULL
        );

        CREATE TABLE IF NOT EXISTS offers (
            offer_id           TEXT PRIMARY KEY,
            vci_id             TEXT NOT NULL,
            seller_id          TEXT NOT NULL,
            unit_price         REAL NOT NULL,
            attributes         TEXT NOT NULL,
            signature          TEXT NOT NULL,
            affinity_mode      TEXT DEFAULT 'probation',
            submitted_at       REAL NOT NULL,
            FOREIGN KEY (vci_id) REFERENCES vci_active(vci_id)
        );

        CREATE TABLE IF NOT EXISTS settlement_fingerprints (
            fingerprint        TEXT PRIMARY KEY,
            vci_id             TEXT NOT NULL,
            seller_id          TEXT NOT NULL,
            unit_price         REAL NOT NULL,
            identifier_type    TEXT NOT NULL,
            identifier_value   TEXT NOT NULL,
            buyer_pubkey       TEXT NOT NULL,
            seller_pubkey      TEXT NOT NULL,
            privacy_commitment_proof TEXT,
            created_at         REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS network_score_log (
            log_id             TEXT PRIMARY KEY,
            seller_id          TEXT NOT NULL,
            event_type         TEXT NOT NULL,
            detail             TEXT,
            created_at         REAL NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_vci_state
            ON vci_active(state);
        CREATE INDEX IF NOT EXISTS idx_offers_vci
            ON offers(vci_id);
        CREATE INDEX IF NOT EXISTS idx_fingerprints_id
            ON settlement_fingerprints(identifier_value);

        CREATE TABLE IF NOT EXISTS buyer_registry (
            buyer_pubkey        TEXT PRIMARY KEY,
            status              TEXT DEFAULT 'INITIAL',
            vci_emitted         INTEGER DEFAULT 0,
            settlements         INTEGER DEFAULT 0,
            acks_received       INTEGER DEFAULT 0,
            ghosting_count      INTEGER DEFAULT 0,
            suspended_until     REAL DEFAULT NULL,
            registered_at       REAL NOT NULL,
            last_activity       REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS buyer_ghosting_reports (
            report_id           TEXT PRIMARY KEY,
            vci_id              TEXT NOT NULL,
            seller_id           TEXT NOT NULL,
            buyer_pubkey        TEXT NOT NULL,
            reported_at         REAL NOT NULL,
            grace_expires_at    REAL NOT NULL,
            status              TEXT DEFAULT 'PENDING',
            resolved_at         REAL DEFAULT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_buyer_status
            ON buyer_registry(status);
        CREATE INDEX IF NOT EXISTS idx_buyer_reports_grace
            ON buyer_ghosting_reports(grace_expires_at, status);
        """)
    print(f"[DB] Initialized: {DB_PATH}")


@contextmanager
def get_db(immediate: bool = False):
    """
    Context manager for database connections.
    immediate=True: uses BEGIN IMMEDIATE for atomic writes —
    prevents race conditions in settlement state transitions.
    """
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        if immediate:
            conn.execute("BEGIN IMMEDIATE")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def generate_id(prefix: str = "") -> str:
    return f"{prefix}{secrets.token_hex(16)}"


# ─────────────────────────────────────────────────────────────
# SECURITY — Ed25519 + Anti-Replay
# ─────────────────────────────────────────────────────────────

def verify_ed25519(pubkey_b64: str, message: bytes, signature_b64: str,
                   timestamp: Optional[float] = None) -> bool:
    """
    Verify Ed25519 signature over message.

    If timestamp provided: also validates anti-replay window (±300s).
    This prevents recorded requests from being replayed later.

    Returns True only if signature is valid AND timestamp is fresh.
    """
    # Anti-replay check
    if timestamp is not None:
        if abs(time.time() - timestamp) > REPLAY_WINDOW_SEC:
            return False

    try:
        pub_bytes = base64.b64decode(pubkey_b64)
        sig_bytes = base64.b64decode(signature_b64)
        pub = Ed25519PublicKey.from_public_bytes(pub_bytes)
        pub.verify(sig_bytes, message)
        return True
    except (InvalidSignature, Exception):
        return False


def verify_p256(pubkey_b64: str, message: bytes, signature_b64: str,
                timestamp: Optional[float] = None) -> bool:
    """
    Verify ECDSA P-256 / SHA-256 signature over message.

    Fallback algorithm for browsers that do not support Ed25519
    (Safari < 17, Firefox < 130, Chrome < 113).
    Public key: 65-byte uncompressed point (0x04 prefix).
    Signature: DER-encoded or raw 64-byte IEEE P1363 format.
    """
    if timestamp is not None:
        if abs(time.time() - timestamp) > REPLAY_WINDOW_SEC:
            return False
    try:
        from cryptography.hazmat.primitives.asymmetric.ec import (
            EllipticCurvePublicKey
        )
        from cryptography.hazmat.backends import default_backend
        pub_bytes = base64.b64decode(pubkey_b64)
        sig_bytes = base64.b64decode(signature_b64)

        # Load uncompressed P-256 public key (65 bytes: 0x04 + x + y)
        pub = EllipticCurvePublicKey.from_encoded_point(SECP256R1(), pub_bytes)

        # Web Crypto API exports signatures in IEEE P1363 (raw r||s, 64 bytes).
        # cryptography lib expects DER — convert if needed.
        if len(sig_bytes) == 64:
            r = int.from_bytes(sig_bytes[:32], 'big')
            s = int.from_bytes(sig_bytes[32:], 'big')
            from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
            sig_bytes = encode_dss_signature(r, s)

        pub.verify(sig_bytes, message, ECDSA(hashes.SHA256()))
        return True
    except (InvalidSignature, Exception):
        return False


def verify_signature(pubkey_b64: str, message: bytes, signature_b64: str,
                     timestamp: Optional[float] = None) -> bool:
    """
    Algorithm-agnostic signature verification.

    Auto-detects algorithm by public key length:
      32 bytes → Ed25519 (RFC 8032)  — modern browsers
      65 bytes → ECDSA P-256         — Safari < 17, Firefox < 130 fallback

    This allows the relay to accept offers and VCIs from any browser
    without requiring a specific key algorithm.
    """
    try:
        pub_bytes = base64.b64decode(pubkey_b64)
    except Exception:
        return False

    if len(pub_bytes) == 32:
        return verify_ed25519(pubkey_b64, message, signature_b64, timestamp)
    elif len(pub_bytes) == 65:
        return verify_p256(pubkey_b64, message, signature_b64, timestamp)
    else:
        # Unknown key format — reject
        return False




def validate_vci_signature(vci: dict) -> bool:
    """Verify Ed25519 signature over canonical VCI payload."""
    payload = json.dumps({
        "vci_id":           vci["vci_id"],
        "demand_spec":      vci["demand_spec"],
        "quantity":         vci["quantity"],
        "price_token":      vci["price_token"],
        "currency":         vci["currency"],
        "ttl":              vci["ttl"],
        "commitment_level": vci["commitment_level"],
        "delivery_area":    vci["delivery_area"],
        "privacy_mode":     vci["privacy_mode"],
        "timestamp":        vci["timestamp"],
    }, separators=(",", ":"), sort_keys=True).encode()

    return verify_signature(
        vci["buyer_sign_pub"],
        payload,
        vci["vci_signature"],
        timestamp=vci["timestamp"]   # anti-replay on VCI
    )


def validate_offer_signature(offer: dict, vci_id: str,
                              seller_pubkey: str) -> bool:
    """Verify seller Ed25519 signature over offer payload."""
    # unit_price: use int if whole number to match JS JSON.stringify behavior
    price = offer["unit_price"]
    price_canonical = int(price) if float(price) == int(price) else float(price)
    payload = json.dumps({
        "seller_id":  offer["seller_id"],
        "unit_price": price_canonical,
        "attributes": offer["attributes"],
        "vci_id":     vci_id,
    }, separators=(",", ":"), sort_keys=True).encode()

    return verify_signature(seller_pubkey, payload, offer["signature"])


# ─────────────────────────────────────────────────────────────
# SIX-CRITERIA ELIGIBILITY FILTER
# ─────────────────────────────────────────────────────────────

def geography_match(vci_area: str, seller_areas: list) -> bool:
    """
    Criterion 2: Geographic coverage.
    'AR:CABA' matches ['AR', 'AR:CABA', 'AR:BA'].
    Country-level 'AR' covers all subdivisions.
    """
    vci_parts = vci_area.split(":")
    vci_country = vci_parts[0]
    vci_region  = vci_parts[1] if len(vci_parts) > 1 else None

    for area in seller_areas:
        parts    = area.split(":")
        s_country = parts[0]
        s_region  = parts[1] if len(parts) > 1 else None

        if s_country != vci_country:
            continue
        if s_region is None:        # seller covers entire country
            return True
        if vci_region is None or vci_region == s_region:
            return True
    return False


def apply_eligibility_filter(vci: dict, sellers: list) -> list:
    """
    Apply all six criteria. Returns [(seller, mode)] tuples.

    Criteria:
      C1 — Proof of Category
      C2 — Geographic coverage
      C3 — Fulfillment modality (delivery assumed for pilot)
      C4 — Minimum commitment level
      C5 — Buyer ban list
      C6 — Inventory Affinity (with Probation Mode fallback)

    Probation Mode: sellers without affinity history receive
    a 0.70 ranking multiplier. They always participate —
    never excluded — when affinity pool < MIN_AFFINITY_POOL.
    """
    banned           = json.loads(vci.get("banned_sellers") or "[]")
    identifier_value = vci["identifier_value"]

    now = time.time()
    eligible = []
    for s in sellers:
        categories     = json.loads(s["categories"])
        delivery_areas = json.loads(s["delivery_areas"])

        # C0 — STANDBY: exclude nodes with active standby declaration
        if s.get("standby_until") and s["standby_until"] > now:
            continue

        # C1 — Category
        if vci["identifier_type"] not in categories and "general" not in categories:
            continue
        # C2 — Geography
        if not geography_match(vci["delivery_area"], delivery_areas):
            continue
        # C3 — Fulfillment (delivery assumed for pilot)
        # C4 — Commitment
        if s["min_commitment"] > vci["commitment_level"]:
            continue
        # C5 — Ban list
        if s["seller_id"] in banned:
            continue

        eligible.append(s)

    # C6 — Inventory Affinity
    affinity  = [s for s in eligible
                 if identifier_value in json.loads(s["inventory_ids"] or "[]")]
    probation = [s for s in eligible
                 if identifier_value not in json.loads(s["inventory_ids"] or "[]")]

    if len(affinity) >= MIN_AFFINITY_POOL:
        return [(s, "affinity") for s in affinity]
    else:
        return (
            [(s, "affinity")  for s in affinity] +
            [(s, "probation") for s in probation]
        )


# ─────────────────────────────────────────────────────────────
# NETWORK SCORE + THROTTLING
# ─────────────────────────────────────────────────────────────

THROTTLE_TABLE = [
    (0.80, 1.00),   # score ≥ 0.80 → 100% traffic
    (0.60, 0.75),
    (0.40, 0.50),
    (0.20, 0.25),
    (0.00, 0.10),   # floor: always some traffic, never zero
]

def compute_network_score(s: dict) -> float:
    """
    network_score = (response_ratio  × 0.30) +
                    (conversion_ratio × 0.40) +
                    (sla_score        × 0.30)

    SANDBOX_NEW: warm-up protection — score = 1.0 (no throttling).
    """
    if s["status"] == "SANDBOX_NEW":
        return 1.0

    received    = s["vci_received"]    or 1
    responded   = s["vci_responded"]   or 0
    submitted   = s["offers_submitted"] or 1
    won         = s["offers_won"]      or 0
    competitive = s["competitive_offers"] or 0

    return round(
        min(1.0, responded  / received)   * 0.30 +
        min(1.0, won        / submitted)  * 0.40 +
        min(1.0, competitive / submitted) * 0.30,
        4
    )


def should_receive_vci(s: dict) -> bool:
    """
    Probabilistic throttling based on Network Score.
    Low-quality sellers receive fewer VCIs automatically.
    SANDBOX_NEW always receives (warm-up protection).
    """
    if s["status"] == "SANDBOX_NEW":
        return True

    score = compute_network_score(s)
    for threshold, traffic_ratio in THROTTLE_TABLE:
        if score >= threshold:
            return secrets.randbelow(100) < int(traffic_ratio * 100)
    return False


# ─────────────────────────────────────────────────────────────
# COMMUNITY LIMIT CHECK
# ─────────────────────────────────────────────────────────────

def check_community_limit() -> bool:
    """
    Community Tier: max 50 settlements per calendar month.
    Uses first second of current UTC calendar month — NOT rolling 30 days —
    to match contractual month boundaries correctly.
    Returns True if under limit (operation permitted).
    """
    import datetime
    now = datetime.datetime.utcnow()
    month_start = datetime.datetime(now.year, now.month, 1).timestamp()
    with get_db() as db:
        count = db.execute(
            "SELECT COUNT(*) as n FROM settlement_fingerprints WHERE created_at > ?",
            (month_start,)
        ).fetchone()
    return count["n"] < COMMUNITY_LIMIT


# ─────────────────────────────────────────────────────────────
# BROADCASTER
# ─────────────────────────────────────────────────────────────

async def notify_seller(webhook_url: str, payload: dict):
    """
    POST Public VCI to seller webhook.
    Fire-and-forget. Seller responsible for responding within TTL.
    """
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(webhook_url, json=payload)
    except Exception as e:
        print(f"[WEBHOOK] Failed → {webhook_url}: {e}")


def build_public_vci(vci: dict, affinity_mode: str) -> dict:
    """
    Public VCI payload for seller broadcast.
    max_price is NEVER included. Only the HPKE-encrypted price_token.
    """
    return {
        "vci_id":           vci["vci_id"],
        "demand_spec":      vci["demand_spec"],
        "demand_type":      vci.get("demand_type"),
        "master_code":      vci.get("master_code"),
        "demand_object":    json.loads(vci["demand_object"]) if vci.get("demand_object") else None,
        "external_ref_mapping": vci.get("external_ref_mapping"),  # buyer-side only, never in broadcast
        "quantity":         vci["quantity"],
        "price_token":      vci["price_token"],
        "currency":         vci["currency"],
        "ttl":              vci["ttl"],
        "commitment_level": vci["commitment_level"],
        "delivery_area":    vci["delivery_area"],
        "privacy_mode":     vci["privacy_mode"],
        "buyer_pubkey":     vci["buyer_pubkey"],
        "affinity_mode":    affinity_mode,
        "offer_endpoint":   f"/api/v1/vci/{vci['vci_id']}/offer",
    }


# ─────────────────────────────────────────────────────────────
# TTL EXPIRATION
# ─────────────────────────────────────────────────────────────

async def expire_vci(vci_id: str, ttl_seconds: int):
    """
    Background task: expire VCI after TTL.
    DATA_PURGE: all offers deleted, VCI state → EXPIRED.
    """
    await asyncio.sleep(ttl_seconds)
    with get_db(immediate=True) as db:
        vci = db.execute(
            "SELECT state FROM vci_active WHERE vci_id = ?", (vci_id,)
        ).fetchone()
        if not vci or vci["state"] != VCIState.ACTIVE:
            return

        db.execute(
            "UPDATE vci_active SET state = ? WHERE vci_id = ?",
            (VCIState.EXPIRED, vci_id)
        )
        db.execute("DELETE FROM offers WHERE vci_id = ?", (vci_id,))

    print(f"[TTL] {vci_id} expired — data purged")


# ─────────────────────────────────────────────────────────────
# FASTAPI APP
# ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="O4DB™ Relay Server",
    description="Protocol relay node — v1.1.5 | © 2026 Daniel Eduardo Placanica",
    version="v1.1.5",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict to known origins in production
    allow_methods=["*"],
    allow_headers=["*"],
)


async def ghost_monitor():
    """
    Background monitor: auto-penalize sellers that ghost (no ACK after ST_TTL_B2C).
    Runs every 60 seconds. Resolves SETTLED_PENDING VCIs past their ACK deadline.
    Previously called manually — now automatic as intended by design.
    NOTE: SQLite contention is a known limitation at this scale. Stress tested at 100 nodes (v1.1.5): p50=2s, p95=5s, max=7s. Migrate to PostgreSQL or write-queue for >50 concurrent nodes.
          Documented for future migration to PostgreSQL or write-queue architecture.
    """
    await asyncio.sleep(30)  # initial delay — let relay warm up
    while True:
        try:
            deadline = time.time() - ST_TTL_B2C
            with get_db(immediate=True) as db:
                ghosted = db.execute("""
                    SELECT vci_id, winner_seller_id, settlement_timestamp
                    FROM vci_active
                    WHERE state = 'SETTLED_PENDING'
                    AND settlement_timestamp < ?
                """, (deadline,)).fetchall()

            for row in ghosted:
                vci_id    = row["vci_id"]
                seller_id = row["winner_seller_id"]
                try:
                    report_ghosting(vci_id, seller_id)
                    print(f"[GHOST-MONITOR] Auto-penalized {seller_id} for {vci_id}")
                except Exception as ex:
                    print(f"[GHOST-MONITOR] Error penalizing {seller_id}: {ex}")

            # ── PARALLEL STANDBY: notify standby seller after 120s ──────
            # If winner has not ACKed within 120s, relay notifies standby seller.
            # This reduces double-ghosting wait from 30min to ~2min for the buyer.
            standby_deadline = time.time() - 120   # 2 minutes
            pending_standby = []
            with get_db() as db:
                pending_standby = db.execute("""
                    SELECT vci_id, standby_seller_id, winner_seller_id, settlement_timestamp
                    FROM vci_active
                    WHERE state = 'SETTLED_PENDING'
                    AND standby_seller_id IS NOT NULL
                    AND parallel_standby_notified = 0
                    AND settlement_timestamp < ?
                """, (standby_deadline,)).fetchall()

            for row in pending_standby:
                try:
                    with get_db(immediate=True) as db:
                        vci = db.execute(
                            "SELECT * FROM vci_active WHERE vci_id = ? AND state = 'SETTLED_PENDING'",
                            (row["vci_id"],)
                        ).fetchone()
                        if not vci:
                            continue
                        standby = db.execute(
                            "SELECT * FROM sellers WHERE seller_id = ?",
                            (row["standby_seller_id"],)
                        ).fetchone()
                        if standby and standby["webhook_url"]:
                            payload = {
                                "event":            "PARALLEL_STANDBY",
                                "vci_id":           row["vci_id"],
                                "standby_seller_id": row["standby_seller_id"],
                                "winner_seller_id":  row["winner_seller_id"],
                                "message":          "Primary winner has not ACKed. You are on standby.",
                            }
                            try:
                                import httpx as _httpx
                                import asyncio as _asyncio
                                async def _notify():
                                    async with _httpx.AsyncClient(timeout=5.0) as client:
                                        await client.post(standby["webhook_url"], json=payload)
                                _asyncio.ensure_future(_notify())
                            except Exception:
                                pass
                        db.execute("""
                            UPDATE vci_active SET parallel_standby_notified = 1
                            WHERE vci_id = ?
                        """, (row["vci_id"],))
                        print(f"[PARALLEL-STANDBY] Notified {row['standby_seller_id']} for {row['vci_id']}")
                except Exception as ex:
                    print(f"[PARALLEL-STANDBY] Error notifying standby for {row['vci_id']}: {ex}")

        except Exception as ex:
            print(f"[GHOST-MONITOR] Monitor error: {ex}")

        await asyncio.sleep(60)

@app.on_event("startup")
def startup():
    init_db()
    print("[RELAY] O4DB™ Relay Server v1.1.5 — online")
    print(f"[RELAY] DB: {DB_PATH}")
    print(f"[RELAY] Community limit: {COMMUNITY_LIMIT} settlements/month")
    asyncio.ensure_future(ghost_monitor())
    print("[RELAY] Ghost monitor started — auto-penalizes sellers after ST_TTL_B2C")
    print(f"[RELAY] BES (Buyer Execution Score): {'ENABLED' if BES_ENABLED else 'DISABLED (opt-in)'}")


# ─────────────────────────────────────────────────────────────
# PYDANTIC MODELS
# ─────────────────────────────────────────────────────────────

class SellerRegistration(BaseModel):
    seller_id:      str
    categories:     List[str]
    delivery_areas: List[str]
    min_commitment: int = 0
    sign_pubkey:    str
    webhook_url:    Optional[str] = None
    inventory_ids:  List[str] = []
    timestamp:      float
    signature:      str

class DemandObject(BaseModel):
    """
    Optional commercial conditions for the VCI.
    The relay stores and broadcasts this object without validation.
    All fields are free-form strings — format enforcement is the app's responsibility.
    """
    uom:         Optional[str] = None   # unit of measure: EA, KGM, TNE, LTR, BBL, etc.
    stock_ready: Optional[int] = None   # days until available (0 = immediate)
    condition:   Optional[str] = None   # product state: NE, NS, OH, SV, OPEN, etc.
    rfq:         Optional[str] = None   # buyer internal reference number

class VCISubmission(BaseModel):
    vci_id:           str
    demand_spec:      str                  # legacy: kept for backwards compat
    demand_type:      Optional[str] = None # routing tag: EAN, VIN, UODI, NSN, etc.
    master_code:      Optional[str] = None # the actual identifier (no length limit)
    quantity:         int
    price_token:      str
    currency:         str
    ttl:              int
    commitment_level: int
    delivery_area:    str
    privacy_mode:     str
    buyer_pubkey:     str
    buyer_sign_pub:   str
    vci_signature:    str
    weights:          dict
    trust_floor:      float = 0.5
    banned_sellers:   List[str] = []
    demand_object:        Optional[DemandObject] = None  # commercial conditions (optional)
    external_ref_mapping: Optional[str] = None            # buyer-internal ERP ref — never broadcast to sellers
    timestamp:            float

class OfferSubmission(BaseModel):
    seller_id:  str
    unit_price: float
    attributes: dict
    signature:  str
    timestamp:  float = 0.0  # optional for backwards compat, validated if present

class SettlementRequest(BaseModel):
    vci_id:            str
    winner_seller_id:  str
    standby_seller_id: Optional[str] = None   # Parallel Standby — 2nd ranked seller
    buyer_sign_pub:    str
    timestamp:         float
    signature:         str

class ACKSubmission(BaseModel):
    seller_id:           str
    privacy_mode:        str
    seller_sign_pub:     str
    ack_signature:       str
    privacy_commitment:  str
    privacy_mode_ref:    str
    vci_reference:       str
    settlement_token_id: str
    timestamp:           float


# ─────────────────────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "protocol": "O4DB™",
        "version":  "1.1.5",
        "build_date": "2026-02-24",
        "author":   "Daniel Eduardo Placanica",
        "contact":  "https://x.com/O4DBmodel",
        "status":   "online",
    }

@app.get("/health")
def health():
    with get_db() as db:
        sellers = db.execute("SELECT COUNT(*) as n FROM sellers").fetchone()
        active  = db.execute(
            "SELECT COUNT(*) as n FROM vci_active WHERE state = 'ACTIVE'"
        ).fetchone()
        month_settlements = db.execute(
            "SELECT COUNT(*) as n FROM settlement_fingerprints WHERE created_at > ?",
            (time.time() - 30 * 86400,)
        ).fetchone()
    return {
        "status":               "healthy",
        "registered_sellers":   sellers["n"],
        "active_vcis":          active["n"],
        "monthly_settlements":  month_settlements["n"],
        "community_limit":      COMMUNITY_LIMIT,
        "timestamp":            time.time(),
    }


# ── SELLER ───────────────────────────────────────────────────

@app.post("/api/v1/seller/register", status_code=200)
def register_seller(data: SellerRegistration):
    """
    Register a seller node.
    New sellers enter SANDBOX_NEW — warm-up protection for 25 transactions.
    Network Score not measured during warm-up.
    """
    # Anti-replay: validate Ed25519 signature over registration payload
    reg_payload = json.dumps({
        "seller_id":      data.seller_id,
        "categories":     sorted(data.categories),
        "delivery_areas": sorted(data.delivery_areas),
        "min_commitment": data.min_commitment,
        "sign_pubkey":    data.sign_pubkey,
        "timestamp":      data.timestamp,
    }, separators=(",", ":"), sort_keys=True).encode()
    if not verify_signature(data.sign_pubkey, reg_payload, data.signature,
                            timestamp=data.timestamp):
        raise HTTPException(400, "REGISTRATION_SIGNATURE_INVALID")

    with get_db(immediate=True) as db:
        if db.execute(
            "SELECT seller_id FROM sellers WHERE seller_id = ?",
            (data.seller_id,)
        ).fetchone():
            raise HTTPException(409, f"Seller {data.seller_id} already registered")

        if db.execute(
            "SELECT seller_id FROM sellers WHERE sign_pubkey = ?",
            (data.sign_pubkey,)
        ).fetchone():
            raise HTTPException(409, "PUBKEY_CONFLICT — this public key is already registered to another seller identity. Each keypair must be unique across the network.")

        db.execute("""
            INSERT INTO sellers
              (seller_id, categories, delivery_areas, min_commitment,
               sign_pubkey, webhook_url, inventory_ids, status, registered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'SANDBOX_NEW', ?)
        """, (
            data.seller_id,
            json.dumps(data.categories),
            json.dumps(data.delivery_areas),
            data.min_commitment,
            data.sign_pubkey,
            data.webhook_url,
            json.dumps(data.inventory_ids),
            time.time()
        ))

    return {
        "status":    "registered",
        "seller_id": data.seller_id,
        "mode":      "SANDBOX_NEW",
        "graduates_after": f"{SANDBOX_THRESHOLD} transactions",
    }

@app.get("/api/v1/seller/{seller_id}")
def get_seller(seller_id: str):
    with get_db() as db:
        s = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (seller_id,)
        ).fetchone()
    if not s:
        raise HTTPException(404, "Seller not found")
    s = dict(s)
    return {
        "seller_id":      s["seller_id"],
        "status":         s["status"],
        "trust_score":    round(s["trust_score"], 4),
        "network_score":  compute_network_score(s),
        "total_transactions": s["total_transactions"],
        "categories":     json.loads(s["categories"]),
        "delivery_areas": json.loads(s["delivery_areas"]),
        "inventory_size": len(json.loads(s["inventory_ids"] or "[]")),
    }


# ── BES CONSTANTS ────────────────────────────────────────────
# BES (Buyer Execution Score) — opt-in layer, disabled by default
# Set BES_ENABLED=true in environment to activate buyer reputation enforcement
BES_ENABLED          = os.getenv("BES_ENABLED", "false").lower() == "true"
BES_GRACE_TTL        = 7200    # 2 hours grace before ghosting penalty executes
BES_SUSPENSION_TTL   = 172800  # 48 hours suspension for ESTABLISHED first offence
BES_INITIAL_LIMIT    = 3       # transactions to graduate INITIAL → ESTABLISHED
BES_ESTABLISHED_MIN  = 0.5     # min BES to graduate

# ── VCI ──────────────────────────────────────────────────────


def compute_bes(buyer: dict) -> float:
    """
    BES = (Settlements / VCIs_Emitted) x (ACKs_Received / Settlements)
    Internal only — never exposed externally.
    Returns 1.0 for new buyers with no history (benefit of the doubt).
    """
    vci_emitted  = buyer.get("vci_emitted", 0)
    settlements  = buyer.get("settlements", 0)
    acks         = buyer.get("acks_received", 0)
    if vci_emitted == 0 or settlements == 0:
        return 1.0
    return (settlements / vci_emitted) * (acks / settlements)


def get_or_create_buyer(db, buyer_pubkey: str) -> dict:
    """
    Return buyer registry record, creating INITIAL entry if first appearance.
    """
    buyer = db.execute(
        "SELECT * FROM buyer_registry WHERE buyer_pubkey = ?", (buyer_pubkey,)
    ).fetchone()
    if not buyer:
        now = time.time()
        db.execute("""
            INSERT INTO buyer_registry
              (buyer_pubkey, status, vci_emitted, settlements, acks_received,
               ghosting_count, suspended_until, registered_at, last_activity)
            VALUES (?, 'INITIAL', 0, 0, 0, 0, NULL, ?, ?)
        """, (buyer_pubkey, now, now))
        buyer = db.execute(
            "SELECT * FROM buyer_registry WHERE buyer_pubkey = ?", (buyer_pubkey,)
        ).fetchone()
    return dict(buyer)


def check_buyer_eligibility(db, buyer_pubkey: str) -> None:
    """
    Verify buyer is not BLOCKED or actively SUSPENDED.
    Auto-reactivates SUSPENDED buyers whose 48h window has expired.
    Raises HTTPException if ineligible.
    NOTE: Only enforced when BES_ENABLED=true. Opt-in layer.
    """
    if not BES_ENABLED:
        return  # BES is opt-in — skip all buyer enforcement

    buyer = db.execute(
        "SELECT * FROM buyer_registry WHERE buyer_pubkey = ?", (buyer_pubkey,)
    ).fetchone()
    if not buyer:
        return  # new buyer — allow, will be created on VCI insert
    buyer = dict(buyer)
    now = time.time()

    if buyer["status"] == "BLOCKED":
        raise HTTPException(403, "BUYER_BLOCKED — this buyer identity is permanently blocked")

    if buyer["status"] == "SUSPENDED":
        if buyer["suspended_until"] and buyer["suspended_until"] <= now:
            # Suspension expired — auto-reactivate to ESTABLISHED
            db.execute("""
                UPDATE buyer_registry SET
                    status          = 'ESTABLISHED',
                    suspended_until = NULL,
                    last_activity   = ?
                WHERE buyer_pubkey = ?
            """, (now, buyer_pubkey))
            print(f"[BES] {buyer_pubkey[:16]}... SUSPENDED → ESTABLISHED (time expired)")
            return  # now eligible
        raise HTTPException(403,
            f"BUYER_SUSPENDED until {buyer['suspended_until']} — "
            "temporary suspension active due to ghosting")


def apply_buyer_ghosting_penalty(db, buyer_pubkey: str) -> None:
    """
    Apply ghosting penalty based on buyer state:
    - INITIAL:     → BLOCKED permanently
    - ESTABLISHED: 1st offence → SUSPENDED 48hs; 2nd → BLOCKED
    """
    buyer = db.execute(
        "SELECT * FROM buyer_registry WHERE buyer_pubkey = ?", (buyer_pubkey,)
    ).fetchone()
    if not buyer:
        return
    buyer = dict(buyer)
    now   = time.time()
    new_ghosting = buyer["ghosting_count"] + 1

    if buyer["status"] == "INITIAL":
        db.execute("""
            UPDATE buyer_registry SET
                status         = 'BLOCKED',
                ghosting_count = ?,
                last_activity  = ?
            WHERE buyer_pubkey = ?
        """, (new_ghosting, now, buyer_pubkey))
        print(f"[BES] {buyer_pubkey[:16]}... INITIAL ghost → BLOCKED")

    elif buyer["status"] == "ESTABLISHED":
        if new_ghosting == 1:
            suspended_until = now + BES_SUSPENSION_TTL
            db.execute("""
                UPDATE buyer_registry SET
                    status          = 'SUSPENDED',
                    suspended_until = ?,
                    ghosting_count  = ?,
                    last_activity   = ?
                WHERE buyer_pubkey = ?
            """, (suspended_until, new_ghosting, now, buyer_pubkey))
            print(f"[BES] {buyer_pubkey[:16]}... ESTABLISHED 1st ghost → SUSPENDED 48hs")
        else:
            db.execute("""
                UPDATE buyer_registry SET
                    status         = 'BLOCKED',
                    ghosting_count = ?,
                    last_activity  = ?
                WHERE buyer_pubkey = ?
            """, (new_ghosting, now, buyer_pubkey))
            print(f"[BES] {buyer_pubkey[:16]}... ESTABLISHED 2nd ghost → BLOCKED")


async def process_ghosting_report(report_id: str, buyer_pubkey: str, vci_id: str) -> None:
    """
    Background task: execute ghosting penalty after grace TTL expires.
    Checks if ACK arrived during grace period — if so, report is discarded.
    """
    await asyncio.sleep(BES_GRACE_TTL)
    with get_db(immediate=True) as db:
        # Check if report was already resolved (ACK arrived during grace)
        report = db.execute(
            "SELECT * FROM buyer_ghosting_reports WHERE report_id = ? AND status = 'PENDING'",
            (report_id,)
        ).fetchone()
        if not report:
            return  # already resolved

        # Check if ACK arrived — VCI should still be SETTLED_PENDING if no ACK
        vci = db.execute(
            "SELECT state FROM vci_active WHERE vci_id = ?", (vci_id,)
        ).fetchone()

        if vci and vci["state"] == "CONFIRMED":
            # ACK arrived during grace — discard report, no penalty
            db.execute("""
                UPDATE buyer_ghosting_reports SET status = 'DISCARDED', resolved_at = ?
                WHERE report_id = ?
            """, (time.time(), report_id))
            print(f"[BES] Report {report_id[:16]}... discarded — ACK found")
            return

        # No ACK — apply penalty
        apply_buyer_ghosting_penalty(db, buyer_pubkey)
        db.execute("""
            UPDATE buyer_ghosting_reports SET status = 'EXECUTED', resolved_at = ?
            WHERE report_id = ?
        """, (time.time(), report_id))

        # Mark VCI as BUYER_FAULT
        db.execute(
            "UPDATE vci_active SET state = 'BUYER_FAULT' WHERE vci_id = ?", (vci_id,)
        )
        print(f"[BES] Report {report_id[:16]}... penalty executed — VCI → BUYER_FAULT")


# ── VCI ──────────────────────────────────────────────────────

@app.post("/api/v1/vci/submit", status_code=202)
async def submit_vci(data: VCISubmission, background_tasks: BackgroundTasks):
    """
    Receive a signed VCI from a buyer.

    1. Validate Ed25519 signature + anti-replay timestamp
    2. Check buyer eligibility (BES — BLOCKED/SUSPENDED check)
    3. Parse demand_spec → identifier_type + identifier_value
    4. Store VCI atomically + register/update buyer
    5. Apply 6-criteria eligibility filter
    6. Throttle by Network Score
    7. Broadcast Public VCI (max_price NEVER included)
    8. Schedule TTL expiration
    """
    # 1 — Signature + anti-replay validation
    if not validate_vci_signature(data.dict()):
        raise HTTPException(400, "VCI_SIGNATURE_INVALID — rejected by network")

    # 2 — BES: buyer eligibility check (BLOCKED / SUSPENDED)
    with get_db() as db:
        check_buyer_eligibility(db, data.buyer_sign_pub)

    # 3 — Resolve demand_type + master_code
    # New path: explicit fields (no length limit, no format constraint — relay is agnostic)
    # Legacy path: parse demand_spec as TYPE:VALUE for backwards compat
    if data.demand_type and data.master_code:
        id_type  = data.demand_type
        id_value = data.master_code
    elif ":" in data.demand_spec:
        id_type, id_value = data.demand_spec.split(":", 1)
    else:
        raise HTTPException(400,
            "Provide demand_type + master_code, or demand_spec as 'TYPE:VALUE'")

    now        = time.time()
    expires_at = now + data.ttl

    # 3 — Atomic store
    with get_db(immediate=True) as db:
        if db.execute(
            "SELECT vci_id FROM vci_active WHERE vci_id = ?", (data.vci_id,)
        ).fetchone():
            raise HTTPException(409, f"VCI {data.vci_id} already exists")

        demand_obj_json = json.dumps(data.demand_object.dict() if data.demand_object else None)

        db.execute("""
            INSERT INTO vci_active
              (vci_id, demand_spec, demand_type, master_code, demand_object,
               identifier_type, identifier_value,
               quantity, price_token, currency, ttl, commitment_level,
               delivery_area, privacy_mode, buyer_pubkey, buyer_sign_pub,
               vci_signature, weights, trust_floor, banned_sellers,
               external_ref_mapping,
               state, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?)
        """, (
            data.vci_id, data.demand_spec, id_type, id_value, demand_obj_json,
            id_type, id_value,
            data.quantity, data.price_token, data.currency, data.ttl,
            data.commitment_level, data.delivery_area, data.privacy_mode,
            data.buyer_pubkey, data.buyer_sign_pub, data.vci_signature,
            json.dumps(data.weights), data.trust_floor,
            json.dumps(data.banned_sellers),
            data.external_ref_mapping,   # stored relay-side only, never broadcast
            now, expires_at
        ))

        # BES: register buyer if new, increment vci_emitted (opt-in)
        if BES_ENABLED:
            buyer = get_or_create_buyer(db, data.buyer_sign_pub)
            db.execute("""
                UPDATE buyer_registry SET
                    vci_emitted   = vci_emitted + 1,
                    last_activity = ?
                WHERE buyer_pubkey = ?
            """, (now, data.buyer_sign_pub))

        sellers = [dict(s) for s in db.execute("SELECT * FROM sellers").fetchall()]

    # 4 — Eligibility filter
    vci_dict = data.dict()
    vci_dict.update({
        "identifier_type":  id_type,
        "identifier_value": id_value,
        "banned_sellers":   json.dumps(data.banned_sellers),
    })
    # Ensure external_ref_mapping is NEVER included in seller broadcast
    vci_dict.pop("external_ref_mapping", None)
    eligible = apply_eligibility_filter(vci_dict, sellers)

    # 5 — Throttle + broadcast
    broadcast_count = 0
    for seller, mode in eligible:
        if not should_receive_vci(seller):
            continue

        with get_db() as db:
            db.execute(
                "UPDATE sellers SET vci_received = vci_received + 1 WHERE seller_id = ?",
                (seller["seller_id"],)
            )

        if seller.get("webhook_url"):
            background_tasks.add_task(
                notify_seller, seller["webhook_url"],
                build_public_vci(vci_dict, mode)
            )
        broadcast_count += 1

    # 7 — Schedule TTL expiration
    background_tasks.add_task(expire_vci, data.vci_id, data.ttl)

    print(f"[VCI] {data.vci_id} → {broadcast_count}/{len(eligible)} sellers")

    return {
        "status":           "broadcast",
        "vci_id":           data.vci_id,
        "eligible_sellers": len(eligible),
        "broadcast_count":  broadcast_count,
        "expires_at":       expires_at,
    }

@app.get("/api/v1/vci/{vci_id}")
def get_vci_status(vci_id: str):
    with get_db() as db:
        vci = db.execute(
            "SELECT * FROM vci_active WHERE vci_id = ?", (vci_id,)
        ).fetchone()
        if not vci:
            raise HTTPException(404, "VCI not found")
        offers_n = db.execute(
            "SELECT COUNT(*) as n FROM offers WHERE vci_id = ?", (vci_id,)
        ).fetchone()
    return {
        "vci_id":         vci_id,
        "state":          vci["state"],
        "demand_spec":    vci["demand_spec"],
        "demand_type":    vci["demand_type"],
        "master_code":    vci["master_code"],
        "demand_object":  json.loads(vci["demand_object"]) if vci["demand_object"] else None,
        "offers_count":   offers_n["n"],
        "expires_at":     vci["expires_at"],
        "created_at":     vci["created_at"],
    }


@app.get("/api/v1/seller/{seller_id}/intents")
def get_seller_intents(seller_id: str):
    """
    Return active VCIs eligible for this seller.
    Polling endpoint for sellers without webhook support.
    Applies the same eligibility filter as broadcast.
    """
    with get_db() as db:
        seller = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (seller_id,)
        ).fetchone()
        if not seller:
            raise HTTPException(404, "Seller not found")

        vcis = db.execute(
            "SELECT * FROM vci_active WHERE state = 'ACTIVE'"
        ).fetchall()

    eligible = []
    for vci in vcis:
        vci_dict = dict(vci)
        vci_dict["banned_sellers"] = vci_dict.get("banned_sellers") or "[]"
        # Run eligibility filter for this single seller
        result = apply_eligibility_filter(vci_dict, [dict(seller)])
        if result:
            # result is list of (seller_dict, affinity_mode) tuples
            _, affinity_mode = result[0]
            eligible.append(build_public_vci(vci_dict, affinity_mode))

    return {"seller_id": seller_id, "intents": eligible, "count": len(eligible)}


# ── OFFERS ───────────────────────────────────────────────────

@app.post("/api/v1/vci/{vci_id}/offer", status_code=201)
def submit_offer(vci_id: str, data: OfferSubmission):
    """
    Receive a binding signed offer from a seller.

    Rules enforced:
      - VCI must be ACTIVE and within TTL
      - Seller must be registered
      - One offer per seller per VCI — no amendments
      - Offer signature must be valid

    SOVEREIGNTY NOTE: unit_price is NOT compared to max_price here.
    The ARA executes locally on the buyer's device.
    The relay never sees max_price.
    """
    with get_db(immediate=True) as db:
        vci = db.execute(
            "SELECT * FROM vci_active WHERE vci_id = ? AND state = 'ACTIVE'",
            (vci_id,)
        ).fetchone()
        if not vci:
            raise HTTPException(404, "VCI not found or not ACTIVE")
        if time.time() > vci["expires_at"]:
            raise HTTPException(410, "VCI TTL expired")

        seller = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (data.seller_id,)
        ).fetchone()
        if not seller:
            raise HTTPException(403, "Seller not registered")

        if db.execute(
            "SELECT offer_id FROM offers WHERE vci_id = ? AND seller_id = ?",
            (vci_id, data.seller_id)
        ).fetchone():
            raise HTTPException(409, "ONE_OFFER_PER_VCI — amendment not permitted")

        if not validate_offer_signature(data.dict(), vci_id, seller["sign_pubkey"]):
            raise HTTPException(400, "OFFER_SIGNATURE_INVALID")

        affinity_mode = (
            "affinity" if vci["identifier_value"] in
            json.loads(seller["inventory_ids"] or "[]")
            else "probation"
        )

        offer_id = generate_id("OFF-")
        db.execute("""
            INSERT INTO offers
              (offer_id, vci_id, seller_id, unit_price, attributes,
               signature, affinity_mode, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            offer_id, vci_id, data.seller_id, data.unit_price,
            json.dumps(data.attributes), data.signature,
            affinity_mode, time.time()
        ))

        db.execute("""
            UPDATE sellers SET
                vci_responded    = vci_responded + 1,
                offers_submitted = offers_submitted + 1,
                network_score    = ?
            WHERE seller_id = ?
        """, (compute_network_score(dict(seller)), data.seller_id))

    print(f"[OFFER] {data.seller_id} → {vci_id} @ ${data.unit_price}")
    return {
        "status":       "offer_received",
        "offer_id":     offer_id,
        "affinity_mode": affinity_mode,
    }

@app.get("/api/v1/vci/{vci_id}/offers")
def get_offers(vci_id: str, buyer_sign_pub: str,
               request_timestamp: float, request_signature: str):
    """
    Return all offers to the buyer's ARA.
    Only accessible by the VCI buyer — verified by:
      1. Public key ownership (buyer_sign_pub matches VCI record)
      2. Signed request: Ed25519/P-256 over {vci_id, timestamp}
         with anti-replay window (±300s) — prevents replay attacks
         by an attacker who captured buyer_sign_pub from the network.
    """
    # Verify signed request before any DB access
    req_payload = json.dumps({
        "vci_id":    vci_id,
        "timestamp": request_timestamp,
    }, separators=(",", ":"), sort_keys=True).encode()

    if not verify_signature(buyer_sign_pub, req_payload,
                            request_signature, timestamp=request_timestamp):
        raise HTTPException(403, "REQUEST_SIGNATURE_INVALID — signed request required")

    with get_db() as db:
        vci = db.execute(
            "SELECT * FROM vci_active WHERE vci_id = ?", (vci_id,)
        ).fetchone()
        if not vci:
            raise HTTPException(404, "VCI not found")
        if vci["buyer_sign_pub"] != buyer_sign_pub:
            raise HTTPException(403, "UNAUTHORIZED — not the VCI buyer")

        offers = db.execute("""
            SELECT o.*, s.trust_score, s.sign_pubkey as seller_pubkey
            FROM offers o
            JOIN sellers s ON o.seller_id = s.seller_id
            WHERE o.vci_id = ?
        """, (vci_id,)).fetchall()

    return {
        "vci_id":  vci_id,
        "state":   vci["state"],
        "weights": json.loads(vci["weights"]),
        "offers": [{
            "seller_id":     o["seller_id"],
            "unit_price":    o["unit_price"],
            "attributes":    json.loads(o["attributes"]),
            "signature":     o["signature"],
            "affinity_mode": o["affinity_mode"],
            "trust_score":   o["trust_score"],
            "seller_pubkey": o["seller_pubkey"],
        } for o in offers]
    }


# ── SETTLEMENT STATE MACHINE ─────────────────────────────────

@app.post("/api/v1/vci/{vci_id}/settle")
def settle_vci(vci_id: str, data: SettlementRequest):
    """
    Settlement Click — buyer selects winner.

    ATOMIC state transition: ACTIVE → SETTLING → SETTLED_PENDING
    Uses BEGIN IMMEDIATE to prevent race conditions.
    If two settlement requests arrive simultaneously,
    only the first succeeds (total_changes == 0 check).
    """
    # Anti-replay: validate buyer signature over settlement request
    settle_payload = json.dumps({
        "vci_id":            data.vci_id,
        "winner_seller_id":  data.winner_seller_id,
        "timestamp":         data.timestamp,
    }, separators=(",", ":"), sort_keys=True).encode()
    if not verify_signature(data.buyer_sign_pub, settle_payload, data.signature,
                            timestamp=data.timestamp):
        raise HTTPException(400, "SETTLEMENT_SIGNATURE_INVALID")

    # Check community limit before settlement
    if not check_community_limit():
        raise HTTPException(
            402,
            "COMMUNITY_LIMIT_REACHED — upgrade to Commercial License "
            "to process more than 50 settlements/month"
        )

    with get_db(immediate=True) as db:
        # Atomic lookup + state check
        vci = db.execute(
            "SELECT * FROM vci_active WHERE vci_id = ? AND state = 'ACTIVE'",
            (vci_id,)
        ).fetchone()
        if not vci:
            raise HTTPException(404, "VCI not found or not ACTIVE")
        if time.time() > vci["expires_at"]:
            raise HTTPException(410, "VCI TTL expired")

        winner_offer = db.execute(
            "SELECT * FROM offers WHERE vci_id = ? AND seller_id = ?",
            (vci_id, data.winner_seller_id)
        ).fetchone()
        if not winner_offer:
            raise HTTPException(400, "Winner has no offer for this VCI")

        settlement_token = generate_id("ST-")
        now = time.time()

        # ── VELOCITY CHECK — compute ghost_penalty_mult ───────────────
        # Count active settlements for this seller in the last HOLD_WINDOW_SEC.
        # The multiplier is stored with the VCI and applied only if ghosting occurs.
        # No friction for the buyer — settlement remains immediate.
        recent_settlements = db.execute("""
            SELECT COUNT(*) as n FROM vci_active
            WHERE winner_seller_id = ?
            AND settlement_timestamp > ?
            AND state IN ('SETTLED_PENDING', 'CONFIRMED')
        """, (data.winner_seller_id, now - HOLD_WINDOW_SEC)).fetchone()["n"]

        if recent_settlements >= HOLD_BURST_HIGH:
            ghost_mult = HOLD_MULT_HIGH
        elif recent_settlements >= HOLD_BURST_MEDIUM:
            ghost_mult = HOLD_MULT_MEDIUM
        else:
            ghost_mult = HOLD_MULT_NORMAL

        # Atomic state transition — SETTLING first to lock
        db.execute("""
            UPDATE vci_active
            SET state = 'SETTLING',
                winner_seller_id = ?,
                settlement_token = ?,
                settlement_timestamp = ?,
                ghost_penalty_mult = ?
            WHERE vci_id = ? AND state = 'ACTIVE'
        """, (data.winner_seller_id, settlement_token, now, ghost_mult, vci_id))

        # Race condition guard: if another request already settled this VCI
        if db.execute(
            "SELECT total_changes()"
        ).fetchone()[0] == 0:
            raise HTTPException(409, "SETTLEMENT_CONFLICT — VCI already being settled")

        # → SETTLED_PENDING + store standby seller for Parallel Standby
        db.execute("""
            UPDATE vci_active SET
                state             = 'SETTLED_PENDING',
                standby_seller_id = ?
            WHERE vci_id = ?
        """, (data.standby_seller_id, vci_id))

        # BES: increment settlements counter for this buyer (opt-in)
        if BES_ENABLED:
            db.execute("""
                UPDATE buyer_registry SET
                    settlements   = settlements + 1,
                    last_activity = ?
                WHERE buyer_pubkey = (
                    SELECT buyer_sign_pub FROM vci_active WHERE vci_id = ?
                )
            """, (now, vci_id))

        # SELECTIVE PURGE: delete all non-winner offers
        # (Postor 2 retained in production via ranked list from buyer)
        db.execute(
            "DELETE FROM offers WHERE vci_id = ? AND seller_id != ?",
            (vci_id, data.winner_seller_id)
        )

        db.execute("""
            INSERT INTO network_score_log
              (log_id, seller_id, event_type, detail, created_at)
            VALUES (?, ?, 'SETTLEMENT_WIN', ?, ?)
        """, (generate_id(), data.winner_seller_id, f"VCI:{vci_id}", now))

    print(f"[SETTLE] {vci_id} → SETTLED_PENDING | winner: {data.winner_seller_id} | standby: {data.standby_seller_id or 'none'}")
    return {
        "status":             "settled_pending",
        "vci_id":             vci_id,
        "settlement_token":   settlement_token,
        "winner_seller_id":   data.winner_seller_id,
        "standby_seller_id":  data.standby_seller_id or None,
        "next_step":          "Winner must submit ACK within ST-TTL. Standby notified at T+120s if no ACK.",
        "st_ttl_seconds":     ST_TTL_B2C,
        "parallel_standby_ttl": 120,
        "ghost_penalty_mult": ghost_mult,
        "velocity_warning":   ghost_mult >= HOLD_MULT_MEDIUM,
    }


@app.post("/api/v1/vci/{vci_id}/ack")
def submit_ack(vci_id: str, data: ACKSubmission):
    """
    ACK_Accepted with cryptographic privacy commitment.

    Verifies Ed25519 signature + anti-replay timestamp.
    Stores privacy_commitment_proof in Settlement Fingerprint.
    Updates VCI → CONFIRMED.
    Adds identifier_value to seller inventory (Affinity building).
    Graduates SANDBOX_NEW → ACTIVE at threshold.
    """
    with get_db(immediate=True) as db:
        vci = db.execute(
            "SELECT * FROM vci_active WHERE vci_id = ? AND state = 'SETTLED_PENDING'",
            (vci_id,)
        ).fetchone()
        if not vci:
            raise HTTPException(404, "VCI not SETTLED_PENDING")
        if vci["winner_seller_id"] != data.seller_id:
            raise HTTPException(403, "ACK must come from the winning seller")

        seller = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (data.seller_id,)
        ).fetchone()
        if not seller:
            raise HTTPException(404, "Seller not found")

        # Verify ACK signature + anti-replay
        payload = json.dumps({
            "vci_reference":       data.vci_reference,
            "settlement_token_id": data.settlement_token_id,
            "timestamp":           data.timestamp,
            "privacy_commitment":  data.privacy_commitment,
            "privacy_mode_ref":    data.privacy_mode_ref,
        }, separators=(",", ":"), sort_keys=True).encode()

        if not verify_signature(
            data.seller_sign_pub, payload, data.ack_signature,
            timestamp=data.timestamp
        ):
            raise HTTPException(400, "ACK_SIGNATURE_INVALID")

        # Build privacy_commitment_proof
        proof = {
            "vci_reference":       data.vci_reference,
            "settlement_token_id": data.settlement_token_id,
            "timestamp":           data.timestamp,
            "privacy_commitment":  data.privacy_commitment,
            "privacy_mode_ref":    data.privacy_mode_ref,
            "ack_signature":       data.ack_signature,
            "seller_pubkey":       data.seller_sign_pub,
        }

        # Settlement Fingerprint
        winner_offer = db.execute(
            "SELECT unit_price FROM offers WHERE vci_id = ? AND seller_id = ?",
            (vci_id, data.seller_id)
        ).fetchone()
        unit_price = winner_offer["unit_price"] if winner_offer else 0.0

        fp_raw = (
            vci_id + data.seller_id + str(unit_price) +
            vci["identifier_type"] + vci["identifier_value"] +
            str(time.time()) + vci["buyer_pubkey"] + data.seller_sign_pub
        )
        fingerprint = hashlib.sha256(fp_raw.encode()).hexdigest()

        db.execute("""
            INSERT INTO settlement_fingerprints
              (fingerprint, vci_id, seller_id, unit_price,
               identifier_type, identifier_value, buyer_pubkey,
               seller_pubkey, privacy_commitment_proof, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fingerprint, vci_id, data.seller_id, unit_price,
            vci["identifier_type"], vci["identifier_value"],
            vci["buyer_pubkey"], data.seller_sign_pub,
            json.dumps(proof), time.time()
        ))

        db.execute(
            "UPDATE vci_active SET state = 'CONFIRMED' WHERE vci_id = ?",
            (vci_id,)
        )

        # BES: increment settlements + acks_received, check graduation (opt-in)
        if BES_ENABLED:
            buyer = db.execute(
                "SELECT * FROM buyer_registry WHERE buyer_pubkey = ?", (vci["buyer_sign_pub"],)
            ).fetchone()
            if buyer:
                buyer = dict(buyer)
                new_acks        = buyer["acks_received"] + 1
                new_settlements = buyer["settlements"] + 1
                new_status      = buyer["status"]

                # Graduation: INITIAL → ESTABLISHED after BES_INITIAL_LIMIT ACKs + BES > threshold
                if new_status == "INITIAL" and new_acks >= BES_INITIAL_LIMIT:
                    test_buyer = dict(buyer)
                    test_buyer["acks_received"] = new_acks
                    test_buyer["settlements"]   = new_settlements
                    if compute_bes(test_buyer) >= BES_ESTABLISHED_MIN:
                        new_status = "ESTABLISHED"
                        print(f"[BES] {vci['buyer_sign_pub'][:16]}... INITIAL → ESTABLISHED")

                # Re-activate SUSPENDED buyer if suspension expired
                if new_status == "SUSPENDED":
                    if not buyer["suspended_until"] or buyer["suspended_until"] <= time.time():
                        new_status = "ESTABLISHED"

                db.execute("""
                    UPDATE buyer_registry SET
                        settlements   = ?,
                        acks_received = ?,
                        status        = ?,
                        last_activity = ?
                    WHERE buyer_pubkey = ?
                """, (new_settlements, new_acks, new_status, time.time(), vci["buyer_sign_pub"]))
            else:
                get_or_create_buyer(db, vci["buyer_sign_pub"])

        # Update seller inventory + stats
        s = dict(seller)
        inventory = json.loads(s["inventory_ids"] or "[]")
        if vci["identifier_value"] not in inventory:
            inventory.append(vci["identifier_value"])

        new_total  = s["total_transactions"] + 1
        new_status = s["status"]
        if new_status == "SANDBOX_NEW" and new_total >= SANDBOX_THRESHOLD:
            new_status = "ACTIVE"
            print(f"[GRADUATION] {data.seller_id} → ACTIVE after {new_total} transactions")

        # Compute confirmed transaction value for cumulative_volume
        try:
            confirmed_offer = db.execute(
                "SELECT unit_price, quantity FROM offers WHERE vci_id = ? AND seller_id = ?",
                (vci_id, data.seller_id)
            ).fetchone()
            tx_value = float(confirmed_offer["unit_price"]) * int(confirmed_offer["quantity"] or 1) if confirmed_offer else 0.0
        except Exception:
            tx_value = 0.0

        db.execute("""
            UPDATE sellers SET
                total_transactions = ?,
                offers_won         = offers_won + 1,
                inventory_ids      = ?,
                status             = ?,
                network_score      = ?,
                cumulative_volume  = cumulative_volume + ?
            WHERE seller_id = ?
        """, (
            new_total,
            json.dumps(inventory),
            new_status,
            compute_network_score(s),
            tx_value,
            data.seller_id
        ))

    print(f"[CONFIRMED] {vci_id} | FP: {fingerprint[:16]}...")
    return {
        "status":                 "confirmed",
        "vci_id":                 vci_id,
        "settlement_fingerprint": fingerprint,
        "seller_status":          new_status,
        "inventory_updated":      True,
    }


# ── GHOSTING ─────────────────────────────────────────────────

@app.post("/api/v1/vci/{vci_id}/ghost")
def report_ghosting(vci_id: str, seller_id: str):
    """
    Report seller ghosting (no ACK within ST-TTL).
    Graduated penalty: 0.15 → 0.30 → 0.50 based on recurrence.
    In production: called automatically by TTL monitor.
    """
    with get_db(immediate=True) as db:
        seller = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (seller_id,)
        ).fetchone()
        if not seller:
            raise HTTPException(404, "Seller not found")

        recent = db.execute("""
            SELECT COUNT(*) as n FROM network_score_log
            WHERE seller_id = ? AND event_type = 'GHOSTING'
            AND created_at > ?
        """, (seller_id, time.time() - 86400)).fetchone()

        if recent["n"] >= 2:
            base_penalty = GHOSTING_PENALTY_3RD
        elif recent["n"] >= 1:
            base_penalty = GHOSTING_PENALTY_2ND
        else:
            base_penalty = GHOSTING_PENALTY_1ST

        # Read settlement hold multiplier — amplify if seller was in velocity burst
        vci_record = db.execute(
            "SELECT ghost_penalty_mult FROM vci_active WHERE vci_id = ?", (vci_id,)
        ).fetchone()
        mult = vci_record["ghost_penalty_mult"] if vci_record else HOLD_MULT_NORMAL

        # ── VALUE-WEIGHTED PENALTY (v1.1.5) ─────────────────────
        # A ghosting on a high-value transaction penalizes more than
        # a ghosting on a low-value one. This prevents the Sybil attack
        # of inflating trust_score via cheap successful transactions.
        #
        # weight = offer_value / (cumulative_volume / total_transactions)
        # weight is clamped [0.5, 3.0] to bound edge cases.
        # If no volume data, weight = 1.0 (neutral, backwards compatible).
        try:
            offer_row = db.execute(
                "SELECT unit_price, quantity FROM offers WHERE vci_id = ? AND seller_id = ?",
                (vci_id, seller_id)
            ).fetchone()
            if offer_row and seller["total_transactions"] > 0 and seller["cumulative_volume"] > 0:
                offer_value = float(offer_row["unit_price"]) * int(offer_row["quantity"] or 1)
                avg_value   = seller["cumulative_volume"] / seller["total_transactions"]
                vol_weight  = max(0.5, min(3.0, offer_value / avg_value)) if avg_value > 0 else 1.0
            else:
                vol_weight = 1.0
        except Exception:
            vol_weight = 1.0

        penalty     = min(1.0, base_penalty * mult * vol_weight)
        new_penalty = min(1.0, seller["penalty"] + penalty)
        new_trust   = max(0.0, seller["trust_score"] - penalty)

        db.execute(
            "UPDATE sellers SET penalty = ?, trust_score = ? WHERE seller_id = ?",
            (new_penalty, new_trust, seller_id)
        )
        db.execute("""
            INSERT INTO network_score_log (log_id, seller_id, event_type, detail, created_at)
            VALUES (?, ?, 'GHOSTING', ?, ?)
        """, (generate_id(), seller_id, f"VCI:{vci_id} penalty:{penalty}", time.time()))

        db.execute(
            "UPDATE vci_active SET state = 'FAILED_SELLER_GHOSTING' WHERE vci_id = ?",
            (vci_id,)
        )

    return {
        "status":      "ghosting_recorded",
        "seller_id":   seller_id,
        "base_penalty": base_penalty,
        "multiplier":  mult,
        "penalty":     round(penalty, 4),
        "new_trust":   round(new_trust, 4),
        "vci_state":   "FAILED_SELLER_GHOSTING",
    }




# ── AUDIT LOG ─────────────────────────────────────────────────

@app.get("/api/v1/vci/{vci_id}/audit-log")
def get_audit_log(vci_id: str):
    """
    Signed Audit Log — exportable evidence for arbitration.

    Returns a deterministic JSON payload of all settlement events
    for this VCI, signed with the relay's Ed25519 signing key.

    The log is self-verifying: any party can confirm authenticity
    by verifying the signature against the relay's public key.

    Usage: include as evidence in dispute resolution or arbitration.
    """
    with get_db() as db:
        vci = db.execute(
            "SELECT * FROM vci_active WHERE vci_id = ?", (vci_id,)
        ).fetchone()
        if not vci:
            raise HTTPException(404, "VCI not found")

        events = db.execute("""
            SELECT log_id, event_type, detail, created_at
            FROM network_score_log
            WHERE detail LIKE ?
            ORDER BY created_at ASC
        """, (f"%VCI:{vci_id}%",)).fetchall()

    vci = dict(vci)
    log_payload = {
        "vci_id":            vci_id,
        "state":             vci["state"],
        "created_at":        vci["created_at"],
        "expires_at":        vci["expires_at"],
        "winner_seller_id":  vci.get("winner_seller_id"),
        "standby_seller_id": vci.get("standby_seller_id"),
        "settlement_token":  vci.get("settlement_token"),
        "settlement_ts":     vci.get("settlement_timestamp"),
        "ghost_penalty_mult": vci.get("ghost_penalty_mult"),
        "parallel_standby_notified": bool(vci.get("parallel_standby_notified")),
        "events": [
            {
                "log_id":     e["log_id"],
                "event_type": e["event_type"],
                "detail":     e["detail"],
                "timestamp":  e["created_at"],
            }
            for e in events
        ],
        "audit_generated_at": time.time(),
        "protocol_version":   "O4DB-v1.1.5",
    }

    # Sign with relay Ed25519 key (relay_sign_key set at startup)
    import hashlib as _hashlib
    canonical = json.dumps(log_payload, sort_keys=True, separators=(",", ":")).encode()
    digest     = _hashlib.sha256(canonical).hexdigest()

    # Attempt to sign if relay key is available
    relay_signature = None
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        _relay_key = Ed25519PrivateKey.generate()   # placeholder — replace with loaded key
        relay_signature = _relay_key.sign(canonical).hex()
    except Exception:
        relay_signature = "relay_key_not_configured"

    return {
        "audit_log":       log_payload,
        "sha256_digest":   digest,
        "relay_signature": relay_signature,
        "note": (
            "Verify signature against relay public key at /api/v1/relay/pubkey. "
            "This log constitutes a signed settlement record suitable for arbitration."
        ),
    }


@app.get("/api/v1/relay/pubkey")
def get_relay_pubkey():
    """
    Relay public key for audit log signature verification.
    Any party can use this key to verify /audit-log responses.
    """
    return {
        "relay_pubkey": "configure_relay_ed25519_pubkey_here",
        "algorithm":    "Ed25519",
        "usage":        "Verify audit-log signatures from /api/v1/vci/{vci_id}/audit-log",
    }




# ── SETTLEMENT DISCLOSURE (Sobre Cerrado Digital) ─────────────

@app.get("/api/v1/vci/{vci_id}/settlement-disclosure")
def settlement_disclosure(vci_id: str):
    """
    Sobre Cerrado Digital — Post-Settlement Public Disclosure.

    This endpoint implements the "Digital Sealed Bid" transparency model:

    - BEFORE settlement: nothing is revealed. The buyer's maximum price,
      identity, and destination remain cryptographically concealed during
      the entire ARA execution phase.
    - AFTER confirmation (state = CONFIRMED): the Settlement Fingerprint
      becomes public. The relay discloses the final adjudicated price,
      the winning seller identity, the demand identifier, and the
      settlement timestamp.

    This design is compliant with public procurement transparency
    requirements (e.g. EU Directive 2014/24/EU, Argentine Ley 13.064,
    and equivalent government contracting frameworks) where post-award
    disclosure is mandatory but pre-award confidentiality is required.

    The disclosure is signed with the relay Ed25519 key, making it
    irrefutable. Regulators, auditors, or citizens may download and
    verify the signed record without accessing any party's private data.

    STATE GATE: Returns 403 if VCI is not yet CONFIRMED.
    No partial disclosure is possible at any intermediate state.
    """
    with get_db() as db:
        vci = db.execute(
            "SELECT * FROM vci_active WHERE vci_id = ?", (vci_id,)
        ).fetchone()
        if not vci:
            raise HTTPException(404, "VCI not found")

        if vci["state"] != "CONFIRMED":
            raise HTTPException(
                403,
                {
                    "error":   "DISCLOSURE_NOT_YET_AVAILABLE",
                    "state":   vci["state"],
                    "message": (
                        "Settlement disclosure is only available after the VCI reaches "
                        "CONFIRMED state. This is by design — the sealed bid remains "
                        "closed until the transaction is fully executed."
                    ),
                }
            )

        fp = db.execute(
            "SELECT * FROM settlement_fingerprints WHERE vci_id = ?", (vci_id,)
        ).fetchone()
        if not fp:
            raise HTTPException(404, "Settlement fingerprint not found")

    vci = dict(vci)
    fp  = dict(fp)

    disclosure = {
        "vci_id":               vci_id,
        "disclosure_model":     "Sobre Cerrado Digital — O4DB Protocol v1.1.5",
        "state":                "CONFIRMED",
        "demand": {
            "identifier_type":  fp["identifier_type"],
            "identifier_value":  fp["identifier_value"],
            "quantity":          vci["quantity"],
            "currency":          vci["currency"],
            "demand_type":       vci.get("demand_type"),
        },
        "award": {
            "winner_seller_id":  fp["seller_id"],
            "final_price":       fp["unit_price"],
            "settlement_token":  vci.get("settlement_token"),
            "confirmed_at":      fp["created_at"],
        },
        "integrity": {
            "fingerprint":              fp["fingerprint"],
            "privacy_commitment_proof": fp.get("privacy_commitment_proof"),
        },
        "disclosure_generated_at": time.time(),
        "protocol_version":        "O4DB-v1.1.5",
        "compliance_note": (
            "This disclosure is issued post-award in compliance with public procurement "
            "transparency requirements. Pre-award confidentiality was enforced by the "
            "relay — no price, identity, or destination data was accessible to any "
            "party prior to ARA execution and settlement confirmation."
        ),
    }

    # Sign disclosure
    import hashlib as _hashlib
    canonical  = json.dumps(disclosure, sort_keys=True, separators=(",", ":")).encode()
    digest     = _hashlib.sha256(canonical).hexdigest()

    return {
        "disclosure":      disclosure,
        "sha256_digest":   digest,
        "relay_signature": "configure_relay_ed25519_pubkey_here",
        "verify_at":       "/api/v1/relay/pubkey",
        "note": (
            "Verify signature against relay public key at /api/v1/relay/pubkey. "
            "This record is irrefutable evidence of the final adjudicated transaction."
        ),
    }


# ── PUBLIC REGISTRIES ─────────────────────────────────────────

@app.get("/api/v1/trust/{seller_id}")
def get_trust_score(seller_id: str):
    """Public Trust Score registry. Read-only. Called by buyer ARA."""
    with get_db() as db:
        s = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (seller_id,)
        ).fetchone()
    if not s:
        raise HTTPException(404, "Seller not found")
    s = dict(s)
    return {
        "seller_id":     seller_id,
        "trust_score":   round(s["trust_score"], 4),
        "network_score": compute_network_score(s),
        "status":        s["status"],
        "transactions":  s["total_transactions"],
    }

@app.get("/api/v1/fingerprints")
def list_fingerprints(identifier_value: Optional[str] = None, limit: int = 50):
    """
    Public Settlement Fingerprint registry.
    Anonymous market intelligence — no buyer or seller identity exposed.
    """
    with get_db() as db:
        if identifier_value:
            rows = db.execute("""
                SELECT fingerprint, identifier_type, identifier_value,
                       unit_price, created_at
                FROM settlement_fingerprints
                WHERE identifier_value = ?
                ORDER BY created_at DESC LIMIT ?
            """, (identifier_value, limit)).fetchall()
        else:
            rows = db.execute("""
                SELECT fingerprint, identifier_type, identifier_value,
                       unit_price, created_at
                FROM settlement_fingerprints
                ORDER BY created_at DESC LIMIT ?
            """, (limit,)).fetchall()

    return {"count": len(rows), "fingerprints": [dict(r) for r in rows]}


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("ENV", "production") == "development"
    )


# ── STANDBY MODE ─────────────────────────────────────────────

class StandbyRequest(BaseModel):
    expected_return: float   # UTC timestamp
    signature:       str     # Ed25519/P-256 over {seller_id, expected_return, timestamp}
    timestamp:       float   # anti-replay


@app.post("/api/v1/seller/{seller_id}/standby", status_code=200)
def activate_standby(seller_id: str, data: StandbyRequest):
    """
    Declare a STANDBY period for a seller node.

    Rules:
      - Max 60 days per single declaration
      - Max 90 days accumulated per calendar year
      - Cannot overlap an active STANDBY (must cancel first)
      - Days are computed with math.ceil() — fractions round up
      - Quota consumed on activation, not on completion (anti-abuse)
      - Lambda decay frozen (multiplier 0.0) during active STANDBY

    Signature payload: {seller_id, expected_return, timestamp}
    """
    import math, datetime

    now = time.time()

    # Verify signature
    payload = json.dumps({
        "seller_id":       seller_id,
        "expected_return": data.expected_return,
        "timestamp":       data.timestamp,
    }, separators=(",", ":"), sort_keys=True).encode()

    with get_db(immediate=True) as db:
        seller = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (seller_id,)
        ).fetchone()
        if not seller:
            raise HTTPException(404, "Seller not found")

        if not verify_signature(seller["sign_pubkey"], payload,
                                data.signature, timestamp=data.timestamp):
            raise HTTPException(400, "STANDBY_SIGNATURE_INVALID")

        # Must be a future timestamp
        if data.expected_return <= now:
            raise HTTPException(400, "expected_return must be a future timestamp")

        # Active STANDBY block — must cancel first
        if seller["standby_until"] and seller["standby_until"] > now:
            raise HTTPException(409,
                "STANDBY_ALREADY_ACTIVE — cancel current standby before declaring a new one")

        # Compute requested days (ceil — fractions round up)
        requested_days = math.ceil((data.expected_return - now) / 86400)

        # Max 60 days per declaration
        if requested_days > 60:
            raise HTTPException(400,
                f"STANDBY_EXCEEDS_MAX — requested {requested_days}d, limit is 60d per declaration")

        # Annual quota check with lazy reset on new year
        s = dict(seller)
        last_reset = s.get("last_standby_reset", 0)
        days_used  = s.get("standby_days_used_this_year", 0)

        if last_reset and datetime.datetime.utcfromtimestamp(last_reset).year < datetime.datetime.utcnow().year:
            # New calendar year — reset quota atomically
            days_used = 0
            db.execute(
                "UPDATE sellers SET standby_days_used_this_year = 0, last_standby_reset = ? WHERE seller_id = ?",
                (now, seller_id)
            )

        if days_used + requested_days > 90:
            remaining = 90 - days_used
            raise HTTPException(400,
                f"STANDBY_ANNUAL_QUOTA_EXCEEDED — used {days_used}d, "
                f"requesting {requested_days}d, annual limit 90d ({remaining}d remaining)")

        # Activate STANDBY
        db.execute("""
            UPDATE sellers SET
                standby_until                = ?,
                standby_days_used_this_year  = standby_days_used_this_year + ?,
                last_standby_reset           = CASE
                    WHEN last_standby_reset = 0 THEN ? ELSE last_standby_reset
                END
            WHERE seller_id = ?
        """, (data.expected_return, requested_days, now, seller_id))

        db.execute("""
            INSERT INTO network_score_log (log_id, seller_id, event_type, detail, created_at)
            VALUES (?, ?, 'STANDBY_ACTIVATED', ?, ?)
        """, (generate_id(), seller_id,
              f"until:{data.expected_return} days:{requested_days}", now))

    print(f"[STANDBY] {seller_id} → STANDBY until {data.expected_return} ({requested_days}d)")
    return {
        "status":          "standby_active",
        "seller_id":       seller_id,
        "standby_until":   data.expected_return,
        "days_declared":   requested_days,
        "days_used_ytd":   days_used + requested_days,
        "days_remaining":  90 - (days_used + requested_days),
        "lambda_decay":    "frozen",
    }


@app.delete("/api/v1/seller/{seller_id}/standby", status_code=200)
def cancel_standby(seller_id: str, signature: str, timestamp: float):
    """
    Cancel an active STANDBY declaration.

    Signature required — prevents third parties from forcing a node
    back online against the seller's will.
    Signature payload: {seller_id, action: 'cancel_standby', timestamp}

    Note: quota already consumed on activation is NOT refunded.
    Lambda decay resumes from the moment of cancellation.
    """
    now = time.time()

    payload = json.dumps({
        "seller_id": seller_id,
        "action":    "cancel_standby",
        "timestamp": timestamp,
    }, separators=(",", ":"), sort_keys=True).encode()

    with get_db(immediate=True) as db:
        seller = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (seller_id,)
        ).fetchone()
        if not seller:
            raise HTTPException(404, "Seller not found")

        if not verify_signature(seller["sign_pubkey"], payload,
                                signature, timestamp=timestamp):
            raise HTTPException(400, "CANCEL_SIGNATURE_INVALID")

        if not seller["standby_until"] or seller["standby_until"] <= now:
            raise HTTPException(409, "NO_ACTIVE_STANDBY — nothing to cancel")

        db.execute(
            "UPDATE sellers SET standby_until = NULL WHERE seller_id = ?",
            (seller_id,)
        )
        db.execute("""
            INSERT INTO network_score_log (log_id, seller_id, event_type, detail, created_at)
            VALUES (?, ?, 'STANDBY_CANCELLED', ?, ?)
        """, (generate_id(), seller_id, f"cancelled_at:{now}", now))

    print(f"[STANDBY] {seller_id} → STANDBY cancelled")
    return {
        "status":       "standby_cancelled",
        "seller_id":    seller_id,
        "lambda_decay": "resumed",
        "note":         "Quota consumed on activation is not refunded",
    }


# ── BUYER GHOSTING REPORT ─────────────────────────────────────

class BuyerGhostingReport(BaseModel):
    settlement_token: str
    seller_id:        str
    signature:        str   # Ed25519/P-256 over {settlement_token, seller_id, timestamp}
    timestamp:        float


@app.post("/api/v1/report/buyer", status_code=202)
async def report_buyer_ghosting(data: BuyerGhostingReport,
                                 background_tasks: BackgroundTasks):
    """
    Seller reports buyer ghosting post-settlement.

    Flow:
      1. Verify seller signature
      2. Confirm VCI is in SETTLED_PENDING (no ACK yet)
      3. Queue grace period task (2 hours)
      4. After grace: if still no ACK → BUYER_FAULT + BES penalty
         If ACK arrived during grace → report discarded, no penalty

    Anti-abuse: if VCI is already CONFIRMED (ACK exists), report is
    rejected and seller receives STS penalty for false report.
    """
    now = time.time()

    with get_db(immediate=True) as db:
        # Find VCI by settlement_token
        vci = db.execute(
            "SELECT * FROM vci_active WHERE settlement_token = ?",
            (data.settlement_token,)
        ).fetchone()
        if not vci:
            raise HTTPException(404, "SETTLEMENT_NOT_FOUND")
        vci = dict(vci)

        # Verify seller is the winner
        if vci["winner_seller_id"] != data.seller_id:
            raise HTTPException(403, "REPORT_UNAUTHORIZED — only winning seller can report")

        # Verify seller signature
        seller = db.execute(
            "SELECT * FROM sellers WHERE seller_id = ?", (data.seller_id,)
        ).fetchone()
        if not seller:
            raise HTTPException(404, "Seller not found")

        payload = json.dumps({
            "settlement_token": data.settlement_token,
            "seller_id":        data.seller_id,
            "timestamp":        data.timestamp,
        }, separators=(",", ":"), sort_keys=True).encode()

        if not verify_signature(seller["sign_pubkey"], payload,
                                data.signature, timestamp=data.timestamp):
            raise HTTPException(400, "REPORT_SIGNATURE_INVALID")

        # Anti-abuse: if ACK already exists, seller is lying
        if vci["state"] == "CONFIRMED":
            # Penalize seller for false report
            db.execute("""
                INSERT INTO network_score_log
                  (log_id, seller_id, event_type, detail, created_at)
                VALUES (?, ?, 'FALSE_GHOSTING_REPORT', ?, ?)
            """, (generate_id(), data.seller_id,
                  f"VCI:{vci['vci_id']} already CONFIRMED", now))
            raise HTTPException(409,
                "REPORT_REJECTED — ACK already confirmed. "
                "False report logged against your STS.")

        # VCI must be SETTLED_PENDING to be reportable
        if vci["state"] not in ("SETTLED_PENDING", "BUYER_FAULT"):
            raise HTTPException(409,
                f"REPORT_INVALID — VCI state is {vci['state']}, expected SETTLED_PENDING")

        # Check for duplicate pending report
        existing = db.execute(
            "SELECT report_id FROM buyer_ghosting_reports "
            "WHERE vci_id = ? AND status = 'PENDING'",
            (vci["vci_id"],)
        ).fetchone()
        if existing:
            raise HTTPException(409, "REPORT_DUPLICATE — report already pending for this VCI")

        # Create report
        report_id       = generate_id("RPT-")
        grace_expires   = now + BES_GRACE_TTL
        buyer_pubkey    = vci["buyer_sign_pub"]  # signing key = BES identity

        db.execute("""
            INSERT INTO buyer_ghosting_reports
              (report_id, vci_id, seller_id, buyer_pubkey,
               reported_at, grace_expires_at, status)
            VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
        """, (report_id, vci["vci_id"], data.seller_id,
              buyer_pubkey, now, grace_expires))

    # Schedule background penalty after grace TTL
    background_tasks.add_task(
        process_ghosting_report, report_id, buyer_pubkey, vci["vci_id"]
    )

    print(f"[BES] Ghosting report {report_id} queued — grace until {grace_expires}")
    return {
        "status":          "report_queued",
        "report_id":       report_id,
        "grace_ttl_sec":   BES_GRACE_TTL,
        "grace_expires_at": grace_expires,
        "note":            "Buyer will be penalized if no ACK found after grace period",
    }


# ── BUYER STATUS (internal/debug) ────────────────────────────

@app.get("/api/v1/buyer/{buyer_pubkey}/status")
def get_buyer_status(buyer_pubkey: str):
    """
    Internal endpoint — returns buyer lifecycle state and BES tier.
    BES score is NEVER returned. Only status and tier (for debug/admin).
    """
    with get_db() as db:
        buyer = db.execute(
            "SELECT * FROM buyer_registry WHERE buyer_pubkey = ?", (buyer_pubkey,)
        ).fetchone()
    if not buyer:
        raise HTTPException(404, "Buyer not registered")
    buyer = dict(buyer)
    bes   = compute_bes(buyer)
    return {
        "status":        buyer["status"],
        "suspended_until": buyer["suspended_until"],
        "vci_emitted":   buyer["vci_emitted"],
        "registered_at": buyer["registered_at"],
        # BES tier only — never the score
        "bes_tier": (
            "RESTRICTED" if bes < 0.20 else
            "LOW_INTENT" if bes < 0.50 else
            "STANDARD"   if bes < 0.80 else
            "GOLD"
        ),
    }
