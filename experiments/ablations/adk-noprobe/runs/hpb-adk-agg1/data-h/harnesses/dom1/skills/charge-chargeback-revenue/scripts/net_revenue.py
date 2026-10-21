#!/usr/bin/env python3
"""Net revenue for one month from charges + chargebacks + customers + fx exports.

usage: python3 net_revenue.py <source_dir> <YYYY-MM> <output_json>
Rules mirror a typical finance-ops POLICY.md; re-read the task's POLICY.md and edit
the constants below if it differs (fee, status, minor-unit divisors).
"""
import csv, json, sys, os
from decimal import Decimal as D, ROUND_HALF_UP
from datetime import datetime, timezone

FEE = D("15.00")
STATUS = "captured"
MINOR = {"USD": 100, "EUR": 100, "INR": 100, "JPY": 1}  # JPY: whole yen

def utc(s):
    return datetime.fromisoformat(s.strip().replace("Z", "+00:00")).astimezone(timezone.utc) if "+" in s[10:] or "-" in s[10:] or s.endswith("Z") else datetime.fromisoformat(s.strip()).replace(tzinfo=timezone.utc)

def rows(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))

def main(src, month, out):
    y, m = map(int, month.split("-"))
    fx = {r["currency"].strip(): D(r["usd_per_unit"]) for r in rows(os.path.join(src, "fx.csv"))}
    test = {r["customer_id"].strip() for r in rows(os.path.join(src, "customers.csv"))
            if r["is_test"].strip().lower() == "true"}
    charges = {}
    for r in rows(os.path.join(src, "charges.csv")):
        if r["charge_id"] in charges:
            print("DUPLICATE charge_id", r["charge_id"])
        charges[r["charge_id"]] = r
    def usd(c):
        cur = c["currency"].strip()
        if cur not in fx or cur not in MINOR:
            sys.exit("missing fx/minor-unit for " + cur)
        return D(c["amount_minor"]) / MINOR[cur] * fx[cur]
    inm = lambda t: (t.year, t.month) == (y, m)
    total, n = D(0), 0
    print("RECOGNISED")
    for c in charges.values():
        if c["status"].strip() != STATUS:
            continue
        if c["customer_id"] in test:
            print("  skip test", c["charge_id"]); continue
        t = utc(c["captured_at"])
        if inm(t):
            n += 1; total += usd(c)
            print("  ", c["charge_id"], c["currency"], t.isoformat(), usd(c))
    cbn = 0
    print("CHARGEBACKS")
    for cb in rows(os.path.join(src, "chargebacks.csv")):
        c = charges.get(cb["charge_id"])
        if c is None:
            print("  ORPHAN", cb["charge_id"]); continue
        t = utc(cb["chargeback_at"])
        why = "test customer" if c["customer_id"] in test else ("not in month" if not inm(t) else "")
        print("  ", cb["chargeback_id"], cb["charge_id"], t.isoformat(), c["status"], why or "BOOKED")
        if why:
            continue
        cbn += 1; total -= usd(c) + FEE
    net = total.quantize(D("0.01"), ROUND_HALF_UP)
    res = {"net_usd": float(net), "transactions": n, "chargebacks": cbn}
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w") as f:
        json.dump(res, f)
    print("unrounded", total, "->", json.load(open(out)))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
