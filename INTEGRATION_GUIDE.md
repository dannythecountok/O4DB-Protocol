# O4DB™ Protocol v1.1.5 — Integration Guide

> **Audience:** developers setting up a local or staging pilot.  
> **Goal:** buyer emits a VCI → seller receives it → seller submits an offer → buyer ranks and settles.

---

## Architecture Overview

```
buyer_interface.html  ──POST /api/v1/vci/submit──►  relay (main.py)
                       ◄─GET /api/v1/vci/{id}/offers─  relay
                       ──POST /api/v1/vci/{id}/settle►  relay

seller_node.html      ──POST /api/v1/seller/register► relay
                       ──POST /api/v1/vci/{id}/offer──► relay

All HTML files served via HTTP (not file://)
Relay served behind nginx reverse proxy (port 80 → 8000 internal)
```

---

## Demand Identification — `demand_type` + `master_code`

O4DB v1.1.5 introduces explicit demand identification fields. The relay is agnostic
to the content — it stores and broadcasts these fields without validation.
Format enforcement is the responsibility of the application layer.

### Supported Master Code Types

| `demand_type` | Standard | Identifies | Example `master_code` |
|:---|:---|:---|:---|
| `EAN` | GS1 EAN/GTIN | Consumer unit | `7791234567890` |
| `VIN` | ISO 3779 | Vehicle (11 digits) | `1HGBH41JXMN109186` |
| `IATA` | IATA/GDS | Flight + route + class | `DL110J15APREZEATL` |
| `NSN` | NATO Stock Number | Military/industrial part | `5306-01-470-3452` |
| `CAGE_MPN` | CAGE + MPN | Factory spare part | `0TC92+9876-A1` |
| `ATC` | WHO ATC | Pharmaceutical molecule | `M01AE01` |
| `CAS` | CAS Registry | Pure chemical substance | `64-17-5` |
| `ISBN` | ISO 2108 | Book / edition | `978-3-16-148410-0` |
| `DOI` | DOI | Digital document / paper | `10.2118/195342-MS` |
| `UNS` | UNS | Metal / alloy | `S31600` |
| `OTA_GIATA` | OTA/GIATA | Hotel + dates + room + board | `H123+20260501+DBL+BB+FLEX` |
| `UODI` | UODI-O4DB v1.2 | Omnimodal transport demand | `P120-PASS-ROAD-...` |
| `GENERIC` | — | Any other identifier | Free form |

### VCI Submission — New Fields

```json
{
  "vci_id": "VCI-...",
  "demand_spec": "EAN:7791234567890",
  "demand_type": "EAN",
  "master_code": "7791234567890",
  ...
}
```

- `demand_type`: routing tag — free string, no validation by relay
- `master_code`: the identifier itself — no length limit, no format constraint
- `demand_spec`: legacy field, still required for backwards compatibility.
  Format: `TYPE:VALUE`. If `demand_type` + `master_code` are present,
  `demand_spec` is stored but not parsed.

### Seller Filtering

Sellers filter by `demand_type` in their webhook handler or polling loop.
The relay does not filter broadcasts by type — all eligible sellers receive all VCIs.

```python
# Example seller webhook handler
def on_vci_received(vci):
    if vci.get("demand_type") not in ["EAN", "GTIN"]:
        return  # ignore — not my domain
    process_vci(vci)
```

---

## Optional Layers

O4DB is neutral infrastructure. The following features are opt-in:

| Layer | Activation | Description |
|:---|:---|:---|
| **BES** | `BES_ENABLED=true` env var | Buyer reputation enforcement (INITIAL→ESTABLISHED→SUSPENDED→BLOCKED) |
| **ARA** | Buyer-side only | Local ranking algorithm — never runs on relay |
| **Escrow** | PSP integration | Application layer — relay is not a guarantor |
| **SPS** | Built-in | Seller network score always active (throttling) |

By default `BES_ENABLED=false` — the relay accepts VCIs from any buyer without
history checks. Activate for production environments where buyer accountability
is required.


---

## ⚠ Known Issue #1 — Crypto Algorithm Mismatch

**This is the most critical blocker for field testing.**

| Component | Algorithm | Key size |
|-----------|-----------|----------|
| `main.py` relay | Ed25519 (RFC 8032) | 32 bytes |
| `seller_node.html` | ECDSA P-256 | 65 bytes (uncompressed) |
| `buyer_interface.html` | ECDSA P-256 | 65 bytes (uncompressed) |

The relay calls `Ed25519PublicKey.from_public_bytes()` on the buyer's `buyer_sign_pub`
and the seller's `sign_pubkey`. A P-256 public key (65 bytes) will cause a hard
rejection — Ed25519 expects exactly 32 bytes.

**Fix Option A — Change the HTML to Ed25519 (Recommended)**

Web Crypto API added Ed25519 support in 2023 but browser support is still inconsistent
(Chrome 113+, Firefox 130+, Safari 17+). For a controlled pilot this is acceptable.

Replace in both HTML files:
```js
// Current (P-256)
const keyPair = await window.crypto.subtle.generateKey(
    { name: 'ECDSA', namedCurve: 'P-256' },
    true, ['sign', 'verify']
);

// Replace with (Ed25519)
const keyPair = await window.crypto.subtle.generateKey(
    { name: 'Ed25519' },
    true, ['sign', 'verify']
);

// Current signing
const sig = await window.crypto.subtle.sign(
    { name: 'ECDSA', hash: 'SHA-256' }, privateKey, data
);

// Replace with
const sig = await window.crypto.subtle.sign('Ed25519', privateKey, data);
```

Export public key stays the same (`exportKey('raw', publicKey)` → 32 bytes for Ed25519).

**Fix Option B — Add ECDSA P-256 support to the relay**

Add to `main.py`:
```python
from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDSA, EllipticCurvePublicKey
)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

def verify_p256(pubkey_b64: str, message: bytes, signature_b64: str,
                timestamp: Optional[float] = None) -> bool:
    """Verify ECDSA P-256 signature."""
    if timestamp is not None:
        if abs(time.time() - timestamp) > REPLAY_WINDOW_SEC:
            return False
    try:
        from cryptography.hazmat.primitives.asymmetric.ec import (
            EllipticCurvePublicKey, SECP256R1
        )
        from cryptography.hazmat.backends import default_backend
        pub_bytes = base64.b64decode(pubkey_b64)
        pub = EllipticCurvePublicKey.from_encoded_point(SECP256R1(), pub_bytes)
        sig_bytes = base64.b64decode(signature_b64)
        pub.verify(sig_bytes, message, ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False
```

Then patch `verify_ed25519` to auto-detect by key length:
```python
def verify_signature(pubkey_b64: str, message: bytes, signature_b64: str,
                     timestamp: Optional[float] = None) -> bool:
    """Detect algorithm by public key length and verify accordingly."""
    pub_bytes = base64.b64decode(pubkey_b64)
    if len(pub_bytes) == 32:
        return verify_ed25519(pubkey_b64, message, signature_b64, timestamp)
    elif len(pub_bytes) == 65:  # uncompressed P-256
        return verify_p256(pubkey_b64, message, signature_b64, timestamp)
    return False
```

**Recommendation for v1.1.4 pilot:** Fix Option A (Ed25519 in HTML). Cleaner,
consistent with the protocol spec, and avoids relay changes. Check browser support
of your pilot users first.

---

## ⚠ Known Issue #2 — Canonical Payload Field Order

The relay signs/verifies with `sort_keys=True` in `json.dumps`. The HTML files
must produce identical canonical JSON before signing. Verify:

```js
// Correct — sort keys before signing
const canonical = JSON.stringify(payload, Object.keys(payload).sort());

// Wrong — key order not guaranteed in JS objects
const canonical = JSON.stringify(payload);
```

The buyer's VCI signing in `buyer_interface.html` uses:
```js
JSON.stringify(vciPayload, Object.keys(vciPayload).sort())
```
This matches the relay's `sort_keys=True` **only if the field names match exactly.**

Cross-check these VCI fields against `validate_vci_signature` in `main.py`:

| Relay expects | HTML sends | Match |
|---|---|---|
| `vci_id` | `vci_id` | ✓ |
| `demand_spec` | `demand_spec` | ✓ |
| `quantity` | `quantity` | ✓ |
| `price_token` | `price_token` | ✓ |
| `currency` | `currency` | ✓ |
| `ttl` | `ttl` | ✓ |
| `commitment_level` | `commitment_level` | ✓ |
| `delivery_area` | `delivery_area` | ✓ |
| `privacy_mode` | `privacy_mode` | ✓ |
| `timestamp` | `timestamp` | ✓ |

All match. ✓

---

## Step 1 — Start the Relay

### Option A: Docker (recommended)

```bash
cd relay/
docker compose up -d
```

Verify:
```bash
curl http://localhost/health
# Expected:
# {"status":"healthy","registered_sellers":0,"active_vcis":0,"total_fingerprints":0}
```

Docker spins up two containers: `relay` (FastAPI on port 8000, internal only)
and `proxy` (nginx on port 80, public-facing). The relay is never directly exposed.

### Option B: Direct Python (dev mode)

```bash
cd relay/
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

CORS is already set to `allow_origins=["*"]` in dev mode — both HTML files
can call `http://localhost:8000` directly without the nginx proxy.

---

## Step 2 — Serve the HTML Files

**Do not open the HTML files via `file://`.** Browser security blocks Web Crypto API
and fetch calls from `file://` origins in some browsers.

Simplest dev server (Python, no install required):
```bash
# From the directory containing seller_node.html and buyer_interface.html
python3 -m http.server 3000
```

Then open:
- Seller: `http://localhost:3000/seller_node.html`
- Buyer: `http://localhost:3000/buyer_interface.html`

Set Relay URL in both interfaces to `http://localhost:8000` (direct)
or `http://localhost` (via nginx proxy).

---

## Step 3 — Register a Seller

Open `http://localhost:3000/seller_node.html`.

**Wizard Step 1 — Identity:**
1. Enter Seller ID (e.g. `SELLER-AR-001`)
2. Set Relay URL to `http://localhost:8000`
3. Click **Generate New Keys** — wait for public key to appear
4. **Copy and save the private key** shown in Step 3 — it will not be shown again

**Wizard Step 2 — Inventory:**
1. Categories: `EAN` (or `EAN, UPC`)
2. Delivery Areas: `AR` or `AR:CABA`
3. Min Commitment Level: `1`
4. Inventory IDs: leave empty (add from Inventory tab after launch)

**Wizard Step 3 — Registration:**
The node calls `POST /api/v1/seller/register`. Expected response:
```json
{"seller_id": "SELLER-AR-001", "status": "registered", "mode": "SANDBOX_NEW"}
```

**After launch:** go to the **Inventory tab** and add at least one product EAN.
The Inventory Affinity system requires at least one registered EAN to produce
`priority` gravity matches.

---

## Step 4 — Dispatch a VCI from the Buyer

Open `http://localhost:3000/buyer_interface.html`.

1. The sovereign identity is generated automatically on load.
2. Set Relay URL to `http://localhost:8000`.
3. Fill in Intent Dispatcher:
   - **Product Identifier:** `EAN:7891234567890` (must match a seller's inventory EAN)
   - **Quantity:** `1`
   - **Maximum Budget:** `950.00` (encrypted locally — relay never sees this)
   - **Currency:** `USD`
   - **Delivery Area:** `AR:CABA`
   - **Commitment Level:** `1`
   - **Intent Window:** `30` (minutes)
4. Adjust ARA sliders if desired (must sum to 100%).
5. Click **Dispatch Intent**.

Expected relay response:
```json
{"vci_id": "VCI-...", "status": "broadcast", "broadcast_count": 1}
```

`broadcast_count` = number of eligible sellers the relay notified.
If `0`: the seller's registered EAN does not match or geographic filter failed.

---

## Step 5 — Submit an Offer from the Seller

Back in `seller_node.html`:

1. Click **Start Polling** in the Live Feed tab.
2. The seller polls `GET /health` every 10 seconds (pilot polling mode).
   In production, the relay pushes via webhook.
3. To simulate a VCI arriving (for testing without relay push):
   ```js
   // Open browser console on seller_node.html
   demoVCI()         // simulates a priority match
   demoInsightVCI()  // simulates a market insight (not in inventory)
   ```
4. When a VCI appears, click **Make Offer**, fill in price and delivery terms,
   click **Sign & Submit Offer**.

The offer is signed with the seller's key and sent to
`POST /api/v1/vci/{vci_id}/offer`.

---

## Step 6 — Rank and Settle

Back in `buyer_interface.html`:

1. Offers appear in the **Live Ranking** table and are ranked in real time
   by the ARA running locally in the browser.
2. Move ARA sliders to see the ranking update immediately — no server call.
3. Check each offer for:
   - **✓ sig** — cryptographic signature verified locally
   - **📡 Network OK / ⚠ Network ↓** — Trust Radar from relay
   - ARA score `V=` computed with your weights
4. Click **★ Select** on the preferred offer.
5. Confirm in the settlement modal — read the binding commitment warning.
6. After confirmation:
   - Settlement Fingerprint is computed locally: `SHA-256(vci_id + seller_id + price + buyer_pubkey + timestamp)`
   - **Download** the fingerprint JSON — this is your proof of settlement
   - If the seller does not ACK within a reasonable time, use **🚨 Report Ghosting**

---

## Step 7 — ACK from Seller (Protocol Completion)

The seller receives a settlement notification (via webhook in production,
via polling in pilot). To complete the protocol, the seller sends:

```bash
curl -X POST http://localhost:8000/api/v1/vci/{vci_id}/ack \
  -H "Content-Type: application/json" \
  -d '{
    "seller_id": "SELLER-AR-001",
    "privacy_mode": "private",
    "seller_sign_pub": "<seller_public_key_b64>",
    "ack_signature": "<ed25519_signature_b64>"
  }'
```

This is not yet wired in the Seller Node Portal UI — it is the next implementation
target for v1.2.

---

## Nginx Config for Development (CORS + HTTP only)

The current `nginx.conf` is production-ready (SSL placeholder, strict routing).
For local dev, use this simplified version:

```nginx
# nginx-dev.conf
events { worker_processes 1; }

http {
    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass         http://relay:8000;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;

            # Dev CORS — remove in production
            add_header 'Access-Control-Allow-Origin'  '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Content-Type';
        }
    }
}
```

The relay already sets CORS headers in Python (`allow_origins=["*"]`) so this
is redundant but harmless — the nginx headers confirm CORS even on error responses
from FastAPI.

---

## Endpoint Reference

| Method | Path | Caller | Required fields |
|--------|------|--------|-----------------|
| `GET` | `/health` | both | — |
| `POST` | `/api/v1/seller/register` | seller | `seller_id`, `categories`, `delivery_areas`, `sign_pubkey`, `webhook_url` |
| `GET` | `/api/v1/seller/{seller_id}` | — | — |
| `GET` | `/api/v1/trust/{seller_id}` | both | — |
| `POST` | `/api/v1/vci/submit` | buyer | full `VCISubmission` — see Issue #1 for signature requirements |
| `GET` | `/api/v1/vci/{vci_id}/offers` | buyer | `?buyer_sign_pub=<b64>` |
| `POST` | `/api/v1/vci/{vci_id}/offer` | seller | `seller_id`, `unit_price`, `attributes`, `signature` |
| `POST` | `/api/v1/vci/{vci_id}/settle` | buyer | `vci_id`, `winner_seller_id`, `buyer_sign_pub` |
| `POST` | `/api/v1/vci/{vci_id}/ack` | seller | `seller_id`, `privacy_mode`, `seller_sign_pub`, `ack_signature` |
| `POST` | `/api/v1/vci/{vci_id}/ghost` | buyer | `?seller_id=<id>` |
| `GET` | `/api/v1/fingerprints` | — | — |

---

## What Is Not Wired Yet (v1.2 Targets)

| Feature | Status | Notes |
|---------|--------|-------|
| Seller ACK button in UI | ❌ | Requires seller to call `/ack` manually via curl for now |
| Relay push to seller (webhook) | ❌ | Seller polls `/health` in pilot; relay has webhook_url field ready |
| Ed25519 in HTML (Issue #1) | ❌ | Must fix before real field test |
| Seller key rotation | ❌ | Not in relay API |
| Multi-offer ranking (buyer selects 2nd choice) | ❌ | UI supports it, relay needs a re-open flow |

---

## Quick Smoke Test (no browser)

Verify the full protocol flow with curl only:

```bash
RELAY="http://localhost:8000"

# 1. Health
curl $RELAY/health

# 2. Register seller (manually generate Ed25519 keypair for testing)
# Use: python3 -c "from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey; import base64; k=Ed25519PrivateKey.generate(); print(base64.b64encode(k.public_key().public_bytes_raw()).decode())"
PUBKEY="<base64_ed25519_pubkey>"

curl -X POST $RELAY/api/v1/seller/register \
  -H "Content-Type: application/json" \
  -d "{\"seller_id\":\"TEST-SELLER\",\"categories\":[\"EAN\"],\"delivery_areas\":[\"AR\"],\"min_commitment\":0,\"sign_pubkey\":\"$PUBKEY\",\"webhook_url\":\"\",\"inventory_ids\":[\"7891234567890\"]}"

# 3. Trust score
curl $RELAY/api/v1/trust/TEST-SELLER
```

Full VCI submission requires a valid Ed25519 signature — use the browser
(buyer_interface.html) or the reference implementation (`o4db_reference.py`).

---

---

*O4DB™ Protocol v1.1.4*
*Copyright © 2026 Daniel Eduardo Placanica. All Rights Reserved.*
*Safe Creative Registration ID: 2602184604821-4XTVN6*
*Patent Application in Preparation — U.S. Patent App. No. 63/993,355 (USPTO)*
*Licensed under O4DB™ Community & Commercial License v1.1.4. See LICENSE file for full terms. Commercial use requires written agreement.*
