# O4DB™ Protocol — Sovereign Agental Commerce Specification v1.1.5

> **Copyright © 2026 Daniel Eduardo Placanica. All Rights Reserved.**  
> Safe Creative Registration ID: 2602184604821-4XTVN6  
> O4DB™ Patent Pending — U.S. Patent App. No. 63/993,946 (USPTO)  
> UODI v1.2 Patent Pending — U.S. Patent App. No. 63/993,355 (USPTO)  
> Licensed under O4DB™ Community & Commercial License v1.1.5.  


**Only For Determined Buyers** A demand-initiated execution protocol for high-intent commerce and autonomous agent-to-agent transactions.

> **IMPORTANT:** This protocol and its reference implementations are governed by the **O4DB™ Community & Commercial License**. This is a Sovereign Open-Standard; it is NOT licensed under CC-BY, MIT, or any permissive open-source license.

---

## 1. Project Identity & Intellectual Property
* **Author:** Daniel Eduardo Placanica
* **Safe Creative ID (v1.0):** 2602184604821-4XTVN6
* **Safe Creative ID (v1.1):** 2602204641140-6FSX6N
* **Safe Creative ID (v1.1.5):** 2603014734558-2D52RP
* **UODI v1.2 Safe Creative:** 2602284718909-6XLBXF
* **O4DB™ Patent Status:** Patent Pending — U.S. Patent App. No. 63/993,946 (USPTO)
* **UODI v1.2 Patent Status:** Patent Pending — U.S. Patent App. No. 63/993,355 (USPTO)
* **Legal Status:** The ARA (Automated Ranking Algorithm) and VCI (Validated Commitment Intent) mechanisms are Trade Secrets and Intellectual Property of the Author.
* **Contact:** [https://x.com/O4DBmodel](https://x.com/O4DBmodel) | daniel@o4db.org

---

## 2. Executive Summary
O4DB™ is a zero-trust commerce protocol that inverts the traditional marketplace model. Instead of sellers listing products for passive discovery, buyers emit a **Validated Commitment Intent (VCI)**. 

The protocol ensures **Buyer Sovereignty** through:
1.  **Direct Intent:** No middleman algorithms or "sponsored results" deciding what the buyer sees.
2.  **Cryptographic Proof:** Every offer is digitally signed (Ed25519) and bound to a specific intent.
3.  **Local Intelligence:** The Ranking Algorithm (ARA) runs locally on the buyer's side, preventing platform-side manipulation or pay-to-play ranking.



---

## Protocol Architecture — Layered Design

O4DB is neutral infrastructure. The core cycle is always active; everything else is opt-in.

### Core Cycle (always active)
```
Buyer emits VCI → Relay filters + broadcasts → Seller submits offer → Buyer settles → Seller ACKs
```
The relay enforces cryptographic integrity, anti-replay, eligibility filtering, and seller network scoring.
It does not rank offers, does not guarantee transactions, and does not expose buyer identity.

### Optional Layers

| Layer | Who activates | Description |
|:---|:---|:---|
| **ARA** | Buyer (local) | Ranking algorithm — runs on buyer device, never on relay |
| **BES** | Relay operator (`BES_ENABLED=true`) | Buyer reputation lifecycle enforcement |
| **SPS** | Always active | Seller network score + throttling |
| **Escrow / FullEscrow** | PSP opt-in | Financial guarantee — relay transports, PSP guarantees |
| **UODI** | App layer | Omnimodal transport demand identifier (`demand_type: "UODI"`) |

### Demand Identification

VCIs carry a `demand_type` routing tag and `master_code` identifier. The relay is agnostic
to their content — it stores and broadcasts without validation. Supported types include
EAN, VIN, IATA, NSN, ATC, CAS, ISBN, DOI, UNS, OTA/GIATA, UODI, and any custom identifier.

See `docs/UODI_v1.2.md` for the UODI-O4DB transport demand specification.


---

## 3. Technical Standards (v1.1.5 Implementation)

### Cryptographic Stack
* **Identity & Authentication:** Ed25519 (RFC 8032) for asymmetric signing of VCIs, Offers, and ACKs.
* **Privacy & Negotiation:** HPKE (RFC 9180) using DHKEM(X25519, HKDF-SHA256) + AES-256-GCM for secure price commitment.
* **Integrity:** SHA-256 Settlement Fingerprints for immutable transaction auditing.

### System Components
* **Component 1 (Relay Server):** The network backbone for eligibility filtering, inventory affinity, and seller network scoring.
* **Component 2 (Seller Node):** Interface for real-time VCI reception and automated/manual offer generation.
* **Component 3 (Buyer ARA):** Local execution environment for intent emission and multi-criteria offer ranking.

### Hardware Compatibility
* **Primary signing curve:** Ed25519 (RFC 8032) — software keys, cloud KMS, modern HSMs.
* **Fallback signing curve:** P-256 / ECDSA — FIDO2/WebAuthn devices, iPhone/Android Secure Enclave,
  YubiKey, and any NIST-certified hardware token. Runtime auto-detection by public key length.
* **Encryption:** X25519 via HPKE (RFC 9180) — independent of the signing curve per Key Separation Principle.

---

## Quick Start (Docker)

```bash
# Clone and deploy the relay in under 2 minutes
git clone https://github.com/youruser/o4db-protocol.git
cd o4db-protocol/relay
docker-compose up -d

# Verify
curl http://localhost/health
# → {"status":"healthy","registered_sellers":0,"active_vcis":0,...}
```

Full deployment documentation: [`relay/DEVELOPER_GUIDE.md`](./relay/DEVELOPER_GUIDE.md)  
End-to-end integration walkthrough: [`INTEGRATION_GUIDE.md`](./INTEGRATION_GUIDE.md)

---

## 4. Licensing & Commercial Terms
All use of this specification and its associated code is subject to the **O4DB™ Community & Commercial License v1.1.5**.

* **Community Tier:** Free for non-commercial research, testing, and production use up to **50 completed settlement operations per month**.
* **Enterprise Tier:** Mandatory commercial licensing is required for entities exceeding the 50-transaction threshold or integrating the protocol into centralized marketplaces.
* **Integrity Clause:** Redistribution or modification of the core ARA or VCI logic for commercial purposes is strictly prohibited without explicit written consent.

**For full legal terms, refer to the [LICENSE](./LICENSE) file.**

---

## 5. Deployment Roadmap
- [x] **Relay Server (v1.1.5):** Core infrastructure with Ed25519/HPKE support.
- [x] **Gold Master Specification:** Full cryptographic and logic reference.
- [ ] **Seller Node Interface:** (In development - Phase 2).
- [ ] **Buyer Sovereign App:** (Planned - Phase 3).

---
© 2026 Daniel Eduardo Placanica. All Rights Reserved. O4DB™ and "Only For Determined Buyers" are protected trademarks.

---

## The Problem in One Sentence

Every e-commerce system built in the last 30 years is optimized  
for the seller. O4DB™ is the first protocol designed exclusively  
for the buyer who already knows what they want.

---

## Why This Is Being Published Now

This specification is published at draft stage intentionally.

The goal is to establish prior art, invite architectural critique,  
and identify implementation partners before committing to a fixed  
schema. The protocol will evolve through this process.

This is not vaporware. Every component described here has been  
designed to be implementable with existing infrastructure —  
no new consensus mechanisms, no new blockchains, no new payment  
rails required for v1.0.

---

## Status

- No production deployment
- No live implementation
- Architecture under active refinement
- Not an industry standard

---

## Problem Context

Modern commerce systems are optimized for discovery:

- Search, browsing, recommendation, behavioral targeting

This works well for exploratory buyers. It fails systematically  
for a different kind of buyer — one who already knows:

- The exact product identifier or full attribute constraints
- The maximum budget they are willing to pay
- The willingness to execute immediately
- The verified financial capacity to settle

Current systems treat these high-intent buyers identically to  
window shoppers. They are forced through discovery flows designed  
to maximize seller revenue, not buyer efficiency.

**O4DB™ proposes an alternative execution path for pre-qualified demand.**

The insight is simple: when a buyer's intent is fully specified  
and financially verifiable, the market should come to them —  
not the other way around.

---

## Core Thesis

When demand is structurally defined, financially validated,  
and time-bound — supply can compete deterministically.

**O4DB™ is not a marketplace.**  
It is a protocol layer for structured demand execution.

The distinction matters: O4DB™ does not hold inventory,  
does not custody funds, does not intermediate the commercial  
relationship between buyer and seller. It is infrastructure —  
like TCP/IP for commerce intent.

---

## Protocol Premises

Six principles govern every architectural decision in O4DB™.  
When a design choice conflicts with any of these, the choice changes —  
not the premise.

**Buyer Sovereignty** — demand is verified, private, and financially  
backed before any seller sees it. Market power belongs to the buyer  
by design, not by negotiation.

**Unbreakable Security** — encrypted identity, invisible max price,  
mandatory cryptographic signatures, local ranking execution, automatic  
penalties. Security is not a layer added on top — it is the architecture.

**Real Decentralization** — no central server runs the ranking, no  
single entity can capture the protocol, no corporation can shut it  
down. Infrastructure like TCP/IP, not a service like AWS.

**Universal Interoperability** — Google, Amazon, Mercado Libre are  
participating nodes, not owners. Any agent from any organization speaks  
the same protocol language because the schema is open and the algorithm  
is public.

**Agnostic Scalability** — the protocol works identically for a consumer  
buying a single iPhone and for fleets of autonomous agents replenishing  
industrial inventory in real time. The protocol does not change —  
implementations scale.

**Protected Authorship, Open Participation** — any corporation can  
implement it, any developer can contribute, any agent can integrate.  
The protocol has a documented intellectual author. Open does not mean  
without origin.

---

## Intended Scope

**O4DB™ is designed for:**

- Uniquely identifiable products (electronics, industrial components)
- Parametrized goods with objective constraints (vehicles, equipment)
- B2B procurement with defined specifications
- High-intent B2C segments
- Agent-to-agent commerce (M2M)

**O4DB™ is NOT designed for:**

- Exploratory shopping or impulse buying
- Products requiring diagnosis before specification
- Content-driven discovery commerce
- General retail browsing

---

## Architectural Components

### 0. Demand Resolution Phase (Pre-VCI)

Before a VCI is emitted, a buyer operating via natural language  
must resolve their demand into a precise, unambiguous specification.

The resolution engine accepts natural language input, queries  
available product and service catalogs, and returns a structured  
selection dashboard. The buyer confirms the exact object of their  
demand — or selects up to three equivalent variants if flexibility  
exists — before any signal is broadcast to the network.

**Human confirmation is mandatory before VCI dispatch,  
regardless of the buyer's configured autonomy level.**

The agent may iterate as many times as necessary to resolve  
ambiguity. It cannot emit the VCI without explicit principal  
confirmation. This is the architectural boundary between an  
agent that assists and an agent that acts without oversight.

This phase is optional for Exact ID Mode (the buyer already  
has the identifier) and mandatory for Attribute Mode.

---

### 1. Verified Intent Signal (VCI)

The VCI is a cryptographically signed, structured demand packet  
emitted by a buyer — human or agent. It is the atomic unit of  
the O4DB™ protocol.

**VCI has two representations:**

- **Private VCI** — held exclusively by the ARA. Contains all fields  
  including `max_price` in plaintext.
- **Public VCI** — broadcast to eligible sellers. Contains all fields  
  except `max_price`, which is replaced by an encrypted `price_token`.  
  Sellers never see the buyer's maximum budget.  
  This is a core anti-scraping primitive of the protocol.

**price_token cryptographic specification:**

The protocol adopts **HPKE (Hybrid Public Key Encryption, RFC 9180)**  
as the official cryptographic standard for price_token construction.  
ECIES remains supported as minimum viable option for prototype  
implementations only.

```
# HPKE RFC 9180 — official standard
kem_id:        DHKEM(X25519, HKDF-SHA256)
kdf_id:        HKDF-SHA256
aead_id:       AES-256-GCM
nonce:         CSPRNG(32 bytes), unique per VCI
ciphertext     = HPKE.Seal(recipient_pub=buyer_pubkey,
                           info=vci_id,
                           aad=nonce,
                           pt=max_price)
hmac           = HMAC-SHA256(key=buyer_privkey, msg=vci_id || nonce)
price_token    = base64(nonce || ciphertext || hmac)

# ECIES — prototype fallback only, not for production
```

The buyer decrypts `price_token` locally using their own private key —  
no server required. The `price_token` exists for external network  
validation only, not for central ARA decryption.

**Constant-time rejection responses (anti-inference):**  
All offer rejection signals are delivered in constant time:

```
T_response = T_fixed + noise
T_fixed:  protocol-defined constant per category (e.g., 200ms for electronics)
noise:    uniform random ∈ [0, T_fixed × 0.1]
```

Every response — accepted or rejected — arrives within the same  
time window. This makes the response time distribution statistically  
indistinguishable regardless of price. A seller cannot approximate  
`max_price` by accumulating timing observations across multiple VCIs  
because the signal is constant, not correlated with the price delta.

This replaces the previous randomized delay approach (50–300ms variable),  
which was vulnerable to statistical accumulation attacks across  
multiple similar VCIs.

**Mandatory fields (all VCIs):**

| Field | Type | Description |
|-------|------|-------------|
| `vci_version` | string | Protocol version. Current: `"1.0"` |
| `demand_spec` | object | Exact ID or Attribute Mode (see below) |
| `quantity` | integer | Units requested |
| `max_price` | decimal | Maximum budget — Private VCI only, ARA-internal |
| `price_token` | string | Encrypted token replacing max_price in Public VCI |
| `currency` | ISO 4217 | Currency of the demand |
| `ttl` | integer | Time-To-Live in seconds (Sovereign TTL) |
| `commitment_level` | integer | 0–4 (see Commitment Levels) |
| `solvency_cert` | string | Certificate issued by regulated Financial Oracle |
| `delivery_accepted` | array | `[pickup]`, `[delivery]`, or `[pickup, delivery]` |
| `delivery_area` | string | ISO 3166-1 + subdivision (e.g., `AR:CABA`, `AR`, `AR,CL`) |
| `privacy_mode` | enum | `private` / `standard` / `open` |
| `buyer_pubkey` | string | Buyer's registered public key |
| `vci_signature` | string | Cryptographic signature over all fields |

`delivery_accepted`, `delivery_area`, and `privacy_mode` are  
inherited from the Buyer Profile by default. Any may be  
overridden per VCI without modifying profile defaults.

**Demand Specification — Two Modes:**

**Exact ID Mode:** The buyer provides a universal identifier  
that resolves unambiguously to a single product or service.  
Offers must match exactly. No interpretation required.

| Category | Identifier Type | Example |
|----------|----------------|---------|
| Consumer products | EAN | `EAN:7891234567890` |
| Consumer products | UPC | `UPC:012345678905` |
| Global trade | GTIN | `GTIN:00012345678905` |
| Industrial / components | OEM_PN | `OEM_PN:365729:SCANIA` |
| Vehicles | VIN | `VIN:1HGBH41JXMN109186` |
| Travel | IATA_ROUTE | `IATA_ROUTE:EZE-ATL:20260415` |
| Books | ISBN | `ISBN:9780141036144` |
| Pharma | ATC | `ATC:M01AE01` |

Format: `identifier_type:identifier_value`  
Both subfields are mandatory. A VCI with either missing is  
rejected by the network before broadcast.

**Consumer Electronics — additional mandatory fields (v1.0):**

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `condition` | enum | `new` / `refurbished_official` | `new` |
| `market` | string | ISO 3166-1 alpha-2 | Required |

**Consumer Electronics — optional fields (v1.0):**

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `revision` | string | Hardware or firmware version | — |
| `accept_equivalents` | boolean | Accept verified interchangeable products | `false` |
| `oem_preference` | enum | `must_have` / `nice_to_have` | — |

When `accept_equivalents: true`, the protocol queries recognized  
industry equivalence databases (TecDoc for automotive, Partslink  
for North America) before broadcast and expands the VCI with  
verified interchangeable identifiers. O4DB™ does not maintain  
its own equivalence database.

**Attribute Mode:** Parametric constraints resolved via the  
Demand Resolution Phase (Section 0) into buyer-confirmed  
variants before VCI issuance.

| Parameter | Description |
|-----------|-------------|
| `must_have` | Non-negotiable attributes. Offers not meeting these are rejected before ranking. May include OEM restrictions, certifications, compatibility requirements. |
| `nice_to_have` | Desirable but non-blocking. Offers meeting these rank higher in the V function. |
| `oem_preference` | Accepted original equipment manufacturers. Set by buyer or inferred by agent from context (warranty status, category standards, buyer profile history). |

**When no recognized equivalence database exists:**  
For categories without an established industry equivalence standard,  
the protocol supports a parametric attribute format:

```
custom_attributes:
  - key:   "tensile_strength_mpa"
    value: "≥420"
    unit:  "MPa"
  - key:   "material_grade"
    value: "316L"
```

These attributes travel in the VCI `must_have` or `nice_to_have`  
fields. The protocol does not validate them — matching is the  
seller's responsibility.

**Signature Requirement:**

Every VCI must be cryptographically signed by the issuer's  
private key before broadcast. The signature serves three functions:

1. **Non-repudiation** — binds the buyer or their authorized  
   agent to all VCI terms including SPS penalty conditions.

2. **Integrity** — any modification in transit invalidates  
   the signature. Tampered VCIs are rejected by the network.

3. **Agentic accountability** — when a VCI is issued by an AI  
   agent, the signature must correspond to a key explicitly  
   delegated by the human principal to that agent, creating  
   a verifiable chain of authorization.

**Cryptographic standard:** All signing operations in O4DB™ use  
**HPKE (RFC 9180)** as the official standard. ECIES is accepted only  
for prototype implementations. Production deployments must use HPKE.

**Key management:** Signing keys for buyers and seller nodes must be  
managed via an external KMS or HSM-compatible system. The protocol  
does not mandate a specific key management solution but requires that  
private keys never exist in plaintext outside a secure enclave.

---

### 2. Commitment Levels

| Level | Name | Financial Mechanism |
|-------|------|---------------------|
| 0 | Soft Intent | No financial backing |
| 1 | Pre-Authorization | Temporary funds hold |
| 2 | Earnest Deposit | Partial escrow via Payment Provider |
| 3 | Full Escrow | Complete funds locked, auto-release on ACK |
| 4 | Institutional Guarantee | Bank-backed irrevocable commitment |

O4DB™ does not custody funds. Financial validation is delegated  
to regulated financial institutions or payment providers.

**Enforcement by level:**

| Level | Enforcement | Mechanism |
|-------|-------------|-----------|
| 0 | None | Good faith only |
| 1 | Contractual | Terms accepted at bid submission |
| 2 | Semi-technical | Partial escrow via Payment Provider |
| 3 | Technical | Full escrow pre-locked, auto-release on ACK |
| 4 | Institutional | Bank guarantee, independent execution |

**O4DB™ does not guarantee enforcement below Level 2.**  
Sellers are advised to configure their minimum accepted  
commitment level in their Seller Profile accordingly.

---

### 3. Anonymous Reverse Auction (ARA)

The ARA is the competitive engine of the protocol. Once a VCI  
is broadcast to the eligible seller network, certified sellers  
submit binding offers within the Sovereign TTL window. Sellers  
do not see competing bids. Ranking is deterministic, defined  
entirely by the buyer's declared weight matrix.

**ARA Execution Model — Local by Design:**

The ranking algorithm runs locally in the buyer's environment —  
on the buyer's device or within the agent's TEE for Level 3.  
There is no central ARA server that computes rankings.

This is a deliberate architectural decision with three consequences:

1. **Buyer sovereignty** — the buyer's agent applies the ranking  
   algorithm to received offers using the buyer's own declared  
   weights. No third party can manipulate the outcome.

2. **Seller auditability** — the ranking formula is a public  
   specification. A seller who loses can verify that the algorithm  
   is correct because the formula and the normalization scales  
   (declared in the VCI) are fully transparent. They cannot see  
   competing offers, but they can verify that a better offer  
   than theirs would win under those weights — and that no  
   other outcome is possible.

3. **No central point of failure** — the protocol requires  
   broadcast infrastructure and a Trust Score registry.  
   It does not require a ranking server. These are categorically  
   different: a Trust Score lookup is a read of public data;  
   a ranking server would be a decision-making authority.

**Local ranking flow:**

```
For each received offer:
  1. Verify offer_signature against seller's registered public key
  2. Compare unit_price against local max_price
     (buyer already holds max_price — no decryption server needed)
  3. If unit_price > max_price → silently discard
  4. Normalize all Aᵢ per scales declared in VCI at issuance
  5. Fetch seller Trust Score S from public Trust Score registry
  6. Compute V = Σ(wᵢ · Aᵢ) + (wₛ · S) - P
  7. Rank offers by V descending
  8. Present to buyer (Level 0,1) or execute autonomously (Level 2,3)
```

**Conformance requirement:**  
Any O4DB™-compatible implementation that moves the ranking  
computation to a remote server is **NON-CONFORMANT** with this  
specification. The protocol is explicit: ranking is a local  
operation performed by or on behalf of the buyer.

**Performance and scalability:**  
The protocol specifies the algorithm, not the execution infrastructure.  
Performance optimization is the responsibility of each implementor.  
A single-buyer deployment and a fleet of 10,000 autonomous agents  
run the same protocol — the implementation scales, the specification  
does not change. Mercado Libre, Google, and Amazon may each optimize  
their agent stack independently without modifying the protocol.

**Pre-broadcast eligibility filter:**

Before broadcasting, the protocol evaluates every certified  
seller node against six criteria. A seller receives the VCI  
only if all six conditions are satisfied simultaneously:

| Criterion | Condition |
|-----------|-----------|
| Category | Seller certified in the VCI's product category (Proof of Category) |
| Geography | Seller's `delivery_areas` intersects VCI `delivery_area` |
| Fulfillment | Seller supports ≥1 mode in VCI `delivery_accepted` |
| Commitment | Seller `min_commitment_level` ≤ VCI commitment level |
| Ban check | Seller not in buyer's `banned_sellers` list |
| Inventory Affinity | Seller has prior Settlement Fingerprints for the same `identifier_type` and compatible `identifier_value` family |

**Inventory Affinity — implementation detail:**

Inventory Affinity is a soft criterion with an automatic fallback.  
It uses the Settlement Fingerprint ledger as ground truth:

```
affinity_match = seller has ≥ 1 confirmed transaction
                 with same identifier_type AND
                 compatible identifier_value family

IF affinity_match: seller receives VCI (priority broadcast)
IF NOT affinity_match AND eligible_affinity_sellers ≥ 3:
  seller excluded (category-level fallback not triggered)
IF NOT affinity_match AND eligible_affinity_sellers < 3:
  filter relaxes to category level — seller included
```

This keeps broadcast surgical without starving new sellers  
or low-volume categories.

**Probation Mode for new sellers:**

Rather than hard restrictions (binary access), new sellers without  
Inventory Affinity history enter a graduated ramp:

```
PROBATION_MODE (no affinity history, category is eligible):
  access:           guaranteed — always included in broadcast
  ranking_weight:   affinity_score multiplier = 0.70
                    (offers visible but ranked below established sellers)
  graduation:       automatic after 5 successful transactions
                    with matching identifier_type
  purpose:          rampa de entrada, no barrera de entrada
```

A seller in `PROBATION_MODE` always participates — they are never  
excluded. Their offers rank slightly below sellers with proven  
affinity history, creating a natural incentive to build track record  
without creating an impossible barrier for new entrants.

This filter minimizes network noise and reduces the number of  
nodes receiving the encrypted buyer identity payload, directly  
reducing the JIT attack surface.

**Seller Profile (declared once at certification):**

```
categories:             [electronics, computers]
delivery_modes:         [pickup, delivery]
delivery_areas:         [AR, UY]
min_commitment_level:   1
```

**Buyer ban list (Buyer Profile field):**

```
banned_sellers: [NODE:AR:00123, NODE:AR:00456]
```

The ban is permanent until explicitly lifted by the buyer.  
Banned sellers receive no notification — they simply do not  
receive VCIs from that buyer. The buyer's ban list is never  
exposed to any seller or third party.

Sellers cannot maintain a ban list. They do not know the  
buyer's identity during the ARA phase.

**Seller Offer — Required Fields:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `vci_reference` | string | SHA-256 hash of the VCI | `sha256:a3f9...` |
| `seller_id` | string | Certified node identifier | `NODE:AR:00123` |
| `unit_price` | decimal | Final price, taxes inclusive | `899.99` |
| `currency` | ISO 4217 | Offer currency | `USD` |
| `fulfillment_mode` | enum | `pickup` / `delivery` | `delivery` |
| `delivery_days` | integer | Maximum calendar days | `3` |
| `delivery_area` | string | Coverage confirmed | `AR:CABA` |
| `warranty_months` | integer | Warranty period | `12` |
| `offer_signature` | string | Cryptographic signature | `sig:...` |

**Seller Offer — Optional Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `pickup_address` | string | Required if `fulfillment_mode: pickup` |
| `stock_confirmed` | boolean | Units available at time of offer |
| `nice_to_have_met` | array | nice_to_have attributes fulfilled |
| `value_added` | string | Additional services (installation, etc.) |
| `financing_available` | boolean | Installment payment available |

**Offer validation rules:**
- `fulfillment_mode` must intersect with VCI `delivery_accepted`
- `unit_price` validated locally against buyer's `max_price` —  
  offers exceeding max_price are silently discarded before ranking
- `offer_signature` must verify against seller's registered public key
- `vci_reference` must match an active VCI — expired references rejected
- **`max_offers_per_seller_per_vci: 1`** — a seller may submit exactly  
  one offer per active VCI. Amendments or resubmissions are rejected  
  by the network. This closes the inference attack vector where a seller  
  approximates `max_price` via iterative price descent across multiple  
  offer attempts on the same VCI.
- Seller identity never revealed to competing sellers or buyer during ARA

---

### 4. Just-In-Time Identity Release (JIT)

Buyer identity and logistics data are encrypted at VCI issuance  
and remain inaccessible to all parties — including the protocol  
operator — until the Settlement Click occurs.

**Technical mechanism:**

1. At certification, each seller node generates a session keypair.  
   The public key is registered on the seller node.

2. At VCI issuance, the protocol encrypts the buyer identity payload  
   using the public keys of all eligible sellers. Each seller receives  
   an individually encrypted version decryptable only by their  
   private key.

3. During the ARA phase, no party can access buyer identity in plaintext.

4. Upon Settlement Click, the encrypted payload is released  
   exclusively to the winning seller. The winning seller decrypts  
   it with their private key.

5. All other sellers' encrypted copies are scheduled for  
   `DATA_PURGE` (see Settlement Flow, Section 5).

**JIT enables:**
- Buyer anonymity throughout the competitive phase
- Elimination of identity-based price discrimination
- Demand-side sovereignty over personal data

---

### 5. Settlement Flow — The Handshake

The Settlement Click initiates a deterministic event-driven  
state machine. Each state transition is triggered by confirmation  
of the previous step — not by a wall clock. Timeouts shown are  
maximum durations per state, not scheduled absolute times.  
If an event arrives before the timeout, the flow advances immediately.

**Retry policy:** each network operation retries up to 3 times  
with exponential backoff (1s, 2s, 4s) before declaring failure.  
**Network partition behavior:** conservative — on unresolvable  
partition, funds are released and VCI is aborted. Buyer capital  
protection takes priority over transaction completion.

```
STATE: SETTLING
  trigger:    Settlement Click received
  action:     ARA generates signed Settlement Token (ST)
  timeout:    immediate
  on_success: → STATE: POP_CHECK

STATE: POP_CHECK
  trigger:    ST generated
  action:     Level 2,3,4: Financial Oracle confirms funds locked
              Level 0,1: auto-confirmed, no oracle required
  timeout:    max 10s (3 retries, exponential backoff: 1s, 2s, 4s)
  on_success: → STATE: IDENTITY_RELEASE
  on_failure: → VCI_ABORTED, funds released, buyer notified

STATE: IDENTITY_RELEASE
  trigger:    PoP confirmed
  action:     Buyer identity payload released to Postor 1 only
              Fulfillment authorized. VCI state → SETTLED_PENDING
  timeout:    max 5s
  on_success: → STATE: SELECTIVE_PURGE

STATE: SELECTIVE_PURGE
  trigger:    Identity released
  action:     Sellers ranked 3..N → DATA_PURGE immediate
              Postor 2 → STANDBY (payload retained, no ST access)
  timeout:    max 10s broadcast window

STATE: ACK_WINDOW
  trigger:    Selective purge broadcast confirmed
  timeout:    ST-TTL (configurable — see timing table below)
              B2C default: 15 min | B2B default: 30 min

  IF ACK_Accepted received from Postor 1:
    → VCI state: CONFIRMED
    → Postor 2 receives DATA_PURGE
    → Trust Score: normal transaction recorded for Postor 1

  IF ST-TTL expires without ACK (SELLER GHOSTING):
    → Postor 1 flagged: GHOSTING
    → SPS: Trust Score penalty applied immediately
    → Level 2+ funds: Released to buyer immediately
    → ST issued to Postor 2. ACK_WINDOW resets from zero.

    IF Postor 2 sends ACK_Accepted:
      → VCI state: CONFIRMED (resilience path)
      → DATA_PURGE broadcast issued
      → Trust Score: Reliability bonus applied to Postor 2
      → Buyer experiences no visible interruption

    IF Postor 2 also fails (DOUBLE GHOSTING):
      → VCI state: FAILED_SELLER_GHOSTING
      → SPS Postor 1: Maximum penalty
      → SPS Postor 2: Secondary penalty
      → Level 2+ funds: Released to buyer immediately
      → Buyer may re-emit a new VCI

STATE: LEVEL_0_1_POP (parallel, only for Level 0 and 1)
  trigger:    CONFIRMED state reached
  timeout:    max 30 min after settlement
  action:     Financial Oracle verifies payment completion
  on_failure: SPS emits penalty instruction against buyer
```


**Settlement timing — parametric by category and region:**

The timing values in the settlement flow are global defaults, not  
fixed constraints. Defaults serve as the protocol floor —  
implementations may extend them, never reduce below:

```
Global defaults (floor values):
  ST-TTL B2C:         15 minutes
  ST-TTL B2B:         30 minutes
  Identity release:   T+5s
  Selective purge:    T+10s
  PoP check L0,1:     T+30m

Category overrides (examples):
  Pharma:             ST-TTL 45 min (regulatory compliance)
  Real estate:        ST-TTL 72h (institutional settlement)
  High-frequency M2M: ST-TTL 5 min (autonomous agents)
```

Regional implementations may adjust defaults upward for local  
regulatory requirements without breaking protocol conformance.

**Formal VCI States:**

| State | Description |
|-------|-------------|
| `ACTIVE` | VCI broadcast, ARA in progress |
| `SETTLING` | Settlement Click received, ST generated |
| `SETTLED_PENDING` | ST activated, within buyer revocation window |
| `CONFIRMED` | ACK received, fulfillment authorized |
| `EXPIRED` | TTL elapsed without Settlement Click |
| `FAILED_SELLER_GHOSTING` | Double Ghosting — VCI aborted, funds released |

**Settlement Fingerprint:**

Every confirmed transaction generates an immutable fingerprint  
registered on-chain:

```
fingerprint = SHA-256(
  vci_id +
  seller_id +
  unit_price +
  identifier_type +
  identifier_value +
  timestamp +
  buyer_pubkey +
  seller_pubkey
)
```

The `identifier_type` and `identifier_value` fields enable  
anonymous market intelligence: aggregate pricing and volume  
statistics by product identifier, without exposing any buyer  
or seller identity. This is a deliberate forward-compatible  
design decision.

---

### 6. Smart Penalty System (SPS)

The SPS is an instruction layer, not a custody layer.  
O4DB™ does not hold or move funds. Upon a breach condition,  
the SPS emits a signed penalty instruction to the connected  
Payment Provider or Smart Contract, which executes enforcement  
under its own regulated framework.

**Penalty conditions:**

- Buyer commits and does not execute → penalty proportional to level
- Seller wins and does not fulfill → penalty on verified breach
- Seller violates buyer's `privacy_mode` post-JIT → immediate  
  decertification and SPS breach procedure
- Seller Ghosting (no ACK within ST-TTL) → Trust Score penalty,  
  graduated by recurrence (see Seller Trust Score section)

**Penalty parameters** are defined at VCI issuance and  
cryptographically accepted by all participating sellers  
at bid submission via their signed offer signature.

**Minimum PSP Integration Interface:**  
For a Payment Provider to be O4DB™-compatible at Level 2+,  
it must expose the following abstract interface:

```
PSP_Interface:
  hold(buyer_id, amount, currency, ttl)     → hold_reference
  confirm(hold_reference)                    → settlement_receipt
  release(hold_reference)                    → release_receipt
  penalize(hold_reference, amount, reason)   → penalty_receipt
```

PSPs implement this interface under their own regulated framework.  
O4DB™ does not dictate internal PSP architecture — only the interface  
contract required for protocol compatibility.

---

### 7. TTL Expiration — No Selection

If the TTL expires without a Settlement Click:

| Action | Detail |
|--------|--------|
| All seller offers | Permanently destroyed. No data retained. |
| Buyer identity payloads | DATA_PURGE across all seller nodes simultaneously. |
| Escrow funds | Released automatically. No manual intervention. |
| Seller notifications | Anonymous expiration notice. No buyer data included. |
| VCI record | Hash logged for anti-abuse monitoring. Content not retained. |
| Buyer penalty | Only if Level ≥ 2 and classified as buyer abandonment. |

**TTL Extension:**  
A buyer may extend the TTL once, up to the original duration,  
provided no offers have been received or all received offers  
have been explicitly declined. Notifies all eligible sellers.

**Abandonment vs. no offers received:**
- **No offers received** → TTL expires with zero participation.  
  No buyer penalty regardless of commitment level.
- **Offers received, no selection** → classified as buyer abandonment.  
  SPS penalty may apply depending on commitment level.

---

### 8. Buyer Privacy Mode

Post-transaction data use policy is defined once in the Buyer  
Profile and travels in every VCI as `privacy_mode`. It is  
enforced at JIT release and is cryptographically binding  
on the winning seller via the Settlement Token.

| Mode | Post-Transaction Data Policy |
|------|------------------------------|
| `private` | Transaction execution only. No marketing, retargeting, or CRM incorporation permitted. |
| `standard` | Transaction plus related commercial communications from winning seller. |
| `open` | Winning seller may use data freely, including future personalized offers. |

**Default: `private`**

**Permitted in all modes:**
- Order fulfillment and logistics
- Warranty and returns processing
- Transaction-specific customer support

**Prohibited in `private` mode:**
- Retargeting or remarketing campaigns
- CRM database incorporation for marketing
- Third-party data sharing
- Behavioral profiling beyond the transaction

Violation triggers immediate network decertification and  
SPS breach procedure, regardless of commitment level.

**Cryptographic Privacy Commitment (ACK-bound):**

At the moment of sending `ACK_Accepted`, the seller signs a structured  
privacy commitment permanently attached to the Settlement Token  
as `privacy_commitment_proof`. This converts a contractual obligation  
into a cryptographically verifiable one.

```
ACK_Accepted payload (privacy fields):
  vci_reference:        SHA-256 of the original VCI
  settlement_token_id:  ID of the received ST
  timestamp:            ACK emission moment
  privacy_commitment:   "I cryptographically commit that buyer data
                         received via JIT release will be used solely
                         for fulfillment of this transaction under
                         privacy_mode: [MODE]. Incorporation into
                         any external system beyond this scope is
                         prohibited and constitutes a protocol breach."
  privacy_mode_ref:     SHA-256 of the privacy_mode declared in VCI
  ack_signature:        seller's cryptographic signature over
                        all fields above
```

The `ack_signature` covers the entire payload — no individual field  
can be repudiated without invalidating the signature on all others.

**What this proves:** that the commitment existed, was accepted  
voluntarily, and was cryptographically bound to this exact transaction.  
**What this does not prove:** internal CRM compliance — that remains  
subject to ex post dispute and SPS enforcement if reported.  
This is the maximum technically achievable without violating  
the decentralization premise.

---

### 9. Agent Autonomy Levels (Internal Agent Specification)

Autonomy level is an internal parameter of the buyer's agent.  
It does not travel in the VCI. This is a deliberate design  
decision: exposing the autonomy level to sellers would enable  
price manipulation against unmonitored agents, breaking the  
integrity of the anonymous auction.

The following four levels define the required behavior for  
any O4DB™-compatible agent implementation:

**Complexity is opt-in, not mandatory:**  
A buyer operating at Level 0 never sees weights, formulas, or  
configuration screens. The agent applies sensible defaults and  
presents a ranked list. The buyer clicks. That is the complete  
interaction for the average user.

Advanced configuration — weight matrices, trust floors, delivery  
preferences, ban lists — is available but never required. The agent  
learns implicit preferences from settlement patterns over time and  
can suggest profile updates. Complexity surfaces only when the  
buyer actively seeks more control.

**Level 0 — Manual (Assisted)**  
The agent resolves the demand and presents ranked offers.  
The human makes all decisions. Settlement Click requires  
human authentication (biometric or password).  
*Use case: high-value purchases, subjective decisions.*

**Level 1 — Shadowing (Recommendation)**  
The agent analyzes offers, applies the buyer's V function,  
and surfaces the recommended winner with full justification.  
Human retains veto via single confirmation click.  
*Use case: standard consumer purchases.*

**Level 2 — Guardrail (Restricted Execution)**  
Buyer defines Hard Constraints (e.g., `price < $500 AND trust_score > 0.9`).  
Agent holds a session-scoped delegated signing key with limited  
spend authority. Executes autonomously only when all constraints  
are satisfied. Proof of Conformity is attached to every ST.  
*Use case: industrial supplies, commodity electronics.*

**Level 3 — Agentic (Full Autonomy)**  
Agent manages a declared budget and time window. May withhold  
purchase if market conditions are unfavorable and re-emit  
a new VCI later. Full signing key autonomy within a  
Trusted Execution Environment (TEE).  
*Use case: automated inventory replenishment, M2M arbitrage.*

**Digital Power of Attorney (dPoA):**

The agent operates as a digital mandatary. The buyer  
(principal) is fully responsible for all agent actions  
executed within the configured parameters. This is legally  
equivalent to a power of attorney in all major jurisdictions:  
actions of the mandatary within granted scope bind the mandant.

**Jurisdictional disclaimer:**  
The validity of the dPoA as a legal instrument depends on local  
legislation. O4DB™ provides the technical infrastructure for  
cryptographic mandate delegation. Legal adoption and enforceability  
are subject to the laws of each jurisdiction. Implementors operating  
in regulated markets must obtain independent legal counsel regarding  
dPoA validity before deploying Level 2 or Level 3 agents in  
commercial contexts.

| Scenario | Agent Action | Legal Status | SPS Consequence |
|----------|-------------|--------------|-----------------|
| Nominal | Within parameters | Mandate fulfilled | Irrevocable |
| User error | Parameters incorrectly set | Principal negligence | Full penalty if reversed |
| Agent bug | Outside declared parameters | Mandate exceeded | SPS suspended, audit opened |
| Ghosting | No ST post-win | Node breach | Penalty to buyer |

**Proof of Conformity:**

At Level 2 and 3, the agent attaches a Proof of Conformity  
to every ST — a hash of the active constraint snapshot  
validated against the winning offer:

```
conformity_proof = SHA-256(constraint_snapshot_hash + offer_hash + timestamp)
```

If a dispute arises, the SPS oracle compares the ST's  
conformity proof against the buyer's registered constraints.  
A verifiable mismatch (e.g., `paid_price > max_price`) triggers  
automatic SPS suspension and audit — without requiring  
human arbitration.

**Constraint Versioning:**

When an agent emits a VCI at Level 2 or 3, the active  
constraint set is sealed with a timestamp. The sealed snapshot  
governs that VCI for its entire lifecycle. Post-emission  
constraint changes do not affect active VCIs. This closes  
the vector where a buyer modifies constraints after execution  
to manufacture a dispute.

**Kill Switch (mandatory for Level 2 and 3 implementations):**

Any O4DB™-compatible agent operating at Level 2 or above  
must implement a Kill Switch that invalidates the delegated  
signing key at the protocol layer immediately upon activation.  
Transactions already signed continue to their natural conclusion.  
New VCI emissions are blocked until the buyer re-establishes  
the delegation.

**Rate Limiting (declared in agent profile):**

```
agent_vci_rate_limit:
  max_per_hour:          10
  max_per_day:           50
  max_concurrent_active: 3
```

Violations are rejected by the protocol before broadcast.  
The Kill Switch addresses catastrophic failure; Rate Limiting  
prevents runaway behavior before it escalates.

**Revocation Window:**

Even at Level 3, the buyer may configure a pre-ST grace  
period (5–60 minutes) between the agent's Settlement Click  
and actual ST emission. During this window, the VCI state  
is `SETTLED_PENDING`. The seller receives a win notification  
and may begin non-irreversible logistics preparation.  
The buyer may cancel without penalty within this window.  
Once the ST is emitted, execution is irrevocable.

---

### 10. Seller Trust Score (STS)

The Trust Score is not a rating system. It is a real-time  
integrity indicator of a seller's commitment to protocol compliance.

**Trust Score Registry — Federated Ledger:**

The Trust Score registry is not a centralized database. It operates  
as a federated ledger where multiple independent Certifying Authorities  
(CAs) each sign their portion of the trust data. No single CA controls  
the full registry. The buyer's agent consults a public decentralized  
registry — analogous to the SSL certificate chain of trust — where  
each CA's signature can be independently verified.

```
Registry architecture:
  CA_1 signs: [seller_id, score_component, timestamp, CA_1_signature]
  CA_2 signs: [seller_id, score_component, timestamp, CA_2_signature]
  ...
  Consensus:  Raft protocol among permissioned CA set
  Quorum:     majority(N/2 + 1) CAs must agree for score to be valid
  Reads:      any CA can serve read requests (eventual consistency)
```

**Consensus mechanism: Raft**  
The CA set uses Raft for leader election and log replication.  
Raft is appropriate for a small, known, permissioned set of CAs  
(target: 5–11 nodes in v1.0). It provides strong consistency  
for writes and graceful degradation when minority of CAs fail.  
PBFT is explicitly rejected as too heavyweight for this use case.

**Permissioned CA set:**  
In v1.0, CAs are permissioned — admission requires protocol  
certification. Any entity may apply to become a CA; admission  
is governed by the certification program. This is not a public  
blockchain — it is a federated ledger with known, accountable  
participants.

A seller's Trust Score is the Raft-committed consensus of CA  
signatures. If a minority of CAs go offline, the registry  
continues operating. If the majority is lost, the registry  
enters safe read-only mode — scores remain readable,  
updates are queued until quorum is restored.

**Formula:**

$$S = (G \cdot 0.3) + (H \cdot 0.7) - P$$

Where:
- **G** = Gravity (external reputation, verified and normalized)
- **H** = History (internal protocol performance)
- **P** = Penalties (direct deductions for protocol violations)

**H — Internal History (three axes):**

$$H = (\text{Precision} \cdot 0.5) + (\text{Velocity} \cdot 0.3) + (\text{Compliance} \cdot 0.2)$$

| Axis | Definition |
|------|------------|
| Precision | Delivered product identifier matches VCI identifier. Verified cryptographically against Settlement Fingerprint. |
| Velocity | Time from ST reception to ACK_Accepted, normalized against category ST-TTL. Faster ACK = higher score. |
| Compliance | Ratio of disputes resolved in seller's favor over total disputes received. |

**G — Gravity Import (cold start mechanism):**

New sellers may import external reputation from verified platforms  
(Mercado Libre, Amazon, eBay) via Verified Oracle. Minimum  
requirements for Gravity Import eligibility:

```
account_age:        ≥ 12 months
min_transactions:   ≥ 50 completed
dispute_rate:       ≤ 5%
legal_entity:       unique — verified against registration number
```

**Explicit consent requirement:** Before Gravity Import is executed,  
the seller must provide written authorization for O4DB™ to access  
their external transaction history. This authorization is contractually  
binding, scoped to the certification process only, and subject to the  
privacy policies of both O4DB™ and the source platform. Gravity Import  
without documented seller consent is a protocol violation.

If requirements are not met, the seller enters as `SANDBOX_NEW`  
with `S = 0.10`, `max_commitment_level: 1`, and  
`max_concurrent_active_vci: 3`. Graduates to `CERTIFIED_ACTIVE`  
automatically upon 25 successful O4DB™ transactions with `S ≥ 0.75`.

The Gravity weight decays as internal history accumulates:

```
G_weight = max(0.30, 1.0 - (o4db_transactions × 0.02))
```

After 35 O4DB™ transactions, G stabilizes at 30% permanently.  
The external reputation never reaches zero — it provides  
permanent context. It never dominates — internal behavior  
governs.

**Sybil Protection:**

A single legal registration number cannot onboard multiple  
seller accounts. Gravity Import from accounts failing minimum  
requirements is rejected. Fabricated external reputation  
enters the network only as `SANDBOX_NEW` — never as a  
full-trust certified node.

**Score Freeze — Force Majeure Protection:**

A seller experiencing documented external disruption may request  
a temporary halt to score decay without resetting their history.

```
Score Freeze process:
  1. Seller submits signed freeze_request:
       reason_category: supply_disruption | regulatory | force_majeure
       evidence_hash:   SHA-256(supporting_documentation)
       requested_days:  1–30

  2. Request broadcast to CA set via Raft

  3. CA majority vote within 48h:
       approved: decay paused for requested duration
       rejected: normal decay continues, reason logged

  Constraints:
    max_duration:    30 days per freeze
    max_per_year:    1 freeze per calendar year
    effect:          decay paused only — score neither
                     improves nor degrades during freeze
    no_human_committee: CAs vote algorithmically via Raft,
                        no manual review required
```

Score Freeze does not improve the score — it only halts  
temporary deterioration caused by verifiable external events.

**Recency (lambda decay):**

History is a weighted moving average favoring recent behavior:

```
H = Σ(transaction_result × e^(-λ × days_elapsed)) / Σ(e^(-λ × days_elapsed))
```

Lambda is defined per category by the protocol — not configurable  
by the seller:

```
Consumer electronics (v1.0):  λ = 0.05  (~20 days to significant decay)
Automotive / B2B:             λ = 0.02  (~50 days)
Industrial components:        λ = 0.01  (~100 days)
```

High-velocity categories apply aggressive decay. A seller  
who pauses activity and returns months later finds a degraded  
score, not a preserved one. This closes the exit-scam vector:  
building reputation over time and exploiting it in a final burst.

**Penalty Scale:**

| Infraction | Penalty | Additional Consequence |
|------------|---------|------------------------|
| Ghosting (1st) | P += 0.15 | Recorded in history |
| Ghosting (2nd in 24h) | P += 0.30 | Auto-suspension 48h |
| Ghosting (3rd in 30d) | P += 0.50 | Decertification review |
| Fulfillment Fraud (EAN mismatch) | P += 0.50 | Forced collateral, next 10 sales |
| Privacy Mode violation | P += 0.60 | Immediate decertification |
| Out-of-protocol contact | P += 0.40 | 7-day suspension |

Recovery rate: `P -= 0.01` per consecutive successful transaction.  
No manual history clearing under any circumstances.

**Seller States:**

| State | Condition | Restrictions |
|-------|-----------|--------------|
| `SANDBOX_NEW` | New entrant, requirements not met | Level ≤ 1, ≤3 concurrent VCI |
| `CERTIFIED_ACTIVE` | S ≥ 0.75, normal operation | None |
| `CERTIFIED_WATCH` | 0.60 ≤ S < 0.75 | Visible in ranking, score displayed |
| `SUSPENDED_TEMP` | Ghosting or Hard Penalty | No participation for N days |
| `COLLATERAL_REQUIRED` | Fraud detected | Level 2 forced, next 10 sales |
| `DECERTIFIED_TEMP` | Requires manual review | Participation blocked |
| `DECERTIFIED_PERMANENT` | Fraud recidivism | Permanent expulsion |

**Dispute Resolution — Evidence Hash:**

The protocol defines three dispute categories with distinct  
resolution paths and SPS consequences:

| Category | Trigger | SPS Target |
|----------|---------|------------|
| `FULFILLMENT_FRAUD` | Delivered identifier ≠ VCI identifier | Seller |
| `PRODUCT_CONDITION` | Product arrived damaged or incomplete | Seller (if no dispatch proof) |
| `LOGISTICS_DAMAGE` | Damage attributable to carrier in transit | Carrier — seller exonerated |

**`DISPUTE_OPEN` fields:**

```
DISPUTE_OPEN:
  dispute_reference:   Settlement Fingerprint hash
  dispute_category:    FULFILLMENT_FRAUD | PRODUCT_CONDITION | LOGISTICS_DAMAGE
  evidence_hash:       SHA-256(unboxing_media + timestamp)
  claimed_identifier:  identifier received (per buyer) — FULFILLMENT_FRAUD only
  expected_identifier: identifier from original VCI — FULFILLMENT_FRAUD only
  timestamp:           DISPUTE_OPEN emission time
```

**Resolution timeline — `FULFILLMENT_FRAUD` and `PRODUCT_CONDITION`:**

- **T+0h** — Seller notified. VCI state → `DISPUTED`
- **T+48h** — Seller presents `counter_evidence_hash`  
  (dispatch scan log with correct identifier and packaging photos):  
  Match → `DISPUTE_CLOSED_SELLER_WIN`  
  No match or no response → `DISPUTE_CLOSED_BUYER_WIN`

**Resolution timeline — `LOGISTICS_DAMAGE`:**

- **T+0h** — Seller notified. VCI state → `DISPUTED`
- **T+72h** — Seller presents logistics proof:
  ```
  dispatch_hash:     SHA-256(packaging_photos + timestamp_at_dispatch)
  tracking_number:   carrier tracking reference
  carrier_report:    carrier damage acknowledgment (if available)
  ```
  If dispatch_hash is valid and predates delivery timestamp:  
  → `DISPUTE_CLOSED_LOGISTICS` — seller exonerated  
  → Buyer reimbursed (cost attributed to carrier/shipping insurance)  
  → Seller Trust Score: no penalty  
  If seller cannot prove intact dispatch:  
  → `DISPUTE_CLOSED_BUYER_WIN` — seller bears responsibility

`DISPUTE_CLOSED_BUYER_WIN` consequences:
- Immediate buyer reimbursement
- `P += 0.50` on seller Trust Score
- Forced collateral on next 10 sales
- `FULFILLMENT_FRAUD` only: identifier registered in protocol blacklist

`DISPUTE_CLOSED_LOGISTICS` — what the protocol does NOT do:  
O4DB™ exonerates the seller from SPS penalties. It does not  
manage the claim against the carrier. That remains the seller's  
operational responsibility under their own logistics contract.

`DISPUTE_ABUSE` protection:  
Buyers with more than 3 disputes lost in 90 days receive  
a flag. Repeated false disputes trigger commitment level  
restrictions on future VCI emissions.

**Post-Settlement Blind Feedback:**

After a VCI reaches `CONFIRMED` state, the protocol sends a  
structured feedback signal to all non-winning sellers. This  
educates sellers to become more competitive without revealing  
confidential information.

```
feedback_type: PRICE_DELTA
  message: "Your offer was ~X% above the winning offer"
  X: rounded to nearest 5% (noise to prevent absolute price inference)

feedback_type: TRUST_DELTA
  message: "Your offer was price-competitive but ranked below
            due to Trust Score difference"

feedback_type: FULFILLMENT_DELTA
  message: "Your offer was ranked below due to delivery time"
```

**What is never revealed:**
- Winning price in absolute value
- Identity of the winning seller
- Buyer's `max_price`
- Total number of offers received

**Timing:** feedback emitted only after `CONFIRMED`.  
Never during `SETTLING` or `SETTLED_PENDING`.  
No feedback emitted if VCI ends in `FAILED_SELLER_GHOSTING`.

The 5% rounding on `PRICE_DELTA` prevents inference attacks  
where a seller accumulates feedback from multiple similar VCIs  
to reverse-engineer the winning price distribution.

---

**Buyer Hard Floor:**

The buyer may set a minimum Trust Score threshold in their profile.  
Sellers below this threshold are excluded from ARA participation  
before ranking begins:

```
trust_floor: 0.75  (default)
trust_weight (wₛ): 0.20  (weight of S in V function, default)
```

The Trust Score enters both as a filter (Hard Floor) and  
as a variable in the selection function, giving the buyer  
full control over the risk-vs-price tradeoff.

---

## Network Integrity

Three mechanisms protect the network from scraping, price fishing,  
and fake participation. They operate in combination with zero  
added latency to the core ARA flow.

### Invisible Max Price

The `max_price` field never travels to sellers in any form.  
The Public VCI carries a `price_token` — an ARA-only encrypted  
value. The ARA decrypts it internally to validate offers.  
Sellers make offers based on their own pricing logic,  
without knowing the buyer's ceiling.

A competitor operating a node to harvest demand intelligence  
obtains: the product identifier, geographic scope, and  
commitment level. They never obtain the price ceiling —  
making the intelligence structurally incomplete and  
commercially useless for algorithmic pricing.

The buyer decrypts `price_token` locally. No server holds  
`max_price` in plaintext at any point during the ARA phase.

### Seller Network Score (Response-Ratio Throttling)

The protocol tracks each seller node's participation quality  
over a rolling 30-day window:

```
network_score = (response_ratio  × 0.30) +
                (conversion_ratio × 0.40) +
                (sla_score        × 0.30)

response_ratio:   VCIs_responded / VCIs_received
conversion_ratio: offers_won / offers_submitted
sla_score:        competitive_offers / offers_submitted
```

An offer is competitive if:

```
unit_price ≤ winning_price × 1.15
```

The ARA calculates `sla_score` retrospectively after each  
settlement. Sellers submitting systematically non-competitive  
offers degrade their `network_score` without a single  
formal penalty.

| network_score | VCI Traffic Received |
|---------------|----------------------|
| ≥ 0.60 | Full traffic |
| 0.40 – 0.59 | 70% of available traffic |
| 0.20 – 0.39 | 40% of available traffic |
| < 0.20 | Priority VCIs only |

**Warm-up protection:** During `SANDBOX_NEW` (first 25 transactions),  
`network_score` is not measured and throttling is not applied.  
New sellers start with full traffic access.

### Proof of Category

Sellers receive VCIs only from categories validated in their  
Gravity Import at certification. Categories are not self-declared —  
they are verified against the seller's external transaction history.

A node attempting to register in unrelated categories without  
supporting history enters as `SANDBOX_NEW` for each additional  
vertical, with a separate warm-up requirement.

---

## Buyer Execution Score (BES)

The BES protects the seller network from buyers using the protocol  
as a price intelligence tool without purchase intent.

```
BES = VCIs_settled / VCIs_emitted  (rolling 30-day window)
```

**VCIs that expire with zero offers received are excluded from  
the BES denominator.** The buyer cannot be penalized for  
absence of supply.

| BES | Access |
|-----|--------|
| ≥ 0.40 | Full access to all commitment levels |
| 0.20 – 0.39 | Level 0 and 1 require TTL justification |
| < 0.20 | Level 0 blocked. Minimum Level 1 with pre-auth. VCI rate limit reduced to 50%. |

The threshold of 0.40 is deliberately conservative — a buyer who  
occasionally explores without purchasing does not trigger restrictions.  
Only systematic non-execution patterns activate the BES mechanism.

**Latency:** BES is a cached score updated asynchronously every  
24 hours. Zero latency added to VCI emission or ARA processing.  
The check occurs at VCI submission, not during the auction.

---

## Buyer Profile

Configured once at registration. Any field may be overridden  
per VCI without modifying profile defaults.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `privacy_mode` | enum | `private` | Post-transaction data policy |
| `delivery_accepted` | array | `[delivery]` | Accepted fulfillment modalities |
| `delivery_area` | string | Buyer's country (ISO 3166) | Default geographic scope |
| `banned_sellers` | array | `[]` | Permanently excluded seller nodes |
| `trust_floor` | decimal | `0.75` | Minimum seller S score for ARA participation |
| `trust_weight` | decimal | `0.20` | Weight of S in V function |

---

## Integration Model

Existing marketplaces, retailers, and logistics operators may  
participate in the O4DB™ network as certified seller nodes  
without replacing their existing infrastructure.

Integration is achieved via the O4DB™ API Gateway — a  
translation layer that:

- Receives broadcast VCIs from the network
- Translates demand parameters into the seller's native query format
- Converts seller responses into valid O4DB™ offers
- Enforces the buyer's `privacy_mode` at JIT release
- Routes SPS penalty instructions via the seller's existing  
  payment infrastructure

**What large platforms contribute:**
- Real-time product catalog and stock
- Established logistics and delivery infrastructure
- Dispute resolution and returns systems
- Existing buyer and seller trust scores (portability via Gravity Import)
- Premium membership benefits declared as `value_added` in offers

**What the protocol guarantees to large platforms:**
- Qualified demand with verified financial commitment
- Anonymous competitive environment — no price exposure to competitors
- Stealth liquidation capability — aggressive pricing to specific  
  buyers without public catalog exposure
- B2B procurement access without dedicated sales infrastructure

The buyer receives offers from large platforms and independent  
sellers in a single ranked dashboard, scored by their own  
declared criteria — not by the seller's algorithm.

---

## Selection Logic

Offers are ranked using a weighted value function declared  
by the buyer at VCI issuance:

$$V = \sum_{i=1}^{n} (w_i \cdot A_i) + (w_s \cdot S) - P$$

Where:
- **V** = perceived value score
- **wᵢ** = buyer-assigned weight for attribute i (Σwᵢ + wₛ = 1)
- **Aᵢ** = normalized attribute value, scaled to [0,1]
- **wₛ** = buyer-assigned weight for Trust Score
- **S** = seller Trust Score (see Section 10)
- **P** = unit price, normalized to the same scale

**Normalization:**  
All Aᵢ values are normalized to [0,1] before scoring.  
Normalization scales are declared in the VCI at issuance  
and applied identically to all competing offers within  
that ARA session. The protocol specifies the method, not  
the scale. Cross-session and cross-regional comparability  
is an implementation-layer concern. Implementors are encouraged  
to publish their normalization scales as open issues in the  
repository to build toward community consensus.

**Example:**
- Delivery 2 days → 0.90 (faster = higher)
- Warranty 24 months → 0.80
- Trust Score 0.94 → 0.94 (already normalized)

The highest V wins. Deterministic. No discretion.

---

## Anti-Collusion Mechanism

The protocol cannot prevent sellers from communicating outside the  
network — that is the domain of antitrust regulation, not protocol  
design. What the protocol can do is make collusion statistically  
detectable and permanently recorded.

**Detection threshold:**

```
Collusion Alert triggers when:
  sellers_involved:     ≥ 3 sellers in the same category
  price_correlation:    Pearson correlation > 0.85
  consecutive_VCIs:     across ≥ 10 consecutive VCIs in that category
  window:               rolling 30-day observation window
```

When the threshold is met, the ARA records a `COLLUSION_ALERT`  
flag in the Settlement Fingerprint of the triggering VCI.  
This flag is:
- Immutable — cannot be removed once recorded on-chain
- Public — visible to any party querying the ledger
- Auditable — regulators and competition authorities can extract  
  all flagged VCIs for investigation

**What the protocol does not do:**  
O4DB™ does not sanction sellers for collusion. Legal enforcement  
is the exclusive domain of competition regulators. The protocol  
provides the evidence trail — permanently, cryptographically,  
without requiring human intervention to generate it.

**Natural market pressure:**  
Colluding sellers with artificially high prices will eventually  
lose to a competitive entrant. Their `conversion_ratio` degrades,  
their Network Score drops, and their VCI traffic throttles.  
The protocol self-regulates economically even without legal action.

---

## Incentive Model

**Buyer-side:** SPS penalties for non-execution after commitment.  
BES restrictions for systematic non-execution patterns.

**Seller-side:** Trust Score degradation and financial penalties  
for Ghosting, fulfillment fraud, and privacy violations.  
Network Score throttling for low-quality participation.

**Anti-price-fishing (seller-side):** Invisible Max Price makes  
demand intelligence structurally incomplete. Network Score  
throttles nodes that receive VCIs without responding genuinely.

**Anti-price-fishing (buyer-side):** BES restricts access for  
buyers with systematic non-execution patterns. Invisible  
Max Price means buyers who fish for prices obtain only  
their own confirmation — never competitors' ceilings.

---

## Open Questions

- Optimal solvency attestation architecture for cross-border VCIs
- Anti-collusion mechanisms for oligopolistic seller markets
- Proof-of-independence for concentrated verticals
- Regulatory constraints across jurisdictions (PSD2, GDPR, LATAM)
- Multi-rail payment interoperability (Stripe, SWIFT, stablecoins)
- Seller adoption incentive design for network bootstrap
- Dynamic normalization scale standardization across categories
- API Gateway schema standardization for platform integration
- Lambda parameter calibration methodology per vertical
- BES threshold calibration across buyer behavior segments
- Inventory Affinity minimum competition threshold calibration  
  per category (default N=3 — empirical validation required)
- Post-Settlement Blind Feedback: optimal noise level for  
  PRICE_DELTA rounding (5% default — subject to market testing)
- HPKE implementation library recommendations per platform  
  (browser, mobile, server, TEE)
- Verified Oracle certification standard for Gravity Import
- Network Score warm-up period optimal length
- Competitive offer threshold (1.15x) empirical validation
- Cold start incentive design: how to attract the first sellers  
  before VCI volume exists (early adopter partner program,  
  synthetic demand simulation, or aggregator integration)

---

## Known Limitations (v1.1.5)

**SPS enforcement below Level 2** is contractual, not technical.  
Sellers participating at Level 0 and 1 accept binding terms of use  
at certification time. These terms are the enforcement mechanism  
for contractual penalties.

**SPS enforcement at Level 2 depends on PSP cooperation.**  
The SPS emits a signed penalty instruction, but execution requires  
the connected Payment Provider to honor that instruction under a  
pre-existing contractual agreement. If a PSP declines to enforce  
SPS instructions, Level 2 degrades effectively to Level 1 in terms  
of technical enforcement. Establishing PSP agreements that explicitly  
bind them to SPS penalty execution is a prerequisite for production  
deployment at Level 2 and above.  
Level 0 and 1 participants accept that penalty execution  
depends on legal agreement, not automated financial mechanics.

**Normalization scales** are session-scoped. The protocol  
does not define universal scales across categories or  
geographies. Cross-market comparability is an  
implementation concern.

**Collusion in oligopolistic markets** is partially mitigated by  
statistical anti-collusion detection (Pearson correlation threshold).  
Legal entity uniqueness reduces but does not eliminate coordinated  
behavior risk among independent sellers.

**Price fishing** via low-commitment VCIs is a known attack vector.  
Partial mitigation exists via BES (opt-in) and commitment level  
requirements. Full mitigation requires empirical calibration of  
BES thresholds after pilot deployment data is available.

**Physical delivery verification** relies on buyer acknowledgment  
or third-party logistics data. The protocol does not operate a  
delivery verification layer; this is delegated to the application layer.

**Broadcast encryption scalability:** The reference implementation  
encrypts buyer identity individually per eligible seller node.  
With the 6-criteria pre-broadcast filter, realistic recipient counts  
of 10–50 nodes per VCI make this feasible at current scale.  
Performance degrades beyond ~1,000 certified nodes.

**Relay scalability:** The reference implementation uses SQLite as  
persistence layer. Stress tested at 100 concurrent nodes: VCI submit  
latency p50=2.04s, p95=5.1s, max=6.9s. Acceptable for production  
at current network size. Migration to PostgreSQL or a write-queue  
architecture is required for >50 sustained concurrent nodes.

**Privacy mode enforcement** post-JIT is contractual. The protocol  
carries the buyer's declared privacy mode in the VCI and binds it  
to the Settlement Token, but technical enforcement of data-use  
restrictions post-delivery is outside protocol scope.

**Post-transaction disputes** — warranty claims, returns,  
delivery failures — are delegated to the winning seller's  
infrastructure or integrated platform. O4DB™ provides  
the Evidence Hash mechanism as input to external dispute  
resolution but does not operate a dispute resolution layer.

**Seller Trust Score** formal specification is complete.  
The Verified Oracle (external reputation import) interface  
is defined but oracle certification requirements are  
an open research question pending pilot deployment.

**BES threshold calibration** (0.40 default) and **Network Score  
thresholds** (0.60 / 0.40 / 0.20) are based on architectural  
reasoning, not empirical data. Adjustment expected after  
pilot deployment data is available.

---

## G2B Extension — Government-to-Business Procurement

Government entities are the ideal O4DB™ buyer profile: they know  
exactly what they need (closed technical specifications), have  
approved budgets (verifiable solvency), and are legally required  
to conduct competitive, transparent procurement.

O4DB™ resolves the core failure of traditional public procurement:  
suppliers systematically bid at the maximum available budget because  
the budget is public. With Invisible Max Price, suppliers bid their  
genuine best price — they do not know the ceiling.

**Additional VCI fields for G2B:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `buyer_type` | enum | `government` / `private` | `government` |
| `procurement_law` | string | Applicable legal framework | `AR:LeyContrataciones2023` |
| `contracting_authority` | string | Official name of the government entity | `Ministerio de Salud AR` |
| `tender_reference` | string | Official procurement reference number | `EXP-2026-00123` |

**G2B behavioral overrides:**

```
privacy_mode:         open (forced — public procurement is transparent)
commitment_level:     ≥ 2 (required — government commitments must be financial)
settlement_approval:  Level 0 mandatory (human authorization required)
ttl:                  configurable in days (not minutes) for tender windows
fingerprint:          includes contracting_authority in plaintext
                      (public audit requirement)
```

**Settlement Fingerprint for G2B:**  
The fingerprint includes `contracting_authority` and `tender_reference`  
in plaintext — unlike private transactions where all buyer data is  
hashed. This enables public audit of government procurement without  
exposing private buyer data in other transaction types.

**Audit trail:**  
Every G2B transaction produces a publicly queryable Settlement  
Fingerprint. Regulators, journalists, and citizens can verify  
that the procurement occurred, at what price, and from which  
certified seller — without accessing any additional private data.

G2B full specification, including multi-lot procurement and  
framework agreements, is planned for a future version.

---

## Future Category Specifications

The field structures defined above apply to Consumer Electronics (v1.1.5).  
The following categories are recognized and will be formally  
specified as independent RFCs prior to implementation:

| Category | Version | Key Additional Fields |
|----------|---------|-----------------------|
| Automotive / Heavy Transport | v1.5 | OEM_PN + manufacturer, pack_quantity, accept_equivalents |
| Pharma | v1.5 | ATC code, lot_expiry_min, cold_chain, batch_number |
| Travel | v2.0 | IATA_ROUTE, flexibility_window, cabin_class, fare_conditions |
| Industrial Components | v2.0 | revision, compliance_cert, pack_quantity |
| Real Estate | v3.0 | parametric_only, inspection_window |

Field structures not listed — lot numbers, pack multiples,  
geographic market variants, certification requirements — are  
acknowledged as necessary and reserved for their respective  
category specifications.

---

## Non-Goals

O4DB™ does not aim to:

- Replace traditional e-commerce or eliminate marketplaces
- Disrupt discovery-driven retail
- Act as a financial intermediary or custody funds
- Provide dispute resolution as a service
- Operate as a marketplace, platform, or data broker

It proposes a complementary execution rail for pre-qualified demand —  
infrastructure that existing commerce actors can plug into,  
not compete against.

---

## Protocol Governance & Compliance

This specification is **NOT** a public domain document.  
It is a **Sovereign Open-Standard** managed exclusively by the Author.

- **Compliance:** Only nodes that strictly adhere to the v1.1.5 cryptographic  
  handshake and ARA logic can claim O4DB™ Compatibility.
- **Licensing:** All implementations, whether partial or full, are governed  
  by the **O4DB™ Community & Commercial License v1.1.5**.  
  See [LICENSE](./LICENSE) for full terms.
- **Community Tier:** Free for research and production use up to  
  **50 completed settlement operations per calendar month**.
- **Enterprise Tier:** Commercial license required above the threshold  
  or for integration into centralized marketplace infrastructure.
- **Prior Versions:** This document supersedes and revokes any previous  
  licensing offers or drafts, including any prior Creative Commons (CC)  
  mentions that may appear in earlier versions of this specification.

---

## How to Contribute

This specification welcomes community input via GitHub Issues and Pull Requests.

Contributions of particular interest:

- Game-theoretic analysis of ARA stability under various seller network configurations
- VCI schema formalization (JSON Schema, Protobuf, or equivalent)
- Seller eligibility filter implementation at scale
- Decentralized relay architecture proposals
- Anti-collusion mechanism design
- Normalization scale standardization proposals
- Privacy mode technical enforcement mechanisms
- Trust Score oracle certification requirements
- Regulatory mapping across target jurisdictions
- Category-specific identifier standard extensions

All accepted contributions are incorporated into the official specification  
at the Author's discretion. Contributors retain no IP rights over accepted changes.  
The Author retains sole authority over the canonical specification.

Please open an Issue or submit a Pull Request on GitHub.

---


---

## Stress Test Results

The relay has been validated under two independent stress test runs using `stress_test/o4db_stress_test.py`.

### v1.1.4 — 30 Buyers / 30 Sellers (Production Deployment)

Run against `api.o4db.org` (production VPS). First external validation after full architecture refactor.

| Metric | Result |
|--------|--------|
| Buyers | 30 |
| Sellers | 30 |
| VCIs submitted | 30 |
| Settlements completed | 28 |
| **Completion rate** | **~95%** |
| Replay attacks blocked | 100% |
| Invalid signatures blocked | 100% |
| VCI submit p50 | ~2.0s |
| VCI submit p95 | ~5.1s |
| VCI submit max | ~6.9s |
| Security bypasses | 0 |

Notes: 2 VCIs expired without settlement due to TTL timing in test harness — not protocol failures. All security checks passed. BES disabled (opt-in).

---

### v1.1.5 — 100 Buyers / 100 Sellers (Local + Production)

Extended scale test validating SQLite contention limits and all v1.1.5 features including Value-Weighted Penalty, Parallel Standby, and Audit Log.

| Metric | Result |
|--------|--------|
| Buyers | 100 |
| Sellers | 100 |
| VCI submit p50 | 2.0s |
| VCI submit p95 | 5.0s |
| VCI submit max | 7.0s |
| Replay attacks blocked | 100% |
| Invalid signatures blocked | 100% |
| Security bypasses | 0 |
| Value-Weighted Penalty | Active — weight range [0.5, 3.0] |
| Parallel Standby triggers | Tested — standby notified at T+120s |
| Audit Log signatures | Verified — SHA-256 + Ed25519 |
| SQLite contention | Acceptable up to ~50 concurrent nodes |

Notes: SQLite write contention is a documented limitation. For deployments exceeding 50 sustained concurrent nodes, migration to PostgreSQL or a write-queue architecture is recommended. This is a deployment decision — no protocol changes required. Value-Weighted Penalty is backwards compatible — neutral weight (1.0) when no volume history exists.

---

### Known Performance Limits

| Limit | Value | Mitigation |
|-------|-------|------------|
| SQLite concurrent writes | ~50 nodes | Migrate to PostgreSQL |
| Broadcast encryption nodes | ~1,000 | LKH/Multicast Encryption planned for v1.5 |
| CA Slashing mechanism | Not yet implemented | Slashing for dishonest CAs planned for v1.2 |
| Community Tier settlements | 50/month | Commercial License for higher volume |

---

---

---

## ERP-Ready Interface

O4DB™ is designed as **protocol infrastructure**, not an application. It abstracts
all cryptographic complexity so that any ERP, middleware, or legacy system can
participate using standard HTTP calls and plain JSON.

### Design Principle

> O4DB™ handles Ed25519 signatures, HPKE encryption, and ARA execution internally.
> Your ERP only manages **intentions** (what to buy) and **confirmations** (who won).

### Integration Model

```
┌─────────────────┐     Plain JSON      ┌──────────────────────┐
│   SAP / ERP /   │ ─── POST /vci ────▶ │   O4DB™ Relay Node   │
│   Legacy System │                     │  (Ed25519 + HPKE)    │
│   MuleSoft /    │ ◀── Webhook ──────── │   All crypto inside  │
│   Zapier / etc. │     Plain JSON       └──────────────────────┘
└─────────────────┘
```

The relay acts as a **cryptographic buffer**: it receives plain business data,
applies protocol-level security, and delivers plain results back via webhook or
polling. No cryptographic knowledge required on the ERP side.

### Webhook Schema (Outbound — relay → ERP)

The relay POSTs to your registered `webhook_url` for all relevant events:

```json
{
  "event":       "VCI_OFFER_RECEIVED | SETTLED | CONFIRMED | GHOSTED | PARALLEL_STANDBY",
  "vci_id":      "VCI-xxxxxxxx",
  "timestamp":   1740000000.0,
  "data": {
    "seller_id":    "NODE:AR:00123",
    "unit_price":   142.50,
    "currency":     "USD",
    "attributes":   {},
    "trust_score":  0.92
  }
}
```

### VCI Submission Schema (Inbound — ERP → relay)

Minimal fields required for a valid VCI:

```json
{
  "vci_id":             "VCI-your-uuid",
  "demand_type":        "EAN",
  "master_code":        "7891234567890",
  "quantity":           100,
  "price_token":        "<HPKE-encrypted-max-price>",
  "currency":           "USD",
  "ttl":                3600,
  "commitment_level":   1,
  "delivery_area":      "AR",
  "privacy_mode":       "STANDARD",
  "buyer_pubkey":       "<X25519-pubkey>",
  "buyer_sign_pub":     "<Ed25519-pubkey>",
  "vci_signature":      "<Ed25519-signature>",
  "weights":            {"trust": 0.4, "price": 0.4, "speed": 0.2},
  "external_ref_mapping": "SAP-PO-2026-00123",
  "timestamp":          1740000000.0
}
```

The `external_ref_mapping` field is stored relay-side only and returned
exclusively to the buyer. It is **never broadcast to sellers** — use it
to carry your internal ERP reference number, PO number, or SAP document ID.

### Headless Node (Docker-First)

The reference relay ships with a `docker-compose.yml` for zero-configuration
deployment:

```bash
docker-compose up -d
# Relay available at http://localhost:8080
# All crypto handled internally — your ERP calls plain HTTP
```

Three endpoints cover 95% of integration needs:

| Action | Endpoint | Direction |
|--------|----------|-----------|
| Emit demand | `POST /api/v1/vci` | ERP → Relay |
| Check status | `GET /api/v1/vci/{id}` | ERP → Relay |
| Confirm winner | `POST /api/v1/vci/{id}/settle` | ERP → Relay |
| Receive offers | Webhook `POST` to your URL | Relay → ERP |

### PROXY_NODE Profile (Legacy / COBOL Systems)

For systems that cannot handle asymmetric cryptography (pre-2000 ERPs,
mainframes, COBOL), the protocol defines a **Proxy Node** profile:

```
┌──────────────┐   Plain text    ┌─────────────────┐   Ed25519+HPKE   ┌──────────┐
│  Legacy ERP  │ ── (internal) ─▶│  O4DB Proxy Node│ ──────────────── ▶│  Relay   │
│  (COBOL/SAP) │                 │  (signs+encrypts)│                  │          │
└──────────────┘                 └─────────────────┘                  └──────────┘
```

- The Proxy Node operates **within the company's secure perimeter**
- Plain data never leaves the internal network unencrypted
- The legacy system requires zero cryptographic capability
- One `docker-compose up` on an internal server enables full O4DB participation
- No modifications to the original system required

### Certified Integrators

O4DB™ does not build ERP connectors. Third-party integrators may build and
commercialize certified connectors (SAP, Oracle, Dynamics, etc.) under the
**Certified Integrator License** — see LICENSE Section 3 for terms.
This creates an ecosystem of certified integration partners without
creating a support burden for the protocol author.


---

## Government Procurement Compatibility

O4DB™ v1.1.5 implements a **Sobre Cerrado Digital** (Digital Sealed Bid) model
natively compatible with public procurement transparency requirements.

| Phase | Visibility | Mechanism |
|-------|-----------|-----------|
| VCI Active (bidding open) | Nothing revealed | Buyer identity, max price, and destination are cryptographically concealed |
| ARA Execution | Nothing revealed | Ranking runs locally on buyer device — relay never sees max price |
| Settlement Pending | Nothing revealed | Winner notified privately — other sellers see no result |
| **Confirmed** | **Full disclosure** | Price, winner identity, demand identifier, and timestamp become public |

### Compliance Reference

| Framework | Requirement | O4DB Mechanism |
|-----------|-------------|----------------|
| EU Directive 2014/24/EU | Pre-award confidentiality + post-award publication | State-gated disclosure endpoint |
| Argentine Ley 13.064 | Sobre cerrado + apertura pública | Settlement Fingerprint public after CONFIRMED |
| General procurement law | Irrefutable award record | Signed Audit Log (Ed25519 + SHA-256) |

### Disclosure Endpoint

`GET /api/v1/vci/{vci_id}/settlement-disclosure`

- Returns `403 DISCLOSURE_NOT_YET_AVAILABLE` for any state other than `CONFIRMED`
- Returns signed disclosure record including: final price, winner seller ID, demand identifier, settlement timestamp, and privacy commitment proof
- Signed with relay Ed25519 key — verifiable by any party at `/api/v1/relay/pubkey`
- No partial disclosure at any intermediate state — the sealed bid stays sealed until fully executed

## Roadmap

| Version | Status | Focus |
|---------|--------|-------|
| v1.1.5 | ✅ Released | Core protocol — production relay. VCI dual representation (demand_type + master_code + demand_object), ARA local-by-design, JIT identity release, SPS with PSP interface, deterministic settlement state machine, privacy mode, buyer profile, 6-criteria eligibility filter + inventory affinity + probation mode, autonomy levels 0–3 (dPoA), seller trust score (federated Raft ledger) + STANDBY mode, BES (opt-in), constant-time rejection, post-settlement blind feedback, anti-collusion detection, G2B extension, anti-replay protection. 10 demand type standards (NSN, EAN, ATC, UODI, VIN, CAGE_MPN, CAS, ISBN, UNS, OTA_GIATA). Validated under 100+100 node stress test. |
| v1.2.x | 🔵 Planned | MCR (Multi-Currency Relay). NTD (Normalized Trust Distribution). PostgreSQL persistence layer migration. Webhook push for seller broadcast. |
| v1.5 | 🔵 Planned | PSP integration standard (full API spec). Verified Oracle certification for Gravity Import. CA admission governance. Normalization scale registry. Broadcast encryption key-tree for >1,000 nodes. Automotive and Pharma category full specifications. |
| v2.0 | 🔵 Planned | Cryptographic delivery proof. Dispute framework. Privacy mode technical enforcement post-JIT. CA admission decentralization. Travel and Industrial category specifications. |
| v3.0 | 🔵 Planned | Full M2M agentic execution. Decentralized relay network. Agent reputation layer. Open CA admission. |

---

## Security & Responsible Disclosure

O4DB™ is a high-assurance commerce protocol. If you discover a security  
vulnerability or cryptographic flaw in this reference implementation,  
please report it privately to: [https://x.com/O4DBmodel](https://x.com/O4DBmodel)

Vulnerability research is encouraged under a strict "no-harm" policy to the ecosystem.

---

© 2026 Daniel Eduardo Placanica. All Rights Reserved.  
Safe Creative IDs: 2602184604821-4XTVN6 / 2602204641140-6FSX6N / 2603014734558-2D52RP
UODI v1.2 Safe Creative: 2602284718909-6XLBXF  
O4DB™ and "Only For Determined Buyers" are protected trademarks.  
O4DB™ Patent Pending — U.S. Patent App. No. 63/993,946 (USPTO) | UODI v1.2 Patent Pending U.S. 63/993,355