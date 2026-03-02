# Changelog — O4DB™ Protocol

All notable changes to this project are documented in this file.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Protocol versioning follows [Semantic Versioning](https://semver.org/).

## [v1.1.5] — 2026-03-01 — USPTO PROVISIONAL FILED

### Legal Milestones
- **O4DB™ Patent Pending** — U.S. Provisional Patent Application No. 63/993,946 filed March 1, 2026
- **UODI v1.2 Patent Pending** — U.S. Provisional Patent Application No. 63/993,355 filed February 28, 2026
- **Safe Creative** registration: 2603014734558-2D52RP (v1.1.5)
- Filing date establishes priority date for all claims in specification

### Added
- **`demand_type` + `master_code` fields:** VCI now supports explicit routing fields
  separate from `demand_spec`. `demand_type` is a free-form string tag (e.g. `EAN`,
  `VIN`, `UODI`, `NSN`, `ATC`, `CAS`, `ISBN`, `IATA`, `UNS`) used for seller-side
  filtering. `master_code` carries the actual identifier with no length or format
  constraint — supports codes from 8-char barcodes to 105-char UODI strings.
  Both fields stored in DB and included in broadcast payload.
  Legacy `demand_spec` format (`TYPE:VALUE`) remains fully supported for backwards
  compatibility. New clients should prefer explicit fields.
- **UODI-O4DB Standard (v1.2):** Universal Omnimodal Demand Identifier for transport
  and logistics demand. Full specification in `docs/UODI_v1.2.md`.
  Interoperates with O4DB as `demand_type: "UODI"`. Patent Pending U.S. 63/993,355.
- **`BES_ENABLED` environment flag:** Buyer Execution Score enforcement is now opt-in.
  Default: `false` (disabled). Set `BES_ENABLED=true` to activate buyer reputation
  lifecycle (INITIAL → ESTABLISHED → SUSPENDED → BLOCKED).
- **Value-Weighted Ghosting Penalty:** Ghosting penalty now scales by the relative
  value of the transaction vs. the seller's historical average. Prevents the
  Value-Weighted Sybil Attack (inflating trust via cheap transactions, then ghosting
  a high-value one). Weight clamped [0.5, 3.0]. Backwards compatible — neutral (1.0)
  when no volume history exists.
- **`cumulative_volume` tracking:** Sellers now accumulate confirmed transaction
  volume. Used by value-weighted penalty and available for ARA scoring.
- **Parallel Standby (Double Ghosting mitigation):** When buyer submits a settlement
  with an optional `standby_seller_id`, the relay notifies the standby seller via
  webhook after 120 seconds if the winner has not ACKed. Reduces buyer wait from
  15 minutes to ~2 minutes in double-ghosting scenarios.
- **Signed Audit Log endpoint:** `GET /api/v1/vci/{vci_id}/audit-log` returns a
  complete settlement event log with SHA-256 digest and Ed25519 relay signature.
  Suitable as evidence in arbitration and dispute resolution.
- **`GET /api/v1/relay/pubkey`:** Exposes relay public key for audit log verification.
- **Sobre Cerrado Digital — Settlement Disclosure:** `GET /api/v1/vci/{vci_id}/settlement-disclosure`
  implements a state-gated public disclosure mechanism. Returns 403 for any state
  other than CONFIRMED. Once confirmed, discloses final price, winner seller ID,
  demand identifier, and settlement timestamp — signed with relay Ed25519 key.
  Designed for government procurement compliance (EU Directive 2014/24/EU,
  Argentine Ley 13.064, and equivalent frameworks). Pre-award confidentiality
  is enforced cryptographically — no partial disclosure is possible.

### Fixed
- **LICENSE Section 3b clarified:** Derivative Works prohibition now explicitly
  scoped to commercial use. Non-commercial Community Tier implementations are
  expressly permitted, removing the internal contradiction with Section 2.
- **License protocol version:** Updated from v1.1.4 to v1.1.5.
- **LICENSE Section 3b (new) — Certified Integrator Program:** Third-party
  developers may build and commercialize O4DB™ integration modules (ERP connectors,
  middleware adapters, legacy bridges) under written certification from the author.
  Defines terms for ecosystem partners without protocol integrity compromise.

### Added (ERP Integration)
- **`external_ref_mapping` field in VCI:** Optional buyer-side field to carry
  internal ERP reference numbers (SAP PO, Oracle Doc ID, etc.). Stored relay-side
  only — never broadcast to sellers. Returned exclusively to the buyer on VCI lookup.
- **ERP-Ready Interface section in README:** Complete integration guide including
  webhook JSON schema, VCI submission schema, Docker-first deployment, PROXY_NODE
  profile for legacy systems, and Certified Integrator model.
- **`docker-compose.yml`:** Reference deployment for zero-configuration relay startup.
  Exposes clean REST API on localhost:8080. All crypto internal — ERP only makes
  plain HTTP calls.
- **PROXY_NODE Profile documented:** Enables legacy systems (COBOL, pre-2000 ERP,
  mainframes) to participate in O4DB™ without cryptographic capability. Proxy signs
  and encrypts within the company's secure perimeter.

### Schema changes
- `sellers` table: added `cumulative_volume REAL DEFAULT 0.0`
- `vci_active` table: added `standby_seller_id TEXT DEFAULT NULL`
- `vci_active` table: added `parallel_standby_notified INTEGER DEFAULT 0`
## [v1.1.4] — 2026-02-22

### Added
- **Buyer Execution Score (BES):** Four-state buyer lifecycle (INITIAL → ESTABLISHED → SUSPENDED → BLOCKED)
  with graduated ghosting penalties. INITIAL buyers are permanently blocked on first ghost;
  ESTABLISHED buyers receive 48-hour suspension before permanent block on repeat offense.
  Ghost reports include a 2-hour grace period — late ACK nullifies report with no penalty.
  False reports penalize the reporting seller's Trust Score. BES never exposed externally;
  relay returns tier classification only (RESTRICTED / LOW_INTENT / STANDARD / GOLD).
  New endpoints: `POST /api/v1/report/buyer`, `GET /api/v1/buyer/{pubkey}/status`.
- **STANDBY mode:** Sellers may declare planned absences via `POST /api/v1/seller/{id}/standby`.
  Trust Score exponential decay is suspended for the declared period (max 30 days/year).
  VCI eligibility suspended during STANDBY. Score preserved at activation value.
  Cancel via `DELETE /api/v1/seller/{id}/standby`. Prevents structural disadvantage
  for legitimate operational interruptions.
- **Cryptographic Policy header (Key Separation Principle):** `main.py` now declares
  explicit cryptographic policy separating signing keys (Ed25519/P-256) from encryption
  keys (X25519/HPKE), per RFC 8032 and RFC 9180. Prevents cross-protocol attack vectors.
- **Anti-replay on all signed endpoints:** `register_seller`, `settle_vci`, and `submit_offer`
  now validate Ed25519 signatures with ±300s timestamp window. Previously only VCI and ACK
  endpoints enforced anti-replay. Full coverage achieved.
- **`webhook_url` optional:** `SellerRegistration` model now accepts `null`/absent
  `webhook_url` field. Previously rejected valid registrations without webhook.
- **Dual-algorithm cryptography:** Ed25519 (primary) / ECDSA P-256 (fallback).  
  Runtime detection via `detectCryptoAlgo()` in both HTML interfaces.  
  Relay auto-detects algorithm by public key length (32 bytes → Ed25519, 65 bytes → P-256).  
  Includes IEEE P1363 → DER signature conversion for P-256 Web Crypto API compatibility.
- **Settlement hold multiplier:** velocity-based ghosting penalty amplification.  
  Measures concurrent settlements in a 10-minute window. Burst of ≥3 → 5× multiplier,  
  ≥10 → 15× multiplier. Applied only on ghosting report — zero friction for honest sellers.
- **ACK submission UI in Seller Node:** `submitACK()` function, ACK panel in offered card,  
  `ack-confirmed` state with fingerprint display. Protocol circle now closes without manual curl.
- **Slider lock in Buyer ARA:** individual weight locks with proportional redistribution  
  among free sliders. Professional-grade ARA control.
- **Settlement fingerprint download:** JSON receipt with local SHA-256 fingerprint,  
  relay comparison status (`verified` / `relay_mismatch`), and computation audit trail.
- **Ghosting report button:** `POST /api/v1/vci/{vci_id}/ghost` wired in buyer UI.  
  Graduated penalties: 0.15 (1st) → 0.30 (2nd) → 0.50 (3rd+) within 24-hour window.
- **Trust Radar with network_score:** real-time seller ecosystem health indicator  
  in buyer offer cards. Three states: Network OK / Network ↓ / Network ↓↓.
- **IndexedDB session persistence:** VCI lifecycle survives browser refresh.  
  Automatic session recovery on reload within TTL window.
- **UNIQUE constraint on `sign_pubkey`:** one keypair per seller identity, enforced  
  at schema level and with explicit `PUBKEY_CONFLICT` error in registration handler.
- **Integration Guide:** end-to-end setup documentation covering all 7 protocol steps,  
  endpoint reference table, dev nginx config, and curl smoke test.
- **GitHub Actions CI:** syntax and AST parse check on relay pushes.

### Changed
- `verify_ed25519()` call sites replaced with `verify_signature()` dispatcher  
  throughout `main.py` — VCI validation, offer validation, ACK validation.
- Docker Compose `restart: always` → `restart: unless-stopped` on both services.  
  Respects manual `docker stop` while still recovering from crashes.
- Version string normalized to `v1.1.4` across all files (`version=` field in FastAPI app).
- Copyright symbol normalized to `©` across all source files (was `(c)` in Python headers).

### Fixed
- **CRITICAL — Orphan decorator on `submit_vci`:** `@app.post("/api/v1/vci/submit")`
  decorator was inadvertently applied to `compute_bes()` instead of `submit_vci()`.
  FastAPI registered `compute_bes` as the VCI submission handler; all VCI submissions
  were accepted (202) but silently discarded without DB persistence.
  Root cause: BES constants block inserted between decorator and function definition.
- **BES identity split:** `submit_vci` registered buyers by `buyer_sign_pub` while
  `submit_ack` updated counters by `buyer_pubkey` (HPKE encryption key). Same buyer
  created two registry records; BES counters never accumulated. Standardized to
  `buyer_sign_pub` (Ed25519 signing key) across all BES operations.
- **`settle_vci` subquery:** Used `buyer_pubkey` column instead of `buyer_sign_pub`
  causing settlement counter increments to silently fail.
- **SUSPENDED auto-expiry:** `check_buyer_eligibility` blocked SUSPENDED buyers
  permanently without checking `suspended_until` expiry. Auto-reactivation added.
- **`register_seller` HTTP status:** was returning 201, now returns 200 for consistency
  with all other protocol endpoints.
- Algorithm mismatch between HTML interfaces (ECDSA P-256) and relay (Ed25519).  
  Root cause: HTML files generated before relay crypto was finalized.  
  Resolution: dual-algorithm support at both ends with runtime detection.
- `ghost_penalty_mult` column added to `vci_active` schema with `DEFAULT 1.0`.  
  Existing deployments retain baseline behavior without migration.

---

## [v1.1.0] — 2026-02-21

### Added
- Relay Server (`main.py`): FastAPI + SQLite, six-criteria eligibility filter,  
  Ed25519 signature verification, anti-replay ±300s window, community tier limit.
- Seller Node Portal (`seller_node.html`): Visual Gravity dual-feed (Matches / Insights),  
  Web Crypto API key generation, offer signing, inventory affinity.
- Buyer Interface (`buyer_interface.html`): Sovereign Vault (PBKDF2 + AES-GCM),  
  ARA local ranking, price_token encryption, VCI dispatch.
- Reference Implementation (`o4db_reference.py`): HPKE RFC 9180, Ed25519, ARA scoring.
- Docker + nginx production deployment configuration.
- README v1.1 — full protocol specification.

---

## [v1.0.0] — 2026-02-18

### Added
- Initial protocol specification and provisional patent draft.
- Core concepts: VCI (Verifiable Commerce Intent), ARA (Agential Ranking Algorithm),  
  SPS (Seller Performance Score), JIT-S (Just-In-Time Settlement).
- Safe Creative registration: `2602184604821-4XTVN6`.

---

*O4DB™ Protocol — Copyright © 2026 Daniel Eduardo Placanica. All Rights Reserved.*  
*Licensed under O4DB™ Community & Commercial License v1.1.5. See LICENSE.*
