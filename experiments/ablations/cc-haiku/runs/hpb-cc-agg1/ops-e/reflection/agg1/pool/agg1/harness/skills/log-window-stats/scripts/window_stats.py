"""Count events of one level inside a UTC window of a mixed-offset log.

Usage: python3 -I skills/log-window-stats/scripts/window_stats.py <log> --start <ISO> --end <ISO> [--level ERROR]
--start is inclusive and --end is exclusive. Both need a UTC offset (Z or +hh:mm).
Only timestamped header lines are events; indented continuation lines (tracebacks) are not.
Prints one JSON object: count, users, top_code (None when tied), top_codes, codes, matches,
events_without_user, events_without_code, headers, continuation_lines, levels, unparsed.
"""
import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone

HEADER = re.compile(
    r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))\s+(\w+)\s+\[([^\]]+)\]\s+(.*)$'
)


def parse_ts(text):
    ts = datetime.fromisoformat(text.replace('Z', '+00:00'))
    if ts.tzinfo is None:
        raise SystemExit(f'timestamp needs a UTC offset: {text}')
    return ts.astimezone(timezone.utc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('log')
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--level', default='ERROR')
    args = ap.parse_args()
    start, end = parse_ts(args.start), parse_ts(args.end)

    levels = Counter()
    matches = []
    headers = continuation = 0
    unparsed = []
    with open(args.log, encoding='utf-8') as fh:
        for n, raw in enumerate(fh, 1):
            line = raw.rstrip('\n')
            if not line.strip():
                continue
            if line[0] in ' \t':
                continuation += 1
                continue
            m = HEADER.match(line)
            if not m:
                unparsed.append({'line': n, 'text': line})
                continue
            headers += 1
            level = m.group(2)
            levels[level] += 1
            ts = parse_ts(m.group(1))
            if level != args.level or not (start <= ts < end):
                continue
            user = re.search(r'\buser=(\S+)', m.group(4))
            code = re.search(r'\bcode=(\S+)', m.group(4))
            matches.append([n, ts.isoformat(), user and user.group(1), code and code.group(1)])

    codes = Counter(e[3] for e in matches if e[3])
    most = codes.most_common()
    top_count = most[0][1] if most else 0
    top_codes = sorted(code for code, k in codes.items() if k == top_count)
    result = {
        'window_utc': [start.isoformat(), end.isoformat()],
        'level': args.level,
        'count': len(matches),
        'users': len({e[2] for e in matches if e[2]}),
        'top_code': top_codes[0] if len(top_codes) == 1 else None,
        'top_codes': top_codes,
        'codes': dict(most),
        'matches': matches,
        'events_without_user': sum(1 for e in matches if not e[2]),
        'events_without_code': sum(1 for e in matches if not e[3]),
        'headers': headers,
        'continuation_lines': continuation,
        'levels': dict(levels),
        'unparsed': unparsed,
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
