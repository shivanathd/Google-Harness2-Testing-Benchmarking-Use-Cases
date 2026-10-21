#!/usr/bin/env python3
"""Monthly net revenue in USD from charges + chargebacks + customers + fx (stdlib only).

usage: net_revenue.py CHARGES.csv CHARGEBACKS.csv CUSTOMERS.csv FX.csv YYYY-MM [--out output/answer.json]
Columns: charges charge_id,customer_id,currency,amount_minor,status,captured_at (ISO with offset);
chargebacks chargeback_id,charge_id,chargeback_at (UTC 'Z'); customers customer_id,is_test;
fx currency,usd_per_unit.
Rules: status exactly 'captured', month decided on the UTC-converted captured_at; amount_minor / 10^exp
(JPY 0, INR/USD/EUR 2); test customers excluded everywhere; chargeback reverses the full original
charge and adds a 15.00 USD fee, both booked in the UTC month of chargeback_at; round only the final net.
Prints an audit, then the JSON; exits non-zero on anything unparseable, unknown currency/customer/charge.
With --out it writes the file and re-reads it.
"""
import csv, json, sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

EXP = {"JPY": 0, "KRW": 0, "USD": 2, "EUR": 2, "INR": 2}
FEE = Decimal("15.00")


def ts(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        d = datetime.fromisoformat(s)
    except ValueError:
        sys.exit(f"UNPARSEABLE TIMESTAMP: {s!r}")
    if d.tzinfo is None:
        sys.exit(f"TIMESTAMP WITHOUT OFFSET: {s!r}")
    return d.astimezone(timezone.utc)


def load(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def usd(row, fx):
    cur = row["currency"].strip().upper()
    if cur not in EXP:
        sys.exit(f"UNKNOWN CURRENCY EXPONENT: {cur}")
    if cur not in fx or fx[cur] <= 0:
        sys.exit(f"NO USABLE FX RATE: {cur}")
    return Decimal(row["amount_minor"].strip()) / (Decimal(10) ** EXP[cur]) * fx[cur]


def main():
    a = sys.argv[1:]
    out = None
    if "--out" in a:
        i = a.index("--out")
        out = a[i + 1]
        del a[i:i + 2]
    ch_p, cb_p, cu_p, fx_p, ym = a[:5]
    year, month = map(int, ym.split("-"))
    fx = {r["currency"].strip().upper(): Decimal(r["usd_per_unit"]) for r in load(fx_p)}
    test = {r["customer_id"].strip(): r["is_test"].strip().lower() == "true" for r in load(cu_p)}
    charges = {}
    for r in load(ch_p):
        k = r["charge_id"].strip()
        if k in charges:
            print(f"DUPLICATE charge_id {k} -- kept first")
            continue
        if r["customer_id"].strip() not in test:
            sys.exit(f"CUSTOMER NOT IN customers.csv: {r['customer_id']} (charge {k})")
        charges[k] = r

    rev, n = Decimal(0), 0
    for k, r in sorted(charges.items()):
        if r["status"].strip() != "captured":
            continue
        if test[r["customer_id"].strip()]:
            print(f"  skip test customer {r['customer_id']} charge {k}")
            continue
        d = ts(r["captured_at"])
        if (d.year, d.month) != (year, month):
            continue
        v = usd(r, fx)
        rev += v
        n += 1
        print(f"  charge {k} {d:%Y-%m-%d %H:%M}Z {r['amount_minor']} {r['currency']} -> {v:.6f}")

    cb, m = Decimal(0), 0
    seen = set()
    for r in load(cb_p):
        cid = r["charge_id"].strip()
        if cid not in charges:
            sys.exit(f"CHARGEBACK {r['chargeback_id']} references unknown charge {cid}")
        c = charges[cid]
        if test[c["customer_id"].strip()]:
            print(f"  skip chargeback {r['chargeback_id']} (test customer)")
            continue
        d = ts(r["chargeback_at"])
        if (d.year, d.month) != (year, month):
            continue
        if cid in seen:
            print(f"  WARNING second chargeback on {cid} -- applied; decide")
        seen.add(cid)
        if c["status"].strip() != "captured":
            print(f"  WARNING chargeback {r['chargeback_id']} on non-captured charge {cid} ({c['status']}) -- applied; decide")
        v = usd(c, fx)
        cb += v + FEE
        m += 1
        print(f"  chargeback {r['chargeback_id']} {cid} {d:%Y-%m-%d}Z -{v:.6f} fee -{FEE}")

    q = lambda x: x.quantize(Decimal("0.01"), ROUND_HALF_UP)
    print(f"revenue={rev:.6f} chargebacks+fees={cb:.6f}")
    result = {"net_usd": float(q(rev - cb)), "transactions": n, "chargebacks": m}
    print(json.dumps(result))
    if out:
        with open(out, "w") as f:
            json.dump(result, f)
        assert json.load(open(out)) == result, "written file differs"
        print(f"wrote and re-read {out}")


main()
