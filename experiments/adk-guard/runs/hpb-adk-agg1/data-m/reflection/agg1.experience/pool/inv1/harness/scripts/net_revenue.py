#!/usr/bin/env python3
"""Monthly net revenue in USD from transactions + refunds + daily fx exports.

Usage (run from the workspace root; the files are listed by list_files "."):
  python3 scripts/net_revenue.py --month 2026-09 [--tx transactions.csv]
      [--refunds refunds.csv] [--fx fx_daily.csv] [--status SETTLED]
      [--out output/answer.json] [--dry]

Rules: a txn_id counts once (first row kept, conflicting duplicates reported);
a transaction is recognised if status matches and settled_on is in the month,
at that day's usd_per_unit; a refund reduces revenue in the month of
refunded_on, in the ORIGINAL transaction's currency, at the refund day's rate.
Stdlib only. Handles thousands separators ("2,845.66"), "(x)" negatives,
currency symbols, several date formats. Rounds once at the end.
Writes {"net_usd","transactions","refunds"} and prints a diagnostic to stderr.
Exit 1 with a message on unparseable value, missing fx rate (no silent
carry-forward), zero/invalid rate, refund for unknown txn, missing column.
"""
import argparse, csv, json, os, re, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

DATE_FORMATS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%Y/%m/%d", "%m/%d/%Y", "%d %b %Y", "%Y-%m-%dT%H:%M:%S"]


def parse_amount(s):
    t = s.strip()
    neg = t.startswith("(") and t.endswith(")")
    t = re.sub(r"[()\s,$€£₹]", "", t)
    if t.startswith("-"):
        neg, t = True, t[1:]
    try:
        v = Decimal(t)
    except InvalidOperation:
        sys.exit("unparseable amount %r" % s)
    return -v if neg else v


def parse_date(s, what):
    t = s.strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(t, f).date()
        except ValueError:
            pass
    sys.exit("unparseable %s %r" % (what, s))


def read(path, cols):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]
    for c in cols:
        if not rows or c not in rows[0]:
            sys.exit("missing column %s in %s" % (c, path))
    return rows


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--tx", default="transactions.csv")
    a.add_argument("--refunds", default="refunds.csv")
    a.add_argument("--fx", default="fx_daily.csv")
    a.add_argument("--month", required=True, help="YYYY-MM, from the task")
    a.add_argument("--status", default="SETTLED")
    a.add_argument("--out", default="output/answer.json")
    a.add_argument("--dry", action="store_true")
    o = a.parse_args()
    year, mon = map(int, o.month.split("-"))

    fx = {}
    for r in read(o.fx, ("date", "currency", "usd_per_unit")):
        fx[(parse_date(r["date"], "fx date"), r["currency"].upper())] = Decimal(r["usd_per_unit"])

    def rate(d, cur, what):
        v = fx.get((d, cur))
        if v is None:
            sys.exit("no fx rate for %s on %s (%s)" % (cur, d, what))
        if v <= 0:
            sys.exit("fx rate for %s on %s is %s (%s): invalid" % (cur, d, v, what))
        return v

    txs = read(o.tx, ("txn_id", "settled_on", "amount", "currency", "status"))
    seen, dupes, conflicts, total, n, by_cur = {}, 0, [], Decimal(0), 0, {}
    for r in txs:
        tid = r["txn_id"]
        key = tuple(r[c] for c in ("settled_on", "amount", "currency", "status"))
        if tid in seen:
            dupes += 1
            if seen[tid] != key:
                conflicts.append(tid)
            continue
        seen[tid] = key
        r["currency"] = r["currency"].upper()
        if r["status"].upper() != o.status.upper() or not r["settled_on"]:
            continue
        d = parse_date(r["settled_on"], "settled_on")
        if (d.year, d.month) != (year, mon):
            continue
        usd = parse_amount(r["amount"]) * rate(d, r["currency"], "txn " + tid)
        total += usd
        n += 1
        by_cur[r["currency"]] = by_cur.get(r["currency"], Decimal(0)) + usd
    cur_of = {r["txn_id"]: r["currency"].upper() for r in txs}

    refs = read(o.refunds, ("refund_id", "txn_id", "refunded_on", "amount"))
    seen_r, rdupes, rtotal, rn = set(), 0, Decimal(0), 0
    for r in refs:
        if r["refund_id"] in seen_r:
            rdupes += 1
            continue
        seen_r.add(r["refund_id"])
        d = parse_date(r["refunded_on"], "refunded_on")
        if (d.year, d.month) != (year, mon):
            continue
        if r["txn_id"] not in cur_of:
            sys.exit("refund %s references unknown txn_id %s" % (r["refund_id"], r["txn_id"]))
        rtotal += parse_amount(r["amount"]) * rate(d, cur_of[r["txn_id"]], "refund " + r["refund_id"])
        rn += 1

    q = lambda x: x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    net = float(q(total - rtotal))
    print("tx_rows=%d unique_txn=%d dup_rows_dropped=%d conflicting_dups=%s recognised=%d gross_usd=%s by_currency=%s | "
          "refund_rows=%d dup_refund_ids=%d refunds_applied=%d refunds_usd=%s | net_usd=%.2f"
          % (len(txs), len(seen), dupes, conflicts or "none", n, q(total),
             {k: str(q(v)) for k, v in sorted(by_cur.items())}, len(refs), rdupes, rn, q(rtotal), net),
          file=sys.stderr)
    ans = {"net_usd": net, "transactions": n, "refunds": rn}
    if not o.dry:
        os.makedirs(os.path.dirname(o.out) or ".", exist_ok=True)
        with open(o.out, "w") as f:
            json.dump(ans, f)
    print(json.dumps(ans))


if __name__ == "__main__":
    main()
