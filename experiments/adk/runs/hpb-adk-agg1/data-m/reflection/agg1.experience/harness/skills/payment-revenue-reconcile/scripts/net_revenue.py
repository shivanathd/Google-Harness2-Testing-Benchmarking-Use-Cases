#!/usr/bin/env python3
"""Monthly net revenue in USD from transactions + refunds + daily FX (stdlib only).

usage: net_revenue.py TRANSACTIONS.csv REFUNDS.csv FX_DAILY.csv YYYY-MM [--out output/answer.json]
Expected columns: transactions txn_id,settled_on,amount,currency,status;
refunds refund_id,txn_id,refunded_on,amount; fx date,currency,usd_per_unit.
Recognises SETTLED transactions by settled_on month at that day's rate, subtracts refunds
issued in the month (currency taken from the original txn) at the refund day's rate.
Prints an audit, then the JSON. Exits non-zero on anything it cannot parse, a missing or
non-positive rate on a needed date, or a refund whose txn_id is unknown. With --out it
writes the file and re-reads it to check.
"""
import csv, json, re, sys
from collections import Counter
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

DATE_FORMATS = ("%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d")


def amount(s):
    t = s.strip().replace("$", "").replace(" ", "")
    neg = (t.startswith("(") and t.endswith(")")) or t.startswith("-")
    t = re.sub(r"[()\-,]", "", t)
    if not re.fullmatch(r"\d+(\.\d+)?", t):
        sys.exit(f"UNPARSEABLE AMOUNT: {s!r}")
    return -Decimal(t) if neg else Decimal(t)


def day(s):
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s.strip(), f).date()
        except ValueError:
            pass
    sys.exit(f"UNPARSEABLE DATE: {s!r}")


def rate(fx, d, cur):
    r = fx.get((d, cur))
    if r is None or r <= 0:
        sys.exit(f"NO USABLE FX RATE for {cur} on {d}: {r}")
    return r


def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    a = sys.argv[1:]
    out = None
    if "--out" in a:
        i = a.index("--out")
        out = a[i + 1]
        del a[i:i + 2]
    tx_p, rf_p, fx_p, ym = a[:4]
    year, month = map(int, ym.split("-"))
    fx = {(day(r["date"]), r["currency"].strip().upper()): Decimal(r["usd_per_unit"]) for r in load(fx_p)}

    # dedupe on id before filtering
    txs = {}
    for r in load(tx_p):
        k = r["txn_id"].strip()
        if k in txs and txs[k] != r:
            print(f"CONFLICTING DUPLICATE {k}: {txs[k]} vs {r} -- decide explicitly")
        txs.setdefault(k, r)
    raw = load(tx_p)
    print(f"tx rows={len(raw)} unique ids={len(txs)} status={dict(Counter(r['status'] for r in txs.values()))}")
    print("duplicate txn_ids:", sorted(k for k, c in Counter(r['txn_id'].strip() for r in raw).items() if c > 1))

    rev, n = Decimal(0), 0
    for k, r in sorted(txs.items()):
        if r["status"].strip().upper() != "SETTLED":
            continue
        if not r["settled_on"].strip():
            sys.exit(f"SETTLED without settled_on: {k}")
        d = day(r["settled_on"])
        if (d.year, d.month) != (year, month):
            continue
        cur = r["currency"].strip().upper()
        usd = amount(r["amount"]) * rate(fx, d, cur)
        rev += usd
        n += 1
        print(f"  txn {k} {d} {r['amount']} {cur} -> {usd:.6f}")

    refs = {}
    for r in load(rf_p):
        k = r["refund_id"].strip()
        if k in refs and refs[k] != r:
            print(f"CONFLICTING DUPLICATE refund {k} -- decide explicitly")
        refs.setdefault(k, r)
    ref, m = Decimal(0), 0
    for k, r in sorted(refs.items()):
        d = day(r["refunded_on"])
        if (d.year, d.month) != (year, month):
            continue
        t = txs.get(r["txn_id"].strip())
        if t is None:
            sys.exit(f"REFUND {k} references unknown txn {r['txn_id']}")
        if t["status"].strip().upper() != "SETTLED":
            print(f"  WARNING refund {k} is on non-SETTLED txn {r['txn_id']} ({t['status']}) -- applied; decide")
        cur = t["currency"].strip().upper()
        usd = amount(r["amount"]) * rate(fx, d, cur)
        ref += usd
        m += 1
        print(f"  refund {k} {r['txn_id']} {d} {r['amount']} {cur} -> -{usd:.6f}")

    q = lambda v: v.quantize(Decimal("0.01"), ROUND_HALF_UP)
    print(f"revenue={rev:.6f} refunds={ref:.6f}")
    result = {"net_usd": float(q(rev - ref)), "transactions": n, "refunds": m}
    print(json.dumps(result))
    if out:
        with open(out, "w") as f:
            json.dump(result, f)
        chk = json.load(open(out))
        assert chk == result, "written file differs"
        print(f"wrote and re-read {out}")


main()
