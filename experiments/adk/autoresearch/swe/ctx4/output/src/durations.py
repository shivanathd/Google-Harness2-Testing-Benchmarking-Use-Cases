import re


def parse_duration(text: str) -> int:
    """Convert a duration such as "1h30m", "45s" or "2h 5m 10s" to seconds.

    Units are h, m and s, case-insensitive; whitespace around and between parts is
    allowed. Each unit may appear at most once, in h-m-s order. Raise ValueError for
    empty input, unknown units, or text that is not a duration.
    """
    text = text.strip()
    if not text:
        raise ValueError("empty input")
    total = 0
    units = {'h': 3600, 'm': 60, 's': 1}
    parts = re.fullmatch(r"(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?", text, re.IGNORECASE)
    if not parts:
        raise ValueError("unknown units or invalid format")
    if parts.group(1):
        total += int(parts.group(1)) * units['h']
    if parts.group(2):
        total += int(parts.group(2)) * units['m']
    if parts.group(3):
        total += int(parts.group(3)) * units['s']
    return total