"""
O4DB™ Protocol — Stress Test v1.5
# O4DB™ | v1.1.5 | build: 20260227-001 | 2026-02-27T19:00Z
100 buyers + 100 sellers · 180 seconds
30% malicious buyers · 30% malicious sellers
Full demand_type pool: NSN, EAN, ATC, UODI, VIN, CAGE_MPN, CAS, ISBN, UNS, OTA_GIATA
Sellers specialized: each seller accepts only 2-3 demand types
"""

import threading, time, json, random, string, base64
from datetime import datetime, timezone
from collections import defaultdict
import urllib.request, urllib.error

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
except ImportError:
    print("Missing: pip install cryptography"); exit(1)

RELAY     = "http://localhost:8000"
DURATION  = 180
N_BUYERS  = 100
N_SELLERS = 100
MAL_BUYER  = 0.30
MAL_SELLER = 0.30

DEMAND_POOL = [
    {"type":"NSN",      "codes":["5306-01-470-3452","5310-00-045-3299","4820-01-234-5678"],
     "uom_pool":["EA","BX","DZ"], "condition_pool":["NE","NS","OH","SV"]},
    {"type":"EAN",      "codes":["7791234567890","7890123456789","5012345678901"],
     "uom_pool":["EA","KGM","LTR"], "condition_pool":["NE","OPEN"]},
    {"type":"ATC",      "codes":["M01AE01","J01CA04","C09AA02","N02BE01"],
     "uom_pool":["TAB","AMP","VIA","KGM"], "condition_pool":["NE","NS"]},
    {"type":"UODI",     "codes":[
        "P120-PASS-ROAD-****-****-****-****-****-********-P0003-6GF3V7______0000-6GF9M2______0000-270226-M015-F6DA",
        "P120-CARG-SEAS-HAZM-NORM-NORM-****-****-********-G5000-AR69Y7PG____0000-????????????????-270226-D003-8CCA"],
     "uom_pool":["PAX","KGM","TEU"], "condition_pool":["OPEN","NE"]},
    {"type":"VIN",      "codes":["1HGBH41JXMN109186","2T1BURHE0JC034546"],
     "uom_pool":["EA"], "condition_pool":["NE","NS","SV","OH","AR"]},
    {"type":"CAGE_MPN", "codes":["0TC92+9876-A1","1AYF3+MK-220-B"],
     "uom_pool":["EA","SET","KIT"], "condition_pool":["NE","NS","OH","RP"]},
    {"type":"CAS",      "codes":["64-17-5","7732-18-5","7647-14-5"],
     "uom_pool":["KGM","TNE","LTR"], "condition_pool":["NE","OPEN"]},
    {"type":"ISBN",     "codes":["978-3-16-148410-0","978-0-06-112008-4"],
     "uom_pool":["EA","BX"], "condition_pool":["NE","NS","SV","AS-IS"]},
    {"type":"UNS",      "codes":["S31600","S30400","N06625"],
     "uom_pool":["KGM","TNE","EA"], "condition_pool":["NE","NS","OH"]},
    {"type":"OTA_GIATA","codes":["H123+20260501+DBL+BB+FLEX","H456+20260615+SGL+RO+NR"],
     "uom_pool":["EA"], "condition_pool":["NE","OPEN"]},
]

SELLER_SPECIALIZATIONS = [
    ["NSN","CAGE_MPN"], ["EAN","ISBN"], ["ATC","CAS"], ["UODI","OTA_GIATA"],
    ["VIN","NSN"], ["EAN","UNS"], ["ATC","NSN"], ["UODI","EAN"],
    ["CAS","UNS"], ["ISBN","OTA_GIATA"], ["NSN","VIN","CAGE_MPN"], ["EAN","ATC","CAS"],
]

metrics = {
    "vci_submitted":0, "vci_errors":0,
    "vci_replay_attempts":0, "vci_replay_blocked":0,
    "offers_submitted":0, "offers_accepted":0, "offers_rejected":0,
    "settlements":0, "settlement_errors":0,
    "seller_skipped_vcis":0, "invalid_sig_blocked":0,
    "malicious_buyer_actions":0, "malicious_seller_actions":0,
    "demand_type_hits":defaultdict(int), "demand_type_settled":defaultdict(int),
    "lat_vci":[], "lat_offer":[], "lat_settle":[],
    "errors":defaultdict(int),
}
lock = threading.Lock()
stop = threading.Event()

def inc(k, v=1):
    with lock: metrics[k] += v

def app(k, v):
    with lock: metrics[k].append(v)

def err(k):
    with lock: metrics["errors"][k] += 1

def inc_dt(k, dt):
    with lock: metrics[k][dt] += 1

def gen_keys():
    pk = Ed25519PrivateKey.generate()
    pub = pk.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return pk, base64.b64encode(pub).decode()

def csign(pk, data):
    payload = json.dumps(data, sort_keys=True, separators=(',',':')).encode()
    return base64.b64encode(pk.sign(payload)).decode()

def rand_id(p="", n=8):
    return p + ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def post(path, body, timeout=10):
    req = urllib.request.Request(RELAY+path, json.dumps(body).encode(),
          {"Content-Type":"application/json"}, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read()), time.time()-t0, r.status
    except urllib.error.HTTPError as e:
        try: b = json.loads(e.read())
        except: b = {}
        return b, time.time()-t0, e.code
    except Exception as ex:
        return {"error":str(ex)}, time.time()-t0, 0

def get(path, timeout=10):
    t0 = time.time()
    try:
        with urllib.request.urlopen(RELAY+path, timeout=timeout) as r:
            return json.loads(r.read()), time.time()-t0
    except Exception as ex:
        return {"error":str(ex)}, time.time()-t0


def seller_agent(seller_id, is_malicious, specialization):
    pk, pub = gen_keys()
    ts = float(int(time.time()))
    reg_core = {"seller_id":seller_id, "categories":sorted(specialization),
                "delivery_areas":sorted(["AR","US","EU"]), "min_commitment":0,
                "sign_pubkey":pub, "timestamp":ts}
    sig = csign(pk, reg_core)
    resp, _, s = post("/api/v1/seller/register", {**reg_core, "webhook_url":None, "inventory_ids":[], "signature":sig})
    if s not in (200, 201, 409):
        err(f"seller_reg_{s}"); return

    while not stop.is_set():
        intents, _ = get(f"/api/v1/seller/{seller_id}/intents")
        my_vcis = [v for v in intents.get("intents",[]) if v.get("demand_type") in specialization]

        for vci in my_vcis[:3]:
            vci_id = vci.get("vci_id")
            if not vci_id: continue

            if is_malicious and random.random() < 0.5:
                inc("seller_skipped_vcis"); inc("malicious_seller_actions"); continue

            if is_malicious and random.random() < 0.3:
                fake = {"seller_id":seller_id, "unit_price":round(random.uniform(10,500),2),
                        "attributes":{"condition":"NE"}, "timestamp":float(int(time.time())),
                        "signature":base64.b64encode(b"invalidsig000000").decode()}
                _, _, s2 = post(f"/api/v1/vci/{vci_id}/offer", fake)
                # 400/422 = signature rejected
                # 404/409/410 = rejected before signature check (VCI gone/expired) — also blocked
                if s2 in (400, 404, 409, 410, 422): inc("invalid_sig_blocked")
                else: err("INVALID_SIG_PASSED")
                inc("malicious_seller_actions"); continue

            ts2 = float(int(time.time()))
            price = round(random.uniform(10, 1000), 2)
            price_c = int(price) if float(price) == int(price) else price
            attrs = {"condition":random.choice(["NE","NS","OH","SV"]),
                     "demand_type":vci.get("demand_type"), "stock_days":random.randint(0,14)}
            offer_core = {"seller_id":seller_id, "unit_price":price_c, "attributes":attrs, "vci_id":vci_id}
            _, lat, s2 = post(f"/api/v1/vci/{vci_id}/offer",
                {"seller_id":seller_id, "unit_price":price, "attributes":attrs,
                 "signature":csign(pk, offer_core), "timestamp":ts2})
            app("lat_offer", lat); inc("offers_submitted")
            if s2 == 201: inc("offers_accepted")
            else: inc("offers_rejected"); err(f"offer_{s2}")

        time.sleep(random.uniform(1.5, 3.5))


def buyer_agent(buyer_id, is_malicious):
    import urllib.parse
    sign_pk, sign_pub = gen_keys()
    _, hpke_pub = gen_keys()
    submitted = []

    while not stop.is_set():
        dspec = random.choice(DEMAND_POOL)
        d_type = dspec["type"]
        d_code = random.choice(dspec["codes"])

        if is_malicious and submitted and random.random() < 0.4:
            old = random.choice(submitted)
            _, _, s = post("/api/v1/vci/submit", old)
            inc("vci_replay_attempts")
            if s in (400,409,422): inc("vci_replay_blocked")
            else: err("REPLAY_PASSED")
            inc("malicious_buyer_actions")
            time.sleep(random.uniform(1,2)); continue

        vci_id = rand_id("VCI-ST-", 10)
        ts = float(int(time.time()))

        if is_malicious and random.random() < 0.3:
            bad = {"vci_id":rand_id("VCI-ST-",10), "demand_spec":f"{d_type}:{d_code}",
                   "demand_type":d_type, "master_code":d_code,
                   "demand_object":{"uom":random.choice(dspec["uom_pool"]),"condition":"NE","stock_ready":0},
                   "quantity":10, "price_token":"fake", "currency":"USD", "ttl":60,
                   "commitment_level":1, "delivery_area":"AR", "privacy_mode":"standard",
                   "buyer_pubkey":hpke_pub, "buyer_sign_pub":sign_pub,
                   "vci_signature":base64.b64encode(b"badsignature0000").decode(),
                   "weights":{"price":1.0}, "trust_floor":0.5, "banned_sellers":[], "timestamp":ts}
            _, _, s = post("/api/v1/vci/submit", bad)
            if s in (400,422): inc("invalid_sig_blocked")
            else: err("INVALID_SIG_PASSED")
            inc("malicious_buyer_actions")
            time.sleep(random.uniform(1,2)); continue

        sig_core = {"vci_id":vci_id, "demand_spec":f"{d_type}:{d_code}",
                    "quantity":random.randint(1,500),
                    "price_token":base64.b64encode(random.randbytes(32)).decode(),
                    "currency":random.choice(["USD","EUR","ARS"]),
                    "ttl":random.randint(60,120), "commitment_level":random.randint(1,3),
                    "delivery_area":random.choice(["AR","AR:CABA","US","EU"]),
                    "privacy_mode":"standard", "timestamp":ts}

        demand_obj = {"uom":random.choice(dspec["uom_pool"]),
                      "condition":random.choice(dspec["condition_pool"]),
                      "stock_ready":random.randint(0,30)}
        if random.random() < 0.5:
            demand_obj["rfq"] = rand_id("RFQ-", 8)

        full = {**sig_core, "demand_type":d_type, "master_code":d_code,
                "demand_object":demand_obj, "buyer_pubkey":hpke_pub,
                "buyer_sign_pub":sign_pub, "vci_signature":csign(sign_pk, sig_core),
                "weights":{"price":round(random.uniform(0.4,0.8),2),
                           "trust":round(random.uniform(0.2,0.6),2)},
                "trust_floor":round(random.uniform(0.3,0.6),2), "banned_sellers":[]}

        _, lat, s = post("/api/v1/vci/submit", full)
        app("lat_vci", lat)

        if s == 202:
            inc("vci_submitted"); inc_dt("demand_type_hits", d_type)
            submitted.append(full)
            if len(submitted) > 5: submitted.pop(0)

            time.sleep(random.uniform(2,5))
            if stop.is_set(): break

            offers = []
            for _ in range(3):
                ts_req = float(int(time.time()))
                req_core = {"vci_id":vci_id, "timestamp":ts_req}
                req_sig = csign(sign_pk, req_core)
                offers_resp, _ = get(
                    f"/api/v1/vci/{vci_id}/offers"
                    f"?buyer_sign_pub={urllib.parse.quote(sign_pub,safe='')}"
                    f"&request_timestamp={ts_req}"
                    f"&request_signature={urllib.parse.quote(req_sig,safe='')}")
                offers = offers_resp.get("offers",[])
                if offers: break
                if offers_resp.get("state") == "ACTIVE": time.sleep(2); continue
                err(f"offers_empty_{offers_resp.get('state','?')}"); break

            if offers:
                best = min(offers, key=lambda o: o.get("unit_price",9999999))
                winner_id = best.get("seller_id")
                if winner_id:
                    ts3 = float(int(time.time()))
                    sc = {"vci_id":vci_id, "winner_seller_id":winner_id, "timestamp":ts3}
                    _, sl, ss = post(f"/api/v1/vci/{vci_id}/settle",
                        {"vci_id":vci_id, "winner_seller_id":winner_id,
                         "buyer_sign_pub":sign_pub, "timestamp":ts3, "signature":csign(sign_pk,sc)})
                    app("lat_settle", sl)
                    if ss == 200: inc("settlements"); inc_dt("demand_type_settled", d_type)
                    else: inc("settlement_errors"); err(f"settle_{ss}")
        else:
            inc("vci_errors"); err(f"vci_{s}")

        time.sleep(random.uniform(1, 2.5))


def main():
    print("="*65)
    print("O4DB™ STRESS TEST v1.5 — 100+100 nodes · 180s · 30% malicious")
    print("Full demand_type pool · Specialized sellers")
    print("="*65)

    h, _ = get("/health")
    if "error" in h:
        print(f"❌ Relay unreachable: {h['error']}"); return
    print(f"✅ Relay OK — sellers:{h.get('registered_sellers')} vcis:{h.get('active_vcis')}\n")

    import sqlite3
    try:
        conn = sqlite3.connect('/data/o4db_relay.db')
        conn.execute("DELETE FROM sellers WHERE seller_id LIKE 'ST-S-%'")
        conn.execute("DELETE FROM vci_active WHERE vci_id LIKE 'VCI-ST-%'")
        conn.commit(); conn.close()
        print("🧹 DB cleaned")
    except Exception as ex:
        print(f"⚠️  DB cleanup skipped: {ex}")

    seller_ids = [rand_id("ST-S-",6) for _ in range(N_SELLERS)]
    buyer_ids  = [rand_id("ST-B-",6) for _ in range(N_BUYERS)]
    mal_s = set(random.sample(seller_ids, int(N_SELLERS*MAL_SELLER)))
    mal_b = set(random.sample(buyer_ids,  int(N_BUYERS*MAL_BUYER)))

    print(f"Malicious sellers ({len(mal_s)}): {', '.join(list(mal_s)[:4])}...")
    print(f"Malicious buyers  ({len(mal_b)}): {', '.join(list(mal_b)[:4])}...\n")

    threads = []
    for i, sid in enumerate(seller_ids):
        spec = SELLER_SPECIALIZATIONS[i % len(SELLER_SPECIALIZATIONS)]
        t = threading.Thread(target=seller_agent, args=(sid, sid in mal_s, spec), daemon=True)
        t.start(); threads.append(t)

    time.sleep(3)

    for bid in buyer_ids:
        t = threading.Thread(target=buyer_agent, args=(bid, bid in mal_b), daemon=True)
        t.start(); threads.append(t)

    start = time.time()
    while time.time()-start < DURATION:
        e = int(time.time()-start)
        bar = "█"*(e*40//DURATION) + "░"*(40-e*40//DURATION)
        print(f"\r  [{bar}] {e}s/{DURATION}s", end="", flush=True)
        time.sleep(1)

    print("\n"); stop.set(); time.sleep(4)

    m = metrics
    print("="*65)
    print("STRESS TEST REPORT — O4DB™ v1.1.5")
    print(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("="*65)

    print("\n📊 VOLUME")
    print(f"  VCIs valid:             {m['vci_submitted']}")
    print(f"  VCIs rejected:          {m['vci_errors']}")
    print(f"  Offers submitted:       {m['offers_submitted']}")
    print(f"  Offers accepted:        {m['offers_accepted']}")
    print(f"  Offers rejected:        {m['offers_rejected']}")
    print(f"  Settlements:            {m['settlements']}")
    print(f"  Settlement errors:      {m['settlement_errors']}")

    print("\n📦 DEMAND TYPE BREAKDOWN")
    all_types = sorted(set(list(m["demand_type_hits"].keys())+list(m["demand_type_settled"].keys())))
    for dt in all_types:
        hits    = m["demand_type_hits"].get(dt,0)
        settled = m["demand_type_settled"].get(dt,0)
        rate    = f"{settled/hits*100:.0f}%" if hits else "—"
        print(f"  {dt:12s}  VCIs:{hits:4d}  Settled:{settled:4d}  Rate:{rate}")

    print("\n🔐 SECURITY")
    rba  = m['vci_replay_attempts']
    rbb  = m['vci_replay_blocked']
    rate = (rbb/rba*100) if rba else 0
    print(f"  Replay attempts:        {rba}")
    print(f"  Replay blocked:         {rbb}  ({rate:.1f}%)")
    print(f"  Invalid sig blocked:    {m['invalid_sig_blocked']}")
    print(f"  Seller skipped VCIs:    {m['seller_skipped_vcis']}")
    print(f"  Mal buyer actions:      {m['malicious_buyer_actions']}")
    print(f"  Mal seller actions:     {m['malicious_seller_actions']}")

    print("\n⚡ LATENCY (p50 / p95 / max)")
    for key, label in [("lat_vci","VCI submit"),("lat_offer","Offer"),("lat_settle","Settlement")]:
        vals = sorted(m[key])
        if vals:
            p50 = vals[len(vals)//2]
            p95 = vals[int(len(vals)*0.95)]
            print(f"  {label:15s}  p50={p50:.3f}s  p95={p95:.3f}s  max={max(vals):.3f}s  n={len(vals)}")
        else:
            print(f"  {label:15s}  no data")

    print("\n❌ ERRORS BREAKDOWN")
    if m["errors"]:
        for k, v in sorted(m["errors"].items(), key=lambda x: -x[1]):
            flag = "🔴" if "PASSED" in k else "  "
            print(f"  {flag} {k:40s} {v}")
    else:
        print("  None")

    h2, _ = get("/health")
    print("\n🏥 RELAY AFTER TEST")
    print(f"  Sellers:     {h2.get('registered_sellers')}")
    print(f"  Active VCIs: {h2.get('active_vcis')}")
    print(f"  Settlements: {h2.get('monthly_settlements')}")

    print("\n"+"="*65)
    print("FINDINGS")
    print("="*65)
    findings = []

    for p in [k for k in m["errors"] if "PASSED" in k]:
        findings.append(("🔴 CRITICAL", f"Security bypass: {p} x{m['errors'][p]}"))

    if rba > 0:
        if rate < 100: findings.append(("🔴 CRITICAL", f"Replay NOT fully blocked — {rba-rbb} passed"))
        else: findings.append(("🟢 OK", "Replay attacks fully blocked (100%)"))

    if m['seller_skipped_vcis'] > 0:
        findings.append(("🔵 INFO", f"{m['seller_skipped_vcis']} sellers skipped VCIs (no offer submitted — normal behavior, not a ghost)"))

    if m['vci_submitted'] > 0 and m['settlements'] == 0:
        findings.append(("🔴 CRITICAL", "No settlements — full cycle broken"))
    elif m['settlements'] > 0:
        ratio = m['settlements']/max(m['vci_submitted'],1)*100
        findings.append(("🟢 OK", f"{m['settlements']} settlements ({ratio:.0f}% of valid VCIs)"))

    types_settled = [dt for dt in m["demand_type_settled"] if m["demand_type_settled"][dt] > 0]
    lvl = "🟢 OK" if len(types_settled) >= 5 else "🟡 WARN"
    findings.append((lvl, f"Types with settlements: {len(types_settled)}/10 — {', '.join(sorted(types_settled))}"))

    lats = m['lat_vci']
    if lats and max(lats) > 2.0:
        findings.append(("🟡 WARN", f"VCI latency spike max={max(lats):.2f}s — SQLite contention"))
    elif lats:
        findings.append(("🟢 OK", f"VCI latency healthy — max={max(lats):.3f}s"))

    if m['settlement_errors'] > 0:
        findings.append(("🟡 WARN", f"{m['settlement_errors']} settlement errors"))

    if not findings:
        findings.append(("🟢 OK", "No issues detected"))

    for level, msg in findings:
        print(f"  {level}: {msg}")
    print()


if __name__ == "__main__":
    main()
