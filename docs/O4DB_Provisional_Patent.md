# UNITED STATES PATENT AND TRADEMARK OFFICE

> **Copyright © 2026 Daniel Eduardo Placanica. All Rights Reserved.**  
> Safe Creative Registration ID: 2602184604821-4XTVN6
UODI v1.2 Safe Creative: 2602284718909-6XLBXF  
> O4DB™ Patent Pending — U.S. Patent App. No. 63/993,946 (USPTO)  
> This document constitutes prior art disclosure. All rights reserved.  

# PROVISIONAL PATENT APPLICATION

---

**TITLE OF THE INVENTION:**

O4DB: A Demand-Initiated Execution Protocol for Verified Intent
Commerce and Agent-to-Agent Transactions

---

**INVENTOR:**

Daniel Eduardo Placanica
Buenos Aires, Argentina

---

**CORRESPONDENCE ADDRESS:**

https://x.com/O4DBmodel

---

**FILING BASIS:**

35 U.S.C. § 111(b) — Provisional Application

---

## BRIEF DESCRIPTION OF THE INVENTION

The present invention relates to a computer-implemented protocol
for executing commerce transactions initiated by buyers with
verified, financially-backed demand. Specifically, the invention
provides a demand-initiated execution protocol — referred to
herein as O4DB (Only for Determined Buyers) — comprising a
Verified Intent Signal (VCI), an Anonymous Reverse Auction (ARA)
with local execution, a Just-In-Time Identity Release mechanism
(JIT), a Smart Penalty System (SPS), and a deterministic
event-driven Settlement Flow. The protocol is designed for
human buyers, autonomous software agents, and machine-to-machine
(M2M) commerce, and extends to Government-to-Business (G2B)
procurement contexts.

---

## FIELD OF THE INVENTION

The invention relates to electronic commerce infrastructure,
cryptographic protocol design, autonomous agent transaction
systems, and demand-side market mechanisms. More specifically,
it relates to a protocol layer that inverts the traditional
supply-initiated commerce model by enabling buyers with
pre-specified, financially verified demand to receive competing
offers from certified seller nodes without exposing their
maximum budget, identity, or personal data during the
competitive phase.

---

## BACKGROUND OF THE INVENTION

Existing electronic commerce systems are optimized for the
seller side of the market. They employ discovery mechanisms —
search, recommendation, behavioral targeting, and retargeting —
that are designed to maximize seller revenue and platform
engagement. These systems treat buyers who have already
determined their exact product requirements identically to
exploratory buyers who have not yet decided what to purchase.

This creates a systematic inefficiency for a specific and
economically significant class of buyer: one who (a) knows
the exact product identifier or full attribute constraints,
(b) has a defined maximum budget, (c) is willing to execute
immediately, and (d) has verified financial capacity to settle.

Current systems force these high-intent buyers through
discovery flows that expose their identity and behavior to
sellers before any competitive process begins, enabling
identity-based price discrimination. No existing protocol
provides a standardized, cryptographically-enforced mechanism
for buyers to express verified demand while maintaining
anonymity throughout the competitive phase.

Furthermore, as autonomous software agents increasingly act
on behalf of human principals in commerce contexts, no
established protocol exists for structured demand expression,
cryptographic commitment, and deterministic settlement
executable without human intervention at each step.

The present invention addresses these deficiencies.

---

## SUMMARY OF THE INVENTION

The invention provides a computer-implemented protocol
comprising the following principal components:

1. **Verified Intent Signal (VCI):** A cryptographically
   signed, structured demand packet with dual representation —
   a Private VCI holding the buyer's maximum price in
   plaintext, and a Public VCI in which the maximum price is
   replaced by an encrypted price_token using HPKE (RFC 9180),
   ensuring that seller nodes never observe the buyer's
   price ceiling.

2. **Pre-broadcast Eligibility Filter:** A six-criteria
   deterministic filter applied before broadcast, comprising:
   product category (Proof of Category), geographic coverage,
   fulfillment modality, minimum commitment level, buyer ban
   list, and Inventory Affinity scoring based on prior
   Settlement Fingerprint history.

3. **Anonymous Reverse Auction (ARA) with Local Execution:**
   A competitive mechanism in which certified seller nodes
   submit binding offers without observing competing bids.
   The ranking algorithm executes locally on the buyer's
   computing environment — not on a central server —
   preserving buyer sovereignty and preventing manipulation.
   Rejection signals are delivered in constant time
   (T_fixed + bounded noise) to prevent price inference
   attacks via timing analysis.

4. **Just-In-Time Identity Release (JIT):** A cryptographic
   mechanism by which buyer identity and logistics data are
   encrypted at VCI issuance and remain inaccessible to all
   parties until a Settlement Click occurs, at which point
   the encrypted payload is released exclusively to the
   winning seller node.

5. **Event-Driven Settlement Flow:** A deterministic state
   machine comprising states SETTLING, POP_CHECK,
   IDENTITY_RELEASE, SELECTIVE_PURGE, and ACK_WINDOW,
   where each transition is triggered by confirmation of
   the previous state — not by wall-clock timestamps —
   with defined retry policies (3 attempts, exponential
   backoff) and conservative network partition behavior
   that releases buyer funds on unresolvable failure.

6. **Smart Penalty System (SPS):** An instruction layer
   that emits signed penalty instructions to connected
   Payment Service Providers upon breach conditions,
   without custodying funds. Includes cryptographic
   privacy commitment bound to the ACK_Accepted payload,
   making seller data-use commitments verifiable and
   irrepudiable.

7. **Seller Trust Score (STS):** A real-time integrity
   indicator computed as S = (G·0.3) + (H·0.7) - P,
   where G is external reputation imported via Gravity
   Import with exponential decay, H is internal history
   comprising Precision, Velocity, and Compliance axes,
   and P is cumulative penalty. Maintained on a federated
   ledger governed by Raft consensus among permissioned
   Certifying Authorities.

8. **Network Integrity Mechanisms:** Comprising Invisible
   Max Price (price_token), Seller Network Score with
   response-ratio throttling, Proof of Category, Buyer
   Execution Score (BES), and Anti-Collusion detection
   with statistically-defined alert thresholds.

9. **Agent Autonomy Framework:** Four graduated levels
   of autonomous execution (Manual, Shadowing, Guardrail,
   Agentic) with Digital Power of Attorney (dPoA),
   Proof of Conformity, Constraint Versioning, Kill
   Switch, and Rate Limiting.

10. **G2B Extension:** Additional fields and behavioral
    overrides for Government-to-Business procurement,
    including forced open privacy mode, mandatory human
    settlement approval, and public audit trail in the
    Settlement Fingerprint.

---

## DETAILED DESCRIPTION OF THE INVENTION

### 1. Verified Intent Signal (VCI)

The VCI is the atomic unit of the protocol. It exists in
two representations:

**Private VCI** — held exclusively by the buyer's agent.
Contains all fields including max_price in plaintext.

**Public VCI** — broadcast to eligible seller nodes.
Identical to the Private VCI except that max_price is
replaced by price_token, computed as follows:

```
kem_id:     DHKEM(X25519, HKDF-SHA256)   [HPKE RFC 9180]
kdf_id:     HKDF-SHA256
aead_id:    AES-256-GCM
nonce:      CSPRNG(32 bytes), unique per VCI emission
ciphertext: HPKE.Seal(recipient_pub=buyer_pubkey,
                      info=vci_id,
                      aad=nonce,
                      pt=max_price)
hmac:       HMAC-SHA256(key=buyer_privkey,
                        msg=vci_id || nonce)
price_token: base64(nonce || ciphertext || hmac)
```

The buyer decrypts price_token locally. No server decrypts
this value. The encryption ensures that seller nodes, relay
nodes, and any network observer cannot determine the buyer's
maximum budget at any point during the competitive phase.

**Mandatory VCI fields include:** vci_version, demand_spec
(Exact ID Mode using universal identifiers EAN/UPC/GTIN/
VIN/ISBN/ATC/OEM_PN/IATA_ROUTE, or Attribute Mode with
must_have/nice_to_have constraints), quantity, max_price
(Private VCI only), price_token (Public VCI only), currency,
ttl (Sovereign TTL), commitment_level (0-4), solvency_cert,
delivery_accepted, delivery_area, privacy_mode, buyer_pubkey,
and vci_signature.

Every VCI is cryptographically signed using Ed25519 (RFC 8032)
before broadcast, providing non-repudiation and identity binding.
The price_token field is separately encrypted using HPKE (RFC 9180),
ensuring the signing key and encryption key are strictly separated
per the Key Separation Principle. Signing keys are managed via
external KMS or HSM-compatible systems. Tampered VCIs are
rejected by the network.

### 2. Pre-Broadcast Eligibility Filter

Before broadcast, each certified seller node is evaluated
against six criteria simultaneously. A seller receives the
Public VCI only if all six conditions are satisfied:

1. **Category:** Seller is certified in the VCI's product
   category via Proof of Category — verified against
   external transaction history, not self-declared.

2. **Geography:** Seller's declared delivery areas
   intersect the VCI's delivery_area field.

3. **Fulfillment:** Seller supports at least one modality
   declared in the VCI's delivery_accepted field.

4. **Commitment:** Seller's minimum accepted commitment
   level does not exceed the VCI's commitment_level.

5. **Ban check:** Seller node identifier is not present
   in the buyer's banned_sellers list.

6. **Inventory Affinity:** Seller has prior confirmed
   transactions (Settlement Fingerprints) with the same
   identifier_type and compatible identifier_value family.
   When fewer than three sellers satisfy this criterion,
   the filter relaxes to category level to preserve
   minimum competition.

New sellers without affinity history enter Probation Mode:
access is guaranteed (never excluded), but their offers
receive an affinity_score multiplier of 0.70 in ranking
until five successful transactions with matching
identifier_type are completed.

### 3. Anonymous Reverse Auction (ARA)

Eligible seller nodes submit binding offers within the
Sovereign TTL window. Sellers do not observe competing bids.

**Local Execution Model:** The ranking algorithm executes
on the buyer's computing environment (device or TEE for
Level 3). No central server computes rankings. Any
O4DB-compatible implementation that computes rankings
remotely is non-conformant with this specification.

**Local ranking flow:**
1. Verify offer_signature against seller's registered
   public key
2. Compare unit_price against local max_price (buyer
   holds this value — no server required)
3. Silently discard offers exceeding max_price
4. Normalize all attributes per scales declared in VCI
5. Fetch seller Trust Score S from federated registry
6. Compute V = Σ(wᵢ·Aᵢ) + (wₛ·S) - P
7. Rank by V descending
8. Present to buyer (Level 0,1) or execute (Level 2,3)

**Constant-time rejection:** All offer responses —
accepted or rejected — are delivered in time T_fixed +
noise, where noise is uniform random within [0, T_fixed
× 0.1]. This prevents price inference attacks where a
seller approximates max_price by observing response time
variations across multiple VCI submissions.

**One-offer constraint:** Each seller may submit exactly
one offer per active VCI. Amendments are rejected.
This closes the binary-search inference attack vector.

**Network Score:** Seller nodes are assigned a network_score:

```
network_score = (response_ratio  × 0.30) +
                (conversion_ratio × 0.40) +
                (sla_score        × 0.30)

sla_score: competitive_offers / offers_submitted
competitive_offer: unit_price ≤ winning_price × 1.15
```

Nodes with low network_score receive throttled VCI traffic.
Scores are not measured during the first 25 transactions
(Sandbox warm-up period).

### 4. Just-In-Time Identity Release (JIT)

Buyer identity and logistics data are encrypted at VCI
issuance using the public keys of all eligible seller nodes.
Each seller receives an individually encrypted payload
decryptable only by their private key.

During the ARA phase, no party — including protocol operators
— can access buyer identity in plaintext.

Upon Settlement Click:
- The encrypted payload is released exclusively to the
  winning seller (Postor 1)
- All other sellers' payloads are scheduled for DATA_PURGE
- The winning seller decrypts using their private key

### 5. Event-Driven Settlement Flow

Settlement is governed by a deterministic state machine:

**STATE: SETTLING**
Trigger: Settlement Click. Action: ARA generates signed
Settlement Token (ST). Transition: → POP_CHECK.

**STATE: POP_CHECK**
Trigger: ST generated. Action: Level 2,3,4: Financial
Oracle confirms funds locked. Level 0,1: auto-confirmed.
Timeout: max 10s with 3 retries (exponential backoff:
1s, 2s, 4s). Failure: VCI_ABORTED, funds released.

**STATE: IDENTITY_RELEASE**
Trigger: PoP confirmed. Action: Buyer identity released
exclusively to winning seller. VCI state → SETTLED_PENDING.
Timeout: max 5s.

**STATE: SELECTIVE_PURGE**
Trigger: Identity released. Action: Sellers ranked 3..N
receive DATA_PURGE. Postor 2 enters STANDBY.

**STATE: ACK_WINDOW**
Trigger: Purge confirmed. Timeout: ST-TTL (B2C default:
15 min; B2B: 30 min; configurable by category/region).

- ACK_Accepted from Postor 1 → VCI: CONFIRMED
- TTL expires (GHOSTING) → penalty to Postor 1; ST
  issued to Postor 2; ACK_WINDOW resets
- ACK_Accepted from Postor 2 → VCI: CONFIRMED
  (resilience path)
- Postor 2 also fails (DOUBLE GHOSTING) → VCI:
  FAILED_SELLER_GHOSTING; maximum penalties applied;
  funds released

Network partition behavior: conservative. On unresolvable
partition, funds are released and VCI is aborted. Buyer
capital protection takes priority over transaction
completion.

**Settlement Fingerprint:**
Every confirmed transaction produces an immutable on-chain
fingerprint:

```
fingerprint = SHA-256(vci_id + seller_id + unit_price +
              identifier_type + identifier_value +
              timestamp + buyer_pubkey + seller_pubkey)
```

### 6. Smart Penalty System (SPS)

The SPS emits signed penalty instructions to connected
Payment Service Providers upon breach conditions. O4DB
does not custody funds. PSPs implement the following
abstract interface:

```
hold(buyer_id, amount, currency, ttl)   → hold_reference
confirm(hold_reference)                  → settlement_receipt
release(hold_reference)                  → release_receipt
penalize(hold_reference, amount, reason) → penalty_receipt
```

**Cryptographic Privacy Commitment:** At ACK_Accepted,
the seller signs a payload including vci_reference,
settlement_token_id, timestamp, privacy_commitment text,
privacy_mode_ref (SHA-256 of declared privacy_mode), and
ack_signature covering all fields. This payload is attached
to the Settlement Token as privacy_commitment_proof,
making the seller's data-use commitment cryptographically
irrepudiable.

**Dispute Categories:**
- FULFILLMENT_FRAUD: delivered identifier ≠ VCI identifier
- PRODUCT_CONDITION: damaged or incomplete product
- LOGISTICS_DAMAGE: damage attributable to carrier
  (seller exonerated if dispatch_hash proves intact dispatch)

### 7. Seller Trust Score (STS)

```
S = (G × 0.3) + (H × 0.7) - P

H = (Precision × 0.5) + (Velocity × 0.3) + (Compliance × 0.2)

G_weight = max(0.30, 1.0 - (o4db_transactions × 0.02))

H = Σ(result × e^(-λ × days)) / Σ(e^(-λ × days))
λ: 0.05 (electronics), 0.02 (automotive), 0.01 (industrial)
```

External reputation (G) is imported via Gravity Import
from verified platforms, requiring: account age ≥ 12 months,
≥ 50 completed transactions, dispute rate ≤ 5%, unique
legal entity. Explicit seller consent is required before
import.

**Federated Trust Score Registry:** Maintained on a
federated ledger using Raft consensus among permissioned
Certifying Authorities (CAs). Quorum: majority (N/2 + 1).
CA set is permissioned in v1.0. Score reads are eventually
consistent; writes require Raft consensus.

**Score Freeze:** A seller may request decay suspension
for up to 30 days (once per year) by submitting a signed
freeze_request with evidence_hash. CA majority vote via
Raft within 48 hours.

### 8. STANDBY Mode — Voluntary Decay Suspension

A registered seller node may declare a planned absence period by
submitting a signed STANDBY request specifying an expected_return
timestamp. Upon activation:

- The seller's exponential Trust Score decay is suspended for the
  declared duration.
- The seller's VCI eligibility is suspended; no VCIs are broadcast
  to the node during STANDBY.
- The seller's current Trust Score is preserved without degradation
  for the declared period, subject to a maximum of 30 days per
  calendar year.
- Upon return (either at declared timestamp or via explicit
  cancel_standby request), decay resumes from the preserved score.

The STANDBY mechanism prevents structural disadvantage for sellers
with legitimate operational interruptions (inventory procurement
cycles, seasonal closures, infrastructure maintenance) that would
otherwise cause Trust Score degradation disproportionate to their
actual reliability record.

**STANDBY state machine:**
```
ACTIVE → STANDBY (on signed standby_request with expected_return)
STANDBY → ACTIVE (on cancel_standby or expected_return reached)
```

Days declared are tracked cumulatively. Requests exceeding the
30-day annual limit are rejected with STANDBY_LIMIT_EXCEEDED.

### 9. Agent Autonomy Framework

Four graduated autonomy levels:

- **Level 0 (Manual):** Human authentication required
  for Settlement Click.
- **Level 1 (Shadowing):** Agent recommends; human
  confirms with single action.
- **Level 2 (Guardrail):** Delegated signing key with
  Hard Constraints. Proof of Conformity attached to ST.
- **Level 3 (Agentic):** Full autonomy within TEE.
  Manages declared budget and time window.

All levels include: Digital Power of Attorney (dPoA)
framework, Constraint Versioning (sealed snapshot at
VCI emission), Kill Switch (mandatory for Level 2+),
and Rate Limiting (max_per_hour, max_per_day,
max_concurrent_active).

Jurisdictional note: dPoA validity depends on local
legislation. The protocol provides technical infrastructure
only.

### 10. Network Integrity Mechanisms

**Anti-Collusion Detection:** A COLLUSION_ALERT is
recorded immutably in the Settlement Fingerprint when:
three or more sellers in the same category exhibit
Pearson price correlation > 0.85 across ten or more
consecutive VCIs within a 30-day rolling window.

**Buyer Execution Score (BES):**

BES is a composite execution integrity metric maintained per
buyer signing key (buyer_sign_pub). The internal formula is:

```
BES = (Settlements / VCIs_Emitted) × (ACKs_Received / Settlements)
```

VCIs expiring with zero offers received are excluded from the
denominator. BES is never exposed externally; the relay exposes
only a tier classification (RESTRICTED / LOW_INTENT / STANDARD / GOLD).

**Buyer lifecycle states:**

- **INITIAL:** New buyer identity. Permits up to 3 VCI emissions.
  First ghosting event results in permanent BLOCKED status.
  Graduation to ESTABLISHED requires ≥ 3 settled ACKs and BES ≥ 0.5.

- **ESTABLISHED:** Graduated buyer with demonstrated execution history.
  First ghosting event triggers SUSPENDED status for 48 hours.
  Second ghosting event results in permanent BLOCKED status.

- **SUSPENDED:** Temporary restriction following first ghosting by an
  ESTABLISHED buyer. Auto-reactivates upon expiry (48h). New VCI
  submissions during suspension are rejected.

- **BLOCKED:** Permanent restriction. The buyer signing key is
  cryptographically blacklisted from the network. New keypair
  required for re-entry (subject to network policy).

**Ghosting Report Mechanism:** Sellers may submit signed ghosting
reports referencing a valid settlement_token. A 2-hour grace period
applies: if the buyer transmits an ACK within the grace window, the
report is discarded with no penalty. False reports (submitted after
a confirmed ACK exists) result in a penalty applied to the reporting
seller's Trust Score. VCI state transitions to BUYER_FAULT only upon
grace period expiry with no ACK received.

**Post-Settlement Blind Feedback:** Non-winning sellers
receive feedback after CONFIRMED state: PRICE_DELTA
(rounded to nearest 5%), TRUST_DELTA, or FULFILLMENT_DELTA.
Absolute winning price is never revealed.

### 11. G2B Extension

For Government-to-Business procurement, the following
additional VCI fields are defined: buyer_type (government),
procurement_law, contracting_authority, tender_reference.

Behavioral overrides: privacy_mode forced to "open",
commitment_level minimum 2, settlement approval requires
Level 0 (human authorization), TTL configurable in days.
Settlement Fingerprint includes contracting_authority
in plaintext for public audit.

---

## CLAIMS

### Independent Claims

**Claim 1.**
A computer-implemented method for demand-initiated commerce
execution, comprising:
generating, by a computing system, a cryptographically
signed demand packet comprising a product identifier,
a quantity, a commitment level, a delivery specification,
and an encrypted maximum price token, wherein said maximum
price token is generated by applying Hybrid Public Key
Encryption to a maximum price value using the buyer's
public key, such that seller nodes receiving said demand
packet cannot determine the buyer's maximum price;
applying a multi-criteria eligibility filter to a set
of certified seller nodes to determine a filtered set
of eligible recipients, said filter comprising at least
product category verification, geographic coverage
verification, and inventory affinity scoring based on
prior confirmed transaction history;
broadcasting said demand packet exclusively to said
filtered set of eligible seller nodes;
receiving, from said eligible seller nodes, binding
price offers submitted without knowledge of competing
offers or the buyer's maximum price;
executing a ranking algorithm locally on the buyer's
computing environment to rank received offers according
to a buyer-declared weight matrix, without transmitting
offer data to any central server;
delivering rejection signals to non-selected sellers
in constant time comprising a fixed duration plus
bounded uniform noise, independent of the relationship
between the seller's offered price and the buyer's
maximum price; and
upon buyer selection of a winning offer, initiating
a deterministic event-driven settlement state machine
that releases buyer identity exclusively to the winning
seller node upon financial confirmation.

**Claim 2.**
A computer-implemented method for protecting buyer
price privacy in a multi-seller competitive auction,
comprising:
maintaining a private demand representation comprising
a maximum price value in plaintext, accessible only
to the buyer's computing environment;
generating a public demand representation comprising
an encrypted price token in place of said maximum
price value, wherein said encrypted price token is
computed using HPKE RFC 9180 with a nonce unique to
each demand packet emission and an HMAC binding the
token to the demand packet identifier;
broadcasting said public demand representation to
seller nodes such that no seller node, relay node,
or network observer can determine the buyer's maximum
price during the competitive phase; and
validating received offers against said maximum price
value locally on the buyer's computing environment,
silently discarding offers exceeding the maximum price
before ranking.

**Claim 3.**
A computer-implemented settlement protocol comprising
a deterministic finite state machine with states:
SETTLING, triggered by buyer selection of a winning
offer, in which a signed Settlement Token is generated;
POP_CHECK, in which financial commitment is verified
by a financial oracle for commitment levels two and
above, with retry policy comprising three attempts
with exponential backoff, and transition to VCI_ABORTED
with immediate fund release upon verification failure;
IDENTITY_RELEASE, in which buyer identity data,
encrypted at demand packet issuance, is decrypted
exclusively by the winning seller node using the
seller's private key;
SELECTIVE_PURGE, in which all non-winning seller
nodes receive a DATA_PURGE instruction for buyer
identity payloads, except the second-ranked seller
which enters STANDBY;
ACK_WINDOW, in which the winning seller must transmit
a signed acknowledgment within a configurable timeout,
and upon timeout expiration, the Settlement Token is
transferred to the second-ranked seller with reset
timeout, and upon second failure, the protocol enters
FAILED_SELLER_GHOSTING state with maximum penalties
applied and funds released to the buyer.

**Claim 4.**
A system for autonomous agent commerce comprising:
a demand specification module configured to generate
cryptographically signed demand packets on behalf of
a human principal;
an autonomy level parameter specifying one of: Manual,
requiring human authentication for each transaction;
Shadowing, presenting recommendations for human
confirmation; Guardrail, executing transactions
autonomously within cryptographically committed Hard
Constraints with Proof of Conformity attached to each
Settlement Token; or Agentic, managing a declared
budget within a Trusted Execution Environment with
full signing key autonomy;
a constraint versioning mechanism that seals the
active constraint set with a timestamp at demand
packet emission, such that post-emission constraint
modifications do not affect active transactions; and
a kill switch that invalidates the delegated signing
key immediately upon activation, blocking new demand
packet emissions while permitting completion of
already-signed transactions.

**Claim 5.**
A method for seller integrity scoring in a
demand-initiated commerce network, comprising:
computing a composite trust score S = (G × w_G) +
(H × w_H) - P, wherein G represents externally-imported
reputation subject to exponential time decay with
category-specific decay constant lambda, H represents
internal protocol history comprising precision of
product identifier fulfillment, velocity of settlement
acknowledgment, and compliance with dispute outcomes,
and P represents cumulative protocol breach penalties;
maintaining said trust score on a federated ledger
governed by Raft consensus among a permissioned set
of Certifying Authorities, wherein score updates
require majority quorum and score reads are served
by any available CA;
applying said trust score both as a hard floor filter
excluding sellers below a buyer-declared minimum
threshold from auction participation, and as a
weighted variable in the offer ranking function; and
recording an immutable COLLUSION_ALERT in the
transaction fingerprint when three or more seller
nodes in the same product category exhibit price
correlation exceeding 0.85 across ten or more
consecutive transactions within a thirty-day window.

### Dependent Claims

**Claim 6** (depends on Claim 1):
The method of claim 1, wherein the inventory affinity
criterion of the eligibility filter relaxes to category-
level verification when fewer than three seller nodes
satisfy the affinity criterion, ensuring minimum
competitive participation.

**Claim 7** (depends on Claim 1):
The method of claim 1, further comprising maintaining a
Buyer Execution Score system comprising: a composite
execution integrity metric computed as the product of
settlement ratio and acknowledgment ratio per buyer
signing key; a four-state buyer lifecycle (INITIAL,
ESTABLISHED, SUSPENDED, BLOCKED) with state transitions
triggered by execution history and ghosting events; a
graduated penalty mechanism wherein first ghosting events
by INITIAL buyers result in permanent blocking, while
ESTABLISHED buyers receive a 48-hour suspension before
permanent blocking on repeat offense; a ghosting report
mechanism with a configurable grace period during which
late ACK transmission nullifies the report; and a
tier-based external representation that exposes only
a classification label without revealing the underlying
score, preventing gaming of the metric.

**Claim 7a** (depends on Claim 7):
The method of claim 7, further comprising a STANDBY mode
wherein a registered seller node may submit a signed request
to suspend Trust Score exponential decay for a declared
period not exceeding thirty cumulative days per calendar year,
during which the node's eligibility for VCI broadcast is
suspended and the Trust Score is preserved at the value
recorded at STANDBY activation, with decay resuming upon
explicit cancellation or expiry of the declared return
timestamp.

**Claim 8** (depends on Claim 1):
The method of claim 1, wherein the ranking algorithm
computes a value score V = Σ(wᵢ × Aᵢ) + (wₛ × S) - P
for each offer, where wᵢ are buyer-declared attribute
weights, Aᵢ are normalized offer attribute values,
wₛ is a buyer-declared trust weight, S is the seller's
trust score, and P is the normalized unit price, with
the highest V determining the winning offer.

**Claim 9** (depends on Claim 3):
The method of claim 3, wherein the settlement state
machine is parametric, with timeout values configurable
by product category and geographic region, subject to
global minimum floor values, enabling category-specific
timing such as extended timeouts for pharmaceutical
regulatory compliance or high-frequency short timeouts
for machine-to-machine autonomous transactions.

**Claim 10** (depends on Claim 1):
The method of claim 1, wherein winning seller nodes,
upon transmitting a signed acknowledgment, attach a
cryptographic privacy commitment comprising: a hash
of the original demand packet, the settlement token
identifier, a timestamp, a natural language privacy
commitment statement, a hash of the declared privacy
mode, and a cryptographic signature covering all
preceding fields, said commitment being permanently
attached to the Settlement Token as an irrepudiable
record of the seller's data-use obligations.

**Claim 11** (depends on Claim 1):
The method of claim 1, further comprising a Government-
to-Business mode wherein a buyer_type field is set to
"government", privacy_mode is forced to "open",
settlement requires human-level authorization regardless
of configured autonomy level, the settlement fingerprint
includes a contracting authority identifier in plaintext
for public audit, and transaction timing is configurable
in units of days rather than minutes.

**Claim 12** (depends on Claim 4):
The system of claim 4, wherein the Guardrail autonomy
level generates a Proof of Conformity for each
transaction equal to a cryptographic hash of the
constraint snapshot hash, the offer hash, and a
timestamp, enabling automated detection of constraint
violations without human arbitration.

**Claim 13** (depends on Claim 5):
The method of claim 5, wherein a seller node may
request suspension of exponential decay (STANDBY mode)
for a period not exceeding thirty cumulative days per
calendar year by submitting a signed request comprising
an expected_return timestamp and a seller_id, said
request taking effect immediately upon cryptographic
signature validation without requiring Certifying
Authority approval, with cumulative day-tracking
enforced by the relay to prevent abuse of the annual
limit.

---

## ABSTRACT

A computer-implemented demand-initiated commerce execution
protocol comprising: a Verified Intent Signal (VCI) with
dual private/public representation in which the buyer's
maximum price is replaced by an HPKE-encrypted token in
the publicly-broadcast version; a six-criteria pre-broadcast
eligibility filter including inventory affinity scoring;
an Anonymous Reverse Auction with mandatory local ranking
execution on the buyer's computing environment; a
Just-In-Time Identity Release mechanism preserving buyer
anonymity throughout the competitive phase; a deterministic
event-driven settlement state machine with resilience
via second-ranked seller fallback; a Smart Penalty System
emitting signed instructions to Payment Service Providers
with cryptographic privacy commitment bound to settlement
acknowledgment; a federated Seller Trust Score registry
governed by Raft consensus; an Agent Autonomy Framework
with four graduated execution levels and Digital Power
of Attorney; and network integrity mechanisms comprising
constant-time rejection responses, anti-collusion
statistical detection, and Buyer Execution Score. The
protocol is applicable to human buyers, autonomous software
agents, machine-to-machine commerce, and Government-to-
Business procurement contexts.

---

## BRIEF DESCRIPTION OF THE DRAWINGS

FIG. 1 — O4DB Protocol Execution Flow v1.1: illustrates
the complete protocol flow from Phase 0 (Demand Resolution,
NLU to EAN/GTIN) through Phase 1 (VCI broadcast with
Filtered Broadcast and Category Filter), Phase 2 (ARA
with Blind Offers and Local Ranking), Phase 3 (Settlement
Click with JIT Identity Release and Resilience Flow to
second-ranked bidder), and Phase 4 (ACK Window and
Settlement Fingerprint on-chain).

---

*End of Provisional Patent Application*

*Daniel Eduardo Placanica*
*Buenos Aires, Argentina*
*February 2026*

---

*This document constitutes prior art disclosure for O4DB™ Protocol v1.1.5.*  
*Copyright © 2026 Daniel Eduardo Placanica. All Rights Reserved.*  
*Safe Creative Registration ID: 2602184604821-4XTVN6
UODI v1.2 Safe Creative: 2602284718909-6XLBXF*  
*O4DB™ Patent Pending — U.S. Patent App. No. 63/993,946 (USPTO). All rights reserved.*  
*Licensed under O4DB™ Community & Commercial License v1.1.5. See LICENSE.*  
