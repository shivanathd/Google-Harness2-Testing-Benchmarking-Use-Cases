#!/usr/bin/env python3
"""Net settled revenue in USD for one month from a payment export + FX table.
Stdlib only.  Usage:
  python3 settled_revenue.py TRANSACTIONS.csv FX.csv YYYY-MM [OUT_JSON]
Prints a reconciliation (row counts, dropped duplicates, per-currency subtotals,
unparseable values) to stdout; writes {"net_usd","transactions"} if OUT_JSON given.
Adjust STATUS / column names at the top if the export differs."""
import csv, json, re, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

STATUS = "SETTLED"
DATE_FORMATS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d"]


def parse_date(s):
    s = s.strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            pass
    raise ValueError("unparseable date: %r" % s)


def parse_amount(s):
    t = s.strip().replace("−", "-")
    neg = t.startswith("(") and t.endswith(")")
    t = re.sub(r"[()\s,$€₹£]", "", t)
    if t.startswith("-"):
        neg, t = True, t[1:]
    v = Decimal(t)
    return -v if neg else v


def main():
    tx_path, fx_path, month = sys.argv[1:4]
    out = sys.argv[4] if len(sys.argv) > 4 else None
    with open(fx_path, newline="", encoding="utf-8-sig") as f:
        fx = {r["currency"].strip().upper(): Decimal(r["usd_per_unit"].strip()) for r in csv.DictReader(f)}
    with open(tx_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    seen, kept, dup, conflict = {}, [], 0, []
    for r in rows:
        r = {k.strip(): (v or "").strip() for k, v in r.items()}
        key = r["txn_id"]
        if key in seen:
            dup += 1
            if seen[key] != r:
                conflict.append((seen[key], r))
            continue
        seen[key] = r
        kept.append(r)
    total, n, by_cur, bad = Decimal(0), 0, {}, []
    for r in kept:
        try:
            d = parse_date(r["date"]); a = parse_amount(r["amount"])
        except Exception as e:
            bad.append((r, str(e))); continue
        if r["status"].upper() != STATUS or d.strftime("%Y-%m") != month:
            continue
        cur = r["currency"].upper()
        if cur not in fx:
            bad.append((r, "no fx rate")); continue
        usd = a * fx[cur]
        total += usd; n += 1
        c = by_cur.setdefault(cur, [0, Decimal(0), Decimal(0)])
        c[0] += 1; c[1] += a; c[2] += usd
    print("rows read=%d unique txn_id=%d duplicate rows dropped=%d" % (len(rows), len(kept), dup))
    print("duplicates with CONFLICTING content:", conflict or "none")
    print("unparseable / unmapped:", bad or "none")
    for cur, (cnt, native, usd) in sorted(by_cur.items()):
        print("  %s: n=%d native=%s usd=%s" % (cur, cnt, native, usd.quantize(Decimal("0.0001"))))
    net = float(total.quantize(Decimal("0.01"), ROUND_HALF_UP))
    print("RESULT net_usd=%s transactions=%d" % (net, n))
    if out:
        with open(out, "w") as f:
            json.dump({"net_usd": net, "transactions": n}, f)


main()
