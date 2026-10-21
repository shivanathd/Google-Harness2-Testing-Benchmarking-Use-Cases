#!/usr/bin/env python3
"""Monthly net revenue in USD from transactions + refunds + daily FX (stdlib only).

Usage: python3 scripts/net_revenue.py \
         TRANSACTIONS.csv REFUNDS.csv FX.csv YYYY-MM [OUT.json]
Defaults (month has none; pass it): transactions.csv refunds.csv fx_daily.csv output/answer.json
Expected columns: transactions txn_id,settled_on,amount,currency,status;
refunds refund_id,txn_id,refunded_on,amount; fx date,currency,usd_per_unit.
Revenue: first row per txn_id, status exactly SETTLED, settled_on in month, FX of settled_on.
Refunds: refunded_on in month, currency of the ORIGINAL txn, FX of refunded_on.
Writes {"net_usd","transactions","refunds"}, re-reads it, prints every skipped row.
Exits 1 on an unparseable value, missing/zero FX rate, or refund with unknown txn_id.
"""
import csv, json, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

FMTS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d"]
C = Decimal("0.01")


def die(msg):
    sys.exit("ERROR: " + msg)


def pdate(s):
    s = s.strip()
    for f in FMTS:
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            pass
    die(f"unparseable date {s!r}")


def pamt(s):
    t = s.strip().replace(",", "").replace("$", "").replace(" ", "")
    neg = t.startswith("(") and t.endswith(")")
    try:
        v = Decimal(t.strip("()"))
    except Exception:
        die(f"unparseable amount {s!r}")
    return -v if neg else v


def main():
    a = sys.argv[1:]
    txp, rfp, fxp, month, out = (a + [None] * 5)[:5]
    txp, rfp, fxp = txp or "transactions.csv", rfp or "refunds.csv", fxp or "fx_daily.csv"
    if not month:
        sys.exit("ERROR: month (YYYY-MM) required: take it from the task")
    out = out or "output/answer.json"
    y, m = map(int, month.split("-"))
    inm = lambda d: (d.year, d.month) == (y, m)

    fx = {}
    for r in csv.DictReader(open(fxp, newline="")):
        fx[(pdate(r["date"]), r["currency"].strip().upper())] = Decimal(r["usd_per_unit"])

    def rate(d, cur, what):
        v = fx.get((d, cur))
        if v is None or v <= 0:
            die(f"{what}: missing or zero FX rate for {cur} on {d}")
        return v

    seen, cur_of = {}, {}
    rev = rev_rl = Decimal(0)
    n = 0
    for r in csv.DictReader(open(txp, newline="")):
        tid = r["txn_id"].strip()
        key = tuple(v.strip() for v in r.values())
        if tid in seen:
            print(f"skip {tid}: {'exact' if seen[tid] == key else 'CONFLICTING'} duplicate")
            continue
        seen[tid] = key
        cur_of[tid] = r["currency"].strip().upper()
        if r["status"].strip() != "SETTLED" or not r["settled_on"].strip():
            continue
        d = pdate(r["settled_on"])
        if not inm(d):
            continue
        v = pamt(r["amount"]) * rate(d, cur_of[tid], tid)
        rev += v
        rev_rl += v.quantize(C, ROUND_HALF_UP)
        n += 1

    ref = ref_rl = Decimal(0)
    k = 0
    rseen = set()
    for r in csv.DictReader(open(rfp, newline="")):
        rid = r["refund_id"].strip()
        if rid in rseen:
            print(f"skip refund {rid}: duplicate refund_id")
            continue
        rseen.add(rid)
        tid = r["txn_id"].strip()
        if tid not in cur_of:
            die(f"refund {rid} references unknown txn_id {tid}")
        d = pdate(r["refunded_on"])
        if not inm(d):
            continue
        if seen[tid][-1] != "SETTLED":
            print(f"WARN refund {rid} on non-SETTLED txn {tid}: counted anyway, review")
        v = pamt(r["amount"]) * rate(d, cur_of[tid], rid)
        ref += v
        ref_rl += v.quantize(C, ROUND_HALF_UP)
        k += 1

    net = (rev - ref).quantize(C, ROUND_HALF_UP)
    net_rl = rev_rl - ref_rl
    import os
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as f:
        json.dump({"net_usd": float(net), "transactions": n, "refunds": k}, f)
    with open(out) as f:
        back = json.load(f)
    assert isinstance(back, dict) and set(back) == {"net_usd", "transactions", "refunds"}
    print(f"unique txn_ids {len(seen)}; revenue {rev:.6f}; refunds {ref:.6f}; net {net}")
    if net_rl != net:
        print(f"NOTE: rounding each line first gives {net_rl} (differs from {net}); total rounded once was written")
    print(f"wrote {out}: {back}")


if __name__ == "__main__":
    main()
