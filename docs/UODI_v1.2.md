# O4DB™ | v1.1.5 | build: 20260227-001 | 2026-02-27T18:00Z
# UODI-O4DB Standard Specification (v1.2)

> **Patent Pending — U.S. Patent App. No. 63/993,355 (USPTO)**  
> Safe Creative: 2602284718909-6XLBXF  
> Author: Daniel Eduardo Placanica — Analista independiente | Desarrollador de protocolos  
> Contact: daniel@o4db.org | https://x.com/O4DBmodel
## Universal Omnimodal Demand Identifier for Object Databases

[![Version](https://img.shields.io/badge/Version-1.2-blue.svg)]()
[![CorePrefix](https://img.shields.io/badge/Core_Prefix-P120-orange.svg)]()
[![License](https://img.shields.io/badge/License-Open_Core-green.svg)]()

---

## 1. Abstract

The **Universal Omnimodal Demand Identifier (UODI)** is a high-density, position-sensitive alphanumeric protocol designed to encode and transmit transport demand across heterogeneous infrastructures without pre-integrated middleware. It acts as a **Universal Indexing Layer** for Machine-to-Machine (M2M) discovery in any logistics ecosystem.

UODI is built for the **O4DB (Only For Determined Buyers)** protocol model, where commerce is initiated by buyer intent. A UODI string is a **Vague Commercial Intent (VCI)**: it expresses what, how many, from where, to where, and when — without revealing exact identity or location until a bilateral cryptographic contract handshake is completed.

---

## 2. Version Prefix Convention

The first block of the Core encodes the **protocol version of the Core structure itself**, not the document version. This allows parsers to detect the block layout before parsing any other field.

| Prefix | Core blocks | Introduced | Notes |
|:-------|:-----------:|:----------:|:------|
| `P100` | 14 | v1.0 / v1.1 | Without CANT block. Deprecated. |
| `P120` | 15 | v1.2 | Adds CANT block at position 10. Current. |

Any parser that reads `P120` MUST expect exactly 15 blocks. A string with prefix `P100` follows the 14-block layout of v1.1. Future breaking changes MUST increment the prefix (e.g. `P200`).

---

## 3. Technical Philosophy: The Triple-Layer Stack

1. **Index Layer (UODI):** A 15-block immutable string for routing and discovery.
2. **Payload Layer (O4DB Object):** Associated JSON/XML containing commercial terms, dimensions, and cargo specifics.
3. **Trust Layer (DID):** Decentralized Identity verification linked to the `OWNR` block for financial clearing.

---

## 4. Core Syntax (P120) — The Protected Core

The Core is composed of **15 mandatory blocks** in strict positional order. Parsers MUST evaluate each block by position. Empty or undisclosed fields MUST be populated with the wildcard of the correct width for that block. No block may be omitted.

```
P120-[MODE]-[TYPE]-[PROP]-[CLAS]-[PRIO]-[AUTO]-[FUEL]-[OWNR]-[CANT]-[ORIG]-[DEST]-[DATE]-[WAIT]-[CHK4]
```

### 4.1 Block Definition Matrix

| Pos | Block | Width | Permitted Values | Description |
|:---:|:------|:-----:|:-----------------|:------------|
| 1 | **PVER** | 4 | `P120` | Core version prefix. Determines block layout. |
| 2 | **MODE** | 4 | `PASS` `CARG` `VALO` `ANIM` | Legal framework: Passenger, Cargo, Values/Currency, Live Animals. |
| 3 | **TYPE** | 4 | `ROAD` `AIRS` `SEAS` `RAIL` `ORBT` `UNDE` | Infrastructure type. `UNDE` = Hyperloop/subterranean. `ORBT` requires tail extension §7.5. |
| 4 | **PROP** | 4 | `FRIG` `HAZM` `ARMD` `LIVE` `****` | Physical handling. Wildcard = standard. |
| 5 | **CLAS** | 4 | `EXEC` `NORM` `ECON` `CRIT` `****` | Service quality tier. Wildcard = no preference. |
| 6 | **PRIO** | 4 | `URGE` `NORM` `LOWP` `****` | Dispatch urgency. Independent of CLAS (§4.2). |
| 7 | **AUTO** | 4 | `FULL` `REMO` `HUMA` `****` | Autonomy level. Wildcard = no preference. |
| 8 | **FUEL** | 4 | `ELEC` `HYDR` `COMB` `****` | Energy/ESG requirement. Wildcard = no preference. |
| 9 | **OWNR** | 8 | `[OWNR8]` `********` | 8-char truncated DID hash (§4.3) or anonymous wildcard. |
| 10 | **CANT** | 5 | `[UNIT][NNNN]` | Quantity or volume (§4.4). |
| 11 | **ORIG** | 16 | `[GH][_pad][SIGN][ZZZ]` `????????????????` | Origin coordinates (§5). Padding char: `_` |
| 12 | **DEST** | 16 | `[GH][_pad][SIGN][ZZZ]` `????????????????` | Destination coordinates (§5). Padding char: `_` |
| 13 | **DATE** | 6 | `[DDMMYY]` | Target date UTC. Century is assumed 20xx. |
| 14 | **WAIT** | 4 | `M[XXX]` `H[XXX]` `D[XXX]` | Max wait SLA. `M000` = immediate dispatch. |
| 15 | **CHK4** | 4 | `[CRC16HEX]` | CRC-16-CCITT integrity check (§6). |

**Canonical string length (blocks 1–14, no hyphens): 87 characters.**
Width breakdown: 4+4+4+4+4+4+4+4+8+5+16+16+6+4 = 87.

### 4.2 CLAS vs PRIO Semantics

Independent signals. **CLAS** defines *which vehicle* (quality tier). **PRIO** defines *when* it is dispatched (urgency). Conflict resolution belongs to the matching engine, not the protocol.

### 4.3 OWNR Block — DID Hash Truncation

8-character uppercase Base32 truncation of SHA-256 of the issuer's DID string. Anonymous: exactly 8 asterisks.

```python
import hashlib, base64

def ownr_from_did(did_string: str) -> str:
    digest = hashlib.sha256(did_string.encode('utf-8')).digest()
    return base64.b32encode(digest).decode()[:8].upper()
    # "did:o4db:danielplacanica" → "XOM6LP4Z"
```

### 4.4 CANT Block — Quantity / Volume

Format: `[UNIT][NNNN]` — 1-letter unit code + 4-digit zero-padded value. Total width: 5 characters.

| Unit | Meaning | Range | Example |
|:----:|:--------|:------|:--------|
| `P` | Passengers | 1–9999 | `P0003` = 3 passengers |
| `K` | Kilograms | 1–9999 | `K0500` = 500 kg |
| `T` | Metric tons | 1–9999 | `T0050` = 50 tons |
| `L` | Litres | 1–9999 | `L0800` = 800 litres |
| `G` | Kilolitres (×1,000 L) | 1–9999 | `G5000` = 5,000,000 L |
| `U` | Units (pallets) | 1–9999 | `U0012` = 12 pallets |
| `C` | Containers (TEU) | 1–9999 | `C0004` = 4 TEU |
| `*` | No preference | `*0000` | Wildcard |

---

## 5. Geometric Precision Framework (GPF)

ORIG and DEST blocks are always exactly **16 characters**.

### 5.1 Canonical Block Format

```
[GEOHASH_12][SIGN][ZZZ]
```

| Component | Width | Description |
|:----------|:-----:|:------------|
| GEOHASH | 12 chars | Geohash chars (lowercase). Right-padded with `_` to fill 12 positions. |
| SIGN | 1 char | `+` above ground, `-` below surface, `0` ground level. |
| ZZZ | 3 chars | Altitude/depth in metres, zero-padded. Range 000–999. |

> **CRITICAL:** Padding character is `_` (underscore). The hyphen `-` is reserved exclusively as block delimiter and MUST NOT appear inside ORIG or DEST. Underscore is not in the Geohash alphabet (0–9, b–z excluding a,i,l,o) and is unambiguous.

### 5.2 Precision Modes

| Mode | Example | Precision | Use Case |
|:-----|:--------|:----------|:---------|
| **Exact** | `AR69Y7PGXQWT0000` | ~3.7 cm | Robotic docking, drone pad |
| **Reduced** | `AR69Y7PG____0000` | ~610 m | City block |
| **Vague** | `AR69Y7______0000` | ~±20 km | Region only, pre-handshake |
| **Incognito** | `????????????????` | None | Locked until contract handshake |

### 5.3 Z-Axis Examples

```
AR69Y7PGXQWT+120  →  120 m above ground (drone)
AR69Y7PGXQWT-015  →  15 m below surface (mining)
AR69Y7PGXQWT0000  →  Ground level
AR69Y7______0000  →  Vague, ground level
????????????????  →  Incognito
```

---

## 6. Integrity Check (CHK4)

**Algorithm:** CRC-16-CCITT, polynomial `0x1021`, initial value `0xFFFF`, no input/output reflection (XModem variant).

**Canonical input:** blocks 1–14 concatenated without hyphens. Always exactly 87 ASCII characters. Implementations MUST assert this length before computing the CRC. Any deviation indicates a block width error.

```python
def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = (crc << 1) ^ 0x1021 if crc & 0x8000 else crc << 1
        crc &= 0xFFFF
    return crc

def compute_chk4(blocks_14: list) -> str:
    canonical = "".join(blocks_14).encode('ascii')
    assert len(canonical) == 87, f"Canonical MUST be 87 chars, got {len(canonical)}"
    return format(crc16_ccitt(canonical), '04X')

def validate_uodi(uodi: str) -> bool:
    parts = uodi.split('-')          # safe: ORIG/DEST use _ not -
    assert len(parts) == 15
    return compute_chk4(parts[:14]) == parts[14]
```

---

## 7. Extensibility: Tail Extensions

Core is immutable. Industry data appended via `::` delimiter. Extensions do not affect CHK4.

```
[UODI-CORE]::[EXT_ID]-[DATA]::[EXT_ID]-[DATA]
```

### 7.1 Standard Extensions

| Extension | Format | Description | Required for |
|:----------|:-------|:------------|:-------------|
| `TEMP` | `TEMP-NEG20` | Temperature in °C | PROP=FRIG |
| `MASS` | `MASS-00750` | Payload mass kg, 5-digit | Optional |
| `SPEC` | `SPEC-BOVI` | Species code | MODE=ANIM (mandatory) |
| `ENRG` | `ENRG-GNGL` | Energy commodity type | Energy cargo §7.4 |
| `SHAR` | `SHAR-YES` / `SHAR-NO` | Shared vs exclusive vehicle | Optional |
| `RETN` | `RETN-NO` / `RETN-YES` / `RETN-SCH` | Return trip | Optional |
| `CERT` | `CERT-PLVR` | Placanica Verified seal | Optional |

### 7.2 SHAR — Shared Service

```
::SHAR-YES   accepts sharing (rideshare, bus, commercial flight)
::SHAR-NO    exclusive vehicle required (private jet, charter)
```

If absent, operator applies its default model. Commercial aviation is shared by default.

### 7.3 RETN — Return Trip

```
::RETN-NO    one-way (default if absent)
::RETN-YES   return to ORIG, same conditions
::RETN-SCH   scheduled return, different conditions — requires second UODI linked via Payload CHAIN-ID
```

### 7.4 ENRG — Energy Commodity

| Code | Description |
|:-----|:------------|
| `ENRG-CRUD` | Crude oil |
| `ENRG-GNGL` | Liquefied natural gas |
| `ENRG-HYDR` | Liquid hydrogen |
| `ENRG-FUEL` | Refined fuel |
| `ENRG-BATT` | Industrial battery units / BESS |

> Electrical energy as grid-transmitted commodity is outside UODI scope. Physical energy carriers are fully supported.

### 7.5 Orbital Extension (mandatory for TYPE=ORBT)

```
::TRAJ-[TLE_LINE1]-[TLE_LINE2]
```

For TYPE=ORBT, ORIG and DEST MUST be `????????????????`. Trajectory via Two-Line Element format.

### 7.6 ANIM Mandatory Extension

MODE=ANIM MUST include `::SPEC-[CODE]`. Implementations receiving ANIM without SPEC SHOULD treat the UODI as incomplete.

---

## 8. Minimum Viable VCI

| Block | Required? | Reason |
|:------|:----------|:-------|
| PVER | Always | Determines block layout |
| MODE | **Yes** | Defines legal framework |
| TYPE | **Yes** | Defines infrastructure to search |
| PROP–FUEL | No (`****`) | All wildcard-able |
| OWNR | No (`********`) | Can be anonymous |
| CANT | **Yes** | Vehicle capacity matching |
| ORIG | **Yes** | Cannot match without origin |
| DEST | No (`????????????????`) | Can be locked until handshake |
| DATE | **Yes** | Scheduling required |
| WAIT | **Yes** | SLA definition |
| CHK4 | Always | Integrity |

### Minimum VCI — 3 passengers, Morón to Barracas, 27 Feb 2026, max 15 min:

```
P120-PASS-ROAD-****-****-****-****-****-********-P0003-6GF3V7______0000-6GF9M2______0000-270226-M015-F6DA
```

---

## 9. Implementation Examples

### 9.1 Minimum VCI — Morón to Barracas, 3 pax
```
P120-PASS-ROAD-****-****-****-****-****-********-P0003-6GF3V7______0000-6GF9M2______0000-270226-M015-F6DA
```

### 9.2 Cold-chain drone, full 3D, 12 kg at -20°C
```
P120-VALO-AIRS-FRIG-CRIT-URGE-REMO-****-XOM6LP4Z-K0012-AR69Y7PGXQWT+120-AR69Y7PVMNBQ+080-270226-M000-FFEB::TEMP-NEG20
```

### 9.3 Anonymous vague cargo, 50 tons, incognito destination
```
P120-CARG-ROAD-****-NORM-NORM-FULL-ELEC-********-T0050-AR69Y7______0000-????????????????-270226-H006-E121
```

### 9.4 Private executive flight, 4 pax, return
```
P120-PASS-AIRS-****-EXEC-NORM-HUMA-****-XOM6LP4Z-P0004-AR69Y7PG____0000-????????????????-270226-H002-F7BA::SHAR-NO::RETN-YES
```

### 9.5 Live cattle transport, 450 kg
```
P120-ANIM-ROAD-LIVE-NORM-NORM-HUMA-****-********-K0450-AR69Y7______0000-????????????????-270226-H006-B185::SPEC-BOVI
```

### 9.6 LNG tanker maritime, 5,000 kL
```
P120-CARG-SEAS-HAZM-NORM-NORM-****-****-********-G5000-AR69Y7PG____0000-????????????????-270226-D003-8CCA::ENRG-GNGL
```

### 9.7 Rideshare / Uber Pool, 1 pax, urgent
```
P120-PASS-ROAD-****-ECON-URGE-****-****-********-P0001-6GF3V7______0000-????????????????-270226-M010-844F::SHAR-YES
```

---

## 10. Privacy & Handshake Protocol

**Phase 1 — Discovery:** Buyer publishes UODI with `OWNR=********` and `DEST=????????????????`. Matching engines filter on MODE, TYPE, CLAS, PRIO, CANT, and approximate ORIG without accessing identity or exact coordinates.

**Phase 2 — Handshake:** Upon bilateral agreement (O4DB DID cryptographic handshake), buyer discloses exact ORIG/DEST and identity. The original CHK4 serves as tamper-evident reference token.

**Two adoption paths:**
- **Direct:** Operator exposes UODI-native endpoint.
- **Via O4DB:** O4DB aggregates across operators; operator need not adopt UODI natively.

---

## 11. License & Intellectual Property

**Copyright © 2026 Daniel Eduardo Placanica. All rights reserved.**

### Open Core License

Free to use for any purpose (including commercial) provided:

1. All implementations include: *"Built on UODI-O4DB Standard — Original specification by Daniel Eduardo Placanica (2026)"*
2. Modifications documented as derivatives; do not claim to be the original UODI standard.
3. Derivatives retain the `P1xx` prefix family to indicate compatibility lineage.

### Protected Elements

- The 15-block Core sequence, positional architecture, name `UODI`, and prefix family `P1xx` are proprietary. No entity may publish a competing standard using these without written authorization from the Author.
- The **Placanica Verified (PLVR)** seal (`::CERT-PLVR`) is issued exclusively by the Author. Commercial certification licensing applies.

---

## 12. Revision History

| Version | Prefix | Blocks | Date | Changes |
|:--------|:------:|:------:|:-----|:--------|
| v1.0 | P100 | 14 | Feb 2026 | Initial specification |
| v1.1 | P100 | 14 | Feb 2026 | ORIG/DEST fixed 16 chars; CRC canonical defined; OWNR algorithm; DATE→DDMMYY; RAIL added; ANIM/SPEC formalized; ORBT tail; CLAS/PRIO semantics |
| v1.2 | P120 | 15 | Feb 2026 | Prefix versioning introduced; CANT block added (pos 10, w=5); padding `_` replacing `-` in ORIG/DEST; ::SHAR; ::RETN; ::ENRG; M000=immediate clarified; Working Group removed — Author is sole certification authority; all 7 examples validated with live CRC |
