#!/usr/bin/env python3
"""Monthly net USD revenue from transactions + refunds + daily fx table.

Usage: python3 scripts/net_revenue.py [YYYY-MM] [transactions.csv] [refunds.csv] [fx_daily.csv] [output/answer.json]
Defaults: 2026-09 transactions.csv refunds.csv fx_daily.csv output/answer.json
Stdlib only. Dedupes txn_id (and refund_id), recognises SETTLED rows by settled_on
month at that day's rate, subtracts refunds by refunded_on month at that day's rate,
rounds once, writes {"net_usd","transactions","refunds"}, re-reads it, prints every
included row and every exclusion. Exits 1 (no file written) on an unparseable value,
a missing fx rate (never substituted), a zero rate, or a conflicting duplicate key.
"""
import csv, json, os, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

FORMATS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d"]


def die(msg):
    sys.exit("ERROR: " + msg)


def pdate(s):
    s = s.strip()
    for f in FORMATS:
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


def rows(path, key):
    """Rows with stripped values, deduped on key; conflicting repeats abort."""
    seen, out = {}, []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            r = {k.strip(): (v or "").strip() for k, v in r.items()}
            if r[key] in seen:
                if seen[r[key]] != r:
                    die(f"{path}: {key} {r[key]} repeats with different values: {seen[r[key]]} vs {r}")
                print(f"skip duplicate {key} {r[key]}")
                continue
            seen[r[key]] = r
            out.append(r)
    return out


def main():
    a = sys.argv[1:]
    month = a[0] if a else "2026-09"
    tx, rf, fxp, outp = (a[1:] + ["transactions.csv", "refunds.csv", "fx_daily.csv", "output/answer.json"][len(a[1:]):])[:4]
    y, m = map(int, month.split("-"))
    inm = lambda d: (d.year, d.month) == (y, m)

    fx = {}
    with open(fxp, newline="") as f:
        for r in csv.DictReader(f):
            fx[(pdate(r["date"]), r["currency"].strip().upper())] = Decimal(r["usd_per_unit"])

    def rate(d, cur):
        v = fx.get((d, cur))
        if v is None or v <= 0:
            die(f"no usable fx rate for {cur} on {d} (got {v})")
        return v

    txs = rows(tx, "txn_id")
    print("statuses:", sorted({r["status"] for r in txs}))
    rev, n, cur_of = Decimal(0), 0, {}
    for r in txs:
        cur_of[r["txn_id"]] = r["currency"].upper()
        if r["status"].upper() != "SETTLED" or not r["settled_on"]:
            continue
        d = pdate(r["settled_on"])
        if not inm(d):
            continue
        cur = r["currency"].upper()
        usd = pamt(r["amount"]) * rate(d, cur)
        rev += usd; n += 1
        print(f"TX  {r['txn_id']} {d} {r['amount']} {cur} -> {usd:.6f}")

    ref, k = Decimal(0), 0
    for r in rows(rf, "refund_id"):
        d = pdate(r["refunded_on"])
        if r["txn_id"] not in cur_of:
            die(f"refund {r['refund_id']} references unknown txn_id {r['txn_id']}")
        if not inm(d):
            print(f"out of month refund {r['refund_id']} {d}")
            continue
        cur = cur_of[r["txn_id"]]
        usd = pamt(r["amount"]) * rate(d, cur)
        ref += usd; k += 1
        print(f"REF {r['refund_id']} {r['txn_id']} {d} {r['amount']} {cur} -> {usd:.6f}")

    net = float((rev - ref).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    os.makedirs(os.path.dirname(outp) or ".", exist_ok=True)
    with open(outp, "w") as f:
        json.dump({"net_usd": net, "transactions": n, "refunds": k}, f)
    with open(outp) as f:
        back = json.load(f)
    assert set(back) == {"net_usd", "transactions", "refunds"}
    print(f"gross {rev:.6f} refunds {ref:.6f}; wrote {outp}: {back}")


if __name__ == "__main__":
    main()
