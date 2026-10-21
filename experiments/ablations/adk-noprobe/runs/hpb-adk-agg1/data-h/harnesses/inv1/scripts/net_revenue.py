#!/usr/bin/env python3
"""Monthly net revenue in USD from charges + chargebacks + customers + fx exports.

Usage (from the workspace root):
  python3 scripts/net_revenue.py YYYY-MM output/answer.json --fee <flat chargeback fee from POLICY.md>
Optional flags: --charges F --chargebacks F --customers F --fx F
Defaults: charges.csv chargebacks.csv customers.csv fx.csv

Rules (as read from POLICY.md; verify against its wording): recognise status == captured by captured_at
converted to UTC; amount_minor / 10**exp (JPY exp 0, others 2) * usd_per_unit;
exclude is_test customers everywhere (charges AND chargebacks); a chargeback
reverses the full original charge plus a flat fee, booked in the UTC month of
chargeback_at whatever the charge month; round only the final figure.
Output keys: net_usd, transactions (recognised charges, chargebacked or not),
chargebacks (booked in month). Stdlib only. Re-reads the file; exits 1 on bad input.
"""
import argparse, csv, json, sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

EXP = {"JPY": 0, "KRW": 0, "VND": 0}  # zero-decimal currencies; all others 2


def ts_utc(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    d = datetime.fromisoformat(s)
    if d.tzinfo is None:
        sys.exit(f"timestamp without timezone: {s!r}")
    return d.astimezone(timezone.utc)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("month")
    p.add_argument("out", nargs="?", default="output/answer.json")
    p.add_argument("--charges", default="charges.csv")
    p.add_argument("--chargebacks", default="chargebacks.csv")
    p.add_argument("--customers", default="customers.csv")
    p.add_argument("--fx", default="fx.csv")
    p.add_argument("--fee", required=True)
    a = p.parse_args()
    y, m = map(int, a.month.split("-"))
    fee = Decimal(a.fee)

    rd = lambda f: list(csv.DictReader(open(f, newline="")))
    fx = {r["currency"].strip().upper(): Decimal(r["usd_per_unit"]) for r in rd(a.fx)}
    test = {r["customer_id"].strip() for r in rd(a.customers) if r["is_test"].strip().lower() == "true"}
    print("test customers:", sorted(test))

    def usd(r):
        c = r["currency"].strip().upper()
        if c not in fx:
            sys.exit(f"no fx rate for {c!r}")
        return Decimal(r["amount_minor"].strip()) / (Decimal(10) ** EXP.get(c, 2)) * fx[c]

    charges = {}
    for r in rd(a.charges):
        cid = r["charge_id"].strip()
        if cid in charges:
            sys.exit(f"duplicate charge_id {cid}: decide explicitly")
        charges[cid] = r

    total, n = Decimal(0), 0
    for cid, r in charges.items():
        if r["status"].strip().lower() != "captured" or r["customer_id"].strip() in test:
            continue
        d = ts_utc(r["captured_at"])
        if (d.year, d.month) == (y, m):
            total += usd(r)
            n += 1
            print(f"rev {cid} {r['currency']} {r['amount_minor']} utc={d:%Y-%m-%d %H:%M} usd={usd(r):.4f}")

    k, seen = 0, set()
    for r in rd(a.chargebacks):
        cid = r["charge_id"].strip()
        if cid not in charges:
            sys.exit(f"chargeback {r['chargeback_id']} references unknown charge {cid}")
        ch = charges[cid]
        d = ts_utc(r["chargeback_at"])
        if ch["customer_id"].strip() in test:
            print(f"skip cb {r['chargeback_id']} {cid}: test customer")
            continue
        if (d.year, d.month) != (y, m):
            continue
        if cid in seen:
            sys.exit(f"charge {cid} charged back twice in month: decide explicitly")
        seen.add(cid)
        if ch["status"].strip().lower() != "captured":
            print(f"WARNING cb {r['chargeback_id']} on non-captured charge {cid} ({ch['status']}); reversed anyway")
        total -= usd(ch) + fee
        k += 1
        print(f"cb {r['chargeback_id']} {cid} utc={d:%Y-%m-%d %H:%M} reverses {usd(ch):.4f} + fee {fee}")

    net = float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    with open(a.out, "w") as f:
        json.dump({"net_usd": net, "transactions": n, "chargebacks": k}, f)
    back = json.load(open(a.out))
    assert set(back) == {"net_usd", "transactions", "chargebacks"}
    print(f"exact total {total}; wrote {a.out}: {back}")


if __name__ == "__main__":
    main()
