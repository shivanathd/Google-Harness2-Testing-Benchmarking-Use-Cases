import re


def parse_duration(text: str) -> int:
    """Convert a duration such as "1h30m", "45s" or "2h 5m 10s" to seconds.

    Units are h, m and s, case-insensitive; whitespace around and between parts is
    allowed. Each unit may appear at most once, in h-m-s order. Raise ValueError for
    empty input, unknown units, or text that is not a duration.
    """
    if not text.strip():
        raise ValueError("Empty input")
    total = 0
    parts = re.findall(r"\s*(\d+)\s*(h|m|s)\s*", text, flags=re.IGNORECASE)
    if not parts:
        raise ValueError("Unknown units or invalid format")
    seen = set()
    for num, unit in parts:
        if unit in seen:
            raise ValueError("Each unit may appear at most once")
        seen.add(unit)
        total += int(num) * (3600 if unit == "h" else 60 if unit == "m" else 1)
    return total