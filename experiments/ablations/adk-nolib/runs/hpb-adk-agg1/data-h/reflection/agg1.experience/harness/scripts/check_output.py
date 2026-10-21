#!/usr/bin/env python3
"""Recompute the monthly net revenue figure from the workspace CSVs and check output/answer.json.

Usage: python3 scripts/check_output.py [--show]   (run from the workspace root)
  --show : print the recomputation breakdown and exit 0.
  default: Stop-hook mode. Exit 2 (reason on stderr) if output/answer.json is missing,
           not plain JSON, lacks the three keys, or disagrees with the recomputation.
           Exit 0 when it matches, or when the inputs are not in the expected shape
           (the check never blocks a run it cannot evaluate).
Policy encoded (this workspace's POLICY.md): captured only, month by UTC timestamp, minor units
(JPY whole yen; USD/EUR/INR /100), fx.csv usd_per_unit, is_test customers excluded everywhere,
chargeback reverses full original charge + 15.00 fee in the month of chargeback_at, round last.
"""
import csv, json, os, sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

MONTH = (2026, 9)
FEE = Decimal("15.00")
ZERO_DEC = {"JPY"}


def rows(name):
    with open(name, newline="") as f:
        return list(csv.DictReader(f))


def utc(ts):
    return datetime.fromisoformat(ts.strip().replace("Z", "+00:00")).astimezone(timezone.utc)


def compute():
    fx = {r["currency"]: Decimal(r["usd_per_unit"]) for r in rows("fx.csv")}
    test = {r["customer_id"] for r in rows("customers.csv") if r["is_test"].strip().lower() == "true"}
    charges = {r["charge_id"]: r for r in rows("charges.csv")}

    def usd(c):
        amt = Decimal(c["amount_minor"])
        if c["currency"] not in ZERO_DEC:
            amt = amt / 100
        return amt * fx[c["currency"]]

    def in_month(ts):
        d = utc(ts)
        return (d.year, d.month) == MONTH

    log, gross, n_tx = [], Decimal(0), 0
    for cid, c in charges.items():
        if c["status"].strip() == "captured" and c["customer_id"] not in test and in_month(c["captured_at"]):
            gross += usd(c); n_tx += 1
            log.append(f"  rev  {cid} {c['customer_id']} {c['currency']} {c['amount_minor']} -> {usd(c):.4f}")
    rev_cb, n_cb = Decimal(0), 0
    for r in rows("chargebacks.csv"):
        c = charges.get(r["charge_id"])
        if c is None:
            log.append(f"  WARN {r['chargeback_id']}: charge {r['charge_id']} not in charges.csv")
            continue
        if c["customer_id"] in test or not in_month(r["chargeback_at"]):
            continue
        rev_cb += usd(c); n_cb += 1
        log.append(f"  cb   {r['chargeback_id']} {r['charge_id']} {c['customer_id']} -> -{usd(c):.4f} (status {c['status']})")
    net = (gross - rev_cb - FEE * n_cb).quantize(Decimal("0.01"), ROUND_HALF_UP)
    log.append(f"  gross={gross:.4f} reversed={rev_cb:.4f} fees={FEE * n_cb}")
    return net, n_tx, n_cb, log


def main():
    show = "--show" in sys.argv
    try:
        net, n_tx, n_cb, log = compute()
    except Exception as e:  # inputs not as expected: do not block
        print(f"check_output: cannot recompute ({e!r})", file=sys.stderr)
        return 0
    if show:
        print("\n".join(log)); print(json.dumps({"net_usd": float(net), "transactions": n_tx, "chargebacks": n_cb}))
        return 0
    path = os.path.join("output", "answer.json")
    exp = {"net_usd": float(net), "transactions": n_tx, "chargebacks": n_cb}
    try:
        got = json.load(open(path))
        assert isinstance(got, dict)
    except Exception as e:
        print(f"output/answer.json is missing or not plain valid JSON ({e}). Write the raw object, "
              f"with no backslash-escaped quotes, e.g. {json.dumps(exp)}", file=sys.stderr)
        return 2
    bad = [k for k in exp if not isinstance(got.get(k), (int, float)) or isinstance(got.get(k), bool)]
    if bad:
        print(f"answer.json keys missing or non-numeric: {bad}", file=sys.stderr); return 2
    if abs(got["net_usd"] - exp["net_usd"]) > 0.005 or got["transactions"] != n_tx or got["chargebacks"] != n_cb:
        print("answer.json disagrees with a scripted recomputation from the CSVs under POLICY.md.\n"
              f"You wrote {got}; recomputed {exp}.\nBreakdown:\n" + "\n".join(log) +
              "\nFind which rows or rule differ from your working, fix it, and rewrite output/answer.json. "
              "If you can show the script misreads POLICY.md, keep your value and say why.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
