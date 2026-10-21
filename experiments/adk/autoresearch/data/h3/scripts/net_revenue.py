#!/usr/bin/env python3
"""Net revenue in USD from a messy transaction export.
Usage: python3 scripts/net_revenue.py TXN_CSV FX_CSV YYYY-MM [STATUS] [--write output/answer.json]
Handles: quoted fields with commas, thousands separators, (123.45) negatives, currency symbols,
mixed date formats, status case/whitespace, duplicate txn_id rows (counted once), FX lookup.
Prints every included row plus every excluded row with the reason, so you can eyeball it."""
import csv, sys, json, re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

FMTS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%b-%Y", "%d %b %Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]

def pdate(s):
    s = s.strip()
    for f in FMTS:
        try: return datetime.strptime(s, f)
        except ValueError: pass
    raise ValueError("unparsed date: %r" % s)

def pamt(s):
    s = s.replace("\u00a0", " ").strip(); neg = False
    if s.startswith("(") and s.endswith(")"): neg, s = True, s[1:-1]
    if s.endswith("-"): neg, s = True, s[:-1]
    if s.startswith("-(") and s.endswith(")"): s = s[2:-1]; neg = False; s = "-" + s
    s = re.sub(r"[^\d.\-+]", "", s.replace(",", ""))
    v = Decimal(s)
    return -v if neg else v

def main():
    a = [x for x in sys.argv[1:]]
    out = None
    if "--write" in a:
        i = a.index("--write"); out = a[i + 1]; del a[i:i + 2]
    txn, fxf, month = a[0], a[1], a[2]
    status = (a[3] if len(a) > 3 else "SETTLED").upper()
    y, m = map(int, month.split("-"))
    fx = {r["currency"].strip().upper(): Decimal(r["usd_per_unit"].strip()) for r in csv.DictReader(open(fxf, newline=""))}
    seen, total, n = {}, Decimal(0), 0
    for r in csv.DictReader(open(txn, newline="")):
        r = {k.strip(): (v or "").strip() for k, v in r.items()}
        tid = r["txn_id"]
        if tid in seen:
            if seen[tid] != r: print("DUP-DIFFERENT", tid, seen[tid], r)
            else: print("skip duplicate", tid)
            continue
        seen[tid] = r
        d = pdate(r["date"])
        if re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", r["date"]) and int(r["date"].split("/")[0]) <= 12 and int(r["date"].split("/")[1]) <= 12:
            print("WARNING ambiguous d/m date", tid, r["date"])
        if r["status"].upper() != status or (d.year, d.month) != (y, m):
            print("excluded", tid, r["date"], r["status"]); continue
        amt, cur = pamt(r["amount"]), r["currency"].upper()
        if cur not in fx:
            print("WARNING no FX rate for", cur, "in", tid, "- skipped; resolve manually"); continue
        usd = amt * fx[cur]
        total += usd; n += 1
        print("include", tid, d.date(), amt, cur, "->", usd)
    net = float(total.quantize(Decimal("0.01"), ROUND_HALF_UP))
    res = {"net_usd": net, "transactions": n}
    print(json.dumps(res))
    if out:
        json.dump(res, open(out, "w"), indent=2); print("wrote", out)

main()
