#!/usr/bin/env python3
"""Deterministic revenue reconciliation: transactions + refunds + daily FX -> net USD for one month.

Usage: python3 scripts/reconcile_revenue.py YYYY-MM [--dir .] [--out output/answer.json] [--dry]
Inputs (in --dir): transactions.csv (txn_id,created_on,settled_on,amount,currency,status),
  refunds.csv (refund_id,txn_id,refunded_on,amount), fx_daily.csv (date,currency,usd_per_unit).
Rules: exact duplicate txn_id rows collapse to one (conflicting duplicates abort); amounts may carry
thousands commas; only status SETTLED with settled_on in the month counts, at that day's rate;
refunds count by refunded_on month, in the ORIGINAL txn's currency, at the refund day's rate.
Writes {"net_usd","transactions","refunds"}; prints a per-row audit and anomalies to stderr.
Exit 1 on missing file/column, conflicting duplicates, unparseable amount, or missing FX rate.
"""
import csv, json, os, sys
from decimal import Decimal, ROUND_HALF_UP

def die(m):
    print("ERROR: " + m, file=sys.stderr); sys.exit(1)

def rows(path, cols):
    if not os.path.exists(path): die("missing " + path)
    with open(path, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        miss = [c for c in cols if c not in (rd.fieldnames or [])]
        if miss: die("%s lacks columns %s (has %s)" % (path, miss, rd.fieldnames))
        return [{k: (v or "").strip() for k, v in r.items()} for r in rd]

def num(s, what):
    try: return Decimal(s.replace(",", ""))
    except Exception: die("bad amount %r in %s" % (s, what))

def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("-"): die(__doc__)
    month = a[0]; d = "."; out = "output/answer.json"; dry = "--dry" in a
    if "--dir" in a: d = a[a.index("--dir") + 1]
    if "--out" in a: out = a[a.index("--out") + 1]
    fx = {}
    for r in rows(os.path.join(d, "fx_daily.csv"), ["date", "currency", "usd_per_unit"]):
        fx[(r["date"], r["currency"])] = Decimal(r["usd_per_unit"])
    def rate(day, cur, what):
        if (day, cur) not in fx: die("no FX rate for %s on %s (%s)" % (cur, day, what))
        return fx[(day, cur)]
    txns = {}
    for r in rows(os.path.join(d, "transactions.csv"), ["txn_id", "settled_on", "amount", "currency", "status"]):
        t = r["txn_id"]
        if t in txns:
            if txns[t] != r: die("conflicting duplicate rows for txn_id %s: %s vs %s" % (t, txns[t], r))
            print("note: exact duplicate row collapsed: " + t, file=sys.stderr); continue
        txns[t] = r
    total = Decimal(0); n = 0
    for t, r in sorted(txns.items()):
        if r["status"].upper() != "SETTLED" or not r["settled_on"].startswith(month): continue
        usd = num(r["amount"], t) * rate(r["settled_on"], r["currency"], t)
        total += usd; n += 1
        print("TXN %s %s %s %s -> %.4f" % (t, r["settled_on"], r["amount"], r["currency"], usd), file=sys.stderr)
    ref = Decimal(0); m = 0
    for r in rows(os.path.join(d, "refunds.csv"), ["refund_id", "txn_id", "refunded_on", "amount"]):
        if not r["refunded_on"].startswith(month): continue
        o = txns.get(r["txn_id"])
        if o is None: print("WARN: refund %s references unknown txn %s -- skipped, decide explicitly" % (r["refund_id"], r["txn_id"]), file=sys.stderr); continue
        if o["status"].upper() != "SETTLED": print("WARN: refund %s is on non-SETTLED txn %s (%s)" % (r["refund_id"], o["txn_id"], o["status"]), file=sys.stderr)
        usd = num(r["amount"], r["refund_id"]) * rate(r["refunded_on"], o["currency"], r["refund_id"])
        ref += usd; m += 1
        print("REF %s %s %s %s %s -> %.4f" % (r["refund_id"], r["txn_id"], r["refunded_on"], r["amount"], o["currency"], usd), file=sys.stderr)
    net = (total - ref).quantize(Decimal("0.01"), ROUND_HALF_UP)
    res = {"net_usd": float(net), "transactions": n, "refunds": m}
    print("gross %.4f refunds %.4f" % (total, ref), file=sys.stderr)
    print(json.dumps(res))
    if not dry:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w") as f: json.dump(res, f)
        print("wrote " + out, file=sys.stderr)

main()
